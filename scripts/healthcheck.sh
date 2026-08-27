#!/usr/bin/env bash
set -e

echo "=== GESTIVA SECURITY (GESTIVASEC V1) — HEALTHCHECK EXECUTION ==="

PORT=${PORT:-8000}
URL="http://localhost:${PORT}/health"

echo "[+] Checking API endpoint: ${URL}"
if curl -s -f "${URL}" > /dev/null; then
    echo "[✓] HEALTHCHECK PASSED: System is operational and healthy."
    exit 0
else
    echo "[✗] HEALTHCHECK FAILED: API endpoint is unreachable."
    exit 1
fi
