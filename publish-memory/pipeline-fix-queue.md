# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260912-001

status: fixed
run_at: 2026-09-12T18:04:22.932337+00:00
pair: pair2
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

### fix_summary
Очередь была заблокирована: 32 строки Airtable, все уже в `published` (ready=0) + 19 failed.
Reconcile: purge tiktok_spam+bad_request (2), clear unknown failed (15).
Purge 30 stale published записей из Airtable+Dropbox.
Итог: airtable_total=0, failed=0, ready=0 — ждём новые карусели от фабрики.

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
