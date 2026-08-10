# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

## INC-20260810-001 (publish — crsl_20260808_1303_092)

status: needs-human
run_at: 2026-08-10T14:06:36+00:00
pair: pair1
stage: publish
carousel: crsl_20260808_1303_092
fix_summary: Instagram Image 5 validation 500 — ошибка платформы/слайда, не код publish. Retry после проверки slide-05.png или повтор через Zernio.

### Error
Instagram Image 5: Failed to validate Instagram image: bad status code: 500

---

## INC-20260810-002 (notify)

status: fixed
run_at: 2026-08-10T14:07:03+00:00
pair: pair1
stage: notify
carousel: unknown
fix_summary: notify_max.py не парсил errors[] при пустом results[] — добавлен record_from_worker_batch в max_notify.py
files_changed: scripts/lib/max_notify.py, scripts/notify_max.py

### Error
MAX report could not parse Zernio instagram/tiktok blocks (not_attempted)

---

## INC-20260810-003 (publish — crsl_20260808_1306_360)

status: needs-human
run_at: 2026-08-10T14:10:45+00:00
pair: pair1
stage: publish
carousel: crsl_20260808_1306_360
fix_summary: TikTok URL ownership not verified — нужна верификация dropbox.com в TikTok Developer Portal (Zernio). Instagram прошёл.

### Error
URL ownership not verified in TikTok developer portal

---

## INC-20260810-004 (publish_incident --list-open)

status: fixed
run_at: 2026-08-10T14:12:26+00:00
pair: pair1
stage: preflight
fix_summary: publish_incident.py --list-open требовал --pair/--stage/--error; INC_ID_RE не находил id в ## заголовках
files_changed: scripts/publish_incident.py, scripts/lib/publish_incidents.py

---
