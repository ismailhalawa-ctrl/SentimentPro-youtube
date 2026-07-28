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

echo "== Building backend image =="
docker build -t "$BACKEND_IMAGE" "$ROOT_DIR/backend"

echo "== Building frontend image =="
docker build -t "$FRONTEND_IMAGE" \
  --build-arg NEXT_PUBLIC_API_URL="http://localhost:${BACKEND_PORT}" \
  "$ROOT_DIR/frontend"

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
backend_healthy=false
for _ in $(seq 1 150); do
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${BACKEND_PORT}/health" || true)
  if [ "$status_code" = "200" ]; then
    backend_healthy=true
    break
  fi
  sleep 5
done

if [ "$backend_healthy" != "true" ]; then
  echo "Backend did not become healthy in time. Logs:"
  docker logs "$BACKEND_CONTAINER" || true
  exit 1
fi

health_body=$(curl -s "http://localhost:${BACKEND_PORT}/health")
echo "Backend health response: $health_body"
echo "$health_body" | grep -q '"database":"ok"' || { echo "Database check did not report ok"; exit 1; }
echo "$health_body" | grep -q '"models":"ok"' || { echo "Model check did not report ok"; exit 1; }

echo "== Verifying security headers are present =="
headers=$(curl -s -D - -o /dev/null "http://localhost:${BACKEND_PORT}/health")
echo "$headers" | grep -qi "x-content-type-options: nosniff" || { echo "Missing X-Content-Type-Options header"; exit 1; }
echo "$headers" | grep -qi "x-frame-options: DENY" || { echo "Missing X-Frame-Options header"; exit 1; }
echo "$headers" | grep -qi "x-request-id:" || { echo "Missing X-Request-ID header"; exit 1; }

echo "== Starting frontend container =="
docker run -d --name "$FRONTEND_CONTAINER" -p "${FRONTEND_PORT}:3000" "$FRONTEND_IMAGE"

echo "== Waiting for frontend to respond =="
frontend_healthy=false
for _ in $(seq 1 30); do
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${FRONTEND_PORT}/login" || true)
  if [ "$status_code" = "200" ]; then
    frontend_healthy=true
    break
  fi
  sleep 3
done

if [ "$frontend_healthy" != "true" ]; then
  echo "Frontend did not become healthy in time. Logs:"
  docker logs "$FRONTEND_CONTAINER" || true
  exit 1
fi

echo "== Verifying frontend container's own HEALTHCHECK reports healthy =="
for _ in $(seq 1 20); do
  health_status=$(docker inspect --format='{{.State.Health.Status}}' "$FRONTEND_CONTAINER" 2>/dev/null || echo "unknown")
  if [ "$health_status" = "healthy" ]; then
    break
  fi
  sleep 3
done
[ "$health_status" = "healthy" ] || { echo "Frontend container HEALTHCHECK never reported healthy (last: $health_status)"; exit 1; }

echo "== All Docker smoke tests passed =="
