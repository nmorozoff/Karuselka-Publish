#!/usr/bin/env python3
"""Автоматический воркер публикации (локально или cloud через publish_engine)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from publish_config import MEMORY  # noqa: E402
from publish_engine import run_publish_batch  # noqa: E402


def _write_and_print(result: dict) -> None:
    out = MEMORY / "output" / "worker-last-run.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("status") == "error" and not result.get("results"):
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", default="pair1", choices=["pair1", "pair2", "pair3"])
    parser.add_argument(
        "--accounts",
        choices=["pair1", "pair2", "pair3"],
        help="Zernio IG/TikTok (default = --pair)",
    )
    parser.add_argument(
        "--queue",
        choices=["pair1", "pair2", "pair3"],
        help="Airtable/Dropbox очередь (default = --pair)",
    )
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--name", help="Конкретная карусель по Name")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--dry-run-first",
        action="store_true",
        help="Сначала dry-run, затем реальная публикация только если он прошёл",
    )
    parser.add_argument("--skip-cleanup", action="store_true")
    parser.add_argument("--tiktok-only", action="store_true")
    parser.add_argument("--include-published", action="store_true")
    parser.add_argument("--retry-failed", action="store_true", help="Повторить карусели из failed")
    parser.add_argument(
        "--include-needs-human",
        action="store_true",
        help="При --retry-failed включать spam/format/ownership (обычно бесполезно)",
    )
    args = parser.parse_args()

    if args.dry_run_first:
        dry_result = run_publish_batch(
            pair_id=args.pair,
            accounts_pair_id=args.accounts or args.pair,
            queue_pair_id=args.queue or args.pair,
            limit=args.limit,
            name=args.name,
            dry_run=True,
            skip_cleanup=True,
            tiktok_only=args.tiktok_only,
            include_published=args.include_published,
            retry_failed=args.retry_failed,
            include_needs_human=args.include_needs_human,
        )
        if dry_result.get("status") == "error":
            dry_result["mode"] = "dry_run_first"
            dry_result["aborted"] = True
            dry_result["reason"] = "dry run failed"
            try:
                from publish_incidents import log_incident

                err = dry_result.get("errors") or dry_result.get("message") or "dry run failed"
                log_incident(
                    pair=args.pair,
                    stage="dry_run",
                    error=str(err)[:4000],
                    context={"worker_last_run": "publish-memory/output/worker-last-run.json"},
                )
            except Exception:
                pass
            _write_and_print(dry_result)
            raise SystemExit(1)
        if dry_result.get("status") == "empty":
            dry_result["mode"] = "dry_run_first"
            dry_result["aborted"] = True
            dry_result["reason"] = "queue empty"
            try:
                from publish_incidents import log_incident

                log_incident(
                    pair=args.pair,
                    stage="queue",
                    error="queue empty at dry-run-first",
                )
            except Exception:
                pass
            _write_and_print(dry_result)
            return

    result = run_publish_batch(
        pair_id=args.pair,
        accounts_pair_id=args.accounts or args.pair,
        queue_pair_id=args.queue or args.pair,
        limit=args.limit,
        name=args.name,
        dry_run=args.dry_run,
        skip_cleanup=args.skip_cleanup,
        tiktok_only=args.tiktok_only,
        include_published=args.include_published,
        retry_failed=args.retry_failed,
        include_needs_human=args.include_needs_human,
    )
    _write_and_print(result)


if __name__ == "__main__":
    main()
