# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260831-001

status: fixed
run_at: 2026-08-31T09:04:41.584576+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Пустая очередь — норма; log_incident заменён на notify_queue_empty в publish_worker.py
files_changed:
- scripts/publish_worker.py
- scripts/lib/max_notify.py

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
