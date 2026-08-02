# Karuselka Publish

**Доставка** Instagram/TikTok каруселей из очереди Airtable → Zernio API.

Генерация контента остаётся в репозитории [Karuselka-emdr](https://github.com/nmorozoff/Karuselka-emdr) и заканчивается на `export_publish_bundle.py`.

```text
┌─────────────────────────────┐     ┌──────────────────────────────┐
│  Karuselka-emdr (фабрика)   │     │  karuselka-publish (этот repo)│
│  copy → Kie → Grok → export │ ──► │  Airtable → Zernio → cleanup  │
└─────────────────────────────┘     └──────────────────────────────┘
         Dropbox + Airtable row              читает ту же очередь
```

## Быстрый старт

```bash
# Секреты (можно symlink на фабрику)
cp publish-memory/*.env.example publish-memory/*.env.local
# или:
cd publish-memory && ln -sf ../../КАРУСЕЛЬКА/carusel-memory/airtable.env.local airtable.env.local
ln -sf ../../КАРУСЕЛЬКА/carusel-memory/dropbox.env.local publish-memory/dropbox.env.local
ln -sf ../../КАРУСЕЛЬКА/carusel-memory/zernio.env.local publish-memory/zernio.env.local
ln -sf ../../КАРУСЕЛЬКА/carusel-memory/telegram.env.local publish-memory/telegram.env.local

# Статус очереди
python scripts/publish_status.py

# Dry-run (без публикации)
python scripts/publish_worker.py --pair pair1 --name crsl_20260802_1320_782 --dry-run

# Публикация — только по явному запросу
python scripts/publish_worker.py --pair pair1 --limit 1
```

## Cursor plugin

Плагин: `~/.cursor/plugins/local/karuselka-publish/`

Директор Publish — статус, dry-run, публикация, Telegram. **Не генерирует** слайды.

## Расписание

| Пара | Cloud Scheduler (MSK) | Локальный cron |
|------|----------------------|----------------|
| pair1 | 10:00, 17:00, 20:00 | `install_publish_cron.sh` |
| pair2 | 11:00, 18:00, 21:00 | то же |

**Один деплой в облако:**

```bash
./deploy/cloud-worker/setup-cloud-automation.sh
```

## Контракт очереди

См. [`shared/queue-contract.md`](shared/queue-contract.md) — единственный мост с фабрикой.

## Структура

```text
scripts/
  publish_worker.py      # CLI воркер
  publish_status.py      # статус очереди
  lib/publish_engine.py  # ядро
publish-memory/
  accounts-pairs.json
  worker-state.json
  *.env.local            # не коммитить
deploy/cloud-worker/     # Cloud Run + Scheduler
shared/queue-contract.md
```

## Переменные

| Переменная | Default | Смысл |
|------------|---------|-------|
| `PUBLISH_MODE` | `grok_hook` | IG: mp4+png; TT: png only |
| `EXPECTED_IMAGE_SLIDES` | `6` | Число PNG в папке |

## Чеклист: deprecated в Karuselka-emdr

| Путь в фабрике | Действие |
|----------------|----------|
| `scripts/publish_worker.py` | Deprecated → karuselka-publish |
| `scripts/lib/publish_*.py`, `worker_state.py` | Перенесено |
| `scripts/run_publish_worker.sh`, `install_publish_cron.sh` | Перенесено |
| `deploy/cloud-worker/` | Деплой из karuselka-publish |
| `scripts/deploy_make_scenario.py` | Deprecated (Make не используется) |

**Оставить в фабрике:** `export_publish_bundle.py`, запись в Airtable/Dropbox.
