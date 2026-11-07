# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261107-001

status: needs-human
run_at: 2026-11-07T16:05:16.802007+00:00
pair: pair1
stage: queue
carousel: —

fix_summary: В Dropbox 2 папки, обе в worker-state failed (conflict + instagram_format); retry не делали. Уточнены message/incident при ready=0 (publish_engine + publish_worker).
files_changed: scripts/lib/publish_engine.py, scripts/publish_worker.py

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "queue_folders": [
    "crsl_k3_20261005_0850_expert-light_1305",
    "crsl_k3_20261013_0800_bordo_3860"
  ],
  "failed_categories": ["conflict", "instagram_format"]
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20261107-001

status: open
run_at: 2026-11-07T16:06:24.207557+00:00
pair: pair1
stage: queue
carousel: —

### Error
```
no ready at dry-run-first: No ready carousels: 2 in queue, all blocked (published/failed/incomplete)
```

### Context
```json
{
  "queue_total": 2,
  "ready": 0,
  "reason": "queue blocked by failed",
  "worker_last_run": "publish-memory/output/worker-last-run.json"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
