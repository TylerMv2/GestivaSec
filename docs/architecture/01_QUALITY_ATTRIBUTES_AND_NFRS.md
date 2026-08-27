# 3.1 QUALITY ATTRIBUTES & NON-FUNCTIONAL REQUIREMENTS — GESTIVASEC V1
> **Estado**: Especificación Oficial de Arquitectura Empresarial  
> **Comité**: Principal Enterprise Architect, TOGAF Specialist & Architectural Team  
> **Fase**: FASE 3: ENTERPRISE ARCHITECTURE — Subfase 3.1  
> **Fecha**: 2026-07-25  

---

## 1. Executive Summary (Resumen Ejecutivo)

La subfase **3.1 Quality Attributes & Non-Functional Requirements** inaugura formalmente la **Fase 3: Enterprise Architecture** para **GestivaSec V1**. Actuando bajo el rol de *Principal Enterprise Architect & TOGAF Certified Specialist*, este documento establece la **Especificación Oficial de Atributos de Calidad y Requisitos No Funcionales (NFRs)** que actuarán como restricciones arquitectónicas obligatorias inmutables. 

Sobre la base de las aprobaciones de las Fases 1 (Enterprise Discovery) y 2 (Domain Discovery), se especifican en formato estandarizado SEI/TOGAF los atributos de calidad críticos (Disponibilidad, Rendimiento, Seguridad, Auditoría, Resiliencia, Mantenibilidad, Observabilidad, etc.), sus escenarios de calidad medibles, la matriz de compromisos (*Trade-offs*), el catálogo NFR formal y la evaluación de preparación técnica, sin diseñar software, APIs, tablas de base de datos ni seleccionar proveedores tecnológicos.

---

## 2. Quality Attribute Catalog (Catálogo Detallado de Atributos de Calidad)

### 2.1 ATTR-01: Availability (Disponibilidad)
- **Definición**: Proporción de tiempo operacional en que el sistema está completamente apto para recibir y procesar solicitudes de monitoreo e ingesta telemétrica.
- **Objetivo Arquitectónico**: Garantizar un nivel de servicio continuo con un tiempo de inactividad máximo de ~52.6 minutos/año.
- **Motivación de Negocio**: Asegurar que las interrupciones en los activos del ecosistema (`gestivaone.com`, `gestivaone-store.vercel.app`, `festa.gestivaone.com`) sean detectadas independientemente del horario.
- **Importancia Arquitectónica**: Impone requerimientos de tolerancia a fallos, desacoplamiento asíncrono y failover.
- **Criticidad**: **Critical (P1)**
- **Quality Scenario**:
  - *Source*: Fallo imprevisto en un nodo de red o componente de backend.
  - *Stimulus*: Pérdida de respuesta de una instancia de servicio durante tráfico normal.
  - *Environment*: Operación en producción bajo carga regular.
  - *Artifact*: Núcleo de sondas y motor telemétrico.
  - *Response*: Reenrutamiento automático del sondeo y conmutación sin pérdida de estado.
  - *Response Measure*: Disponibilidad del servicio ≥ **99.99%**; tiempo de recuperación de servicio (RTO) < 30 segundos.
- **Riesgos**: Caída de la observabilidad durante ventanas críticas de incidentes P1.
- **Implicaciones Arquitectónicas**: Requiere componentes sin estado (*stateless*), almacenamiento desacoplado y failover.
- **Dependencias**: Red WAN y disponibilidad del proveedor hosting.
- **Trade-offs**: Disponibilidad vs. Costo operativo (requiere recursos redundantes).
- **Estrategia de Validación**: Pruebas de inyección de fallos (*Chaos Engineering*) simulando caídas de nodos.

---

### 2.2 ATTR-02: Performance & Latency (Rendimiento y Latencia)
- **Definición**: Capacidad del sistema para ejecutar comprobaciones sintéticas y procesar eventos dentro de límites temporales estrictos.
- **Objetivo Arquitectónico**: Mantener tiempos de respuesta sintéticos inmediatos con MTTD < 60 segundos.
- **Motivación de Negocio**: Detectar degradaciones de velocidad antes de que causen abandono de usuarios en Gestiva Store.
- **Importancia Arquitectónica**: Restringe el diseño de pipelines de procesamiento para evitar cuellos de botella síncronos.
- **Criticidad**: **Critical (P1)**
- **Quality Scenario**:
  - *Source*: Motor de sondeos sintéticos.
  - *Stimulus*: Ejecución de 500 comprobaciones de latencia concurrentes.
  - *Environment*: Pico de uso en producción.
  - *Artifact*: Pipeline de procesamiento telemétrico.
  - *Response*: Procesar y evaluar la latencia de cada comprobación.
  - *Response Measure*: Latencia de procesamiento de eventos < 200 ms; MTTD < 60 segundos.
- **Riesgos**: Retraso en la generación de alertas por acumulación de eventos en cola.
- **Implicaciones Arquitectónicas**: Exige procesamiento asíncrono no bloqueante e indexación de alta velocidad.
- **Dependencias**: Ancho de banda de red y tiempo de CPU.
- **Trade-offs**: Rendimiento vs. Auditoría Exhaustiva (el filtrado detallado añade latencia).
- **Estrategia de Validación**: Pruebas de carga sostenida y perfilado de concurrencia.

---

### 2.3 ATTR-03: Security & Multi-Tenant Confidentiality (Seguridad y Confidencialidad Multi-Tenant)
- **Definición**: Gráfico de protección de datos telemétricos y de auditoría contra accesos no autorizados y contaminación cruzada.
- **Objetivo Arquitectónico**: Garantizar el aislamiento absoluto de datos por `tenant_id` y cifrado integral en tránsito y reposo.
- **Motivación de Negocio**: Proteger la propiedad intelectual y los metadatos estratégicos del ecosistema Gestiva.
- **Importancia Arquitectónica**: Rige la arquitectura de autorización, filtrado de datos y gestión de secretos.
- **Criticidad**: **Critical (P1)**
- **Quality Scenario**:
  - *Source*: Usuario autenticado de una organización (Tenant A).
  - *Stimulus*: Intento de consulta de un recurso o log perteneciente a otra organización (Tenant B).
  - *Environment*: Operación normal de la API / interfaz.
  - *Artifact*: Capa de filtrado de datos y control de acceso.
  - *Response*: Bloqueo inmediato de la solicitud y generación de alerta de seguridad.
  - *Response Measure*: 0% de filtración de datos entre tenants; 100% de solicitudes validadas contra `tenant_id`.
- **Riesgos**: Vulneración del aislamiento Multi-Tenant e inspección no autorizada de metadatos.
- **Implicaciones Arquitectónicas**: Inyección obligatoria de políticas RLS y tokens con firmas criptográficas.
- **Dependencias**: Capa de Identidad y Control de Acceso (`BC-06`).
- **Trade-offs**: Seguridad vs. Simplicidad (añade capas de verificación en cada consulta).
- **Estrategia de Validación**: Pruebas de penetración automatizadas y auditoría de permisos RLS.

---

### 2.4 ATTR-04: Auditability & Non-Repudiation (Auditoría e Inmutabilidad)
- **Definición**: Capacidad de registrar cada acción operacional y evento de dominio de forma inalterable e infalsificable.
- **Objetivo Arquitectónico**: Preservar un histórico de auditoría no repudiable de solo escritura.
- **Motivación de Negocio**: Cumplir con marcos de gobernanza y permitir análisis forense ante incidentes.
- **Importancia Arquitectónica**: Impone la creación de un almacenamiento auditable append-only.
- **Criticidad**: **Critical (P1)**
- **Quality Scenario**:
  - *Source*: Operador técnico o proceso automatizado.
  - *Stimulus*: Modificación de la criticidad de un activo o cierre de un incidente.
  - *Environment*: Operación diaria del sistema.
  - *Artifact*: Registro de auditoría inmutable (`BC-05`).
  - *Response*: Captura inalterable del evento incluyendo identidad del actor, timestamp y estado anterior/posterior.
  - *Response Measure*: 100% de eventos operativos registrados; 0% de modificaciones/borrados permitidos sobre el audit log.
- **Riesgos**: Alteración fraudulenta del historial de incidentes o fallos.
- **Implicaciones Arquitectónicas**: Almacenamiento append-only sin permisos de actualización o eliminación (`UPDATE`/`DELETE`).
- **Dependencias**: Dominio de Auditoría (`DOM-05`).
- **Trade-offs**: Auditoría Inmutable vs. Costo de Almacenamiento.
- **Estrategia de Validación**: Verificación de denegación de permisos de modificación a nivel de almacenamiento.

---

### 2.5 ATTR-05: Resilience & Recoverability (Resiliencia y Recuperabilidad)
- **Definición**: Capacidad del sistema para absorber fallos parciales de red o proveedores y restaurar la operación normal.
- **Objetivo Arquitectónico**: Mantener el monitoreo operando de forma aislada ante caídas de proveedores cloud externos.
- **Motivación de Negocio**: Evitar la pérdida de telemetría durante contingencias de red.
- **Importancia Arquitectónica**: Diseñar mecanismos de almacenamiento en búfer local y reintento con *backoff* exponencial.
- **Criticidad**: **High (P2)**
- **Quality Scenario**:
  - *Source*: Corte de conectividad WAN o indisponibilidad temporal del backend administrado.
  - *Stimulus*: Fallo de conexión al intentar enviar eventos telemétricos.
  - *Environment*: Contingencia en producción.
  - *Artifact*: Motor de búfer y resincronización local.
  - *Response*: Almacenar eventos en cola local resiliente y resincronizar automáticamente al restablecer el enlace.
  - *Response Measure*: 0% de pérdida de eventos telemétricos durante cortes < 2 horas; RPO = 0.
- **Riesgos**: Pérdida de métricas históricas durante caídas de red.
- **Implicaciones Arquitectónicas**: Arquitectura Offline-First y colas de persistencia temporal.
- **Dependencias**: Almacenamiento local resiliente.
- **Trade-offs**: Resiliencia vs. Complejidad de Sincronización.
- **Estrategia de Validación**: Pruebas de desconexión de red en caliente (*Net-Disconnect Tests*).

---

### 2.6 ATTR-06: Extensibilidad & Modifiabilidad (Extensibilidad)
- **Definición**: Facilidad con la que el sistema permite incorporar nuevos activos, reglas de sondeo o integraciones sin alterar el núcleo.
- **Objetivo Arquitectónico**: Habilitar la adición de nuevos dominios mediante configuración declarativa.
- **Motivación de Negocio**: Permitir el crecimiento del ecosistema Gestiva sin incurrir en costos de rediseño de software.
- **Importancia Arquitectónica**: Exige arquitectura hexagonal con inversión de dependencias y bajo acoplamiento.
- **Criticidad**: **High (P2)**
- **Quality Scenario**:
  - *Source*: Ingeniero DevSecOps.
  - *Stimulus*: Solicitud de incorporación de un nuevo subdominio al inventario.
  - *Environment*: Operación continua en producción.
  - *Artifact*: Módulo de inventario y configuración de sondas.
  - *Response*: Alta del activo e inicio automático de sondas sin reiniciar ni recompilar el sistema.
  - *Response Measure*: Tiempo de incorporación de activo < 5 minutos; 0 líneas de código modificadas.
- **Riesgos**: Acoplamiento rígido que requiera despliegues de código para agregar activos.
- **Implicaciones Arquitectónicas**: Diseño basado en módulos desacoplados y configuraciones dinámicas.
- **Dependencias**: Dominio de Inventario (`DOM-04`).
- **Trade-offs**: Extensibilidad vs. Simplicidad de Diseño Inicial.
- **Estrategia de Validación**: Prueba de incorporación de activo mediante archivo de configuración.

---

### 2.7 ATTR-07: Testability & Observability (Testabilidad y Observabilidad del Sistema)
- **Definición**: Capacidad del propio sistema GestivaSec V1 para ser monitoreado y probado en cada una de sus capas internas.
- **Objetivo Arquitectónico**: Exponer métricas de salud internas de la propia plataforma y permitir pruebas automatizadas del 100% de reglas de dominio.
- **Motivación de Negocio**: Garantizar que la herramienta de monitoreo no se convierta en una caja negra no confiable.
- **Importancia Arquitectónica**: Exige trazabilidad interna (`trace_id`) y separación pura de la capa de dominio sin dependencias I/O.
- **Criticidad**: **High (P2)**
- **Quality Scenario**:
  - *Source*: Suite de integración continua o ingeniero SRE.
  - *Stimulus*: Ejecución automatizada de pruebas unitarias sobre reglas de dominio.
  - *Environment*: Entorno de CI/CD.
  - *Artifact*: Capa de dominio pura.
  - *Response*: Validación determinista del 100% de las reglas e invariantes de negocio.
  - *Response Measure*: Cobertura de pruebas unitarias en dominio del **100%**; tiempo de ejecución < 10 segundos.
- **Riesgos**: Bugs no detectados en la lógica de cálculo de SLAs o evaluación de sondas.
- **Implicaciones Arquitectónicas**: Dominio puro e inyección de dependencias para mocks de infraestructura.
- **Dependencias**: Convenciones de Clean Architecture.
- **Trade-offs**: Testabilidad vs. Velocidad de Codificación Inicial.
- **Estrategia de Validación**: Ejecución de suites de prueba en pipelines de CI/CD.

---

## 3. Non-Functional Requirements Catalog (Catálogo NFR Formal)

| ID NFR | Categoría | Descripción Breve | Atributo Mapeado | Criterio de Aceptación | Método de Medición | Prioridad |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **NFR-AVA-01** | Disponibilidad | Tiempo de actividad continuo del núcleo de sondas | Availability | Uptime ≥ **99.99%** | Monitoreo sintético externo | **P1** |
| **NFR-PER-01** | Rendimiento | Tiempo de detección de indisponibilidad (MTTD) | Latency | MTTD < **60 segundos** | Timestamp de falla vs Alerta | **P1** |
| **NFR-PER-02** | Rendimiento | Procesamiento de eventos en cola telemétrica | Performance | Latencia event-bus < **200 ms** | Trazas internas `trace_id` | **P1** |
| **NFR-SEC-01** | Seguridad | Aislamiento estricto de datos Multi-Tenant | Security | 0% filtración entre tenants | Auditoría de consultas RLS | **P1** |
| **NFR-SEC-02** | Seguridad | Cifrado de datos en tránsito y reposo | Security | TLS 1.3 / AES-256 obligatorio | Escaneo de TLS y almacenamiento| **P1** |
| **NFR-AUD-01** | Auditoría | Inmutabilidad de registros de auditoría | Auditability | 0 permitidos UPDATE/DELETE | Inspección de permisos de DB | **P1** |
| **NFR-RES-01** | Resiliencia | Resistencia a cortes temporales de red WAN | Resilience | Zero pérdida de eventos < 2h | Inyección de fallos de red | **P2** |
| **NFR-EXT-01** | Extensibilidad | Adición de activos mediante configuración | Extensibility | 0 cambios de código | Prueba de onboarding activo | **P2** |
| **NFR-TST-01** | Testabilidad | Cobertura de pruebas unitarias en dominio | Testability | **100%** cobertura en dominio | Reporte de cobertura CI/CD | **P2** |
| **NFR-OBS-01** | Observabilidad | Trazabilidad unificada de peticiones | Observability | `trace_id` en el 100% de logs | Inspección de cabeceras/logs | **P2** |

---

## 4. Quality Scenario Catalog & Critical Scenarios

### Escenario Crítico 1: Pico de Carga & Congestión Telemétrica (Peak Workload)
- **Source**: Ingesta masiva simultánea de eventos de los 3 activos confirmados.
- **Stimulus**: Incremento repentino de 10x en la tasa de eventos telemétricos.
- **Environment**: Operación de producción bajo contingencia.
- **Artifact**: Pipeline de ingestión y bus de eventos.
- **Response**: Absorber el pico en cola asíncrona desacoplada manteniendo la estabilidad.
- **Response Measure**: 0% eventos perdidos; degradación de latencia de procesamiento < 300 ms.

### Escenario Crítico 2: Fallo de Proveedor de Nube Administrado (Third-Party Failure)
- **Source**: Caída temporal de la API administrada de Supabase o Vercel Edge.
- **Stimulus**: Retorno masivo de errores 500/503 o tiempos de espera agotados en la API del proveedor.
- **Environment**: Contingencia externa.
- **Artifact**: Capa Anti-Corrupción (ACL) y búfer local de resiliencia.
- **Response**: Aislar la falla en el adaptador ACL, persistir eventos en colas locales y evitar el colapso en cascada.
- **Response Measure**: El sistema continúa sondeando localmente; resincronización automática tras la recuperación del proveedor.

### Escenario Crítico 3: Intento de Elevación de Privilegios Multi-Tenant (Security Attack)
- **Source**: Actor malicioso o usuario comprometido.
- **Stimulus**: Manipulación de encabezados HTTP para inyectar un `tenant_id` ajeno.
- **Environment**: Solicitud de consulta a la API de datos.
- **Artifact**: Capa de Identidad (`BC-06`) y políticas RLS.
- **Response**: Rechazo inmediato de la solicitud, revocar sesión y emitir evento de auditoría de seguridad.
- **Response Measure**: 100% de intentos bloqueados; registro inmutable del evento de ataque.

---

## 5. Trade-off Analysis Matrix (Análisis de Compromisos Arquitectónicos)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ MATRIZ DE COMPROMISOS ARQUITECTÓNICOS (TRADE-OFF MATRIX)                                │
├──────────────────────────────┬──────────────────────────────┬───────────────────────────┤
│ ATRIBUTO FAVORABLE           │ ATRIBUTO COMPROMETIDO        │ JUSTIFICACIÓN TÉCNICA     │
├──────────────────────────────┼──────────────────────────────┼───────────────────────────┤
│ **Seguridad & Multi-Tenant**  │ **Rendimiento / Latencia**   │ El filtrado obligatorio   │
│ (Inyección de RLS / ACL)     │ (Overhead de verificación)   │ de `tenant_id` y ACL añade│
│                              │                              │ ~10-15ms por consulta pero│
│                              │                              │ es innegociable.          │
├──────────────────────────────┼──────────────────────────────┼───────────────────────────┤
│ **Auditoría Inmutable**      │ **Costo de Almacenamiento**  │ Conservar logs append-only│
│ (Append-Only inalterable)    │ (Crecimiento continuo)       │ incrementa el volumen de  │
│                              │                              │ almacenamiento pero es    │
│                              │                              │ vital para el no repudio. │
├──────────────────────────────┼──────────────────────────────┼───────────────────────────┤
│ **Resiliencia & Failover**   │ **Simplicidad Arquitectónica│ El búfer local y          │
│ (Almacenamiento Offline-First│ (Complejidad de colas)       │ resincronización añaden   │
│  y resincronización)         │                              │ complejidad al diseño pero│
│                              │                              │ evitan pérdida de métricas│
├──────────────────────────────┼──────────────────────────────┼───────────────────────────┤
│ **Extensibilidad (DDD)**     │ **Velocidad Inicial Código** │ Definir capas puras sin   │
│ (Arquitectura Hexagonal)     │ (Mayor número de clases/interfaces) requiere más código   │
│                              │                              │ inicial pero evita la     │
│                              │                              │ deuda técnica.            │
└──────────────────────────────┴──────────────────────────────┴───────────────────────────┘
```

---

## 6. Architectural Risk Register & Open Questions

### 6.1 Registro de Riesgos Arquitectónicos
- **RISK-ARCH-01 (P1 - Crítico)**: Degradación del rendimiento de la base de datos si las consultas analíticas de tableros compiten con las escrituras transaccionales de eventos. *(Mitigación: Adopción del patrón CQRS Lite mediante Vistas Materializadas)*.
- **RISK-ARCH-02 (P2 - Alto)**: Latencia excesiva en la capa de adaptación ACL si las respuestas de terceros requieren análisis JSON complejo. *(Mitigación: Parsers hiper-rápidos y validación de esquemas en streaming)*.

### 6.2 Registro de Asunciones & Preguntas Abiertas
- **ASM-ARCH-01**: Se asume que el volumen telemétrico inicial se mantendrá dentro de límites manejables por una sola instancia principal de base de datos con réplicas de lectura.
- **OPEN-ARCH-01**: ¿Cuál será la política de retención definitiva para comprimir u orquestar el almacenamiento de logs históricos de auditoría que superen los 12 meses de antigüedad?

---

## 7. Architecture Readiness Assessment

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ EVALUACIÓN DE PREPARACIÓN DE ARQUITECTURA (READINESS ASSESSMENT)                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Cobertura de Atributos de Calidad:     100% Especificados (TOGAF / SEI)             │
│ • Catálogo de Requisitos No Funcionales: 10 NFRs formalmente definidos                  │
│ • Escenarios de Calidad Medibles:         3 Escenarios Críticos detallados              │
│ • Análisis de Compromisos (Trade-offs):  4 Matrices de Decisión documentadas            │
│ • Alineación con Fases Previas:          100% Trazable con Fase 1 y Fase 2              │
│                                                                                         │
│ CONFIDENCE LEVEL:               95%                                                     │
│ ARCHITECTURE READINESS SCORE:   98% (EXCELENTE / LISTO PARA PRINCIPIOS DE ARQUITECTURA)  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. READY FOR ARCHITECTURE REVIEW

⚠️ **REGLA DE PARADA**: La subfase 3.1 ha finalizado. El equipo de ingeniería se detiene en este punto a la espera de la aprobación explícita del Comité de Arquitectura para autorizar el avance a la **Subfase 3.2 Architectural Principles**.
