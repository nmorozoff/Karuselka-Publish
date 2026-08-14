#!/usr/bin/env python3
"""Пометить карусели опубликованными: worker-state + purge Airtable/Dropbox."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from dropbox_client import get_access_token  # noqa: E402
from publish_cleanup import purge_carousel_by_name  # noqa: E402
from publish_config import load_runtime_env, pair_config  # noqa: E402
from publish_engine import delete_dropbox_folder, list_queue_records  # noqa: E402
from worker_state import load_state, save_state  # noqa: E402


def _published_key(pair_id: str) -> str:
    return "published" if pair_id == "pair1" else f"published_{pair_id}"


def _find_record(env: dict[str, str], name: str) -> dict | None:
    pair = pair_config("pair1")
    for rec in list_queue_records(env, pair):
        if rec.get("fields", {}).get("Name") == name:
            return rec
    return None


def mark_done(
    names: list[str],
    *,
    pair_id: str,
    dry_run: bool,
    purge_assets: bool,
) -> dict:
    env = load_runtime_env()
    import os

    token = get_access_token(env)
    state_token = token if os.environ.get("WORKER_STATE_BACKEND") == "dropbox" else None
    state = load_state(state_token)

    key = _published_key(pair_id)
    published = set(state.get(key) or [])
    results = []

    for name in names:
        entry: dict = {"name": name, "pair": pair_id}
        rec = _find_record(env, name)
        entry["airtable_found"] = bool(rec)

        if not dry_run:
            published.add(name)
            state.get("failed", {}).pop(name, None)
            state.get("partial_published", {}).pop(name, None)
            state.setdefault("last_run", {})[name] = {
                "at": datetime.now(timezone.utc).isoformat(),
                "ok": True,
                "manual_done": True,
            }

        if purge_assets and rec and not dry_run:
            try:
                purge = purge_carousel_by_name(
                    env=env,
                    queue_pair=pair_config("pair1"),
                    carousel_name=name,
                    fields=rec.get("fields", {}),
                    record_id=rec["id"],
                    dropbox_token=token,
                    delete_dropbox_folder=delete_dropbox_folder,
                )
                entry["purge"] = purge.get("cleanup", {})
            except Exception as exc:  # noqa: BLE001
                entry["purge_error"] = str(exc)
        elif purge_assets and rec and dry_run:
            entry["purge"] = {"dry_run": True}
        elif purge_assets and not rec:
            entry["purge"] = {"skipped": "not in airtable"}

        results.append(entry)

    if not dry_run:
        state[key] = sorted(published)
        save_state(state, state_token)

    return {"dry_run": dry_run, "marked": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Mark carousels manually published + cleanup")
    parser.add_argument("--names", nargs="+", required=True)
    parser.add_argument("--pair", default="pair1", choices=["pair1", "pair2", "pair3"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-purge", action="store_true", help="Only worker-state, keep Airtable/Dropbox")
    args = parser.parse_args()

    out = mark_done(
        args.names,
        pair_id=args.pair,
        dry_run=args.dry_run,
        purge_assets=not args.no_purge,
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
