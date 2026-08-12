#!/usr/bin/env python3
"""Перенос каруселей из Pair1/2/3 → единая /Content_Plan/Queue."""

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
sys.path.insert(0, str(SCRIPTS / "lib"))

from dropbox_client import create_folder, get_access_token  # noqa: E402
from http_client import http_json, urlopen  # noqa: E402
from publish_config import load_accounts_pairs, load_runtime_env, pair_config, queue_dropbox_root  # noqa: E402
from publish_engine import delete_dropbox_folder, list_folder_entries  # noqa: E402

LEGACY_ROOTS = ("pair1", "pair2", "pair3")


def list_all_airtable_records(env: dict[str, str], pair: dict) -> list[dict]:
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


def folder_has_slides(entries: list[dict]) -> bool:
    return any(
        e.get(".tag") == "file"
        and str(e.get("name", "")).lower().startswith("slide-")
        and str(e.get("name", "")).lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".mp4"))
        for e in entries
    )


def list_crsl_index(token: str, root: str) -> dict[str, dict]:
    """name -> {path, has_slides, entries_count}."""
    root = root.rstrip("/")
    try:
        entries = list_folder_entries(token, root)
    except Exception:
        return {}
    out: dict[str, dict] = {}
    for e in entries:
        if e.get(".tag") != "folder":
            continue
        name = str(e.get("name", ""))
        if not name.startswith("crsl_"):
            continue
        path = f"{root}/{name}"
        try:
            files = list_folder_entries(token, path)
        except Exception:
            files = []
        out[name] = {
            "path": path,
            "has_slides": folder_has_slides(files),
            "files": len([x for x in files if x.get(".tag") == "file"]),
        }
    return out


def move_dropbox_folder(token: str, from_path: str, to_path: str) -> None:
    req = urllib.request.Request(
        "https://api.dropboxapi.com/2/files/move_v2",
        data=json.dumps({"from_path": from_path, "to_path": to_path, "autorename": False}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=120) as resp:
        resp.read()


def build_plan(token: str, cfg: dict, names: set[str]) -> list[dict]:
    queue_root = queue_dropbox_root(cfg)
    queue_index = list_crsl_index(token, queue_root)
    legacy_index: dict[str, str] = {}
    for pid in LEGACY_ROOTS:
        root = cfg[pid]["dropbox_root"]
        for name, meta in list_crsl_index(token, root).items():
            if name not in legacy_index and meta.get("has_slides"):
                legacy_index[name] = meta["path"]
            elif name not in legacy_index and meta.get("files", 0) > 0:
                legacy_index[name] = meta["path"]

    # Старый плоский /Content_Plan/{name}
    flat_index = list_crsl_index(token, "/Content_Plan")
    for name, meta in flat_index.items():
        if name in (queue_root.split("/")[-1], "Pair1", "Pair2", "Pair3"):
            continue
        if name not in legacy_index and (meta.get("has_slides") or meta.get("files", 0) > 0):
            legacy_index[name] = meta["path"]

    all_names = set(names) | set(legacy_index) | set(queue_index)
    plan: list[dict] = []
    for name in sorted(all_names):
        dest = f"{queue_root}/{name}"
        q = queue_index.get(name)
        src = legacy_index.get(name)
        if q and q.get("has_slides"):
            if src and src != dest:
                plan.append({"name": name, "action": "delete_legacy", "source": src, "dest": dest})
            else:
                plan.append({"name": name, "action": "already_in_queue", "dest": dest})
        elif src:
            plan.append({"name": name, "action": "move", "source": src, "dest": dest})
        elif q:
            plan.append({"name": name, "action": "already_in_queue", "dest": dest})
        elif name in names:
            plan.append({"name": name, "action": "skip_no_source", "dest": dest})
    return plan


def execute_plan(token: str, plan: list[dict], *, dry_run: bool) -> list[dict]:
    queue_root = queue_dropbox_root()
    if not dry_run:
        create_folder(queue_root, token)

    results: list[dict] = []
    for item in plan:
        action = item["action"]
        name = item["name"]
        try:
            if action == "already_in_queue":
                results.append({**item, "status": "ok"})
            elif action == "skip_no_source":
                results.append({**item, "status": "skip"})
            elif action == "move":
                if dry_run:
                    results.append({**item, "status": "would_move"})
                else:
                    move_dropbox_folder(token, item["source"], item["dest"])
                    results.append({**item, "status": "moved"})
            elif action == "delete_legacy":
                if dry_run:
                    results.append({**item, "status": "would_delete_legacy"})
                else:
                    deleted = delete_dropbox_folder(token, item["source"], optional=True)
                    results.append({**item, "status": "deleted_legacy", "deleted": deleted})
            else:
                results.append({**item, "status": "unknown"})
        except Exception as exc:  # noqa: BLE001
            results.append({**item, "status": "error", "error": str(exc)})
        time.sleep(0.1)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate carousel folders to /Content_Plan/Queue")
    parser.add_argument("--dry-run", action="store_true", help="Only report actions")
    args = parser.parse_args()

    env = load_runtime_env()
    token = get_access_token(env)
    cfg = load_accounts_pairs()

    airtable_names: set[str] = set()
    for pair_id in LEGACY_ROOTS:
        for rec in list_all_airtable_records(env, pair_config(pair_id)):
            name = rec.get("fields", {}).get("Name")
            if name:
                airtable_names.add(name)

    print(json.dumps({"phase": "indexing", "airtable_names": len(airtable_names)}, ensure_ascii=False), flush=True)
    plan = build_plan(token, cfg, airtable_names)
    results = execute_plan(token, plan, dry_run=args.dry_run)

    summary = {
        "dry_run": args.dry_run,
        "queue_root": queue_dropbox_root(),
        "airtable_names": len(airtable_names),
        "planned": len(plan),
        "moved": sum(1 for r in results if r.get("status") == "moved"),
        "would_move": sum(1 for r in results if r.get("status") == "would_move"),
        "already_in_queue": sum(1 for r in results if r.get("action") == "already_in_queue"),
        "deleted_legacy": sum(1 for r in results if r.get("status") == "deleted_legacy"),
        "would_delete_legacy": sum(1 for r in results if r.get("status") == "would_delete_legacy"),
        "skip_no_source": sum(1 for r in results if r.get("action") == "skip_no_source"),
        "errors": [r for r in results if r.get("status") == "error"],
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
