# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260913-001

status: fixed
run_at: 2026-09-13T18:03:38.602982+00:00
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

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

### Fix
fix_summary: Очередь легитимно пуста (airtable=0, failed=0, ready=0). Preflight OK. Automation cron 0 18 UTC (21:00 MSK pair2) сработал. Код не требует правок — ждём карусели от фабрики.
files_changed: —

---
