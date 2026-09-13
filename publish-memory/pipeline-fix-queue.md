# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260913-001

status: needs-human
run_at: 2026-09-13T19:04:12.443630+00:00
pair: pair3
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 0,
  "published_pair3": 52,
  "failed": 0,
  "ready": 0,
  "slot_msk": "22:00",
  "slot_utc": "19:00"
}
```

### fix_summary
Операционный инцидент: глобальная очередь пуста (Airtable 0, failed 0). Automation/cron работает штатно. Нужен экспорт новых каруселей из фабрики (Karuselka-emdr → Dropbox `/Content_Plan/Queue/` + Airtable).

### files_changed
(none — no code fix)

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
