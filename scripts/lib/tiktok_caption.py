"""TikTok caption helpers: hashtag limits (spam prevention)."""

from __future__ import annotations

import os
import re

_HASHTAG_RE = re.compile(r"#[\w\u0400-\u04FF]+", re.UNICODE)
_CTA_RE = re.compile(
    r"(?:^|[\.\s])(?:"
    r"Это блог практикующего психолога[^#\.]*[\.\s]*|"
    r"Перешли тому[^#\.]*[\.\s]*|"
    r"сохрани чтоб не потерять[^#\.]*[\.\s]*|"
    r"подпишись[^#\.]*[\.\s]*"
    r")",
    re.IGNORECASE,
)
_BIO_DUP_RE = re.compile(
    r"\s*Я[,\s]+Наталья\s+Морозова[^#]*$",
    re.IGNORECASE | re.DOTALL,
)


def count_hashtags(text: str) -> int:
    return len(_HASHTAG_RE.findall(text or ""))


def max_hashtags_limit() -> int:
    raw = os.environ.get("TIKTOK_MAX_HASHTAGS", "4").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 4


def max_description_chars() -> int:
    raw = os.environ.get("TIKTOK_MAX_DESCRIPTION_CHARS", "800").strip()
    try:
        return max(100, int(raw))
    except ValueError:
        return 800


def _split_body_and_hashtags(text: str) -> tuple[str, list[str]]:
    tags = _HASHTAG_RE.findall(text)
    body = _HASHTAG_RE.sub("", text)
    body = re.sub(r"\s{2,}", " ", body).strip()
    return body, tags


def _trim_hashtags(tags: list[str], limit: int) -> list[str]:
    return tags[:limit] if limit >= 0 else []


def sanitize_tiktok_text(text: str, *, max_hashtags: int | None = None) -> tuple[str, dict]:
    """
    Оставить не больше max_hashtags хэштегов (по порядку в тексте).
    Убрать CTA-хвосты и дубли bio после хэштегов — снижает риск TikTok spam.
    """
    tag_limit = max_hashtags if max_hashtags is not None else max_hashtags_limit()
    char_limit = max_description_chars()
    original = (text or "").strip()
    if not original:
        return "", {
            "hashtags_before": 0,
            "hashtags_after": 0,
            "trimmed": False,
            "description_truncated": False,
            "cta_stripped": False,
            "bio_dup_stripped": False,
        }

    before = count_hashtags(original)
    body, tags = _split_body_and_hashtags(original)
    cta_stripped = bool(_CTA_RE.search(body))
    body = _CTA_RE.sub(" ", body).strip()
    bio_dup_stripped = bool(_BIO_DUP_RE.search(body))
    body = _BIO_DUP_RE.sub("", body).strip()
    body = re.sub(r"\s{2,}", " ", body).strip(" .")

    kept_tags = _trim_hashtags(tags, tag_limit)
    tag_suffix = (" " + " ".join(kept_tags)) if kept_tags else ""
    max_body = max(0, char_limit - len(tag_suffix))
    description_truncated = len(body) > max_body
    if description_truncated:
        body = body[:max_body].rstrip(" ,.;—-")
    cleaned = (body + tag_suffix).strip()

    trimmed = before > len(kept_tags) or cta_stripped or bio_dup_stripped or description_truncated
    return cleaned, {
        "hashtags_before": before,
        "hashtags_after": len(kept_tags),
        "trimmed": trimmed,
        "description_truncated": description_truncated,
        "cta_stripped": cta_stripped,
        "bio_dup_stripped": bio_dup_stripped,
        "char_limit": char_limit,
    }


def prepare_tiktok_fields(fields: dict) -> tuple[str, str, dict]:
    """Заголовок ≤90, описание с лимитом хэштегов."""
    title = (fields.get("TikTok заголовок") or "Карусель")[:90]
    raw_desc = fields.get("TikTok описание") or fields.get("Описание карусели") or ""
    description, meta = sanitize_tiktok_text(raw_desc)
    meta["title_len"] = len(title)
    meta["description_len"] = len(description)
    return title, description, meta
