"""MAX Bot notifications after publish."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dropbox_client import get_access_token, upload_file
from max_http import send_message as max_send_message
from publish_config import MEMORY, load_runtime_env

LOG_PATH = MEMORY / "output" / "max-notify.log"
DROPBOX_NOTIFY_DIR = "/Content_Plan/.karuselka/notifications"


def _log(event: str, detail: dict | str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = {
        "at": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "detail": detail,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


def _parse_chat_id(raw: str) -> int:
    raw = raw.strip()
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    raise ValueError(
        f"MAX chat id must be numeric (e.g. -76326762551894), not username. Got: {raw!r}"
    )


def _resolve_chat_id(env: dict[str, str]) -> int:
    for key in ("MAX_NOTIFY_CHAT_ID", "MAX_PREVIEW_CHAT_ID", "MAX_DM_CHAT_ID", "MAX_CHAT_ID"):
        raw = env.get(key, "").strip()
        if raw:
            return _parse_chat_id(raw)
    raise RuntimeError(
        "MAX: set MAX_NOTIFY_CHAT_ID or MAX_PREVIEW_CHAT_ID in publish-memory/max.env.local"
    )


def _insecure_tls(env: dict[str, str]) -> bool:
    return env.get("MAX_API_INSECURE_TLS", "true").lower() == "true"


def _extract_post_url(result: dict | None) -> str:
    if not result or not isinstance(result, dict):
        return ""
    for key in ("postUrl", "post_url", "url", "permalink", "link"):
        val = result.get(key)
        if isinstance(val, str) and val.startswith("http"):
            return val
    data = result.get("data")
    if isinstance(data, dict):
        return _extract_post_url(data)
    posts = result.get("posts")
    if isinstance(posts, list) and posts:
        first = posts[0]
        if isinstance(first, dict):
            return _extract_post_url(first)
    post = result.get("post")
    if isinstance(post, dict):
        for platform in post.get("platforms") or []:
            if not isinstance(platform, dict):
                continue
            pdata = platform.get("platformSpecificData") or {}
            for key in ("permalink", "postUrl", "url"):
                val = pdata.get(key) or platform.get(key)
                if isinstance(val, str) and val.startswith("http"):
                    return val
    return ""


def _zernio_platform_status(zernio_response: dict | None) -> str:
    """Parse a single Zernio API response (instagram or tiktok block)."""
    if not zernio_response or not isinstance(zernio_response, dict):
        return "not_attempted"
    if zernio_response.get("dry_run"):
        return "dry_run"
    if zernio_response.get("duplicate_accepted") or zernio_response.get("resumed"):
        return "ok"
    if zernio_response.get("error") or zernio_response.get("errors"):
        return "failed"

    post = zernio_response.get("post")
    if isinstance(post, dict):
        post_status = str(post.get("status") or "").lower()
        if post_status in ("published", "success", "completed"):
            return "ok"
        if post_status in ("failed", "error"):
            return "failed"
        if post_status in ("scheduled", "pending", "processing"):
            return "pending"
        for platform in post.get("platforms") or []:
            if not isinstance(platform, dict):
                continue
            ps = str(platform.get("status") or "").lower()
            if ps in ("published", "success"):
                return "ok"
            if ps in ("failed", "error"):
                return "failed"
            if ps == "pending":
                return "pending"
        if post.get("_id"):
            return "ok"

    if zernio_response.get("_id") or zernio_response.get("id"):
        return "ok"

    msg = str(zernio_response.get("message") or "")
    lower = msg.lower()
    if msg and any(x in lower for x in ("fail", "error", "invalid")):
        return "failed"
    if msg and any(x in lower for x in ("retry", "pending", "scheduled")):
        return "pending"
    return "unknown"


def _zernio_platform_detail(zernio_response: dict | None) -> str:
    if not zernio_response or not isinstance(zernio_response, dict):
        return "—"
    if zernio_response.get("dry_run"):
        return "dry-run"
    if zernio_response.get("duplicate_accepted"):
        post_id = (zernio_response.get("post") or {}).get("_id")
        return f"duplicate ok (post_id={post_id})" if post_id else "duplicate ok"
    if zernio_response.get("resumed"):
        return "resumed partial publish"

    url = _extract_post_url(zernio_response)
    if url:
        return url

    post = zernio_response.get("post")
    if isinstance(post, dict):
        for platform in post.get("platforms") or []:
            if not isinstance(platform, dict):
                continue
            err = platform.get("errorMessage") or platform.get("error")
            if err:
                return str(err)[:200]
        if post.get("_id"):
            return f"post_id={post['_id']}"

    err = (
        zernio_response.get("error")
        or zernio_response.get("message")
        or zernio_response.get("detail")
    )
    if err:
        return str(err)[:200]
    return "—"


def build_publish_report_text(
    *,
    pair_id: str,
    pair_label: str,
    carousel_name: str,
    mode: str = "mixed",
    instagram_result: dict | None = None,
    tiktok_result: dict | None = None,
    next_folder: str | None = None,
    queue_ready: int | None = None,
    error: str | None = None,
) -> str:
    lines = [f"🚀 Karuselka Publish — {pair_id}"]
    if pair_label and pair_label != pair_id:
        lines.append(f"({pair_label})")
    lines.append(f"Папка: {carousel_name}")
    if error:
        lines.append(f"❌ Ошибка: {error}")
    else:
        lines.append(f"Режим: {mode}")
        ig_status = _zernio_platform_status(instagram_result)
        tt_status = _zernio_platform_status(tiktok_result)
        if tt_status == "failed" and tiktok_result and tiktok_result.get("status") == "skipped":
            tt_status = "skipped (needs human)"
        lines.append(f"Instagram: {ig_status} ({_zernio_platform_detail(instagram_result)})")
        lines.append(f"TikTok: {tt_status} ({_zernio_platform_detail(tiktok_result)})")
    if queue_ready is not None and queue_ready > 0 and next_folder:
        lines.append(f"Следующий: {next_folder} (ещё {queue_ready} в очереди)")
    elif next_folder:
        lines.append(f"Следующий: {next_folder}")
    else:
        lines.append("Следующий: очередь пуста")
    return "\n".join(lines)


def _dropbox_notify_backup(text: str, carousel_name: str) -> None:
    env = load_runtime_env()
    token = get_access_token(env)
    payload = {
        "at": datetime.now(timezone.utc).isoformat(),
        "carousel": carousel_name,
        "channel": "max",
        "message": text,
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    path = f"{DROPBOX_NOTIFY_DIR}/{carousel_name}.json"
    upload_file(path, body, token)
    _log("dropbox_backup", {"path": path})


def send_message(text: str, chat_id: int | None = None) -> dict:
    env = load_runtime_env()
    token = env.get("MAX_BOT_TOKEN", "").strip()
    if not token:
        msg = "MAX: MAX_BOT_TOKEN required in publish-memory/max.env.local"
        _log("error", {"reason": msg})
        raise RuntimeError(msg)

    cid = chat_id if chat_id is not None else _resolve_chat_id(env)
    insecure = _insecure_tls(env)

    try:
        data = max_send_message(
            token,
            text,
            chat_id=cid,
            format_mode="markdown",
            insecure_tls=insecure,
        )
    except Exception as exc:  # noqa: BLE001
        _log("send_failed", {"chat_id": cid, "error": str(exc), "preview": text[:120]})
        raise

    message_id = None
    if isinstance(data, dict):
        message_id = (data.get("message") or {}).get("body", {}).get("mid") or data.get("message_id")
    _log("sent", {"chat_id": cid, "message_id": message_id})
    return data


def notify_publish_complete(
    *,
    pair_id: str,
    pair_label: str,
    carousel_name: str,
    mode: str = "mixed",
    instagram_result: dict | None = None,
    tiktok_result: dict | None = None,
    next_folder: str | None = None,
    queue_ready: int | None = None,
    error: str | None = None,
) -> None:
    send_message(
        build_publish_report_text(
            pair_id=pair_id,
            pair_label=pair_label,
            carousel_name=carousel_name,
            mode=mode,
            instagram_result=instagram_result,
            tiktok_result=tiktok_result,
            next_folder=next_folder,
            queue_ready=queue_ready,
            error=error,
        )
    )


def notify_from_publish_result(
    pair_id: str,
    pair_label: str,
    carousel_name: str,
    result: dict,
    queue_remaining: dict[str, int] | None = None,
    next_folder: str | None = None,
    queue_ready: int | None = None,
) -> None:
    if queue_ready is None and queue_remaining:
        queue_ready = queue_remaining.get(pair_id)

    ig = result.get("instagram") if isinstance(result.get("instagram"), dict) else None
    tt = result.get("tiktok") if isinstance(result.get("tiktok"), dict) else None
    tiktok_skipped = result.get("tiktok_skipped")
    if tiktok_skipped and not tt:
        tt = {"error": str(tiktok_skipped)[:500], "status": "skipped"}
    ig_status = _zernio_platform_status(ig)
    tt_status = _zernio_platform_status(tt)
    if ig_status in ("unknown", "not_attempted") and tt_status in ("unknown", "not_attempted"):
        try:
            from publish_incidents import log_incident

            log_incident(
                pair=pair_id,
                stage="notify",
                error="MAX report could not parse Zernio instagram/tiktok blocks",
                carousel=carousel_name,
                context={"instagram_status": ig_status, "tiktok_status": tt_status},
            )
        except Exception:
            pass

    text = build_publish_report_text(
        pair_id=pair_id,
        pair_label=pair_label,
        carousel_name=carousel_name,
        mode=str(result.get("mode") or "mixed"),
        instagram_result=ig,
        tiktok_result=tt,
        next_folder=next_folder,
        queue_ready=queue_ready,
        error=result.get("error"),
    )
    try:
        send_message(text)
    except Exception as exc:  # noqa: BLE001
        try:
            _dropbox_notify_backup(text, carousel_name)
            result["max_fallback"] = "dropbox"
            result["max_error"] = str(exc)
            _log("fallback_ok", {"carousel": carousel_name, "error": str(exc)})
        except Exception as drop_exc:  # noqa: BLE001
            result["max_error"] = f"{exc}; dropbox: {drop_exc}"
            _log("fallback_failed", {"carousel": carousel_name, "error": str(drop_exc)})
            raise
