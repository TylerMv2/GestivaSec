#!/usr/bin/env bash
set -e

echo "=== GESTIVA SECURITY (GESTIVASEC V1) — REPOSITORY BOOTSTRAP ==="

# 1. Ensure Directory Tree
echo "[+] Creating required workspace directories..."
mkdir -p backend frontend shared database infra docker scripts tests .github/workflows

# 2. Check Python Environment
if [ ! -d "venv" ]; then
    echo "[+] Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "[+] Upgrading pip & installing dependencies..."
pip install --quiet --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install --quiet -r requirements.txt
fi

# 3. Environment Config Check
if [ ! -f ".env" ]; then
    echo "[+] Creating .env from .env.example..."
    cp .env.example .env
fi

echo "=== BOOTSTRAP COMPLETE. REPOSITORY IS READY FOR EXECUTION. ==="
