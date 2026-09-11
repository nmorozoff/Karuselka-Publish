# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260911-001

status: needs-human
run_at: 2026-09-11T18:02:14.819137+00:00
pair: pair2
stage: queue
carousel: —
fix_summary: Очередь реально пуста (ready=0): Airtable 32 строки, все либо published либо в failed (19). Новых каруселей от фабрики нет. Код publish в порядке; нужен export_publish_bundle от Karuselka-emdr.
files_changed: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 32,
  "ready": 0,
  "failed": 19,
  "published_pair2": 61,
  "failed_breakdown": {
    "tiktok_capacity": 2,
    "tiktok_spam": 1,
    "unknown_partial": 16
  }
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
