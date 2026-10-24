# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260818-001

status: needs-human
run_at: 2026-08-18T17:31:06.486176+00:00
pair: pair2
stage: publish
carousel: crsl_20260810_2039_728
fix_summary: TikTok spam — фабрика переписывает TikTok-тексты для crsl_20260810_2039_728; retry publish не делать. CLI publish_incident.py --list-open восстановлен.
files_changed: scripts/publish_incident.py

### Error
```
TikTok spam: partial IG ok, TT rejected (needs_human)
```

### Context
```json
{
  "failure_category": "tiktok_spam",
  "instagram": "processing",
  "tiktok": "failed",
  "cleanup_skipped": true
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
