# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20261027-001

status: needs-human
run_at: 2026-10-27T15:05:42.173366+00:00
pair: pair3
stage: queue
carousel: —

fix_summary: В Dropbox Queue 2 полностью готовые карусели (6 PNG), но обе в global failed с needs_human/retryable=false (409 conflict + instagram_format). Ещё 7 папок — незавершённый экспорт фабрики (1–5 слайдов). Публикация pair3 невозможна без ручного purge/clear failed или дозавершения очереди на фабрике.

### Error
```
queue empty at dry-run-first (effective ready=0: 2 ready folders skipped as failed)
```

### Context
```json
{
  "ready_folders_in_dropbox": 2,
  "failed_ready": [
    "crsl_k3_20261005_0850_expert-light_1305",
    "crsl_k3_20261013_0800_bordo_3860"
  ],
  "incomplete_folders": 7,
  "max_notified": true
}
```

### Suggested files to inspect/change
- `scripts/manage_failed_queue.py` (purge/clear после решения человека)
- фабрика Karuselka-emdr — дозавершить PNG в Queue

---
