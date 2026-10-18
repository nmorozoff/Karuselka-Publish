# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260911-001

status: fixed
run_at: 2026-09-11T08:07:01.290784+00:00
pair: pair2
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first (ready=0, failed=19 — partial IG blocked retry)
```

### Context
```json
{"ready": 0, "failed": 19, "airtable_total": 32}
```

### fix_summary
Добавлен `_partial_resume_names` в `publish_engine.py`: `--retry-failed` включает partial_published с IG ok даже если имя уже в published_pair*.

### files_changed
- `scripts/lib/publish_engine.py`

---

## INC-20260911-002

status: fixed
run_at: 2026-09-11T08:08:50.138004+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_0746_191

### Error
```
TikTok direct posting is at capacity (tiktok_capacity, transient)
```

### Context
```json
{"mode": "tiktok_resume", "instagram": "ok @natalia_morozova_psy", "partial_instagram": true}
```

### fix_summary
Transient TikTok capacity — код корректен, retry на слоте 21:00 MSK. Cleanup skipped (partial).

### files_changed
—

---
