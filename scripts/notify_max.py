#!/usr/bin/env python3
"""Send a plain-text or structured report to MAX bot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from max_notify import notify_from_publish_result, send_message  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Send report to MAX bot")
    parser.add_argument("--text", help="Free message body (markdown ok)")
    parser.add_argument("--pair", default="pair1", choices=["pair1", "pair2", "pair3"])
    parser.add_argument("--result-file", help="Path to worker-last-run.json (or result JSON)")
    parser.add_argument("--next-folder", default="очередь пуста")
    args = parser.parse_args()

    if args.text:
        send_message(args.text)
        print("OK")
        return

    if args.result_file:
        path = Path(args.result_file)
        result = json.loads(path.read_text(encoding="utf-8"))
        if result.get("results"):
            record = result["results"][0]
            carousel_name = record.get("name", "unknown")
        elif result.get("errors"):
            err_item = result["errors"][0]
            carousel_name = err_item.get("name", "unknown")
            record = {
                "name": carousel_name,
                "error": err_item.get("error", result.get("message", "publish failed")),
            }
        else:
            record = result
            carousel_name = record.get("name", "unknown")
        pair_label = args.pair
        notify_from_publish_result(
            pair_id=args.pair,
            pair_label=pair_label,
            carousel_name=carousel_name,
            result=record,
            next_folder=args.next_folder,
        )
        print("OK")
        return

    parser.error("Use --text or --result-file")


if __name__ == "__main__":
    main()
