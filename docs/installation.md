# Gestiva Observability & Security Platform - Installation Guide

Follow these steps to deploy and execute the NOC/SOC observability platform on localhost (tested on Kali Linux).

## Prerequisites
Ensure Python 3.10+ and pip are installed:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## Running Setup
1. Create a python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install packages listed in dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database and seeds structure:
   ```bash
   python backend/database/db_init.py
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```

Open `http://127.0.0.1:8000` in your web browser. The Cyberpunk dashboard will render immediately, and background monitoring tasks will record host parameters.
