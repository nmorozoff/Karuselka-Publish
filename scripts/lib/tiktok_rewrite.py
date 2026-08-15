"""Спокойные TikTok title/description без LLM — anti-spam эвристики."""

from __future__ import annotations

import re
from typing import Any

from tiktok_caption import count_hashtags, sanitize_tiktok_text

_HASHTAG_RE = re.compile(r"#[\w\u0400-\u04FF]+", re.UNICODE)

TITLE_MAX = 40
TITLE_HARD_MAX = 90
DESC_MAX = 2200

# Мягкие замены (регистронезависимо где уместно)
_SOFTEN: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bтоксичн\w*", re.I), "сложн"),
    (re.compile(r"\bразруш\w*", re.I), "измен"),
    (re.compile(r"\bпрямо сейчас\b", re.I), ""),
    (re.compile(r"\bжми\b", re.I), ""),
    (re.compile(r"\bподпишись\b", re.I), ""),
    (re.compile(r"\b100\s*%", re.I), ""),
    (re.compile(r"\bкак за \d+\s*\w*", re.I), ""),
    (re.compile(r"\bза \d+\s*(сесс|минут|дн)", re.I), ""),
    (re.compile(r"\bглубоко\b", re.I), ""),
    (re.compile(r"\bсрочно\b", re.I), ""),
    (re.compile(r"\bшок\b", re.I), ""),
    (re.compile(r"\bсенсаци\w*", re.I), ""),
    (re.compile(r"\bжесток\w*", re.I), "резк"),
    (re.compile(r"\bбездарност\w*", re.I), "самокритик"),
    (re.compile(r"\bобманываеш\w*", re.I), "сомневаешься"),
]

_SPAM_PARA = re.compile(
    r"потерянн\w*\s+деньг|ссылка в bio|подпишись|жми|100\s*%|сделай сегодня",
    re.I,
)
_DESC_DROP_LINES = re.compile(
    r"^.*("
    r"сделай сегодня|жми|подпишись|переходи|ссылка в bio|="
    r").*$",
    re.I | re.M,
)

_HASHTAG_PRIORITY = [
    "#психология",
    "#эмдр",
    "#отношения",
    "#самооценка",
    "#тревога",
    "#границы",
    "#родители",
    "#выгорание",
    "#самопомощь",
    "#ментальноездоровье",
    "#психолог",
    "#эмоции",
]


def _soften(text: str) -> str:
    out = text or ""
    for pat, repl in _SOFTEN:
        out = pat.sub(repl, out)
    out = re.sub(r"\s{2,}", " ", out)
    out = re.sub(r"\s+([,.!?])", r"\1", out)
    return out.strip()


def _extract_hashtags(text: str) -> list[str]:
    seen: set[str] = set()
    tags: list[str] = []
    for m in _HASHTAG_RE.finditer(text or ""):
        tag = m.group(0)
        low = tag.lower()
        if low not in seen:
            seen.add(low)
            tags.append(tag)
    return tags


def _strip_hashtags_from_body(text: str) -> str:
    body = _HASHTAG_RE.sub("", text or "")
    body = re.sub(r"\n{3,}", "\n\n", body)
    return re.sub(r"[ \t]{2,}", " ", body).strip()


def _pick_hashtags(existing: list[str], *, limit: int = 4) -> list[str]:
    if not existing:
        return ["#психология", "#эмдр", "#самопомощь", "#ментальноездоровье"][:limit]
    lower_map = {t.lower(): t for t in existing}
    picked: list[str] = []
    for pref in _HASHTAG_PRIORITY:
        if pref.lower() in lower_map and pref.lower() not in {p.lower() for p in picked}:
            picked.append(lower_map[pref.lower()])
        if len(picked) >= limit:
            return picked
    for tag in existing:
        if tag.lower() not in {p.lower() for p in picked}:
            picked.append(tag)
        if len(picked) >= limit:
            break
    return picked[:limit]


_TOPIC_TITLES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"родительск|матер|отец|детств", re.I), "О влиянии родительских привычек"),
    (re.compile(r"финансов|потолок|деньг|заработ", re.I), "О финансовом потолке и опыте"),
    (re.compile(r"внутренн\w*\s+критик", re.I), "О внутреннем критике"),
    (re.compile(r"тревог", re.I), "О тревоге без давления"),
    (re.compile(r"границ", re.I), "О личных границах"),
    (re.compile(r"выгоран", re.I), "О выгорании и восстановлении"),
    (re.compile(r"отношен|партнёр|брак", re.I), "О сложных отношениях"),
    (re.compile(r"самооцен|уверен", re.I), "О самооценке и опоре на себя"),
    (re.compile(r"травм|эмдр", re.I), "О бережной переработке опыта"),
    (re.compile(r"стыд|вин", re.I), "О чувстве вины и стыда"),
    (re.compile(r"одобрен|начальник", re.I), "Об одобрении и самоценности"),
    (re.compile(r"семь", re.I), "О семейных сценариях"),
    (re.compile(r"прояв", re.I), "О страхе проявляться"),
]


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _title_from_topic(text: str) -> str | None:
    for pat, title in _TOPIC_TITLES:
        if pat.search(text):
            return title
    return None


def _pick_title_sentence(text: str) -> str:
    sents = _sentences(text)
    kept: list[str] = []
    for s in sents:
        if re.search(r"\b(забудь|жми|подпишись|переходи)\b", s, re.I):
            continue
        kept.append(s)
    pool = kept or sents
    if not pool:
        return text
    # Предпочитаем фразу до тире во втором предложении, если первое — крючок
    if len(pool) >= 2 and len(pool[0]) > 55:
        candidate = pool[1]
        for sep in (" — ", " – ", " - "):
            if sep in candidate:
                head = candidate.split(sep, 1)[0].strip()
                if 12 <= len(head) <= TITLE_MAX:
                    return head
        return candidate
    pick = pool[0]
    for sep in (" — ", " – ", " - ", ": "):
        if sep in pick:
            head = pick.split(sep, 1)[0].strip()
            if 12 <= len(head) <= TITLE_MAX + 5:
                return head
    return pick


def _truncate_title(text: str, max_len: int = TITLE_MAX) -> str:
    cleaned = _strip_hashtags_from_body(text).strip(" .—-–")
    if not cleaned:
        return "О психологии и поддержке"
    if len(cleaned) <= max_len:
        return cleaned[0].upper() + cleaned[1:] if cleaned else cleaned

    for sep in (" — ", " – ", " - ", ": "):
        if sep in cleaned:
            head = cleaned.split(sep, 1)[0].strip()
            if 12 <= len(head) <= max_len:
                return head[0].upper() + head[1:]

    slice_ = cleaned[: max_len + 1]
    sp = slice_.rfind(" ")
    if sp >= 12:
        out = slice_[:sp].strip()
    else:
        out = cleaned[:max_len].strip()
    if out and out[-1] in ",;:":
        out = out[:-1]
    return out[0].upper() + out[1:] if out else out


def rewrite_tiktok_title(raw: str, *, ig_caption: str = "") -> str:
    source = (raw or "").strip() or (ig_caption or "").split("\n", 1)[0].strip()
    topic = _title_from_topic(source) or (_title_from_topic(ig_caption) if ig_caption else None)
    if topic:
        return topic[:TITLE_HARD_MAX]

    pick = _pick_title_sentence(source)
    softened = _soften(pick)
    softened = re.sub(r"^как\s+", "О том, ", softened, flags=re.I)
    softened = re.sub(r"^\d+\s+", "", softened)
    title = _truncate_title(softened, TITLE_MAX)
    if len(title) < 12 and ig_caption:
        topic2 = _title_from_topic(ig_caption)
        if topic2:
            return topic2[:TITLE_HARD_MAX]
        title = _truncate_title(_soften(_pick_title_sentence(ig_caption)), TITLE_MAX)
    return title[:TITLE_HARD_MAX]


def rewrite_tiktok_description(raw: str, *, ig_caption: str = "") -> str:
    source = (raw or "").strip() or (ig_caption or "").strip()
    tags = _extract_hashtags(source)
    body = _strip_hashtags_from_body(source)

    # Убрать строки с жёстким CTA
    lines = []
    for line in body.splitlines():
        if _DESC_DROP_LINES.match(line.strip()):
            continue
        lines.append(_soften(line))
    body = "\n".join(lines).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)

    # Сократить длинные тексты: 2–3 абзаца
    paras = [p.strip() for p in re.split(r"\n{2,}", body) if p.strip()]
    paras = [p for p in paras if not _SPAM_PARA.search(p)]
    if len(paras) > 3:
        paras = paras[:3]
    body = "\n\n".join(paras)

    # Убрать формулы с =
    body = re.sub(r"[^.\n]*=[^.\n]*\.?", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    if len(body) > 900:
        body = body[:900].rsplit(" ", 1)[0].strip() + "…"

    tags4 = _pick_hashtags(tags, limit=4)
    if not body:
        body = "Коротко о теме карусели — без обещаний и давления. Можно сохранить, если откликается."

    out = body
    if tags4:
        out = f"{body}\n\n{' '.join(tags4)}"

    out, _meta = sanitize_tiktok_text(out, max_hashtags=4)
    return out[:DESC_MAX]


def rewrite_tiktok_fields(fields: dict) -> dict[str, Any]:
    ig = fields.get("Описание карусели") or ""
    old_title = fields.get("TikTok заголовок") or ""
    old_desc = fields.get("TikTok описание") or ""

    new_title = rewrite_tiktok_title(old_title, ig_caption=ig)
    new_desc = rewrite_tiktok_description(old_desc, ig_caption=ig)

    return {
        "TikTok заголовок": new_title,
        "TikTok описание": new_desc,
        "before": {
            "title": old_title,
            "title_len": len(old_title),
            "desc_hashtags": count_hashtags(old_desc),
            "desc_len": len(old_desc),
        },
        "after": {
            "title": new_title,
            "title_len": len(new_title),
            "desc_hashtags": count_hashtags(new_desc),
            "desc_len": len(new_desc),
        },
    }
