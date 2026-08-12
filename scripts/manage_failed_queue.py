#!/usr/bin/env python3
"""Классификация, очистка failed и purge мусорных каруселей из очереди."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from dropbox_client import get_access_token  # noqa: E402
from publish_config import load_runtime_env, pair_config  # noqa: E402
from publish_engine import delete_dropbox_folder, list_queue_records  # noqa: E402
from publish_failure import classify_failure_message  # noqa: E402
from publish_cleanup import purge_carousel_by_name  # noqa: E402
from worker_state import load_state, save_state  # noqa: E402

PURGE_CATEGORIES = frozenset(
    {
        "instagram_format",
        "tiktok_spam",
        "bad_request",
    }
)
CLEAR_CATEGORIES = frozenset({"rate_limit", "transient", "unknown"})


def _state_token(env: dict[str, str]) -> str:
    import os

    if os.environ.get("WORKER_STATE_BACKEND") == "dropbox":
        return get_access_token(env)
    return ""


def _find_record(env: dict[str, str], name: str) -> tuple[str, dict] | None:
    pair = pair_config("pair1")
    for rec in list_queue_records(env, pair):
        if rec.get("fields", {}).get("Name") == name:
            return "queue", rec
    return None


def classify_failed(state: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for name, meta in sorted((state.get("failed") or {}).items()):
        err = meta.get("error", "") if isinstance(meta, dict) else str(meta)
        cat = meta.get("category") if isinstance(meta, dict) and meta.get("category") else None
        if not cat:
            cat = classify_failure_message(err).get("category", "unknown")
        out.setdefault(str(cat), []).append(name)
    return out


def cmd_classify(state: dict) -> int:
    groups = classify_failed(state)
    print(json.dumps(groups, ensure_ascii=False, indent=2))
    for cat, names in sorted(groups.items()):
        print(f"\n{cat}: {len(names)}")
        for n in names:
            print(f"  {n}")
    return 0


def _names_for_action(state: dict, args: argparse.Namespace) -> list[str]:
    if args.names:
        return list(args.names)
    groups = classify_failed(state)
    cats = set(args.category or [])
    if args.purge_junk:
        cats |= PURGE_CATEGORIES
    if args.clear_retryable:
        cats |= CLEAR_CATEGORIES
    names: list[str] = []
    for cat in cats:
        names.extend(groups.get(cat, []))
    if args.legacy:
        for name in (state.get("failed") or {}):
            if "202606" in name:
                names.append(name)
    return sorted(set(names))


def cmd_clear(state: dict, names: list[str], *, dry_run: bool, token: str) -> dict:
    removed = []
    for name in names:
        if name not in (state.get("failed") or {}):
            continue
        if dry_run:
            removed.append(name)
            continue
        state.get("failed", {}).pop(name, None)
        removed.append(name)
    if not dry_run and removed:
        save_state(state, token or None)
    return {"action": "clear_failed", "dry_run": dry_run, "removed": removed}


def cmd_purge(
    env: dict[str, str],
    state: dict,
    names: list[str],
    *,
    dry_run: bool,
    token: str,
) -> dict:
    purged = []
    missing = []
    errors = []
    for name in names:
        found = _find_record(env, name)
        if not found:
            missing.append(name)
            if not dry_run:
                state.get("failed", {}).pop(name, None)
            continue
        pair_id, rec = found
        if dry_run:
            purged.append({"name": name, "pair": pair_id, "dry_run": True})
            continue
        try:
            # purge из единой очереди; Zernio-пара при purge не важна — используем pair1 как шаблон
            result = purge_carousel_by_name(
                env=env,
                queue_pair=pair_config("pair1"),
                carousel_name=name,
                fields=rec.get("fields", {}),
                record_id=rec["id"],
                dropbox_token=token,
                delete_dropbox_folder=delete_dropbox_folder,
            )
            state.get("failed", {}).pop(name, None)
            state.get("partial_published", {}).pop(name, None)
            purged.append({"name": name, "pair": pair_id, **result})
        except Exception as exc:  # noqa: BLE001
            errors.append({"name": name, "error": str(exc)})
    if not dry_run and (purged or missing):
        save_state(state, token or None)
    return {
        "action": "purge",
        "dry_run": dry_run,
        "purged": purged,
        "missing_record": missing,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Управление failed-очередью Karuselka Publish")
    parser.add_argument(
        "command",
        choices=["classify", "clear", "purge", "reconcile"],
        help="classify — сводка; clear — убрать из failed; purge — удалить Airtable+Dropbox; reconcile — purge junk + clear retryable",
    )
    parser.add_argument("--names", nargs="+", help="Конкретные crsl_...")
    parser.add_argument(
        "--category",
        nargs="+",
        help="Категории: rate_limit, instagram_format, tiktok_spam, bad_request, ...",
    )
    parser.add_argument("--purge-junk", action="store_true", help="purge категорий без retry")
    parser.add_argument("--clear-retryable", action="store_true", help="clear rate_limit/transient")
    parser.add_argument("--legacy", action="store_true", help="включить crsl_202606*")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_runtime_env()
    token = get_access_token(env)
    state_token = _state_token(env)
    state = load_state(state_token or None)

    if args.command == "classify":
        raise SystemExit(cmd_classify(state))

    if args.command == "reconcile":
        purge_names = _names_for_action(
            state,
            argparse.Namespace(
                names=None,
                category=None,
                purge_junk=True,
                clear_retryable=False,
                legacy=True,
            ),
        )
        clear_names = _names_for_action(
            state,
            argparse.Namespace(
                names=None,
                category=None,
                purge_junk=False,
                clear_retryable=True,
                legacy=False,
            ),
        )
        purge_result = cmd_purge(env, state, purge_names, dry_run=args.dry_run, token=token)
        state = load_state(state_token or None)
        clear_result = cmd_clear(state, clear_names, dry_run=args.dry_run, token=state_token)
        print(
            json.dumps(
                {"purge": purge_result, "clear": clear_result},
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    names = _names_for_action(state, args)
    if not names:
        print(json.dumps({"status": "empty", "message": "no names matched"}, ensure_ascii=False))
        return

    if args.command == "clear":
        result = cmd_clear(state, names, dry_run=args.dry_run, token=state_token)
    else:
        result = cmd_purge(env, state, names, dry_run=args.dry_run, token=token)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
