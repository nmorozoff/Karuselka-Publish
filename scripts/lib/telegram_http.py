"""Telegram API: direct connection, no proxy."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

from http_client import urlopen


def api(token: str, method: str, params: dict | None = None, *, timeout: int = 45) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    if params:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())
