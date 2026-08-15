"""Classify publish failures and inspect Zernio responses."""

from __future__ import annotations

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
            "timeout",
            "timed out",
            "502",
            "503",
            "504",
            "connection reset",
            "connection refused",
            "operation timed out",
        )
    ):
        return {
            "category": "transient",
            "needs_human": False,
            "retryable": True,
        }
    if "409" in lower or "conflict" in lower:
        return {
            "category": "conflict",
            "needs_human": True,
            "retryable": False,
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


def parse_rate_limited_until(text: str) -> str | None:
    """Extract ISO timestamp from Zernio 429 response, e.g. rateLimitedUntil."""
    import re

    match = re.search(r'rateLimitedUntil["\']?\s*[:=]\s*["\']?([^"\'>,\s]+)', text)
    if match:
        return match.group(1)
    return None


def failed_record(error_text: str, *, at: str | None = None) -> dict[str, Any]:
    from datetime import datetime, timezone

    meta = classify_failure_message(error_text)
    out: dict[str, Any] = {
        "at": at or datetime.now(timezone.utc).isoformat(),
        "error": error_text[:8000],
        **meta,
    }
    return out
