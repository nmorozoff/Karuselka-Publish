# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260828-001

status: fixed
run_at: 2026-08-28T08:14:16.214813+00:00
pair: pair2
stage: queue
carousel: crsl_20260810_1920_020
fix_summary: ready=0 из-за failed в worker-state; retry-failed опубликовал crsl_20260810_1920_020 (IG+TT processing, cleanup ok)
files_changed: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{"failed_in_airtable": 2, "resolution": "publish_worker --retry-failed --dry-run-first"}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
