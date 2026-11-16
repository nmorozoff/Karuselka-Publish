# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261116-001

status: needs-human
run_at: 2026-11-16T15:04:04.832128+00:00
pair: pair3
stage: queue
carousel: —

### Error
```
queue empty at dry-run-first (единственная папка в failed, ready=0)
```

### Context
```json
{"queue_folder":"crsl_k3_20261109_1033_sketch-p3_9606","failed_category":"conflict"}
```

fix_summary: Очередь заблокирована failed; авто-FIFO не берёт карусель. Требуется разблокировка Zernio (см. INC publish ниже) или новый экспорт с фабрики.

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

---

## INC-20261116-002

status: needs-human
run_at: 2026-11-16T15:08:22.814453+00:00
pair: pair3
stage: publish
carousel: crsl_k3_20261109_1033_sketch-p3_9606

### Error
```
Zernio instagram: Post created but publishing failed — Post is not scheduled or is already processing (stuck publishing).
```

### Context
```json
{"zernio_post_id":"6afb1b8b4c625e8a60d8c191","detail":"Post is not scheduled or is already processing"}
```

fix_summary: Зависший пост в Zernio (status=publishing). Ручное удаление/завершение в UI Zernio для @morozova_natalia_psy, затем clear failed + повтор. Кодовый фикс не внедрялся (needs-human).

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

---
