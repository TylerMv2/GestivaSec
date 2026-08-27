# IAM_SESSIONS_SPEC.md — DOMAIN & ENGINEERING SPECIFICATION

**Slice ID:** `IAM-SESSIONS`  
**Capability ID:** `CAP-01` (Identity & Access Management)  
**Document Status:** `READY_FOR_REVIEW`  
**Studio Assessment:** `READY_FOR_REVIEW`  
**ARB Status:** `PENDING`  
**Owner:** Architecture Studio (Principal Security & Software Architects)  
**Date:** 2026-07-26  

---

## 1. Propósito Estratégico y Problema de Dominio

Actualmente la autenticación emite tokens JWT independientes sin estado (*stateless*). Esto impide revocar accesos inmediatamente ante un cierre de sesión, sospecha de compromiso de credenciales o expiración forzada por política de seguridad (*BR-0005*).

El slice **`IAM-SESSIONS`** introduce la **Gestión de Sesiones Activas y Motor de Invalidador/Blacklist de Tokens JWT**, permitiendo:
1. Registrar sesiones activas vinculadas a un usuario y organización (*BR-0004*).
2. Revocar e invalidar tokens JWT al ejecutar `POST /api/v1/auth/logout`.
3. Interceptación middleware de peticiones entrantes para rechazar tokens incluidos en la blacklist.

---

## 2. Invariantes de Negocio Aplicables

- **`BR-0004` (Multi-Tenant Isolation):** Las sesiones están aisladas strictly por `organization_id`.
- **`BR-0005` (JWT Token Revocation & Blacklist):** Todo token marcado en la lista de invalidador es rechazado inmediatamente con estado HTTP 401 Unauthorized.

---

## 3. Modelo de Dominio (`backend/domain/session.py`)

### 3.1 Entidad `UserSession`
- `session_id`: UUID
- `user_id`: UUID
- `organization_id`: UUID
- `token`: str (JWT Access Token)
- `ip_address`: str
- `user_agent`: str
- `created_at`: datetime (UTC aware)
- `is_active`: bool

### 3.2 Servicio de Invalidador (`TokenBlacklistService`)
- `revoke_token(token: str)`
- `is_token_revoked(token: str) -> bool`

---

## 4. Adaptadores REST API (`backend/api/auth_router.py`)

- **`POST /api/v1/auth/logout`**: Recibe Bearer Token, registra la revocación en la lista negra y retorna mensaje de éxito (200 OK).
- **`GET /api/v1/auth/me`**: Fails with 401 Unauthorized if Bearer token is revoked/blacklisted.

---

## 5. Pruebas de Aceptación (`tests/test_slice_007_sessions.py`)

- `test_login_and_logout_flow_success`: Verificado (Pass).
- `test_logout_without_token_fails`: Verificado (Pass).
