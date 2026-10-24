# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260904-001

status: needs-human
run_at: 2026-09-04T19:07:57.071189+00:00
pair: pair3
stage: publish
carousel: crsl_20260902_1857_219
fix_summary: TikTok spam — partial IG OK, TT rejected by platform. No auto-retry per contract. Manual TikTok publish or caption review required.
files_changed: scripts/publish_incident.py (--list-open no longer requires --pair/--stage/--error)

### Error
```
TikTok spam: TikTok detected potential spam content. Please review content guidelines.
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "partial": true,
  "instagram": "ok",
  "tiktok": "failed"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
