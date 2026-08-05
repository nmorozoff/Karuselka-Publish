# Контракт очереди: фабрика → publish

Единственный мост между **Karuselka-emdr** (фабрика) и **karuselka-publish** (доставка).

## Поток

```text
Фабрика (export_publish_bundle.py)
  → Dropbox /Content_Plan/Pair1|Pair2|Pair3/{Name}/
  → Airtable row (очередь)
        ↓
Publish (publish_worker.py)
  → Zernio API (PUBLISH_MODE=grok_hook / mixed)
  → cleanup Airtable + Dropbox
  → Макс-бот notify
```

## Airtable

| Пара | Base | Table |
|------|------|-------|
| pair1 | `appQTNsDMuodYyp34` | `tblFWCmLCXLrOdKut` |
| pair2 | `appQTNsDMuodYyp34` | `tbl2zotNwOmWLSTyC` |
| pair3 | `appQTNsDMuodYyp34` | `tblNv5eMi1BXbu4Tq` |

### Поля (обязательные)

| Поле Airtable | Смысл |
|---------------|-------|
| `Name` | Имя папки карусели, напр. `crsl_20260802_1320_782` |
| `Описание карусели` | Caption Instagram (Zernio) |
| `TikTok заголовок` | Заголовок TikTok (≤90 символов) |
| `TikTok описание` | Описание TikTok |

`Dropbox Path` — **опционально** (сейчас ломает Airtable 422 при create; publish резолвит путь из `accounts-pairs.json`).

## Dropbox

| Пара | Корень папки |
|------|--------------|
| pair1 | `/Content_Plan/Pair1/{Name}/` |
| pair2 | `/Content_Plan/Pair2/{Name}/` |
| pair3 | `/Content_Plan/Pair3/{Name}/` |

`resolve_carousel_dropbox_path()` использует `pair.dropbox_root` из `publish-memory/accounts-pairs.json`, **не** legacy `/Content_Plan/{Name}`.

### Файлы в папке карусели

| Файл | Instagram | TikTok |
|------|-----------|--------|
| `slide-01.mp4` | ✅ hook (mixed carousel) | ❌ не уходит |
| `slide-01.png` … `slide-06.png` | slide-02..06 в mixed carousel или все 6 в photo | все 6 PNG |
| `caption.txt` | справочно | — |
| `manifest.json` | контракт export | — |

### manifest.json (от фабрики)

```json
{
  "publish": {
    "instagram": { "mode": "mixed", "slide1": "slide-01.mp4", "slides2n": "slide-02..06.png" },
    "tiktok": { "mode": "photo_carousel", "slides": "slide-01..06.png" }
  }
}
```

Publish-воркер ориентируется на `PUBLISH_MODE=grok_hook` + наличие `slide-01.mp4`, не на поле manifest.

## Zernio

- **Instagram:** `slide-01.mp4` + `slide-02..06.png` (mixed carousel)
- **TikTok:** только `slide-01..06.png` (`auto_add_music: true`)
- Режим: `PUBLISH_MODE=grok_hook` (default)

## Worker state

`publish-memory/worker-state.json` (локально) или Dropbox `/Content_Plan/.karuselka/worker-state.json` (cloud):

```json
{
  "published": ["crsl_..."],
  "published_pair2": [],
  "published_pair3": [],
  "failed": { "crsl_...": { "at": "...", "error": "..." } },
  "last_run": {}
}
```

Ошибка одной карусели → `failed`, очередь продолжается.

## Секреты (не коммитить)

| Файл | Переменные |
|------|------------|
| `publish-memory/airtable.env.local` | `AIRTABLE_ACCESS_TOKEN` |
| `publish-memory/dropbox.env.local` | `DROPBOX_ACCESS_TOKEN` или OAuth trio |
| `publish-memory/zernio.env.local` | `ZERNIO_API_KEY`, `ZERNIO_PAIR2_API_KEY`, `ZERNIO_PAIR3_API_KEY`, `PUBLISH_MODE` |
| `publish-memory/max.env.local` | `MAX_BOT_TOKEN`, `MAX_NOTIFY_CHAT_ID` или `MAX_PREVIEW_CHAT_ID` |

Можно symlink на `Karuselka-emdr/carusel-memory/*.env.local` при локальной разработке.

## Команды publish

```bash
# Статус очереди
python scripts/publish_status.py

# Dry-run (без Zernio/cleanup)
python scripts/publish_worker.py --pair pair1 --name crsl_... --dry-run

# Публикация (только по явному запросу)
python scripts/publish_worker.py --pair pair1 --limit 1
```
