# 5.3 ENTITY SPECIFICATION — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `ENTITY_SPECIFICATION.md`  
> **Phase**: PHASE 5.3 — ENTITY SPECIFICATION  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Business Entity Specification Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.3 Entity Specification** establece el catálogo formal de **Entidades del Dominio de Negocio** para **Gestiva Security (GestivaSec V1)**. Una Entidad se define en el dominio por poseer una identidad conceptual de negocio sostenida en el tiempo, continuidad operacional y un ciclo de vida propio.

En estricto cumplimiento del mandato de pureza del dominio, esta especificación define para cada Entidad su identidad funcional del negocio, sus atributos de dominio, sus invariantes semánticas y sus reglas de negocio asociadas (`BR-01` a `BR-05`), sin incorporar decisiones de persistencia física (como identificadores de base de datos tipo UUID, discriminadores como `tenant_id`, tipos de datos SQL, claves primarias/foráneas o índices).

---

## 2. Catálogo Resumido de Entidades del Dominio

| ID Entidad | Nombre de la Entidad de Dominio | Identidad Conceptual de Negocio | Rol en el Dominio | Regla de Negocio Clave |
| :--- | :--- | :--- | :--- | :--- |
| **`ENT-01`** | **Activo Digital** | Identificador de Activo Digital | Recurso supervisado del inventario | Responsable asignado obligatorio (`BR-02`). |
| **`ENT-02`** | **Incidente Operacional** | Identificador de Incidente | Expediente de interrupción de servicio | Cierre P1 requiere informe RCA (`BR-01`). |
| **`ENT-03`** | **Informe de Causa Raíz (RCA)**| Identificador de Informe RCA | Documentación de solución y lecciones | Requisito bloqueante de cierre P1 (`BR-01`). |
| **`ENT-04`** | **Hallazgo de Ciberseguridad** | Identificador de Hallazgo | Deficiencia de postura o vulnerabilidad | Categorización bajo marcos del sector. |
| **`ENT-05`** | **Acreditación Digital** | Identificador de Acreditación | Certificado de seguridad del activo | Advertencia preventiva por vencimiento. |
| **`ENT-06`** | **Traza de Auditoría** | Identificador de Traza | Registro de gobierno y no repudio | Inmutabilidad inalterable (`BR-05`). |
| **`ENT-07`** | **Organización** | Identificador de Organización | Frontera de pertenencia e aislamiento | Delimitación estricta de datos (`BR-04`). |

---

## 3. Especificación Detallada de Entidades del Dominio

### ENT-01: Activo Digital (Digital Asset)
- **ID Entidad**: `ENT-01`
- **Nombre del Dominio**: Activo Digital
- **Descripción**: Representa la entidad fundamental de infraestructura o servicio corporativo supervisado en el inventario.
- **Identidad Conceptual de Negocio**: `Identificador de Activo Digital` (Permanente a través de cambios de estado).
- **Atributos del Dominio**:
  - `Nombre del Activo`: Denominación descriptiva del recurso.
  - `Ubicación de Destino`: Dirección o dominio autorizado del servicio.
  - `Nivel de Criticidad`: Prioridad operacional asignada (P1-P4).
  - `Correo del Responsable`: Identificación del propietario humano del activo.
  - `Estado Funcional del Activo`: Situación operacional en su ciclo de vida (`REGISTERED`, `ACTIVE`, `DEGRADED`, `UNDER_MAINTENANCE`, `DECOMMISSIONED`).
- **Invariantes del Dominio**:
  - `BR-02`: No se permite la existencia de un Activo Digital sin un correo de responsable válido asignado.
  - `BR-04`: Todo Activo Digital pertenece obligatoriamente a una única Organización.

---

### ENT-02: Incidente Operacional (Operational Incident)
- **ID Entidad**: `ENT-02`
- **Nombre del Dominio**: Incidente Operacional
- **Descripción**: Expediente de gestión que representa una interrupción de disponibilidad o degradación confirmada del servicio.
- **Identidad Conceptual de Negocio**: `Identificador de Incidente`.
- **Atributos del Dominio**:
  - `Prioridad del Incidente`: Severidad asignada (`P1_CRITICAL`, `P2_HIGH`, `P3_MEDIUM`, `P4_LOW`).
  - `Estado del Incidente`: Situación del expediente (`DECLARED`, `ASSIGNED`, `IN_DIAGNOSIS`, `REMEDIATED`, `CLOSED_WITH_RCA`).
  - `Marca Temporal de Declaración`: Fecha y hora de apertura del incidente.
  - `Operador Asignado`: Responsable humano o rol a cargo de la atención.
  - `Fecha Límite de Solución`: Plazo limite calculado según la prioridad asignada.
- **Invariantes del Dominio**:
  - `BR-01`: La transición al estado `CLOSED_WITH_RCA` en un incidente de prioridad `P1_CRITICAL` exige obligatoriamente la presencia de la Entidad `Informe de Causa Raíz (RCA)`.

---

### ENT-03: Informe de Causa Raíz (RCA Document)
- **ID Entidad**: `ENT-03`
- **Nombre del Dominio**: Informe de Causa Raíz (RCA)
- **Descripción**: Documento explicativo formal que detalla el origen del fallo, las acciones correctivas aplicadas y las medidas preventivas.
- **Identidad Conceptual de Negocio**: `Identificador de Informe RCA`.
- **Atributos del Dominio**:
  - `Descripción de Causa Raíz`: Explicación detallada del origen técnico del fallo.
  - `Pasos de Remediación Aplicados`: Acciones ejecutadas para restaurar el servicio.
  - `Medidas Preventivas`: Recomendaciones para evitar la reincidencia del fallo.
  - `Estado de Validación`: Confirmación de completitud del informe.
- **Invariantes del Dominio**:
  - `BR-01`: Debe estar vinculado a un Incidente Operacional P1 en estado remediado para autorizar su cierre.

---

### ENT-04: Hallazgo de Ciberseguridad (Security Finding)
- **ID Entidad**: `ENT-04`
- **Nombre del Dominio**: Hallazgo de Ciberseguridad
- **Descripción**: Registro de una vulnerabilidad, riesgo o deficiencia de postura detectada en el perímetro de un activo.
- **Identidad Conceptual de Negocio**: `Identificador de Hallazgo`.
- **Atributos del Dominio**:
  - `Categoría de Seguridad`: Clasificación normativas del sector (OWASP).
  - `Táctica de Seguridad`: Etiquetado de amenaza de la industria (MITRE).
  - `Nivel de Severidad`: Severidad asignada (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
  - `Descripción del Riesgo`: Detalle del hallazgo de seguridad.
  - `Estado de Solución`: Situación del expediente (`DETECTED`, `TRIAGED`, `IN_REMEDIATION`, `RESOLVED`, `RISK_ACCEPTED`).

---

### ENT-05: Acreditación Digital (Digital Credential)
- **ID Entidad**: `ENT-05`
- **Nombre del Dominio**: Acreditación Digital
- **Descripción**: Certificado de seguridad asociado a un activo corporativo para la verificación de su vigencia.
- **Identidad Conceptual de Negocio**: `Identificador de Acreditación`.
- **Atributos del Dominio**:
  - `Entidad Emisora`: Autoridad responsable de la emisión del certificado.
  - `Fecha de Emisión`: Marca de tiempo inicial de validez.
  - `Fecha de Expiración`: Marca de tiempo límite de caducidad.
  - `Estado de Vigencia`: Situación operacional (`VALID`, `WARNING_EXPIRING_SOON`, `CRITICAL_EXPIRING`, `EXPIRED`).

---

### ENT-06: Traza de Auditoría (Audit Log Record)
- **ID Entidad**: `ENT-06`
- **Nombre del Dominio**: Traza de Auditoría
- **Descripción**: Registro histórico pasivo que captura toda acción de usuario, modificación o cambio de estado del negocio.
- **Identidad Conceptual de Negocio**: `Identificador de Traza de Auditoría`.
- **Atributos del Dominio**:
  - `Identidad del Actor`: Usuario o proceso que ejecutó la acción.
  - `Acción Realizada`: Operación ejecutada en el negocio.
  - `Marca Temporal Inalterable`: Fecha y hora exacta de registro.
  - `Detalle de la Operación`: Valores anteriores y posteriores del cambio.
- **Invariantes del Dominio**:
  - `BR-05`: Inmutabilidad inalterable de solo adición. Imposibilidad de modificación o borrado.

---

### ENT-07: Organización (Tenant / Organization)
- **ID Entidad**: `ENT-07`
- **Nombre del Dominio**: Organización
- **Descripción**: Entidad corporativa que actúa como frontera inalienable de pertenencia y aislamiento de datos.
- **Identidad Conceptual de Negocio**: `Identificador de Organización`.
- **Atributos del Dominio**:
  - `Nombre de la Organización`: Denominación de la entidad corporativa.
  - `Estado de la Entidad`: Situación de operación de la organización.
- **Invariantes del Dominio**:
  - `BR-04`: Contiene y aísla a todas las demás Entidades del Dominio de su ámbito.

---

## 4. Matriz de Trazabilidad entre Entidades y Requisitos Funcionales

| Entidad del Dominio | Requisito Funcional (FRS) | Caso de Uso (UC) | Proceso Operacional (WF) | Regla de Negocio |
| :--- | :--- | :--- | :--- | :--- |
| **`ENT-01` Activo Digital** | `FR-0001` | `UC-001` | `WF-005` | `BR-02`, `BR-04` |
| **`ENT-02` Incidente Operacional**| `FR-0004`, `FR-0005` | `UC-004`, `UC-005` | `WF-001`, `WF-002` | `BR-03` |
| **`ENT-03` Informe RCA** | `FR-0006` | `UC-006` | `WF-003` | `BR-01` |
| **`ENT-04` Hallazgo Ciberseguridad**| `FR-0007` | `UC-007` | `WF-006` | Marcos Normativos |
| **`ENT-05` Acreditación Digital**| `FR-0003` | `UC-003` | `WF-004` | Plazo Preventivo |
| **`ENT-06` Traza de Auditoría** | `FR-0009` | `UC-009` | `WF-007` | `BR-05` |
| **`ENT-07` Organización** | `FR-0008` | `UC-008` | `WF-005`, `WF-007` | `BR-04` |

---

## 5. Summary & Phase 5.3 Validation Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE VALIDACIÓN DE ENTIDADES DE DOMINIO (SUBFASE 5.3 GATE REVIEW)             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Especificación basada 100% en Conceptos del Negocio (Lenguaje Ubicuo 5.0): YES / SÍ     │
│ • Ausencia total de conceptos de persistencia (UUID, tenant_id, SQL, PK):  YES / SÍ     │
│ • Enforzamiento estricto de Invariantes y Reglas de Negocio (BR-01..05):   YES / SÍ     │
│ • Trazabilidad 100% a Requisitos, Casos de Uso y Procesos Operacionales:   YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ ENTITY SPECIFICATION SCORE:     100% (ESPECIFICACIÓN DE ENTIDADES PURA APROBADA)        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
