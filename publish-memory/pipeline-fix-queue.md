# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260927-001

status: needs-human
run_at: 2026-09-27T09:04:25.589107+00:00
pair: pair3
stage: automation
carousel: —

### Error
```
Airtable HTTP 429 Too Many Requests during publish_status (preflight queue read)
```

### Context
```json
{
  "trigger": "cron 0 9 * * *",
  "phase": "B",
  "slot": "pair3"
}
```

### Root cause
Airtable ответ `PUBLIC_API_BILLING_LIMIT_EXCEEDED` — исчерпан месячный лимит API, не transient rate limit.

### fix_summary
- Улучшен backoff для HTTP 429 в `scripts/lib/http_client.py` (Retry-After, до 5 попыток).
- Публикация невозможна до сброса квоты или апгрейда плана Airtable (workspace settings / pricing).

### files_changed
- `scripts/lib/http_client.py`

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
