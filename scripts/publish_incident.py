#!/usr/bin/env python3
"""Log a publish pipeline incident for Fixic."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from publish_incidents import list_open_incidents, log_incident  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Log publish incident to pipeline-fix-queue.md")
    parser.add_argument("--pair", choices=["pair1", "pair2", "pair3"])
    parser.add_argument("--stage", help="preflight|queue|dry_run|publish|notify|automation")
    parser.add_argument("--error", help="Error message or summary")
    parser.add_argument("--carousel", default="")
    parser.add_argument("--context-json", default="{}", help="JSON object with extra context")
    parser.add_argument("--list-open", action="store_true", help="List open incidents and exit")
    args = parser.parse_args()

    if args.list_open:
        print(json.dumps(list_open_incidents(), ensure_ascii=False, indent=2))
        return

    if not args.pair or not args.stage or not args.error:
        parser.error("--pair, --stage, and --error are required unless using --list-open")

    context = json.loads(args.context_json)
    inc_id = log_incident(
        pair=args.pair,
        stage=args.stage,
        error=args.error,
        carousel=args.carousel or None,
        context=context,
    )
    print(json.dumps({"incident_id": inc_id, "status": "open"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
