# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

## INC-20260807-001 (TikTok spam)

status: needs-human
run_at: 2026-08-07T14:04:36+00:00
pair: pair1
stage: publish
carousel: crsl_20260803_1936_830

### Error
TikTok detected potential spam content (user_abuse). Платформенная модерация, не баг publish.

### fix_summary
Карусель в failed. Нужна правка caption/контента на стороне фабрики или ручной retry позже.

---

## INC-20260807-001 (notify not_attempted)

status: fixed
run_at: 2026-08-07T14:04:40+00:00
pair: pair1
stage: notify
carousel: crsl_20260803_1936_830

### Error
MAX report could not parse Zernio instagram/tiktok blocks (not_attempted при batch error)

### fix_summary
`notify_max.py` — при `errors[]` без `results` отправляет отчёт с текстом ошибки вместо not_attempted.

### files_changed
- scripts/notify_max.py

---

## INC-20260807-001 (Zernio 429)

status: fixed
run_at: 2026-08-07T14:07:24+00:00
pair: pair1
stage: publish
carousel: crsl_20260803_1937_059, crsl_20260803_1937_448

### Error
HTTP 429 Too Many Requests от Zernio API

### fix_summary
- `http_client.py`: backoff 60с при 429
- `publish_engine.py`: post_zernio retries 2→3, пауза 5с между IG и TT

### files_changed
- scripts/lib/http_client.py
- scripts/lib/publish_engine.py
