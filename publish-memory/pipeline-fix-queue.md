# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260815-001

status: fixed
run_at: 2026-08-15T08:05:02.977364+00:00
pair: pair2
stage: publish
carousel: crsl_20260810_1929_691
fix_summary: TikTok spam — усилена санитизация caption (800 символов, CTA/bio strip); partial IG при tiktok_spam в теле ответа Zernio
files_changed:
- scripts/lib/tiktok_caption.py
- scripts/lib/publish_engine.py
- scripts/materialize_cloud_env.py

### Error
```
TikTok detected potential spam content (user_abuse) на crsl_20260810_1929_691
```

### Context
```json
{"category": "tiktok_spam", "needs_human": true}
```

---

## INC-20260815-002

status: fixed
run_at: 2026-08-15T08:06:01.008195+00:00
pair: pair2
stage: notify
carousel: crsl_20260810_1929_691
fix_summary: notify_max.py теперь читает errors[] из worker-last-run.json вместо not_attempted
files_changed:
- scripts/notify_max.py

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

---

## INC-20260815-003

status: needs-human
run_at: 2026-08-15T08:13:41.279563+00:00
pair: pair2
stage: publish
carousel: crsl_20260811_0719_672
fix_summary: Zernio 429 rate limit на TikTok после успешного Instagram (partial_instagram). Повторить на следующем cron или --retry-failed после паузы.
files_changed: []

### Error
```
PARTIAL_IG_OK|HTTP Error 429: Too Many Requests
```

### Context
```json
{"partial_instagram": true, "category": "rate_limit"}
```

---
