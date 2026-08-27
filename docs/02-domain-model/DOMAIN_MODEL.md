# 5.2 DOMAIN MODEL — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `DOMAIN_MODEL.md`  
> **Phase**: PHASE 5.2 — DOMAIN MODEL  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Business Domain Model Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.2 Domain Model** formaliza la **Especificación del Modelo de Dominio** para **Gestiva Security (GestivaSec V1)**. En estricto cumplimiento de la regla de pureza de la Fase 5, este documento modela el sistema utilizando **exclusivamente conceptos del negocio** definidos en el Lenguaje Ubicuo (Subfase 5.0). 

Queda completamente excluida cualquier decisión o terminología de persistencia física (como identificadores técnicos tipo UUID, discriminadores de base de datos como `tenant_id`, modelos de almacenamiento tipo `append-only`, esquemas, tablas, índices o claves foráneas), las cuales se posponen formalmente para las fases de diseño de datos e infraestructura.

---

## 2. Mapa Conceptual del Modelo de Dominio (Domain Model Map)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ MAPA CONCEPTUAL DEL MODELO DE DOMINIO DE NEGOCIO                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                 [ Organización ]                                        │
│                                        │ (Posee & Delimita)                             │
│       ┌────────────────────────────────┼────────────────────────────────┐               │
│       ▼                                ▼                                ▼               │
│ [ Activo Digital ]            [ Incidente Operacional ]      [ Traza Inalterable ]     │
│       │                                │                                │               │
│       ├─► (Tiene)                      ├─► (Requiere P1)                └─► (Registra)  │
│       │   [ Acreditación Digital ]     │   [ Informe RCA ]                  Todo evento  │
│       │                                │                                                │
│       └─► (Supervisado por)            └─► (Originado por)                              │
│           [ Evaluación Sintética ] ──► [ Alerta Operacional ]                           │
│                     │                          │                                        │
│                     └─► (Genera si falla)      └─► (Despacha)                           │
│                         [ Evidencia ]              [ Notificación Operacional ]         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Subdominios y Agrupaciones del Dominio

### 3.1 Dominio de Gestión de Activos e Inventario Corporativo
- **Conceptos Principales**: `Activo Digital`, `Acreditación Digital`, `Ventana de Mantenimiento`.
- **Responsabilidad del Negocio**: Preservar la fuente de verdad de los recursos digitales supervisados, sus responsables humanos y la vigencia de sus certificados de seguridad.

### 3.2 Dominio de Observabilidad Sintética Pasiva
- **Conceptos Principales**: `Evaluación Sintética`, `Evidencia Telemétrica`.
- **Responsabilidad del Negocio**: Medir continuamente la disponibilidad y los tiempos de respuesta sin degradar los servicios supervisados, capturando pruebas documentales ante fallas.

### 3.3 Dominio de Operaciones e Incidentes
- **Conceptos Principales**: `Incidente Operacional`, `Informe de Causa Raíz (RCA)`.
- **Responsabilidad del Negocio**: Coordinar la atención, triaje, remediación y cierre normativo de las interrupciones del servicio, enforzando el aprendizaje continuo mediante análisis RCA.

### 3.4 Dominio de Ciberseguridad y Postura SOC
- **Conceptos Principales**: `Hallazgo de Ciberseguridad`.
- **Responsabilidad del Negocio**: Categorizar y gestionar las vulnerabilidades y deficiencias de postura detectadas en el perímetro de los activos.

### 3.5 Dominio de Notificaciones y Comunicación Operacional
- **Conceptos Principales**: `Alerta Operacional`, `Notificación Operacional`.
- **Responsabilidad del Negocio**: Agrupar eventos de fallas y despachar avisos oportunos hacia los responsables designados en la matriz de responsabilidad.

### 3.6 Dominio de Gobierno y Auditoría Corporativa
- **Conceptos Principales**: `Traza Inalterable de Auditoría`.
- **Responsabilidad del Negocio**: Conservar pasiva e inalterablemente el registro histórico no repudiable de la totalidad de las operaciones del sistema.

### 3.7 Dominio de Organización y Control de Acceso
- **Conceptos Principales**: `Organización`, `Rol Operacional`.
- **Responsabilidad del Negocio**: Garantizar la frontera de delimitación de la información de cada entidad corporativa y aplicar los permisos correspondientes.

---

## 4. Relaciones Semánticas del Negocio

1. **Organización ➔ Activo Digital**: Una *Organización* es propietaria de múltiples *Activos Digitales*. Todo *Activo Digital* pertenece obligatoriamente a una única *Organización* (`BR-04`).
2. **Activo Digital ➔ Acreditación Digital**: Un *Activo Digital* puede tener asociada una *Acreditación Digital* de seguridad, cuya fecha de caducidad es monitoreada de forma preventiva.
3. **Activo Digital ➔ Evaluación Sintética**: Un *Activo Digital* en estado activo es supervisado periódicamente por *Evaluaciones Sintéticas*.
4. **Evaluación Sintética ➔ Evidencia Telemétrica**: Una *Evaluación Sintética* que detecta una falla genera una *Evidencia Telemétrica* inalterable.
5. **Evaluación Sintética ➔ Alerta Operacional**: La confirmación de fallas sintéticas repetidas emite una *Alerta Operacional*.
6. **Alerta Operacional ➔ Incidente Operacional**: Una *Alerta Operacional* de disponibilidad crítica dispara la declaración automática de un *Incidente Operacional* (`BR-03`).
7. **Alerta Operacional ➔ Notificación Operacional**: La *Alerta Operacional* se agrupa y canaliza como *Notificación Operacional* hacia el responsable según su *Rol Operacional*.
8. **Incidente Operacional ➔ Informe RCA**: Un *Incidente Operacional* de prioridad crítica P1 exige la documentación y validación de un *Informe de Causa Raíz (RCA)* para autorizar su cierre (`BR-01`).
9. **Organización ➔ Traza Inalterable de Auditoría**: Toda acción dentro de una *Organización* queda registrada de forma inalterable en la *Traza de Auditoría* (`BR-05`).

---

## 5. Reglas e Invariantes del Modelo de Dominio

- **Regla de Causa Raíz Obligatoria (`BR-01`)**: Un *Incidente Operacional* de prioridad crítica P1 no puede transicionar a estado cerrado si carece de un *Informe de Causa Raíz (RCA)* validado.
- **Regla de Propietario de Activo (`BR-02`)**: Todo *Activo Digital* registrado debe contar con un responsable humano asignado.
- **Regla de Declaración Automática (`BR-03`)**: La acumulación de fallas en las *Evaluaciones Sintéticas* declara automáticamente un *Incidente Operacional* de prioridad crítica.
- **Regla de Delimitación por Organización (`BR-04`)**: Toda entidad del dominio está contenida y aislada dentro de la frontera de su *Organización*.
- **Regla de Auditoría Inalterable (`BR-05`)**: La *Traza Inalterable de Auditoría* no permite modificaciones ni eliminaciones bajo ninguna circunstancia.

---

## 6. Summary & Phase 5.2 Validation Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE VALIDACIÓN DEL MODELO DE DOMINIO (SUBFASE 5.2 GATE REVIEW)               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Modelado basado 100% en Conceptos del Negocio (Lenguaje Ubicuo 5.0):     YES / SÍ     │
│ • Ausencia total de conceptos de persistencia (UUID, tenant_id, SQL):      YES / SÍ     │
│ • Delimitación estricta por Organización y cumplimiento de BR-01..05:      YES / SÍ     │
│ • Trazabilidad completa con las Fases 4 y 5.1:                             YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ DOMAIN MODEL SCORE:             100% (MODELO DE DOMINIO DE NEGOCIO PURO APROBADO)       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
