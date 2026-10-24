# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260826-001

status: open
run_at: 2026-08-26T19:06:44.046770+00:00
pair: pair3
stage: publish
carousel: crsl_20260826_1252_656

### Error
```
Partial publish: Instagram OK, TikTok spam (user_abuse). TikTok detected potential spam content. Cleanup skipped — needs human TikTok review. Do NOT retry.
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "instagram": "@morozova_natalia_psy OK",
  "tiktok": "@psy_morozova_ FAILED",
  "mode": "photo_carousel_instagram_only",
  "next_fifo": "crsl_20260826_1253_951"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
