#!/usr/bin/env python3
"""Статус очереди публикации: Airtable + worker-state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from publish_config import MEMORY  # noqa: E402
from publish_engine import get_queue_summary  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", choices=["pair1", "pair2", "pair3"], help="Показать только одну пару")
    args = parser.parse_args()

    summary = get_queue_summary()
    if args.pair and args.pair in summary.get("pairs", {}):
        summary = {
            "at": summary["at"],
            "pair": args.pair,
            **summary["pairs"][args.pair],
            "worker_state_path": summary.get("worker_state_path"),
        }
    out = MEMORY / "output" / "queue-status.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
