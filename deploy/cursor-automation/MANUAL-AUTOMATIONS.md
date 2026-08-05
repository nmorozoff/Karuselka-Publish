# Ручная настройка 9 Cursor Automations

Если `open_automation` не открыл редактор — создай вручную.

## Общие настройки (для всех 9)

| Поле | Значение |
|------|----------|
| **Repository** | `nmorozoff/Karuselka-Publish` |
| **Branch** | `main` |
| **Compute** | Cloud Agent |
| **Trigger** | Schedule (cron) |
| **Memory** | Off |

Cursor → **Automations** → **New automation**

---

## Расписание

Если UI просит **UTC** (MSK − 3):

| Name | Pair | MSK | Cron UTC |
|------|------|-----|----------|
| Karuselka Publish pair1 10:00 MSK | pair1 | 10:00 | `0 7 * * *` |
| Karuselka Publish pair1 17:00 MSK | pair1 | 17:00 | `0 14 * * *` |
| Karuselka Publish pair1 20:00 MSK | pair1 | 20:00 | `0 17 * * *` |
| Karuselka Publish pair2 11:00 MSK | pair2 | 11:00 | `0 8 * * *` |
| Karuselka Publish pair2 18:00 MSK | pair2 | 18:00 | `0 15 * * *` |
| Karuselka Publish pair2 21:00 MSK | pair2 | 21:00 | `0 18 * * *` |
| Karuselka Publish pair3 12:00 MSK | pair3 | 12:00 | `0 9 * * *` |
| Karuselka Publish pair3 19:00 MSK | pair3 | 19:00 | `0 16 * * *` |
| Karuselka Publish pair3 22:00 MSK | pair3 | 22:00 | `0 19 * * *` |

Если UI позволяет **Europe/Moscow** — ставь время MSK напрямую (10:00, 17:00, …).

---

## Agents Instruction — шаблон

Замени `{PAIR}` на `pair1`, `pair2` или `pair3`.

```
Ты — Cloud Agent доставщик каруселей для проекта karuselka-publish (репозиторий nmorozoff/Karuselka-Publish).
Ты не генерируешь слайды, не пишешь caption и не вызываешь Kie/Grok.

Пара: {PAIR}. Лимит: 1 карусель.

Обязательно:
1. Прочитай `.cursor/karuselka-publish-handoff.md` и `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`
2. `python3 scripts/materialize_cloud_env.py --check`
3. Если preflight не проходит — `python3 scripts/notify_max.py --text "❌ Preflight {PAIR}: <ошибка>"` и stop.
4. `python3 scripts/publish_status.py --pair {PAIR}`
   - Если ready = 0 — `python3 scripts/notify_max.py --text "📭 Очередь {PAIR} пуста"` и stop.
5. `python3 scripts/publish_worker.py --pair {PAIR} --limit 1 --dry-run-first`
6. Прочитай `publish-memory/output/worker-last-run.json`.
   - Если `aborted: true` — отчёт в Макс с причиной и stop.
   - Если `status: error` — `python3 scripts/notify_max.py --result-file publish-memory/output/worker-last-run.json --pair {PAIR}` и stop.
7. При успехе воркер уже отправил отчёт в Макс. Опционально: `python3 scripts/publish_status.py --pair {PAIR}`.

Контракт: `shared/queue-contract.md`.
Не коммить *.env.local. Не генерировать контент.
```

---

## Готовые инструкции (copy-paste)

### pair1 — 10:00 / 17:00 / 20:00 MSK

Три automation с **одинаковым** текстом ниже, разный только cron и name.

```
Ты — Cloud Agent доставщик каруселей для проекта karuselka-publish (репозиторий nmorozoff/Karuselka-Publish).
Ты не генерируешь слайды, не пишешь caption и не вызываешь Kie/Grok.

Пара: pair1. Лимит: 1 карусель.

Обязательно:
1. Прочитай `.cursor/karuselka-publish-handoff.md` и `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`
2. `python3 scripts/materialize_cloud_env.py --check`
3. Если preflight не проходит — `python3 scripts/notify_max.py --text "❌ Preflight pair1: <ошибка>"` и stop.
4. `python3 scripts/publish_status.py --pair pair1`
   - Если ready = 0 — `python3 scripts/notify_max.py --text "📭 Очередь pair1 пуста"` и stop.
5. `python3 scripts/publish_worker.py --pair pair1 --limit 1 --dry-run-first`
6. Прочитай `publish-memory/output/worker-last-run.json`.
   - Если `aborted: true` — отчёт в Макс с причиной и stop.
   - Если `status: error` — `python3 scripts/notify_max.py --result-file publish-memory/output/worker-last-run.json --pair pair1` и stop.
7. При успехе воркер уже отправил отчёт в Макс.

Контракт: `shared/queue-contract.md`.
```

### pair2 — 11:00 / 18:00 / 21:00 MSK

```
Ты — Cloud Agent доставщик каруселей для проекта karuselka-publish (репозиторий nmorozoff/Karuselka-Publish).
Ты не генерируешь слайды, не пишешь caption и не вызываешь Kie/Grok.

Пара: pair2. Лимит: 1 карусель.

Обязательно:
1. Прочитай `.cursor/karuselka-publish-handoff.md` и `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`
2. `python3 scripts/materialize_cloud_env.py --check`
3. Если preflight не проходит — `python3 scripts/notify_max.py --text "❌ Preflight pair2: <ошибка>"` и stop.
4. `python3 scripts/publish_status.py --pair pair2`
   - Если ready = 0 — `python3 scripts/notify_max.py --text "📭 Очередь pair2 пуста"` и stop.
5. `python3 scripts/publish_worker.py --pair pair2 --limit 1 --dry-run-first`
6. Прочитай `publish-memory/output/worker-last-run.json`.
   - Если `aborted: true` — отчёт в Макс с причиной и stop.
   - Если `status: error` — `python3 scripts/notify_max.py --result-file publish-memory/output/worker-last-run.json --pair pair2` и stop.
7. При успехе воркер уже отправил отчёт в Макс.

Контракт: `shared/queue-contract.md`.
```

### pair3 — 12:00 / 19:00 / 22:00 MSK

```
Ты — Cloud Agent доставщик каруселей для проекта karuselka-publish (репозиторий nmorozoff/Karuselka-Publish).
Ты не генерируешь слайды, не пишешь caption и не вызываешь Kie/Grok.

Пара: pair3. Лимит: 1 карусель.

Обязательно:
1. Прочитай `.cursor/karuselka-publish-handoff.md` и `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`
2. `python3 scripts/materialize_cloud_env.py --check`
3. Если preflight не проходит — `python3 scripts/notify_max.py --text "❌ Preflight pair3: <ошибка>"` и stop.
4. `python3 scripts/publish_status.py --pair pair3`
   - Если ready = 0 — `python3 scripts/notify_max.py --text "📭 Очередь pair3 пуста"` и stop.
5. `python3 scripts/publish_worker.py --pair pair3 --limit 1 --dry-run-first`
6. Прочитай `publish-memory/output/worker-last-run.json`.
   - Если `aborted: true` — отчёт в Макс с причиной и stop.
   - Если `status: error` — `python3 scripts/notify_max.py --result-file publish-memory/output/worker-last-run.json --pair pair3` и stop.
7. При успехе воркер уже отправил отчёт в Макс.

Контракт: `shared/queue-contract.md`.
```

---

## После создания

1. **Run once** на одной automation (например pair3 12:00) — проверить Макс-отчёт.
2. Убедиться, что все 9 в статусе **Enabled**.
3. GCP Scheduler уже paused — не включать обратно.

## Тест вручную (без automation)

```bash
python3 scripts/materialize_cloud_env.py --check
python3 scripts/publish_worker.py --pair pair3 --limit 1 --dry-run-first
```
