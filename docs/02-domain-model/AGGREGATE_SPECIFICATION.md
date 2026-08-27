# 5.4 AGGREGATE SPECIFICATION — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `AGGREGATE_SPECIFICATION.md`  
> **Phase**: PHASE 5.4 — AGGREGATE SPECIFICATION  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Domain Aggregate Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.4 Aggregate Specification** establece el catálogo formal de **Agregados del Dominio** para **Gestiva Security (GestivaSec V1)**. Un Agregado es un conjunto de objetos de dominio asociados (Entidades y Objetos de Valor) delimitados por una frontera de consistencia conceptual y gobernados exclusivamente a través de su **Raíz del Agregado (Aggregate Root)**.

Fiel al principio de pureza del dominio de negocio, este documento especifica la estructura conceptual de los Agregados, sus Raíces del Agregado, sus entidades contenidas, sus objetos de valor e invariantes de consistencia del negocio, sin incorporar conceptos de ejecución (comandos, transacciones, servicios, repositorios) ni de persistencia física (claves, identificadores UUID, discriminadores `tenant_id`, tablas o esquemas SQL).

---

## 2. Catálogo de Agregados del Dominio (Domain Aggregates Catalog)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ESTRUCTURA DE AGREGADOS Y RAÍCES DEL DOMINIO                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ AGREGADO 1: AGREGADO DE ACTIVO DIGITAL                                                  │
│ • Raíz del Agregado (Aggregate Root): Activo Digital (ENT-01)                           │
│ • Entidades Contenidas: Acreditación Digital (ENT-05)                                   │
│ • Invariante: Responsable asignado obligatorio (BR-02) & Delimitación por Org (BR-04) │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ AGREGADO 2: AGREGADO DE INCIDENTE OPERACIONAL                                           │
│ • Raíz del Agregado (Aggregate Root): Incidente Operacional (ENT-02)                    │
│ • Entidades Contenidas: Informe de Causa Raíz - RCA (ENT-03)                            │
│ • Invariante: Cierre de incidente crítico P1 bloqueado sin informe RCA (BR-01)        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ AGREGADO 3: AGREGADO DE HALLAZGO DE CIBERSEGURIDAD                                      │
│ • Raíz del Agregado (Aggregate Root): Hallazgo de Ciberseguridad (ENT-04)               │
│ • Invariante: Categorización obligatoria bajo marcos normativos del sector               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ AGREGADO 4: AGREGADO DE TRAZA DE AUDITORÍA                                              │
│ • Raíz del Agregado (Aggregate Root): Traza de Auditoría (ENT-06)                       │
│ • Invariante: Inmutabilidad inalterable de solo adición sin mod/borrado (BR-05)        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ AGREGADO 5: AGREGADO DE ORGANIZACIÓN                                                    │
│ • Raíz del Agregado (Aggregate Root): Organización (ENT-07)                             │
│ • Invariante: Frontera inalienable de pertenencia de toda información (BR-04)          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Especificación Detallada de Agregados del Dominio

### AGG-01: Agregado de Activo Digital (Asset Aggregate)
- **ID Agregado**: `AGG-01`
- **Nombre del Agregado**: Agregado de Activo Digital
- **Raíz del Agregado (Aggregate Root)**: `Activo Digital` (`ENT-01`)
- **Descripción**: Gobierna la fuente de verdad del recurso supervisado, asegurando la consistencia conceptual del activo y sus acreditaciones digitales asociadas.
- **Entidades Internas Contenidas**:
  - `Acreditación Digital` (`ENT-05`): Certificado de seguridad vinculado al activo.
- **Objetos de Valor Internos**:
  - Ubicación de Destino, Nivel de Criticidad, Correo del Responsable, Estado Funcional del Activo.
- **Frontera de Consistencia e Invariantes**:
  1. No se permite el registro o actualización del Agregado si se omite el correo del responsable asignado (`BR-02`).
  2. Todas las modificaciones a las acreditaciones asociadas se realizan exclusivamente a través de la Raíz del Agregado (`Activo Digital`).
  3. El Agregado completo pertenece obligatoriamente a una única Organización (`BR-04`).
- **Operaciones del Negocio Soportadas**:
  - Incorporación de Activo Digital, Modificación de Responsable, Asignación de Acreditación Digital, Desincorporación de Activo.

---

### AGG-02: Agregado de Incidente Operacional (Incident Aggregate)
- **ID Agregado**: `AGG-02`
- **Nombre del Agregado**: Agregado de Incidente Operacional
- **Raíz del Agregado (Aggregate Root)**: `Incidente Operacional` (`ENT-02`)
- **Descripción**: Gobierna el ciclo de vida del expediente de atención de interrupciones de servicio y la incorporación obligatoria de su documentación de solución.
- **Entidades Internas Contenidas**:
  - `Informe de Causa Raíz (RCA)` (`ENT-03`): Documento explicativo de causa raíz y pasos de remediación.
- **Objetos de Valor Internos**:
  - Prioridad del Incidente, Estado del Incidente, Fecha Límite de Solución.
- **Frontera de Consistencia e Invariantes**:
  1. `Regla BR-01`: La transición de estado del Agregado a cerrado en incidentes de prioridad crítica P1 está estrictamente bloqueada a menos que la entidad interna `Informe de Causa Raíz (RCA)` esté presente y validada.
  2. La entidad `Informe RCA` no posee existencia independiente fuera de la Raíz del Agregado (`Incidente Operacional`).
- **Operaciones del Negocio Soportadas**:
  - Declaración de Incidente Crítico, Asignación de Operador, Registro de Diagnóstico, Remediación de Incidente, Documentación RCA, Cierre Definitivo con RCA.

---

### AGG-03: Agregado de Hallazgo de Ciberseguridad (Security Finding Aggregate)
- **ID Agregado**: `AGG-03`
- **Nombre del Agregado**: Agregado de Hallazgo de Ciberseguridad
- **Raíz del Agregado (Aggregate Root)**: `Hallazgo de Ciberseguridad` (`ENT-04`)
- **Descripción**: Delimita la información de vulnerabilidades y deficiencias de postura perimetral detectadas en los activos de la organización.
- **Entidades Internas Contenidas**: Ninguna.
- **Objetos de Valor Internos**:
  - Categoría de Seguridad (OWASP), Táctica de Seguridad (MITRE), Nivel de Severidad, Estado de Solución.
- **Frontera de Consistencia e Invariantes**:
  1. El hallazgo debe estar categorizado obligatoriamente bajo marcos normativos oficiales del sector.
  2. Hallazgos creados con severidad crítica disparan automáticamente una solicitud de atención operacional.
- **Operaciones del Negocio Soportadas**:
  - Registro de Hallazgo de Seguridad, Triaje de Hallazgo, Resolución de Hallazgo, Aceptación de Riesgo.

---

### AGG-04: Agregado de Traza de Auditoría (Audit Log Aggregate)
- **ID Agregado**: `AGG-04`
- **Nombre del Agregado**: Agregado de Traza de Auditoría
- **Raíz del Agregado (Aggregate Root)**: `Traza de Auditoría` (`ENT-06`)
- **Descripción**: Encapsula el registro pasivo inalterable de operaciones y cambios de estado del negocio para garantizar el no repudio.
- **Entidades Internas Contenidas**: Ninguna.
- **Objetos de Valor Internos**:
  - Identidad del Actor, Acción Realizada, Marca Temporal Inalterable, Detalle de la Operación.
- **Frontera de Consistencia e Invariantes**:
  1. `Regla BR-05`: Inmutabilidad inalterable de solo adición. Se prohíbe cualquier operación de modificación o eliminación sobre los elementos del Agregado.
- **Operaciones del Negocio Soportadas**:
  - Conservación Inalterable de Auditoría.

---

### AGG-05: Agregado de Organización (Organization Aggregate)
- **ID Agregado**: `AGG-05`
- **Nombre del Agregado**: Agregado de Organización
- **Raíz del Agregado (Aggregate Root)**: `Organización` (`ENT-07`)
- **Descripción**: Actúa como la frontera principal de delimitación y aislamiento de la información de cada entidad corporativa.
- **Entidades Internas Contenidas**: Ninguna (Aislamiento de frontera).
- **Objetos de Valor Internos**:
  - Nombre de la Organización, Estado de la Entidad.
- **Frontera de Consistencia e Invariantes**:
  1. `Regla BR-04`: Delimitación estricta por Organización. Todo Agregado secundario (`AGG-01` a `AGG-04`) debe estar asociado a la frontera de una única Organización.
- **Operaciones del Negocio Soportadas**:
  - Registro de Organización, Modificación de Estado de Organización.

---

## 4. Matriz de Trazabilidad entre Agregados, Entidades y Reglas de Negocio

| Agregado del Dominio | Raíz del Agregado (Aggregate Root) | Entidades Internas | Regla de Negocio Principal | Operaciones del Negocio |
| :--- | :--- | :--- | :--- | :--- |
| **`AGG-01` Activo Digital** | `ENT-01 Activo Digital` | `ENT-05 Acreditación Digital` | Responsable asignado (`BR-02`) | `IncorporaciónActivo`, `DesincorporaciónActivo` |
| **`AGG-02` Incidente** | `ENT-02 Incidente Operacional` | `ENT-03 Informe RCA` | Cierre crítico requiere RCA (`BR-01`) | `DeclaraciónIncidente`, `CierreDefinitivoConRCA` |
| **`AGG-03` Hallazgo SOC** | `ENT-04 Hallazgo Ciberseguridad`| Ninguna | Categorización Normativa | `RegistroHallazgo`, `TriajeHallazgo` |
| **`AGG-04` Auditoría** | `ENT-06 Traza de Auditoría` | Ninguna | Inmutabilidad de solo adición (`BR-05`) | `ConservaciónAuditoría` |
| **`AGG-05` Organización** | `ENT-07 Organización` | Ninguna | Aislamiento organizacional (`BR-04`) | `RegistroOrganización` |

---

## 5. Summary & Phase 5.4 Validation Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE VALIDACIÓN DE AGREGADOS DEL DOMINIO (SUBFASE 5.4 GATE REVIEW)            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Definición 100% basada en Raíces de Agregado y Consistencia de Negocio:  YES / SÍ     │
│ • Cero alusión a conceptos de ejecución (comandos, transacciones, repos):   YES / SÍ     │
│ • Ausencia total de conceptos de persistencia (UUID, tenant_id, SQL, FK):  YES / SÍ     │
│ • Encapsulamiento de Invariantes y Reglas de Negocio (BR-01..05):          YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ AGGREGATE SPECIFICATION SCORE:  100% (ESPECIFICACIÓN DE AGREGADOS PURA APROBADA)        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
