# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260811-001

status: fixed
run_at: 2026-08-11T09:02:15.940300+00:00
pair: pair3
stage: publish
carousel: crsl_20260808_1305_851 (и др. 409 duplicate)

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 409: Conflict
Zernio: This exact content is already scheduled/posted within 24h (existingPostId)
```

### fix_summary
Zernio 409 duplicate content → idempotent ok via `existingPostId`. HTTPError body preserved in `http_client.urlopen`. Partial TikTok failures in JSON body handled in `_publish_instagram_then_tiktok`. MAX notify parses `duplicate_accepted`.

### files_changed
- `scripts/lib/http_client.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---

## INC-20260811-002

status: needs-human
run_at: 2026-08-11T09:08:24.278126+00:00
pair: pair3
stage: publish
carousel: crsl_20260810_1914_076

### Error
```
TikTok detected potential spam content (user_abuse). Instagram likely published; TikTok needs human review.
```

### fix_summary
Partial IG path now works; carousel in `partial_published` / `failed` with `needs_human`. Retry TikTok manually or edit content in Airtable.

---

## INC-20260811-003

status: fixed
run_at: 2026-08-11T09:16:07.283518+00:00
pair: pair3
stage: publish
carousel: crsl_20260810_1918_699

### Error
```
HTTP 429 TikTok rate-limited (wait ~3m). Partial Instagram ok.
```

### fix_summary
Recorded as `PARTIAL_IG_OK` + retryable failed state. Next cron run should resume TikTok via `partial_published`.

---
