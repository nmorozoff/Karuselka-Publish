# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260831-001

status: needs-human
run_at: 2026-08-31T19:02:03.723803+00:00
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
  "published_pair3": 38,
  "failed": 0,
  "ready": 0,
  "slot": "22:00 MSK (19:00 UTC)"
}
```

### Fixic
fix_summary: Очередь пуста — Airtable 0 строк, ready=0, failed=0. Код publish в порядке; нужен экспорт новых каруселей из фабрики (Karuselka-emdr → Queue).
files_changed: —

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
