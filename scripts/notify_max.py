#!/usr/bin/env python3
"""Send a plain-text or structured report to MAX bot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from max_notify import notify_from_publish_result, notify_publish_complete, send_message  # noqa: E402


def _record_from_worker_output(result: dict) -> tuple[str, dict]:
    """Normalize worker-last-run.json (success or batch error) into a notify record."""
    if result.get("results"):
        rec = result["results"][0]
        return rec.get("name", "unknown"), rec
    if result.get("errors"):
        err = result["errors"][0]
        name = err.get("name", "unknown")
        rec: dict = {"name": name, "error": err.get("error", "unknown error")}
        if err.get("partial_instagram"):
            rec["instagram"] = {"status": "published", "partial": True}
            rec["tiktok"] = {"error": str(err.get("error", ""))[:500]}
        return name, rec
    return result.get("name", "unknown"), result


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
        carousel_name, record = _record_from_worker_output(result)
        pair_label = args.pair
        if record.get("error") and not record.get("instagram") and not record.get("tiktok"):
            notify_publish_complete(
                pair_id=args.pair,
                pair_label=pair_label,
                carousel_name=carousel_name,
                error=str(record.get("error", ""))[:1500],
                next_folder=args.next_folder,
            )
        else:
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
