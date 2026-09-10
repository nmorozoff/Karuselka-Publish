# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260910-001

status: needs-human
run_at: 2026-09-10T19:04:57.521165+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Очередь пуста (ready=0). Airtable 32 строк, published_pair3 52, failed 19 — все записи либо опубликованы, либо в failed. Нужен export новых каруселей с фабрики Karuselka-emdr.
files_changed: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 32,
  "published_pair3": 52,
  "failed": 19,
  "ready": 0,
  "next_fifo": null
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
