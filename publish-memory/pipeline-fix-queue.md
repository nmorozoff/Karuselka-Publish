# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261005-001

status: needs-human
run_at: 2026-10-05T17:12:53.773569+00:00
pair: pair1
stage: publish
carousel: crsl_20261001_1615_b_style_1990

### Error
```
TikTok Zernio HTTP 400 after IG ok (partial bad_request)
```

### Context
```json
{
  "failure_category": "bad_request",
  "needs_human_tiktok": true,
  "instagram": "ok"
}
```

### fix_summary
Instagram опубликован (Zernio post 6ac3d91d…). TikTok: HTTP 400 на POST /api/v1/posts — типично валидация payload/аккаунта в Zernio, не transient. Retry запрещён (needs_human). Папка Queue и Airtable сохранены (partial). Ручной TikTok или разбор ответа 400 в кабинете Zernio для pair1_tiktok.

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
