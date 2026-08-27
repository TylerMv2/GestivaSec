# 4.2 FUNCTIONAL REQUIREMENTS SPECIFICATION (FRS) — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `FUNCTIONAL_REQUIREMENTS_SPECIFICATION.md`  
> **Phase**: PHASE 4.2 — FUNCTIONAL REQUIREMENTS SPECIFICATION  
> **Purification Status**: 100% Layer Pure (L2 Functional Requirements Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **4.2 Functional Requirements Specification (FRS)** especifica el catálogo formal de Requisitos Funcionales de **Gestiva Security (GestivaSec V1)**. Este documento establece de manera exhaustiva y determinista el comportamiento funcional del sistema, detallando para cada requisito sus actores, entradas, salidas, precondiciones, postcondiciones, reglas de negocio, criterios de aceptación, condiciones de error, prioridad, trazabilidad y dependencias, sin incorporar decisiones de implementación, tecnologías, lenguajes, estructuras de base de datos ni umbrales técnicos de infraestructura.

---

## 2. Functional Requirements Catalog (Catálogo de Requisitos Funcionales)

### FR-0001: Registrar y Catalogar Activo Digital
- **ID**: `FR-0001`
- **Nombre**: Registrar y Catalogar Activo Digital en Inventario
- **Descripción**: La plataforma debe permitir registrar un activo tecnológico en el inventario único de la organización, asociándolo a una ubicación o identificador de destino autorizado, nivel de criticidad y propietario responsable.
- **Actores**: Responsable de Confiabilidad, Administrador del Sistema.
- **Entradas**: Nombre del activo, identificador de destino, nivel de criticidad inicial, correo del propietario, organización de pertenencia.
- **Salidas**: Activo registrado con identificador inmutable en estado registrado.
- **Precondiciones**: La ubicación o identificador de destino debe pertenecer a la lista de dominios o activos autorizados.
- **Postcondiciones**: El activo queda habilitado para la supervisión automática de disponibilidad.
- **Reglas de Negocio**: `BR-02` (Todo activo debe tener un propietario asignado).
- **Criterios de Aceptación**:
  1. El sistema valida el formato de la ubicación de destino.
  2. El sistema asigna un identificador de activo único e inalterable.
  3. El activo se asocia obligatoriamente a la organización del usuario solicitante.
- **Condiciones de Error**:
  - `ERR-001.1`: Ubicación no pertenece a la lista de destinos autorizados.
  - `ERR-001.2`: Omisión del responsable del activo.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Inventario de Activos.
- **Dependencias**: Ninguna.

---

### FR-0002: Ejecutar Sondeo Sintético de Disponibilidad
- **ID**: `FR-0002`
- **Nombre**: Ejecutar Sondeo Sintético de Disponibilidad
- **Descripción**: El sistema debe realizar verificaciones de disponibilidad sintética periódicas sobre la ubicación del activo registrado, midiendo el tiempo de respuesta y el estado de disponibilidad del servicio.
- **Actores**: Evaluador de Disponibilidad Sintética (Proceso Automático).
- **Entradas**: Identificador de activo, ubicación de destino, parámetros de evaluación.
- **Salidas**: Registro del resultado de evaluación (tiempo de respuesta, estado de disponibilidad, marca de tiempo) y actualización de salud.
- **Precondiciones**: El activo debe encontrarse en estado activo.
- **Postcondiciones**: Si la evaluación detecta un número configurado de fallos repetidos consecutivos, el estado de la evaluación cambia a fallido y se emite la notificación correspondiente.
- **Reglas de Negocio**: `BR-03` (Confirmación de fallas repetidas declara automáticamente un incidente crítico).
- **Criterios de Aceptación**:
  1. La evaluación mide el tiempo de respuesta del servicio.
  2. La acumulación de fallos repetidos confirmados dispara el evento de falla de disponibilidad.
- **Condiciones de Error**:
  - `ERR-002.1`: Tiempo de espera agotado al conectar con el activo objetivo.
  - `ERR-002.2`: Respuesta de error o estado no disponible en el servicio supervisado.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Observabilidad Sintética.
- **Dependencias**: `FR-0001`.

---

### FR-0003: Inspeccionar Vigencia de Acreditaciones Digitales
- **ID**: `FR-0003`
- **Nombre**: Inspeccionar Vigencia de Acreditaciones Digitales
- **Descripción**: La plataforma debe inspeccionar periódicamente la validez de las acreditaciones y certificados digitales asociados al activo, verificando la fecha de vencimiento y anticipando riesgos de caducidad.
- **Actores**: Monitor de Acreditaciones Digitales.
- **Entradas**: Ubicación del activo supervisado.
- **Salidas**: Información de vigencia de la acreditación (fecha de emisión, fecha de expiración, entidad emisora, tiempo restante).
- **Precondiciones**: El activo debe contar con acreditaciones digitales habilitadas.
- **Postcondiciones**: Si el tiempo de vigencia restante alcanza el umbral de advertencia preventiva, se genera la alerta de caducidad próxima.
- **Reglas de Negocio**: Emisión preventiva de alertas al alcanzar el plazo limite fijado por la organización.
- **Criterios de Aceptación**:
  1. El sistema determina el tiempo restante de validez del certificado.
  2. Generar notificación de advertencia al alcanzar el plazo preventivo establecido.
- **Condiciones de Error**:
  - `ERR-003.1`: Acreditación no válida o cadena de validación no reconocida.
  - `ERR-003.2`: Imposibilidad de verificar la información de la acreditación.
- **Prioridad**: **Alta (P2)**
- **Trazabilidad**: Módulo de Observabilidad Sintética.
- **Dependencias**: `FR-0001`.

---

### FR-0004: Declaración Automática y Triaje de Incidente Crítico
- **ID**: `FR-0004`
- **Nombre**: Declaración Automática y Triaje de Incidente Crítico
- **Descripción**: Al recibir la confirmación de una falla de disponibilidad repetida, el sistema debe generar automáticamente un expediente de incidente clasificado con prioridad crítica.
- **Actores**: Gestor de Incidentes (Proceso Automático), Operador de Turno.
- **Entradas**: Evento de falla de disponibilidad confirmada (identificador de activo, causa de falla, marca de tiempo).
- **Salidas**: Expediente de incidente creado en estado declarado con identificador y plazo de solución asignado.
- **Precondiciones**: Confirmación de la falla repetida en la evaluación de disponibilidad (`FR-0002`).
- **Postcondiciones**: Notificación inmediata enviada al operador de guardia e inicio del tiempo de solución.
- **Reglas de Negocio**: `BR-03` (Generación automática de incidente crítico), `BR-01` (Informe de causa raíz obligatorio para cierre).
- **Criterios de Aceptación**:
  1. Creación del expediente de incidente de forma inmediata tras recibir la confirmación de la falla.
  2. Asignación automática de prioridad crítica.
  3. Determinación de la fecha límite de solución según la prioridad.
- **Condiciones de Error**:
  - `ERR-004.1`: Fallo al enviar la notificación de apertura de incidente.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Gestión de Incidentes.
- **Dependencias**: `FR-0002`.

---

### FR-0005: Gestión del Ciclo de Vida y Asignación de Incidentes
- **ID**: `FR-0005`
- **Nombre**: Gestión del Ciclo de Vida y Asignación de Incidentes
- **Descripción**: Permitir a los operarios actualizar el estado del incidente a través de sus fases (Declarado ➔ Asignado ➔ En Diagnóstico ➔ Remediado), registrando responsables y observaciones de trabajo.
- **Actores**: Operador de Red, Analista de Ciberseguridad, Responsable de Confiabilidad.
- **Entradas**: Identificador de incidente, nuevo estado, usuario asignado, notas de diagnóstico.
- **Salidas**: Expediente actualizado con registro de cambio de estado y marcas de tiempo.
- **Precondiciones**: El incidente debe existir y no estar en estado cerrado.
- **Postcondiciones**: Registro auditado del cambio de estado del incidente.
- **Reglas de Negocio**: Las modificaciones de estado deben corresponder a los permisos asignados al rol del usuario.
- **Criterios de Aceptación**:
  1. El sistema verifica que el usuario disponga de los permisos requeridos para realizar el cambio de estado.
  2. Cada actualización registra la identidad del usuario y la fecha y hora de la modificación.
- **Condiciones de Error**:
  - `ERR-005.1`: Intento de cambio de estado no permitido por el flujo de trabajo.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Gestión de Incidentes.
- **Dependencias**: `FR-0004`.

---

### FR-0006: Requerimiento y Validación Obligatoria de Informe RCA
- **ID**: `FR-0006`
- **Nombre**: Requerimiento y Validación Obligatoria de Informe de Causa Raíz (RCA) para Cierre
- **Descripción**: La plataforma debe impedir el cierre de cualquier incidente crítico si no se ha registrado previamente un informe completo de Análisis de Causa Raíz (RCA).
- **Actores**: Responsable de Operaciones, Director Técnico / Aprobador.
- **Entradas**: Identificador de incidente, detalle de Causa Raíz, acciones correctivas aplicadas.
- **Salidas**: Informe RCA asociado al incidente y actualización del expediente a estado cerrado.
- **Precondiciones**: El incidente crítico debe encontrarse en estado remediado.
- **Postcondiciones**: Expediente de incidente cerrado definitivamente.
- **Reglas de Negocio**: `BR-01` (Cierre de incidente crítico bloqueado si no incluye informe RCA).
- **Criterios de Aceptación**:
  1. Solicitar el cierre de un incidente crítico sin informe RCA genera el rechazo explicito de la operación.
  2. Registrar el informe RCA permite completar la transición al estado cerrado.
- **Condiciones de Error**:
  - `ERR-006.1`: Intento de cierre de incidente crítico con campos del informe RCA incompletos.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Gestión de Incidentes.
- **Dependencias**: `FR-0005`.

---

### FR-0007: Registrar y Clasificar Hallazgos de Ciberseguridad
- **ID**: `FR-0007`
- **Nombre**: Registrar y Clasificar Hallazgos de Ciberseguridad
- **Descripción**: El módulo de seguridad debe permitir registrar hallazgos y vulnerabilidades detectadas en los activos, clasificándolos según marcos normativos y niveles de severidad.
- **Actores**: Analista de Ciberseguridad.
- **Entradas**: Identificador de activo, categoría de seguridad, nivel de severidad (Crítica, Alta, Media, Baja), descripción del hallazgo.
- **Salidas**: Hallazgo de seguridad registrado con identificador inmutable.
- **Precondiciones**: El activo asociado debe estar registrado en el inventario.
- **Postcondiciones**: Hallazgos de severidad crítica generan automáticamente un expediente de atención en el módulo de incidentes.
- **Reglas de Negocio**: Clasificación obligatoria bajo las categorías formales del sistema.
- **Criterios de Aceptación**:
  1. El sistema valida que la categoría y severidad pertenezcan a los catálogos oficiales.
  2. Hallazgos críticos generan la solicitud de atención correspondiente.
- **Condiciones de Error**:
  - `ERR-007.1`: Categoría de seguridad o nivel de severidad no válido.
- **Prioridad**: **Alta (P2)**
- **Trazabilidad**: Módulo de Seguridad y Postura.
- **Dependencias**: `FR-0001`.

---

### FR-0008: Enforzar Aislamiento Lógico de Datos por Organización
- **ID**: `FR-0008`
- **Nombre**: Enforzar Aislamiento Lógico de Datos por Organización
- **Descripción**: Toda consulta, registro o procesamiento sobre la información de la plataforma debe requerir y validar obligatoriamente la organización de pertenencia del usuario solicitante.
- **Actores**: Todos los usuarios y servicios del sistema.
- **Entradas**: Contexto de sesión del usuario autenticado con la identificación de su organización.
- **Salidas**: Operación ejecutada exclusivamente dentro del ámbito de la organización del usuario o rechazo por falta de autorización.
- **Precondiciones**: Usuario o servicio autenticado.
- **Postcondiciones**: Cero acceso a información perteneciente a otras organizaciones.
- **Reglas de Negocio**: `BR-04` (Delimitación estricta de la información por organización).
- **Criterios de Aceptación**:
  1. Las consultas filtran la información garantizando la pertenencia a la organización del usuario.
  2. Intentos de acceder a recursos de otra organización son bloqueados y registrados en la auditoría.
- **Condiciones de Error**:
  - `ERR-008.1`: Ausencia o incoherencia en la identificación de la organización solicitante.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Control de Acceso y Organizaciones.
- **Dependencias**: Ninguna (Transversal).

---

### FR-0009: Captura Inalterable e Inmutable de Registro de Auditoría
- **ID**: `FR-0009`
- **Nombre**: Captura Inalterable e Inmutable de Registro de Auditoría
- **Descripción**: La plataforma debe registrar de forma automática e inalterable cualquier acción de usuario, modificación de activo o actualización de incidente en la traza de auditoría de solo adición.
- **Actores**: Bóveda de Auditoría (Proceso de Gobierno).
- **Entradas**: Identidad del usuario, acción ejecutada, tipo de registro, identificador del recurso, detalles del cambio, fecha y hora.
- **Salidas**: Registro de auditoría inalterable conservado en la traza de gobierno.
- **Precondiciones**: Ocurrencia de cualquier operación o cambio en el sistema.
- **Postcondiciones**: Imposibilidad de modificar o eliminar el registro generado.
- **Reglas de Negocio**: `BR-05` (Inmutabilidad absoluta de los registros de auditoría).
- **Criterios de Aceptación**:
  1. El sistema genera un registro de auditoría para todas las operaciones ejecutadas.
  2. El sistema rechaza cualquier solicitud de modificación o eliminación sobre los registros de auditoría.
- **Condiciones de Error**:
  - `ERR-009.1`: Intento de alteración o borrado de un registro de auditoría.
- **Prioridad**: **Crítica (P1)**
- **Trazabilidad**: Módulo de Auditoría y Gobierno.
- **Dependencias**: Ninguna (Transversal).

---

### FR-0010: Despacho y Canalización Inteligente de Notificaciones Operacionales
- **ID**: `FR-0010`
- **Nombre**: Despacho y Canalización Inteligente de Notificaciones Operacionales
- **Descripción**: El sistema debe filtrar, agrupar y canalizar notificaciones de alerta ante la declaración de incidentes críticos o advertencias de acreditaciones por vencer hacia los destinatarios asignados.
- **Actores**: Despachador de Notificaciones.
- **Entradas**: Eventos de alertas de disponibilidad, advertencias de acreditaciones o apertura de incidentes.
- **Salidas**: Notificación distribuida a los responsables asignados.
- **Precondiciones**: Generación de un evento que requiera notificación.
- **Postcondiciones**: Notificación entregada evitando la duplicación por eventos repetidos en una misma ventana de tiempo.
- **Reglas de Negocio**: Agrupación de alertas repetidas para prevenir la sobrecarga de notificaciones.
- **Criterios de Aceptación**:
  1. La notificación se despacha de forma oportuna tras la ocurrencia del evento.
  2. Alertas idénticas recibidas dentro de la ventana de agrupación se entregan consolidadas.
- **Condiciones de Error**:
  - `ERR-010.1`: Fallo de entrega en la canalización de la notificación.
- **Prioridad**: **Alta (P2)**
- **Trazabilidad**: Módulo de Notificaciones.
- **Dependencias**: `FR-0002`, `FR-0004`.

---

## 3. CRUD Matrix (Matriz CRUD por Entidad de Dominio)

| Entidad / Concepto | Create (Crear) | Read (Consultar) | Update (Actualizar) | Delete (Eliminar) |
| :--- | :---: | :---: | :---: | :---: |
| **Activo Digital** | `FR-0001` (Responsable Confiabilidad) | `FR-0001` (Usuarios Autorizados) | `FR-0001` (Responsable Confiabilidad) | Estado Desincorporado |
| **Sonda Sintética** | `FR-0002` (Automático / Admin) | `FR-0002` (Operadores) | `FR-0002` (Administrador) | Estado Pausado |
| **Incidente Operacional**| `FR-0004` (Automático / Operaciones)| `FR-0005` (Usuarios Autorizados) | `FR-0005`, `FR-0006` (Operadores / SOC) | Prohibido (Preservación Histórica) |
| **Hallazgo de Seguridad**| `FR-0007` (Analista SOC / Auto) | `FR-0007` (SOC / Dirección) | `FR-0007` (Analista SOC) | Prohibido (Preservación Histórica) |
| **Registro de Auditoría**| `FR-0009` (Automático) | `FR-0009` (Auditor / Dirección) | **Prohibido (`BR-05`)** | **Prohibido (`BR-05`)** |

---

## 4. Feature Matrix (Matriz de Funcionalidades por Módulo)

| Módulo | Requisitos Funcionales Asociados | Roles Autorizados | Nivel de Criticidad |
| :--- | :--- | :--- | :---: |
| **Módulo de Observabilidad Sintética** | `FR-0002`, `FR-0003` | Operadores de Red, Confiabilidad | **Crítica (P1)** |
| **Módulo de Gestión de Incidentes** | `FR-0004`, `FR-0005`, `FR-0006` | Operadores de Red, Ciberseguridad, Dirección | **Crítica (P1)** |
| **Módulo de Seguridad y Postura** | `FR-0007` | Analistas de Ciberseguridad | **Alta (P2)** |
| **Módulo de Inventario de Activos** | `FR-0001` | Responsables de Confiabilidad, Admin | **Crítica (P1)** |
| **Módulo de Auditoría y Gobierno** | `FR-0009` | Auditores de Cumplimiento, Dirección | **Crítica (P1)** |
| **Módulo de Control de Acceso y Organizaciones** | `FR-0008` | Transversal (Todos) | **Crítica (P1)** |
| **Módulo de Notificaciones** | `FR-0010` | Operadores, Confiabilidad | **Alta (P2)** |
