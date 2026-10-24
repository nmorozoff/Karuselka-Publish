# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260808-001

status: needs-human
run_at: 2026-08-08T09:03:36.891051+00:00
pair: pair3
stage: publish
carousel: crsl_20260805_2037_511
fix_summary: Zernio IG 400 — aspect ratio 0.75:1 (580×777px), слайды в Story/TikTok формате. Нужен экспорт 4:5 в фабрике Karuselka-emdr.
files_changed: scripts/lib/http_client.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 400: Bad Request
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260808-002

status: fixed
run_at: 2026-08-08T09:05:26.234968+00:00
pair: pair3
stage: notify
carousel: crsl_20260805_2037_511
fix_summary: notify_max.py теперь шлёт текст ошибки при status=error без results, без ложного notify-инцидента.
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
- `scripts/lib/publish_engine.py`

---

## INC-20260808-003

status: needs-human
run_at: 2026-08-08T09:05:51.257205+00:00
pair: pair3
stage: publish
carousel: crsl_20260805_2108_731
fix_summary: Та же причина — IG aspect ratio 0.75:1 вне допустимого диапазона. http_client.py теперь сохраняет тело ответа Zernio в ошибках.
files_changed: scripts/lib/http_client.py, scripts/publish_incident.py, scripts/lib/publish_incidents.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 400: Bad Request
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---
