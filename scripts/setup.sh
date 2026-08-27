#!/usr/bin/env bash

# Gestiva Observability NOC/SOC Setup Script
set -e

echo "[*] Initializing Gestiva Platform Setup..."

# Get current script folder path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( dirname "$SCRIPT_DIR" )"

cd "$PROJECT_DIR"

# 1. Create Python Virtual Environment if missing
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment (venv)..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# 2. Install Python Dependencies
echo "[*] Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Initialize SQLite DB
echo "[*] Initializing SQLite database and seeding defaults..."
python backend/database/db_init.py

echo "[+] Setup completed successfully!"
echo "[*] Run the following commands to start the platform:"
echo "    source venv/bin/activate"
echo "    uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"
