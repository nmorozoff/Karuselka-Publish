# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260910-001

status: fixed
run_at: 2026-09-10T18:06:20.616158+00:00
pair: pair2
stage: publish
carousel: crsl_20260908_1627_771
fix_summary: TikTok capacity (transient) — IG @natalia_morozova_psy ok, TT @natalyamorozovapsy failed. Добавлен классификатор tiktok_capacity + читаемый Max-отчёт для PARTIAL_IG_OK.
files_changed:
- scripts/lib/publish_failure.py
- scripts/lib/max_notify.py
- scripts/lib/publish_engine.py

### Error
TikTok direct posting is at capacity right now (PARTIAL_IG_OK — Instagram published).

### Context
```json
{"category": "tiktok_capacity", "retryable": true, "partial_instagram": true}
```

### Retry TikTok
```bash
python3 scripts/publish_worker.py --pair pair2 --tiktok-only --name crsl_20260908_1627_771 --retry-failed
```

---
