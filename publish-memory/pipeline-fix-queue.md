# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260914-001

status: fixed
run_at: 2026-09-14T18:04:16.623911+00:00
pair: pair2
stage: publish
carousel: crsl_20260914_1236_281

### Error
Instagram fetch failed (Zernio media container 1) → retry blocked by 409 → Fixic retry → partial IG OK, TikTok capacity.

### Context
```json
{
  "first_error": "Failed to create media container 1: fetch failed",
  "retry_error": "HTTP 409 Conflict",
  "final": "PARTIAL_IG_OK tiktok_capacity"
}
```

### fix_summary
Удалён зависший Zernio-пост (DELETE), повторная публикация: IG @natalia_morozova_psy ✅, TikTok @natalyamorozovapsy ❌ capacity. Добавлены классификаторы `media_fetch`/`tiktok_capacity` и авто-cleanup 409 в `post_zernio`.

### files_changed
- `scripts/lib/publish_failure.py`
- `scripts/lib/publish_engine.py`

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_failure.py`

---
