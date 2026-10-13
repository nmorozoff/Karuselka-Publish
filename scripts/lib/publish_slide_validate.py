"""Instagram carousel slide checks before Zernio (Meta aspect 0.8–1.91)."""

from __future__ import annotations

import json
import struct
import urllib.request

from http_client import urlopen

# width / height — same bounds as shared/KARUSELKA-FACTORY-PUBLISH-SPEC.md
IG_MIN_ASPECT = 0.8
IG_MAX_ASPECT = 1.91


def _png_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    w, h = struct.unpack(">II", data[16:24])
    if w <= 0 or h <= 0:
        raise ValueError("invalid PNG IHDR")
    return w, h


def _download_bytes(token: str, path: str) -> bytes:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/download",
        headers={"Authorization": f"Bearer {token}", "Dropbox-API-Arg": json.dumps({"path": path})},
        method="POST",
    )
    with urlopen(req, timeout=90) as resp:
        return resp.read()


def validate_instagram_slides(token: str, slide_paths: list[str]) -> None:
    """Raise RuntimeError if any slide is outside Instagram carousel aspect bounds."""
    sizes: list[tuple[str, int, int, float]] = []
    for path in slide_paths:
        name = path.rsplit("/", 1)[-1]
        try:
            raw = _download_bytes(token, path)
            w, h = _png_dimensions(raw)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"instagram_format: cannot read slide {name}: {exc}"
            ) from exc
        ratio = w / h
        sizes.append((name, w, h, ratio))

    ref = sizes[0][1:3]
    problems: list[str] = []
    for name, w, h, ratio in sizes:
        if (w, h) != ref:
            problems.append(f"{name}: size {w}x{h} differs from {ref[0]}x{ref[1]}")
        if ratio < IG_MIN_ASPECT or ratio > IG_MAX_ASPECT:
            problems.append(f"{name}: aspect {ratio:.4f} outside {IG_MIN_ASPECT}–{IG_MAX_ASPECT}")

    if problems:
        detail = "; ".join(problems)
        raise RuntimeError(f"instagram_format: {detail}")
