# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260811-001

status: needs-human
run_at: 2026-08-11T19:27:21.733506+00:00
pair: pair3
stage: publish
carousel: crsl_20260810_1934_222
fix_summary: TikTok spam (user_abuse) — тексты фабрики; publish теперь сохраняет partial IG success
files_changed: scripts/lib/publish_engine.py, scripts/lib/publish_failure.py

### Error
```
TikTok spam detection: TikTok detected potential spam content (user_abuse)
```

### Context
```json
{"action": "Фабрика: переписать TikTok описание без spam-триггеров (см. shared/KARUSELKA-FACTORY-PUBLISH-SPEC.md)"}
```

---

## INC-20260811-002

status: fixed
run_at: 2026-08-11T19:27:45.000914+00:00
pair: pair3
stage: notify
carousel: crsl_20260810_1934_222
fix_summary: notify_max.py теперь парсит batch errors из worker-last-run.json
files_changed: scripts/notify_max.py

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks
```

---

## INC-20260811-003

status: fixed
run_at: 2026-08-11T19:35:38.626657+00:00
pair: pair3
stage: publish
carousel: crsl_20260810_1941_261
fix_summary: Zernio 429 rate-limit — partial_instagram записан, TikTok resume на следующем run
files_changed: scripts/lib/publish_engine.py

### Error
```
PARTIAL_IG_OK|HTTP Error 429: Too Many Requests
```

---
