# GESTIVASEC V1 — MANUAL DE INSTALACIÓN Y CONEXIONES API / SUPABASE / HOSTINGER
**Dominio Objetivo:** `security.gestivaone.com`  
**Plataforma:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Fecha:** 2026-07-26  

---

## 1. GUÍA RÁPIDA DE IMPORTACIÓN A SUPABASE (DATABASE & LOGIN)

Para alojar la sección de Login y la base de datos completa de **Gestiva Security** en Supabase para el dominio `security.gestivaone.com`:

### Paso 1: Crear Proyecto en Supabase
1. Ingrese a [Supabase Dashboard](https://supabase.com/dashboard) e inicie sesión.
2. Haga clic en **"New Project"**.
3. Ingrese los datos del proyecto:
   - **Name:** `GestivaSec-V1`
   - **Database Password:** Guarde una contraseña segura.
   - **Region:** Seleccione la región más cercana (ej: `us-east-1` o `sa-east-1`).
4. Una vez creado, vaya a **Project Settings** -> **API** y copie:
   - `Project URL` (ejemplo: `https://xyzcompany.supabase.co`)
   - `anon public key` (ejemplo: `eyJhbGciOi...`)

### Paso 2: Importar la Base de Datos (SQL Editor)
1. En el menú lateral de Supabase, haga clic en **SQL Editor**.
2. Abra el archivo local del proyecto:  
   [`database/supabase_schema.sql`](file:///home/sh4d0w/Projects/gestiva_observability/database/supabase_schema.sql)
3. Copie todo el contenido SQL y péguelo en la consola del SQL Editor de Supabase.
4. Haga clic en **"Run"**.
5. **Resultado:** Se crearán las tablas `organizations`, `user_profiles`, `assets`, `actionable_alerts`, `incident_cases`, `audit_logs` con sus políticas de seguridad RLS (*Row Level Security*) y datos semilla iniciales.

---

## 2. UBICACIÓN EXACTA DE ARCHIVOS A MODIFICAR MANUALMENTE (CONEXIONES & APIs)

A continuación se detallan **todos los archivos** donde debes colocar tus credenciales, llaves API y URLs de producción:

| Recurso / Conexión | Ruta Exacta del Archivo | Variables / Líneas a Editar | Descripción |
| :--- | :--- | :--- | :--- |
| **Variables de Entorno Backend** | [`.env`](file:///home/sh4d0w/Projects/gestiva_observability/.env) | `SUPABASE_URL`<br>`SUPABASE_KEY`<br>`DATABASE_URL`<br>`JWT_SECRET` | Credenciales de conexión a Supabase PostgreSQL y firma JWT backend |
| **Credenciales Frontend Auth Gate** | [`frontend/static/js/auth_gate.js`](file:///home/sh4d0w/Projects/gestiva_observability/frontend/static/js/auth_gate.js#L14-L16) | `SUPABASE_URL`<br>`SUPABASE_ANON_KEY` | Llaves públicas para inicializar el cliente JS de Supabase Auth |
| **Orígenes de Dominio CORS** | [`backend/main.py`](file:///home/sh4d0w/Projects/gestiva_observability/backend/main.py#L48-L55) | `origins = [...]` | Lista de dominios permitidos (`https://security.gestivaone.com`) |
| **Enrutamiento Serverless Vercel** | [`vercel.json`](file:///home/sh4d0w/Projects/gestiva_observability/vercel.json) | `"env"` | Configuración de rutas y variables para hosting Vercel |
| **Configuración Nginx Hostinger** | [`install_gestivasec_hostinger.sh`](file:///home/sh4d0w/Projects/gestiva_observability/install_gestivasec_hostinger.sh#L23-L25) | `DOMAIN`<br>`INSTALL_DIR` | Dominio objetivo (`security.gestivaone.com`) y directorio base |

---

## 3. CÓMO IMPORTAR Y DESPLEGAR EN UN SERVIDOR UBUNTU DE HOSTINGER (SIN AFECTAR OTROS SITIOS)

### ¿Cómo instalarlo sin tocar nada más en el servidor?
El instalador automatizado [`install_gestivasec_hostinger.sh`](file:///home/sh4d0w/Projects/gestiva_observability/install_gestivasec_hostinger.sh) está diseñado bajo un **paradigma de aislamiento total**:
1. **Directorio Independiente:** Se instala exclusivamente en `/var/www/gestivasec`.
2. **Puerto Backend Aislado:** Ejecuta el backend FastAPI en el puerto interno `127.0.0.1:8005` (localhost), evitando conflictos con MySQL, Apache u otros servicios en los puertos 80/443/3306/8000.
3. **Bloque Nginx Dedicado:** Crea un archivo de configuración separado en `/etc/nginx/sites-available/security.gestivaone.com.conf`. **No toca ningún archivo de `gestivaone.com` ni de otros sitios alojados en el servidor.**

---

### PASOS PARA DESPLEGAR EN HOSTINGER (UBUNTU):

#### 1. Transferir o Clonar el Proyecto al Servidor Hostinger
Vía SSH en tu servidor Ubuntu de Hostinger:
```bash
# Clonar o copiar el proyecto
cd /tmp
git clone https://github.com/tu-usuario/gestiva_observability.git gestivasec
cd gestivasec
```

#### 2. Ejecutar el Instalador Aislado Unclik
```bash
sudo chmod +x install_gestivasec_hostinger.sh
sudo ./install_gestivasec_hostinger.sh
```

El instalador realizará automáticamente:
- Instalación de Python 3, venv, Nginx y Certbot.
- Creación del entorno virtual aislado en `/var/www/gestivasec/venv`.
- Configuración y activación del servicio daemon `systemctl start gestivasec-backend.service`.
- Configuración de Nginx para responder exclusivamente en el subdominio `security.gestivaone.com`.

#### 3. Activar Certificado SSL Gratuito (HTTPS)
Una vez apuntado el registro DNS tipo `A` de `security.gestivaone.com` a la IP de tu servidor Hostinger, ejecuta:
```bash
sudo certbot --nginx -d security.gestivaone.com
```

---

## 4. VERIFICACIÓN Y AUDITORÍA DE PRUEBAS
Para validar la instalación en el servidor Ubuntu:
```bash
cd /var/www/gestivasec
PYTHONPATH=. ./venv/bin/pytest
```
**Resultado Esperado:** 76 passed (100% verde).
