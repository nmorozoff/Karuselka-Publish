#!/usr/bin/env bash
# Пауза legacy GCP Cloud Scheduler (после включения Cursor Automations).

set -euo pipefail
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy

DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=/dev/null
source "$DIR/../cloud-worker/.env.deploy" 2>/dev/null || true

PROJECT_ID="${PROJECT_ID:-}"
SCHEDULER_LOCATION="${SCHEDULER_LOCATION:-europe-west1}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "Задайте PROJECT_ID в deploy/cloud-worker/.env.deploy" >&2
  exit 1
fi

if ! command -v gcloud >/dev/null 2>&1; then
  echo "gcloud не найден — пауза jobs вручную в GCP Console" >&2
  exit 1
fi

gcloud config set project "$PROJECT_ID" >/dev/null

JOBS=(
  karuselka-publish-pair1-1000
  karuselka-publish-pair1-1700
  karuselka-publish-pair1-2000
  karuselka-publish-pair2-1100
  karuselka-publish-pair2-1800
  karuselka-publish-pair2-2100
)

for id in "${JOBS[@]}"; do
  if gcloud scheduler jobs describe "$id" --location="$SCHEDULER_LOCATION" >/dev/null 2>&1; then
    echo "Pause: $id"
    gcloud scheduler jobs pause "$id" --location="$SCHEDULER_LOCATION"
  else
    echo "Skip (not found): $id"
  fi
done

echo ""
echo "GCP Scheduler paused. Cursor Automations — основной путь."
gcloud scheduler jobs list --location="$SCHEDULER_LOCATION" --filter="name:karuselka-publish" \
  --format="table(name,schedule,timeZone,state)"
