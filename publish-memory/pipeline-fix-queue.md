# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260927-001

status: needs-human
run_at: 2026-09-27T17:00:46.008844+00:00
pair: pair1
stage: queue
carousel: —
fix_summary: Добавлен backoff/retry для HTTP 429 в scripts/lib/http_client.py (до 6 попыток, Retry-After). После ~6 мин ожидания Airtable всё ещё 429 — лимит на стороне API; повторить слот вручную или дождаться следующего cron.
files_changed:
- scripts/lib/http_client.py

### Error
```
Airtable HTTP 429 Too Many Requests during publish_status (Phase B)
```

### Context
```json
{
  "trigger": "cron 17:00 UTC",
  "phase": "B",
  "script": "publish_status.py"
}
```

### Suggested files to inspect/change
- `scripts/lib/http_client.py`

---
