# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260807-001

status: fixed
run_at: 2026-08-07T19:04:11.071603+00:00
pair: pair3
stage: publish
carousel: crsl_20260805_0825_516
fix_summary: Zernio HTTP 400 терялся в urlopen; IG/TT публикуются независимо; ошибки теперь с телом ответа Zernio
files_changed: scripts/lib/http_client.py, scripts/lib/publish_engine.py

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

## INC-20260807-001

status: fixed
run_at: 2026-08-07T19:04:21.737119+00:00
pair: pair3
stage: notify
carousel: unknown
fix_summary: notify not_attempted из-за исключения до возврата result; исправлено независимой публикацией платформ
files_changed: scripts/lib/publish_engine.py

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

## INC-20260807-001

status: needs-human
run_at: 2026-08-07T19:08:04.660628+00:00
pair: pair3
stage: publish
carousel: crsl_20260805_1852_903
fix_summary: Zernio отклоняет PNG pair3 — aspect ratio 3:4/9:16 вместо 4:5 для Instagram feed. Нужен экспорт 4:5 в фабрике Karuselka-emdr (export_publish_bundle). TikTok публикуется успешно (partial).

### Error
```
instagram: HTTP 400 — Instagram Image 2 aspect ratio 0.75:1 (815×1087px) вне допустимого для feed; crop to 4:5
```

### Context
```json
{
  "partial": true,
  "tiktok": "ok/processing",
  "instagram": "failed aspect ratio"
}
```

### Suggested files to inspect/change
- Karuselka-emdr export_publish_bundle.py (4:5 PNG для Instagram)

---
