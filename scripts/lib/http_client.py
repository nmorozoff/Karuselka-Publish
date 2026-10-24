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


def _retry_delay_for_rate_limit(exc: urllib.error.HTTPError, attempt: int) -> float:
    ra = exc.headers.get("Retry-After") or exc.headers.get("retry-after")
    if ra:
        try:
            return min(float(ra) + 1.0, 120.0)
        except ValueError:
            pass
    return min(15.0 * (attempt + 1), 90.0)


def urlopen(req: urllib.request.Request, *, timeout: int = 60, retries: int = 3) -> Any:
    last_err: Exception | None = None
    rate_limit_retries = int(os.environ.get("HTTP_429_MAX_RETRIES", "8"))
    max_attempts = max(max(1, retries), rate_limit_retries)
    with _without_proxy_env():
        for attempt in range(max_attempts):
            try:
                return _direct_opener().open(req, timeout=timeout)
            except urllib.error.HTTPError as exc:
                last_err = exc
                if exc.code in (429, 503) and attempt + 1 < max_attempts:
                    time.sleep(_retry_delay_for_rate_limit(exc, attempt))
                    continue
                raise
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                if attempt + 1 < retries:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                break
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
        if e.code == 429 and "PUBLIC_API_BILLING_LIMIT_EXCEEDED" in detail:
            raise RuntimeError(
                "Airtable monthly API limit exceeded (PUBLIC_API_BILLING_LIMIT_EXCEEDED). "
                "Upgrade plan or wait for billing reset — publish queue cannot be read."
            ) from e
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
