"""Очистка после публикации: Airtable + Dropbox Content_Plan + Ready_Carousel."""

from __future__ import annotations

from typing import Any

from airtable_client import delete_record
from publish_config import resolve_carousel_dropbox_path


def assert_zernio_ok(res: dict[str, Any], platform: str) -> None:
    if res.get("dry_run"):
        return
    if res.get("error") or res.get("errors"):
        raise RuntimeError(f"Zernio {platform} error: {_zernio_error_summary(res)}")
    post_id = res.get("_id") or res.get("id")
    if post_id:
        return
    msg = str(res.get("message") or res.get("status") or "")
    if msg and any(x in msg.lower() for x in ("error", "fail", "invalid")):
        raise RuntimeError(f"Zernio {platform} rejected: {_zernio_error_summary(res)}")
    if res.get("post") and isinstance(res["post"], dict) and res["post"].get("_id"):
        post = res["post"]
        for plat in post.get("platforms") or []:
            if not isinstance(plat, dict):
                continue
            ps = str(plat.get("status") or "").lower()
            if ps in ("failed", "error"):
                err = plat.get("errorMessage") or plat.get("error") or msg
                raise RuntimeError(f"Zernio {platform} error: {err}")
        return
    if not res:
        raise RuntimeError(f"Zernio {platform}: empty response")


def _zernio_error_summary(res: dict[str, Any]) -> str:
    """Краткое сообщение об ошибке Zernio без полного JSON."""
    post = res.get("post")
    if isinstance(post, dict):
        for plat in post.get("platforms") or []:
            if not isinstance(plat, dict):
                continue
            err = plat.get("errorMessage") or plat.get("error")
            if err:
                return str(err)[:500]
    for key in ("error", "message", "detail"):
        val = res.get(key)
        if val:
            return str(val)[:500]
    return str(res)[:500]


def cleanup_carousel_assets(
    *,
    env: dict[str, str],
    queue_pair: dict,
    record_id: str | None,
    dropbox_token: str,
    dropbox_folder: str,
    carousel_name: str,
    delete_dropbox_folder,
) -> dict[str, bool]:
    """Удалить Airtable-строку, папку карусели и Ready_Carousel."""
    out = {"airtable": False, "dropbox": False, "ready_carousel": False}
    if record_id:
        delete_record(
            env["AIRTABLE_ACCESS_TOKEN"],
            queue_pair["airtable"]["base_id"],
            queue_pair["airtable"]["table_id"],
            record_id,
        )
        out["airtable"] = True
    delete_dropbox_folder(dropbox_token, dropbox_folder)
    out["dropbox"] = True
    out["ready_carousel"] = delete_dropbox_folder(
        dropbox_token, f"/Ready_Carousel/{carousel_name}", optional=True
    )
    return out


def purge_carousel_by_name(
    *,
    env: dict[str, str],
    queue_pair: dict,
    carousel_name: str,
    fields: dict,
    record_id: str,
    dropbox_token: str,
    delete_dropbox_folder,
) -> dict[str, Any]:
    dropbox_folder = resolve_carousel_dropbox_path(queue_pair, fields, carousel_name)
    cleanup = cleanup_carousel_assets(
        env=env,
        queue_pair=queue_pair,
        record_id=record_id,
        dropbox_token=dropbox_token,
        dropbox_folder=dropbox_folder,
        carousel_name=carousel_name,
        delete_dropbox_folder=delete_dropbox_folder,
    )
    return {"name": carousel_name, "dropbox_folder": dropbox_folder, "cleanup": cleanup}
