# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260831-001

status: fixed
run_at: 2026-08-31T08:06:27.422672+00:00
pair: pair2
stage: queue
carousel: —
fix_summary: Очередь пуста — все 5 записей Airtable уже published, cleanup не выполнен. Purge stale через mark_carousel_done + reconcile failed.
files_changed: scripts/mark_carousel_done.py (used), scripts/manage_failed_queue.py (used)

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
