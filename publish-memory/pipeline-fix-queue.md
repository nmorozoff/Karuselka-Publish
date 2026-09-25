# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260925-001

status: fixed
run_at: 2026-09-25T07:05:23.899836+00:00
pair: pair1
stage: publish
carousel: crsl_20260923_1254_151
fix_summary: orphan Airtable row без папки в Dropbox — auto-purge + skip FIFO в run_publish_batch
files_changed: scripts/lib/publish_engine.py, scripts/lib/publish_failure.py

### Error
```
No Dropbox carousel folder for crsl_20260923_1254_151: Dropbox list_folder failed for /Content_Plan/Pair1/crsl_20260923_1254_151: HTTP unreachable https://api.dropboxapi.com/2/files/list_folder: HTTP Error 409: Conflict
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260925-001

status: fixed
run_at: 2026-09-25T07:05:23.899980+00:00
pair: pair1
stage: dry_run
carousel: —
fix_summary: см. INC-20260925-001 publish — orphan purge разблокировал dry-run-first

### Error
```
[{'name': 'crsl_20260923_1254_151', 'error': 'No Dropbox carousel folder for crsl_20260923_1254_151: Dropbox list_folder failed for /Content_Plan/Pair1/crsl_20260923_1254_151: HTTP unreachable https://api.dropboxapi.com/2/files/list_folder: HTTP Error 409: Conflict'}]
```

### Context
```json
{
  "worker_last_run": "publish-memory/output/worker-last-run.json"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
