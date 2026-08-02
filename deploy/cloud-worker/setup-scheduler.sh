#!/usr/bin/env bash
# Cloud Scheduler — 6 jobs MSK:
#   pair1: 10:00, 17:00, 20:00
#   pair2: 11:00, 18:00, 21:00

set -euo pipefail
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy NO_PROXY no_proxy

DIR="$(cd "$(dirname "$0")" && pwd)"

# shellcheck source=/dev/null
source "$DIR/.env.deploy" 2>/dev/null || true

PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-europe-west1}"
SERVICE_NAME="${SERVICE_NAME:-karuselka-publish-worker}"
WORKER_URL="${WORKER_URL:-}"
WORKER_API_KEY="${WORKER_API_KEY:-}"
SCHEDULER_LOCATION="${SCHEDULER_LOCATION:-europe-west1}"

if [[ -z "$PROJECT_ID" || -z "$WORKER_API_KEY" ]]; then
  echo "Нужны PROJECT_ID и WORKER_API_KEY (deploy/cloud-worker/.env.deploy)" >&2
  exit 1
fi

if [[ -z "$WORKER_URL" ]]; then
  WORKER_URL="$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format='value(status.url)' 2>/dev/null || true)"
fi
if [[ -z "$WORKER_URL" ]]; then
  echo "Задайте WORKER_URL или задеплойте: ./deploy/cloud-worker/deploy.sh" >&2
  exit 1
fi

gcloud config set project "$PROJECT_ID" >/dev/null
gcloud services enable cloudscheduler.googleapis.com run.googleapis.com >/dev/null 2>&1 || true

# Удалить legacy jobs (только pair1 @ 11/17/21)
for legacy in karuselka-publish-1100 karuselka-publish-1700 karuselka-publish-2100; do
  if gcloud scheduler jobs describe "$legacy" --location="$SCHEDULER_LOCATION" >/dev/null 2>&1; then
    echo "Удаляю legacy job: $legacy"
    gcloud scheduler jobs delete "$legacy" --location="$SCHEDULER_LOCATION" --quiet
  fi
done

create_job() {
  local id="$1"
  local schedule="$2"
  local pair="$3"
  local desc="$4"
  local uri="${WORKER_URL}/run?pair=${pair}&limit=1"

  if gcloud scheduler jobs describe "$id" --location="$SCHEDULER_LOCATION" >/dev/null 2>&1; then
    gcloud scheduler jobs update http "$id" \
      --location="$SCHEDULER_LOCATION" \
      --schedule="$schedule" \
      --time-zone="Europe/Moscow" \
      --uri="$uri" \
      --http-method=POST \
      --headers="X-Worker-Key=${WORKER_API_KEY}" \
      --description="$desc"
  else
    gcloud scheduler jobs create http "$id" \
      --location="$SCHEDULER_LOCATION" \
      --schedule="$schedule" \
      --time-zone="Europe/Moscow" \
      --uri="$uri" \
      --http-method=POST \
      --headers="X-Worker-Key=${WORKER_API_KEY}" \
      --description="$desc"
  fi
}

# pair1 — 10:00, 17:00, 20:00 MSK
create_job "karuselka-publish-pair1-1000" "0 10 * * *" "pair1" "Karuselka pair1 publish 10:00 MSK"
create_job "karuselka-publish-pair1-1700" "0 17 * * *" "pair1" "Karuselka pair1 publish 17:00 MSK"
create_job "karuselka-publish-pair1-2000" "0 20 * * *" "pair1" "Karuselka pair1 publish 20:00 MSK"

# pair2 — 11:00, 18:00, 21:00 MSK
create_job "karuselka-publish-pair2-1100" "0 11 * * *" "pair2" "Karuselka pair2 publish 11:00 MSK"
create_job "karuselka-publish-pair2-1800" "0 18 * * *" "pair2" "Karuselka pair2 publish 18:00 MSK"
create_job "karuselka-publish-pair2-2100" "0 21 * * *" "pair2" "Karuselka pair2 publish 21:00 MSK"

echo ""
echo "Scheduler OK (Europe/Moscow):"
echo "  pair1 → 10:00, 17:00, 20:00"
echo "  pair2 → 11:00, 18:00, 21:00"
echo "Target: ${WORKER_URL}/run"
gcloud scheduler jobs list --location="$SCHEDULER_LOCATION" --filter="name:karuselka-publish" --format="table(name,schedule,timeZone,state)"
