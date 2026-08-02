"""Airtable queue records."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from http_client import urlopen


def delete_record(token: str, base_id: str, table_id: str, record_id: str) -> None:
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
        method="DELETE",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Airtable delete error: {e.read().decode()}") from e
