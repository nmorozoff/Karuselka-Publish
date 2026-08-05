# Cursor Cloud Secrets — Karuselka Publish

Добавить в [Cursor → Cloud Agents → Runtime Secrets](https://cursor.com/dashboard/cloud-agents).

Список имён: `cloud-secrets-checklist.txt`

## Обязательные

| Переменная | Назначение |
|------------|------------|
| `AIRTABLE_ACCESS_TOKEN` | Очередь публикации |
| `DROPBOX_APP_KEY` | OAuth refresh |
| `DROPBOX_APP_SECRET` | OAuth refresh |
| `DROPBOX_REFRESH_TOKEN` | Медиа + worker-state |
| `ZERNIO_API_KEY` | pair1 IG + TikTok |
| `ZERNIO_PAIR2_API_KEY` | pair2 (если отдельный ключ) |
| `ZERNIO_INSTAGRAM_ACCOUNT_ID` | fallback для pair1 |
| `ZERNIO_TIKTOK_ACCOUNT_ID` | fallback для pair1 |
| `MAX_BOT_TOKEN` | Отчёты в Макс |
| `MAX_PREVIEW_CHAT_ID` | Личка с ботом (из «Посты EMDR») |

## Рекомендуемые defaults (можно в Secrets)

| Переменная | Значение |
|------------|----------|
| `WORKER_STATE_BACKEND` | `dropbox` |
| `WORKER_STATE_DROPBOX_PATH` | `/Content_Plan/.karuselka/worker-state.json` |
| `PUBLISH_MODE` | `grok_hook` |
| `EXPECTED_IMAGE_SLIDES` | `6` |
| `MAX_API_INSECURE_TLS` | `true` |

## Не нужны в Cursor Cloud

| Переменная | Почему |
|------------|--------|
| `WORKER_API_KEY` | Только для legacy GCP Cloud Run |
| `TELEGRAM_*` | Заменено на Макс |
| `CLOUD_RUN_API_KEY` | Legacy render path |

## Проверка

```bash
python3 scripts/materialize_cloud_env.py --check
python3 scripts/cloud_preflight.py
```

Exit `0` = готово к scheduled publish.

## Источник значений

Локальные symlink:

```bash
cd publish-memory
ln -sf ../../КАРУСЕЛЬКА/carusel-memory/{airtable,dropbox,zernio}.env.local .
ln -sf ../../Посты\ EMDR/posts-emdr-memory/max.env.local max.env.local
```

Скопировать значения ключей в Cursor Dashboard (не коммитить).
