# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261110-001

status: needs-human
run_at: 2026-11-10T15:09:58.761338+00:00
pair: pair3
stage: publish
carousel: crsl_k3_20261109_1033_sketch-p3_9606
fix_summary: http_client.urlopen теперь пробрасывает HTTPError (тело Zernio в сообщении); publish_incident --list-open без --pair. Карусель sketch-p3_9606 остаётся в failed (Zernio 409) — ручной разбор / retry с --include-needs-human.
files_changed: scripts/lib/http_client.py, scripts/publish_incident.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 409: Conflict
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---
