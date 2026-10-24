# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260905-001

status: needs-human
run_at: 2026-09-05T08:08:03.456946+00:00
pair: pair2
stage: publish
carousel: crsl_20260902_1947_178
fix_summary: TikTok spam detection — IG опубликован @natalia_morozova_psy, TT отклонён. Retry запрещён. Нужна правка TikTok-текста на фабрике (copywriter). Airtable+Dropbox сохранены для ручного retry.
files_changed: —

### Error
```
TikTok spam: partial IG ok, TT needs-human (crsl_20260902_1947_178)
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "instagram": "ok",
  "tiktok": "spam",
  "cleanup": "skipped",
  "retry": false
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
