"""Telegram notifications after publish."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dropbox_client import get_access_token, upload_file
from publish_config import MEMORY, load_runtime_env
from telegram_http import api as tg_api

LOG_PATH = MEMORY / "output" / "telegram-notify.log"
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


def build_publish_success_text(
    *,
    pair_id: str,
    pair_label: str,
    carousel_name: str,
    queue_remaining: dict[str, int] | None = None,
    instagram_result: dict | None = None,
    tiktok_result: dict | None = None,
) -> str:
    """Шаблон уведомления после успешной публикации."""
    remaining = queue_remaining or {}
    n1 = remaining.get("pair1", 0)
    n2 = remaining.get("pair2", 0)
    lines = [
        f"✅ Карусель опубликована: {carousel_name} ({pair_id})",
        "📸 Instagram: видео hook + 5 фото",
        "🎵 Добавь музыку в Instagram вручную",
        f"📦 В очереди осталось: {n1} (pair1) / {n2} (pair2)",
    ]
    ig_url = _extract_post_url(instagram_result)
    tt_url = _extract_post_url(tiktok_result)
    if ig_url:
        lines.extend(["", f"IG: {ig_url}"])
    if tt_url:
        lines.append(f"TikTok: {tt_url}")
    if pair_label and pair_label != pair_id:
        lines.insert(1, f"({pair_label})")
    return "\n".join(lines)


def _dropbox_notify_backup(text: str, carousel_name: str) -> None:
    env = load_runtime_env()
    token = get_access_token(env)
    payload = {
        "at": datetime.now(timezone.utc).isoformat(),
        "carousel": carousel_name,
        "message": text,
    }
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    path = f"{DROPBOX_NOTIFY_DIR}/{carousel_name}.json"
    upload_file(path, body, token)
    _log("dropbox_backup", {"path": path})


def send_message(text: str, chat_id: str | None = None) -> dict:
    env = load_runtime_env()
    token = env.get("TELEGRAM_BOT_TOKEN", "")
    cid = chat_id or env.get("TELEGRAM_NOTIFY_CHAT_ID", "")
    if not token or not cid:
        msg = "Telegram: TELEGRAM_BOT_TOKEN and TELEGRAM_NOTIFY_CHAT_ID required"
        _log("error", {"reason": msg, "has_token": bool(token), "has_chat_id": bool(cid)})
        raise RuntimeError(msg)

    try:
        data = tg_api(
            token,
            "sendMessage",
            {"chat_id": cid, "text": text, "disable_web_page_preview": "true"},
        )
    except Exception as exc:  # noqa: BLE001
        _log("send_failed", {"chat_id": cid, "error": str(exc), "preview": text[:120]})
        raise

    if not data.get("ok"):
        _log("api_error", {"chat_id": cid, "response": data})
        raise RuntimeError(f"Telegram API error: {data}")

    _log("sent", {"chat_id": cid, "message_id": (data.get("result") or {}).get("message_id")})
    return data


def notify_publish_complete(
    *,
    pair_id: str,
    pair_label: str,
    carousel_name: str,
    queue_remaining: dict[str, int] | None = None,
    instagram_result: dict | None = None,
    tiktok_result: dict | None = None,
) -> None:
    send_message(
        build_publish_success_text(
            pair_id=pair_id,
            pair_label=pair_label,
            carousel_name=carousel_name,
            queue_remaining=queue_remaining,
            instagram_result=instagram_result,
            tiktok_result=tiktok_result,
        )
    )


def notify_from_publish_result(
    pair_id: str,
    pair_label: str,
    carousel_name: str,
    result: dict,
    queue_remaining: dict[str, int] | None = None,
) -> None:
    text = build_publish_success_text(
        pair_id=pair_id,
        pair_label=pair_label,
        carousel_name=carousel_name,
        queue_remaining=queue_remaining,
        instagram_result=result.get("instagram") if isinstance(result.get("instagram"), dict) else None,
        tiktok_result=result.get("tiktok") if isinstance(result.get("tiktok"), dict) else None,
    )
    try:
        send_message(text)
    except Exception as exc:  # noqa: BLE001
        try:
            _dropbox_notify_backup(text, carousel_name)
            result["telegram_fallback"] = "dropbox"
            result["telegram_error"] = str(exc)
            _log("fallback_ok", {"carousel": carousel_name, "error": str(exc)})
        except Exception as drop_exc:  # noqa: BLE001
            result["telegram_error"] = f"{exc}; dropbox: {drop_exc}"
            _log("fallback_failed", {"carousel": carousel_name, "error": str(drop_exc)})
            raise
