"""Ядро публикации: Airtable → Zernio (grok_hook). Локально и Cloud Run."""

from __future__ import annotations

import json
import os
import random
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from publish_cleanup import assert_zernio_ok, cleanup_carousel_assets
from dropbox_client import ensure_shared_link, get_access_token
from http_client import http_json, urlopen
from publish_config import (
    load_runtime_env,
    pair_config,
    resolve_carousel_dropbox_path,
    zernio_api_key_for_platform,
    zernio_instagram_account_id,
    zernio_tiktok_account_id,
)
from worker_state import load_state, save_state

CLOUD_RUN_URL = os.environ.get(
    "CLOUD_RUN_RENDER_URL",
    "https://ai-carousel-renderer-861393245289.europe-west1.run.app/generate-carousel",
)
TRACKS_TABLE = os.environ.get("AIRTABLE_TRACKS_TABLE_ID", "tblfLD5ET7vvp1raT")
ZERNIO_URL = "https://zernio.com/api/v1/posts"
ZERNIO_TIMEOUT_SEC = int(os.environ.get("ZERNIO_TIMEOUT_SEC", "600"))
RENDER_TIMEOUT_SEC = int(os.environ.get("RENDER_TIMEOUT_SEC", "1200"))
POLL_INTERVAL_SEC = int(os.environ.get("RENDER_POLL_INTERVAL_SEC", "30"))
EXPECTED_IMAGE_SLIDES = int(os.environ.get("EXPECTED_IMAGE_SLIDES", "6"))
PUBLISH_MODE = os.environ.get("PUBLISH_MODE", "grok_hook").strip().lower()


def list_queue_records(env: dict[str, str], pair: dict) -> list[dict]:
    base = pair["airtable"]["base_id"]
    table = pair["airtable"]["table_id"]
    token = env["AIRTABLE_ACCESS_TOKEN"]
    url = f"https://api.airtable.com/v0/{base}/{table}?maxRecords=50"
    data = http_json("GET", url, headers={"Authorization": f"Bearer {token}"})
    return data.get("records", [])


def _published_state_key(accounts_pair_id: str) -> str:
    return "published" if accounts_pair_id == "pair1" else f"published_{accounts_pair_id}"


def _load_published_set(state: dict, accounts_pair_id: str) -> set[str]:
    key = _published_state_key(accounts_pair_id)
    raw = state.get(key, [])
    if isinstance(raw, list):
        return set(raw)
    return set()


def _ready_records(records: list[dict], state: dict, pair_id: str) -> list[dict]:
    published = _load_published_set(state, pair_id)
    failed_names = set(state.get("failed", {}).keys())
    return [
        r
        for r in records
        if r.get("fields", {}).get("Name")
        and r["fields"]["Name"] not in published
        and r["fields"]["Name"] not in failed_names
    ]


def queue_next_hint(
    env: dict[str, str],
    pair_id: str,
    state: dict,
    *,
    exclude_name: str | None = None,
) -> tuple[str | None, int]:
    """Return (next carousel name, ready count) after optional exclude."""
    pair = pair_config(pair_id)
    ready = _ready_records(list_queue_records(env, pair), state, pair_id)
    if exclude_name:
        ready = [r for r in ready if r.get("fields", {}).get("Name") != exclude_name]
    ready.sort(key=lambda r: r.get("fields", {}).get("Name", ""))
    if not ready:
        return None, 0
    name = ready[0].get("fields", {}).get("Name")
    return name, len(ready)


def get_queue_summary(env: dict[str, str] | None = None) -> dict[str, Any]:
    """Статус очереди: Airtable, published, failed, ready."""
    env = env or load_runtime_env()
    token = get_access_token(env)
    state = load_state(token if os.environ.get("WORKER_STATE_BACKEND") == "dropbox" else None)

    pairs_summary: dict[str, dict[str, int]] = {}
    for pair_id in ("pair1", "pair2", "pair3"):
        pair = pair_config(pair_id)
        records = list_queue_records(env, pair)
        published = _load_published_set(state, pair_id)
        failed = {
            name
            for name, meta in (state.get("failed") or {}).items()
            if isinstance(meta, dict)
        }
        ready = _ready_records(records, state, pair_id)
        pairs_summary[pair_id] = {
            "airtable_total": len(records),
            "published": len(published),
            "failed": len([r for r in records if r.get("fields", {}).get("Name") in failed]),
            "ready": len(ready),
        }

    return {
        "at": datetime.now(timezone.utc).isoformat(),
        "pairs": pairs_summary,
        "worker_state_path": str(state.get("_path", "publish-memory/worker-state.json")),
    }


def pick_track(env: dict[str, str], pair: dict) -> dict:
    base = pair["airtable"]["base_id"]
    token = env["AIRTABLE_ACCESS_TOKEN"]
    formula = urllib.parse.quote("{Active}=1")
    url = f"https://api.airtable.com/v0/{base}/{TRACKS_TABLE}?filterByFormula={formula}"
    data = http_json("GET", url, headers={"Authorization": f"Bearer {token}"})
    records = data.get("records", [])
    if not records:
        raise RuntimeError("No active tracks in Airtable")
    return random.choice(records).get("fields", {})


def _slide_sort_key(path: str) -> int:
    stem = Path(path).stem.lower()
    match = re.search(r"(\d+)", stem)
    return int(match.group(1)) if match else 0


def dropbox_folder_candidates(pair: dict, fields: dict, name: str) -> list[str]:
    """Кандидаты путей: Pair1/Pair2 → legacy /Content_Plan/{Name}."""
    primary = resolve_carousel_dropbox_path(pair, fields, name)
    root = os.environ.get("DROPBOX_CONTENT_PLAN_ROOT", "/Content_Plan").rstrip("/")
    candidates = [primary, f"{root}/{name}"]
    pair_root = pair.get("dropbox_root")
    if pair_root:
        candidates.append(f"{str(pair_root).rstrip('/')}/{name}")
    seen: set[str] = set()
    out: list[str] = []
    for path in candidates:
        norm = path if path.startswith("/") else f"/{path}"
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
    return out


def find_carousel_dropbox_folder(token: str, pair: dict, fields: dict, name: str) -> str:
    """Первая существующая папка с файлами слайдов."""
    last_err: Exception | None = None
    for path in dropbox_folder_candidates(pair, fields, name):
        try:
            entries = list_folder_entries(token, path)
            if any(
                e.get(".tag") == "file"
                and e.get("name", "").lower().startswith("slide-")
                and e.get("name", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".mp4"))
                for e in entries
            ):
                return path
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
    raise RuntimeError(f"No Dropbox carousel folder for {name}: {last_err}")


def list_folder_entries(token: str, dropbox_folder: str) -> list[dict]:
    last_err: Exception | None = None
    for attempt in range(5):
        req = urllib.request.Request(
            "https://api.dropboxapi.com/2/files/list_folder",
            data=json.dumps({"path": dropbox_folder, "recursive": False}).encode(),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=60, retries=2) as resp:
                return json.loads(resp.read().decode()).get("entries", [])
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"Dropbox list_folder failed for {dropbox_folder}: {last_err}") from last_err


def list_media_bundle(token: str, dropbox_folder: str) -> dict[str, Any]:
    entries = list_folder_entries(token, dropbox_folder)
    images = sorted(
        (
            e["path_lower"]
            for e in entries
            if e.get(".tag") == "file"
            and e.get("name", "").lower().startswith("slide-")
            and e.get("name", "").lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
        ),
        key=_slide_sort_key,
    )
    videos = sorted(
        (
            e["path_lower"]
            for e in entries
            if e.get(".tag") == "file"
            and e.get("name", "").lower().startswith("slide-")
            and e.get("name", "").lower().endswith(".mp4")
        ),
        key=_slide_sort_key,
    )
    hook_video = next(
        (p for p in videos if Path(p).stem.lower() in ("slide-01", "slide-1")),
        videos[0] if videos else None,
    )

    count = len(images)
    if count < 2:
        raise RuntimeError(f"Too few image slides in {dropbox_folder}: {count}")
    # Допустимые размеры: 6, 7 (legacy), 9 (3x3 grid)
    allowed = {6, 7, 9}
    if count not in allowed:
        raise RuntimeError(f"Unexpected slide count in {dropbox_folder}: expected 6/7/9, got {count}")
    expected = count
    return {
        "folder": dropbox_folder,
        "images": images,
        "hook_video": hook_video,
        "expected": expected,
    }


IG_MIN_ASPECT = 0.75
IG_MAX_ASPECT = 1.91


def _png_dimensions_from_bytes(header: bytes) -> tuple[int, int]:
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError("Not a PNG file")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def _dropbox_png_dimensions(token: str, path: str) -> tuple[int, int]:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps({"path": path}),
            "Range": "bytes=0-23",
        },
        method="POST",
    )
    with urlopen(req, timeout=60) as resp:
        return _png_dimensions_from_bytes(resp.read(24))


def validate_instagram_image_slides(token: str, image_paths: list[str]) -> None:
    """Fail fast when PNG aspect ratio is outside Instagram feed limits."""
    for path in image_paths:
        width, height = _dropbox_png_dimensions(token, path)
        if height <= 0:
            raise RuntimeError(f"Invalid image dimensions for {Path(path).name}: {width}x{height}")
        ratio = width / height
        if ratio < IG_MIN_ASPECT or ratio > IG_MAX_ASPECT:
            max_h = int(width / IG_MIN_ASPECT)
            raise RuntimeError(
                f"Instagram aspect ratio for {Path(path).name}: {width}x{height} "
                f"({ratio:.3f}:1). Allowed {IG_MIN_ASPECT:.2f}–{IG_MAX_ASPECT:.2f}. "
                f"Max height for {width}px width is {max_h}px (crop to 4:5). "
                "Re-export from factory."
            )


    """Instagram photo carousel — все PNG (нет hook-видео)."""
    return {
        "content": (fields.get("Описание карусели") or "")[:2200],
        "mediaItems": [{"type": "image", "url": u} for u in image_urls],
        "platforms": [{"platform": "instagram", "accountId": account_id}],
        "publishNow": True,
    }


def build_instagram_images_payload(fields: dict, image_urls: list[str], account_id: str) -> dict:
    """Deprecated alias — keep for compatibility."""
    return build_instagram_photo_payload(fields, image_urls, account_id)


def build_instagram_mixed_payload(
    fields: dict, hook_video_url: str, image_urls: list[str], account_id: str
) -> dict:
    """Instagram: video hook + остальные PNG."""
    rest = image_urls[1:] if len(image_urls) > 1 else []
    media: list[dict[str, str]] = [{"type": "video", "url": hook_video_url}]
    media.extend({"type": "image", "url": u} for u in rest)
    return {
        "content": (fields.get("Описание карусели") or "")[:2200],
        "mediaItems": media,
        "platforms": [{"platform": "instagram", "accountId": account_id}],
        "publishNow": True,
    }


def build_instagram_grok_payload(
    fields: dict, hook_video_url: str, image_urls: list[str], account_id: str
) -> dict:
    """Deprecated alias — keep for compatibility."""
    return build_instagram_mixed_payload(fields, hook_video_url, image_urls, account_id)


def build_tiktok_payload(fields: dict, image_urls: list[str], account_id: str) -> dict:
    return {
        "content": (fields.get("TikTok заголовок") or "Карусель")[:90],
        "mediaItems": [{"type": "image", "url": u} for u in image_urls],
        "platforms": [{"platform": "tiktok", "accountId": account_id}],
        "tiktokSettings": {
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "allow_comment": True,
            "media_type": "photo",
            "photo_cover_index": 0,
            "description": (fields.get("TikTok описание") or fields.get("Описание карусели") or "")[:4000],
            "auto_add_music": True,
            "content_preview_confirmed": True,
            "express_consent_given": True,
        },
        "publishNow": True,
    }


def post_zernio(api_key: str, body: dict | str, *, dry_run: bool = False, retries: int = 1) -> dict:
    body_json = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
    if dry_run:
        return {"dry_run": True, "platforms": json.loads(body_json).get("platforms")}
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return http_json(
                "POST",
                ZERNIO_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body=body_json,
                timeout=ZERNIO_TIMEOUT_SEC,
            )
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            text = str(exc).lower()
            retryable = any(
                s in text
                for s in ("429", "500", "502", "503", "504", "rate limit", "timeout")
            )
            if attempt < retries and retryable:
                time.sleep(60)
                continue
            break
    raise last_exc or RuntimeError("post_zernio failed")


def _is_dropbox_missing(exc: BaseException) -> bool:
    text = str(exc).lower()
    return "409" in text or "404" in text or "not_found" in text


def dropbox_download_json(token: str, path: str) -> dict | None:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        headers={"Authorization": f"Bearer {token}", "Dropbox-API-Arg": json.dumps({"path": path})},
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError:
        return None
    except RuntimeError as exc:
        if _is_dropbox_missing(exc):
            return None
        raise


def count_ready_videos(token: str, name: str) -> int:
    path = f"/Ready_Carousel/{name}"
    req = urllib.request.Request(
        "https://api.dropboxapi.com/2/files/list_folder",
        data=json.dumps({"path": path, "recursive": True}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            entries = json.loads(resp.read().decode()).get("entries", [])
    except urllib.error.HTTPError:
        return 0
    except RuntimeError as exc:
        if _is_dropbox_missing(exc):
            return 0
        raise
    return len([e for e in entries if e.get("name", "").endswith(".mp4")])


def delete_dropbox_folder(token: str, path: str, *, optional: bool = False) -> bool:
    req = urllib.request.Request(
        "https://api.dropboxapi.com/2/files/delete_v2",
        data=json.dumps({"path": path}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            resp.read()
        return True
    except urllib.error.HTTPError as e:
        if e.code in (409, 404):
            return optional
        if optional:
            return False
        raise
    except Exception:
        if optional:
            return False
        raise


def build_render_payload(fields: dict, slide_paths: list[str], track: dict) -> dict:
    name = fields["Name"]
    return {
        "carousel_name": name,
        "folder_name": name,
        "job_id": name,
        "instagram_caption": fields.get("Описание карусели", ""),
        "tiktok_title": fields.get("TikTok заголовок", ""),
        "tiktok_description": fields.get("TikTok описание", ""),
        "dropbox_image_paths": slide_paths,
        "dropbox_audio_path": track.get("Audio Path", ""),
        "audio_start": track.get("Audio Start", 0),
        "audio_end": track.get("Audio End", 30),
        "reuse_audio_segment": bool(track.get("Reuse Audio Segment")),
        "output_folder": "/Ready_Carousel",
    }


def wait_for_render(
    env: dict[str, str],
    payload: dict,
    token: str,
    name: str,
    pair: dict,
    *,
    expected_count: int | None = None,
) -> dict:
    expected_count = expected_count or len(payload.get("dropbox_image_paths") or []) or 7
    result_box: dict = {}
    error_box: dict = {}

    def _run() -> None:
        try:
            api_key = env.get("CLOUD_RUN_API_KEY", "")
            if not api_key:
                raise RuntimeError("CLOUD_RUN_API_KEY is not set")
            result_box["data"] = http_json(
                "POST",
                CLOUD_RUN_URL,
                headers={"X-API-Key": api_key, "Accept": "application/json"},
                body=payload,
                timeout=RENDER_TIMEOUT_SEC,
            )
        except Exception as exc:  # noqa: BLE001
            error_box["error"] = exc

    threading.Thread(target=_run, daemon=True).start()
    deadline = time.time() + RENDER_TIMEOUT_SEC
    manifest_path = f"/Ready_Carousel/{name}/render-result.json"

    while time.time() < deadline:
        if "data" in result_box:
            data = result_box["data"]
            if data.get("status") == "success":
                return data
            raise RuntimeError(f"Cloud Run error: {json.dumps(data, ensure_ascii=False)[:1500]}")

        manifest = dropbox_download_json(token, manifest_path)
        if manifest and manifest.get("slide_count") == expected_count:
            break

        time.sleep(POLL_INTERVAL_SEC)

    if "data" in result_box and result_box["data"].get("status") == "success":
        return result_box["data"]

    manifest = dropbox_download_json(token, manifest_path)
    if not manifest or manifest.get("slide_count") != expected_count:
        err = error_box.get("error", "timeout")
        raise RuntimeError(
            f"Incomplete render for {name}: {count_ready_videos(token, name)}/{expected_count} mp4 — {err}"
        )

    videos = manifest.get("videos", [])
    ig_items = [{"type": "video", "url": v["url"]} for v in videos if v.get("url")]
    image_urls = [ensure_shared_link(p, token) for p in payload["dropbox_image_paths"]]
    fields = {
        "TikTok заголовок": payload.get("tiktok_title", ""),
        "TikTok описание": payload.get("tiktok_description", ""),
        "Описание карусели": payload.get("instagram_caption", ""),
    }
    tt_payload = build_tiktok_payload(fields, image_urls, zernio_tiktok_account_id(pair, env))
    ig_payload = {
        "content": (payload.get("instagram_caption") or "")[:2200],
        "mediaItems": ig_items,
        "platforms": [{"platform": "instagram", "accountId": zernio_instagram_account_id(pair, env)}],
        "publishNow": True,
    }
    return {
        "status": "success",
        "instagram_zernio_post_json": json.dumps(ig_payload, ensure_ascii=False),
        "tiktok_zernio_post_json": json.dumps(tt_payload, ensure_ascii=False),
        "recovered_from_manifest": True,
    }


def process_record(
    env: dict[str, str],
    accounts_pair: dict,
    queue_pair: dict,
    rec: dict,
    *,
    dry_run: bool,
    skip_cleanup: bool,
    tiktok_only: bool,
) -> dict[str, Any]:
    fields = rec.get("fields", {})
    name = fields.get("Name")
    if not name:
        raise RuntimeError("Record missing Name")

    dropbox_token = get_access_token(env)
    dropbox_folder = find_carousel_dropbox_folder(dropbox_token, queue_pair, fields, name)
    ig_key = zernio_api_key_for_platform(env, accounts_pair, "instagram")
    tt_key = zernio_api_key_for_platform(env, accounts_pair, "tiktok")
    ig_acc = zernio_instagram_account_id(accounts_pair, env)
    tt_acc = zernio_tiktok_account_id(accounts_pair, env)
    media = list_media_bundle(dropbox_token, dropbox_folder)
    slide_paths: list[str] = media["images"]
    hook_video: str | None = media["hook_video"]
    has_video = bool(hook_video)

    ig_image_paths = slide_paths[1:] if has_video else slide_paths
    validate_instagram_image_slides(dropbox_token, ig_image_paths)

    if dry_run:
        mode = "mixed" if has_video else "photo_carousel"
        return {
            "dry_run": True,
            "name": name,
            "pair": accounts_pair.get("id"),
            "queue_pair": queue_pair.get("id"),
            "dropbox_folder": dropbox_folder,
            "zernio_instagram_account_id": ig_acc,
            "zernio_tiktok_account_id": tt_acc,
            "mode": mode,
            "images": len(slide_paths),
            "hook_video": hook_video,
        }

    image_urls = [ensure_shared_link(p, dropbox_token) for p in slide_paths]
    if tiktok_only:
        tt_payload = build_tiktok_payload(fields, image_urls, tt_acc)
        result: dict[str, Any] = {
            "name": name,
            "tiktok": post_zernio(tt_key, tt_payload),
            "mode": "tiktok_only",
        }
    elif has_video:
        assert hook_video is not None
        video_url = ensure_shared_link(hook_video, dropbox_token)
        ig_payload = build_instagram_mixed_payload(fields, video_url, image_urls, ig_acc)
        tt_payload = build_tiktok_payload(fields, image_urls, tt_acc)
        result = {
            "name": name,
            "airtable_id": rec["id"],
            "mode": "mixed",
            "instagram": post_zernio(ig_key, ig_payload),
            "tiktok": post_zernio(tt_key, tt_payload),
        }
    else:
        ig_payload = build_instagram_photo_payload(fields, image_urls, ig_acc)
        tt_payload = build_tiktok_payload(fields, image_urls, tt_acc)
        result = {
            "name": name,
            "airtable_id": rec["id"],
            "mode": "photo_carousel",
            "instagram": post_zernio(ig_key, ig_payload),
            "tiktok": post_zernio(tt_key, tt_payload),
        }

    if not dry_run:
        try:
            from max_notify import notify_from_publish_result

            summary = get_queue_summary(env)
            remaining = {pid: summary["pairs"][pid]["ready"] for pid in ("pair1", "pair2", "pair3")}
            notify_state = load_state(
                dropbox_token if os.environ.get("WORKER_STATE_BACKEND") == "dropbox" else None
            )
            next_name, next_count = queue_next_hint(
                env, accounts_pair.get("id", "pair1"), notify_state, exclude_name=name
            )
            notify_from_publish_result(
                accounts_pair.get("id", "pair1"),
                accounts_pair.get("label", "pair"),
                name,
                result,
                queue_remaining=remaining,
                next_folder=next_name,
                queue_ready=next_count,
            )
        except Exception as exc:  # noqa: BLE001
            if "max_error" not in result:
                result["max_error"] = str(exc)

    if not skip_cleanup:
        for label, key in (("instagram", "instagram"), ("tiktok", "tiktok")):
            if key in result:
                assert_zernio_ok(result[key], label)
        result["cleanup"] = cleanup_carousel_assets(
            env=env,
            queue_pair=queue_pair,
            record_id=rec["id"],
            dropbox_token=dropbox_token,
            dropbox_folder=dropbox_folder,
            carousel_name=name,
            delete_dropbox_folder=delete_dropbox_folder,
        )

    return result


def run_publish_batch(
    *,
    pair_id: str = "pair1",
    accounts_pair_id: str | None = None,
    queue_pair_id: str | None = None,
    limit: int = 1,
    name: str | None = None,
    dry_run: bool = False,
    skip_cleanup: bool = False,
    tiktok_only: bool = False,
    include_published: bool = False,
    retry_failed: bool = False,
) -> dict[str, Any]:
    env = load_runtime_env()
    accounts_pair_id = accounts_pair_id or pair_id
    queue_pair_id = queue_pair_id or pair_id
    accounts_pair = pair_config(accounts_pair_id)
    queue_pair = pair_config(queue_pair_id)
    dropbox_token = get_access_token(env)
    state = load_state(dropbox_token if os.environ.get("WORKER_STATE_BACKEND") == "dropbox" else None)
    published = _load_published_set(state, accounts_pair_id)
    pair1_published = _load_published_set(state, "pair1")
    records = list_queue_records(env, queue_pair)

    if name:
        records = [r for r in records if r.get("fields", {}).get("Name") == name]
    elif not include_published:
        failed_names = set() if retry_failed else set(state.get("failed", {}).keys())
        records = [
            r
            for r in records
            if r.get("fields", {}).get("Name") not in published
            and r.get("fields", {}).get("Name") not in failed_names
        ]
        if queue_pair_id == "pair1" and accounts_pair_id == "pair2":
            records = [
                r
                for r in records
                if r.get("fields", {}).get("Name") not in pair1_published
            ]

    records = sorted(records, key=lambda r: r.get("fields", {}).get("Name", ""))
    if not records:
        return {"status": "empty", "message": "Queue empty or all published", "results": []}

    results: list[dict] = []
    errors: list[dict] = []

    for rec in records[: max(1, limit)]:
        carousel_name = rec.get("fields", {}).get("Name", "")
        try:
            res = process_record(
                env,
                accounts_pair,
                queue_pair,
                rec,
                dry_run=dry_run,
                skip_cleanup=skip_cleanup,
                tiktok_only=tiktok_only,
            )
            if not dry_run:
                published.add(carousel_name)
                state[_published_state_key(accounts_pair_id)] = sorted(published)
                state.get("failed", {}).pop(carousel_name, None)
                state.setdefault("last_run", {})[carousel_name] = {
                    "at": datetime.now(timezone.utc).isoformat(),
                    "ok": True,
                }
            results.append(res)
        except Exception as exc:  # noqa: BLE001
            err_text = str(exc)
            state.setdefault("failed", {})[carousel_name] = {
                "at": datetime.now(timezone.utc).isoformat(),
                "error": err_text,
            }
            try:
                from publish_incidents import log_incident

                log_incident(
                    pair=accounts_pair_id,
                    stage="publish",
                    error=err_text,
                    carousel=carousel_name,
                    suggested_files=[
                        "scripts/lib/publish_engine.py",
                        "scripts/lib/publish_cleanup.py",
                        "scripts/lib/max_notify.py",
                    ],
                )
            except Exception:
                pass
            errors.append({"name": carousel_name, "error": err_text})

    if not dry_run:
        save_state(state, dropbox_token if os.environ.get("WORKER_STATE_BACKEND") == "dropbox" else None)

    if not results and not errors:
        status = "empty"
    elif results and not errors:
        status = "ok"
    elif results:
        status = "partial"
    else:
        status = "error"
    return {
        "status": status,
        "pair": accounts_pair_id,
        "queue_pair": queue_pair_id,
        "processed": len(results),
        "errors": errors,
        "results": results,
        "at": datetime.now(timezone.utc).isoformat(),
    }
