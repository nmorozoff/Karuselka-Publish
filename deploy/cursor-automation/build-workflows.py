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
    # pair1
    ("pair1", "10:00", "0 7 * * *", "karuselka-publish-pair1-1000"),
    ("pair1", "17:00", "0 14 * * *", "karuselka-publish-pair1-1700"),
    ("pair1", "20:00", "0 17 * * *", "karuselka-publish-pair1-2000"),
    # pair2
    ("pair2", "11:00", "0 8 * * *", "karuselka-publish-pair2-1100"),
    ("pair2", "18:00", "0 15 * * *", "karuselka-publish-pair2-1800"),
    ("pair2", "21:00", "0 18 * * *", "karuselka-publish-pair2-2100"),
    # pair3
    ("pair3", "12:00", "0 9 * * *", "karuselka-publish-pair3-1200"),
    ("pair3", "19:00", "0 16 * * *", "karuselka-publish-pair3-1900"),
    ("pair3", "22:00", "0 19 * * *", "karuselka-publish-pair3-2200"),
]


def prompt(pair: str) -> str:
    return f"""Ты — Cloud Agent доставщик каруселей для проекта karuselka-publish (репозиторий nmorozoff/Karuselka-Publish).
Ты не генерируешь слайды, не пишешь caption и не вызываешь Kie/Grok.

Пара: **{pair}**. Лимит: 1 карусель.

Обязательно:
1. Прочитай `.cursor/karuselka-publish-handoff.md`
2. `python3 scripts/materialize_cloud_env.py --check`
3. Если preflight не проходит — `python3 scripts/notify_max.py --text "❌ Preflight {pair}: <ошибка>"` и stop.
4. `python3 scripts/publish_status.py --pair {pair}`
   - Если ready = 0 — `python3 scripts/notify_max.py --text "📭 Очередь {pair} пуста"` и stop.
5. `python3 scripts/publish_worker.py --pair {pair} --limit 1 --dry-run-first`
6. Прочитай `publish-memory/output/worker-last-run.json`.
   - Если `aborted: true` — отчёт в Макс с причиной и stop.
   - Если `status: error` — `python3 scripts/notify_max.py --result-file publish-memory/output/worker-last-run.json --pair {pair}` и stop.
7. При успехе воркер уже отправил отчёт в Макс. Опционально: `python3 scripts/publish_status.py --pair {pair}` и итог в Макс.

Контракт: `shared/queue-contract.md`."""


def build(pair: str, time_msk: str, cron: str, slug: str) -> dict:
    return {
        "name": f"Karuselka Publish {pair} {time_msk} MSK",
        "description": f"Автопубликация 1 карусели ({pair}) в {time_msk} MSK (cron UTC).",
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
