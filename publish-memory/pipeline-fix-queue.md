# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260912-001

status: needs-human
run_at: 2026-09-12T19:03:14.862553+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Очередь пуста (airtable_total=0, ready=0, failed=0). Фабрика должна экспортировать новые карусели в Queue. Код publish в порядке.
files_changed: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 0,
  "published_pair3": 52,
  "failed": 0,
  "ready": 0,
  "slot": "pair3 @ 19:00 UTC (22:00 MSK)"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
