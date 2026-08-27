# SOC INCIDENT CENTER & CONSOLE SPECIFICATION (INCIDENT_CENTER_SPEC.md)

---

## 1. OBJETIVO DE LA PANTALLA
Gestionar el ciclo de vida completo de los incidentes de seguridad e interrupciones críticas operativas del ecosistema **GestivaOne**. Permite investigar evidencias telemétricas, asignar analistas responsables y forzar el cumplimiento estricto de la regla **`BR-0001` (Cierre P1 exige informe RCA)**.

---

## 2. USUARIO OBJETIVO
- **Tier 1 (SOC Operator)**: Registro de incidentes iniciales y escalamiento a Tier 2.
- **Tier 2 / 3 (Incident Responder / Lead Analyst)**: Investigación, contención, mitigación y redacción de Causa Raíz (RCA).
- **SOC Manager**: Auditoría del cumplimiento del ciclo de vida y tiempos de resolución (MTTR).

---

## 3. CASOS DE USO
1. **Caso 1: Triaje de Incidente Crítico P1**: Abrir un nuevo incidente originado por la regla `BR-03` (3 fallas sintéticas consecutivas).
2. **Caso 2: Transición de Estado**: Transicionar un incidente de `NEW` a `INVESTIGATING` y luego a `CONTAINED`.
3. **Caso 3: Cierre Obligatorio con RCA (`BR-0001`)**: Transicionar a `CLOSED_WITH_RCA` ingresando la justificación técnica de Causa Raíz.
4. **Caso 4: Asignación de Analista Responsable**: Asignar el incidente al correo de un analista autenticado.
5. **Caso 5: Registro de Notas de Evidencia**: Agregar entradas a la cronología de investigación del incidente.

---

## 4. WIREFRAME TEXTUAL ASCII COMPLETO

```
+---------------------------------------------------------------------------------------------------------+
| [NAV] Dashboard | Assets | Passive Discovery | Threat Intel | Alerts | Incident Center* | Audit Logs   |
+---------------------------------------------------------------------------------------------------------+
| BREADCRUMB: GestivaSec / SOC Incident Center / Incident INC-001                                         |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  +---------------------------------------------------------------------------------------------------+  |
|  | INCIDENT DETAILS: INC-001 | Falla Crítica de Disponibilidad en GestivaOne Core Web Portal             |  |
|  | Severity: [P1 CRITICAL] | Status: [INVESTIGATING] | Assigned: analyst@gestivaone.com                 |  |
|  | Created: 2026-07-25 20:34:12 UTC | Target: https://gestivaone.com                                   |  |
|  +---------------------------------------------------------------------------------------------------+  |
|                                                                                                         |
|  +---------------------------------------------------+ +---------------------------------------------+  |
|  | EVIDENCE & TELEMETRY LOGS                         | | LIFECYCLE TRANSITION CONSOLE (BR-0001)       |  |
|  | - Synthetic Observation: HTTP Status 500 (Fail)   | | Select Target Status:                       |  |
|  | - Latency: 504.0ms                                | | [ ] NEW  [X] INVESTIGATING  [ ] CONTAINED   |  |
|  | - Error: 500 Internal Server Error                | | [ ] MITIGATED  [ ] CLOSED_WITH_RCA          |  |
|  | - Rule Triggered: BR-03 (3 Consecutive Failures)  | |                                             |  |
|  |                                                   | | Root Cause Analysis (RCA) Report (Required):|  |
|  | INVESTIGATION NOTES:                              | | +-----------------------------------------+ |  |
|  | [20:35:00] Analista asignado a la investigación.   | | | Enter mandatory RCA report before       | |  |
|  | [20:40:00] Worker pod restarted. Latency nominal. | | | transitioning status to CLOSED...       | |  |
|  |                                                   | | +-----------------------------------------+ |  |
|  | [➕ Add Note]                                     | | [Apply Status Transition]                 |  |
|  +---------------------------------------------------+ +---------------------------------------------+  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 5. JERARQUÍA VISUAL
1. **Prioridad 1**: Encabezado del Incidente con ID semántico (`INC-001`), severidad (`CRITICAL`), estado actual y botón de transición.
2. **Prioridad 2**: Panel de Formulario RCA y Transición de Estado (`BR-0001`).
3. **Prioridad 3**: Historial de Evidencias Telemétricas y Notas Cronológicas de Investigación.

---

## 6. WIDGETS & CONTROLES

### 6.1 Widget: Lifecycle Transition Form
- **Fuente de Datos**: `POST /api/v1/incidents/{incident_id}/transition`
- **Regla de Negocio `BR-0001`**: Si se selecciona `CLOSED_WITH_RCA`, el campo de texto RCA Report es estrictamente obligatorio. Si se envía vacío, el sistema rechaza la solicitud con HTTP 400.
- **Acción**: `[Apply Status Transition]`.

---

## 7. ACCESIBILIDAD Y DEFINICIÓN DE HECHO
- **Accesibilidad**: Tecla `Esc` cancela la edición de notas, navegabilidad completa por `Tab`, alertas de pantalla (*Screen Readers*) al cambiar de estado.
- **Definition of Done**: Especificación aprobada, 100% de pruebas unitarias pasando, enforzamiento de la regla `BR-0001` verificado en test suite.
