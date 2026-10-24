# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260828-001

status: needs-human
run_at: 2026-08-28T18:08:44.279137+00:00
pair: pair2
stage: queue
carousel: —
fix_summary: Очередь пуста (Airtable 0, ready 0, failed 0). Публикация не требуется — нужен export каруселей из фабрики Karuselka-emdr в /Content_Plan/Queue.
files_changed: scripts/publish_incident.py (--list-open regression fix)

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
