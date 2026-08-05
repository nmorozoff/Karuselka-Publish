# Publish Fixic — Cloud Agent

Fixic **обязателен** в конце каждого automation run, если был любой инцидент, частичный успех, странный отчёт в Макс или публикация не состоялась.

## Вход

- `publish-memory/pipeline-fix-queue.md` — `status: open`
- `publish-memory/output/worker-last-run.json`
- `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`
- `shared/queue-contract.md`

## Алгоритм

1. `python3 scripts/publish_incident.py --list-open`
2. Для каждого open INC:
   - Прочитать Error + Context + stage
   - Найти root cause (код, env, Airtable, Dropbox, Zernio, cron, notify)
   - Внести **минимальный** fix в `scripts/`, `deploy/cursor-automation/`, `shared/`
3. Проверки:
   - `python3 -m py_compile` на изменённых `.py`
   - `python3 scripts/materialize_cloud_env.py --check` если трогали env
4. Обновить INC в `pipeline-fix-queue.md`:
   - `status: fixed` + `fix_summary` + `files_changed`
   - или `status: needs-human` если нужен секрет/ручное действие в Cursor UI
5. Итог в Макс:
   ```bash
   python3 scripts/notify_max.py --text "🔧 Fixic: <краткий итог — что сломалось, что починено, что осталось>"
   ```

## Типовые фиксы

| Симптом | Действие |
|---------|----------|
| `not_attempted` в Макс при успехе | `scripts/lib/max_notify.py` — парсинг Zernio |
| Очередь не пуста, а «очередь пуста» | `queue_next_hint` / notify |
| Dropbox 409 / path | legacy path, `find_carousel_dropbox_folder` |
| Zernio media fetch failed | retry `--retry-failed`, проверить Dropbox shared links |
| Automation не в Runs | cron timezone UTC vs MSK, Enabled, repo/branch |
| Preflight secrets | `materialize_cloud_env.py`, Cursor Runtime Secrets scope |

## Запреты

- Не коммитить `*.env.local`
- Не удалять failed из state без диагностики
- Не генерировать слайды / Kie / caption
