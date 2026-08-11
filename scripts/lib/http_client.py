"""HTTP для publish-пайплайна: только прямое подключение, без proxy."""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from typing import Any

_PROXY_KEYS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)


@contextmanager
def _without_proxy_env():
    saved = {k: os.environ.pop(k) for k in _PROXY_KEYS if k in os.environ}
    try:
        yield
    finally:
        os.environ.update(saved)


def _direct_opener() -> urllib.request.OpenerDirector:
    ctx = ssl.create_default_context()
    https = urllib.request.HTTPSHandler(context=ctx)
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), https)


def _retryable_http_error(exc: urllib.error.HTTPError) -> bool:
    return exc.code == 429 or exc.code >= 500


def urlopen(req: urllib.request.Request, *, timeout: int = 60, retries: int = 3) -> Any:
    last_err: Exception | None = None
    with _without_proxy_env():
        for attempt in range(max(1, retries)):
            try:
                return _direct_opener().open(req, timeout=timeout)
            except urllib.error.HTTPError as exc:
                if not _retryable_http_error(exc) or attempt + 1 >= retries:
                    raise
                last_err = exc
                time.sleep(0.5 * (attempt + 1))
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                if attempt + 1 < retries:
                    time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"HTTP unreachable {req.full_url}: {last_err}") from last_err


def http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: dict | list | str | None = None,
    timeout: int = 600,
) -> dict:
    hdrs = dict(headers or {})
    body_raw: str | None = None
    if body is not None:
        body_raw = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=None, headers=hdrs, method=method)
    try:
        with urlopen(_request_with_body(req, body_raw), timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {url}: {detail[:2000]}") from e


def _request_with_body(req: urllib.request.Request, body: str | None) -> urllib.request.Request:
    if body is None:
        return req
    return urllib.request.Request(
        req.full_url,
        data=body.encode("utf-8"),
        headers=dict(req.header_items()),
        method=req.get_method(),
    )
