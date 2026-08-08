# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260808-001

status: fixed
run_at: 2026-08-08T16:10:04.681558+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_0644_557
fix_summary: Dropbox shared links for slide-01.mp4 returned application/binary; Instagram rejected video fetch. Use get_temporary_link for .mp4 via ensure_media_link().
files_changed: scripts/lib/dropbox_client.py, scripts/lib/publish_engine.py

### Error
```
Instagram couldn't download video from Dropbox media URL (platform_error). Shared scl/fi link served application/binary instead of video/mp4.
```

### Context
```json
{}
```

---

## INC-20260808-002

status: fixed
run_at: 2026-08-08T16:10:13.995842+00:00
pair: pair3
stage: notify
carousel: crsl_20260806_0644_557
fix_summary: notify_max.py now parses worker-last-run errors[] batch format and passes error text to Max report.
files_changed: scripts/notify_max.py

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks (not_attempted on batch error)
```

### Context
```json
{
  "instagram_status": "not_attempted",
  "tiktok_status": "not_attempted"
}
```

---

## INC-20260808-003

status: fixed
run_at: 2026-08-08T16:13:44.353533+00:00
pair: pair3
stage: publish
carousel: crsl_20260806_0644_557
fix_summary: Zernio 429 after rapid retry post-fix; transient rate limit. Carousel remains in failed; next cron/retry-failed should succeed with temporary video links.
files_changed: (none — transient)

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 429: Too Many Requests
```

### Context
```json
{}
```

---
