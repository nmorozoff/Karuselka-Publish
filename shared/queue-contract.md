# Контракт очереди: фабрика → publish

Единственный мост между **Karuselka-emdr** (фабрика) и **karuselka-publish** (доставка).

## Поток (Dropbox-first)

```text
Фабрика (export_publish_bundle.py)
  → 6 вариантов стиля (a–f), каждый в свою папку
  → Dropbox /Content_Plan/Queue/{Name}/
  → manifest.json + caption.txt (+ slide-*.png, опционально slide-01.mp4)
  → Airtable НЕ используется при publish_queue_backend=dropbox

Publish (publish_worker.py --pair pairN --pick top|bottom|fifo)
  → список ready-папок в Queue (6/7/9 PNG)
  → выбор по --pick (баланс стилей между слотами)
  → публикует в Instagram+TikTok аккаунты pairN
  → cleanup: удалить папку Queue/{Name} (полный успех)
  → worker-state.json + Макс-бот
```

**Имена папок:** `crsl_{YYYYMMDD}_{HHMM}_{variant}_{styleSlug}_{rand4}`  
Пример: `crsl_20260928_1410_a_expert-light_4821`

## Pick по automation (согласовано)

Ready-папки сортируются по `Name` ASC.

| Слот MSK | `--pair` | `--pick` |
|----------|----------|----------|
| 10:00 | pair1 | **top** |
| 20:00 | pair1 | **bottom** |
| 11:00 | pair2 | **bottom** |
| 21:00 | pair2 | **top** |
| 12:00 | pair3 | **fifo** |
| 22:00 | pair3 | **fifo** |

`--pair` = **куда публиковать** (Zernio IG/TT), не фильтр по стилю.

## Конфиг

`publish-memory/accounts-pairs.json`:

- `publish_queue_backend`: `"dropbox"` (default) или `"airtable"` (legacy)
- `queue_dropbox_root`: `/Content_Plan/Queue`
- `airtable_queue` — только mapping имён полей для caption (legacy + manifest)

Env:

- `PUBLISH_QUEUE_BACKEND=dropbox`
- `EXPORT_SKIP_AIRTABLE=1` на фабрике (авто при dropbox backend)

## Dropbox

**Единая очередь:** `/Content_Plan/Queue/{Name}/`

### Файлы в папке карусели

| Файл | Назначение |
|------|------------|
| `slide-01.mp4` | Instagram hook (mixed) |
| `slide-01.png` … `slide-06.png` | IG + TikTok |
| `caption.txt` | Instagram caption |
| `manifest.json` | variant, style_id, tiktok title/desc, createdAt |

## Zernio

- **Instagram:** mixed или photo carousel
- **TikTok:** все PNG, `auto_add_music: true`
- Режим: `PUBLISH_MODE=grok_hook`

## Worker state

Dropbox `/Content_Plan/.karuselka/worker-state.json` (cloud):

- `published` / `published_pair2` / `published_pair3`
- `failed` — глобально по имени папки

## Команды

```bash
python scripts/publish_status.py
python scripts/publish_worker.py --pair pair1 --pick top --limit 1 --dry-run-first
python scripts/publish_worker.py --pair pair2 --pick bottom --limit 1 --dry-run-first
python scripts/publish_worker.py --pair pair3 --pick fifo --limit 1 --dry-run-first
```
