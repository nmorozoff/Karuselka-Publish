# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260928-001

status: needs-human
run_at: 2026-09-28T17:22:15.338425+00:00
pair: pair1
stage: preflight
carousel: —
fix_summary: Airtable 429 persists after http_client 429 backoff (8 attempts, ~2min). Retry slot manually when Airtable rate limit clears.
files_changed: scripts/lib/http_client.py

### Error
```
Airtable HTTP 429 on publish_status (get_queue_summary)
```

### Context
```json
{
  "slot": "pair1-2000-msk",
  "phase": "B"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
