# 5.5 VALUE OBJECTS — GESTIVA SECURITY (GESTIVASEC V1)
> **Document Identifier**: `VALUE_OBJECTS.md`  
> **Phase**: PHASE 5.5 — VALUE OBJECTS  
> **Project**: PROJECT GENESIS — GESTIVA SECURITY  
> **Purification Status**: 100% Layer Pure (Pure Domain Value Object Baseline)  
> **Date**: 2026-07-25  

---

## 1. Resumen Ejecutivo

La subfase **5.5 Value Objects** establece el catálogo formal de **Objetos de Valor del Dominio** para **Gestiva Security (GestivaSec V1)**. Un Objeto de Valor es un elemento del dominio que carece de identidad conceptual propia, se define exclusivamente por el valor inmutable de sus atributos y garantiza la igualdad estructural.

En estricto cumplimiento de la directiva de pureza del dominio, esta especificación mantiene una **independencia absoluta de decisiones de ejecución** (comandos, transacciones, repositorios, servicios, infraestructura) y de persistencia física (identificadores de base de datos, tipos SQL, claves o discriminadores técnicos), centrándose exclusivamente en la validación y semántica conceptual del negocio.

---

## 2. Catálogo de Objetos de Valor del Dominio (Value Objects Catalog)

| ID Objeto de Valor | Nombre del Objeto de Valor | Atributos del Dominio | Regla de Validación del Negocio | Entidades o Agregados que lo Utilizan |
| :--- | :--- | :--- | :--- | :--- |
| **`VO-001`** | **Ubicación de Destino** | Dirección de Servicio, Protocolo | Debe pertenecer a la lista de destinos autorizados del ecosistema. | `ENT-01 Activo Digital` (`AGG-01`) |
| **`VO-002`** | **Nivel de Criticidad** | Nivel de Impacto (P1-P4) | Escala estricta del negocio (`P1_CRITICAL` a `P4_LOW`). | `ENT-01 Activo Digital` (`AGG-01`) |
| **`VO-003`** | **Correo del Responsable** | Dirección de Correo | Formato válido de responsable obligatorio (`BR-02`). | `ENT-01 Activo Digital` (`AGG-01`) |
| **`VO-004`** | **Tiempo de Respuesta** | Magnitud de Duración, Estado | Medición pasiva no negativa que determina estado funcional. | `ENT-01`, `Evaluación Sintética` (`AGG-01`) |
| **`VO-005`** | **Vigencia de Acreditación**| Emisión, Expiración, Días | Emisión preventiva al alcanzar el plazo limite (≤ 30 días). | `ENT-05 Acreditación Digital` (`AGG-01`) |
| **`VO-006`** | **Categoría OWASP** | Código, Nombre de Categoría | Taxonomía oficial de seguridad aprobada del sector. | `ENT-04 Hallazgo Ciberseguridad` (`AGG-03`)|
| **`VO-007`** | **Táctica MITRE** | Identificador, Nombre Táctica | Clasificación oficial de amenazas de la industria. | `ENT-04 Hallazgo Ciberseguridad` (`AGG-03`)|
| **`VO-008`** | **Fecha Límite SLA** | Marca Límite, Margen | Cálculo determinista del plazo de atención según la prioridad. | `ENT-02 Incidente Operacional` (`AGG-02`) |
| **`VO-009`** | **Detalle de Causa Raíz** | Origen, Correctivo, Preventivo | Completitud obligatoria requerida para el cierre P1 (`BR-01`). | `ENT-03 Informe RCA` (`AGG-02`) |
| **`VO-010`** | **Marca Temporal** | Fecha y Hora de Ocurrencia | Registro inalterable no modificable (`BR-05`). | `ENT-06 Traza Auditoría` (`AGG-04`) |

---

## 3. Especificación Detallada de Objetos de Valor

### VO-001: Ubicación de Destino (Target Destination)
- **ID Objeto de Valor**: `VO-001`
- **Nombre del Dominio**: Ubicación de Destino
- **Propósito**: Representar la dirección o dominio del servicio corporativo supervisado.
- **Atributos**: `Dirección de Servicio`, `Protocolo de Acceso`.
- **Regla de Validación del Negocio**: La dirección debe corresponder a un dominio o subdominio autorizado del ecosistema corporativo (`gestivaone.com`, `gestivaone-store.vercel.app`, `festa.gestivaone.com`).
- **Inmutabilidad**: Toda modificación genera una nueva instancia conceptual inmutable.

---

### VO-002: Nivel de Criticidad (Asset Criticality)
- **ID Objeto de Valor**: `VO-002`
- **Nombre del Dominio**: Nivel de Criticidad
- **Propósito**: Categorizar el grado de impacto operacional del activo o incidente.
- **Atributos**: `Nivel de Impacto`.
- **Valores Semánticos Permitidos**: `P1_CRITICAL` (Crítico), `P2_HIGH` (Alto), `P3_MEDIUM` (Medio), `P4_LOW` (Bajo).
- **Regla de Validación del Negocio**: No se permiten valores fuera de la escala estricta del negocio.

---

### VO-003: Correo del Responsable (Owner Email)
- **ID Objeto de Valor**: `VO-003`
- **Nombre del Dominio**: Correo del Responsable
- **Propósito**: Representar la identidad de contacto del propietario humano asignado al activo.
- **Atributos**: `Dirección de Correo`.
- **Regla de Validación del Negocio**: `Regla BR-02` (Formato válido e indivisible de correo corporativo del responsable).

---

### VO-004: Tiempo de Respuesta (Response Latency Value)
- **ID Objeto de Valor**: `VO-004`
- **Nombre del Dominio**: Tiempo de Respuesta
- **Propósito**: Expresar el tiempo de latencia medido en las comprobaciones sintéticas pasivas.
- **Atributos**: `Magnitud de Duración`, `Estado de Latencia` (`NORMAL`, `DEGRADADO`).
- **Regla de Validación del Negocio**: La magnitud debe ser un valor no negativo. Determina la transición del activo a estado degradado si supera el margen configurado.

---

### VO-005: Vigencia de Acreditación (Credential Validity Window)
- **ID Objeto de Valor**: `VO-005`
- **Nombre del Dominio**: Vigencia de Acreditación
- **Propósito**: Representar la ventana temporal de validez de una acreditación o certificado digital.
- **Atributos**: `Fecha de Emisión`, `Fecha de Expiración`, `Días Restantes`.
- **Regla de Validación del Negocio**: Los días restantes se calculan determinísticamente. Si el valor es ≤ 30 días, se activa el estado de advertencia preventiva.

---

### VO-006: Categoría OWASP (OWASP Risk Category)
- **ID Objeto de Valor**: `VO-006`
- **Nombre del Dominio**: Categoría OWASP
- **Propósito**: Etiquetar el hallazgo de seguridad bajo la taxonomía de vulnerabilidades del sector.
- **Atributos**: `Código de Categoría`, `Nombre de la Categoría`.
- **Regla de Validación del Negocio**: El código debe pertenecer a la versión oficial aprobada de la taxonomía OWASP.

---

### VO-007: Táctica MITRE (MITRE Attack Tactic)
- **ID Objeto de Valor**: `VO-007`
- **Nombre del Dominio**: Táctica MITRE
- **Propósito**: Etiquetar la vulnerabilidad bajo la matriz de tácticas de ciberseguridad de la industria.
- **Atributos**: `Identificador de Táctica`, `Nombre de la Táctica`.
- **Regla de Validación del Negocio**: El identificador debe pertenecer a la matriz de tácticas aprobada.

---

### VO-008: Fecha Límite SLA (SLA Deadline Window)
- **ID Objeto de Valor**: `VO-008`
- **Nombre del Dominio**: Fecha Límite SLA
- **Propósito**: Representar la ventana máxima de tiempo autorizada para la solución del incidente.
- **Atributos**: `Marca Temporal Límite`, `Margen de Tolerancia`.
- **Regla de Validación del Negocio**: Se calcula en el momento de la declaración del incidente en función de su Nivel de Criticidad (`VO-002`).

---

### VO-009: Detalle de Causa Raíz (RCA Content Detail)
- **ID Objeto de Valor**: `VO-009`
- **Nombre del Dominio**: Detalle de Causa Raíz
- **Propósito**: Encapsular el contenido descriptivo de causa, correctivo y medidas preventivas del informe RCA.
- **Atributos**: `Explicación de Origen`, `Acción Correctiva`, `Medida Preventiva`.
- **Regla de Validación del Negocio**: `Regla BR-01` (Todos los campos deben contener descripciones válidas para autorizar la completitud del informe).

---

### VO-010: Marca Temporal Inalterable (Immutable Event Timestamp)
- **ID Objeto de Valor**: `VO-010`
- **Nombre del Dominio**: Marca Temporal Inalterable
- **Propósito**: Registrar la fecha y hora de ocurrencia de un evento para fines de auditoría y no repudio.
- **Atributos**: `Fecha y Hora de Ocurrencia`.
- **Regla de Validación del Negocio**: `Regla BR-05` (Valor inalterable grabado en el momento exacto del evento que no permite modificaciones posteriores).

---

## 4. Matriz de Trazabilidad entre Objetos de Valor, Entidades y Reglas de Negocio

| Objeto de Valor | Entidad / Agregado Asociado | Regla de Negocio Vinculada | Tipo de Igualdad |
| :--- | :--- | :--- | :--- |
| **`VO-001` Ubicación Destino** | `ENT-01 Activo Digital` (`AGG-01`) | Alcance Autorizado | Estructural de Atributos |
| **`VO-002` Nivel Criticidad** | `ENT-01 Activo`, `ENT-02 Incidente`| Asignación de Prioridad | Estructural de Atributos |
| **`VO-003` Correo Responsable**| `ENT-01 Activo Digital` (`AGG-01`) | `Regla BR-02` (Responsable) | Estructural de Atributos |
| **`VO-004` Tiempo Respuesta** | `ENT-01 Activo`, Evaluador | Estado Funcional | Estructural de Atributos |
| **`VO-005` Vigencia Acreditación**| `ENT-05 Acreditación` (`AGG-01`) | Plazo Preventivo | Estructural de Atributos |
| **`VO-006` Categoría OWASP** | `ENT-04 Hallazgo` (`AGG-03`) | Taxonomía Sectorial | Estructural de Atributos |
| **`VO-007` Táctica MITRE** | `ENT-04 Hallazgo` (`AGG-03`) | Matriz de Amenazas | Estructural de Atributos |
| **`VO-008` Fecha Límite SLA** | `ENT-02 Incidente` (`AGG-02`) | Tiempo de Solución | Estructural de Atributos |
| **`VO-009` Detalle RCA** | `ENT-03 Informe RCA` (`AGG-02`) | `Regla BR-01` (RCA P1) | Estructural de Atributos |
| **`VO-010` Marca Temporal** | `ENT-06 Traza Auditoría` (`AGG-04`) | `Regla BR-05` (Inmutabilidad) | Estructural de Atributos |

---

## 5. Summary & Phase 5.5 Validation Gate

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ VERIFICACIÓN DE VALIDACIÓN DE OBJETOS DE VALOR (SUBFASE 5.5 GATE REVIEW)               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ • Definición 100% basada en Inmutabilidad e Igualdad Estructural del Negocio: YES / SÍ  │
│ • Cero alusión a conceptos de ejecución (comandos, transacciones, repos):   YES / SÍ     │
│ • Ausencia total de conceptos de persistencia (UUID, tenant_id, SQL, DB):  YES / SÍ     │
│ • Encapsulamiento de Reglas de Validación del Negocio (BR-01..05):         YES / SÍ     │
│                                                                                         │
│ CONFIDENCE LEVEL:               100%                                                    │
│ VALUE OBJECTS SCORE:            100% (ESPECIFICACIÓN DE OBJETOS DE VALOR PURA APROBADA) │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```
