# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260811-001

status: needs-human
run_at: 2026-08-11T16:19:47.665025+00:00
pair: pair3
stage: publish
carousel: crsl_20260810_1927_506
fix_summary: Transient Zernio/Instagram 500 при валидации slide-02; Zernio auto-retry. Retry через --retry-failed на следующем cron.
files_changed: scripts/notify_max.py, scripts/publish_incident.py

### Error
```
Zernio instagram: Instagram Image 2: Failed to validate Instagram image: bad status code: 500
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260811-001-notify

status: fixed
run_at: 2026-08-11T16:20:10.228066+00:00
pair: pair3
stage: notify
carousel: crsl_20260810_1927_506
fix_summary: notify_max.py теперь читает errors[] из worker-last-run.json вместо not_attempted.
files_changed: scripts/notify_max.py

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
- `scripts/notify_max.py`

---

## INC-20260811-002

status: needs-human
run_at: 2026-08-11T16:28:08.065391+00:00
pair: pair3
stage: publish
carousel: crsl_20260810_1931_173
fix_summary: Zernio 429 после retry в том же run; partial Instagram ok. Retry --retry-failed на следующем cron.
files_changed: scripts/notify_max.py, scripts/publish_incident.py

### Error
```
PARTIAL_IG_OK|HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 429: Too Many Requests
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---
