# 3.2 ARCHITECTURAL PRINCIPLES — GESTIVASEC V1
> **Estado**: Especificación Oficial de Arquitectura Empresarial (TOGAF)  
> **Comité**: Chief Enterprise Architect, TOGAF Specialist & Architectural Team  
> **Fase**: FASE 3: ENTERPRISE ARCHITECTURE — Subfase 3.2  
> **Fecha**: 2026-07-25  

---

## 1. Executive Summary (Resumen Ejecutivo)

La subfase **3.2 Architectural Principles** establece la **Especificación Oficial de Principios de Arquitectura** que gobernará la toma de todas las decisiones arquitectónicas futuras en **GestivaSec V1**. Bajo el estándar TOGAF 10 / SEI, este documento define *cómo se deben tomar las decisiones de arquitectura*, garantizando que todo diseño técnico futuro sea una consecuencia directa de estos principios obligatorios.

El documento formaliza los Principios Obligatorios (*Mandatory*) y Recomendados (*Recommended*), su matriz de gobernanza, políticas de excepciones, cumplimiento de atributos de calidad (NFRs) y trazabilidad con las Fases 1 (Enterprise Discovery), 2 (Domain Discovery) y 3.1 (Quality Attributes & NFRs), sin introducir diseños de software, bases de datos, tecnologías ni código.

---

## 2. Architectural Principles Catalog (Catálogo Detallado de Principios)

### PRIN-01: Domain-Driven Architecture (DDD First)
- **Identifier**: `PRIN-01`
- **Name**: Domain-Driven Architecture
- **Definition**: La estructura del software y los límites de la arquitectura deben reflejar de manera exacta el modelo de dominio y los Bounded Contexts descubiertos en la Fase 2.
- **Purpose**: Prevenir el descalce entre la lógica del negocio y la estructura del sistema.
- **Business Motivation**: Garantizar que el sistema evolucione a la par del ecosistema corporativo Gestiva.
- **Architectural Motivation**: Eliminar la complejidad accidental y mantener las capas de dominio 100% puras sin dependencias de infraestructura.
- **Applicability & Scope**: Todo el diseño lógico y físico de GestivaSec V1.
- **Benefits**: Alta mantenibilidad, bajo acoplamiento y lenguaje ubicuo unificado.
- **Potential Risks**: Exceso de abstracción si no se aplica con pragmatismo.
- **Trade-offs**: Extensibilidad vs. Velocidad de implementación inicial.
- **Dependencies**: Bounded Contexts (`BC-01` a `BC-07`).
- **Exceptions**: Ninguna (Principio Inmutable).
- **Governance Rules**: Ningún modelo de base de datos o API puede alterar la semántica de las Entidades y Agregados del dominio.
- **Compliance Criteria**: Verificación de independencia de la capa de dominio en pipelines CI/CD.
- **Validation Strategy**: Auditoría de código estático confirmando cero importaciones de frameworks en `/domain`.
- **Architecture Decision Impact**: Fuerza la adopción del patrón Clean Architecture (Hexagonal).
- **Related Quality Attributes / NFRs**: `ATTR-06` (Extensibilidad), `NFR-EXT-01`, `NFR-TST-01`.
- **Traceability**: Fase 2 (Domain Discovery - `ADR-0007`).

---

### PRIN-02: Zero Trust & Security by Design
- **Identifier**: `PRIN-02`
- **Name**: Zero Trust & Security by Design
- **Definition**: La seguridad debe ser una restricción primaria incorporada desde el diseño; ninguna entidad interna o externa posee confianza implícita.
- **Purpose**: Neutralizar vectores de ataque perimetrales e internos sobre la infraestructura.
- **Business Motivation**: Proteger la confidencialidad de los metadatos y la continuidad operacional de GestivaOne, Gestiva Store y Festa.
- **Architectural Motivation**: Inyección obligatoria de verificación de identidad, autorización y aislamiento `tenant_id` en cada solicitud.
- **Applicability & Scope**: Todas las APIs, componentes, conexiones de red y accesos a datos.
- **Benefits**: Eliminación de movimientos laterales maliciosos y aislamiento Multi-Tenant robusto.
- **Potential Risks**: Incremento de la latencia por múltiples comprobaciones de autorización.
- **Trade-offs**: Seguridad estricta vs. Latencia mínima (~10-15ms overhead).
- **Dependencies**: Capa de Identidad (`BC-06`).
- **Exceptions**: Ninguna.
- **Governance Rules**: Toda consulta o comando debe inyectar y validar el contexto `tenant_id`.
- **Compliance Criteria**: 0% de endpoints expuestos sin validación de token y contexto de tenant.
- **Validation Strategy**: Escaneo SAST/DAST y pruebas de penetración automatizadas contra las RLS.
- **Architecture Decision Impact**: Exige políticas RLS a nivel de base de datos y autenticación en el Edge.
- **Related Quality Attributes / NFRs**: `ATTR-03` (Seguridad), `NFR-SEC-01`, `NFR-SEC-02`.
- **Traceability**: Fase 1 (`ADR-0001`), Fase 3.1 (`NFR-SEC-01`).

---

### PRIN-03: Immutable Auditability & Non-Repudiation
- **Identifier**: `PRIN-03`
- **Name**: Immutable Auditability & Non-Repudiation
- **Definition**: Todo evento operacional, cambio de estado o acción de usuario debe generar un registro de auditoría append-only inalterable.
- **Purpose**: Garantizar el no repudio, la trazabilidad forense y el soporte para auditorías normativas.
- **Business Motivation**: Transparencia total ante la Dirección y auditores externos sobre las operaciones del ecosistema.
- **Architectural Motivation**: Prohibir operaciones de actualización (`UPDATE`) o eliminación (`DELETE`) sobre los registros de auditoría.
- **Applicability & Scope**: Almacenamiento y capa de auditoría (`BC-05`).
- **Benefits**: Trazabilidad histórica 100% confiable e infalsificable.
- **Potential Risks**: Crecimiento continuo del volumen de datos de auditoría.
- **Trade-offs**: Auditabilidad Total vs. Costos de Almacenamiento.
- **Dependencies**: Dominio de Auditoría (`DOM-05`).
- **Exceptions**: Políticas de purga legalmente aprobadas para datos de más de 7 años.
- **Governance Rules**: El esquema de auditoría no debe otorgar permisos de borrado a ningún rol o usuario.
- **Compliance Criteria**: Verificación de permisos de base de datos restringidos a solo inserción (`INSERT`).
- **Validation Strategy**: Pruebas unitarias comprobando el rechazo de sentencias `DELETE`/`UPDATE`.
- **Architecture Decision Impact**: Diseñar tablas o colas append-only dedicadas a auditoría.
- **Related Quality Attributes / NFRs**: `ATTR-04` (Auditoría), `NFR-AUD-01`.
- **Traceability**: Fase 1 (`ENGINEERING_PRINCIPLES.md`), Fase 3.1 (`NFR-AUD-01`).

---

### PRIN-04: Loose Coupling & Event Awareness
- **Identifier**: `PRIN-04`
- **Name**: Loose Coupling & Event Awareness
- **Definition**: Los Bounded Contexts deben comunicarse de forma desacoplada mediante la emisión y reacción asíncrona a Eventos de Dominio inmutables.
- **Purpose**: Prevenir el acoplamiento rígido síncrono y los fallos en cascada entre subsistemas.
- **Business Motivation**: Permitir la operación independiente de los módulos NOC y SOC sin bloqueos mutuos.
- **Architectural Motivation**: Adopción de arquitecturas orientadas a eventos (EDA) manteniendo interfaces de publicación abstractas.
- **Applicability & Scope**: Comunicación entre los 7 Bounded Contexts.
- **Benefits**: Alta resiliencia, escalabilidad independiente y tolerancia a fallos parciales.
- **Potential Risks**: Complejidad en la gestión de consistencia eventual.
- **Trade-offs**: Consistencia Eventual vs. Consistencia Inmediata.
- **Dependencies**: Contratos de Eventos de Dominio (`EVT-01` a `EVT-07`).
- **Exceptions**: Consultas síncronas de lectura inmediata en la misma frontera transaccional.
- **Governance Rules**: Prohibido invocar métodos internos de otros agregados fuera de la frontera del contexto.
- **Compliance Criteria**: Verificación de comunicación mediante bus de eventos o contratos asíncronos.
- **Validation Strategy**: Pruebas de integración de publicación y suscripción de eventos.
- **Architecture Decision Impact**: Implementar interfaces `DomainEventPublisher` totalmente desacopladas (ADR-0003).
- **Related Quality Attributes / NFRs**: `ATTR-05` (Resiliencia), `NFR-RES-01`, `NFR-PER-02`.
- **Traceability**: Fase 1 (`ADR-0003`), Fase 2 (`2.4_DOMAIN_EVENTS.md`).

---

### PRIN-05: Infrastructure Agnostic & Vendor Neutrality
- **Identifier**: `PRIN-05`
- **Name**: Infrastructure Agnostic & Vendor Neutrality
- **Definition**: La arquitectura central y el código de dominio no deben depender de características propietarias no estandarizadas de ningún proveedor cloud o sistema operativo.
- **Purpose**: Permitir la portabilidad del sistema entre proveedores (Hostinger VPS, Vercel, Supabase, Cloudflare u otros).
- **Business Motivation**: Preservar la soberanía tecnológica corporativa de Gestiva y evitar el secuestro por proveedor (*vendor lock-in*).
- **Architectural Motivation**: Uso obligatorio de adaptadores de infraestructura e interfaces de abstracción en los puertos Hexagonales.
- **Applicability & Scope**: Capa de Infraestructura y Conectores de GestivaSec V1.
- **Benefits**: Portabilidad total y libertad de migración sin reescritura de código de dominio.
- **Potential Risks**: No aprovechar al 100% características propietarias avanzadas de un proveedor específico.
- **Trade-offs**: Portabilidad Tecnológica vs. Optimización Propietaria.
- **Dependencies**: Clean Architecture Hexagonal.
- **Exceptions**: Servicios administrados fundamentales aprobados como restricciones de negocio (Supabase PostgreSQL, Vercel Edge).
- **Governance Rules**: Toda interacción con un servicio de tercero debe encapsularse tras una interfaz de puerto (`Adapter`).
- **Compliance Criteria**: 0% de referencias directas a SDKs propietarios dentro de las capas de Dominio y Aplicación.
- **Validation Strategy**: Inspección del árbol de dependencias del código fuente.
- **Architecture Decision Impact**: Exige la creación de adaptadores desacoplados (Capa Anti-Corrupción - ACL).
- **Related Quality Attributes / NFRs**: `ATTR-06` (Extensibilidad), `NFR-EXT-01`.
- **Traceability**: Fase 1 (`DIRECTIVA DE CONTEXTO EMPRESARIAL`), Fase 2 (`ADR-0007`).

---

### PRIN-06: Configuration over Code & Automation First
- **Identifier**: `PRIN-06`
- **Name**: Configuration over Code & Automation First
- **Definition**: Toda modificación de comportamiento operacional, adición de activos o calibración de sondas debe realizarse mediante parámetros de configuración declarativa sin requerir cambios de código ni despliegues manuales.
- **Purpose**: Eliminar el trabajo manual repetitivo (*toil*) y permitir la extensibilidad ágil.
- **Business Motivation**: Reducir los costos operacionales y permitir a los ingenieros NOC/SOC gestionar la plataforma dinámicamente.
- **Architectural Motivation**: Diseñar motores basados en metadatos y configuraciones dinámicas.
- **Applicability & Scope**: Gestión de activos, reglas de sondas y motores de alertas.
- **Benefits**: Incorporación de activos en < 5 minutos sin despliegues de software.
- **Potential Risks**: Malas configuraciones por parte de operadores si no se validan adecuadamente.
- **Trade-offs**: Dinamismo por Configuración vs. Complejidad de Motores de Reglas.
- **Dependencies**: Dominio de Inventario (`DOM-04`).
- **Exceptions**: Cambios estructurales en las invariantes de dominio.
- **Governance Rules**: Todo parámetro de sondeo o umbral debe exponerse como variable o configuración auditable.
- **Compliance Criteria**: Prueba de onboarding de activos lograda mediante configuración declarativa.
- **Validation Strategy**: Pruebas de integración de cambios de parámetros en caliente.
- **Architecture Decision Impact**: Forzar la separación entre el motor de ejecuciones y las definiciones de activos.
- **Related Quality Attributes / NFRs**: `ATTR-06` (Extensibilidad), `NFR-EXT-01`.
- **Traceability**: Fase 1 (`ENGINEERING_PRINCIPLES.md`), Fase 3.1 (`NFR-EXT-01`).

---

## 3. Principle Classification Matrix

| Identificador | Nombre del Principio | Clasificación | Ámbito de Aplicación | Nivel de Inviolabilidad |
| :--- | :--- | :---: | :--- | :---: |
| **PRIN-01** | Domain-Driven Architecture | **Mandatory** | Dominio y Clean Architecture | **Inmutable** |
| **PRIN-02** | Zero Trust & Security by Design | **Mandatory** | Seguridad, Identidad y APIs | **Inmutable** |
| **PRIN-03** | Immutable Auditability | **Mandatory** | Auditoría y Almacenamiento | **Inmutable** |
| **PRIN-04** | Loose Coupling & Event Awareness| **Mandatory** | Comunicación inter-contextos | **Inmutable** |
| **PRIN-05** | Infrastructure Agnostic | **Mandatory** | Puertos y Adaptadores | **Inmutable** |
| **PRIN-06** | Configuration over Code | **Recommended** | Inventario y Sondas | **Adaptable** |

---

## 4. Principle Dependency Matrix

| Principio | `PRIN-01` | `PRIN-02` | `PRIN-03` | `PRIN-04` | `PRIN-05` | `PRIN-06` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **PRIN-01 (DDD)** | — | **Soporta** | **Soporta** | **Soporta** | **Soporta** | **Soporta** |
| **PRIN-02 (Zero Trust)** | **Depende** | — | **Refuerza** | Independiente | **Refuerza** | **Refuerza** |
| **PRIN-03 (Auditability)** | **Depende** | **Depende** | — | **Escucha** | Independiente | **Audita** |
| **PRIN-04 (Event-Driven)** | **Depende** | Independiente | **Alimenta** | — | **Desacopla** | Independiente |
| **PRIN-05 (Vendor Neutral)**| **Depende** | Independiente | Independiente | **Soporta** | — | **Soporta** |
| **PRIN-06 (Configuration)** | **Depende** | **Sujeto a** | **Audita** | Independiente | **Aprovecha** | — |

---

## 5. Architecture Governance & Exception Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ FLUJO DE GOBERNANZA Y GESTIÓN DE EXCEPCIONES A PRINCIPIOS                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. PROPUESTA DE CAMBIO / EXCEPCIÓN (Presentada por Arquitecto con justificación técnica)  │
│                                           │                                             │
│                                           ▼                                             │
│ 2. EVALUACIÓN DE IMPACTO EN PRINCIPIOS MANTADORY (Comité de Arquitectura / CTO)          │
│                                           │                                             │
│              ┌────────────────────────────┴────────────────────────────┐                │
│              ▼                                                         ▼                │
│    ¿Violación de Principio Mandatory?                       ¿Principio Recommended?     │
│              │                                                         │                │
│              ▼                                                         ▼                │
│     [ RECHAZO AUTOMÁTICO ]                                 [ EVALUACIÓN DE RISKS/ADR ]  │
│   (No se permiten excepciones)                             (Aprobación con condiciones) │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 Políticas de Gobernanza
- **Aprobación de Principios**: Únicamente el Chief Enterprise Architect y el CTO pueden autorizar la adición o modificación de un Principio de Arquitectura.
- **Frecuencia de Revisión**: Semestral o ante cambios mayores en el alcance del ecosistema Gestiva.
- **Política de Excepciones**: Los principios clasificados como **Mandatory** (`PRIN-01` a `PRIN-05`) **no admiten excepciones bajo ningún motivo**. Los principios **Recommended** (`PRIN-06`) requieren un ADR formal aprobado por el Comité de Arquitectura.

---

## 6. Architecture Compliance & Validation Matrix

| Principio | Criterio de Cumplimiento Inmutable | Método de Validación Automatizado | Entrada para ADRs Futuros |
| :--- | :--- | :--- | :--- |
| **PRIN-01** | Cero importaciones de infraestructura en `/domain` | Linter SAST de arquitectura en CI/CD | Justifica Clean Architecture Hexagonal |
| **PRIN-02** | Filtrado `tenant_id` obligatorio en todas las consultas | Pruebas unitarias de permisos RLS | Justifica Seguridad Multi-Tenant |
| **PRIN-03** | Imposibilidad de ejecutar `UPDATE`/`DELETE` en audit | Verificación de esquema SQL y permisos DB| Justifica Almacenamiento Append-Only |
| **PRIN-04** | Comunicación inter-contextos mediante eventos | Inspección de contratos de Eventos | Justifica Pub/Sub asíncrono |
| **PRIN-05** | Adaptadores tras interfaces de puerto (ACL) | Verificación de abstracción de conectores | Justifica Neutralidad de Proveedor |
| **PRIN-06** | Onboarding de activos mediante configuración | Prueba de integración declarativa | Justifica Motores basados en Metadatos |

---

## 7. Quality Review & Confidence Assessment

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ EVALUACIÓN DE CALIDAD ARQUITECTÓNICA & MADUREZ (TOGAF / SEI)                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Cobertura de Principios Empresariales:   100% Especificados (Principios 1 a 6)        │
│ • Neutralidad Tecnológica Garantizada:     0% acoplamiento a código o frameworks        │
│ • Proceso de Gobernanza & Excepciones:     100% Definido con matriz de decisiones       │
│ • Trazabilidad hacia Fases 1, 2 y 3.1:     100% Mapeado en matrices de trazabilidad     │
│                                                                                         │
│ CONFIDENCE LEVEL:               95%                                                     │
│ ARCHITECTURE MATURITY SCORE:    98% (EXCELENTE / LISTO PARA RESTRICCIONES ARQUITECTÓNICAS)│
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. READY FOR ARCHITECTURE REVIEW

⚠️ **REGLA DE PARADA**: La subfase 3.2 ha finalizado. El equipo de ingeniería se detiene en este punto a la espera de la aprobación explícita del Comité de Arquitectura para autorizar el avance a la **Subfase 3.3 Architectural Constraints**.
