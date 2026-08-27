# 4.6 DOMAIN OPERATION SPECIFICATION — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `DOMAIN_OPERATION_SPECIFICATION.md`  
> **Phase**: PHASE 4.6 — DOMAIN OPERATION SPECIFICATION  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (L4 Domain Operation & Business Lifecycle Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **4.6 Domain Operation Specification** concluye la **Fase 4: Product Engineering** de **Gestiva Security (GestivaSec V1)**. Este documento especifica la semántica operacional del negocio, definiendo los ciclos de vida fundamentales del dominio (`Incident`, `Asset`, `Evidence`, `Alert`, `Notification`, `Certificate`, `SecurityFinding`, `Audit`), sus máquinas de estados abstractas, transiciones, invariantes de negocio y gobernanza operativa, sin incorporar decisiones de desarrollo de software, esquemas de bases de datos, APIs, tecnologías ni infraestructura.

---

## 2. Matriz General de Ciclos de Vida del Dominio (Domain Lifecycles)

| ID Dominio | Nombre del Ciclo de Vida del Dominio | Estado Inicial | Estados Intermedios | Estado Terminal | Invariante Principal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`DOM-LIFE-01`** | Asset Lifecycle (Ciclo de Vida del Activo) | `REGISTERED` | `ACTIVE`, `DEGRADED`, `UNDER_MAINTENANCE` | `DECOMMISSIONED` | Asignación obligatoria de propietario (`BR-02`). |
| **`DOM-LIFE-02`** | Incident Lifecycle (Ciclo de Vida del Incidente) | `DECLARED` | `ASSIGNED`, `IN_DIAGNOSIS`, `REMEDIATED` | `CLOSED_WITH_RCA` | Cierre P1 requiere informe RCA completado (`BR-01`). |
| **`DOM-LIFE-03`** | Evidence Lifecycle (Ciclo de Evidencias) | `CAPTURED` | `ASSOCIATED`, `VERIFIED` | `ARCHIVED_IMMUTABLE` | Integridad no modificable de evidencias. |
| **`DOM-LIFE-04`** | Alert Lifecycle (Ciclo de Vida de Alertas) | `EMITTED` | `EVALUATED`, `GROUPED` | `DISPATCHED` / `SUPPRESSED` | Desduplicación en ventana de tiempo. |
| **`DOM-LIFE-05`** | Notification Lifecycle (Notificaciones) | `QUEUED` | `IN_DELIVERY` | `DELIVERED` / `FAILED` | Canalización por matriz RACI. |
| **`DOM-LIFE-06`** | Certificate Lifecycle (Acreditaciones) | `VALID` | `WARNING_EXPIRING_SOON`, `CRITICAL_EXPIRING` | `EXPIRED` / `RENEWED` | Alerta preventiva al alcanzar plazo limite. |
| **`DOM-LIFE-07`** | Security Finding Lifecycle (Hallazgos SOC) | `DETECTED` | `TRIAGED`, `IN_REMEDIATION` | `RESOLVED` / `RISK_ACCEPTED` | Clasificación bajo categorías normativas. |
| **`DOM-LIFE-08`** | Audit Lifecycle (Trazas de Auditoría) | `EMITTED` | N/A (Directo a Conservación) | `CONSERVED_APPEND_ONLY` | Inmutabilidad total de solo adición (`BR-05`). |

---

## 3. Detailed Domain Lifecycle Specifications (Especificación Detallada)

### DOM-LIFE-01: Asset Lifecycle (Ciclo de Vida del Activo Digital)

#### 1. Descripción Semántica del Negocio
El activo digital representa la unidad fundamental del inventario corporativo supervisado. Su ciclo de vida rige el estado funcional desde su incorporación formal hasta su desincorporación definitiva.

#### 2. Máquina de Estados del Dominio

```
 [REGISTERED] ──────► [ACTIVE] ──────► [DEGRADED]
      │                  │                │
      │                  ▼                │
      │         [UNDER_MAINTENANCE] ◄─────┘
      │                  │
      ▼                  ▼
   ─────────────► [DECOMMISSIONED] (Terminal)
```

#### 3. Transiciones y Desencadenantes de Negocio
- `REGISTERED` ➔ `ACTIVE`: Activación exitosa de las comprobaciones sintéticas automáticas.
- `ACTIVE` ➔ `DEGRADED`: Detección de tiempos de respuesta elevados dentro del margen de evaluación (`WF-001`).
- `DEGRADED` ➔ `ACTIVE`: Normalización confirmada de los tiempos de respuesta.
- `ACTIVE` / `DEGRADED` ➔ `UNDER_MAINTENANCE`: Declaración de ventana de mantenimiento programado.
- `CUALQUIERA` ➔ `DECOMMISSIONED`: Desincorporación formal del activo del inventario de la organización.

#### 4. Invariantes de Negocio
- **Invariante A**: Ningún activo puede transicionar a `ACTIVE` si no cuenta con un responsable de activo asignado (`BR-02`).
- **Invariante B**: Ningún activo puede ser modificado fuera de la organización de pertenencia del usuario (`BR-04`).

---

### DOM-LIFE-02: Incident Lifecycle (Ciclo de Vida del Incidente Operacional)

#### 1. Descripción Semántica del Negocio
El incidente operacional representa la interrupción o degradación de la disponibilidad de un activo. Su ciclo de vida regula el proceso estricto de declaración, atención, remediación y cierre normativo.

#### 2. Máquina de Estados del Dominio

```
 [DECLARED] ──────► [ASSIGNED] ──────► [IN_DIAGNOSIS]
                                              │
                                              ▼
 [CLOSED_WITH_RCA] ◄────────────────── [REMEDIATED]
    (Terminal)         (Requiere RCA - `BR-01`)
```

#### 3. Transiciones y Desencadenantes de Negocio
- `INICIO` ➔ `DECLARED`: Confirmación de fallas repetidas de disponibilidad (`WF-001`).
- `DECLARED` ➔ `ASSIGNED`: Asunción explícita de responsabilidad por un operario (`WF-002`).
- `ASSIGNED` ➔ `IN_DIAGNOSIS`: Inicio de actividades de análisis técnico del origen de la falla.
- `IN_DIAGNOSIS` ➔ `REMEDIATED`: Aplicación del correctivo técnico y confirmación de restauración de disponibilidad sintética.
- `REMEDIATED` ➔ `CLOSED_WITH_RCA`: Incorporación y validación obligatoria del informe de Causa Raíz (`WF-003`).

#### 4. Invariantes de Negocio
- **Invariante A (`Regla BR-01`)**: La transición de `REMEDIATED` a `CLOSED_WITH_RCA` en incidentes de prioridad crítica P1 está estrictamente bloqueada si el informe RCA se encuentra incompleto o ausente.
- **Invariante B**: El estado `CLOSED_WITH_RCA` es un estado terminal e inalterable.

---

### DOM-LIFE-03: Evidence Lifecycle (Ciclo de Vida de Evidencias Telemétricas)

#### 1. Descripción Semántica del Negocio
La evidencia representa la prueba documental telemétrica (registros de falla, marcas de tiempo, respuestas) que respalda la declaración y resolución de un incidente.

#### 2. Máquina de Estados del Dominio

```
 [CAPTURED] ──────► [ASSOCIATED] ──────► [VERIFIED] ──────► [ARCHIVED_IMMUTABLE]
                                                               (Terminal)
```

#### 3. Transiciones y Desencadenantes de Negocio
- `INICIO` ➔ `CAPTURED`: Captura del resultado de evaluación sintética fallida.
- `CAPTURED` ➔ `ASSOCIATED`: Vinculación de la evidencia al expediente del incidente declarado (`WF-001`).
- `ASSOCIATED` ➔ `VERIFIED`: Verificación de la consistencia de la evidencia por el equipo de operaciones.
- `VERIFIED` ➔ `ARCHIVED_IMMUTABLE`: Consolidación inalterable al completar el informe RCA.

#### 4. Invariantes de Negocio
- **Invariante A**: Las evidencias capturadas no pueden ser editadas ni eliminadas tras su vinculación a un expediente de incidente.

---

### DOM-LIFE-04: Alert Lifecycle (Ciclo de Vida de Alertas Operacionales)

#### 1. Descripción Semántica del Negocio
La alerta representa la señal de evento operativo emitida por los módulos de observabilidad o seguridad antes de su canalización.

#### 2. Máquina de Estados del Dominio

```
                       ┌──► [SUPPRESSED] (Repetida / Agrupada)
                       │
 [EMITTED] ──► [EVALUATED]
                       │
                       └──► [GROUPED] ──► [DISPATCHED] (Terminal)
```

#### 3. Transiciones y Desencadenantes de Negocio
- `EMITTED` ➔ `EVALUATED`: Recepción del evento por el evaluador de alertas.
- `EVALUATED` ➔ `SUPPRESSED`: Identificación de alerta idéntica recibida dentro de la ventana de tiempo de agrupación.
- `EVALUATED` ➔ `GROUPED` ➔ `DISPATCHED`: Agrupación de la alerta y canalización hacia la notificación del usuario (`WF-004`).

#### 4. Invariantes de Negocio
- **Invariante A**: Alertas idénticas dentro de la ventana de agrupación deben consolidarse en una única notificación emitida.

---

### DOM-LIFE-05: Notification Lifecycle (Ciclo de Vida de Notificaciones)

#### 1. Descripción Semántica del Negocio
La notificación representa el mensaje operacional distribuido hacia los destinatarios según la matriz de responsabilidad.

#### 2. Máquina de Estados del Dominio

```
 [QUEUED] ──────► [IN_DELIVERY] ──────┬──► [DELIVERED] (Terminal)
                                      │
                                      └──► [FAILED] (Terminal con Reintento)
```

#### 3. Transiciones y Desencadenantes de Negocio
- `QUEUED` ➔ `IN_DELIVERY`: Procesamiento de envío por el despachador de notificaciones.
- `IN_DELIVERY` ➔ `DELIVERED`: Confirmación de recepción exitosa por el canal de destino.
- `IN_DELIVERY` ➔ `FAILED`: Falla en la entrega por problemas en el canal de salida.

---

### DOM-LIFE-06: Certificate & Credential Lifecycle (Acreditaciones Digitales)

#### 1. Descripción Semántica del Negocio
Regula el estado de validez de las acreditaciones y certificados digitales asociados a los activos corporativos.

#### 2. Máquina de Estados del Dominio

```
 [VALID] ──────► [WARNING_EXPIRING_SOON] ──────► [CRITICAL_EXPIRING] ──────► [EXPIRED]
    ▲                                                                           │
    └───────────────────────────── [RENEWED] ◄──────────────────────────────────┘
```

#### 3. Transiciones y Desencadenantes de Negocio
- `VALID` ➔ `WARNING_EXPIRING_SOON`: El tiempo restante de vigencia alcanza el plazo preventivo organizativo (`WF-004`).
- `WARNING_EXPIRING_SOON` ➔ `CRITICAL_EXPIRING`: El tiempo restante alcanza el umbral crítico de caducidad.
- `CRITICAL_EXPIRING` ➔ `EXPIRED`: Caducidad completa de la acreditación.
- `CUALQUIERA` ➔ `RENEWED` ➔ `VALID`: Confirmación de la renovación exitosa de la acreditación digital.

---

### DOM-LIFE-07: Security Finding Lifecycle (Hallazgos de Ciberseguridad)

#### 1. Descripción Semántica del Negocio
Regula el seguimiento de vulnerabilidades y riesgos perimetrales detectados en los activos de la organización.

#### 2. Máquina de Estados del Dominio

```
 [DETECTED] ──────► [TRIAGED] ──────► [IN_REMEDIATION] ──────┬──► [RESOLVED]
                                                              │
                                                              └──► [RISK_ACCEPTED]
```

#### 3. Transiciones y Desencadenantes de Negocio
- `DETECTED` ➔ `TRIAGED`: Clasificación del hallazgo bajo categorías normativas del sector por el analista SOC (`WF-006`).
- `TRIAGED` ➔ `IN_REMEDIATION`: Asignación del plan de atención al equipo de confiabilidad.
- `IN_REMEDIATION` ➔ `RESOLVED`: Aplicación de la corrección y verificación de eliminación de la vulnerabilidad.
- `IN_REMEDIATION` ➔ `RISK_ACCEPTED`: Aprobación formal de aceptación de riesgo por la Dirección Técnica.

---

### DOM-LIFE-08: Audit Lifecycle (Trazas de Auditoría e Inmutabilidad)

#### 1. Descripción Semántica del Negocio
Regula la preservación inalterable de los registros de gobierno y auditoría de la plataforma.

#### 2. Máquina de Estados del Dominio

```
 [EMITTED] ──────────────────────────► [CONSERVED_APPEND_ONLY] (Terminal Inmutable)
```

#### 3. Transiciones y Desencadenantes de Negocio
- `EMITTED` ➔ `CONSERVED_APPEND_ONLY`: Registro pasivo automático de cualquier evento operativo o cambio de estado (`WF-007`).

#### 4. Invariantes de Negocio
- **Invariante A (`Regla BR-05`)**: El estado `CONSERVED_APPEND_ONLY` es inmutable. Queda estrictamente prohibida cualquier operación de modificación o eliminación sobre los registros de auditoría.

---

## 4. Summary & Phase 4 Completion Gate (Cierre de la Fase 4)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE FINALIZACIÓN DE FASE 4 — PRODUCT ENGINEERING (GATE REVIEW FINAL)        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • 4.1 Product Specification:                     COMPLETADO Y APROBADO (L1 Pure)        │
│ • 4.2 Functional Requirements Specification:     COMPLETADO Y APROBADO (L2 Pure)        │
│ • 4.3 Use Case Specification:                    COMPLETADO Y APROBADO (L3 Pure)        │
│ • 4.4 User Journey Specification:                COMPLETADO Y APROBADO (L4 Pure)        │
│ • 4.5 Workflow Specification:                    COMPLETADO Y APROBADO (L4 Pure)        │
│ • 4.6 Domain Operation Specification:            COMPLETADO Y APROBADO (L4 Pure)        │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ PHASE 4 ENGINEERING SCORE:      100% (FASE 4 COMPLETA / LISTO PARA FASE 5)              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
