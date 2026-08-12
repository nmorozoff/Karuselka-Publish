#!/usr/bin/env python3
"""Создать единую таблицу Airtable Queue и перенести строки из pair1/2/3."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
MEMORY = SCRIPTS.parent / "publish-memory"
PAIRS_PATH = MEMORY / "accounts-pairs.json"
sys.path.insert(0, str(SCRIPTS / "lib"))

from http_client import http_json, urlopen  # noqa: E402
from publish_config import load_runtime_env, pair_config  # noqa: E402

TABLE_NAME = "Каруселька Queue"
PAIR_IDS = ("pair1", "pair2", "pair3")
LEGACY_TABLES = {
    "pair1": "tblFWCmLCXLrOdKut",
    "pair2": "tbl2zotNwOmWLSTyC",
    "pair3": "tblNv5eMi1BXbu4Tq",
}
BASE_ID = "appQTNsDMuodYyp34"


def api_request(method: str, url: str, token: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method=method,
    )
    try:
        with urlopen(req, timeout=120) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Airtable API {e.code}: {e.read().decode()}") from e


def find_table_id(token: str, base_id: str, name: str) -> str | None:
    data = api_request("GET", f"https://api.airtable.com/v0/meta/bases/{base_id}/tables", token)
    for table in data.get("tables", []):
        if table.get("name") == name:
            return table.get("id")
    return None


def create_unified_table(token: str, base_id: str) -> str:
    existing = find_table_id(token, base_id, TABLE_NAME)
    if existing:
        return existing
    schema = {
        "name": TABLE_NAME,
        "description": "Единая очередь публикации — все пары, FIFO по createdTime",
        "fields": [
            {"name": "Name", "type": "singleLineText"},
            {
                "name": "Пара",
                "type": "singleSelect",
                "options": {
                    "choices": [{"name": "pair1"}, {"name": "pair2"}, {"name": "pair3"}],
                },
            },
            {"name": "Описание карусели", "type": "multilineText"},
            {"name": "TikTok заголовок", "type": "singleLineText"},
            {"name": "TikTok описание", "type": "multilineText"},
        ],
    }
    result = api_request("POST", f"https://api.airtable.com/v0/meta/bases/{base_id}/tables", token, schema)
    table_id = result.get("id")
    if not table_id:
        raise SystemExit(f"No table id: {result}")
    return table_id


def list_all_records(token: str, base_id: str, table_id: str) -> list[dict]:
    records: list[dict] = []
    offset: str | None = None
    while True:
        qs = urllib.parse.urlencode({"pageSize": 100, **({"offset": offset} if offset else {})})
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}?{qs}"
        data = http_json("GET", url, headers={"Authorization": f"Bearer {token}"})
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return records


def map_fields(rec: dict, pair_id: str) -> dict:
    f = rec.get("fields", {})
    out = {
        "Name": f.get("Name", ""),
        "Пара": pair_id,
        "Описание карусели": f.get("Описание карусели", ""),
        "TikTok заголовок": f.get("TikTok заголовок", ""),
        "TikTok описание": f.get("TikTok описание", ""),
    }
    return {k: v for k, v in out.items() if v not in ("", None)}


def batch_create(token: str, base_id: str, table_id: str, rows: list[dict]) -> list[str]:
    created: list[str] = []
    for i in range(0, len(rows), 10):
        chunk = rows[i : i + 10]
        payload = {"records": [{"fields": r} for r in chunk], "typecast": True}
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
        data = http_json(
            "POST",
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            body=payload,
        )
        for rec in data.get("records", []):
            if rec.get("id"):
                created.append(rec["id"])
        time.sleep(0.25)
    return created


def batch_delete(token: str, base_id: str, table_id: str, record_ids: list[str]) -> int:
    deleted = 0
    for i in range(0, len(record_ids), 10):
        chunk = record_ids[i : i + 10]
        qs = "&".join(f"records[]={urllib.parse.quote(rid)}" for rid in chunk)
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}?{qs}"
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}"},
            method="DELETE",
        )
        with urlopen(req, timeout=120) as resp:
            resp.read()
        deleted += len(chunk)
        time.sleep(0.25)
    return deleted


def update_accounts_pairs(table_id: str, base_id: str) -> None:
    pairs = json.loads(PAIRS_PATH.read_text(encoding="utf-8"))
    pairs["airtable_queue"] = {
        "base_id": base_id,
        "table_id": table_id,
        "fields": {
            "name": "Name",
            "pair": "Пара",
            "instagram_caption": "Описание карусели",
            "tiktok_title": "TikTok заголовок",
            "tiktok_description": "TikTok описание",
        },
    }
    for pid in PAIR_IDS:
        pairs[pid]["airtable"]["base_id"] = base_id
        pairs[pid]["airtable"]["table_id"] = table_id
        pairs[pid]["airtable"]["fields"]["pair"] = "Пара"
    PAIRS_PATH.write_text(json.dumps(pairs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_factory_pairs(table_id: str, base_id: str) -> None:
    factory_path = SCRIPTS.parent.parent / "КАРУСЕЛЬКА" / "carusel-memory" / "publish" / "accounts-pairs.json"
    if not factory_path.exists():
        return
    pairs = json.loads(factory_path.read_text(encoding="utf-8"))
    pairs["airtable_queue"] = {
        "base_id": base_id,
        "table_id": table_id,
        "fields": {
            "name": "Name",
            "pair": "Пара",
            "instagram_caption": "Описание карусели",
            "tiktok_title": "TikTok заголовок",
            "tiktok_description": "TikTok описание",
        },
    }
    for pid in PAIR_IDS:
        if pid in pairs:
            pairs[pid]["airtable"]["base_id"] = base_id
            pairs[pid]["airtable"]["table_id"] = table_id
            pairs[pid]["airtable"]["fields"]["pair"] = "Пара"
    factory_path.write_text(json.dumps(pairs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-delete-legacy", action="store_true")
    args = parser.parse_args()

    env = load_runtime_env()
    token = env["AIRTABLE_ACCESS_TOKEN"]
    base_id = env.get("AIRTABLE_BASE_ID") or BASE_ID

    unified_id = find_table_id(token, base_id, TABLE_NAME)
    if not unified_id and not args.dry_run:
        unified_id = create_unified_table(token, base_id)
    elif not unified_id:
        unified_id = "(new)"

    to_create: list[dict] = []
    legacy_delete: dict[str, list[str]] = {pid: [] for pid in PAIR_IDS}
    seen_names: set[str] = set()

    for pair_id in PAIR_IDS:
        legacy_table = pair_config(pair_id)["airtable"]["table_id"]
        if legacy_table == unified_id and unified_id != "(new)":
            # already migrated config — read from unified with filter
            formula = urllib.parse.quote("{Пара}='" + pair_id + "'")
            url = f"https://api.airtable.com/v0/{base_id}/{unified_id}?filterByFormula={formula}"
            existing = http_json("GET", url, headers={"Authorization": f"Bearer {token}"})
            for rec in existing.get("records", []):
                seen_names.add(rec.get("fields", {}).get("Name", ""))
            continue
        records = list_all_records(token, base_id, LEGACY_TABLES[pair_id])
        for rec in records:
            name = rec.get("fields", {}).get("Name", "")
            if not name or name in seen_names:
                continue
            seen_names.add(name)
            to_create.append({"fields": map_fields(rec, pair_id), "legacy": {"pair": pair_id, "id": rec["id"], "table": LEGACY_TABLES[pair_id]}})
            legacy_delete[pair_id].append(rec["id"])

    plan = {
        "unified_table": unified_id,
        "to_create": len(to_create),
        "legacy_delete": {k: len(v) for k, v in legacy_delete.items()},
    }
    print(json.dumps({"phase": "plan", **plan}, ensure_ascii=False), flush=True)

    if args.dry_run:
        print(json.dumps({"dry_run": True, **plan}, ensure_ascii=False, indent=2))
        return 0

    if not isinstance(unified_id, str) or unified_id == "(new)":
        raise SystemExit("Unified table id missing")

    if not to_create:
        update_accounts_pairs(unified_id, base_id)
        update_factory_pairs(unified_id, base_id)
        print(json.dumps({"status": "already_migrated", "table_id": unified_id}, indent=2))
        return 0

    rows = [item["fields"] for item in to_create]
    created = batch_create(token, base_id, unified_id, rows)

    deleted_total = 0
    if not args.skip_delete_legacy:
        for pair_id in PAIR_IDS:
            ids = legacy_delete[pair_id]
            if ids:
                deleted_total += batch_delete(token, base_id, LEGACY_TABLES[pair_id], ids)

    update_accounts_pairs(unified_id, base_id)
    update_factory_pairs(unified_id, base_id)

    summary = {
        "status": "ok",
        "unified_table_id": unified_id,
        "created": len(created),
        "deleted_legacy": deleted_total,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
