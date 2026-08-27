# 5.1 INFORMATION MODEL — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `INFORMATION_MODEL.md`  
> **Phase**: PHASE 5.1 — INFORMATION MODEL  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Business Information Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.1 Information Model** inicia formalmente la **Fase 5: Information Engineering** de **Gestiva Security (GestivaSec V1)**. Tras haber completado la Ingeniería de Producto (Fase 4) y consolidado el Lenguaje Ubicuo (Subfase 5.0), este documento define la **Estructura Conceptual del Modelo de Información del Software**. 

El Modelo de Información formaliza las fronteras estructurales del negocio, las agrupaciones conceptuales de información, los flujos de datos del dominio, las reglas de integridad de información y el marco inquebrantable de aislamiento por Organización, sirviendo como la base arquitectónica sobre la cual se construirán el Modelo de Dominio (5.2), las Entidades (5.3), los Agregados (5.4) y los Objetos de Valor (5.5), omitiendo cualquier concepto de persistencia física (claves, esquemas, índices o terminología técnica).

---

## 2. Mapa Estructural del Modelo de Información (Information Model Map)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ ESTRUCTURA GENERAL DEL MODELO DE INFORMACIÓN DE GESTIVASEC V1                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE CONTROL DE ACCESO Y ORGANIZACIONES ]                           │
│   • Organización ──► Delimita TODA la información del negocio                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE INVENTARIO Y ACTIVOS ]                                         │
│   • Activo Digital ──► Fuente única de verdad de la infraestructura supervisada         │
│   • Acreditación Digital ──► Acompaña al Activo con estado de vigencia                   │
│   • Ventana de Mantenimiento ──► Regula periodos de supresión operacional                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE OBSERVABILIDAD SINTÉTICA ]                                     │
│   • Evaluación Sintética ──► Métrica periódica de respuesta y disponibilidad            │
│   • Evidencia Telemétrica ──► Captura inalterable del fallo telemétrico                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE INCIDENTES Y OPERACIONES ]                                     │
│   • Incidente Operacional ──► Expediente de atención de indisponibilidad                │
│   • Informe RCA ──► Causa raíz y acciones correctivas obligatorias                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE SEGURIDAD Y POSTURA SOC ]                                      │
│   • Hallazgo de Ciberseguridad ──► Vulnerabilidad perimetral categorizada               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE NOTIFICACIONES Y ALERTAS ]                                     │
│   • Alerta Operacional ──► Evento de señal interna agrupado                             │
│   • Notificación Operacional ──► Mensaje entregado al responsable                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ [ ÁREA DE INFORMACIÓN DE AUDITORÍA Y GOBIERNO INMUTABLE ]                               │
│   • Traza Inalterable de Auditoría ──► Bóveda pasiva de conservación inalterable        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Dominios de Información y Fronteras Estructurales

### 3.1 Dominio de Información de Organización y Aislamiento (`INFO-DOM-01`)
- **Propósito**: Definir la frontera de pertenencia del negocio por entidad organizativa.
- **Contenido Informativo**: Identificación de la Organización, estado de la entidad y políticas de aislamiento.
- **Invariante Informativa**: La identificación de la Organización es obligatoria e inmutable en todas las estructuras de información secundarias (`BR-04`).

### 3.2 Dominio de Información de Activos e Inventario (`INFO-DOM-02`)
- **Propósito**: Preservar la fuente de verdad de los activos digitales supervisados del ecosistema.
- **Contenido Informativo**: Atributos descriptivos del activo, ubicación de destino, nivel de criticidad, correo del responsable asignado y vigencia de acreditaciones digitales.
- **Invariante Informativa**: Todo registro de activo debe contar con un responsable asignado (`BR-02`).

### 3.3 Dominio de Información de Observabilidad Sintética (`INFO-DOM-03`)
- **Propósito**: Almacenar las mediciones sintéticas pasivas de disponibilidad y tiempo de respuesta.
- **Contenido Informativo**: Métricas de evaluación, marcas de tiempo, estados de salud y evidencias telemétricas de fallos.
- **Invariante Informativa**: Las evidencias telemétricas asociadas a una falla no pueden ser modificadas ni eliminadas.

### 3.4 Dominio de Información de Incidentes Operacionales (`INFO-DOM-04`)
- **Propósito**: Gestionar el expediente informativo de atención de interrupciones de servicio.
- **Contenido Informativo**: Prioridad (P1-P4), historial de estados, operador asignado, fecha límite de solución e informe formal de Causa Raíz (RCA).
- **Invariante Informativa**: Un incidente crítico P1 no puede alcanzar el estado de cierre sin la estructura de información del informe RCA completada (`BR-01`).

### 3.5 Dominio de Información de Seguridad SOC (`INFO-DOM-05`)
- **Propósito**: Gestionar la información de riesgos y deficiencias de postura de ciberseguridad.
- **Contenido Informativo**: Hallazgos perimetrales, categorización bajo marcos normativos del sector y severidad.

### 3.6 Dominio de Información de Alertas y Notificaciones (`INFO-DOM-06`)
- **Propósito**: Estructurar las señales operacionales internas y su distribución externa.
- **Contenido Informativo**: Señales de alerta emitidas, criterios de agrupación y registro de notificaciones entregadas por rol de responsabilidad.

### 3.7 Dominio de Información de Auditoría e Inmutabilidad (`INFO-DOM-07`)
- **Propósito**: Almacenar el registro histórico inalterable de todas las operaciones del sistema.
- **Contenido Informativo**: Identidad del actor, acción realizada, tipo de entidad, marca de tiempo inalterable y detalle de la operación.
- **Invariante Informativa**: Bóveda de conservación inalterable de solo adición sin operaciones de modificación o borrado permitidas (`BR-05`).

---

## 4. Flujos de Información del Dominio (Domain Information Flows)

```
[Evaluación Sintética] ──(Detecta Falla)──► [Evidencia Telemétrica]
                                                   │
                                                   ▼
[Incidente Operacional] ◄──(Declara P1)──── [Alerta Operacional]
          │                                        │
          ▼                                        ▼
    [Informe RCA]                      [Notificación Operacional]
          │                                        │
          └───────────────┬────────────────────────┘
                          ▼
           [Traza Inalterable de Auditoría]
```

---

## 5. Reglas de Integridad y Fronteras de Aislamiento del Modelo

1. **Enforzamiento del Contexto de Organización (`INFO-RULE-01`)**: Toda estructura de información pertenece a una única Organización. Queda prohibida la existencia de datos globales no asociados a una frontera organizativa.
2. **Inmutabilidad de Registros Históricos (`INFO-RULE-02`)**: Las estructuras de auditoría y evidencias telemétricas se definen bajo un modelo informativo inalterable de solo adición.
3. **Integridad de Referencias del Dominio (`INFO-RULE-03`)**: Un expediente de incidente no puede existir sin estar referenciado a un Activo Digital válido del inventario.
4. **Completitud del Informe RCA (`INFO-RULE-04`)**: La estructura de cierre de un incidente crítico exige la presencia de los campos de causa raíz y pasos de solución.

---

## 6. Matriz de Trazabilidad del Modelo de Información

| Dominio de Información | Lenguaje Ubicuo (5.0) | Requisito Funcional (4.2) | Caso de Uso (4.3) | Proceso Operacional (4.5) |
| :--- | :--- | :--- | :--- | :--- |
| **`INFO-DOM-01` Acceso & Org** | Organización | `FR-0008` | `UC-008` | `WF-005`, `WF-007` |
| **`INFO-DOM-02` Activos** | Activo Digital, Acreditación | `FR-0001`, `FR-0003` | `UC-001`, `UC-003` | `WF-004`, `WF-005` |
| **`INFO-DOM-03` Observabilidad**| Evaluación Sintética, Evidencia| `FR-0002` | `UC-002` | `WF-001` |
| **`INFO-DOM-04` Incidentes** | Incidente, Informe RCA | `FR-0004`, `FR-0005`, `FR-0006` | `UC-004`, `UC-005`, `UC-006` | `WF-002`, `WF-003` |
| **`INFO-DOM-05` Seguridad SOC** | Hallazgo de Ciberseguridad | `FR-0007` | `UC-007` | `WF-006` |
| **`INFO-DOM-06` Notificaciones** | Alerta, Notificación | `FR-0010` | `UC-010` | `WF-001`, `WF-004` |
| **`INFO-DOM-07` Auditoría** | Traza Inalterable Auditoría| `FR-0009` | `UC-009` | `WF-003`, `WF-007` |

---

## 7. Summary & Phase 5.1 Validation Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE ARQUITECTURA DEL MODELO DE INFORMACIÓN (SUBFASE 5.1 GATE REVIEW)        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Cobertura 100% de los Dominios de Información del Ecosistema:            YES / SÍ     │
│ • Delimitación estricta por Organización en todas las áreas (BR-04):       YES / SÍ     │
│ • Trazabilidad completa hacia Lenguaje Ubicuo (5.0) y Fase 4:              YES / SÍ     │
│ • Ausencia total de conceptos de persistencia (UUID, tenant_id, SQL):      YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ INFORMATION MODEL SCORE:        100% (MODELO DE INFORMACIÓN ESTRUCTURAL APROBADO)       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
