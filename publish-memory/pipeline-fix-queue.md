# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260825-001

status: needs-human
run_at: 2026-08-25T19:06:18.100612+00:00
pair: pair3
stage: publish
carousel: crsl_20260820_1550_743
fix_summary: TikTok user_abuse/spam — автоматический retry запрещён. Instagram опубликован (@morozova_natalia_psy). Ручная проверка TikTok или purge/mark-done.
files_changed: scripts/publish_incident.py (--list-open fix)

### Error
```
TikTok spam (user_abuse): potential spam content. Instagram OK, partial publish.
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "needs_human_tiktok": true,
  "instagram": "ok",
  "tiktok": "failed"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
