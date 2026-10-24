# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260808-001

status: open
run_at: 2026-08-08T14:01:52.461550+00:00
pair: pair1
stage: publish
carousel: crsl_20260805_1939_322

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

## INC-20260808-001

status: open
run_at: 2026-08-08T14:02:00.426479+00:00
pair: pair1
stage: publish
carousel: crsl_20260805_1939_322

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

## INC-20260808-001

status: open
run_at: 2026-08-08T14:02:03.496362+00:00
pair: pair1
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

## INC-20260808-001

status: open
run_at: 2026-08-08T14:02:28.799103+00:00
pair: pair1
stage: publish
carousel: crsl_20260805_2037_971

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
