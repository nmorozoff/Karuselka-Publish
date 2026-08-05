# Karuselka Publish — Director Handoff

> Полный контекст от предыдущей сессии в проекте КАРУСЕЛЬКА. Читать перед продолжением.

## 1. Архитектура

- **Фабрика:** `Karuselka-emdr` (репо `nmorozoff/Karuselka-emdr`, локально `/Users/natala/Documents/Проекты СURSOR/КАРУСЕЛЬКА/`).
- **Доставка:** `karuselka-publish` (репо `nmorozoff/Karuselka-Publish`, локально `/Users/natala/Documents/Проекты СURSOR/КАРУСЕЛЬКА-publish/`).
- Фабрика генерирует карусели и пишет в `Dropbox /Content_Plan/Pair{N}/{Name}/` + Airtable.
- Publish читает Airtable, забирает файлы, публикует в Instagram/TikTok через Zernio API.

## 2. Account Pairs (обновлено 2026-08-05)

| Pair | Instagram | TikTok | Style | Zernio IG ID | Zernio TT ID | API keys | Dropbox | Airtable table | Times MSK |
|------|-----------|--------|-------|--------------|--------------|----------|---------|----------------|-----------|
| **pair1** | pair1_instagram | pair1_tiktok | Excalibur sketch pink | `6a3b7aae9d9472faaecf24f5` | `6a37de5c5f7d1751ab2d389e` | `ZERNIO_API_KEY` | `/Content_Plan/Pair1` | `tblFWCmLCXLrOdKut` | 10:00, 17:00, 20:00 |
| **pair2** | @natalia_morozova_psy | @natalyamorozovapsy | Minimalism / BORDO | `6a6a3ccadf17280d93d6828d` | `6a6a3bf5df17280d93d66feb` | `ZERNIO_PAIR2_API_KEY` | `/Content_Plan/Pair2` | `tbl2zotNwOmWLSTyC` | 11:00, 18:00, 21:00 |
| **pair3** | @morozova_natalia_psy | @psy_morozova_ | Sketch neon / BORDO | `6a70613ddf17280d93060b44` | `6a7063ecdf17280d9306f184` | `ZERNIO_PAIR3_INSTAGRAM_API_KEY`, `ZERNIO_PAIR3_TIKTOK_API_KEY` | `/Content_Plan/Pair3` | `tblNv5eMi1BXbu4Tq` | 12:00, 19:00, 22:00 |

Файл: `publish-memory/accounts-pairs.json` (version 2) — уже обновлён реальными ID.

## 3. Что уже работает

- Pair3 dry-run прошёл успешно (2026-08-05 12:22 UTC).
- Pair3 публикация прошла успешно: `crsl_20260803_1749_244` опубликован в Instagram + TikTok (2026-08-05 12:24 UTC).
- Cleanup включён: Airtable + Dropbox папка удаляются после успеха.
- Cloud Agent Prompt: `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`.

## 4. Что нужно сделать дальше (задача пользователя)

**Создать 9 Cursor Automations** (3 пары × 3 времени) в репозитории `nmorozoff/Karuselka-Publish`.

### Требования к automation

- **Trigger:** cron (UTC = MSK − 3).
- **Repo:** `nmorozoff/Karuselka-Publish` / `main`.
- **Compute:** Cloud Agent (Cursor Dashboard).
- **Command:** `python3 scripts/publish_worker.py --pair {pair} --limit 1`.
- **Always:** материализовать env + preflight + dry-run (см. CLOUD_AGENT_PROMPT.md).
- **Secrets:** Cursor Dashboard Runtime Secrets (`CLOUD-SECRETS.md`).
- **Notify:** Макс-бот после успеха/ошибки.

### Расписание (UTC cron)

| Pair | MSK | UTC | Cron |
|------|-----|-----|------|
| pair1 | 10:00 | 07:00 | `0 7 * * *` |
| pair1 | 17:00 | 14:00 | `0 14 * * *` |
| pair1 | 20:00 | 20:00 | `0 17 * * *` |
| pair2 | 11:00 | 08:00 | `0 8 * * *` |
| pair2 | 18:00 | 15:00 | `0 15 * * *` |
| pair2 | 21:00 | 18:00 | `0 18 * * *` |
| pair3 | 12:00 | 09:00 | `0 9 * * *` |
| pair3 | 19:00 | 16:00 | `0 16 * * *` |
| pair3 | 22:00 | 19:00 | `0 19 * * *` |

### Naming convention

`karuselka-publish-{pair}-{utc-hour}00`

Например:
- `karuselka-publish-pair1-0700`
- `karuselka-publish-pair2-1500`
- `karuselka-publish-pair3-1900`

## 5. Secrets checklist (Cursor Dashboard)

- `AIRTABLE_ACCESS_TOKEN`
- `DROPBOX_ACCESS_TOKEN` (или `DROPBOX_APP_KEY` + `DROPBOX_APP_SECRET` + `DROPBOX_REFRESH_TOKEN`)
- `ZERNIO_API_KEY` (pair1)
- `ZERNIO_PAIR2_API_KEY` (pair2)
- `ZERNIO_PAIR3_INSTAGRAM_API_KEY` (pair3 IG)
- `ZERNIO_PAIR3_TIKTOK_API_KEY` (pair3 TT)
- `MAX_BOT_TOKEN`
- `MAX_NOTIFY_CHAT_ID` (или `MAX_PREVIEW_CHAT_ID`)

## 6. Important Notes

- `PUBLISH_MODE=grok_hook` (default).
- `EXPECTED_IMAGE_SLIDES=6` (default). Если появится 9-слайдный формат — обновить env.
- 2 failed в pair1 (`worker-state.json`) — можно retry через `publish_worker.py --pair pair1 --retry-failed`.
- Publish-воркер не запускает публикацию без dry-run в cloud agent context (см. prompt).
- Не коммитить `*.env.local`.

## 7. Next Action

Открыть Automations editor и создать 9 шедулеров по спецификации выше. Использовать `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md` как prompt для каждого Cloud Agent run.
