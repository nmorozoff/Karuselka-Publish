#!/usr/bin/env python3
"""Build Cursor Automation prefill JSON for scheduled publish jobs (3 pairs × 3 times)."""

from __future__ import annotations

import json
from pathlib import Path

REPO = "nmorozoff/Karuselka-Publish"
BRANCH = "main"
OUT = Path(__file__).resolve().parent / "workflows"

# Cron UTC = MSK − 3
JOBS = [
    ("pair1", "10:00", "0 7 * * *", "karuselka-publish-pair1-1000"),
    ("pair1", "17:00", "0 14 * * *", "karuselka-publish-pair1-1700"),
    ("pair1", "20:00", "0 17 * * *", "karuselka-publish-pair1-2000"),
    ("pair2", "11:00", "0 8 * * *", "karuselka-publish-pair2-1100"),
    ("pair2", "18:00", "0 15 * * *", "karuselka-publish-pair2-1800"),
    ("pair2", "21:00", "0 18 * * *", "karuselka-publish-pair2-2100"),
    ("pair3", "12:00", "0 9 * * *", "karuselka-publish-pair3-1200"),
    ("pair3", "19:00", "0 16 * * *", "karuselka-publish-pair3-1900"),
    ("pair3", "22:00", "0 19 * * *", "karuselka-publish-pair3-2200"),
]


def prompt(pair: str) -> str:
    return f"""Ты — Cloud Agent доставщик каруселей (karuselka-publish, репозиторий nmorozoff/Karuselka-Publish).
Не генерируешь слайды, caption, Kie/Grok.

Пара: **{pair}**. Лимит: 1 карусель за run.

## Правило №1 — не сдаваться на первой ошибке

При любой проблеме: диагностика → retry (если уместно) → `publish_incident.py` → продолжай run → **Fixic в конце**.

Запрещено: увидел ошибку и сразу stop без инцидента и без Fixic.

## Фаза A — Preflight

1. Прочитай `.cursor/karuselka-publish-handoff.md` и `deploy/cursor-automation/CLOUD_AGENT_PROMPT.md`
2. `python3 scripts/materialize_cloud_env.py --check`
   - fail → `python3 scripts/materialize_cloud_env.py` → повтори check (1 раз)
   - снова fail → `python3 scripts/publish_incident.py --pair {pair} --stage preflight --error "<текст>"` → иди в Fixic

## Фаза B — Очередь

3. `WORKER_STATE_BACKEND=dropbox WORKER_STATE_DROPBOX_PATH=/Content_Plan/.karuselka/worker-state.json python3 scripts/publish_status.py --pair {pair}`
4. ready=0 и failed>0 → прочитай failed в worker-state, попробуй `python3 scripts/publish_worker.py --pair {pair} --retry-failed --limit 1 --dry-run-first` (1 раз)
5. ready=0 и failed=0 → `python3 scripts/notify_max.py --text "📭 Очередь {pair} пуста"` → **Fixic** (проверь cron/automation) → stop

## Фаза C — Публикация

6. `WORKER_STATE_BACKEND=dropbox WORKER_STATE_DROPBOX_PATH=/Content_Plan/.karuselka/worker-state.json python3 scripts/publish_worker.py --pair {pair} --limit 1 --dry-run-first`
7. Прочитай `publish-memory/output/worker-last-run.json`
   - `aborted: true` → incident + диагностика (Dropbox path, слайды, secrets) → retry dry-run на **следующей** ready карусели если есть
   - `status: error` → `python3 scripts/publish_incident.py --pair {pair} --stage publish --error "<текст>" --carousel "<name>"` → `notify_max.py --result-file ...` → retry failed или следующую ready (макс 1 retry)
   - success → проверь отчёт Макс: Instagram/TikTok не должны быть `not_attempted` при реальной публикации; иначе incident stage=notify

## Фаза D — Fixic (обязательно при любом инциденте)

8. Прочитай `deploy/cursor-automation/PUBLISH_FIXIC.md`
9. `python3 scripts/publish_incident.py --list-open`
10. Почини код/скрипты/промпты в репозитории (минимальный diff), `py_compile` изменённых файлов
11. Закрой INC (`status: fixed`) в `publish-memory/pipeline-fix-queue.md` или `needs-human`
12. Итог в Макс: `python3 scripts/notify_max.py --text "🔧 Fixic {pair}: ..."`

Контракт: `shared/queue-contract.md`."""


def build(pair: str, time_msk: str, cron: str, slug: str) -> dict:
    return {
        "name": f"Karuselka Publish {pair} {time_msk} MSK",
        "description": f"Автопубликация 1 карусели ({pair}) в {time_msk} MSK (cron UTC). Resilient + Fixic.",
        "workflow": {
            "triggers": [{"cron": {"cron": cron}}],
            "actions": [],
            "prompts": [prompt(pair)],
            "model": "",
            "gitConfig": {"repo": REPO, "branch": BRANCH},
            "memoryEnabled": False,
            "agentOptions": {"skipInstall": False},
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for pair, time_msk, cron, slug in JOBS:
        data = build(pair, time_msk, cron, slug)
        path = OUT / f"{slug}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index.append({"id": slug, "pair": pair, "time_msk": time_msk, "cron": cron, "file": path.name})
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"written": len(index), "dir": str(OUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
