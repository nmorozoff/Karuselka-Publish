# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260809-001

status: needs-human
run_at: 2026-08-09T14:04:06.280947+00:00
pair: pair1
stage: publish
carousel: crsl_20260806_1559_385

### Error
```
Zernio 400: Instagram aspect ratio 0.75:1 (3:4 Story/TikTok) — нужен 4:5 для Instagram feed. Фабрика Karuselka-emdr должна экспортировать PNG 4:5.
```

### Context
```json
{
  "root_cause": "factory_aspect_ratio",
  "zernio_detail": "Instagram Image 2: Aspect ratio 0.75:1 is outside Instagram's allowed range. Crop to 4:5 for feed posts."
}
```

### Fix
status: fixed (publish-side diagnostics)
fix_summary: http_client больше не маскирует HTTPError — Zernio body виден в логах; notify_max корректно шлёт ошибку при пустом results[]
files_changed:
- `scripts/lib/http_client.py`
- `scripts/notify_max.py`

### Remaining (needs-human)
- Перегенерировать слайды pair1 в формате 4:5 (Karuselka-emdr), затем `--retry-failed`

---

## INC-20260809-002

status: needs-human
run_at: 2026-08-09T14:06:09.521877+00:00
pair: pair1
stage: publish
carousel: crsl_20260621_1151_8oaunh

### Error
```
Zernio 400: Instagram aspect ratio 3:4 — та же причина, retry-failed не помог.
```

### Fix
status: needs-human
fix_summary: legacy carousel, aspect ratio 3:4 — нужна перегенерация на фабрике

---

## INC-20260809-003

status: needs-human
run_at: 2026-08-09T14:07:27.140087+00:00
pair: pair1
stage: publish
carousel: crsl_20260806_1601_709

### Error
```
Zernio 400: Instagram aspect ratio 3:4 — следующая ready карусель, та же ошибка.
```

### Fix
status: needs-human
fix_summary: все текущие ready pair1 имеют 3:4 PNG — блокер на стороне фабрики

---

## INC-20260809-004

status: fixed
run_at: 2026-08-09T14:06:23.396707+00:00
pair: pair1
stage: notify
carousel: unknown

### Error
```
MAX report could not parse Zernio instagram/tiktok blocks (not_attempted при error status)
```

### Fix
status: fixed
fix_summary: notify_max.py теперь читает errors[] из worker-last-run.json при status=error
files_changed:
- `scripts/notify_max.py`

---
