"""Очередь публикации из Dropbox /Content_Plan/Queue (без Airtable)."""

from __future__ import annotations

import json
from typing import Any

from dropbox_client import download_file_text, list_folder_entries
from publish_config import queue_airtable_config, queue_dropbox_root


def _slide_count(entries: list[dict]) -> int:
    n = 0
    for e in entries:
        if e.get(".tag") != "file":
            continue
        name = e.get("name", "").lower()
        if name.startswith("slide-") and name.endswith((".png", ".jpg", ".jpeg", ".webp")):
            n += 1
    return n


def folder_is_ready(entries: list[dict]) -> bool:
    count = _slide_count(entries)
    return count in (6, 7, 9)


def _parse_manifest(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        obj = json.loads(raw)
        return obj if isinstance(obj, dict) else {}
    except json.JSONDecodeError:
        return {}


def fields_from_dropbox_folder(
    *,
    name: str,
    folder_path: str,
    caption_text: str,
    manifest: dict[str, Any],
    field_map: dict[str, str],
) -> dict[str, str]:
    tiktok = manifest.get("tiktok") if isinstance(manifest.get("tiktok"), dict) else {}
    title = str(tiktok.get("title") or manifest.get("tiktokTitle") or "").strip()
    desc = str(tiktok.get("description") or manifest.get("tiktokDescription") or "").strip()
    caption = caption_text.strip()
    if not caption and manifest.get("instagram_caption"):
        caption = str(manifest["instagram_caption"]).strip()

    fields: dict[str, str] = {
        field_map["name"]: name,
        field_map["instagram_caption"]: caption[:100000],
        field_map["tiktok_title"]: title,
        field_map["tiktok_description"]: desc,
    }
    folder_key = field_map.get("folder_path")
    if folder_key:
        fields[folder_key] = folder_path
    return fields


def list_dropbox_queue_records(token: str, *, cfg: dict | None = None) -> list[dict]:
    """Synthetic Airtable-shaped records from Queue subfolders."""
    root = queue_dropbox_root(cfg)
    at = queue_airtable_config(cfg)
    field_map = at["fields"]
    entries = list_folder_entries(token, root)
    records: list[dict] = []

    for ent in entries:
        if ent.get(".tag") != "folder":
            continue
        name = str(ent.get("name") or "").strip()
        if not name or name.startswith("."):
            continue
        folder_path = f"{root}/{name}"
        try:
            files = list_folder_entries(token, folder_path)
        except Exception:
            continue
        if not folder_is_ready(files):
            continue

        manifest_path = f"{folder_path}/manifest.json"
        caption_path = f"{folder_path}/caption.txt"
        manifest = _parse_manifest(download_file_text(token, manifest_path))
        caption_text = download_file_text(token, caption_path) or ""
        created = str(manifest.get("createdAt") or ent.get("client_modified") or name)

        records.append(
            {
                "id": f"dropbox:{name}",
                "createdTime": created,
                "fields": fields_from_dropbox_folder(
                    name=name,
                    folder_path=folder_path,
                    caption_text=caption_text,
                    manifest=manifest,
                    field_map=field_map,
                ),
            }
        )

    records.sort(key=lambda r: str(r.get("fields", {}).get(field_map["name"], "")))
    return records


def apply_pick(ready: list[dict], pick: str) -> list[dict]:
    if not ready:
        return []
    mode = (pick or "fifo").strip().lower()
    if mode == "bottom":
        return [ready[-1]]
    return [ready[0]]
