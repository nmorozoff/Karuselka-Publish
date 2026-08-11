"""Classify publish failures and inspect Zernio responses."""

from __future__ import annotations

import json
import re
from typing import Any


def zernio_response_ok(res: dict[str, Any] | None) -> bool:
    if not res or not isinstance(res, dict):
        return False
    if res.get("dry_run"):
        return True
    if res.get("error") or res.get("errors"):
        return False
    if res.get("_id") or res.get("id"):
        return True
    post = res.get("post")
    if isinstance(post, dict):
        if post.get("_id"):
            return True
        status = str(post.get("status") or "").lower()
        if status in ("published", "success", "completed", "scheduled"):
            return True
        for platform in post.get("platforms") or []:
            if not isinstance(platform, dict):
                continue
            ps = str(platform.get("status") or "").lower()
            if ps in ("published", "success"):
                return True
    msg = str(res.get("message") or "")
    if msg and any(x in msg.lower() for x in ("error", "fail", "invalid")):
        return False
    return bool(post)


def zernio_duplicate_conflict_response(text: str) -> dict[str, Any] | None:
    """Zernio 409: same content already scheduled/posted within 24h — treat as idempotent ok."""
    lower = text.lower()
    if "409" not in lower:
        return None
    if not any(
        x in lower
        for x in (
            "already scheduled",
            "already posted",
            "exact content is already",
        )
    ):
        return None
    payload: dict[str, Any] | None = None
    for match in re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text):
        try:
            payload = json.loads(match.group())
            break
        except json.JSONDecodeError:
            continue
    if not payload:
        return None
    details = payload.get("details") if isinstance(payload.get("details"), dict) else {}
    post_id = details.get("existingPostId") or payload.get("existingPostId")
    if not post_id:
        return None
    return {
        "post": {"_id": post_id},
        "duplicate_accepted": True,
        "message": str(payload.get("error") or "duplicate content accepted"),
    }


def classify_failure_message(text: str) -> dict[str, Any]:
    lower = text.lower()
    if zernio_duplicate_conflict_response(text):
        return {
            "category": "duplicate_content",
            "needs_human": False,
            "retryable": False,
        }
    if any(
        x in lower
        for x in (
            "url ownership not verified",
            "verify domain ownership",
            "developers.tiktok.com",
        )
    ):
        return {
            "category": "tiktok_url_ownership",
            "needs_human": True,
            "retryable": False,
        }
    if any(x in lower for x in ("spam", "user_abuse", "content guidelines")):
        return {
            "category": "tiktok_spam",
            "needs_human": True,
            "retryable": False,
        }
    if any(
        x in lower
        for x in (
            "aspect ratio",
            "invalid instagram image resolution",
            "failed to validate instagram image",
        )
    ):
        return {
            "category": "instagram_format",
            "needs_human": True,
            "retryable": False,
        }
    if any(x in lower for x in ("429", "rate limit", "too many requests")):
        return {
            "category": "rate_limit",
            "needs_human": False,
            "retryable": True,
        }
    if any(x in lower for x in ("timeout", "502", "503", "504")):
        return {
            "category": "transient",
            "needs_human": False,
            "retryable": True,
        }
    if "http error 400" in lower or (
        "400" in lower and any(x in lower for x in ("bad request", "all platforms failed"))
    ):
        return {
            "category": "bad_request",
            "needs_human": True,
            "retryable": False,
        }
    return {
        "category": "unknown",
        "needs_human": False,
        "retryable": True,
    }


def failed_record(error_text: str, *, at: str | None = None) -> dict[str, Any]:
    from datetime import datetime, timezone

    meta = classify_failure_message(error_text)
    out: dict[str, Any] = {
        "at": at or datetime.now(timezone.utc).isoformat(),
        "error": error_text[:8000],
        **meta,
    }
    return out
