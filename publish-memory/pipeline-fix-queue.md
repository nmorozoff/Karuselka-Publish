# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260810-001

status: fixed
run_at: 2026-08-10T16:03:12.776155+00:00
pair: pair3
stage: publish
carousel: crsl_20260805_0825_516
fix_summary: Zernio 400 — слайды 9:16 не проходят IG feed (aspect 0.50:1). Mixed carousel публикуется как Story через platformSpecificData.contentType=story.
files_changed:
- scripts/lib/publish_engine.py
- scripts/lib/http_client.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 400: Bad Request
```

### Context
```json
{
  "zernio_detail": "Instagram Image 2: Aspect ratio 0.50:1 outside allowed range 0.75-1.91. Use contentType story for 9:16 slides."
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260810-002

status: fixed
run_at: 2026-08-10T16:03:30.009399+00:00
pair: pair3
stage: queue
carousel: —
fix_summary: ready=0 при failed>0 ошибочно логировался как «queue empty». Теперь reason=queue blocked by failed, инцидент не создаётся.
files_changed:
- scripts/publish_worker.py

### Error
```
queue empty at dry-run-first
```

### Context
```json
{
  "failed": 11,
  "ready": 0
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260810-001

status: open
run_at: 2026-08-10T16:07:30.624529+00:00
pair: pair3
stage: notify
carousel: crsl_20260805_0825_516

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks
```

### Context
```json
{
  "instagram_status": "not_attempted",
  "tiktok_status": "not_attempted"
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
