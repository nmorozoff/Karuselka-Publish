#!/usr/bin/env bash
# Запуск воркера публикации (3×/день ≈ 11/17/21 MSK по cron).
# Production: deploy/cloud-worker/ (Cloud Scheduler).

set -euo pipefail
export PYTHONUNBUFFERED=1
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/scripts"
PAIR="${KARUSELKA_PUBLISH_PAIR:-pair1}"
exec python3 publish_worker.py --pair "$PAIR" --limit 1 "$@"
