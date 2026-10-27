# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261027-001

status: needs-human
run_at: 2026-10-27T16:02:17.389346+00:00
pair: pair1
stage: queue
carousel: —
fix_summary: ready=0 подтверждено publish_status; failed=2 (conflict, instagram_format) — retry не применялся. Нужна генерация в фабрике (Karuselka-emdr) в /Content_Plan/Queue/. Код publish без изменений.
files_changed: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{"ready": 0, "failed": 2, "published": 127, "failed_categories": ["conflict", "instagram_format"]}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
