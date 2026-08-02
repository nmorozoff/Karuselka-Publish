#!/usr/bin/env bash
# Локальный cron (резерв): pair1 @ 10/17/20, pair2 @ 11/18/21 MSK.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKER1="$ROOT/scripts/run_publish_worker.sh --pair pair1"
WORKER2="$ROOT/scripts/run_publish_worker.sh --pair pair2"
LOG="$ROOT/publish-memory/output/worker-cron.log"
MARKER_BEGIN="# KARUSELKA_PUBLISH_CRON_BEGIN"
MARKER_END="# KARUSELKA_PUBLISH_CRON_END"

chmod +x "$ROOT/scripts/run_publish_worker.sh"
mkdir -p "$(dirname "$LOG")"

CRON_BLOCK=$(cat <<EOF
$MARKER_BEGIN
0 10 * * * /bin/bash -lc '$WORKER1 >> $LOG 2>&1'
0 17 * * * /bin/bash -lc '$WORKER1 >> $LOG 2>&1'
0 20 * * * /bin/bash -lc '$WORKER1 >> $LOG 2>&1'
0 11 * * * /bin/bash -lc '$WORKER2 >> $LOG 2>&1'
0 18 * * * /bin/bash -lc '$WORKER2 >> $LOG 2>&1'
0 21 * * * /bin/bash -lc '$WORKER2 >> $LOG 2>&1'
$MARKER_END
EOF
)

if [[ "${1:-}" == "--uninstall" ]]; then
  if crontab -l >/dev/null 2>&1; then
    crontab -l | awk -v b="$MARKER_BEGIN" -v e="$MARKER_END" '
      $0 == b { skip=1; next }
      $0 == e { skip=0; next }
      !skip { print }
    ' | crontab -
    echo "Удалено: расписание karuselka-publish из crontab."
  else
    echo "Crontab пуст — нечего удалять."
  fi
  exit 0
fi

EXISTING=""
if crontab -l >/dev/null 2>&1; then
  EXISTING="$(crontab -l | awk -v b="$MARKER_BEGIN" -v e="$MARKER_END" '
    $0 == b { skip=1; next }
    $0 == e { skip=0; next }
    !skip { print }
  ')"
fi

{
  if [[ -n "$EXISTING" ]]; then
    printf '%s\n' "$EXISTING"
  fi
  printf '%s\n' "$CRON_BLOCK"
} | crontab -

echo "Cron установлен (Mac должен быть включён)."
echo "  pair1: 10:00, 17:00, 20:00"
echo "  pair2: 11:00, 18:00, 21:00"
echo "Production: ./deploy/cloud-worker/setup-cloud-automation.sh"
echo "Лог: $LOG"
