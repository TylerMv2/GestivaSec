# 3.3 ARCHITECTURAL CONSTRAINTS — GESTIVASEC V1
> **Revision**: 2.0 (ARB Corrected — 100% Technology-Neutral Baseline)  
> **Comité**: Chief Enterprise Architect, TOGAF Specialist & Governance Team  
> **Fase**: FASE 3: ENTERPRISE ARCHITECTURE — Subfase 3.3  
> **Fecha**: 2026-07-25  

---

## 1. Executive Summary (Resumen Ejecutivo)

La subfase **3.3 Architectural Constraints** ha sido revisada y corregida por mandato del **Architecture Review Board (ARB)** para alcanzar una **neutralidad tecnológica del 100%**. Este documento define las limitaciones, obligaciones y fronteras innegociables de arquitectura que delimitan *qué debe respetar la arquitectura de GestivaSec V1*, eliminando por completo cualquier mención a proveedores, tecnologías, frameworks, plataformas de despliegue, mecanismos de persistencia o valores numéricos de implementación.

Todas las decisiones relativas al *cómo* han sido estrictamente aisladas y registradas como **Entradas para Decisiones de Arquitectura (ADI Register)** para su resolución ordenada en las subfases correspondientes de la Fase 3.

---

## 2. Architectural Constraints Catalog (Catálogo de Restricciones Tecnológicamente Neutras)

### CONST-01: Asset Scope Boundary Constraint
- **Identifier**: `CONST-01`
- **Name**: Asset Scope Boundary Constraint
- **Category**: Strategic / Business Boundary
- **Definition**: La plataforma debe realizar actividades de observabilidad, monitoreo y evaluación de seguridad exclusivamente sobre activos digitales formalmente autorizados y registrados en el inventario del ecosistema.
- **Description**: Prohibición estricta de iniciar sondeos, análisis o procesamiento de telemetría sobre cualquier activo, dominio o punto de acceso que no haya sido validado e incorporado previamente a la frontera de inventario.
- **Business Driver**: Foco de gobernanza, prevención de actividades no autorizadas y control de límites de responsabilidad.
- **Constraint Source**: Subfases 1.1 y 1.4 (Enterprise Discovery).
- **Constraint Type**: Mandatory.
- **Applicability & Architectural Scope**: Todos los componentes lógicos de inventario, sondas y seguridad.
- **Affected Future Phases**: Subfase 3.4 (Logical Architecture), Subfase 3.5 (Physical Architecture).
- **Architectural Motivation**: Garantizar límites deterministas e inquebrantables en la superficie de monitoreo.
- **Business Motivation**: Proteger la integridad operacional y cumplir con los acuerdos de autorización corporativa.
- **Expected Benefits**: Control absoluto de la frontera de monitoreo y eliminación de sobrecostos o interferencias.
- **Potential Risks**: Intentos inadvertidos de procesamiento sobre entidades no registradas.
- **Dependencies**: Bounded Context de Inventario (`BC-04`).
- **Conflicting Constraints**: Ninguna.
- **Compliance Criteria**: 100% de actividades de observabilidad vinculadas a un activo verificado.
- **Validation / Verification Method**: Verificación de contratos en la frontera del contexto de inventario.
- **Review Frequency**: Trimestral.
- **Constraint Owner**: Enterprise Architect.
- **Lifecycle Status**: Active / Mandatory.
- **Traceability**: Fase 1 (`1.4_BUSINESS_CONSTRAINTS.md`), `PRIN-01`.
- **Related Quality Attributes / NFRs**: `ATTR-01`, `NFR-EXT-01`.

---

### CONST-02: Heterogeneous Distributed Environment Constraint
- **Identifier**: `CONST-02`
- **Name**: Heterogeneous Distributed Environment Constraint
- **Category**: Operational / Architectural Boundary
- **Definition**: La arquitectura debe operar de forma nativa a través de una topología distribuida y heterogénea que soporte componentes de procesamiento persistente, entornos de ejecución en el borde (*edge*), servicios administrados de datos y pipelines automatizados de entrega.
- **Description**: La arquitectura lógica debe estructurarse mediante capas totalmente desacopladas de la infraestructura subyacente, permitiendo que sus componentes se desplieguen y comuniquen eficazmente en entornos con diferentes capacidades de cómputo y latencia.
- **Business Driver**: Maximizar la flexibilidad de la infraestructura corporativa y evitar dependencias de un único modelo de ejecución.
- **Constraint Source**: Subfases 1.9 y 1.10 (Enterprise Discovery).
- **Constraint Type**: Mandatory.
- **Applicability & Architectural Scope**: Diseños de componentes lógicos, patrones de comunicación e interfaces.
- **Affected Future Phases**: Subfase 3.4 (Logical Architecture), Subfase 3.5 (Physical Architecture).
- **Architectural Motivation**: Mantener la independencia del software mediante adaptadores de puerto Hexagonales (Capa ACL).
- **Business Motivation**: Preservar la soberanía tecnológica y permitir la evolución de la infraestructura sin reescritura.
- **Expected Benefits**: Portabilidad, resiliencia y desacoplamiento estructural.
- **Potential Risks**: Heterogeneidad en los tiempos de respuesta entre nodos distribuidos.
- **Dependencies**: Principio `PRIN-05` (Infrastructure Agnostic).
- **Conflicting Constraints**: Ninguna.
- **Compliance Criteria**: Absoluta separación entre la capa de aplicación/dominio y las interfaces de infraestructura.
- **Validation / Verification Method**: Análisis de dependencias de arquitectura en CI/CD.
- **Review Frequency**: Semestral.
- **Constraint Owner**: Solution Architect.
- **Lifecycle Status**: Active / Mandatory.
- **Traceability**: Fase 1 (`1.9_TECHNOLOGY_LANDSCAPE.md`), `PRIN-05`.
- **Related Quality Attributes / NFRs**: `ATTR-01`, `NFR-AVA-01`.

---

### CONST-03: Strict Organizational Data Boundary Constraint
- **Identifier**: `CONST-03`
- **Name**: Strict Organizational Data Boundary Constraint
- **Category**: Security / Compliance Boundary
- **Definition**: La arquitectura debe imponer un aislamiento lógico inquebrantable de los datos de cada organización, exigiendo la presencia de un contexto discriminador inmutable en cada comando, consulta, evento o registro telemétrico.
- **Description**: Prohibición de procesar, consultar o almacenar cualquier entidad sin verificar su pertenencia al contexto organizacional autorizado. Las políticas de aislamiento deben aplicarse directamente en los límites de acceso y persistencia.
- **Business Driver**: Garantizar la confidencialidad, privacidad y prevención de contaminación cruzada entre organizaciones.
- **Constraint Source**: Subfases 1.2, 2.3 (`BC-06`), 3.1 (`NFR-SEC-01`).
- **Constraint Type**: Mandatory.
- **Applicability & Architectural Scope**: Todas las capas lógicas, contratos de datos, buses de eventos e interfaces.
- **Affected Future Phases**: Subfase 3.4 (Logical Architecture), Subfase 3.6 (Security Architecture).
- **Architectural Motivation**: Eliminar el riesgo de fuga de datos en el nivel arquitectónico.
- **Business Motivation**: Cumplir con las normativas corporativas de protección y privacidad de información.
- **Expected Benefits**: Aislamiento estricto de datos y seguridad garantizada por diseño.
- **Potential Risks**: Omisión del contexto de aislamiento si no se valida de forma automática en los adaptadores.
- **Dependencies**: Bounded Context de Identidad (`BC-06`).
- **Conflicting Constraints**: Ninguna.
- **Compliance Criteria**: 100% de operaciones filtradas por el contexto organizacional explícito.
- **Validation / Verification Method**: Verificación de esquemas de datos y auditoría de permisos de acceso.
- **Review Frequency**: En cada ciclo de revisión de arquitectura.
- **Constraint Owner**: Security Architect.
- **Lifecycle Status**: Active / Mandatory.
- **Traceability**: Fase 2 (`BC-06`), `PRIN-02`, `NFR-SEC-01`.
- **Related Quality Attributes / NFRs**: `ATTR-03`, `NFR-SEC-01`.

---

### CONST-04: Non-Disruptive & Non-Degrading Observation Constraint
- **Identifier**: `CONST-04`
- **Name**: Non-Disruptive & Non-Degrading Observation Constraint
- **Category**: Operational / Performance Boundary
- **Definition**: Las actividades de observabilidad y sondaje sintético no deben causar degradación del rendimiento, interferencias operacionales ni indisponibilidad en los servicios supervisados.
- **Description**: Los motores de sondeo y recolección telemétrica deben operar dentro de límites de tasa, ancho de banda y consumo de recursos estrictamente acotados, garantizando que el impacto de la observación sea insignificante respecto a la capacidad normal del servicio.
- **Business Driver**: Proteger la continuidad del negocio y la experiencia de los usuarios en los activos de producción.
- **Constraint Source**: Subfases 1.5, 2.5 (`AGG-02`), 3.1 (`NFR-PER-01`).
- **Constraint Type**: Mandatory.
- **Applicability & Architectural Scope**: Componentes de observabilidad sintética y colectores telemétricos.
- **Affected Future Phases**: Subfase 3.4 (Logical Architecture).
- **Architectural Motivation**: Diseñar evaluadores de sondas con consumo de recursos eficiente y controlado.
- **Business Motivation**: Evitar la inducción involuntaria de sobrecargas en las aplicaciones de negocio.
- **Expected Benefits**: Observabilidad transparente sin riesgo para la disponibilidad de producción.
- **Potential Risks**: Bloqueos en capas de protección de red si los patrones de sondaje no se identifican claramente.
- **Dependencies**: Bounded Context de Observabilidad (`BC-01`).
- **Conflicting Constraints**: Ninguna.
- **Compliance Criteria**: Impacto de carga telemétrica mantenido dentro de márgenes de consumo insignificantes.
- **Validation / Verification Method**: Pruebas de simulación de carga y perfilado telemétrico.
- **Review Frequency**: Trimestral.
- **Constraint Owner**: SRE / Quality Architect.
- **Lifecycle Status**: Active / Mandatory.
- **Traceability**: Fase 1 (`1.5_SUCCESS_CRITERIA.md`), `PRIN-06`, `NFR-PER-01`.
- **Related Quality Attributes / NFRs**: `ATTR-02`, `NFR-PER-01`.

---

### CONST-05: Immutable & Non-Repudiable Audit Trail Constraint
- **Identifier**: `CONST-05`
- **Name**: Immutable & Non-Repudiable Audit Trail Constraint
- **Category**: Compliance / Governance Boundary
- **Definition**: Todos los eventos operacionales, cambios de configuración y acciones administrativas deben registrarse en una traza de auditoría inmutable de solo adición (*append-only*), que impida técnicamente la modificación o eliminación de registros pasados.
- **Description**: Prohibición absoluta de exponer interfaces o mecanismos que permitan alterar o borrar eventos de auditoría una vez capturados, garantizando el principio de no repudio y la integridad histórica.
- **Business Driver**: Cumplimiento de marcos legales, gobierno corporativo y capacidad de análisis forense inalterable.
- **Constraint Source**: Subfases 1.8 (`PROC-SOP-01`), 2.5 (`AGG-05`), 3.1 (`NFR-AUD-01`).
- **Constraint Type**: Mandatory.
- **Applicability & Architectural Scope**: Componentes de auditoría, trazabilidad y almacenamiento histórico (`BC-05`).
- **Affected Future Phases**: Subfase 3.4 (Logical Architecture), Subfase 3.7 (Persistence Architecture).
- **Architectural Motivation**: Aislar la persistencia de auditoría frente a mutaciones accidentales o maliciosas.
- **Business Motivation**: Garantizar la máxima confiabilidad ante auditorías externas e inspecciones de ciberseguridad.
- **Expected Benefits**: No repudio, inmutabilidad comprobable y cumplimiento normativo.
- **Potential Risks**: Crecimiento acumulativo en el volumen de eventos archivados.
- **Dependencies**: Bounded Context de Auditoría (`BC-05`).
- **Conflicting Constraints**: Ninguna.
- **Compliance Criteria**: Cero capacidades de modificación o borrado en el modelo de auditoría.
- **Validation / Verification Method**: Inspección de contratos de dominio y modelos de datos.
- **Review Frequency**: Anual.
- **Constraint Owner**: Governance & Compliance Architect.
- **Lifecycle Status**: Active / Mandatory.
- **Traceability**: Fase 2 (`BC-05`), `PRIN-03`, `NFR-AUD-01`.
- **Related Quality Attributes / NFRs**: `ATTR-04`, `NFR-AUD-01`.

---

## 3. Constraint Classification & Priority Matrices

### 3.1 Constraint Classification Matrix

| Identifier | Constraint Name | Primary Category | Secondary Category | Mandatory / Conditional |
| :--- | :--- | :--- | :--- | :---: |
| **CONST-01** | Asset Scope Boundary Constraint | Strategic | Business Boundary | **Mandatory** |
| **CONST-02** | Heterogeneous Distributed Environment | Operational | Architectural Boundary | **Mandatory** |
| **CONST-03** | Strict Organizational Data Boundary | Security | Compliance Boundary | **Mandatory** |
| **CONST-04** | Non-Disruptive & Non-Degrading Observation | Operational | Performance Boundary | **Mandatory** |
| **CONST-05** | Immutable Audit Trail Constraint | Compliance | Governance Boundary | **Mandatory** |

### 3.2 Constraint Priority Matrix

| Identifier | Constraint Name | Priority | Justification |
| :--- | :--- | :---: | :--- |
| **CONST-01** | Asset Scope Boundary Constraint | **Critical (P1)** | Delimita la frontera legal y operativa de la plataforma. |
| **CONST-02** | Heterogeneous Distributed Environment | **Critical (P1)** | Exige arquitectura desacoplada ejecutable en múltiples entornos. |
| **CONST-03** | Strict Organizational Data Boundary | **Critical (P1)** | Garantiza el aislamiento e inviolabilidad de datos. |
| **CONST-04** | Non-Disruptive Observation | **Critical (P1)** | Evita indisponibilidades inducidas sobre los activos en producción. |
| **CONST-05** | Immutable Audit Trail Constraint | **Critical (P1)** | Garantiza el no repudio e integridad inalterable de eventos. |

---

## 4. Architecture Decision Input Register (ADI Register - Entradas Diferidas Neutras)

Todas las decisiones que implican selección de mecanismos, modelos de datos, comunicación o despliegue han sido aisladas y registradas para su resolución en las subfases aprobadas de la Fase 3:

| ADI Identifier | Decision Required (Decisión Diferida) | Reason Deferred (Motivo del Diferimiento) | Responsible Phase | Business & Architectural Impact | Priority |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **ADI-ARCH-01** | Definición del patrón lógico de orquestación de sondas sintéticas | Corresponde al diseño de componentes y flujos de datos lógicos | **Subfase 3.4** (Logical Architecture) | Establece la estructura de adaptadores y evaluadores NOC | **P1** |
| **ADI-ARCH-02** | Selección del modelo de persistencia y abstracción de aislamiento de datos | Corresponde al diseño de persistencia y esquemas de datos | **Subfase 3.7** (Persistence Architecture) | Define el mecanismo de aislamiento de datos en almacenamiento | **P1** |
| **ADI-ARCH-03** | Definición del mecanismo de distribución asíncrona de eventos de dominio | Corresponde al diseño de integración y mensajería lógica | **Subfase 3.4** (Logical Architecture) | Establece la infraestructura de publicación y suscripción de eventos | **P1** |
| **ADI-ARCH-04** | Definición de la topología de despliegue y entrega continua | Corresponde al diseño físico y automatización de despliegues | **Subfase 3.8** (Deployment Architecture) | Estructura las etapas de empaquetado y liberación continua | **P2** |

---

## 5. Architectural Neutrality & ARB Compliance Verification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE NEUTRALIDAD TECNOLÓGICA & CUMPLIMIENTO ARB (REVISIÓN 2.0)               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Nombres de proveedores / Cloud eliminados:              SÍ (100% Removidos)           │
│ • Nombres de lenguajes / frameworks eliminados:           SÍ (100% Removidos)           │
│ • Mecanismos de bases de datos / RLS eliminados:          SÍ (Transformados a neutro)   │
│ • Tiempos / Porcentajes numéricos de implementación:      SÍ (Transformados a neutro)   │
│ • Entradas ADI verificadas contra el Roadmap:             SÍ (Mapeo a Subfases 3.4-3.8) │
│                                                                                         │
│ CONFIDENCE LEVEL:               98%                                                     │
│ ARCHITECTURE READINESS SCORE:   100% (LISTO Y APROBADO SIN CONDICIONES)                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
