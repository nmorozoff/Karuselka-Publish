#!/usr/bin/env python3
"""Статус очереди публикации: Airtable + worker-state."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS / "lib"))

from publish_config import MEMORY  # noqa: E402
from publish_engine import get_queue_summary  # noqa: E402


def main() -> None:
    summary = get_queue_summary()
    out = MEMORY / "output" / "queue-status.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
