# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260808-001

status: needs-human
run_at: 2026-08-08T19:05:40.045260+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_1555_455
fix_summary: TikTok отклонил карусель как spam (user_abuse). Нужна правка caption/описания в фабрике или ручная публикация.
files_changed: —

### Error
```
Zernio tiktok error: TikTok detected potential spam content. Please review content guidelines.
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20260808-002

status: fixed
run_at: 2026-08-08T19:05:43.858571+00:00
pair: pair3
stage: notify
carousel: crsl_20260806_1555_455
fix_summary: notify_max.py не парсил batch-error из worker-last-run.json (errors[] вместо results[]). Добавлена ветка с build_publish_report_text по errors[0].
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
- `scripts/lib/max_notify.py`

---

## INC-20260808-003

status: fixed
run_at: 2026-08-08T19:05:34.049943+00:00
pair: pair3
stage: automation
carousel: —
fix_summary: publish_incident.py --list-open требовал --pair/--stage/--error; INC_ID_RE не матчил ## INC-... в queue file. Исправлено.
files_changed: scripts/publish_incident.py, scripts/lib/publish_incidents.py

### Error
```
publish_incident.py --list-open failed: required arguments missing
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/publish_incident.py`
- `scripts/lib/publish_incidents.py`

---

## INC-20260808-004

status: needs-human
run_at: 2026-08-08T19:08:41.988237+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_1558_540
fix_summary: Zernio HTTP 429 после retry (60s). Повторить позже через --retry-failed.
files_changed: —

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
