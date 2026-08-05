#!/usr/bin/env python3
"""Materialize publish-memory/*.env.local from Cursor Cloud Secrets.

Run at Cloud Agent install / before scheduled publish:
  python3 scripts/materialize_cloud_env.py
  python3 scripts/materialize_cloud_env.py --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cloud_preflight import run_preflight  # noqa: E402
from publish_cloud_env import WORKSPACE, materialize_env_files  # noqa: E402

CLOUD_DEFAULTS = {
    "WORKER_STATE_BACKEND": "dropbox",
    "WORKER_STATE_DROPBOX_PATH": "/Content_Plan/.karuselka/worker-state.json",
    "PUBLISH_MODE": "grok_hook",
    "EXPECTED_IMAGE_SLIDES": "6",
}


def _apply_cloud_defaults() -> None:
    for key, val in CLOUD_DEFAULTS.items():
        os.environ.setdefault(key, val)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite existing .env.local keys from env")
    parser.add_argument("--check", action="store_true", help="Run preflight after materialize")
    args = parser.parse_args()

    _apply_cloud_defaults()
    written = materialize_env_files(force=args.force)
    out = {"written": written, "project_root": str(WORKSPACE)}
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if args.check:
        report = run_preflight()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if not report.get("ready"):
            sys.exit(2)
