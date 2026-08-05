#!/usr/bin/env bash
# Собрать app/ для Docker.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$(cd "$(dirname "$0")" && pwd)/app"

rm -rf "$OUT"
mkdir -p "$OUT/lib" "$OUT/config"

cp "$ROOT/deploy/cloud-worker/main.py" "$OUT/main.py"
cp "$ROOT/scripts/lib/publish_engine.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/publish_cleanup.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/http_client.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/worker_state.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/publish_config.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/dropbox_client.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/airtable_client.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/max_http.py" "$OUT/lib/"
cp "$ROOT/scripts/lib/max_notify.py" "$OUT/lib/"
cp "$ROOT/publish-memory/accounts-pairs.json" "$OUT/config/accounts-pairs.json"

echo "Bundle ready: $OUT"
