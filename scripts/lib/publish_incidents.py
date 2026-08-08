"""Incident queue for publish pipeline — consumed by Cloud Agent Fixic."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from publish_config import MEMORY

QUEUE_PATH = MEMORY / "pipeline-fix-queue.md"
INC_ID_RE = re.compile(r"INC-\d{8}-\d{3}")


def _next_incident_id() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"INC-{today}-"
    if not QUEUE_PATH.exists():
        return f"{prefix}001"
    text = QUEUE_PATH.read_text(encoding="utf-8")
    nums = [
        int(m.group(0)[len(prefix) :])
        for m in INC_ID_RE.finditer(text)
        if m.group(0).startswith(prefix)
    ]
    n = max(nums, default=0) + 1
    return f"{prefix}{n:03d}"


def _ensure_queue_file() -> None:
    if QUEUE_PATH.exists():
        return
    MEMORY.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(
        "# Publish pipeline fix queue\n\n"
        "Инциденты для Fixic после Cloud Agent / publish_worker.\n\n",
        encoding="utf-8",
    )


def log_incident(
    *,
    pair: str,
    stage: str,
    error: str,
    carousel: str | None = None,
    context: dict[str, Any] | None = None,
    suggested_files: list[str] | None = None,
) -> str:
    """Append open incident; return incident id."""
    _ensure_queue_file()
    inc_id = _next_incident_id()
    now = datetime.now(timezone.utc).isoformat()
    ctx = json.dumps(context or {}, ensure_ascii=False, indent=2)
    files = "\n".join(f"- `{f}`" for f in (suggested_files or [])) or "- `scripts/lib/publish_engine.py`"
    block = f"""
## {inc_id}

status: open
run_at: {now}
pair: {pair}
stage: {stage}
carousel: {carousel or "—"}

### Error
```
{error.strip()[:4000]}
```

### Context
```json
{ctx}
```

### Suggested files to inspect/change
{files}

---
"""
    with QUEUE_PATH.open("a", encoding="utf-8") as f:
        f.write(block)
    return inc_id


def list_open_incidents() -> list[dict[str, str]]:
    if not QUEUE_PATH.exists():
        return []
    text = QUEUE_PATH.read_text(encoding="utf-8")
    incidents: list[dict[str, str]] = []
    for m in re.finditer(
        r"## (INC-\d{8}-\d{3})\n(.*?)(?=\n## INC-|\Z)",
        text,
        re.DOTALL,
    ):
        inc_id = m.group(1)
        body = m.group(2)
        if "status: open" not in body:
            continue
        pair_m = re.search(r"^pair: (.+)$", body, re.MULTILINE)
        stage_m = re.search(r"^stage: (.+)$", body, re.MULTILINE)
        incidents.append(
            {
                "id": inc_id,
                "pair": pair_m.group(1).strip() if pair_m else "",
                "stage": stage_m.group(1).strip() if stage_m else "",
            }
        )
    return incidents
