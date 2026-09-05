# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260905-001

status: open
run_at: 2026-09-05T18:08:36.220537+00:00
pair: pair2
stage: publish
carousel: crsl_20260903_0806_019

### Error
```
TikTok spam (user_abuse): partial_instagram_needs_human_tiktok. IG @natalia_morozova_psy processing OK, TikTok @natalyamorozovapsy failed. Cleanup skipped.
```

### Context
```json
{
  "mode": "photo_carousel_instagram_only",
  "slides": 6,
  "failure_category": "tiktok_spam",
  "hashtags": "#отношения #самооценка #психология #эмдр",
  "action": "factory_rewrite_tiktok_texts_no_retry"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
