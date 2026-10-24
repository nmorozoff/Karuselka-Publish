# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260901-001

status: fixed
run_at: 2026-09-01T09:03:21.871398+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Пустая очередь — штатный skip; notify_queue_empty в Макс вместо log_incident
files_changed: scripts/lib/max_notify.py, scripts/publish_worker.py

### Error
```
queue empty at dry-run-first
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
