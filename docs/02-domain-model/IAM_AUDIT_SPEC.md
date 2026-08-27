# IAM_AUDIT_SPEC.md — DOMAIN & ENGINEERING SPECIFICATION

**Slice ID:** `IAM-AUDIT`  
**Capability ID:** `CAP-01` (Identity & Access Management)  
**Document Status:** `READY_FOR_REVIEW`  
**Studio Assessment:** `READY_FOR_REVIEW`  
**ARB Status:** `PENDING`  
**Owner:** Architecture Studio (Principal Security & Software Architects)  
**Date:** 2026-07-26  

---

## 1. Propósito Estratégico y Problema de Dominio

Para cumplir con estándares de auditoría corporativa y trazabilidad de ciberseguridad, todas las acciones administrativas sensibles (creación de usuarios, cambios de roles, modificación de activos, intentos de autenticación) deben quedar registradas en una bitácora inmutable de auditoría (*Audit Trail*).

El slice **`IAM-AUDIT`** introduce el **Registro Inmutable de Auditoría Administrativa**, permitiendo:
1. Registrar de forma inmutable eventos administrativos (`user_created`, `role_changed`, `login_success`, `login_failed`, `asset_created`).
2. Aislar los registros por organización (*BR-0004*).
3. Exponer el endpoint de consulta `GET /api/v1/audit/logs` autenticado y filtrado por fecha y actor.

---

## 2. Invariantes de Negocio Aplicables

- **`BR-0004` (Multi-Tenant Isolation):** Los registros de auditoría están aislados estrictamente por `organization_id`.
- **`BR-0005` (Audit Trail Inmutabilidad):** Los registros de auditoría no pueden ser modificados ni eliminados vía API (Append-Only Store).

---

## 3. Modelo de Dominio (`backend/domain/audit_log.py`)

### 3.1 Entidad `AuditEvent`
- `event_id`: UUID
- `organization_id`: UUID
- `actor_user_id`: UUID
- `actor_email`: str
- `action`: str (ej. `USER_CREATED`, `ROLE_UPDATED`, `LOGIN_SUCCESS`, `LOGOUT`)
- `resource_type`: str (ej. `USER`, `ASSET`, `AUTH`)
- `resource_id`: str
- `details`: dict
- `ip_address`: str
- `timestamp`: datetime (UTC aware)

---

## 4. Adaptadores REST API (`backend/api/audit_router.py`)

- **`GET /api/v1/audit/logs`**: Retorna los eventos de auditoría registrados para la organización del usuario autenticado.

---

## 5. Acceptance Criteria Checklist (Estándar ARB)

- [x] **Criterion 1:** Entidad de dominio `AuditEvent` creada e inmutable en `backend/domain/audit_log.py`.
- [x] **Criterion 2:** Repositorio registrando eventos de auditoría con aislamiento `organization_id` (*BR-0004*).
- [x] **Criterion 3:** Endpoint REST `GET /api/v1/audit/logs` autenticado vía JWT.
- [x] **Criterion 4:** Suite de pruebas en `tests/test_slice_008_audit.py` pasando al 100% (2 test cases passing).

---

## 6. Pruebas de Aceptación (`tests/test_slice_008_audit.py`)

- `test_record_and_query_audit_events`: Verificado (Pass).
- `test_unauthenticated_audit_access_fails`: Verificado (Pass).
