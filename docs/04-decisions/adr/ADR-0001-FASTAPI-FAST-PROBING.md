# ADR-0001: ADOPCIÓN DE FASTAPI & HTTPX ASÍNCRONO PARA OBSERVABILIDAD SINTÉTICA

---

## 1. ESTADO
**APPROVED** (Decisión congelada).

---

## 2. CONTEXTO Y PROBLEMA
La plataforma GestivaSec requiere ejecutar sondeos pasivos y sintéticos continuos a intervalos de 1 minuto sin bloquear las solicitudes HTTP de la API REST.

---

## 3. DECISIÓN
Adoptar **FastAPI** con **HTTPX AsyncClient** no bloqueante y motor de eventos asyncio de Python 3.13.

---

## 4. CONSECUENCIAS
- Permite ejecutar cientos de sondeos asíncronos concurrentes con una latencia de respuesta < 5ms en los controladores REST.
