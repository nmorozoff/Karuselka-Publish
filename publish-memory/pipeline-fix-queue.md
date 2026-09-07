# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260907-001

status: needs-human
run_at: 2026-09-07T19:02:23.622273+00:00
pair: pair3
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 20,
  "published_pair3": 48,
  "failed": 7,
  "ready": 0,
  "next_fifo": null
}
```

### fix_summary
Очередь пуста: все 20 строк Airtable уже published или failed (7 TikTok spam). Фабрика должна экспортировать новые карусели в Queue. Код publish не требует изменений.

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
