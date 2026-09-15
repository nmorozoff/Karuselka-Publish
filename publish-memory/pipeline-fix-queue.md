# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260915-001

status: fixed
run_at: 2026-09-15T18:02:04.315620+00:00
pair: pair2
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

fix_summary: `--retry-failed` не видел partial IG (карусель уже в published). Добавлена отдельная ветка `elif retry_failed` без фильтра `all_published`.
files_changed:
- `scripts/lib/publish_engine.py`

---

## INC-20260915-002

status: needs-human
run_at: 2026-09-15T18:03:49.433678+00:00
pair: pair2
stage: publish
carousel: crsl_20260914_1235_730

### Error
```
TikTok direct posting is at capacity (quota_exhausted). IG уже опубликован (partial).
```

### Context
```json
{"also_failed": "crsl_20260914_1236_281", "category": "tiktok_capacity"}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`

fix_summary: Retry через `--retry-failed` теперь работает (см. INC-20260915-001). TikTok capacity — внешняя квота Zernio/TikTok; повтор на следующем слоте (11:00/21:00 MSK) или `tiktokSettings.draft: true`.
files_changed:
- `scripts/lib/publish_engine.py`

---
