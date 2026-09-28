# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260928-001

status: needs-human
run_at: 2026-09-28T08:18:38.784991+00:00
pair: pair2
stage: preflight
carousel: —

### Error
```
Airtable HTTP 429 PUBLIC_API_BILLING_LIMIT_EXCEEDED — monthly API quota exhausted; publish_status failed
```

### Context
```json
{
  "slot": "pair2-1100-msk",
  "trigger": "cron 0 8 * * *",
  "api_error": "PUBLIC_API_BILLING_LIMIT_EXCEEDED"
}
```

### fix_summary
Лимит Airtable Public API на месяц исчерпан (не rate-limit). Publish не может читать очередь FIFO. Действие: повысить план / дождаться сброса квоты в workspace settings Airtable. Публикация возобновится автоматически после восстановления API.

### files_changed
- (нет — инфраструктура Airtable)

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
