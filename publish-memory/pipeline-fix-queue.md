# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261013-001

status: needs-human
run_at: 2026-10-13T07:06:19.509630+00:00
pair: pair1
stage: queue
carousel: crsl_k3_20261005_0850_expert-light_1305

### Error
```
queue empty at dry-run-first (ready=0): единственная папка в Queue — failed Zernio 409 conflict
```

### Context
```json
{
  "reconciled_orphans": ["crsl_20260923_1926_588", "crsl_20260924_1835_562"],
  "failed_category": "conflict",
  "retryable": false
}
```

### fix_summary
Авто-purge orphan Queue-папок, уже в worker-state published (`_reconcile_published_queue_orphans` в `run_publish_batch`).

### files_changed
- `scripts/lib/publish_engine.py`

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20261013-001

status: open
run_at: 2026-10-13T07:07:57.592792+00:00
pair: pair1
stage: queue
carousel: —

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
