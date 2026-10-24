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


def _retry_sleep_seconds(exc: Exception, attempt: int) -> float | None:
    """Backoff for transient errors; None = do not retry."""
    if isinstance(exc, urllib.error.HTTPError) and exc.code == 429:
        retry_after = exc.headers.get("Retry-After") if exc.headers else None
        if retry_after:
            try:
                return max(1.0, float(retry_after))
            except ValueError:
                pass
        return min(120.0, 15.0 * (2**attempt))
    if isinstance(exc, urllib.error.HTTPError) and exc.code in (502, 503, 504):
        return min(60.0, 2.0 * (2**attempt))
    return 0.5 * (attempt + 1)


def urlopen(req: urllib.request.Request, *, timeout: int = 60, retries: int = 3) -> Any:
    last_err: Exception | None = None
    max_attempts = max(1, retries)
    attempt = 0
    with _without_proxy_env():
        while attempt < max_attempts:
            try:
                return _direct_opener().open(req, timeout=timeout)
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                attempt += 1
                if isinstance(exc, urllib.error.HTTPError) and exc.code == 429:
                    max_attempts = max(max_attempts, 6)
                if attempt >= max_attempts:
                    break
                delay = _retry_sleep_seconds(exc, attempt - 1)
                if delay is None:
                    break
                time.sleep(delay)
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
