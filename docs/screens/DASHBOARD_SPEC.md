# SOC EXECUTIVE OVERVIEW DASHBOARD SPECIFICATION (DASHBOARD_SPEC.md)

---

## 1. OBJETIVO DE LA PANTALLA
Proporcionar una consola centralizada de observación continua de la postura de seguridad en tiempo real (*Single Pane of Glass*) para el ecosistema **GestivaOne**. Permite identificar en menos de 5 segundos la disponibilidad de activos, el nivel de amenaza (*Threat Score*), incidentes activos P1 y alertas críticas sin depender de escaneos intrusivos.

---

## 2. USUARIO OBJETIVO
- **Tier 1 (SOC Operator)**: Detección rápida de caídas HTTP, alertas y sondeos sintéticos.
- **Tier 2 / 3 (SOC Analyst / Incident Responder)**: Correlación de eventos y transición a la consola de incidentes.
- **SOC Manager**: Supervisión del cumplimiento de SLAs de disponibilidad y resolución de incidentes.
- **Executive (CISO / Director Security)**: Estado de postura global y Threat Score de la organización.

---

## 3. CASOS DE USO
1. **Caso 1: Diagnóstico en 5 Segundos**: Identificar si existe algún activo en estado de falla crítica (`CRITICAL` / `HTTP 500`).
2. **Caso 2: Selección de Tenant Multi-Organizaciones**: Conmutar el contexto de visualización entre `GestivaOne Corporation` y `Festa Event Systems` (`BR-04`).
3. **Caso 3: Correlación de Alertas e Incidentes**: Pasar directamente desde el widget de Top Alertas a la Consola de Incidentes en 1 clic.
4. **Caso 4: Verificación de Cadencia de Monitoreo**: Comprobar la ejecución periódica de trabajos sintéticos y pasivos de 1m, 5m y 1h.
5. **Caso 5: Control de Postura de Amenazas**: Evaluar variaciones en el Threat Score compuesto (0 a 100).

---

## 4. WIREFRAME TEXTUAL ASCII COMPLETO

```
+---------------------------------------------------------------------------------------------------------+
| [LOGO] GESTIVASEC SOC CONSOLE | Org: [GestivaOne Corporation v] | Status: [HEALTHY] | User: admin@gestiva |
+---------------------------------------------------------------------------------------------------------+
| [NAV] Dashboard* | Assets | Passive Discovery | Threat Intel | Alerts | Incident Center | Audit Logs    |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  +-----------------------+ +-----------------------+ +-----------------------+ +---------------------+  |
|  | TOTAL MONITORED ASSETS | | COMPOSITE THREAT SCORE| | ACTIVE INCIDENTS (P1) | | SCHEDULER HEALTH    |  |
|  |         127           | |   12 / 100 (SAFE)     | |      1 (P1 CRITICAL)   | | 1m: OK | 5m: OK    |  |
|  +-----------------------+ +-----------------------+ +-----------------------+ +---------------------+  |
|                                                                                                         |
|  +---------------------------------------------------+ +---------------------------------------------+  |
|  | ATTACK SURFACE & SUBDOMAINS (PASSIVE DISCOVERY)   | | TOP CRITICAL ALERTS FEED                    |  |
|  | Domain: gestivaone.com (104.21.55.12 - AS13335)     | | [CRITICAL] HTTP 500 in Core Web Portal     |  |
|  | Subdomains Discovered: 5                          | | [HIGH] Security Header Missing (CSP)        |  |
|  | - api.gestivaone.com (A: 104.21.55.12)            | | [WARNING] TLS Cert Expires in 14 Days      |  |
|  | - app.gestivaone.com (A: 104.21.55.13)            | | [INFO] New Subdomain Discovered (vpn)      |  |
|  | - auth.gestivaone.com (A: 104.21.55.14)           | |                                             |  |
|  | [⚡ Run Passive Scan Now]                          | | [View All Alerts ->]                        |  |
|  +---------------------------------------------------+ +---------------------------------------------+  |
|                                                                                                         |
|  +---------------------------------------------------------------------------------------------------+  |
|  | CHRONOLOGICAL SOC TIMELINE STREAM (REAL-TIME EVENTS)                                               |  |
|  | [20:34:12] ALERT | Critical HTTP 500 Error recorded for GestivaOne Portal                            |  |
|  | [20:30:00] SCHEDULER | Job [job-1m-http] executed successfully (Latency: 42.1ms)                     |  |
|  | [20:25:00] DISCOVERY | Passive scan baseline completed. SSL Grade: A+                                 |  |
|  +---------------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 5. JERARQUÍA VISUAL
1. **Zona 1 (Prioridad 1 - Top Bar & Context)**: Tenant selector de Organización (`BR-04`) y estado de salud del sistema.
2. **Zona 2 (Prioridad 1 - Metric KPI Cards)**: Activos totales, Threat Score (0-100), Incidentes P1 Activos y Estado del Scheduler.
3. **Zona 3 (Prioridad 2 - Central Operational Panels)**: Superficie de ataque (Subdominios pasivos) y Alimentación de Top Alertas Críticas.
4. **Zona 4 (Prioridad 3 - Bottom Activity Feed)**: Transmisión cronológica del Timeline de eventos.

---

## 6. WIDGETS

### 6.1 Widget: Composite Threat Score Gauge
- **Fuente de Datos**: `GET /api/v1/threat-intel/report/{asset_id}`
- **Frecuencia de Actualización**: 12 Horas (en caché) o bajo demanda.
- **Estados**: Safe (0-20), Low (21-40), Medium (41-60), High (61-80), Critical (81-100).
- **Acciones**: Clic abre modal de desglose VirusTotal / AbuseIPDB / CISA KEV.

### 6.2 Widget: Top Critical Alerts Feed
- **Fuente de Datos**: `GET /api/v1/alerts`
- **Frecuencia de Actualización**: En tiempo real (WebSockets / Polling 5s).
- **Acciones**: Clic en alerta resalta el incidente correspondiente en la Consola SOC.

---

## 7. NAVEGACIÓN Y ACCESOS RÁPIDOS
- **Breadcrumb**: `SOC Console / Executive Dashboard`
- **Teclas de Atajo**:
  - `Ctrl + Shift + D`: Volver al Dashboard principal.
  - `Ctrl + Shift + I`: Abrir la Consola de Incidentes.
  - `Ctrl + Shift + A`: Abrir Inventario de Activos.

---

## 8. ESTADOS DE INTERFAZ
- **Loading**: Skeleton pulsing grid de 4 tarjetas y 2 paneles.
- **Error**: Banner emergente de error con botón `[Reintentar Conexión]`.
- **Empty**: *"Organización activa no posee activos registrados. [➕ Registrar Activo]"*.
- **Permission Denied**: Banner indicando *"Rol no autorizado para visualizar telemetría avanzada"*.

---

## 9. RESPONSIVIDAD Y ACCESIBILIDAD
- **Responsive**: Ultrawide (4 columnas), Desktop (4 columnas), Tablet (2 columnas), Mobile (1 columna vertical).
- **Accesibilidad**: Cumplimiento WCAG 2.1 AAA, ratio de contraste > 7:1 en fondos oscuros (`#0B0F17`), soporte nativo de lectores de pantalla (*ARIA live regions* para alertas en tiempo real).
