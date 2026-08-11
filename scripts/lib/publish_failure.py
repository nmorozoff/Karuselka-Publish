"""Classify publish failures and inspect Zernio responses."""

from __future__ import annotations

import json
import re
from typing import Any


def parse_zernio_duplicate_error(text: str) -> dict[str, Any] | None:
    """If Zernio 409 means content already posted, return a synthetic ok response."""
    lower = text.lower()
    if "409" not in text and "already scheduled" not in lower and "already posted" not in lower:
        return None
    if "already scheduled" not in lower and "already posted" not in lower and "exact content" not in lower:
        return None
    post_id = ""
    match = re.search(r'"existingPostId"\s*:\s*"([^"]+)"', text)
    if match:
        post_id = match.group(1)
    else:
        try:
            payload_start = text.find("{")
            if payload_start >= 0:
                payload = json.loads(text[payload_start:])
                details = payload.get("details") if isinstance(payload, dict) else None
                if isinstance(details, dict):
                    post_id = str(details.get("existingPostId") or "")
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    out: dict[str, Any] = {
        "duplicate_skipped": True,
        "post": {"status": "published"},
    }
    if post_id:
        out["post"]["_id"] = post_id
    return out


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


def classify_failure_message(text: str) -> dict[str, Any]:
    lower = text.lower()
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
    if any(
        x in lower
        for x in (
            "already scheduled",
            "already posted",
            "exact content is already",
            "http 409",
        )
    ):
        return {
            "category": "zernio_duplicate",
            "needs_human": False,
            "retryable": False,
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
