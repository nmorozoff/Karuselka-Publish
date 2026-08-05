#!/usr/bin/env python3
"""Shared env loader for karuselka-publish — local files + Cursor Cloud Secrets."""

from __future__ import annotations

import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
MEMORY = WORKSPACE / "publish-memory"

ENV_SPECS: dict[str, list[str]] = {
    "airtable.env.local": [
        "AIRTABLE_ACCESS_TOKEN",
        "AIRTABLE_BASE_ID",
        "AIRTABLE_PAIR1_TABLE_ID",
        "AIRTABLE_PAIR2_TABLE_ID",
    ],
    "dropbox.env.local": [
        "DROPBOX_ACCESS_TOKEN",
        "DROPBOX_APP_KEY",
        "DROPBOX_APP_SECRET",
        "DROPBOX_REFRESH_TOKEN",
    ],
    "zernio.env.local": [
        "PUBLISH_MODE",
        "EXPECTED_IMAGE_SLIDES",
        "ZERNIO_API_KEY",
        "ZERNIO_PAIR2_API_KEY",
        "ZERNIO_PAIR3_API_KEY",
        "ZERNIO_PAIR3_INSTAGRAM_API_KEY",
        "ZERNIO_PAIR3_TIKTOK_API_KEY",
        "ZERNIO_INSTAGRAM_ACCOUNT_ID",
        "ZERNIO_TIKTOK_ACCOUNT_ID",
    ],
    "max.env.local": [
        "MAX_BOT_TOKEN",
        "MAX_NOTIFY_CHAT_ID",
        "MAX_PREVIEW_CHAT_ID",
        "MAX_CHAT_ID",
        "MAX_API_INSECURE_TLS",
    ],
}


def _parse_env_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.is_file():
        return data
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_env(
    filename: str,
    *,
    required: list[str] | None = None,
    memory_dir: Path | None = None,
) -> dict[str, str]:
    base = memory_dir or MEMORY
    path = base / filename
    data = _parse_env_file(path)

    for key in ENV_SPECS.get(filename, []):
        val = os.environ.get(key, "").strip()
        if val:
            data[key] = val

    if required:
        missing = [k for k in required if not data.get(k)]
        if missing:
            raise SystemExit(f"Missing {filename}: {', '.join(missing)}")

    return data


def materialize_env_files(*, memory_dir: Path | None = None, force: bool = False) -> list[str]:
    """Write publish-memory/*.env.local from os.environ (Cursor Cloud Secrets)."""
    base = memory_dir or MEMORY
    written: list[str] = []
    for filename, keys in ENV_SPECS.items():
        values = {k: os.environ.get(k, "").strip() for k in keys}
        if not any(values.values()):
            continue
        path = base / filename
        if path.exists() and not force:
            existing = _parse_env_file(path)
            merged = {**existing}
            for k, v in values.items():
                if v:
                    merged[k] = v
            values = merged
        else:
            values = {k: v for k, v in values.items() if v}
        if not values:
            continue
        lines = ["# materialized for Cursor Cloud — do not commit secrets\n"]
        for key in keys:
            if key in values:
                lines.append(f"{key}={values[key]}")
        for key, val in values.items():
            if key not in keys:
                lines.append(f"{key}={val}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(str(path.relative_to(WORKSPACE)))
    return written


def is_cloud_runtime() -> bool:
    return bool(
        os.environ.get("CURSOR_CLOUD")
        or os.environ.get("CURSOR_AGENT")
        or os.environ.get("KARUSELKA_RUNTIME", "").lower() == "cloud"
    )
