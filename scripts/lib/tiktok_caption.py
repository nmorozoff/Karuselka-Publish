"""TikTok caption helpers: hashtag limits (spam prevention)."""

from __future__ import annotations

import os
import re

_HASHTAG_RE = re.compile(r"#[\w\u0400-\u04FF]+", re.UNICODE)


def count_hashtags(text: str) -> int:
    return len(_HASHTAG_RE.findall(text or ""))


def max_hashtags_limit() -> int:
    raw = os.environ.get("TIKTOK_MAX_HASHTAGS", "4").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 4


def sanitize_tiktok_text(text: str, *, max_hashtags: int | None = None) -> tuple[str, dict]:
    """
    Оставить не больше max_hashtags хэштегов (по порядку в тексте).
    Лишние #теги удаляются — снижает риск TikTok spam.
    """
    limit = max_hashtags if max_hashtags is not None else max_hashtags_limit()
    original = (text or "").strip()
    if not original:
        return "", {"hashtags_before": 0, "hashtags_after": 0, "trimmed": False}

    before = count_hashtags(original)
    if before <= limit:
        return original, {"hashtags_before": before, "hashtags_after": before, "trimmed": False}

    kept = 0
    out_parts: list[str] = []
    for token in original.split():
        if _HASHTAG_RE.fullmatch(token):
            if kept < limit:
                out_parts.append(token)
                kept += 1
            continue
        out_parts.append(token)

    cleaned = " ".join(out_parts)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned, {
        "hashtags_before": before,
        "hashtags_after": kept,
        "trimmed": True,
    }


def prepare_tiktok_fields(fields: dict) -> tuple[str, str, dict]:
    """Заголовок ≤90, описание с лимитом хэштегов."""
    title = (fields.get("TikTok заголовок") or "Карусель")[:90]
    raw_desc = fields.get("TikTok описание") or fields.get("Описание карусели") or ""
    description, meta = sanitize_tiktok_text(raw_desc)
    description = description[:4000]
    meta["title_len"] = len(title)
    meta["description_len"] = len(description)
    return title, description, meta
