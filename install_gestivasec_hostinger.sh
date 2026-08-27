#!/usr/bin/env bash
# ================================================================================
# GESTIVASEC V1 — AUTOMATED ISOLATED INSTALLER FOR SECURITY.GESTIVAONE.COM
# Target OS: Ubuntu 20.04 / 22.04 / 24.04 LTS (Hostinger VPS / Dedicated Server)
# Guarantee: Zero side-effects on existing sites or main gestivaone.com domain.
# ================================================================================

set -e

# COLOR SYSTEM
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}====================================================================${NC}"
echo -e "${PURPLE}   GESTIVASEC V1 — ISOLATED HOSTINGER INSTALLER (SECURITY DOMAIN)   ${NC}"
echo -e "${PURPLE}====================================================================${NC}"

DOMAIN="security.gestivaone.com"
INSTALL_DIR="/var/www/gestivasec"
BACKEND_PORT="8005"
SYSTEMD_SERVICE="gestivasec-backend.service"

# 1. ROOT & OS VERIFICATION
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Debe ejecutar este instalador como root o con sudo.${NC}"
    echo -e "Uso: sudo ./install_gestivasec_hostinger.sh"
    exit 1
fi

echo -e "${CYAN}[1/6] Verificando dependencias base del sistema Ubuntu...${NC}"
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip nginx certbot python3-certbot-nginx git curl ufw

# 2. CREATE ISOLATED DIRECTORY STRUCTURE
echo -e "${CYAN}[2/6] Creando directorio aislado en ${INSTALL_DIR}...${NC}"
mkdir -p "${INSTALL_DIR}"
cp -rf . "${INSTALL_DIR}/"
cd "${INSTALL_DIR}"

# 3. PYTHON VIRTUALENV & DEPENDENCIES
echo -e "${CYAN}[3/6] Configurando entorno virtual Python aislado...${NC}"
if [ ! -d "${INSTALL_DIR}/venv" ]; then
    python3 -m venv "${INSTALL_DIR}/venv"
fi

"${INSTALL_DIR}/venv/bin/pip" install --upgrade pip -q
"${INSTALL_DIR}/venv/bin/pip" install -r requirements.txt -q

# 4. SYSTEMD SERVICE CONFIGURATION (PORT 8005 ISOLATED)
echo -e "${CYAN}[4/6] Configurando servicio Systemd (${SYSTEMD_SERVICE})...${NC}"
cat <<EOF > /etc/systemd/system/${SYSTEMD_SERVICE}
[Unit]
Description=GestivaSec V1 Enterprise SOC Platform Backend (security.gestivaone.com)
After=network.target

[Service]
User=root
WorkingDirectory=${INSTALL_DIR}
Environment="PYTHONPATH=${INSTALL_DIR}"
Environment="GESTIVASEC_ENV=production"
ExecStart=${INSTALL_DIR}/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port ${BACKEND_PORT} --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ${SYSTEMD_SERVICE}
systemctl restart ${SYSTEMD_SERVICE}

# 5. DEDICATED NGINX VIRTUAL HOST FOR SECURITY.GESTIVAONE.COM
echo -e "${CYAN}[5/6] Configurando Nginx para el subdominio ${DOMAIN}...${NC}"
NGINX_CONF="/etc/nginx/sites-available/${DOMAIN}.conf"

cat <<EOF > ${NGINX_CONF}
# Configuration for ${DOMAIN} (Gestiva Security Platform)
# Isolated block: Does NOT affect main gestivaone.com domain

server {
    listen 80;
    server_name ${DOMAIN};

    client_max_body_size 50M;

    # Static Frontend
    location / {
        root ${INSTALL_DIR}/frontend;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # Static CSS & JS Assets
    location /static/ {
        alias ${INSTALL_DIR}/frontend/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # REST API Proxy to Isolated FastAPI Service (Port ${BACKEND_PORT})
    location /api/ {
        proxy_pass http://127.0.0.1:${BACKEND_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
EOF

# Enable Nginx Site
ln -sf ${NGINX_CONF} /etc/nginx/sites-enabled/${DOMAIN}.conf

# Verify Nginx configuration syntax
nginx -t

echo -e "${CYAN}[6/6] Reiniciando Nginx...${NC}"
systemctl reload nginx

echo -e "${GREEN}====================================================================${NC}"
echo -e "${GREEN}✅ ¡INSTALACIÓN COMPLETADA EXITOSAMENTE SIN AFECTAR OTROS SITIOS! ${NC}"
echo -e "${GREEN}====================================================================${NC}"
echo -e " Dominio Configurado: https://${DOMAIN}"
echo -e " Directorio de Instalación: ${INSTALL_DIR}"
echo -e " Servicio Backend: systemctl status ${SYSTEMD_SERVICE}"
echo -e ""
echo -e "${PURPLE}🔒 PARA ACTIVAR CERTIFICADO SSL GRATUITO (HTTPS):${NC}"
echo -e " Ejecute: sudo certbot --nginx -d ${DOMAIN}"
echo -e "===================================================================="
