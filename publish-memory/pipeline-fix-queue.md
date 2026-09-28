# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260928-001

status: needs-human
run_at: 2026-09-28T17:05:34.774789+00:00
pair: pair3
stage: preflight
carousel: —
fix_summary: Внешний rate limit Airtable API (429). materialize_cloud_env --check OK. Повтор publish_status через 30с — снова 429. По контракту run: incident + stop, publish_worker не запускался. Дождаться снятия лимита Airtable или снизить частоту обращений к API; следующий слот pair3 MSK 19:00 UTC 16:00.
files_changed: —

### Error
```
Airtable HTTP 429 Too Many Requests при publish_status (list_queue_records)
```

### Context
```json
{
  "slot": "pair3",
  "cron_utc": "17:00 Mon",
  "phase": "B"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
