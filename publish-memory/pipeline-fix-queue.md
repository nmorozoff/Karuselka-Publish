# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260824-001

status: needs-human
run_at: 2026-08-24T19:04:56.442806+00:00
pair: pair3
stage: publish
carousel: crsl_20260820_1450_022
fix_summary: TikTok user_abuse (spam) — не retry. IG @morozova_natalia_psy опубликован; cleanup пропущен (partial). Нужна правка TikTok текста на фабрике / ручная проверка в TikTok UI.
files_changed: —

### Error
```
TikTok spam: partial IG OK, TT failed user_abuse
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "partial_instagram": true,
  "needs_human_tiktok": true
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
