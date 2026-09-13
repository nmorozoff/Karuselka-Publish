# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260913-001

status: fixed
run_at: 2026-09-13T08:02:11.647337+00:00
pair: pair2
stage: queue
carousel: —
fix_summary: Очередь Airtable пуста (airtable_total=0, ready=0, failed=0). Automation pair2 11:00 MSK enabled, cron 08:00 UTC сработал штатно. Публикация не требуется — ждём export из фабрики.
files_changed: —

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
