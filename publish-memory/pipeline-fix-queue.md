# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260906-001

status: open
run_at: 2026-09-06T18:08:22.858623+00:00
pair: pair2
stage: publish
carousel: crsl_20260903_0834_860

### Error
```
TikTok partial: direct posting at capacity (IG ok @natalia_morozova_psy processing). Retry TikTok later or draft inbox.
```

### Context
```json
{
  "failure_category": "bad_request",
  "mode": "photo_carousel_instagram_only",
  "instagram": "processing",
  "tiktok_error": "TikTok direct posting is at capacity right now"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
