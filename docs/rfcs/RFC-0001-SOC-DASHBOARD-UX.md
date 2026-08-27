# RFC-0001: ENTERPRISE SOC DASHBOARD & CONTINUOUS PASSIVE OBSERVABILITY UX

---

## 1. HEADER
- **RFC Number**: RFC-0001
- **Version**: 1.0.0
- **Status**: APPROVED
- **Author**: Principal Product Architect & UX Engineer
- **Date**: 2026-07-25
- **Reviewers**: Architecture Review Board (ARB), SOC Operations Lead
- **Related RFCs**: N/A
- **Dependencies**: `PROJECT_GENESIS.md` Constitution, Backend Baseline v0.1.0

---

## 2. PROBLEM STATEMENT
Los analistas y operadores de SOC enfrentan una alta carga cognitiva y fatiga visual al intentar identificar amenazas e interrupciones del servicio en interfaces administrativas tradicionales de tipo CRUD. La falta de visibilidad en tiempo real de activos críticos, la dispersión telemétrica y la ausencia de correlación cronológica incrementan el Tiempo Medio de Detección (MTTD) a más de 15 minutos por evento.

---

## 3. CONTEXT
- **Estado Actual**: GestivaSec V1 cuenta con un motor Backend funcional (IAM, Activos, Inspección Pasiva de 10 vectores, Scheduler distribuido, Inteligencia de Amenazas e Incidentes), pero la interfaz visual inicial requiere una arquitectura de experiencia de usuario (*Product Experience*) diseñada específicamente para consolas de seguridad tipo SOC.
- **Limitaciones**: Interfaces genéricas ocultan información crítica de disponibilidad y requieren múltiples clics para acceder al informe de Causa Raíz (RCA).
- **Dolores del Usuario**: Dificultad para priorizar incidentes P1 y verificar el cumplimiento de las reglas invariantes `BR-0001` a `BR-0005`.

---

## 4. RESEARCH
Se analizaron los patrones de experiencia de usuario y jerarquía visual de consolas Enterprise líderes:
- **CrowdStrike Falcon**: Uso de tarjetas KPI de severidad con código de color estricto e indicadores de estado luminosos.
- **Datadog / Grafana**: Paneles oscuros tipo *Dark-First* (`#0B0F17`) con alta densidad de datos y gráficos de latencia en milisegundos.
- **Microsoft Defender XDR**: Navegación directa en 2 clics desde la alerta hasta el expediente del incidente y telemetría de activos.

---

## 5. ALTERNATIVES
1. **Alternativa 1: Interfaz Administrativa Genérica (Tabla CRUD)**
   - *Ventajas*: Rápida de construir.
   - *Desventajas*: Alta carga cognitiva, imposibilidad de priorizar incidentes en < 5s.
   - *Veredicto*: **DESCARTADA**.
2. **Alternativa 2: Múltiples Dashboards Separados (Páginas Independientes)**
   - *Ventajas*: Aislamiento de módulos.
   - *Desventajas*: Navegación fragmentada, incrementa el MTTD y requiere más de 5 clics por investigación.
   - *Veredicto*: **DESCARTADA**.
3. **Alternativa 3: Consola SOC Unificada "Single Pane of Glass" con Design System Dark-First**
   - *Ventajas*: Visualización centralizada en < 5s, navegación en 2 clics max, enforzamiento visual de invariantes `BR-01..BR-05`.
   - *Desventajas*: Requiere diseño estricto y tokens de diseño consolidados.
   - *Veredicto*: **SELECCIONADA Y PROUESTA (RFC-0001)**.

---

## 6. PROPOSED SOLUTION
Implementar la Consola SOC Unificada basada en el Design System oficial (`DESIGN_SYSTEM.md`) estructurada en 4 zonas de alta densidad telemétrica:
- **Zona 1: Header & Scope Gate**: Contexto multi-tenant aislado (`BR-04`).
- **Zona 2: KPI Metrics Cards**: Activos totales, Composite Threat Score (0-100), Incidentes P1 Activos y Estado del Scheduler.
- **Zona 3: Surface & Critical Alerts Panels**: Enumeración pasiva de subdominios y alimentación de alertas en tiempo real.
- **Zona 4: Chronological Event Stream**: Stream cronológico del Timeline del SOC.

---

## 7. UX IMPACT
- **Reducción de Tiempo de Detección**: De 15 minutos a **menos de 5 segundos**.
- **Reducción de Clics**: Pasar de una Alerta Crítica al Informe RCA (`BR-0001`) en **máximo 2 clics**.
- **Carga Cognitiva**: Reducida mediante código de color normativo (`#EF4444` Critical, `#F97316` High, `#F59E0B` Warning, `#10B981` Healthy).

---

## 8. RISKS
- **Riesgo Técnico**: Saturación por refresco de datos en tiempo real (Mitigado mediante debounce de 5s y WebSocket opcional).
- **Riesgo de Performance**: Renderizado de listas largas de eventos en el Timeline (Mitigado mediante virtualización de listas).

---

## 9. SUCCESS METRICS
- **MTTD Target**: < 5 segundos para detectar incidentes P1.
- **Navegación**: <= 2 clics para el flujo completo de investigación.
- **Cobertura Automatizada**: 100% de tests de arquitectura y fitness verdes.

---

## 10. ROLLOUT PLAN
- **Fase 1**: Aprobación oficial del RFC-0001 por el ARB. *(COMPLETADO)*
- **Fase 2**: Publicación de especificaciones de pantalla (`DASHBOARD_SPEC.md`, `INCIDENT_CENTER_SPEC.md`). *(COMPLETADO)*
- **Fase 3**: Implementación del Frontend SPA reactivo en modo oscuro siguiendo el Design System.
- **Fase 4**: Verificación del flujo E2E Golden Demo y emisión de la Release v0.1.0.

---

## 11. OPEN QUESTIONS
- *¿Se requerirá soporte offline para el estado del Dashboard?*  
  **Respuesta**: No en v0.1.0; se mostrará un banner explícito de estado degradado si falla la conexión HTTP con el backend.
