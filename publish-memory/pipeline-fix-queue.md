# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260828-001

status: open
run_at: 2026-08-28T19:20:06.260284+00:00
pair: pair3
stage: publish
carousel: crsl_20260827_1954_935

### Error
```
TikTok partial: direct posting at capacity. IG @morozova_natalia_psy OK. TT @psy_morozova_ failed. needs_human_tiktok, cleanup skipped.
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
