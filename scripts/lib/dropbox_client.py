"""Dropbox helpers for publish worker."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from http_client import urlopen


def get_access_token(env: dict[str, str]) -> str:
    if env.get("DROPBOX_ACCESS_TOKEN"):
        return env["DROPBOX_ACCESS_TOKEN"]
    key = env.get("DROPBOX_APP_KEY", "")
    secret = env.get("DROPBOX_APP_SECRET", "")
    refresh = env.get("DROPBOX_REFRESH_TOKEN", "")
    if not (key and secret and refresh):
        raise SystemExit("Dropbox: set DROPBOX_ACCESS_TOKEN or OAuth trio in dropbox.env.local")
    body = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh,
            "client_id": key,
            "client_secret": secret,
        }
    ).encode()
    req = urllib.request.Request("https://api.dropboxapi.com/oauth2/token", data=body, method="POST")
    with urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    token = data.get("access_token")
    if not token:
        raise SystemExit(f"Dropbox token refresh failed: {data}")
    return token


def create_folder(path: str, token: str) -> None:
    req = urllib.request.Request(
        "https://api.dropboxapi.com/2/files/create_folder_v2",
        data=json.dumps({"autorename": False, "path": path}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", errors="replace")
        if e.code == 409 and "conflict" in text:
            return
        raise SystemExit(f"Dropbox folder error: {text}") from e
    except RuntimeError as exc:
        if "409" in str(exc) and "conflict" in str(exc).lower():
            return
        raise


def upload_file(path: str, content: bytes, token: str) -> None:
    req = urllib.request.Request(
        "https://content.dropboxapi.com/2/files/upload",
        data=content,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": json.dumps(
                {
                    "autorename": False,
                    "mode": "overwrite",
                    "mute": False,
                    "path": path,
                    "strict_conflict": False,
                }
            ),
        },
        method="POST",
    )
    with urlopen(req, timeout=120) as resp:
        resp.read()


def upload_directory(local_dir: Path, dropbox_folder: str, token: str) -> int:
    create_folder(dropbox_folder, token)
    count = 0
    for fp in sorted(local_dir.rglob("*")):
        if not fp.is_file():
            continue
        rel = fp.relative_to(local_dir).as_posix()
        upload_file(f"{dropbox_folder.rstrip('/')}/{rel}", fp.read_bytes(), token)
        count += 1
    return count


def ensure_shared_link(path: str, token: str) -> str:
    """Return dl=1 URL for Zernio media fetch."""

    def list_links() -> str:
        req = urllib.request.Request(
            "https://api.dropboxapi.com/2/sharing/list_shared_links",
            data=json.dumps({"path": path, "direct_only": True}).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=60) as resp:
                links = json.loads(resp.read().decode()).get("links", [])
            return links[0].get("url", "") if links else ""
        except (urllib.error.HTTPError, RuntimeError):
            return ""

    url = list_links()
    if not url:
        req = urllib.request.Request(
            "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings",
            data=json.dumps(
                {
                    "path": path,
                    "settings": {
                        "requested_visibility": "public",
                        "audience": "public",
                        "access": "viewer",
                    },
                }
            ).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=60) as resp:
                url = json.loads(resp.read().decode()).get("url", "")
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", errors="replace")
            if "shared_link_already_exists" not in text and e.code != 409:
                raise SystemExit(f"Dropbox create_shared_link error: {text}") from e
            url = list_links()
        except RuntimeError as exc:
            if "409" not in str(exc) and "shared_link_already_exists" not in str(exc):
                raise
            url = list_links()

    if not url:
        raise SystemExit(f"Dropbox shared link missing for {path}")
    if "?dl=" in url:
        return url.replace("?dl=0", "?dl=1")
    return f"{url}?dl=1" if "?" not in url else url.replace("dl=0", "dl=1")


def get_temporary_link(path: str, token: str) -> str:
    """Direct download URL (4h TTL). Instagram rejects shared links with application/binary."""
    req = urllib.request.Request(
        "https://api.dropboxapi.com/2/files/get_temporary_link",
        data=json.dumps({"path": path}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    link = data.get("link")
    if not link:
        raise SystemExit(f"Dropbox get_temporary_link missing link for {path}")
    return link


def ensure_media_link(path: str, token: str) -> str:
    """Video → temporary direct link (video/mp4); images → shared dl=1 link."""
    if Path(path).suffix.lower() == ".mp4":
        return get_temporary_link(path, token)
    return ensure_shared_link(path, token)
