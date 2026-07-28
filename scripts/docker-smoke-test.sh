#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

BACKEND_IMAGE="sentiment-backend-smoketest"
FRONTEND_IMAGE="sentiment-frontend-smoketest"
BACKEND_CONTAINER="sentiment-backend-smoketest-run"
FRONTEND_CONTAINER="sentiment-frontend-smoketest-run"
BACKEND_PORT="18000"
FRONTEND_PORT="13000"

DATABASE_URL="${SMOKE_TEST_DATABASE_URL:?SMOKE_TEST_DATABASE_URL must be set to a reachable SQL Server instance}"
JWT_SECRET="${SMOKE_TEST_JWT_SECRET:-smoke-test-jwt-secret-at-least-32-characters-long}"

cleanup() {
  docker rm -f "$BACKEND_CONTAINER" "$FRONTEND_CONTAINER" > /dev/null 2>&1 || true
}
trap cleanup EXIT

# In CI these images are already built by dedicated, individually-timed
# "Build ... image" steps (see .github/workflows/ci.yml) so this script only
# has to run/verify them. Building here too keeps the script usable standalone
# for local smoke testing without needing to remember separate build commands.
if ! docker image inspect "$BACKEND_IMAGE" > /dev/null 2>&1; then
  echo "== Building backend image =="
  docker build --progress=plain -t "$BACKEND_IMAGE" "$ROOT_DIR/backend"
fi

if ! docker image inspect "$FRONTEND_IMAGE" > /dev/null 2>&1; then
  echo "== Building frontend image =="
  docker build --progress=plain -t "$FRONTEND_IMAGE" \
    --build-arg NEXT_PUBLIC_API_URL="http://localhost:${BACKEND_PORT}" \
    "$ROOT_DIR/frontend"
fi

echo "== Starting backend container =="
docker run -d --name "$BACKEND_CONTAINER" -p "${BACKEND_PORT}:8000" \
  --add-host=host.docker.internal:host-gateway \
  -v sentiment-smoketest-onnx-models:/app/onnx_models \
  -e database_url="$DATABASE_URL" \
  -e jwt_secret_key="$JWT_SECRET" \
  -e environment="development" \
  -e cors_origins="http://localhost:3000" \
  "$BACKEND_IMAGE"

echo "== Waiting for backend health check =="
# curl's own retry loop instead of a hand-rolled sleep loop: bounded by
# --retry-max-time regardless of --retry count, so this fails fast instead of
# hanging if the backend never comes up, and each individual attempt is capped
# by --max-time so one slow/stuck request can't eat the whole budget.
if ! curl -sf \
    --retry 60 --retry-delay 3 --retry-all-errors --retry-connrefused \
    --retry-max-time 180 --max-time 5 \
    -o /dev/null "http://localhost:${BACKEND_PORT}/health"; then
  echo "Backend did not become healthy within 180s. Logs:"
  docker logs "$BACKEND_CONTAINER" || true
  exit 1
fi

health_body=$(curl -sf --max-time 5 "http://localhost:${BACKEND_PORT}/health")
echo "Backend health response: $health_body"
echo "$health_body" | grep -q '"database":"ok"' || { echo "Database check did not report ok"; exit 1; }
echo "$health_body" | grep -q '"models":"ok"' || { echo "Model check did not report ok"; exit 1; }

echo "== Verifying security headers are present =="
headers=$(curl -sf --max-time 5 -D - -o /dev/null "http://localhost:${BACKEND_PORT}/health")
echo "$headers" | grep -qi "x-content-type-options: nosniff" || { echo "Missing X-Content-Type-Options header"; exit 1; }
echo "$headers" | grep -qi "x-frame-options: DENY" || { echo "Missing X-Frame-Options header"; exit 1; }
echo "$headers" | grep -qi "x-request-id:" || { echo "Missing X-Request-ID header"; exit 1; }

echo "== Starting frontend container =="
docker run -d --name "$FRONTEND_CONTAINER" -p "${FRONTEND_PORT}:3000" "$FRONTEND_IMAGE"

echo "== Waiting for frontend to respond =="
if ! curl -sf \
    --retry 20 --retry-delay 3 --retry-all-errors --retry-connrefused \
    --retry-max-time 60 --max-time 5 \
    -o /dev/null "http://localhost:${FRONTEND_PORT}/login"; then
  echo "Frontend did not become healthy within 60s. Logs:"
  docker logs "$FRONTEND_CONTAINER" || true
  exit 1
fi

echo "== Verifying frontend container's own HEALTHCHECK reports healthy =="
health_status="unknown"
for _ in $(seq 1 20); do
  health_status=$(docker inspect --format='{{.State.Health.Status}}' "$FRONTEND_CONTAINER" 2>/dev/null || echo "unknown")
  if [ "$health_status" = "healthy" ]; then
    break
  fi
  sleep 3
done
[ "$health_status" = "healthy" ] || { echo "Frontend container HEALTHCHECK never reported healthy (last: $health_status)"; exit 1; }

echo "== All Docker smoke tests passed =="
