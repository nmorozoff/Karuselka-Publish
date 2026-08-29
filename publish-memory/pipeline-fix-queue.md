# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260829-001

status: needs-human
run_at: 2026-08-29T19:15:22.863781+00:00
pair: pair3
stage: publish
carousel: crsl_20260827_1955_468
fix_summary: TikTok capacity — авто-fallback draft inbox в publish_engine; tiktok_capacity в classify_failure; fix INC id regex в publish_incidents
files_changed: scripts/lib/publish_engine.py, scripts/lib/publish_failure.py, scripts/lib/publish_incidents.py

### Error
```
PARTIAL IG OK @morozova_natalia_psy; TikTok @psy_morozova_ — at capacity (direct posting). Draft retry pending after Zernio 429 cooldown.
```

### Context
```json
{
  "instagram": "published",
  "tiktok": "needs_human",
  "next_fifo": "crsl_20260827_0923_361",
  "retry_cmd": "python3 scripts/publish_worker.py --pair pair3 --name crsl_20260827_1955_468 --tiktok-only --limit 1"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_incidents.py`

---
