# GESTIVA SECURITY (GESTIVASEC V1) — MANUAL DEL ADMINISTRADOR DE SISTEMAS (RELEASE V0.1.0)

---

## 1. Mantenimiento y Operación con Docker
- **Verificar estado de contenedores**:
  ```bash
  docker compose ps
  ```
- **Revisar logs en tiempo real del backend**:
  ```bash
  docker compose logs -f backend
  ```
- **Reiniciar servicios de la plataforma**:
  ```bash
  docker compose restart
  ```

---

## 2. Variables de Entorno y Seguridad
La configuración global reside en el archivo `.env`:
- `JWT_SECRET`: Clave privada para firma de tokens JWT (Cambiar obligatoriamente en producción).
- `DATABASE_URL`: Cadena de conexión PostgreSQL/Supabase.
- `REDIS_URL`: Servidor Redis para broker de eventos.
- `LOG_LEVEL`: Nivel de detalle de logs (`INFO`, `DEBUG`, `WARNING`).

---

## 3. Verificación de Fitness y Deuda Técnica
Para ejecutar la suite completa de calidad y pruebas de arquitectura:
```bash
PYTHONPATH=. ./venv/bin/python -m pytest tests/
```
Garantiza:
- Zero marcas `FIXME`.
- Cero importaciones circulares.
- Pureza del dominio sin fugas de infraestructura.
- 100% de pruebas verdes (38/38 passing).
