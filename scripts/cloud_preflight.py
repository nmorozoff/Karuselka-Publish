#!/usr/bin/env python3
"""Preflight checks for karuselka-publish (local + Cursor Cloud Agent)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_cloud_env import MEMORY, WORKSPACE, is_cloud_runtime, load_env  # noqa: E402


def _has_dropbox(data: dict) -> bool:
    if data.get("DROPBOX_ACCESS_TOKEN"):
        return True
    return bool(
        data.get("DROPBOX_APP_KEY")
        and data.get("DROPBOX_APP_SECRET")
        and data.get("DROPBOX_REFRESH_TOKEN")
    )


def _has_max_chat(data: dict) -> bool:
    return bool(
        data.get("MAX_NOTIFY_CHAT_ID")
        or data.get("MAX_PREVIEW_CHAT_ID")
        or data.get("MAX_CHAT_ID")
    )


def _check_file(name: str, *, required: list[str] | None = None, validator=None) -> dict:
    path = MEMORY / name
    try:
        data = load_env(name, required=required or [])
        ok = validator(data) if validator else True
        return {"ok": bool(ok), "path": str(path), "keys": sorted(data.keys())}
    except SystemExit as exc:
        return {"ok": False, "path": str(path), "error": str(exc)}


def _has_zernio(data: dict) -> bool:
    """Как минимум pair1 должен работать; pair2/pair3 могут иметь свои ключи."""
    return bool(data.get("ZERNIO_API_KEY"))


def _has_pair3(data: dict) -> bool:
    """pair3 требует либо общий pair3 ключ, либо два разных (IG/TT)."""
    if data.get("ZERNIO_PAIR3_API_KEY"):
        return True
    return bool(data.get("ZERNIO_PAIR3_INSTAGRAM_API_KEY") or data.get("ZERNIO_PAIR3_TIKTOK_API_KEY"))


def run_preflight() -> dict:
    checks: dict[str, dict] = {}
    checks["airtable"] = _check_file("airtable.env.local", required=["AIRTABLE_ACCESS_TOKEN"])
    checks["dropbox"] = _check_file("dropbox.env.local", validator=_has_dropbox)
    checks["zernio"] = _check_file("zernio.env.local", validator=_has_zernio)
    checks["zernio_pair3"] = _check_file("zernio.env.local", validator=_has_pair3)
    checks["max"] = _check_file(
        "max.env.local",
        required=["MAX_BOT_TOKEN"],
        validator=_has_max_chat,
    )

    ready = all(item.get("ok") for item in checks.values())
    return {
        "project_root": str(WORKSPACE),
        "cloud_runtime": is_cloud_runtime(),
        "ready": ready,
        "checks": checks,
    }


if __name__ == "__main__":
    report = run_preflight()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report.get("ready") else 2)
