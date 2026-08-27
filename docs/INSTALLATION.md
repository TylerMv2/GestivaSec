# Gestiva Security — Installation Guide

## System Requirements

- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+, Kali Linux, CentOS 8+, AlmaLinux, RHEL 8+)
- **CPU**: 2 Cores minimum (4 Cores recommended for high-volume telemetry)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 20 GB free space for database & forensic evidence storage

---

## Installation Options

### Option A: Portable Installer (Recommended for Bare-Metal & VMs)
```bash
sudo ./install.sh
```

The installer will automatically:
1. Install system utilities (`python3`, `python3-venv`, `ping`, `dnsutils`, `traceroute`).
2. Create Python virtual environment under `/opt/gestivasecurity/venv`.
3. Install dependencies from `requirements.txt`.
4. Generate `.env` configuration file from `.env.example`.
5. Configure and start Systemd service (`gestivasec-backend.service`).
6. Run diagnostic tests to verify installation integrity.

---

### Option B: Manual Virtual Environment Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
