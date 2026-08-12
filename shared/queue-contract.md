# Контракт очереди: фабрика → publish

Единственный мост между **Karuselka-emdr** (фабрика) и **karuselka-publish** (доставка).

## Поток

```text
Фабрика (export_publish_bundle.py)
  → Dropbox /Content_Plan/Queue/{Name}/
  → Airtable row (единая таблица, FIFO по createdTime / порядку строк)
        ↓
Publish (publish_worker.py --pair pairN)
  → берёт ПЕРВУЮ строку глобальной очереди (поле «Пара» НЕ фильтрует)
  → публикует в Instagram+TikTok аккаунты pairN (слот расписания)
  → cleanup: удалить строку Airtable + папку Queue/{Name}
  → Макс-бот notify
```

**Маршрутизация стилей → аккаунты:** не через столбец Airtable, а через **расписание automation**:

| Слот MSK | `--pair` | Куда уходит первая карусель в очереди |
|----------|----------|--------------------------------------|
| 10:00, 17:00, 20:00 | pair1 | IG/TikTok pair1 |
| 11:00, 18:00, 21:00 | pair2 | IG/TikTok pair2 |
| 12:00, 19:00, 22:00 | pair3 | IG/TikTok pair3 |

Фабрика кладёт карусели любого стиля в одну очередь; какой аккаунт получит конкретную карусель — определяет **кто первый забрал слот** после её появления в Queue.

## Airtable

**Единая таблица:** `Каруселька Queue` (`tblIf0GuVmiDj199M`).

| Поле | Смысл |
|------|-------|
| `Name` | Имя папки карусели |
| `Описание карусели` | Caption Instagram |
| `TikTok заголовок` | Заголовок TikTok (≤90 символов) |
| `TikTok описание` | Описание TikTok |
| `Пара` | **Справочно** (фабрика); publish **игнорирует** при выборе строки |

Конфиг: `airtable_queue` в `accounts-pairs.json`.

## Dropbox

**Единая очередь:** `/Content_Plan/Queue/{Name}/`

Конфиг: `queue_dropbox_root` в `publish-memory/accounts-pairs.json`.

Legacy fallback (если папка ещё в старом месте): `/Content_Plan/Pair1|2|3/{Name}/`.

### Файлы в папке карусели

| Файл | Instagram | TikTok |
|------|-----------|--------|
| `slide-01.mp4` | ✅ hook (mixed carousel) | ❌ |
| `slide-01.png` … `slide-06.png` | slide-02..06 или все 6 | все 6 PNG |
| `caption.txt` | справочно | — |
| `manifest.json` | контракт export | — |

## Zernio

- **Instagram:** `slide-01.mp4` + `slide-02..06.png` (mixed) или все PNG
- **TikTok:** `slide-01..06.png`, `auto_add_music: true`
- Режим: `PUBLISH_MODE=grok_hook`

## Worker state

Dropbox `/Content_Plan/.karuselka/worker-state.json` (cloud):

- `published` / `published_pair2` / `published_pair3` — история по слотам
- `failed` — глобально по имени карусели (блокирует очередь до retry/purge)

## Команды

```bash
python scripts/publish_status.py
python scripts/publish_worker.py --pair pair2 --limit 1 --dry-run-first
```

`--pair` = **куда публиковать** (Zernio аккаунты), не фильтр Airtable.
