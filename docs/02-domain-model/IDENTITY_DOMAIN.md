# GESTIVA SECURITY — IDENTITY & ACCESS MANAGEMENT (IAM) DOMAIN SPECIFICATION

---

## 1. OBJETIVO Y ALCANCE
El Dominio de Identidad rige la autenticación de usuarios, la emisión de tokens JWT firmados, la hashing seguro con Bcrypt y el aislamiento multi-tenant estricto por organización (`BR-0004`).

---

## 2. REGLAS DE NEGOCIO E INVARIANTES
- Autenticación con firma de clave secreta JWT.
- Hashing directo con biblioteca `bcrypt`.
- Verificación del encabezado `X-Organization-ID` en toda solicitud REST protegida.
