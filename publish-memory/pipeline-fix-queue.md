# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260807-001

status: needs-human
run_at: 2026-08-07T17:07:45.849869+00:00
pair: pair1
stage: publish
carousel: crsl_20260803_1938_315
fix_summary: TikTok user_abuse — spam detection на стороне платформы; требуется ручная проверка контента/caption
files_changed: —

### Error
```
TikTok detected potential spam content. Please review content guidelines.
```

### Context
```json
{"errorCategory": "user_abuse", "platform": "tiktok"}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260807-002

status: fixed
run_at: 2026-08-07T17:07:57.670606+00:00
pair: pair1
stage: notify
carousel: crsl_20260803_1938_315
fix_summary: notify_max.py теперь читает errors[] из worker-last-run; max_notify не логирует ложный notify-инцидент при top-level error
files_changed: scripts/notify_max.py, scripts/lib/max_notify.py

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks
```

### Context
```json
{"instagram_status": "not_attempted", "tiktok_status": "not_attempted"}
```

### Suggested files to inspect/change
- `scripts/lib/max_notify.py`
- `scripts/notify_max.py`

---

## INC-20260807-003

status: fixed
run_at: 2026-08-07T17:10:45.968985+00:00
pair: pair1
stage: publish
carousel: crsl_20260803_1946_621
fix_summary: Zernio 429 — retries 2→3 попытки, пауза 5с между IG и TT post
files_changed: scripts/lib/publish_engine.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 429: Too Many Requests
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260807-004

status: fixed
run_at: 2026-08-07T17:12:00.000000+00:00
pair: pair1
stage: tooling
carousel: —
fix_summary: publish_incident.py --list-open работает без обязательных --pair/--stage/--error; INC id regex исправлен; assert_zernio_ok — краткие ошибки
files_changed: scripts/publish_incident.py, scripts/lib/publish_incidents.py, scripts/lib/publish_cleanup.py

### Error
```
publish_incident.py --list-open требовал --pair/--stage/--error; дубли INC-001
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/publish_incident.py`
- `scripts/lib/publish_incidents.py`
- `scripts/lib/publish_cleanup.py`

---
