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
    return ""


def _platform_status(result: dict | None, platform: str) -> str:
    if not result or not isinstance(result, dict):
        return "not_attempted"
    data = result.get(platform) if isinstance(result.get(platform), dict) else {}
    if not data:
        return "not_attempted"
    if data.get("ok") or data.get("status") == "success" or data.get("published"):
        return "ok"
    if data.get("error") or data.get("message") or data.get("dry_run"):
        return "failed"
    return "unknown"


def _platform_detail(result: dict | None, platform: str) -> str:
    if not result or not isinstance(result, dict):
        return "—"
    data = result.get(platform) if isinstance(result.get(platform), dict) else {}
    if not data:
        return "—"
    url = _extract_post_url(data)
    if url:
        return url
    err = data.get("error") or data.get("message") or data.get("detail")
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
    error: str | None = None,
) -> str:
    """Шаблон отчёта из CLOUD_AGENT_PROMPT.md."""
    lines = [f"🚀 Karuselka Publish — {pair_id}"]
    if pair_label and pair_label != pair_id:
        lines.append(f"({pair_label})")
    lines.append(f"Папка: {carousel_name}")
    if error:
        lines.append(f"❌ Ошибка: {error}")
    else:
        lines.append(f"Режим: {mode}")
        ig_status = _platform_status(instagram_result, "instagram")
        tt_status = _platform_status(tiktok_result, "tiktok")
        lines.append(f"Instagram: {ig_status} ({_platform_detail(instagram_result, 'instagram')})")
        lines.append(f"TikTok: {tt_status} ({_platform_detail(tiktok_result, 'tiktok')})")
    lines.append(f"Следующий: {next_folder or 'очередь пуста'}")
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
) -> None:
    text = build_publish_report_text(
        pair_id=pair_id,
        pair_label=pair_label,
        carousel_name=carousel_name,
        mode=str(result.get("mode") or "mixed"),
        instagram_result=result.get("instagram") if isinstance(result.get("instagram"), dict) else None,
        tiktok_result=result.get("tiktok") if isinstance(result.get("tiktok"), dict) else None,
        next_folder=next_folder,
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
