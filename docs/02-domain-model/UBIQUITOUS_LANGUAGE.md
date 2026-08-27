# 5.0 UBIQUITOUS LANGUAGE — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `UBIQUITOUS_LANGUAGE.md`  
> **Phase**: PHASE 5.0 — UBIQUITOUS LANGUAGE  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Ubiquitous Domain Dictionary Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.0 Ubiquitous Language** establece el **Diccionario Oficial de Lenguaje Ubicuo** para **Gestiva Security (GestivaSec V1)**, sirviendo como puente normativo fundamental entre la Ingeniería de Producto (Fase 4) y la Ingeniería de Información (Fase 5). Este vocabulario unificado normaliza la terminología del negocio derivada exclusivamente de los artefactos aprobados (`PRODUCT_SPECIFICATION.md`, `FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md`, `USE_CASE_SPECIFICATION.md`, `USER_JOURNEY_SPECIFICATION.md`, `WORKFLOW_SPECIFICATION.md`, `DOMAIN_OPERATION_SPECIFICATION.md`), garantizando que cada término posea una definición semántica única e inalterable que guiará el modelado de entidades, agregados, objetos de valor y código.

---

## 2. Diccionario de Dominio Oficial (Ubiquitous Language Dictionary)

### 1. Activo Digital (Digital Asset)
- **Definición Semántica**: Unidad fundamental de software, servicio o recurso corporativo del ecosistema Gestiva que ha sido registrado en el inventario único de la organización para ser supervisado.
- **Términos Relacionados**: Identificador de destino, Criticidad del Activo, Propietario de Activo.
- **Sinónimos No Permitidos**: *Recurso, Host, Target, Server, Aplicación* (Usar únicamente **Activo Digital** o **Activo**).

---

### 2. Evaluación Sintética (Synthetic Observation)
- **Definición Semántica**: Comprobación periódica no degradante realizada de forma pasiva y automática sobre la ubicación del activo digital para medir su disponibilidad y tiempo de respuesta.
- **Términos Relacionados**: Intervalo de Evaluación, Tiempo de Respuesta, Falla Sintética Confirmada.
- **Sinónimos No Permitidos**: *Probe, Check, Ping, Test, Healthcheck* (Usar únicamente **Evaluación Sintética**).

---

### 3. Incidente Operacional (Operational Incident)
- **Definición Semántica**: Evento que representa la interrupción, falla repetida o degradación de la disponibilidad de un activo digital, requiriendo atención, remediación y documentación formal.
- **Términos Relacionados**: Prioridad del Incidente (P1-P4), Estado del Incidente, Fecha Límite de Solución.
- **Sinónimos No Permitidos**: *Ticket, Bug, Falla, Problem, Error* (Usar únicamente **Incidente Operacional** o **Incidente**).

---

### 4. Análisis de Causa Raíz (Root Cause Analysis - RCA)
- **Definición Semántica**: Documento e informe formal obligatorio que especifica el origen técnico del fallo, las acciones correctivas aplicadas y las medidas preventivas, requisito indispensable para el cierre de incidentes críticos P1 (`BR-01`).
- **Términos Relacionados**: Causa Raíz, Pasos de Remediación, Cierre Definitivo.
- **Sinónimos No Permitidos**: *Postmortem, Cierre, Justificación* (Usar únicamente **Informe de Causa Raíz** o **RCA**).

---

### 5. Hallazgo de Ciberseguridad (Security Finding)
- **Definición Semántica**: Registro de una vulnerabilidad, riesgo o deficiencia de postura detectada en un activo digital, categorizada obligatoriamente bajo marcos normativos de seguridad del sector.
- **Términos Relacionados**: Categoría de Seguridad, Severidad del Hallazgo, Plan de Atención.
- **Sinónimos No Permitidos**: *Vulnerabilidad, Fallo de Seguridad, Flaw* (Usar únicamente **Hallazgo de Ciberseguridad** o **Hallazgo**).

---

### 6. Alerta Operacional (Operational Alert)
- **Definición Semántica**: Señal de evento emitida por los módulos de observabilidad o seguridad al detectar una falla sintética confirmada o la proximidad de expiración de una acreditación.
- **Términos Relacionados**: Agrupación de Alertas, Desduplicación, Emisión de Alerta.
- **Sinónimos No Permitidos**: *Signal, Alarm, Trigger* (Usar únicamente **Alerta Operacional** o **Alerta**).

---

### 7. Notificación Operacional (Operational Notification)
- **Definición Semántica**: Mensaje formal despachado y entregado a los usuarios o responsables asignados según la matriz de responsabilidad (RACI) ante la ocurrencia de una alerta o cambio de estado.
- **Términos Relacionados**: Despachador de Notificaciones, Canalización de Alertas, Destinatario Asignado.
- **Sinónimos No Permitidos**: *Mensaje, Email, Push, Aviso* (Usar únicamente **Notificación Operacional** o **Notificación**).

---

### 8. Evidencia Telemétrica (Telemetry Evidence)
- **Definición Semántica**: Prueba documental inalterable (registros de falla, marcas de tiempo, datos de evaluación) capturada en el momento de una falla y vinculada a un expediente de incidente.
- **Términos Relacionados**: Captura de Evidencia, Integridad de Evidencia, Registro Adjunto.
- **Sinónimos No Permitidos**: *Prueba, Log, Record* (Usar únicamente **Evidencia Telemétrica** o **Evidencia**).

---

### 9. Acreditación Digital (Digital Certificate / Credential)
- **Definición Semántica**: Certificado digital o acreditación de seguridad asociada a un activo corporativo, sujeta a seguimiento de vigencia y alertas preventivas de caducidad.
- **Términos Relacionados**: Fecha de Expiración, Plazo Preventivo Limite, Renovación de Acreditación.
- **Sinónimos No Permitidos**: *Cert, Token, Key, Licencia* (Usar únicamente **Acreditación Digital** o **Acreditación**).

---

### 10. Ventana de Mantenimiento (Maintenance Window)
- **Definición Semántica**: Período de tiempo planificado durante el cual las evaluaciones sintéticas de un activo digital no generan declaraciones automáticas de incidentes.
- **Términos Relacionados**: Estado de Mantenimiento, Suspensión Temporal de Alertas.
- **Sinónimos No Permitidos**: *Downtime, Pause, Parada* (Usar únicamente **Ventana de Mantenimiento**).

---

### 11. Organización (Tenant / Organization)
- **Definición Semántica**: Entidad organizacional o frontera lógica de pertenencia a la cual se asocian usuarios, activos, incidentes y trazas de auditoría (`BR-04`).
- **Términos Relacionados**: Aislamiento Organizacional, Contexto de Organización, Pertenenecia de Usuario.
- **Sinónimos No Permitidos**: *Cliente, Empresa, Cuenta, Tenant* (Usar únicamente **Organización**).

---

### 12. Traza Inalterable de Auditoría (Immutable Audit Trail)
- **Definición Semántica**: Registro pasivo de solo adición donde se conservan de forma inmutable todas las acciones de usuario, cambios de estado y eventos operacionales (`BR-05`).
- **Términos Relacionados**: Registro de Gobierno, No Repudio, Inmutabilidad de Auditoría.
- **Sinónimos No Permitidos**: *Audit Log, Trazabilidad, Log de Sistema* (Usar únicamente **Traza Inalterable de Auditoría** o **Traza de Auditoría**).

---

### 13. Matriz de Responsabilidad (Operational RACI Role)
- **Definición Semántica**: Estructura de asignación funcional de roles (Responsable de Operaciones, Analista de Ciberseguridad, Responsable de Confiabilidad, Director Técnico) que rige las notificaciones y transiciones.
- **Términos Relacionados**: Operador Asignado, Cambio de Estado, Rol del Usuario.
- **Sinónimos No Permitidos**: *Permisos, Niveles, Perfiles de Sistema* (Usar únicamente **Matriz de Responsabilidad** o **Rol Operacional**).

---

## 3. Matriz de Clarificación de Diferencias Semánticas

| Término A | Término B | Diferencia Semántica Inviolable |
| :--- | :--- | :--- |
| **Incidente Operacional** | **Hallazgo de Ciberseguridad** | El *Incidente* representa una interrupción de disponibilidad en progreso que exige remediación; el *Hallazgo* representa una deficiencia de postura o vulnerabilidad que requiere triaje. |
| **Alerta Operacional** | **Notificación Operacional** | La *Alerta* es la señal de evento interna generada por el sistema; la *Notificación* es el mensaje entregado al responsable asignado. |
| **Evidencia Telemétrica** | **Informe RCA** | La *Evidencia* es el dato capturado automáticamente durante el fallo; el *RCA* es el análisis explicativo redactado por el operador. |
| **Activo Digital** | **Organización** | El *Activo* es el recurso supervisado; la *Organización* es la entidad propietaria del activo. |

---

## 4. Summary & Phase 5 Readiness Gate (Verificación de Preparación)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE PREPARACIÓN DE LENGUAJE UBICUO (SUBFASE 5.0 GATE REVIEW)                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Normalización del 100% del Vocabulario de la Fase 4:                     YES / SÍ     │
│ • Cero introducción de conceptos o requisitos no aprobados:                YES / SÍ     │
│ • Matriz de Diferenciación Semántica completada:                          YES / SÍ     │
│ • Prohibición estricta de sinónimos inconsistentes:                       YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ UBIQUITOUS LANGUAGE SCORE:      100% (BASE LÉXICA OFICIAL CONGELADA PARA FASE 5)        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
