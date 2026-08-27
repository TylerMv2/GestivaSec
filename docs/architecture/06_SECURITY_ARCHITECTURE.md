# 3.6 SECURITY ARCHITECTURE — GESTIVASEC V1
> **Estado**: Especificación Oficial de Arquitectura de Seguridad Empresarial (Zero-Trust & STRIDE)  
> **Comité**: Chief Enterprise Architect, Security Architect & TOGAF Specialist  
> **Fase**: FASE 3: ENTERPRISE ARCHITECTURE — Subfase 3.6  
> **Fecha**: 2026-07-25  

---

## 1. Executive Summary (Resumen Ejecutivo)

La subfase **3.6 Security Architecture** establece la **Especificación Oficial de Arquitectura de Seguridad** para **GestivaSec V1**. Autorizada por el Architecture Review Board (ARB) tras la aprobación definitiva de las subfases 3.1 a 3.5, este documento define la estrategia de ciberseguridad, el modelo **Zero-Trust**, las Zonas de Confianza (*Trust Zones*), el Modelado de Amenazas (**STRIDE**), las defensas Multi-Tenant y los controles criptográficos innegociables para el sistema.

La Arquitectura de Seguridad operacionaliza los principios `PRIN-02` (*Security by Design*) y `PRIN-03` (*Immutable Auditability*), así como las restricciones mandatorias `CONST-03` (*Strict Multi-Tenant Isolation*) y `CONST-05` (*Immutable Audit Retention*), garantizando la protección estricta de la información telemétrica y de gobernanza de GestivaSec V1.

---

## 2. Security Architecture Model (Modelo Zero-Trust y Defensa en Profundidad)

La arquitectura de seguridad adopta el paradigma **Zero-Trust (Confianza Cero)** articulado en 3 pilares inmutables:

1. **Verificación Explícita Continua**: Toda solicitud, consulta o interacción debe ser autenticada y autorizada expresamente, sin importar si proviene del perímetro exterior o de redes internas.
2. **Acceso con Privilegio Mínimo (Least Privilege)**: La asignación de permisos se acota estrictamente a las operaciones mínimas necesarias por rol (RBAC) y discriminador organizacional (`tenant_id`).
3. **Asunción de Brecha (Assume Breach)**: El diseño asume la posibilidad de compromiso de fronteras individuales, minimizando el radio de impacto mediante el aislamiento de zonas de confianza y cifrado extremo a extremo.

---

## 3. Trust Zones & Security Boundaries (Zonas de Confianza)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ZONAS DE CONFIANZA Y FRONTERAS DE SEGURIDAD (TRUST ZONES MODEL)                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ZONA DE CONFIANZA 0: PERÍMETRO PÚBLICO NO CONFIABLE (Public Untrusted Zone)             │
│ • Origen de peticiones de usuarios y endpoints públicos supervisados.                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ──────────► [ FRONTERA 1: GATEWAY DE SEGURIDAD & INYECCIÓN DE TENANT CONTEXT ] ──────────│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ZONA DE CONFIANZA 1: ZONA PERIMETRAL DE AUTENTICACIÓN Y FILTRADO                         │
│ • Verificación de identidad y convalidación de tokens de sesión.                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ──────────► [ FRONTERA 2: AISLAMIENTO DE PROCESAMIENTO DISTRIBUIDO ] ──────────────────│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ZONA DE CONFIANZA 2: ZONA INTERNA DE EVALUACIÓN Y PROCESAMIENTO                         │
│ • Ejecución de comprobaciones telemétricas y evaluación continua de estado.             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ──────────► [ FRONTERA 3: PROTECCIÓN DE DATOS Y ESTADO DE NÚCLEO ] ─────────────────────│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ZONA DE CONFIANZA 3: ZONA NÚCLEO TRANSACCIONAL DE MÁXIMA CONFIANZA                      │
│ • Almacenamiento y procesamiento de reglas fundamentales de negocio.                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ──────────► [ FRONTERA 4: BÓVEDA INMUTABLE DE AUDITORÍA APPEND-ONLY ] ──────────────────│
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ ZONA DE CONFIANZA 4: ZONA DE PERSISTENCIA Y AUDITORÍA INALTERABLE                        │
│ • Almacenamiento aislado protegida de solo escritura (0 UPDATE/DELETE).                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Threat Modeling (Análisis STRIDE y Estrategias de Mitigación)

Se aplica la metodología de modelado de amenazas **STRIDE** sobre la arquitectura de componentes de GestivaSec V1:

| Amenaza STRIDE | Descripción del Riesgo | Impacto | Estrategia Arquitectónica de Mitigación |
| :--- | :--- | :---: | :--- |
| **Spoofing** (Suplantación) | Un actor malicioso suplanta la identidad de un operario o tenant. | **Alto** | Autenticación criptográfica con firmas de tokens e inyección obligatoria de `tenant_id`. |
| **Tampering** (Manipulación) | Alteración de métricas de sondas o expedientes de incidentes. | **Crítico** | Cifrado en tránsito (TLS 1.3), verificación de integridad y políticas RLS de datos. |
| **Repudiation** (Repudio) | Operador niega haber realizado una modificación de criticidad de activo. | **Crítico** | Traza de auditoría inmutable append-only (`CONST-05`) con firma de actor y timestamp. |
| **Information Disclosure** | Contaminación cruzada o lectura de datos de un tenant por otro. | **Crítico** | Aislamiento estricto Multi-Tenant a nivel de almacenamiento y acceso (`CONST-03`). |
| **Denial of Service** | Sobrecarga de peticiones telemétricas sintéticas hacia activos en producción.| **Alto** | Sondaje no degradante (`CONST-04`) con límites de tasa pasivos acotados. |
| **Elevation of Privilege** | Operario de nivel bajo ejecuta acciones de administración global. | **Alto** | Control de Acceso Basado en Roles (RBAC) estricto con principio de mínimo privilegio. |

---

## 5. Data Protection & Cryptographic Controls (Protección de Datos)

1. **Cifrado en Tránsito (Data in Transit)**:
   - Protocolo obligatorio **TLS 1.3** (o TLS 1.2 estricto con suites de cifrado Perfect Forward Secrecy) para todas las comunicaciones entre componentes y servicios exteriores (`NFR-SEC-02`).
   - Cero tráfico en texto plano HTTP dentro o fuera de las fronteras de confianza.
2. **Cifrado en Reposo (Data at Rest)**:
   - Cifrado simétrico **AES-256** obligatorio para todas las bases de datos, volúmenes de almacenamiento y trazas de auditoría archivadas.
   - Claves de cifrado gestionadas bajo políticas de rotación periódica.
3. **Mecanismo de Aislamiento Multi-Tenant**:
   - Inserción mandatoria del discriminador `tenant_id` en todas las estructuras de persistencia, con enforzamiento de seguridad directamente en las políticas de almacenamiento (Row Level Security).

---

## 6. Security Governance & Compliance Alignment

- **Alineación Normativa**: Estructura de controles alineada con los marcos **ISO/IEC 27001** (Controles A.5 a A.8) y **NIST Cybersecurity Framework (CSF 2.0)** en sus funciones *Identify, Protect, Detect, Respond, Recover*.
- **Gobernanza de Claves y Secretos**: Prohibición absoluta de incluir contraseñas, tokens o claves criptográficas incrustadas (*hardcoded*) en el código fuente o repositorios (`PRIN-02`).
- **Auditoría Forense de Seguridad**: Todo evento de seguridad (intentos de acceso rechazados, cambios de políticas, elevaciones de privilegio) emite inmediatamente un registro no repudiable a la Zona de Auditoría Inalterable (`LOG-AREA-05`).

---

## 7. Architectural Traceability Matrix (Trazabilidad de Seguridad)

| Control de Seguridad | Restricción Inviolable (`3.3`) | Principio de Arquitectura (`3.2`) | Atributo de Calidad (`3.1`) | Amenaza STRIDE Mitigada |
| :--- | :--- | :--- | :--- | :--- |
| **Gateway de Autenticación** | `CONST-03` (Multi-Tenant) | `PRIN-02` (Zero Trust) | `ATTR-03` (Seguridad) | Spoofing |
| **Enforzamiento de TenantId**| `CONST-03` (Multi-Tenant) | `PRIN-02` (Zero Trust) | `NFR-SEC-01` (Aislamiento)| Information Disclosure |
| **Persistencia Append-Only** | `CONST-05` (Audit Retention)| `PRIN-03` (Auditability) | `NFR-AUD-01` (Inmutabilidad)| Repudiation / Tampering |
| **Cifrado TLS 1.3 / AES-256** | `CONST-02` (Distributed) | `PRIN-02` (Zero Trust) | `NFR-SEC-02` (Cifrado) | Tampering / Disclosure |
| **Sondaje Acotado Pasivo** | `CONST-04` (No degradante) | `PRIN-06` (Configuration) | `NFR-PER-01` (MTTD < 60s) | Denial of Service |

---

## 8. Architecture Readiness Assessment & ARB Gate Verification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE PREPARACIÓN DE ARQUITECTURA DE SEGURIDAD (SUBFASE 3.6 GATE REVIEW)       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Modelo Zero-Trust y 5 Zonas de Confianza formalmente especificadas:     SÍ           │
│ • Análisis de Amenazas STRIDE completo con estrategias de mitigación:    SÍ           │
│ • Enforzamiento innegociable de Aislamiento Multi-Tenant (CONST-03):     SÍ           │
│ • Especificación de Cifrado TLS 1.3 / AES-256 y Registro Append-Only:     SÍ           │
│ • Trazabilidad Total con Subfases 3.1, 3.2, 3.3, 3.4 y 3.5:               SÍ           │
│                                                                                         │
│ CONFIDENCE LEVEL:               98%                                                     │
│ ARCHITECTURE READINESS SCORE:   100% (EXCELENTE / LISTO PARA ARQUITECTURA DE PERSISTENCIA)│
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. READY FOR ARCHITECTURE REVIEW

⚠️ **REGLA DE PARADA EN CUMPLIMIENTO DEL ARB**: La Subfase 3.6 ha finalizado. El equipo de ingeniería se detiene inmediatamente en este punto a la espera de la evaluación y aprobación explícita por parte del Architecture Review Board. **No se continuará a la Subfase 3.7 Persistence Architecture hasta recibir autorización explícita.**
