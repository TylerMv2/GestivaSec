#!/usr/bin/env bash
# ================================================================================
# GESTIVASEC V1 — HOSTINGER ZERO-DOWNTIME DEPLOYMENT SCRIPT
# Authority: Gestiva Security Infrastructure & DevOps Team
# System Target: Hostinger VPS / Linux Ubuntu 22.04 / 24.04 LTS
# ================================================================================

set -e

echo "🚀 Starting GestivaSec V1 Deployment to Hostinger Environment..."

# CONFIGURATION VARIABLES
HOSTINGER_USER="${HOSTINGER_USER:-gestiva}"
HOSTINGER_HOST="${HOSTINGER_HOST:-sec.gestivaone.com}"
REMOTE_APP_DIR="/home/u987654321/public_html/gestivasec"
VENV_PATH="${REMOTE_APP_DIR}/venv"
SERVICE_NAME="gestivasec-backend.service"

echo "📌 Target Host: ${HOSTINGER_USER}@${HOSTINGER_HOST}"
echo "📁 Deployment Directory: ${REMOTE_APP_DIR}"

# 1. VERIFY SYSTEM DEPS & PYTHON VERSION
python3 --version || { echo "❌ Python3 missing!"; exit 1; }

# 2. SYNC CODE REPOSITORY
if [ -d "${REMOTE_APP_DIR}/.git" ]; then
    echo "🔄 Pulling latest release from Git repository..."
    cd "${REMOTE_APP_DIR}"
    git fetch origin main
    git reset --hard origin/main
else
    echo "📦 Initializing production release directory..."
    mkdir -p "${REMOTE_APP_DIR}"
fi

# 3. VIRTUAL ENVIRONMENT & DEPENDENCIES
if [ ! -d "${VENV_PATH}" ]; then
    echo "🐍 Creating Virtualenv environment..."
    python3 -m venv "${VENV_PATH}"
fi

echo "📦 Installing production dependencies..."
"${VENV_PATH}/bin/pip" install --upgrade pip
if [ -f "${REMOTE_APP_DIR}/requirements.txt" ]; then
    "${VENV_PATH}/bin/pip" install -r "${REMOTE_APP_DIR}/requirements.txt"
fi

# 4. EXECUTE AUTOMATED INTEGRITY TESTS
echo "🧪 Running Automated Verification Test Suite..."
PYTHONPATH="${REMOTE_APP_DIR}" "${VENV_PATH}/bin/pytest" --maxfail=1 || {
    echo "❌ Deployment aborted: Test Suite Failed!"
    exit 1;
}

# 5. ZERO-DOWNTIME SERVICE RESTART (SYSTEMD OR GUNICORN)
if command -v systemctl >/dev/null 2>&1; then
    echo "♻️ Reloading systemd backend service ${SERVICE_NAME}..."
    sudo systemctl restart "${SERVICE_NAME}" || systemctl --user restart "${SERVICE_NAME}"
else
    echo "⚡ Restarting Uvicorn production server process..."
    pkill -f "uvicorn backend.main:app" || true
    nohup "${VENV_PATH}/bin/uvicorn" backend.main:app --host 0.0.0.0 --port 8000 --workers 4 > "${REMOTE_APP_DIR}/server.log" 2>&1 &
fi

echo "✅ GestivaSec V1 Successfully Deployed to Hostinger!"
