# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260806-001

status: open
run_at: 2026-08-06T08:01:15.127256+00:00
pair: pair2
stage: publish
carousel: crsl_20260805_1935_596

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

## INC-20260806-001

status: open
run_at: 2026-08-06T08:01:37.196483+00:00
pair: pair2
stage: publish
carousel: crsl_20260805_1935_596

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

---

## INC-20260806-001

status: open
run_at: 2026-08-06T08:01:37.222411+00:00
pair: pair2
stage: notify
carousel: unknown

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

## INC-20260806-001

status: open
run_at: 2026-08-06T08:02:42.828491+00:00
pair: pair2
stage: publish
carousel: crsl_20260805_2033_209

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
