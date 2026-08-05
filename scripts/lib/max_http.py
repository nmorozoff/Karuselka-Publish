"""MAX Bot API client (platform-api2.max.ru)."""

from __future__ import annotations

import json
import ssl
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://platform-api2.max.ru"


def api_request(
    token: str,
    method: str,
    path: str,
    *,
    query: dict | None = None,
    body: dict | None = None,
    insecure_tls: bool = False,
) -> dict:
    url = API_BASE + path
    if query:
        url += "?" + urlencode({k: str(v) for k, v in query.items() if v is not None})

    headers = {"Authorization": token}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = Request(url, data=data, headers=headers, method=method)
    ctx = ssl._create_unverified_context() if insecure_tls else None
    try:
        with urlopen(req, timeout=60, context=ctx) as resp:
            text = resp.read().decode("utf-8")
            return json.loads(text) if text else {}
    except HTTPError as exc:
        err = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"MAX API {exc.code} {path}: {err}") from exc


def send_message(
    token: str,
    text: str,
    *,
    chat_id: int,
    format_mode: str | None = "markdown",
    insecure_tls: bool = False,
) -> dict:
    payload: dict = {"text": text, "notify": True}
    if format_mode:
        payload["format"] = format_mode
    return api_request(
        token,
        "POST",
        "/messages",
        query={"chat_id": chat_id},
        body=payload,
        insecure_tls=insecure_tls,
    )
