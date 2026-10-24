# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260809-001

status: fixed
run_at: 2026-08-09T16:02:00.228670+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_1603_092

### Error
```
Instagram Image 1: aspect ratio 0.75:1 outside allowed range (580x777px, need 4:5 max 773px height)
```

### Context
```json
{
  "root_cause": "factory_export_wrong_aspect_ratio",
  "tiktok_ok": true
}
```

### fix_summary
Карусель в failed (контент фабрики). Retry следующей ready — успех crsl_20260806_1606_292. Код: http_client сохраняет тело Zernio 400, publish_incident --list-open без обязательных args, notify_max для batch error.

### files_changed
- `scripts/lib/http_client.py`
- `scripts/publish_incident.py`
- `scripts/notify_max.py`

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260809-001-notify

status: fixed
run_at: 2026-08-09T16:03:50.900268+00:00
pair: pair3
stage: notify
carousel: crsl_20260806_1603_092

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

### fix_summary
notify_max.py теперь читает errors[] из worker-last-run при status=error вместо ложного not_attempted.

### files_changed
- `scripts/notify_max.py`

---

## INC-20260809-001-factory

status: needs-human
run_at: 2026-08-09T16:03:41.166186+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_1603_092

### Error
```
Instagram rejects slide-01.png: 580×777px (aspect 0.75:1) — crop to 4:5 (max 773px height) in Karuselka-emdr export
```

### Context
```json
{
  "action": "re-export carousel in factory with correct 4:5 dimensions, then --retry-failed"
}
```

### fix_summary
Требуется правка экспорта слайдов в фабрике (Karuselka-emdr), не в publish.

---
