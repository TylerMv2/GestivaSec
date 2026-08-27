# GESTIVA SECURITY (GESTIVASEC V1) — SOC PRODUCT BLUEPRINT & UX ARCHITECTURE

---

## 1. INTRODUCCIÓN Y MISIÓN DE UX
Gestiva Security no es una aplicación administrativa CRUD. Es una **Consola de Operaciones de Seguridad (SOC Operations Center)** diseñada para analistas y operadores que interactúan con la interfaz durante jornadas continuas de 8 a 10 horas.

### Principios Fundamentales de UX:
1. **Detección Rápida (< 5 Segundos)**: Toda falla crítica (HTTP 500, TLS Expirado, Invariante BR-03) debe ser visible de inmediato sin desplazar la pantalla.
2. **Baja Carga Cognitiva**: Uso estricto de colores de severidad (`CRITICAL` #EF4444, `HIGH` #F97316, `WARNING` #F59E0B, `INFO` #3B82F6) sobre fondo oscuro profundo (`#0B0F17`).
3. **Mínimos Clics (Navegación en 2 Clics)**: Un analista puede pasar de una Alerta Crítica al Informe de Causa Raíz (RCA) o la telemetría del activo en 2 clics como máximo.
4. **Visibilidad Continua de Invariantes**: Reglas `BR-0001` (Cierre con RCA), `BR-0002` (Owner Email), `BR-0003` (Falla sintética P1) y `BR-0004` (Contexto Multi-Tenant) siempre visibles.

---

## 2. MAPA COMPLETO DEL PRODUCTO (PRODUCT MAP)

```
GESTIVASEC SOC PLATFORM
├── 0. Auth & Session Gate
│   ├── Login Modal / Form (Bcrypt + JWT)
│   └── OAuth SSO Gate (Google, GitHub, GestivaOne)
├── 1. Executive SOC Overview Dashboard
│   ├── Executive Health KPI Pill Matrix (Healthy, Warning, Critical)
│   ├── Active Tenant Selector (BR-04 Multi-Tenant Scope)
│   ├── Threat Score Dial (0-100 Rating)
│   ├── Attack Surface Card (Discovered Subdomains & IPs)
│   ├── Latency & Availability Gauge Chart
│   ├── Top Critical Alerts Feed
│   └── Real-time Timeline Stream
├── 2. Asset Management & Living Inventory
│   ├── Digital Assets Grid (URL, Criticality, Owner Email)
│   ├── Active Owner Verification (BR-02)
│   └── Asset Modal & Registration Trigger
├── 3. Continuous Passive Observability & Monitoring
│   ├── HTTP Availability & Latency Prober
│   ├── Passive Subdomain Enumeration Engine (10 Vectors)
│   ├── TLS Certificate Inspection & Expiration Countdown
│   ├── Security Headers Audit Grade (A+ to F)
│   └── Distributed Scheduler Status (1m, 5m, 1h Jobs)
├── 4. Threat Intelligence Enrichment Feed
│   ├── VirusTotal, AbuseIPDB, GreyNoise, CISA KEV & NVD Panel
│   └── Composite Threat Score Audit
├── 5. Security Alert & Correlation Engine
│   └── Configurable Rules Feed (TLS, HTTP 500, Subdomain, Headers)
├── 6. SOC Incident Center & Console
│   ├── Incident Lifecycle Grid (NEW -> INVESTIGATING -> CONTAINED -> MITIGATED -> CLOSED_WITH_RCA)
│   └── BR-0001 RCA Enforcer & Evidence Logger
└── 7. System Administration & Audit Trail
    └── Append-Only Audit Log Viewer (BR-0005)
```

---

## 3. MAPA DE NAVEGACIÓN Y FLUJO DE INVESTIGACIÓN (NAVIGATION MAP)

### Flujo Principal de Investigación de Incidente:
```
[1. Login Gate] ──► [2. Executive SOC Dashboard] ──► [3. Top Alert Highlight] 
                              │
                              ▼
                  [4. Incident Console] ──► [5. Telemetry & Evidence] ──► [6. RCA Report & Closure (BR-01)]
```

- **Paso 1: Autenticación**: El analista ingresa credenciales o SSO.
- **Paso 2: Contexto Operativo**: El Dashboard muestra la matriz de salud general y la tarjeta del activo afectado.
- **Paso 3: Identificación de Alerta**: La vista resalta una alerta de severidad `CRITICAL` (por ejemplo, HTTP 500 o 3 fallas sintéticas `BR-03`).
- **Paso 4: Consola de Incidentes**: El analista hace clic en la alerta, abriendo el incidente en estado `INVESTIGATING`.
- **Paso 5: Inspección de Evidencias**: Se consulta la telemetría sintética y el informe de inspección pasiva.
- **Paso 6: Mitigación y Cierre con RCA (`BR-0001`)**: Se ingresa la causa raíz y se cierra el incidente.

---

## 4. ESTADOS DE INTERFAZ (UI STATES & DEGRADATION)

1. **Estado Normal (Operational State)**: Todas las tarjetas con bordes verde sutil (`#10B981`), latencia < 200ms, Threat Score < 20.
2. **Estado Degradado (Degraded State)**: Un activo presenta latencia > 1000ms o advertencia de expiración TLS (< 15 días). Borde amarillo (`#F59E0B`).
3. **Estado Crítico (Critical State)**: 3 fallas sintéticas consecutivas (`BR-03`) o HTTP 500. Borde rojo vibrante (`#EF4444`) con pulso de atención.
4. **Estado Vacío (Empty State)**: Mensaje ilustrado con indicación clara: *"No hay incidentes abiertos en esta organización"*.
5. **Estado de Carga (Loading State)**: Esqueletos animados (*Skeletons*) en lugar de spinners molestos.
6. **Estado Sin Datos (No Data State)**: Indicador de *"Ejecutar primer sondeo pasivo para generar telemetría"*.
