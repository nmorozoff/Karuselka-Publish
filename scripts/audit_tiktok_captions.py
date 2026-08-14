#!/usr/bin/env python3
"""Аудит хэштегов в TikTok полях очереди Airtable."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from publish_config import MEMORY, load_runtime_env, pair_config  # noqa: E402
from publish_engine import list_queue_records  # noqa: E402
from tiktok_caption import count_hashtags, max_hashtags_limit, sanitize_tiktok_text  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Показать только с хэштегов > лимита")
    args = parser.parse_args()

    env = load_runtime_env()
    pair = pair_config("pair1")
    records = list_queue_records(env, pair)
    limit = max_hashtags_limit()
    rows = []

    for rec in records:
        fields = rec.get("fields", {})
        name = fields.get("Name", "")
        title = fields.get("TikTok заголовок") or ""
        desc = fields.get("TikTok описание") or fields.get("Описание карусели") or ""
        ht_title = count_hashtags(title)
        ht_desc = count_hashtags(desc)
        _, meta = sanitize_tiktok_text(desc)
        row = {
            "name": name,
            "hashtags_title": ht_title,
            "hashtags_description": ht_desc,
            "would_trim": meta.get("trimmed", False),
            "after_trim": meta.get("hashtags_after", ht_desc),
        }
        if args.limit and ht_desc <= limit and ht_title <= limit:
            continue
        rows.append(row)

    rows.sort(key=lambda r: (-r["hashtags_description"], r["name"]))
    report = {
        "limit": limit,
        "total_in_queue": len(records),
        "flagged": len([r for r in rows if r["hashtags_description"] > limit or r["would_trim"]]),
        "rows": rows,
    }
    out = MEMORY / "output" / "tiktok-caption-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
