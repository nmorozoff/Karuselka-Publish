# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260809-001

status: needs-human
run_at: 2026-08-09T17:05:16.933753+00:00
pair: pair1
stage: publish
carousel: crsl_20260806_1604_181
fix_summary: Zernio HTTP 400 — slide-02.png 670×894 (0.75:1) не проходит IG feed (нужен 4:5). Фабрика Karuselka-emdr: пересобрать слайды или crop для Instagram.
files_changed: scripts/lib/http_client.py (HTTPError body в лог)

### Error
```
HTTP 400: Instagram Image 2 aspect ratio 0.75:1 outside allowed range; 670×894px — Story/TikTok format, crop to 4:5 for IG feed
```

### Context
```json
{"mode": "mixed", "images": 7, "hook_video": "slide-01.mp4"}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- Karuselka-emdr export / slide dimensions

---

## INC-20260809-001-notify

status: fixed
run_at: 2026-08-09T17:05:26.666033+00:00
pair: pair1
stage: notify
carousel: crsl_20260806_1604_181
fix_summary: Ложный notify-инцидент при publish error до Zernio — skip если instagram/tiktok не в result; notify_max.py для batch error.
files_changed: scripts/lib/max_notify.py, scripts/notify_max.py, scripts/publish_incident.py

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
- `scripts/lib/max_notify.py`
- `scripts/notify_max.py`

---
