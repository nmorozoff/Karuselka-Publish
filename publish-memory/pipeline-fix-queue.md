# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260811-001

status: needs-human
run_at: 2026-08-11T08:05:08.020171+00:00
pair: pair2
stage: publish
carousel: crsl_20260810_1913_144
fix_summary: TikTok отклонил карусель как spam (user_abuse). Требуется ручная проверка контента/caption в TikTok Developer Portal или правка текста на фабрике.
files_changed: —

### Error
```
TikTok detected potential spam content. Please review content guidelines.
```

### Context
```json
{"category": "tiktok_spam", "needs_human": true}
```

### Suggested files to inspect/change
- `scripts/lib/publish_failure.py`

---

## INC-20260811-002

status: fixed
run_at: 2026-08-11T08:05:38.596144+00:00
pair: pair2
stage: notify
carousel: crsl_20260810_1913_144
fix_summary: notify_max.py не парсил batch error worker-last-run.json → ложный not_attempted. Исправлен _record_from_worker_output + skip incident при явном error.
files_changed: scripts/notify_max.py, scripts/lib/max_notify.py, scripts/publish_incident.py

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
- `scripts/lib/max_notify.py`

---

## INC-20260811-003

status: needs-human
run_at: 2026-08-11T08:12:38.552082+00:00
pair: pair2
stage: publish
carousel: crsl_20260810_1917_709
fix_summary: Instagram опубликован (partial_instagram), TikTok — Zernio 429 после retry. Следующий run: resume TikTok для этой карусели (partial_published в worker-state).
files_changed: —

### Error
```
PARTIAL_IG_OK|HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 429: Too Many Requests
```

### Context
```json
{"category": "rate_limit", "partial_instagram": true}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---
