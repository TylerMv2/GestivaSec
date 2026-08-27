#!/usr/bin/env bash
# ================================================================================
# GESTIVA SECURITY (GESTIVASEC V1) — PORTABLE SELF-HOSTED INSTALLER
# Target OS: Ubuntu / Debian / Kali / CentOS / RHEL / AlmaLinux
# Paradigm: Completely isolated, self-hosted, cloud-agnostic deployment.
# ================================================================================

set -e

# COLOR SYSTEM
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}====================================================================${NC}"
echo -e "${PURPLE}   GESTIVASEC V1 — PORTABLE SELF-HOSTED ENTERPRISE SOC INSTALLER    ${NC}"
echo -e "${PURPLE}====================================================================${NC}"

INSTALL_DIR="${GESTIVA_INSTALL_DIR:-/opt/gestivasecurity}"
BACKEND_PORT="${PORT:-8000}"
SYSTEMD_SERVICE="gestivasec-backend.service"

# 1. ROOT & OS VERIFICATION
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Must run installer as root or with sudo.${NC}"
    echo -e "Usage: sudo ./install.sh"
    exit 1
fi

echo -e "${CYAN}[1/6] Verifying system dependencies...${NC}"
if command -v apt-get &> /dev/null; then
    apt-get update -qq
    apt-get install -y -qq python3 python3-venv python3-pip git curl ufw iputils-ping dnsutils traceroute net-tools
elif command -v dnf &> /dev/null; then
    dnf install -y python3 python3-pip git curl ping bind-utils net-tools
fi

# 2. CREATE ISOLATED DIRECTORY STRUCTURE
echo -e "${CYAN}[2/6] Creating installation directory at ${INSTALL_DIR}...${NC}"
mkdir -p "${INSTALL_DIR}"
cp -rf . "${INSTALL_DIR}/"
cd "${INSTALL_DIR}"

# 3. PYTHON VIRTUALENV & DEPENDENCIES
echo -e "${CYAN}[3/6] Setting up isolated Python virtual environment...${NC}"
if [ ! -d "${INSTALL_DIR}/venv" ]; then
    python3 -m venv "${INSTALL_DIR}/venv"
fi

"${INSTALL_DIR}/venv/bin/pip" install --upgrade pip -q
"${INSTALL_DIR}/venv/bin/pip" install -r requirements.txt -q

# Create .env if not existing
if [ ! -f "${INSTALL_DIR}/.env" ]; then
    cp "${INSTALL_DIR}/.env.example" "${INSTALL_DIR}/.env"
fi

# Create Storage directory
mkdir -p "${INSTALL_DIR}/storage"

# 4. SYSTEMD SERVICE CONFIGURATION
echo -e "${CYAN}[4/6] Configuring Systemd service (${SYSTEMD_SERVICE})...${NC}"
cat <<EOF > /etc/systemd/system/${SYSTEMD_SERVICE}
[Unit]
Description=GestivaSec V1 Enterprise SOC Platform Backend
After=network.target

[Service]
User=root
WorkingDirectory=${INSTALL_DIR}
Environment="PYTHONPATH=${INSTALL_DIR}"
Environment="ENVIRONMENT=production"
ExecStart=${INSTALL_DIR}/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port ${BACKEND_PORT} --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ${SYSTEMD_SERVICE}
systemctl restart ${SYSTEMD_SERVICE}

# 5. VALIDATING INSTALLATION & RUNNING CRITICAL SUITE
echo -e "${CYAN}[5/6] Executing self-test validation suite...${NC}"
cd "${INSTALL_DIR}"
PYTHONPATH=. ./venv/bin/pytest tests/test_e2e_golden_demo.py -q

echo -e "${GREEN}====================================================================${NC}"
echo -e "${GREEN}✅ GESTIVA SECURITY INSTALLATION COMPLETED SUCCESSFULLY!           ${NC}"
echo -e "${GREEN}====================================================================${NC}"
echo -e " Installation Path: ${INSTALL_DIR}"
echo -e " Backend Service  : systemctl status ${SYSTEMD_SERVICE}"
echo -e " Web Interface    : http://localhost:${BACKEND_PORT}"
echo -e " Environment File : ${INSTALL_DIR}/.env"
echo -e " Storage Location : ${INSTALL_DIR}/storage"
echo -e "===================================================================="
