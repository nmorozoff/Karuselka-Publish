# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261030-001

status: needs-human
run_at: 2026-10-30T16:07:30.410251+00:00
pair: pair1
stage: publish
carousel: crsl_k3_20261027_1813_expert-dark_1884
fix_summary: Zernio 409 Conflict (duplicate post). Папка Queue уже не в Dropbox; запись в worker-state failed (conflict). Удалить дубликат поста в Zernio UI для pair1 или подтвердить, что слот закрыт. Код: `run_publish_batch` больше не трактует `--limit 0` как 1 (случайный двойной publish attempt в этом run).
files_changed:
- scripts/lib/publish_engine.py

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 409: Conflict
```

### Context
```json
{"dry_run_first": true, "next_fifo_ok": "crsl_k3_20261027_1813_expert-dark_7450 slide_count=6"}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---
