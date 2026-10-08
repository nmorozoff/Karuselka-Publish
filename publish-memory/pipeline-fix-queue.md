# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260915-001

status: fixed
run_at: 2026-09-15T08:01:40.553811+00:00
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

### fix_summary
Восстановлен `_partial_resume_names`: partial IG (failed + published) блокировали dry-run-first. Авто-retry partial в `publish_worker.py`.

### files_changed
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/publish_worker.py`

---

## INC-20260915-002

status: fixed
run_at: 2026-09-15T08:04:01.494281+00:00
pair: pair2
stage: publish
carousel: crsl_20260914_1236_281

### Error
```
TikTok direct posting is at capacity (tiktok_capacity, transient)
```

### Context
```json
{"mode": "tiktok_resume", "instagram": "ok @natalia_morozova_psy"}
```

### fix_summary
Ожидаемый transient TikTok capacity. IG ok, cleanup skipped. Resume tiktok на слоте 21:00 MSK. Классификатор tiktok_capacity добавлен; incident skip для partial transient.

### files_changed
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_engine.py`

---
