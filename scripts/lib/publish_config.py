"""Shared config for karuselka-publish worker."""

from __future__ import annotations

import json
import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
MEMORY = WORKSPACE / "publish-memory"


def load_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def accounts_pairs_path() -> Path:
    raw = os.environ.get("ACCOUNTS_PAIRS_PATH", "")
    if raw:
        return Path(raw)
    return MEMORY / "accounts-pairs.json"


def load_accounts_pairs() -> dict:
    return json.loads(accounts_pairs_path().read_text(encoding="utf-8"))


def queue_dropbox_root(cfg: dict | None = None) -> str:
    """Единая папка очереди для всех каруселей (все пары)."""
    data = cfg if cfg is not None else load_accounts_pairs()
    root = (
        data.get("queue_dropbox_root")
        or os.environ.get("DROPBOX_QUEUE_ROOT")
        or "/Content_Plan/Queue"
    )
    return str(root).rstrip("/")


def merge_env(*paths: Path) -> dict[str, str]:
    merged: dict[str, str] = dict(os.environ)
    for p in paths:
        merged.update(load_dotenv(p))
    return merged


def load_runtime_env() -> dict[str, str]:
    """Cloud: только os.environ. Локально: publish-memory/*.env.local + os.environ."""
    if os.environ.get("KARUSELKA_RUNTIME", "").lower() == "cloud":
        required = [
            "AIRTABLE_ACCESS_TOKEN",
            "DROPBOX_APP_KEY",
            "DROPBOX_APP_SECRET",
            "DROPBOX_REFRESH_TOKEN",
            "ZERNIO_API_KEY",
            "ZERNIO_INSTAGRAM_ACCOUNT_ID",
            "ZERNIO_TIKTOK_ACCOUNT_ID",
        ]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            raise RuntimeError(f"Missing cloud env: {', '.join(missing)}")
        env = dict(os.environ)
        if not env.get("MAX_BOT_TOKEN") or not (
            env.get("MAX_NOTIFY_CHAT_ID")
            or env.get("MAX_PREVIEW_CHAT_ID")
            or env.get("MAX_CHAT_ID")
        ):
            env.setdefault("MAX_NOTIFY_MISSING", "1")
        return env

    return merge_env(
        MEMORY / "airtable.env.local",
        MEMORY / "dropbox.env.local",
        MEMORY / "zernio.env.local",
        MEMORY / "max.env.local",
        MEMORY / "cloud-worker.env.local",
    )


def pair_config(pair_id: str) -> dict:
    cfg = load_accounts_pairs()
    key = pair_id if pair_id in ("pair1", "pair2", "pair3") else "pair1"
    out = dict(cfg[key])
    out.setdefault("id", key)
    unified = cfg.get("airtable_queue")
    if unified:
        at = dict(unified)
        fields = dict(at.get("fields") or {})
        fields.setdefault("pair", "Пара")
        at["fields"] = fields
        out["airtable"] = at
    return out


def queue_airtable(cfg: dict | None = None) -> dict | None:
    """Единая таблица очереди (если настроена)."""
    data = cfg if cfg is not None else load_accounts_pairs()
    return data.get("airtable_queue")


def pair_queue_airtable(pair_id: str, cfg: dict | None = None) -> dict:
    """Airtable config для пары: unified queue или legacy per-pair table."""
    data = cfg if cfg is not None else load_accounts_pairs()
    unified = data.get("airtable_queue")
    if unified:
        at = dict(unified)
        at["pair_id"] = pair_id
        return at
    key = pair_id if pair_id in ("pair1", "pair2", "pair3") else "pair1"
    return data[key]["airtable"]


def zernio_api_key(env: dict[str, str], pair: dict) -> str:
    """Zernio API key: pair2 может иметь свой, pair3 — отдельные IG/TT."""
    pid = pair.get("id", "pair1")
    if pid == "pair3":
        # Pair3 может использовать разные ключи для IG и TikTok.
        # Возвращаем fallback-цепочку; caller выбирает нужный через zernio_api_key_for_platform.
        return (
            env.get("ZERNIO_PAIR3_API_KEY", "")
            or env.get("ZERNIO_PAIR3_INSTAGRAM_API_KEY", "")
            or env.get("ZERNIO_PAIR3_TIKTOK_API_KEY", "")
            or env.get("ZERNIO_API_KEY", "")
        )
    if pid == "pair2":
        return env.get("ZERNIO_PAIR2_API_KEY") or env.get("ZERNIO_API_KEY", "")
    return env.get("ZERNIO_API_KEY", "")


def zernio_api_key_for_platform(env: dict[str, str], pair: dict, platform: str) -> str:
    """API key для конкретной платформы (instagram/tiktok)."""
    pid = pair.get("id", "pair1")
    platform = platform.lower()
    if pid == "pair3":
        specific = env.get(f"ZERNIO_PAIR3_{platform.upper()}_API_KEY", "")
        if specific:
            return specific
        return env.get("ZERNIO_PAIR3_API_KEY") or env.get("ZERNIO_API_KEY", "")
    if pid == "pair2":
        return env.get("ZERNIO_PAIR2_API_KEY") or env.get("ZERNIO_API_KEY", "")
    return env.get("ZERNIO_API_KEY", "")


def zernio_instagram_account_id(pair: dict, env: dict[str, str]) -> str:
    acc = pair.get("zernio_instagram_account_id") or env.get("ZERNIO_INSTAGRAM_ACCOUNT_ID", "")
    if not acc or "FILL" in str(acc):
        raise RuntimeError(f"Instagram account id missing for {pair.get('id', 'pair')}")
    return acc


def zernio_tiktok_account_id(pair: dict, env: dict[str, str]) -> str:
    acc = pair.get("zernio_tiktok_account_id") or env.get("ZERNIO_TIKTOK_ACCOUNT_ID", "")
    if not acc or "FILL" in str(acc):
        raise RuntimeError(f"TikTok account id missing for {pair.get('id', 'pair')}")
    return acc


def resolve_carousel_dropbox_path(pair: dict, fields: dict, name: str) -> str:
    """Путь к папке карусели: единая Queue, затем legacy pair root."""
    folder_field = pair.get("airtable", {}).get("fields", {}).get("folder_path")
    if folder_field and fields.get(folder_field):
        path = str(fields[folder_field]).strip()
        return path if path.startswith("/") else f"/{path}"
    return f"{queue_dropbox_root()}/{name}"
