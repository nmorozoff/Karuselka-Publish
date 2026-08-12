#!/usr/bin/env python3
"""Build automation artifacts: plain .txt instructions + optional workflow JSON."""

from __future__ import annotations

import json
from pathlib import Path

REPO = "nmorozoff/Karuselka-Publish"
BRANCH = "main"
ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "workflows"
OUT_TXT = ROOT / "instructions"

# Cron UTC = MSK - 3
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

ENV_PREFIX = (
    "WORKER_STATE_BACKEND=dropbox "
    "WORKER_STATE_DROPBOX_PATH=/Content_Plan/.karuselka/worker-state.json"
)


def agent_instruction(pair: str) -> str:
    return f"""Ты Cloud Agent доставщик каруселей karuselka-publish.
Репозиторий: nmorozoff/Karuselka-Publish
Не генерируешь слайды, caption, Kie, Grok.

Пара: {pair}
Лимит: 1 карусель за run.

ПРАВИЛО: при ошибке не останавливайся сразу.
Диагностика, retry если уместно, publish_incident.py, продолжай run, Fixic в конце.
Запрещено: увидел ошибку и stop без инцидента и без Fixic.

ФАЗА A PREFLIGHT
1. Прочитай .cursor/karuselka-publish-handoff.md
2. Прочитай deploy/cursor-automation/CLOUD_AGENT_PROMPT.md
3. python3 scripts/materialize_cloud_env.py --check
   если fail: python3 scripts/materialize_cloud_env.py и повтори check один раз
   если снова fail: python3 scripts/publish_incident.py --pair {pair} --stage preflight --error "текст ошибки"
   затем Fixic

ФАЗА B ОЧЕРЕДЬ
4. {ENV_PREFIX} python3 scripts/publish_status.py --pair {pair}
5. если ready=0 и failed больше 0:
   прочитай failed в worker-state
   попробуй один раз:
   {ENV_PREFIX} python3 scripts/publish_worker.py --pair {pair} --retry-failed --limit 1 --dry-run-first
6. если ready=0 и failed=0:
   python3 scripts/notify_max.py --text "Очередь {pair} пуста"
   Fixic проверь cron и automation
   stop

ФАЗА C ПУБЛИКАЦИЯ
7. {ENV_PREFIX} python3 scripts/publish_worker.py --pair {pair} --limit 1 --dry-run-first
8. Прочитай publish-memory/output/worker-last-run.json
   если aborted true: incident, диагностика Dropbox path и слайды, retry dry-run на следующей ready карусели если есть
   если status error:
     python3 scripts/publish_incident.py --pair {pair} --stage publish --error "текст" --carousel "имя"
     python3 scripts/notify_max.py --result-file publish-memory/output/worker-last-run.json --pair {pair}
     один retry failed или следующей ready
   если success:
     проверь отчет Макс
     Instagram и TikTok не должны быть not_attempted при реальной публикации
     иначе incident stage notify

ФАЗА D FIXIC обязательно при любом инциденте
9. Прочитай deploy/cursor-automation/PUBLISH_FIXIC.md
10. python3 scripts/publish_incident.py --list-open
11. Почини код и скрипты в репозитории минимальным diff
12. py_compile на измененных py файлах
13. Закрой INC в publish-memory/pipeline-fix-queue.md status fixed или needs-human
14. Итог в Макс:
    python3 scripts/notify_max.py --text "Fixic {pair}: краткий итог"

Контракт: shared/queue-contract.md
"""


def load_instruction(pair: str) -> str:
    """Берёт готовый промпт из instructions/pairN.txt (источник правды)."""
    path = OUT_TXT / f"{pair}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip() + "\n"
    return agent_instruction(pair)


def schedule_lines() -> str:
    lines = [
        "Karuselka Publish — расписание automations",
        "",
        "Общие настройки для всех 9:",
        "Repository: nmorozoff/Karuselka-Publish",
        "Branch: main",
        "Compute: Cloud Agent",
        "Trigger: Schedule",
        "Memory: Off",
        "",
        "Agents Instruction: скопируй целиком файл instructions/pairN.txt (см. ниже)",
        "",
        "Если cron в UTC (MSK минус 3 часа):",
        "",
    ]
    for pair, time_msk, cron, slug in JOBS:
        lines.append(f"{slug}  pair={pair}  MSK={time_msk}  cron_UTC={cron}")
    lines.extend(
        [
            "",
            "Если timezone Europe/Moscow — ставь время MSK напрямую.",
            "",
            "Файлы инструкций агента (copy-paste в Agents Instruction):",
            "instructions/pair1.txt  — для всех трех слотов pair1",
            "instructions/pair2.txt  — для всех трех слотов pair2",
            "instructions/pair3.txt  — для всех трех слотов pair3",
            "",
            "Пересобрать: python3 deploy/cursor-automation/build-workflows.py",
        ]
    )
    return "\n".join(lines) + "\n"


def build_json(pair: str, time_msk: str, cron: str, slug: str) -> dict:
    return {
        "name": f"Karuselka Publish {pair} {time_msk} MSK",
        "description": f"Автопубликация 1 карусели ({pair}) в {time_msk} MSK (cron UTC).",
        "workflow": {
            "triggers": [{"cron": {"cron": cron}}],
            "actions": [],
            "prompts": [load_instruction(pair)],
            "model": "",
            "gitConfig": {"repo": REPO, "branch": BRANCH},
            "memoryEnabled": False,
            "agentOptions": {"skipInstall": False},
        },
    }


def main() -> None:
    OUT_JSON.mkdir(parents=True, exist_ok=True)

    # instructions/pairN.txt — редактируются вручную; JSON собирается из них
    (OUT_TXT / "SCHEDULE.txt").write_text(schedule_lines(), encoding="utf-8")

    index = []
    for pair, time_msk, cron, slug in JOBS:
        data = build_json(pair, time_msk, cron, slug)
        path = OUT_JSON / f"{slug}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index.append(
            {
                "id": slug,
                "pair": pair,
                "time_msk": time_msk,
                "cron": cron,
                "instruction_file": f"instructions/{pair}.txt",
                "json_file": path.name,
            }
        )
    (OUT_JSON / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "instructions": str(OUT_TXT),
                "workflows": str(OUT_JSON),
                "pairs": 3,
                "jobs": len(JOBS),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
