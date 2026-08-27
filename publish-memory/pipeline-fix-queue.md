# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260827-001

status: needs-human
run_at: 2026-08-27T19:05:33.466430+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Все 22 строки Airtable Queue исчерпаны (published или failed). ready=0 — фабрика должна export новые карусели в /Content_Plan/Queue/. Код publish исправен.
files_changed: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 22,
  "ready": 0,
  "failed": 12,
  "partial_published": 25,
  "failed_breakdown": {"rate_limit": 8, "transient": 2, "unknown": 3}
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
