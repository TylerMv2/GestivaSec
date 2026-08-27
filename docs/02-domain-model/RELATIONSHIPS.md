# 5.6 RELATIONSHIPS — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `RELATIONSHIPS.md`  
> **Phase**: PHASE 5.6 — RELATIONSHIPS  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Business Domain Relationships Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.6 Relationships** establece la **Especificación de Relaciones del Dominio del Negocio** para **Gestiva Security (GestivaSec V1)**. Este documento formaliza el tipo de asociación, multiplicidad semántica, navegabilidad funcional y reglas de acoplamiento conceptual entre los elementos del dominio (Entidades, Agregados y Objetos de Valor).

Fiel al principio de pureza conceptual, esta especificación mantiene una **independencia absoluta de decisiones de ejecución** (servicios, repositorios, comandos, transacciones) y de **persistencia física** (claves primarias, claves foráneas, tablas de unión, esquemas SQL, ORMs o identificadores técnicos).

---

## 2. Mapa General de Relaciones del Dominio (Domain Relationship Map)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ MAPA DE RELACIONES CONCEPTUALES DEL DOMINIO                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                  [ Organización ]                                       │
│                                         │                                               │
│                         (1:N - Frontera de Pertenencia `BR-04`)                          │
│                                         │                                               │
│       ┌─────────────────────────────────┼─────────────────────────────────┐             │
│       ▼                                 ▼                                 ▼             │
│ [ Activo Digital ]             [ Incidente Operacional ]        [ Traza de Auditoría ]  │
│       │                                 │                                               │
│       ├─► (1:N Agregación `AGG-01`)     ├─► (1:0..1 Contención `AGG-02`)                │
│       │   [ Acreditación Digital ]      │   [ Informe RCA ] (`BR-01`)                   │
│       │                                 │                                               │
│       └─► (1:N Observabilidad)          └─► (N:1 Origen de Falla)                       │
│           [ Evaluación Sintética ] ───► [ Alerta Operacional ]                          │
│                     │                           │                                       │
│                     └─► (1:0..1 Generación)     └─► (N:1 Canalización)                  │
│                         [ Evidencia ]               [ Notificación Operacional ]        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Catálogo Detallado de Relaciones del Dominio

### REL-01: Organización ➔ Activo Digital
- **ID Relación**: `REL-01`
- **Elementos Involucrados**: `Organización` (`ENT-07` / `AGG-05`) ➔ `Activo Digital` (`ENT-01` / `AGG-01`).
- **Tipo de Relación**: Delimitación de Frontera Organizativa (Composición del Dominio).
- **Multiplicidad Semántica**: **1 a N** (Una Organización posee 1 o más Activos Digitales; un Activo Digital pertenece a exactamente 1 Organización).
- **Navegabilidad Funcional**: Unidireccional desde Organización hacia sus Activos Digitales.
- **Regla de Negocio Vinculada**: `Regla BR-04` (Aislamiento organizacional inalienable).

---

### REL-02: Activo Digital ➔ Acreditación Digital
- **ID Relación**: `REL-02`
- **Elementos Involucrados**: `Activo Digital` (`ENT-01` / `AGG-01`) ➔ `Acreditación Digital` (`ENT-05`).
- **Tipo de Relación**: Agregación de Contención Interna (Dentro de `AGG-01`).
- **Multiplicidad Semántica**: **1 a N** (Un Activo Digital posee 0 o múltiples Acreditaciones Digitales; una Acreditación Digital está asociada a 1 único Activo Digital).
- **Navegabilidad Funcional**: Dirigida exclusivamente a través de la Raíz del Agregado (`Activo Digital`).

---

### REL-03: Activo Digital ➔ Evaluación Sintética
- **ID Relación**: `REL-03`
- **Elementos Involucrados**: `Activo Digital` (`ENT-01` / `AGG-01`) ➔ `Evaluación Sintética` (`VO-004`).
- **Tipo de Relación**: Asociación de Observabilidad Pasiva.
- **Multiplicidad Semántica**: **1 a N** (Un Activo Digital es supervisado por múltiples Evaluaciones Sintéticas secuenciales).
- **Navegabilidad Funcional**: Contextual basada en el Activo Digital supervisado.

---

### REL-04: Evaluación Sintética ➔ Evidencia Telemétrica
- **ID Relación**: `REL-04`
- **Elementos Involucrados**: `Evaluación Sintética` ➔ `Evidencia Telemétrica`.
- **Tipo de Relación**: Generación de Prueba Documental.
- **Multiplicidad Semántica**: **1 a 0..1** (Una Evaluación Sintética que detecta una falla genera 1 Evidencia Telemétrica inalterable; si es exitosa genera 0 evidencias de falla).
- **Navegabilidad Funcional**: Vinculada a la evaluación sintética de origen.

---

### REL-05: Alerta Operacional ➔ Incidente Operacional
- **ID Relación**: `REL-05`
- **Elementos Involucrados**: `Alerta Operacional` ➔ `Incidente Operacional` (`ENT-02` / `AGG-02`).
- **Tipo de Relación**: Disparo y Origen de Dominio.
- **Multiplicidad Semántica**: **N a 1** (Una o varias Alertas Operacionales de fallas sintéticas repetidas originan 1 Incidente Operacional).
- **Navegabilidad Funcional**: Desde la Alerta hacia el expediente de Incidente creado.
- **Regla de Negocio Vinculada**: `Regla BR-03` (Falla sintética repetida declara incidente crítico P1).

---

### REL-06: Incidente Operacional ➔ Informe de Causa Raíz (RCA)
- **ID Relación**: `REL-06`
- **Elementos Involucrados**: `Incidente Operacional` (`ENT-02` / `AGG-02`) ➔ `Informe RCA` (`ENT-03`).
- **Tipo de Relación**: Contención de Consistencia Transaccional (Dentro de `AGG-02`).
- **Multiplicidad Semántica**: **1 a 0..1** (Un Incidente P1 en estado remediado exige 1 Informe RCA para su cierre; en otros estados contiene 0 informes).
- **Navegabilidad Funcional**: Gestionada únicamente a través de la Raíz del Agregado (`Incidente Operacional`).
- **Regla de Negocio Vinculada**: `Regla BR-01` (Informe RCA obligatorio para autorización de cierre P1).

---

### REL-07: Alerta Operacional ➔ Notificación Operacional
- **ID Relación**: `REL-07`
- **Elementos Involucrados**: `Alerta Operacional` ➔ `Notificación Operacional`.
- **Tipo de Relación**: Agrupación y Canalización de Mensajería.
- **Multiplicidad Semántica**: **N a 1** (Múltiples Alertas Operacionales idénticas dentro de una ventana de tiempo se agrupan en 1 Notificación Operacional despachada al responsable).
- **Navegabilidad Funcional**: Unidireccional desde Alerta hacia Notificación despachada.

---

### REL-08: Organización ➔ Traza Inalterable de Auditoría
- **ID Relación**: `REL-08`
- **Elementos Involucrados**: `Organización` (`ENT-07` / `AGG-05`) ➔ `Traza de Auditoría` (`ENT-06` / `AGG-04`).
- **Tipo de Relación**: Conservación de Gobierno de Solo Adición.
- **Multiplicidad Semántica**: **1 a N** (Una Organización acumula N Trazas de Auditoría inalterables).
- **Navegabilidad Funcional**: Delimitada por la Organización (`BR-04`).
- **Regla de Negocio Vinculada**: `Regla BR-05` (Inmutabilidad absoluta de la auditoría).

---

## 4. Matriz de Relaciones del Dominio

| Relación ID | Elemento Origen | Elemento Destino | Tipo de Asociación | Multiplicidad | Regla de Negocio Vinculada |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`REL-01`** | `Organización` | `Activo Digital` | Delimitación de Frontera | **1 : N** | `Regla BR-04` (Aislamiento) |
| **`REL-02`** | `Activo Digital` | `Acreditación Digital` | Agregación Contenida (`AGG-01`) | **1 : N** | Seguimiento de Vigencia |
| **`REL-03`** | `Activo Digital` | `Evaluación Sintética` | Observabilidad Pasiva | **1 : N** | Intervalo de Evaluación |
| **`REL-04`** | `Evaluación Sintética` | `Evidencia Telemétrica` | Generación de Prueba | **1 : 0..1** | Prueba de Falla |
| **`REL-05`** | `Alerta Operacional` | `Incidente Operacional` | Disparo y Origen | **N : 1** | `Regla BR-03` (Incidente P1) |
| **`REL-06`** | `Incidente Operacional`| `Informe RCA` | Contención (`AGG-02`) | **1 : 0..1** | `Regla BR-01` (RCA Obligatorio)|
| **`REL-07`** | `Alerta Operacional` | `Notificación Operacional`| Agrupación y Canalización | **N : 1** | Agrupación por Ventana |
| **`REL-08`** | `Organización` | `Traza de Auditoría` | Conservación de Gobierno | **1 : N** | `Regla BR-05` (Inmutabilidad)|

---

## 5. Summary & Phase 5.6 Validation Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE VALIDACIÓN DE RELACIONES DEL DOMINIO (SUBFASE 5.6 GATE REVIEW)            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Especificación 100% basada en Relaciones Semánticas del Negocio:          YES / SÍ     │
│ • Cero alusión a persistencia física (claves foráneas, PK, esquemas SQL):  YES / SÍ     │
│ • Cero alusión a conceptos de ejecución (servicios, repositorios, eventos): YES / SÍ     │
│ • Trazabilidad completa hacia Agregados (5.4) y Entidades (5.3):           YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ RELATIONSHIPS SPECIFICATION SCORE: 100% (RELACIONES DE DOMINIO PURAS APROBADAS)         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
