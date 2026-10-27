# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261027-001

status: open
run_at: 2026-10-27T17:02:59.894328+00:00
pair: pair2
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "diagnosis": "ready=0: обе полные папки в Queue уже в failed (needs_human). FIFO пуст для publish.",
  "ready_folders_failed": [
    "crsl_k3_20261005_0850_expert-light_1305 (conflict/409)",
    "crsl_k3_20261013_0800_bordo_3860 (instagram_format)"
  ],
  "incomplete_queue_folders": 8,
  "action": "Человек: разобрать failed в Zernio/Dropbox или удалить папки; догрузить неполные с фабрики. Не --retry-failed для spam/format."
}

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
