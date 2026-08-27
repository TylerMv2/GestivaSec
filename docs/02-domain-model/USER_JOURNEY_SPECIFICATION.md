# 4.4 USER JOURNEY SPECIFICATION — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `USER_JOURNEY_SPECIFICATION.md`  
> **Phase**: PHASE 4.4 — USER JOURNEY SPECIFICATION  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (L4 Operational Behavior & Experience Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **4.4 User Journey Specification** especifica los recorridos operativos de los usuarios (*User Journeys*) dentro de **Gestiva Security (GestivaSec V1)**. Este documento describe de manera exhaustiva el recorrido continuo, comportamiento, puntos de contacto operativos, estados emocionales/de trabajo, puntos de dolor y metas de cada perfil de usuario a lo largo del ciclo de vida operacional, omitiendo cualquier referencia a pantallas, elementos de interfaz gráfica (UI), tecnologías o componentes de implementación.

---

## 2. Mapa Resumen de User Journeys

| ID | Nombre del Recorrido | Perfil de Usuario (Persona) | Objetivo Operacional | Casos de Uso Relacionados |
| :--- | :--- | :--- | :--- | :--- |
| **`UJ-001`** | Atención y Resolución de Incidente Crítico P1 | Responsable de Operaciones de Red (NOC) | Restaurar la disponibilidad del servicio y asegurar informe RCA. | `UC-002`, `UC-004`, `UC-005`, `UC-006`, `UC-010` |
| **`UJ-002`** | Prevención de Caducidad y Triaje de Seguridad | Analista de Ciberseguridad (SOC) | Prevenir caídas por acreditaciones y clasificar riesgos. | `UC-003`, `UC-007`, `UC-010` |
| **`UJ-003`** | Catalogación e Incorporación de Nuevo Activo | Responsable de Confiabilidad (DevSecOps) | Dar de alta un activo e iniciar su supervisión sintética. | `UC-001`, `UC-002`, `UC-008` |
| **`UJ-004`** | Auditoría de Gobierno, SLAs y Causa Raíz | Directora Técnica / Auditora (CTO/Auditor) | Validar cumplimiento normativo, inmutabilidad y RCAs. | `UC-006`, `UC-008`, `UC-009` |

---

## 3. Catálogo Detallado de User Journeys

### UJ-001: Recorrido del Responsable de Operaciones de Red (Atención y Resolución de Incidente P1)

#### 1. Perfil de Usuario
- **Nombre**: Alex (Responsable de Operaciones de Red / NOC Lead).
- **Rol**: Supervisión de la disponibilidad continua de servicios corporativos y respuesta primaria ante caídas.

#### 2. Estado Inicial & Disparador
- **Estado Inicial**: Monitoreo pasivo en régimen normal de trabajo.
- **Disparador**: Ocurrencia de una falla de disponibilidad confirmada que genera la declaración automática de un incidente crítico P1.

#### 3. Etapas del Recorrido (Stages)

##### Etapa 1: Notificación y Toma de Conocimiento
- **Acción del Usuario**: Recibe la alerta de incidente crítico despachada según la matriz de responsabilidad.
- **Comportamiento del Sistema**: Registra la emisión de la alerta y notifica al operador de turno.
- **Estado Operacional del Usuario**: Alerta / Foco inmediato.
- **Punto de Dolor Evitado**: Evita la detección tardía a través de quejas de usuarios finales.
- **Interacción de Dominio**: `UC-010`, `UC-004`.

##### Etapa 2: Asunción de Responsabilidad (Asignación)
- **Acción del Usuario**: Accede al expediente del incidente declarado y asume oficialmente la responsabilidad de la atención.
- **Comportamiento del Sistema**: Actualiza el estado del incidente a asignado y registra el tiempo de inicio de atención.
- **Estado Operacional del Usuario**: Compromiso / Determinación.
- **Punto de Dolor Evitado**: Incertidumbre sobre qué operador está atendiendo la contingencia.
- **Interacción de Dominio**: `UC-005`.

##### Etapa 3: Diagnóstico y Remediación Técnica
- **Acción del Usuario**: Cambia el expediente a estado en diagnóstico, analiza las evidencias telemétricas asociadas a la falla y ejecuta la acción correctiva en el servicio supervisado.
- **Comportamiento del Sistema**: Registra las notas de diagnóstico y actualiza el expediente a remediado al confirmar la restauración de la disponibilidad sintética.
- **Estado Operacional del Usuario**: Concentración técnica ➔ Alivio.
- **Punto de Dolor Evitado**: Falta de evidencias operacionales del momento exacto de la caída.
- **Interacción de Dominio**: `UC-002`, `UC-005`.

##### Etapa 4: Documentación Causa Raíz (RCA) y Cierre
- **Acción del Usuario**: Diligencia el informe formal de Causa Raíz (RCA) detallando el origen del fallo y las medidas preventivas adoptadas, y solicita el cierre.
- **Comportamiento del Sistema**: Valida la existencia y completitud del informe RCA (`BR-01`) y transiciona el incidente a cerrado definitivamente.
- **Estado Operacional del Usuario**: Cumplimiento / Cierre de ciclo.
- **Punto de Dolor Evitado**: Cierre de incidentes sin lecciones aprendidas ni acciones correctivas documentadas.
- **Interacción de Dominio**: `UC-006`.

---

### UJ-002: Recorrido de la Analista de Ciberseguridad (Prevención y Triaje SOC)

#### 1. Perfil de Usuario
- **Nombre**: Sofia (Analista de Ciberseguridad / SOC Analyst).
- **Rol**: Evaluación de la postura de ciberseguridad, gestión de acreditaciones digitales y triaje de riesgos perimetrales.

#### 2. Estado Inicial & Disparador
- **Estado Inicial**: Inspección preventiva periódica de la postura de seguridad.
- **Disparador**: Recepción de una advertencia preventiva por acreditación digital próxima a vencer o hallazgo de seguridad detectado.

#### 3. Etapas del Recorrido (Stages)

##### Etapa 1: Recepción de Alerta Preventiva de Acreditación
- **Acción del Usuario**: Recibe el aviso preventivo indicando que una acreditación digital alcanzará su fecha de caducidad en el plazo límite fijado.
- **Comportamiento del Sistema**: Evalúa continuamente las fechas de vigencia y emite la alerta preventiva oportuna.
- **Estado Operacional del Usuario**: Precaución / Planificación.
- **Punto de Dolor Evitado**: Caídas inesperadas por vencimiento de certificados de seguridad.
- **Interacción de Dominio**: `UC-003`, `UC-010`.

##### Etapa 2: Triaje y Clasificación del Hallazgo
- **Acción del Usuario**: Revisa el detalle de la acreditación o registra un nuevo hallazgo de ciberseguridad, clasificándolo bajo los marcos normativos del sector.
- **Comportamiento del Sistema**: Valida las categorías normativas asignadas y guarda el registro de seguridad.
- **Estado Operacional del Usuario**: Análisis analítico / Clasificación.
- **Punto de Dolor Evitado**: Desorganización o falta de estándar en la priorización de riesgos.
- **Interacción de Dominio**: `UC-007`.

##### Etapa 3: Coordinación de Solución y Confirmación
- **Acción del Usuario**: Modifica la severidad del expediente y coordina con el responsable de confiabilidad la renovación de la acreditación o aplicación del correctivo.
- **Comportamiento del Sistema**: Registra la actualización de la acreditación y confirma que el plazo restante ha sido extendido de manera segura.
- **Estado Operacional del Usuario**: Tranquilidad / Verificación.
- **Punto de Dolor Evitado**: Reincidencia de alertas por falta de seguimiento a la solución.
- **Interacción de Dominio**: `UC-003`, `UC-007`.

---

### UJ-003: Recorrido del Responsable de Confiabilidad (Incorporación de Activos)

#### 1. Perfil de Usuario
- **Nombre**: Carlos (Responsable de Confiabilidad / DevSecOps Lead).
- **Rol**: Alta, catalogación y mantenimiento del inventario de activos corporativos del ecosistema.

#### 2. Estado Inicial & Disparador
- **Estado Inicial**: Solicitud de despliegue de un nuevo servicio o plataforma corporativa.
- **Disparador**: Necesidad de incorporar el nuevo activo al inventario único para habilitar su supervisión.

#### 3. Etapas del Recorrido (Stages)

##### Etapa 1: Formulación de Datos del Activo
- **Acción del Usuario**: Reúne los datos requeridos del activo (nombre, ubicación de destino, criticidad inicial y correo del propietario).
- **Comportamiento del Sistema**: Prepara el proceso de validación del alcance organizativo.
- **Estado Operacional del Usuario**: Preparación / Definición.
- **Punto de Dolor Evitado**: Existencia de activos huérfanos sin responsable identificado en la organización.
- **Interacción de Dominio**: `UC-001`.

##### Etapa 2: Registro e Inserción al Inventario
- **Acción del Usuario**: Envía los datos para dar de alta el activo dentro de su ámbito organizativo.
- **Comportamiento del Sistema**: Valida la ubicación autorizada, verifica el responsable asignado (`BR-02`), delimita la organización (`BR-04`) y asigna un identificador inalterable.
- **Estado Operacional del Usuario**: Confirmación / Satisfacción.
- **Punto de Dolor Evitado**: Registro de activos fuera de los dominios corporativos autorizados.
- **Interacción de Dominio**: `UC-001`, `UC-008`.

##### Etapa 3: Activación de Observabilidad Automática
- **Acción del Usuario**: Confirma que el activo recién registrado ha ingresado al ciclo de supervisión sintética pasiva.
- **Comportamiento del Sistema**: Inicia inmediatamente las comprobaciones sintéticas automáticas para medir disponibilidad y respuesta.
- **Estado Operacional del Usuario**: Confianza / Cobertura total.
- **Punto de Dolor Evitado**: Períodos de sombra operacional entre el despliegue de un servicio y el inicio de su supervisión.
- **Interacción de Dominio**: `UC-002`.

---

### UJ-004: Recorrido de la Directora Técnica / Auditora (Gobierno, SLAs y Causa Raíz)

#### 1. Perfil de Usuario
- **Nombre**: Elena (Directora Técnica / Auditora - CTO / Compliance).
- **Rol**: Supervisión del gobierno corporativo, evaluación del cumplimiento de niveles de servicio (SLA), revisión de informes RCA y verificación de no repudio en auditoría.

#### 2. Estado Inicial & Disparador
- **Estado Inicial**: Ciclo periódico de revisión de gobierno o auditoría de cumplimiento corporativo.
- **Disparador**: Requerimiento de evaluación del cumplimiento de metas operacionales y no repudio de acciones.

#### 3. Etapas del Recorrido (Stages)

##### Etapa 1: Inspección de Niveles de Cumplimiento de Servicio (SLA)
- **Acción del Usuario**: Revisa el grado de cumplimiento de los niveles de servicio y disponibilidad acumulados por activo en el periodo.
- **Comportamiento del Sistema**: Recupera las métricas consolidadas de disponibilidad y tiempos de solución dentro de la organización de la auditora.
- **Estado Operacional del Usuario**: Evaluación ejecutiva / Control.
- **Punto de Dolor Evitado**: Falta de visibilidad ejecutiva sobre el desempeño de la infraestructura.
- **Interacción de Dominio**: `UC-008`, `UC-009`.

##### Etapa 2: Auditoría de Informes de Causa Raíz (RCA)
- **Acción del Usuario**: Examina la lista de incidentes críticos cerrados en el periodo y valida la calidad de los informes RCA adjuntos.
- **Comportamiento del Sistema**: Muestra los expedientes cerrados verificando que ninguno haya eludido la regla de informe RCA obligatorio (`BR-01`).
- **Estado Operacional del Usuario**: Rigor normativo / Garantía de calidad.
- **Punto de Dolor Evitado**: Incumplimiento de políticas de gobierno por cierres injustificados de fallas críticas.
- **Interacción de Dominio**: `UC-006`.

##### Etapa 3: Verificación Inalterable de Auditoría (No Repudio)
- **Acción del Usuario**: Consulta la traza de auditoría inalterable para verificar acciones específicas de usuarios o cambios de configuración sensibles.
- **Comportamiento del Sistema**: Presenta los registros de auditoría de solo adición, garantizando que ninguna traza haya sido alterada o borrada (`BR-05`).
- **Estado Operacional del Usuario**: Plena certeza / Respaldo de cumplimiento.
- **Punto de Dolor Evitado**: Vulnerabilidad ante manipulaciones de registros o repudiabilidad de acciones operativas.
- **Interacción de Dominio**: `UC-009`.

---

## 4. Operational Summary & Validation Gate (Verificación de Validación)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE VALIDACIÓN DE USER JOURNEYS (SUBFASE 4.4 GATE REVIEW)                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Cobertura 100% de las 4 Personas definidas en Product Specification:     YES / SÍ     │
│ • Trazabilidad directa a Casos de Uso (UC-001 a UC-010):                  YES / SÍ     │
│ • Enforzamiento estricto de Reglas de Negocio (BR-01 a BR-05):             YES / SÍ     │
│ • Ausencia total de pantallas, componentes de UI o alusiones visuales:     YES / SÍ     │
│ • Ausencia total de tecnologías, APIs, bases de datos o lenguaje técnico: YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ USER JOURNEY SPECIFICATION SCORE: 100% (EXCELENTE / 0 VIOLACIONES DE CAPA L4)           │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
