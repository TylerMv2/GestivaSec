# ASSUMPTIONS & HYPOTHESES — GESTIVASEC V1
> **Estado**: Registro Inicial de Hipótesis  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Regla de Validación de Hipótesis

Ninguna hipótesis registrada en este documento podrá convertirse en código, esquema de base de datos o infraestructura sin haber sido validada mediante un experimento técnico, PoC (Proof of Concept) autorizado o aprobación expresa en la fase correspondiente.

---

## 2. Registro Inicial de Hipótesis (Fase 0.1)

| ID | Hipótesis / Asunción | Dominio Afectado | Estado de Validación |
| :--- | :--- | :--- | :--- |
| **ASM-01** | **GestivaSec V1** operará en una topología híbrida (algunos componentes en nube privada/SaaS y sondas locales On-Premise). | Infraestructura & Redes | **Pendiente** (A validar en Fase 1: Arquitectura) |
| **ASM-02** | El volumen telemétrico de métricas y logs requerirá una estrategia de persistencia optimizada para series temporales (Time-Series). | Base de Datos | **Pendiente** (A validar en Fase 4: Datos) |
| **ASM-03** | La autenticación del sistema se basará en esquemas federados SSO/OAuth2/OIDC con soporte para MFA obligatorio. | Seguridad & Auth | **Pendiente** (A validar en Fase 3: Seguridad) |
| **ASM-04** | El frontend requerirá un sistema de diseño unificado (UIS) optimizado para pantallas de operación continua (Dark & Light Mode). | UX & Frontend | **Pendiente** (A validar en Fase 7: Frontend) |
| **ASM-05** | La plataforma requerirá procesamiento distribuido de eventos en tiempo real mediante un bus pub/sub. | Arquitectura & Backend | **Pendiente** (A validar en Fase 1 y 6) |
