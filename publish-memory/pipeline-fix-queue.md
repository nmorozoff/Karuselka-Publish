# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260911-001

status: needs-human
run_at: 2026-09-11T19:02:22.435370+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: ready=0 — все 32 строки Airtable либо published, либо в failed (19: 16 unknown, 2 tiktok_capacity, 1 tiktok_spam). Код publish в порядке; нужен экспорт новых каруселей с фабрики и/или ручная очистка failed (manage_failed_queue.py). tiktok_spam — не retry.

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
  "failed_breakdown": {
    "unknown": 16,
    "tiktok_capacity": 2,
    "tiktok_spam": 1
  }
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
