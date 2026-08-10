# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260810-001

status: needs-human
run_at: 2026-08-10T17:07:52.091648+00:00
pair: pair1
stage: publish
carousel: crsl_20260621_1151_8oaunh
fix_summary: Zernio TikTok 400 — повреждён slide-06.png (libspng read error). Путь legacy /Content_Plan/crsl_20260621_1151_8oaunh, 7 PNG. Нужен re-export слайда из фабрики. http_client: HTTPError body теперь в тексте ошибки.
files_changed: scripts/lib/http_client.py

### Error
```
HTTP 400 https://zernio.com/api/v1/posts: {"error":"TikTok Image 5: Failed to resize image: pngload_buffer: libspng read error"}
```

### Context
```json
{
  "dropbox_folder": "/Content_Plan/crsl_20260621_1151_8oaunh",
  "images": 7,
  "instagram_may_be_published": true
}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/http_client.py`

---
