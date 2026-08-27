# Gestiva Security — Diagnostic & Troubleshooting Guide

## Common Issues & Diagnostics

### 1. Backend Service Fails to Start
- **Symptoms**: `systemctl status gestivasec-backend` shows `failed`.
- **Diagnostic Command**:
  ```bash
  journalctl -u gestivasec-backend -n 50 --no-pager
  ```
- **Resolution**: Verify `.env` file exists and `DATABASE_URL` is accessible.

### 2. Database Connection Error
- **Symptoms**: `sqlalchemy.exc.OperationalError: could not connect to server`.
- **Resolution**: If PostgreSQL is not installed, update `DATABASE_URL` in `.env` to fallback SQLite:
  ```env
  DATABASE_URL=sqlite:///./gestivasec.db
  ```

### 3. Missing Local Monitoring Tools
- **Symptoms**: Uptime or DNS probe shows disabled capability.
- **Resolution**: Install local Linux network utilities:
  ```bash
  sudo apt-get install -y iputils-ping dnsutils traceroute net-tools
  ```

### 4. Run Diagnostic Test Suite
```bash
PYTHONPATH=. ./venv/bin/pytest tests/test_diagnostics_and_native_tools.py
```
