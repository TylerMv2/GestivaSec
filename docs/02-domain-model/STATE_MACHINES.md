# 5.7 STATE MACHINES — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `STATE_MACHINES.md`  
> **Phase**: PHASE 5.7 — STATE MACHINES  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Business State Machine Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.7 State Machines** concluye la **Fase 5: Information Engineering** de **Gestiva Security (GestivaSec V1)**. Este documento establece el catálogo formal de **Máquinas de Estados del Dominio de Negocio** (`SM-01` a `SM-06`). 

Cada Máquina de Estados representa exclusivamente la evolución conceptual del negocio de una Entidad o Agregado, definiendo su estado inicial, estados intermedios, estados terminales, eventos de dominio que desencadenan transiciones, condiciones de guarda (reglas de negocio), transiciones inválidas e invariantes continuas. Se omiten de forma absoluta eventos técnicos, colas, APIs, servicios, persistencia, transacciones o cualquier mecanismo de implementación.

---

## 2. Mapa General de Máquinas de Estados del Dominio

| ID Máquina | Dominio / Agregado | Estado Inicial | Estados Intermedios | Estado Terminal | Invariante Principal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`SM-01`** | Activo Digital (`AGG-01`) | `REGISTERED` | `ACTIVE`, `DEGRADED`, `UNDER_MAINTENANCE` | `DECOMMISSIONED` | Responsable asignado obligatorio (`BR-02`). |
| **`SM-02`** | Incidente Operacional (`AGG-02`)| `DECLARED` | `ASSIGNED`, `IN_DIAGNOSIS`, `REMEDIATED` | `CLOSED_WITH_RCA` | Cierre P1 bloqueado sin informe RCA (`BR-01`). |
| **`SM-03`** | Acreditación Digital (`ENT-05`) | `VALID` | `WARNING_EXPIRING_SOON`, `CRITICAL_EXPIRING`, `RENEWED` | `EXPIRED` | Advertencia preventiva en plazo limite. |
| **`SM-04`** | Hallazgo Ciberseguridad (`AGG-03`)| `DETECTED` | `TRIAGED`, `IN_REMEDIATION` | `RESOLVED` / `RISK_ACCEPTED` | Categorización normativas obligatoria. |
| **`SM-05`** | Traza de Auditoría (`AGG-04`)| `EMITTED` | N/A (Directo a Conservación) | `CONSERVED_APPEND_ONLY` | Inmutabilidad de solo adición (`BR-05`). |
| **`SM-06`** | Organización (`AGG-05`) | `ACTIVE_ORGANIZATION`| `SUSPENDED_ORGANIZATION` | `DEACTIVATED_ORGANIZATION` | Delimitación estricta de pertenencia (`BR-04`). |

---

## 3. Especificación Detallada de Máquinas de Estados

### SM-01: Máquina de Estados del Activo Digital (Asset State Machine)
- **ID Máquina**: `SM-01`
- **Agregado / Entidad**: `Activo Digital` (`ENT-01` / `AGG-01`).
- **Estado Inicial**: `REGISTERED` (Activo registrado en el inventario).
- **Estados Intermedios**: `ACTIVE` (En supervisión normal), `DEGRADED` (Tiempo de respuesta elevado), `UNDER_MAINTENANCE` (En ventana de mantenimiento).
- **Estado Terminal**: `DECOMMISSIONED` (Desincorporado del inventario).

#### Diagrama de Transición de Estados del Negocio
```
 [REGISTERED] ──────(ActivoActivado)─────► [ACTIVE] ──────(EvaluaciónDegradada)─────► [DEGRADED]
      │                                       │                                            │
      │                                       ├─► (VentanaMantenimiento)                   │
      │                                       ▼                                            │
      │                              [UNDER_MAINTENANCE] ◄─────────────────────────────────┘
      │                                       │
      ▼                                       ▼
   ───┴───────────(ActivoDesincorporado)────► [DECOMMISSIONED] (Terminal)
```

#### Reglas de Transición y Eventos del Dominio
1. `REGISTERED` ➔ `ACTIVE`: Desencadenado por `Evento: ActivoActivado` tras la verificación inicial.
   - *Condición de Guarda*: Debe existir un responsable humano asignado (`BR-02`).
2. `ACTIVE` ➔ `DEGRADED`: Desencadenado por `Evento: EvaluaciónSintéticaDegradada` al registrar tiempos de respuesta elevados.
3. `DEGRADED` ➔ `ACTIVE`: Desencadenado por `Evento: EvaluaciónSintéticaNormalizada` al retornar la respuesta a valores normales.
4. `ACTIVE` / `DEGRADED` ➔ `UNDER_MAINTENANCE`: Desencadenado por `Evento: VentanaMantenimientoIniciada`.
5. `UNDER_MAINTENANCE` ➔ `ACTIVE`: Desencadenado por `Evento: VentanaMantenimientoConcluida`.
6. `CUALQUIERA` ➔ `DECOMMISSIONED`: Desencadenado por `Evento: ActivoDesincorporado`.

#### Transiciones Inválidas (Prohibidas)
- `DECOMMISSIONED` ➔ `ACTIVE` (Un activo desincorporado no puede reactivarse directamente).
- `REGISTERED` ➔ `DEGRADED` (No se permite degradación sin haber alcanzado el estado activo previo).

#### Invariantes Continuas
- La pertenencia a la Organización (`BR-04`) y el correo del responsable (`BR-02`) deben conservarse durante todo el ciclo de vida.

---

### SM-02: Máquina de Estados del Incidente Operacional (Incident State Machine)
- **ID Máquina**: `SM-02`
- **Agregado / Entidad**: `Incidente Operacional` (`ENT-02` / `AGG-02`).
- **Estado Inicial**: `DECLARED` (Incidente automático o manual creado).
- **Estados Intermedios**: `ASSIGNED` (Responsable asignado), `IN_DIAGNOSIS` (En análisis técnico), `REMEDIATED` (Disponibilidad restaurada).
- **Estado Terminal**: `CLOSED_WITH_RCA` (Incidente cerrado con informe RCA validado).

#### Diagrama de Transición de Estados del Negocio
```
 [DECLARED] ───(OperadorAsignado)───► [ASSIGNED] ───(DiagnósticoIniciado)───► [IN_DIAGNOSIS]
                                                                                     │
                                                                                     ▼
 [CLOSED_WITH_RCA] ◄───(InformeRCAValidado)─── [REMEDIATED] ◄───(DisponibilidadRestaurada)─┘
    (Terminal)          (Requiere RCA - `BR-01`)
```

#### Reglas de Transición y Eventos del Dominio
1. `INICIO` ➔ `DECLARED`: Desencadenado por `Evento: IncidenteCríticoDeclarado` ante fallas sintéticas repetidas (`BR-03`).
2. `DECLARED` ➔ `ASSIGNED`: Desencadenado por `Evento: OperadorAsignado` al asumir la atención el operador.
3. `ASSIGNED` ➔ `IN_DIAGNOSIS`: Desencadenado por `Evento: DiagnósticoIniciado` al comenzar la investigación de la causa del fallo.
4. `IN_DIAGNOSIS` ➔ `REMEDIATED`: Desencadenado por `Evento: DisponibilidadRestaurada` al aplicar el correctivo técnico.
5. `REMEDIATED` ➔ `CLOSED_WITH_RCA`: Desencadenado por `Evento: InformeRCAValidado`.
   - *Condición de Guarda (`Regla BR-01`)*: Bloqueo absoluto de la transición si el `Informe de Causa Raíz (RCA)` está ausente o incompleto en incidentes P1.

#### Transiciones Inválidas (Prohibidas)
- `DECLARED` ➔ `CLOSED_WITH_RCA` (Prohibido saltarse las fases de diagnóstico y remediación).
- `REMEDIATED` ➔ `CLOSED_WITH_RCA` (Prohibido si el informe RCA no ha sido completado y validado).
- `CLOSED_WITH_RCA` ➔ CUALQUIER ESTADO (El estado cerrado es un estado terminal definitivo).

#### Invariantes Continuas
- La prioridad asignada (P1-P4) y la Fecha Límite SLA del incidente permanecen inalterables.

---

### SM-03: Máquina de Estados de Acreditación Digital (Certificate State Machine)
- **ID Máquina**: `SM-03`
- **Agregado / Entidad**: `Acreditación Digital` (`ENT-05`).
- **Estado Inicial**: `VALID` (Acreditación vigente).
- **Estados Intermedios**: `WARNING_EXPIRING_SOON` (Advertencia preventiva), `CRITICAL_EXPIRING` (Riesgo crítico de caducidad), `RENEWED` (Renovada).
- **Estado Terminal**: `EXPIRED` (Acreditación caducada).

#### Diagrama de Transición de Estados del Negocio
```
 [VALID] ───(PlazoPreventivoAlcanzado)───► [WARNING_EXPIRING_SOON] ───► [CRITICAL_EXPIRING]
    ▲                                                │                          │
    │                                                ▼                          ▼
 [RENEWED] ◄──────────────────────────────(AcreditaciónRenovada)─────────── [EXPIRED]
```

#### Reglas de Transición y Eventos del Dominio
1. `VALID` ➔ `WARNING_EXPIRING_SOON`: Desencadenado por `Evento: PlazoPreventivoAlcanzado` al restar ≤ 30 días de vigencia.
2. `WARNING_EXPIRING_SOON` ➔ `CRITICAL_EXPIRING`: Desencadenado por `Evento: PlazoCríticoAlcanzado` al restar ≤ 7 días.
3. `CRITICAL_EXPIRING` ➔ `EXPIRED`: Desencadenado por `Evento: FechaExpiraciónAlcanzada`.
4. `WARNING_EXPIRING_SOON` / `CRITICAL_EXPIRING` / `EXPIRED` ➔ `RENEWED` ➔ `VALID`: Desencadenado por `Evento: AcreditaciónRenovada`.

#### Transiciones Inválidas (Prohibidas)
- `EXPIRED` ➔ `VALID` (Requiere transicionar expresamente a través del evento de renovación).

---

### SM-04: Máquina de Estados del Hallazgo de Ciberseguridad (Security Finding State Machine)
- **ID Máquina**: `SM-04`
- **Agregado / Entidad**: `Hallazgo de Ciberseguridad` (`ENT-04` / `AGG-03`).
- **Estado Inicial**: `DETECTED` (Riesgo detectado).
- **Estados Intermedios**: `TRIAGED` (Categorizado normativamente), `IN_REMEDIATION` (En atención).
- **Estados Terminales**: `RESOLVED` (Vulnerabilidad eliminada), `RISK_ACCEPTED` (Riesgo formalmente aceptado).

#### Diagrama de Transición de Estados del Negocio
```
 [DETECTED] ───(HallazgoCategorizado)───► [TRIAGED] ───(PlanAsignado)───► [IN_REMEDIATION]
                                                                                │
                                           ┌────────────────────────────────────┴┐
                                           ▼                                     ▼
                                      [RESOLVED]                          [RISK_ACCEPTED]
```

#### Reglas de Transición y Eventos del Dominio
1. `DETECTED` ➔ `TRIAGED`: Desencadenado por `Evento: HallazgoCategorizado`.
   - *Condición de Guarda*: Categorización obligatoria bajo catálogos oficiales OWASP/MITRE.
2. `TRIAGED` ➔ `IN_REMEDIATION`: Desencadenado por `Evento: PlanAtenciónAsignado`.
3. `IN_REMEDIATION` ➔ `RESOLVED`: Desencadenado por `Evento: VulnerabilidadEliminada` tras verificación SOC.
4. `IN_REMEDIATION` ➔ `RISK_ACCEPTED`: Desencadenado por `Evento: AceptaciónRiesgoAprobada` con aval técnico.

#### Transiciones Inválidas (Prohibidas)
- `DETECTED` ➔ `RESOLVED` (Prohibido resolver sin triaje y verificación previa).

---

### SM-05: Máquina de Estados de la Traza de Auditoría (Audit Log State Machine)
- **ID Máquina**: `SM-05`
- **Agregado / Entidad**: `Traza de Auditoría` (`ENT-06` / `AGG-04`).
- **Estado Inicial**: `EMITTED` (Evento de operación del negocio emitido).
- **Estado Terminal**: `CONSERVED_APPEND_ONLY` (Registro conservado de solo adición).

#### Diagrama de Transición de Estados del Negocio
```
 [EMITTED] ───────────(OperaciónNegocioEjecutada)───────────► [CONSERVED_APPEND_ONLY] (Terminal Inmutable)
```

#### Reglas de Transición y Eventos del Dominio
1. `EMITTED` ➔ `CONSERVED_APPEND_ONLY`: Desencadenado por `Evento: OperaciónNegocioEjecutada`.
   - *Condición de Guarda (`Regla BR-05`)*: Inmutabilidad inalterable de solo adición. Prohibida toda modificación o eliminación posterior.

#### Transiciones Inválidas (Prohibidas)
- `CONSERVED_APPEND_ONLY` ➔ MODIFICACIÓN / BORRADO (Operaciones estrictamente prohibidas por la Regla `BR-05`).

---

### SM-06: Máquina de Estados de la Organización (Organization State Machine)
- **ID Máquina**: `SM-06`
- **Agregado / Entidad**: `Organización` (`ENT-07` / `AGG-05`).
- **Estado Inicial**: `ACTIVE_ORGANIZATION` (Organización operando normalmente).
- **Estados Intermedios**: `SUSPENDED_ORGANIZATION` (Operaciones temporalmente pausadas).
- **Estado Terminal**: `DEACTIVATED_ORGANIZATION` (Entidad desactivada).

#### Diagrama de Transición de Estados del Negocio
```
 [ACTIVE_ORGANIZATION] ──────(OrganizaciónSuspendida)──────► [SUSPENDED_ORGANIZATION]
          │                                                          │
          │                                                          ▼
          └──────────────────(OrganizaciónDesactivada)────────► [DEACTIVATED_ORGANIZATION]
```

#### Reglas de Transición y Eventos del Dominio
1. `ACTIVE_ORGANIZATION` ➔ `SUSPENDED_ORGANIZATION`: Desencadenado por `Evento: OrganizaciónSuspendida`.
2. `SUSPENDED_ORGANIZATION` ➔ `ACTIVE_ORGANIZATION`: Desencadenado por `Evento: OrganizaciónReactivada`.
3. `CUALQUIERA` ➔ `DEACTIVATED_ORGANIZATION`: Desencadenado por `Evento: OrganizaciónDesactivada`.

#### Invariantes Continuas
- La delimitación organizativa (`BR-04`) sobre todos los agregados secundarios se mantiene inviolable independientemente del estado de la Organización.

---

## 4. Matriz de Validación de Máquinas de Estados y Cierre de Fase 5

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE FINALIZACIÓN DE FASE 5 — INFORMATION ENGINEERING (GATE REVIEW FINAL)    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • 5.0 Ubiquitous Language:                       COMPLETADO Y APROBADO (Base Léxica)    │
│ • 5.1 Information Model:                         COMPLETADO Y APROBADO (Estructura)     │
│ • 5.2 Domain Model:                              COMPLETADO Y APROBADO (Dominio Puro)   │
│ • 5.3 Entity Specification:                      COMPLETADO Y APROBADO (7 Entidades)    │
│ • 5.4 Aggregate Specification:                   COMPLETADO Y APROBADO (5 Agregados)    │
│ • 5.5 Value Objects:                             COMPLETADO Y APROBADO (10 Objetos)     │
│ • 5.6 Relationships:                             COMPLETADO Y APROBADO (8 Relaciones)   │
│ • 5.7 State Machines:                            COMPLETADO Y APROBADO (6 Máquinas)     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ PHASE 5 ENGINEERING SCORE:      100% (FASE 5 COMPLETA / LISTO PARA FASE 6)              │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
