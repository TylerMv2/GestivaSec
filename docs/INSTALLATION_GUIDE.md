# GESTIVA SECURITY (GESTIVASEC V1) — INSTALLATION & DEPLOYMENT GUIDE (RELEASE V0.1.0)

---

## 1. Requisitos del Sistema (System Requirements)
- **Docker** 20.10+ y **Docker Compose** v2.0+
- **Python** 3.11+ (para desarrollo local sin Docker)
- **Navegador Web** (Chrome, Firefox, Edge o Safari)

---

## 2. Instalación Rápida con Docker Compose (Opción Recomendada)

1. Clonar el repositorio y acceder a la raíz:
   ```bash
   cd /home/sh4d0w/Projects/gestiva_observability
   ```

2. Generar el archivo de configuración de entorno:
   ```bash
   cp .env.example .env
   ```

3. Levantar la pila completa de servicios:
   ```bash
   docker compose up -d
   ```

4. Abrir la plataforma en el navegador:
   - **Frontend Dashboard SOC**: `http://localhost:8000` (o `http://localhost:3000`)
   - **Documentación Interactiva API (OpenAPI)**: `http://localhost:8000/docs`
   - **Métricas Prometheus**: `http://localhost:9090`

---

## 3. Instalación Local con Script Bootstrap (Desarrollo)

1. Ejecutar el script automatizado de inicialización:
   ```bash
   ./scripts/bootstrap.sh
   ```

2. Iniciar el motor Backend FastAPI:
   ```bash
   PYTHONPATH=. ./venv/bin/python backend/main.py
   ```

3. Verificar la salud del sistema:
   ```bash
   ./scripts/healthcheck.sh
   ```

---

## 4. Credenciales Demo por Defecto

- **Usuario Admin SOC**: `admin@gestivaone.com`
- **Contraseña**: `GestivaSec2026!`
- **Organización Inicial**: `GestivaOne Corporation` (`gestivaone-corp`)
