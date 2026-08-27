FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (required for paramiko, cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize DB on startup and run FastAPI
CMD python backend/database/db_init.py && uvicorn backend.main:app --host 0.0.0.0 --port 8000
