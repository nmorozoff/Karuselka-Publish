# Publish pipeline fix queue

Инциденты для Fixic после Cloud Agent / `publish_worker.py`.

Формат: `scripts/publish_incident.py` или автоматически из `publish_engine` при ошибке.

## INC-20260807-001

status: fixed
run_at: 2026-08-07T18:04:53.369088+00:00
pair: pair2
stage: publish
carousel: crsl_20260806_1602_927

### Error
```
HTTP unreachable https://zernio.com/api/v1/posts: HTTP Error 400: Bad Request
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`
- `scripts/lib/publish_cleanup.py`
- `scripts/lib/max_notify.py`

fix_summary: `http_client.urlopen` теперь пробрасывает HTTPError с телом ответа Zernio; добавлена `validate_instagram_image_slides()` — dry-run ловит aspect ratio до реальной публикации.
files_changed:
- `scripts/lib/http_client.py`
- `scripts/lib/publish_engine.py`

---

## INC-20260807-002

status: needs-human
run_at: 2026-08-07T18:07:25.337383+00:00
pair: pair2
stage: publish
carousel: crsl_20260806_1602_927, crsl_20260806_1605_671

### Error
```
Instagram aspect ratio 671x895 (0.75:1) — 1px выше лимита Zernio/IG (max height 894 для width 671). TikTok публикуется OK.
```

### Context
```json
{"root_cause": "factory export pair2 minimalism — PNG 671x895 вместо 671x894 или 4:5 crop"}
```

### Suggested files to inspect/change
- Karuselka-emdr export_publish_bundle.py (фабрика, не publish)

fix_summary: publish не может исправить ассеты; нужен re-export в фабрике с crop 4:5 (max height width/0.75). После фикса — `--retry-failed` для pair2.

---

## INC-20260807-003

status: fixed
run_at: 2026-08-07T18:08:13.763684+00:00
pair: pair2
stage: publish
carousel: crsl_20260806_1602_927

### Error
```
Instagram aspect ratio for slide-02.png: 671x895 (0.750:1). Allowed 0.75–1.91. Max height for 671px width is 894px (crop to 4:5). Re-export from factory.
```

### Context
```json
{}
```

### Suggested files to inspect/change
- `scripts/lib/publish_engine.py`

fix_summary: дубликат INC-002; валидация в dry-run работает.

---
