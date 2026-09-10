# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260910-001

status: fixed
run_at: 2026-09-10T08:06:35.635380+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_1616_400
fix_summary: TikTok at capacity (transient). IG ok. Classified tiktok_capacity; PARTIAL_IG_OK no longer opens Fixic incident; tiktok_resume retry attempted same run — still capacity. Resume on 21:00 MSK slot.
files_changed:
- scripts/lib/publish_failure.py
- scripts/lib/publish_engine.py
- scripts/publish_incident.py

### Error
```
PARTIAL_IG_OK — TikTok direct posting is at capacity right now
```

### Context
```json
{"instagram": "ok", "tiktok": "tiktok_capacity", "retry": "tiktok_resume still capacity"}
```

---

## INC-20260910-002

status: fixed
run_at: 2026-09-10T08:08:53.905945+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_1616_400
fix_summary: Fixic tiktok_resume retry — same tiktok_capacity. No code change needed; resume on 21:00 MSK.
files_changed: (none)

### Error
```
Zernio tiktok error: TikTok direct posting is at capacity right now
```

### Context
```json
{"mode": "tiktok_resume", "retryable": true}
```

---
