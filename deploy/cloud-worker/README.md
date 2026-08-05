# Облачная автоматизация публикации (LEGACY)

> **Deprecated.** Основной путь: [`deploy/cursor-automation/README.md`](../cursor-automation/README.md) (Cursor Cloud Agent + Automations).

**Cloud Scheduler → Cloud Run → Zernio** (без Mac, без Make).

## Расписание (Europe/Moscow)

| Пара | Время MSK |
|------|-----------|
| **pair1** | 10:00, 17:00, 20:00 |
| **pair2** | 11:00, 18:00, 21:00 |

По 1 карусели за запуск (`limit=1`) → 3 карусели/день на пару.

```text
Cloud Scheduler (6 jobs)
    → POST /run?pair=pair1|pair2&limit=1  (X-Worker-Key)
    → karuselka-publish-worker (Cloud Run)
        → Airtable → Dropbox → Zernio IG+TikTok
        → cleanup → Макс-бот
    → worker-state в Dropbox /Content_Plan/.karuselka/worker-state.json
```

## Одна команда (полный setup)

```bash
# Секреты уже в publish-memory/*.env.local (symlink с фабрики OK)
./deploy/cloud-worker/setup-cloud-automation.sh
```

Шаги внутри:
1. `scripts/prepare_cloud_env.sh` → `.env.deploy.yaml`
2. `deploy/cloud-worker/deploy.sh` → Cloud Run
3. `deploy/cloud-worker/setup-scheduler.sh` → 6 cron jobs

## Пошагово

```bash
cp publish-memory/cloud-worker.env.example publish-memory/cloud-worker.env.local
# PROJECT_ID, WORKER_API_KEY, CLOUD_RUN_API_KEY

./scripts/prepare_cloud_env.sh
./deploy/cloud-worker/deploy.sh
./deploy/cloud-worker/setup-scheduler.sh
```

## Ручной тест

```bash
WORKER_URL=$(gcloud run services describe karuselka-publish-worker --region europe-west1 --format='value(status.url)')

# pair1 dry-run
curl -sS -X POST \
  -H "X-Worker-Key: $WORKER_API_KEY" \
  "${WORKER_URL}/run?pair=pair1&limit=1&dry_run=true"

# pair2 dry-run
curl -sS -X POST \
  -H "X-Worker-Key: $WORKER_API_KEY" \
  "${WORKER_URL}/run?pair=pair2&limit=1&dry_run=true"
```

## Scheduler jobs (имена)

| Job ID | Pair | Cron MSK |
|--------|------|----------|
| `karuselka-publish-pair1-1000` | pair1 | 10:00 |
| `karuselka-publish-pair1-1700` | pair1 | 17:00 |
| `karuselka-publish-pair1-2000` | pair1 | 20:00 |
| `karuselka-publish-pair2-1100` | pair2 | 11:00 |
| `karuselka-publish-pair2-1800` | pair2 | 18:00 |
| `karuselka-publish-pair2-2100` | pair2 | 21:00 |

Legacy jobs `karuselka-publish-1100/1700/2100` удаляются при setup.

## Требования GCP

- Cloud Run API, Cloud Scheduler API
- Billing включён
- `gcloud auth login`
- Секреты: Airtable, Dropbox OAuth, Zernio, MAX (`MAX_BOT_TOKEN`, `MAX_PREVIEW_CHAT_ID`), `WORKER_API_KEY`

## Локальный резерв (Mac)

```bash
./scripts/install_publish_cron.sh   # то же расписание через crontab
```
