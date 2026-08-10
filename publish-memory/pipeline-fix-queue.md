# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260810-001

status: needs-human
run_at: 2026-08-10T19:06:39.517885+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_0644_557
fix_summary: TikTok spam (user_abuse) — дублирующийся/агрессивный текст в TikTok описании. Нужна правка caption на фабрике (Karuselka-emdr), не publish-код.
files_changed: []

### Error
```
Zernio tiktok error: TikTok detected potential spam content. Please review content guidelines.
```

### Context
```json
{"category": "tiktok_spam", "needs_human": true}
```

---

## INC-20260810-002

status: fixed
run_at: 2026-08-10T19:07:03.520210+00:00
pair: pair3
stage: notify
carousel: crsl_20260806_0644_557
fix_summary: notify_max.py не парсил worker-last-run.json при status=error (errors[] без results[]). Добавлен разбор errors[] + пропуск ложного notify-инцидента при result.error.
files_changed:
- scripts/notify_max.py
- scripts/lib/max_notify.py

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks
```

---

## INC-20260810-003

status: needs-human
run_at: 2026-08-10T19:14:36.658530+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_1558_540
fix_summary: Instagram опубликован, TikTok 429 после 3 retry. Карусель в failed (retryable). Повторить: publish_worker.py --pair pair3 --retry-failed --limit 1 --dry-run-first
files_changed: []

### Error
```
PARTIAL_IG_OK|HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 429: Too Many Requests
```

### Context
```json
{"category": "rate_limit", "retryable": true, "partial_instagram": true}
```

---
