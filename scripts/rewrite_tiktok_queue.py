#!/usr/bin/env python3
"""Переписать TikTok заголовки/описания в очереди Airtable (спокойный тон, ≤4 #)."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from http_client import http_json  # noqa: E402
from publish_config import MEMORY, load_runtime_env, pair_config  # noqa: E402
from tiktok_rewrite import rewrite_tiktok_fields  # noqa: E402


def list_all_records(env: dict[str, str]) -> list[dict]:
    pair = pair_config("pair1")
    base = pair["airtable"]["base_id"]
    table = pair["airtable"]["table_id"]
    token = env["AIRTABLE_ACCESS_TOKEN"]
    records: list[dict] = []
    offset: str | None = None
    while True:
        qs = urllib.parse.urlencode({"pageSize": 100, **({"offset": offset} if offset else {})})
        url = f"https://api.airtable.com/v0/{base}/{table}?{qs}"
        data = http_json("GET", url, headers={"Authorization": f"Bearer {token}"})
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return records


def batch_update(env: dict[str, str], updates: list[dict]) -> None:
    pair = pair_config("pair1")
    base = pair["airtable"]["base_id"]
    table = pair["airtable"]["table_id"]
    token = env["AIRTABLE_ACCESS_TOKEN"]
    url = f"https://api.airtable.com/v0/{base}/{table}"
    for i in range(0, len(updates), 10):
        chunk = updates[i : i + 10]
        http_json(
            "PATCH",
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            body={"records": chunk, "typecast": True},
        )
        time.sleep(0.25)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_runtime_env()
    records = list_all_records(env)
    report_rows: list[dict] = []
    updates: list[dict] = []

    for rec in records:
        fields = rec.get("fields", {})
        name = fields.get("Name", "")
        result = rewrite_tiktok_fields(fields)
        row = {
            "id": rec["id"],
            "name": name,
            "pair": fields.get("Пара"),
            **{k: v for k, v in result.items() if k not in ("TikTok заголовок", "TikTok описание")},
        }
        report_rows.append(row)
        updates.append(
            {
                "id": rec["id"],
                "fields": {
                    "TikTok заголовок": result["TikTok заголовок"],
                    "TikTok описание": result["TikTok описание"],
                },
            }
        )

    summary = {
        "dry_run": args.dry_run,
        "total": len(records),
        "title_len_avg_before": round(
            sum(r["before"]["title_len"] for r in report_rows) / max(1, len(report_rows)), 1
        ),
        "title_len_avg_after": round(
            sum(r["after"]["title_len"] for r in report_rows) / max(1, len(report_rows)), 1
        ),
        "rows": report_rows,
    }

    out = MEMORY / "output" / "tiktok-rewrite-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.dry_run:
        batch_update(env, updates)

    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, ensure_ascii=False, indent=2))
    print(f"report: {out}")
    for row in report_rows[:5]:
        print("\n---", row["name"])
        print("TITLE:", row["after"]["title"], f"({row['after']['title_len']})")
        print("HT:", row["before"]["desc_hashtags"], "→", row["after"]["desc_hashtags"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
