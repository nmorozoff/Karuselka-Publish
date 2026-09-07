# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260907-001

status: needs-human
run_at: 2026-09-07T18:03:14.519002+00:00
fixed_at: 2026-09-07T18:05:00+00:00
pair: pair2
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
  "ready": 0,
  "failed": 7,
  "diagnosis": "Все 20 строк Airtable уже в published; 7 из них также в failed (partial IG ok / TikTok fail). retry-failed не помогает — published блокирует повтор в run_publish_batch.",
  "retryable_failed": [
    "crsl_20260902_0759_318",
    "crsl_20260902_1256_179",
    "crsl_20260902_1305_415",
    "crsl_20260902_1325_952",
    "crsl_20260902_1818_518",
    "crsl_20260902_1948_511"
  ],
  "needs_human_failed": ["crsl_20260903_0809_909"]
}
```

### fix_summary
Операционная блокировка, не баг кода. Нужны новые карусели от фабрики в Queue. Для partial TikTok (capacity): ручной `--tiktok-only --retry-failed --name <carousel>`. Spam: переписать TikTok-тексты, не retry.

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py` (опционально: retry_failed для partial+published)

---
