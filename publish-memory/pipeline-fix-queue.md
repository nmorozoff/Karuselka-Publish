# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260828-001

status: fixed
run_at: 2026-08-28T09:03:35.905927+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Нормальное состояние — Airtable Queue пуст (ready=0, failed=0). Убран log_incident на empty; добавлен notify в Макс; --list-open без обязательных pair/stage/error.
files_changed:
- scripts/publish_worker.py
- scripts/publish_incident.py

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
