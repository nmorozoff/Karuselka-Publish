# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260927-001

status: needs-human
run_at: 2026-09-27T07:07:50.310299+00:00
pair: pair1
stage: queue
carousel: —
fix_summary: Код — classify airtable_billing_limit + fail-fast в http_client без бессмысленных retry. Публикация заблокирована до сброса/апгрейда Airtable API quota (ручное действие владельца workspace).
files_changed:
- scripts/lib/http_client.py
- scripts/lib/publish_failure.py

### Error
```
Airtable PUBLIC_API_BILLING_LIMIT_EXCEEDED: monthly API quota exhausted (HTTP 429). Publish blocked until workspace usage resets or plan upgrade.
```

### Context
```json
{
  "category": "airtable_billing_limit",
  "cron": "0 7 * * *",
  "slot": "pair1"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
