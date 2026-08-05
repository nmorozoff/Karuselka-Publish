# Cursor Automations — Karuselka Publish

**Замена** GCP Cloud Run + Cloud Scheduler на **Cursor Cloud Agent** по расписанию.

## Зачем

| Было (GCP) | Стало (Cursor) |
|------------|----------------|
| Cloud Run HTTP worker | Cloud Agent в репозитории |
| gcloud deploy, proxy на Mac | Secrets в Cursor Dashboard |
| Telegram (не доходил) | Макс-бот (работает) |
| Чёрный ящик curl | Агент видит логи, может починить |

## Расписание (MSK)

| Пара | Время |
|------|-------|
| **pair1** | 10:00, 17:00, 20:00 |
| **pair2** | 11:00, 18:00, 21:00 |
| **pair3** | 12:00, 19:00, 22:00 |

По 1 карусели за запуск. Cron в JSON — **UTC** (MSK−3).

## Быстрый старт

### 1. Secrets в Cursor

[Cloud Agents → Runtime Secrets](https://cursor.com/dashboard/cloud-agents)

Список: `CLOUD-SECRETS.md` / `cloud-secrets-checklist.txt`

Скопировать значения из локальных `publish-memory/*.env.local` (symlink с фабрики + Макс из «Посты EMDR»).

### 2. Проверка (локально или Cloud Agent)

```bash
python3 scripts/materialize_cloud_env.py --check
python3 scripts/cloud_preflight.py
```

### 3. Создать 9 Automations

Черновики: `workflows/*.json` (пересобрать: `python3 deploy/cursor-automation/build-workflows.py`).

**В Cursor:** Automations → New → Import / или попроси агента открыть редактор с prefill:

- `deploy/cursor-automation/workflows/karuselka-publish-pair1-1000.json`
- … (ещё 8 файлов, см. `workflows/index.json`)

Для каждой automation:

- **Trigger:** Schedule (cron из JSON)
- **Repo:** `nmorozoff/Karuselka-Publish` / `main`
- **Compute:** Cloud Agent (в dashboard)
- **Install:** `.cursor/environment.json` → `materialize_cloud_env.py`

### 4. Отключить legacy GCP

После тестового run automation:

```bash
chmod +x deploy/cursor-automation/disable-gcp-scheduler.sh
./deploy/cursor-automation/disable-gcp-scheduler.sh
```

Cloud Run можно оставить выключенным (Scheduler paused) или удалить позже.

## Что делает агент

См. `.cursor/karuselka-publish-handoff.md`:

1. Materialize secrets
2. Статус очереди
3. `publish_worker.py --pair pairN --limit 1 --dry-run-first`
4. Отчёт в Макс (авто при успехе + вручную при ошибке/пустой очереди)

## Ручной тест (без automation)

```bash
python3 scripts/publish_status.py
python3 scripts/publish_worker.py --pair pair1 --limit 1 --dry-run
```

## Legacy

`deploy/cloud-worker/` — прежний GCP путь. Не удалён, но **deprecated** после миграции.
