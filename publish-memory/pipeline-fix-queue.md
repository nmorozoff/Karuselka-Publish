# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260901-001

status: needs-human
run_at: 2026-09-01T19:05:16.879664+00:00
pair: pair3
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

### Fixic
fix_summary: operational — Airtable queue empty (airtable_total=0, ready=0, failed=0). No code fix; factory must export new carousels to /Content_Plan/Queue/.
files_changed: —

---
