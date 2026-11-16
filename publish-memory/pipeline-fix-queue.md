# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261116-001

status: needs-human
run_at: 2026-11-16T17:02:38.616695+00:00
pair: pair2
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{"dropbox_queue_folders": 0, "published": 112, "failed": 0}
```

### fix_summary
Dropbox `/Content_Plan/Queue/` пуст (0 подпапок). Publish-воркер в норме; нужен выпуск каруселей на фабрике Karuselka-emdr (cron/automation).

### Suggested files to inspect/change
- фабрика: `export_publish_bundle.py`, cron Karuselka-emdr

---
