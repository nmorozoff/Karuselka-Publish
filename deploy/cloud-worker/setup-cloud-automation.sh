#!/usr/bin/env bash
# Полный деплой облачной автоматизации: env → Cloud Run → Scheduler (6 jobs).

set -euo pipefail
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy NO_PROXY no_proxy

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "==> 1/3 prepare_cloud_env"
chmod +x scripts/prepare_cloud_env.sh deploy/cloud-worker/*.sh
./scripts/prepare_cloud_env.sh

echo ""
echo "==> 2/3 deploy Cloud Run worker"
./deploy/cloud-worker/deploy.sh

echo ""
echo "==> 3/3 setup Cloud Scheduler (pair1 + pair2)"
./deploy/cloud-worker/setup-scheduler.sh

echo ""
echo "Готово. Проверка health:"
WORKER_URL="$(gcloud run services describe karuselka-publish-worker --region europe-west1 --format='value(status.url)' 2>/dev/null || true)"
if [[ -n "$WORKER_URL" ]]; then
  curl -sS "${WORKER_URL}/health" || true
  echo ""
fi
