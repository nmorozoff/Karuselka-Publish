# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260830-001

status: needs-human
run_at: 2026-08-30T19:01:02.292988+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: Очередь пуста (ready=0): все 5 строк Airtable уже в published_pair3; 3 partial TikTok needs-human. Код publish корректен — нужны новые карусели от фабрики + ручной TT retry для partial.

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "airtable_total": 5,
  "ready": 0,
  "failed_in_queue": 3,
  "published_pair3": 38,
  "partial_tiktok": [
    "crsl_20260827_0936_359",
    "crsl_20260827_1938_387",
    "crsl_20260827_1955_468"
  ]
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
