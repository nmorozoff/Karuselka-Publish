# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260806-001

status: fixed
run_at: 2026-08-06T15:05:03.466747+00:00
pair: pair2
stage: publish
carousel: crsl_20260806_0643_471
fix_summary: http_client не пробрасывал body Zernio 4xx; trim PNG до EXPECTED_IMAGE_SLIDES для legacy 7-slide; notify_max для error-only batch.
files_changed: scripts/lib/http_client.py, scripts/lib/publish_engine.py, scripts/notify_max.py, scripts/publish_incident.py

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

## INC-20260806-002

status: needs-human
run_at: 2026-08-06T15:07:21.345291+00:00
pair: pair2
stage: publish
carousel: crsl_20260806_0643_471
fix_summary: Zernio 400 — slide-02.png 580×777 вне aspect ratio Instagram (max 773px height). Фабрика должна экспортировать 4:5 для IG feed или story mode.
files_changed: —

### Error
```
HTTP 400: Instagram Image 2 aspect ratio 0.75:1 outside allowed range; 580×777px — crop to 4:5 for feed
```

### Context
```json
{}
```

### Suggested files to inspect/change
- Karuselka-emdr export_publish_bundle.py (aspect ratio)

---

## INC-20260806-003

status: needs-human
run_at: 2026-08-06T15:05:54.701788+00:00
pair: pair2
stage: publish
carousel: crsl_20260803_1722_484
fix_summary: Zernio 409 Conflict — вероятно дубликат поста или карусель уже в Zernio; проверить вручную и очистить failed после решения.
files_changed: —

### Error
```
HTTP 409 Conflict on zernio.com/api/v1/posts
```

### Context
```json
{}
```

### Suggested files to inspect/change
- Zernio dashboard / worker-state failed entry

---

## INC-20260806-004

status: fixed
run_at: 2026-08-06T15:05:16.211010+00:00
pair: pair2
stage: notify
carousel: unknown
fix_summary: notify_max.py теперь шлёт текст ошибки из errors[] когда results пуст.
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
