# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260904-001

status: needs-human
run_at: 2026-09-04T18:10:05.226093+00:00
pair: pair2
stage: publish
carousel: crsl_20260902_1819_886
fix_summary: TikTok spam (user_abuse) — retry бесполезен. Instagram @natalia_morozova_psy опубликован (partial_published). Фабрика: переписать TikTok заголовок/описание для crsl_20260902_1819_886, затем ручной TikTok-only retry или mark_carousel_done после проверки IG.
files_changed: scripts/publish_incident.py (--list-open fix)

### Error
```
TikTok spam: potential spam content detected. Instagram published (partial). needs_human_tiktok=true
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "partial": true,
  "instagram": "processing",
  "tiktok": "failed"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
