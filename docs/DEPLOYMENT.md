# Gestiva Security — Deployment Guide

This document details deployment strategies for self-hosted environments behind Nginx, Systemd, and Docker containers.

---

## 1. Systemd + Nginx Bare-Metal / VM Deployment

### Step 1: Clone and Run Portable Installer
```bash
git clone https://github.com/gestivaone/gestiva_observability.git /opt/gestivasecurity
cd /opt/gestivasecurity
sudo ./install.sh
```

### Step 2: Nginx Reverse Proxy Configuration (`/etc/nginx/sites-available/gestivasec.conf`)
```nginx
server {
    listen 80;
    server_name security.yourdomain.com;

    client_max_body_size 50M;

    location / {
        root /opt/gestivasecurity/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        alias /opt/gestivasecurity/frontend/static/;
        expires 30d;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and reload:
```bash
sudo ln -sf /etc/nginx/sites-available/gestivasec.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 2. Docker Compose Deployment

Gestiva Security includes an isolated `docker-compose.yml` pre-configured with PostgreSQL and Redis.

```bash
# Start all services in background
docker compose up -d

# Inspect running containers
docker compose ps

# View logs
docker compose logs -f backend
```

---

## 3. Database Migration & Initialization

Initialize or upgrade the PostgreSQL schema:
```bash
PYTHONPATH=. ./venv/bin/alembic upgrade head
```
