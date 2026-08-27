# GESTIVASEC_ENTERPRISE_SOC_ARCHITECTURE.md — MASTER OPERATIONAL BLUEPRINT

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `LOCKED & APPROVED`  
**Architectural Baseline:** Hexagonal Architecture + Domain-Driven Design (DDD)  
**Governance:** EOS V1.0 (Project Kernel Status: `LOCKED`)  
**Target Ecosystem:** GestivaOne, Marketplace, Festa, Infrastructure, Cloud, Containers, Network & Third-Party Integrations  
**Date:** 2026-07-26  

---

## 1. VISION ESTRATÉGICA E INVARIANTES DEL SISTEMA

Gestiva Security no es únicamente un panel de monitoreo visual; es el **Centro de Operaciones de Seguridad (SOC) y SIEM Enterprise** diseñado para monitorear, detectar, correlacionar, investigar y responder de manera autónoma ante incidentes de ciberseguridad en todo el ecosistema de GestivaOne.

### 1.1 Invariantes Arquitectónicos
1. **Desacoplamiento Estricto de Capas:** Las interfaces de usuario y paneles visuales son únicamente consumidores desacoplados. La arquitectura funcional (backend, lógica de dominio, motores telemétricos) opera de forma autónoma.
2. **Tecnología Agnóstica & Heterogénea:** Los colectores de eventos y agentes son independientes de los paneles y servicios de persistencia.
3. **Multi-Tenancy por Diseño (*BR-0004*):** Cada entidad, evento, activo, alerta, incidente y log está aislado lógicamente por `organization_id`.
4. **Trazabilidad e Inmutabilidad (*BR-0005*):** Los registros de auditoría y evidencias de incidentes son inalterables (Append-Only Store).

---

## 2. TAXONOMÍA DE LOS 16 DOMINIOS DE NEGOCIO (BOUNDED CONTEXTS)

```
                       +-------------------------------------------------------+
                       |              GESTIVA SECURITY ENTERPRISE              |
                       +-------------------------------------------------------+
                                                   |
    +-----------------------+----------------------+-----------------------+
    |                       |                      |                       |
[ CORE PLATFORM ]    [ SOC OBSERVABILITY ]   [ DETECTION & SIEM ]   [ SOAR & RESPONSE ]
 • IAM                • Asset Management      • Event Collection     • Incident Mgmt
 • Administration     • Discovery Engine      • Normalization        • Case Mgmt
 • Multi-Tenancy      • Monitoring Engine     • Detection Engine     • SOAR / Automation
                      • Threat Intel          • Correlation Engine   • Notification Engine
                                              • Reporting Engine
```

### 2.1 Identity & Access Management (IAM)
- **Responsabilidades:** Autenticación (JWT/OAuth2), Autorización RBAC/ABAC, control de sesiones activas, lista negra de tokens invalidados.
- **Límites:** Exclusivamente credenciales, identidades de usuarios y permisos.
- **Entidades:** `User`, `Role`, `Permission`, `UserSession`, `Organization`.
- **Servicios:** `AuthenticationService`, `SessionService`, `AuthorizationService`.
- **Eventos:** `UserAuthenticated`, `UserLoggedOut`, `RoleAssigned`, `PermissionRevoked`.

### 2.2 Asset Management (Gestión de Activos)
- **Responsabilidades:** Inventario unificado y categorización de todos los activos de la infraestructura corporativa.
- **Límites:** Modelado de componentes físicos, virtuales y lógicos con su nivel de criticidad.
- **Entidades:** `Asset`, `NetworkInterface`, `ServiceEndpoint`, `TLSCertificate`, `AssetOwner`.
- **Servicios:** `AssetInventoryService`, `AssetCriticalityCalculator`.
- **Eventos:** `AssetRegistered`, `AssetUpdated`, `AssetDecommissioned`, `TLSExpiringNotice`.

### 2.3 Discovery Engine (Motor de Descubrimiento Pasivo y Activo)
- **Responsabilidades:** Escaneo e identificación automática de subdominios, puertos abiertos, huellas digitales de SO, servicios activos e interfaces de red.
- **Límites:** Sondaje pasivo y descubrimiento dinámico de red.
- **Entidades:** `DiscoveryJob`, `DiscoveredHost`, `DiscoveredService`, `PortScanResult`.
- **Servicios:** `PassiveDiscoveryService`, `PortScannerAdapter`, `FingerprintEngine`.
- **Eventos:** `HostDiscovered`, `NewPortOpened`, `UnregisteredAssetDetected`.

### 2.4 Monitoring Engine (Motor de Observabilidad Sintética & Métricas)
- **Responsabilidades:** Sondaje periódico de disponibilidad HTTP/TLS/DNS, medición de latencia y tiempos de respuesta.
- **Límites:** Verificación activa de SLA/SLO y estado funcional.
- **Entidades:** `SyntheticProbe`, `ProbeResult`, `SLORecord`.
- **Servicios:** `SyntheticProbingService`, `UptimeCalculatorService`.
- **Eventos:** `ProbeFailed`, `ServiceLatencySpike`, `ServiceRestored`.

### 2.5 Event Collection (Capa de Recolección de Eventos)
- **Responsabilidades:** Ingesta de eventos provenientes de fuentes heterogéneas (Syslog, Windows Event Logs, Agents, SNMP, Cloud APIs, Webhooks, NetFlow, Suricata, Wazuh, Zeek).
- **Límites:** Recepción masiva e ingesta no bloqueante (High-throughput buffer).
- **Entidades:** `RawEvent`, `CollectorEndpoint`, `IngestionBatch`.
- **Servicios:** `SyslogCollector`, `WindowsEventCollector`, `WebhookCollectorService`.
- **Eventos:** `RawEventReceived`, `CollectionBufferOverflowWarning`.

### 2.6 Event Normalization (Motor de Normalización Schema GestivaSec)
- **Responsabilidades:** Transformación de formatos heterogéneos (JSON, XML, Syslog RFC5424, CEF) al esquema unificado **GestivaSec Event Schema (GES)**.
- **Límites:** Parser, enriquecimiento de IPs con GeoIP/ASN y validación de tipos.
- **Entidades:** `NormalizedEvent`, `FieldMappingRule`, `ParserDefinition`.
- **Servicios:** `EventNormalizationService`, `GeoIPEnricher`, `SchemaValidator`.
- **Eventos:** `EventNormalized`, `EventParsingFailed`.

### 2.7 Detection Engine (Motor de Detección Basado en Reglas)
- **Responsabilidades:** Evaluación de eventos individuales normalizados frente a reglas de firma, umbrales y patrones de comportamiento.
- **Límites:** Generación de hallazgos (*Findings*) y alertas (*Alerts*).
- **Entidades:** `DetectionRule`, `Finding`, `Alert`, `ThresholdPolicy`.
- **Servicios:** `RuleEvaluationEngine`, `FindingAggregatorService`.
- **Eventos:** `FindingGenerated`, `AlertTriggered`.

### 2.8 Correlation Engine (Motor de Correlación Multi-Evento y SIEM)
- **Responsabilidades:** Correlación espacio-temporal de múltiples eventos en ventanas de tiempo dinámicas, secuenciamiento de ataques, puntuación de riesgo (*Risk Scoring*) y mapeo al marco MITRE ATT&CK.
- **Límites:** Análisis multitrama entre diferentes fuentes de eventos.
- **Entidades:** `CorrelationRule`, `TimeWindow`, `AttackSequence`, `RiskScoreCard`.
- **Servicios:** `ComplexEventProcessingEngine (CEP)`, `MITREMapperService`, `RiskCalculator`.
- **Eventos:** `CorrelationPatternMatched`, `MultiStageAttackDetected`.

### 2.9 Incident Management (Centro de Gestión de Incidentes)
- **Responsabilidades:** Agregación de alertas correlacionadas en incidentes operacionales clasificados por criticidad (P1 Crítico, P2 Alto, P3 Medio, P4 Bajo).
- **Límites:** Ciclo de vida del incidente (Abierto, En Investigación, Contenido, Mitigado, Cerrado).
- **Entidades:** `Incident`, `IncidentTimeline`, `IncidentEvidenceLink`.
- **Servicios:** `IncidentManagementService`, `SeverityAssessorService`.
- **Eventos:** `IncidentCreated`, `IncidentEscalated`, `IncidentResolved`.

### 2.10 Case Management (Gestión de Casos e Investigación Forense)
- **Responsabilidades:** Agrupación de incidentes y evidencias para investigación forense en profundidad por analistas SOC.
- **Límites:** Manejo de artefactos forenses, notas de investigación y cadena de custodia.
- **Entidades:** `InvestigationCase`, `CaseArtifact`, `InvestigatorNote`, `EvidenceChain`.
- **Servicios:** `CaseManagementService`, `ForensicEvidenceService`.
- **Eventos:** `CaseOpened`, `EvidenceAttached`, `CaseClosed`.

### 2.11 Threat Intelligence (Motor de Inteligencia de Amenazas / IoC)
- **Responsabilidades:** Cotejo de indicadores de compromiso (IoCs: IPs maliciosas, Hashes SHA256, Dominios Phishing, YARA rules) contra fuentes de ciberamenazas.
- **Límites:** Base de datos de reputación e integración con feeds de ciberinteligencia.
- **Entidades:** `IoCRecord`, `ThreatFeed`, `ReputationScore`.
- **Servicios:** `ThreatIntelMatchingService`, `FeedIngestionService`.
- **Eventos:** `IoCMatchDetected`, `ThreatFeedUpdated`.

### 2.12 Notification Engine (Motor de Notificaciones & Alertas)
- **Responsabilidades:** Despacho multi-canal de alertas (Telegram, Discord, Slack, Webhooks, Correo electrónico, SMS).
- **Límites:** Entrega confiable con políticas de reintento y supresión de ruido.
- **Entidades:** `NotificationChannel`, `NotificationTemplate`, `DispatchLog`.
- **Servicios:** `NotificationDispatcherService`, `ChannelAdapterRegistry`.
- **Eventos:** `NotificationSent`, `NotificationDeliveryFailed`.

### 2.13 Automation / SOAR (Orquestación y Respuesta Automatizada)
- **Responsabilidades:** Ejecución de Playbooks automáticos en respuesta a incidentes de seguridad (bloqueo de IP en firewall, revocación de sesión de usuario, aislamiento de host).
- **Límites:** Acciones de respuesta activa y remediación.
- **Entidades:** `Playbook`, `PlaybookStep`, `ExecutionLog`.
- **Servicios:** `SOAROrchestratorService`, `PlaybookExecutionEngine`.
- **Eventos:** `PlaybookTriggered`, `RemediationActionExecuted`.

### 2.14 Reporting Engine (Motor de Reportes Ejecutivos y Cumplimiento)
- **Responsabilidades:** Generación de informes de postura de seguridad, métricas de tiempo medio de detección (MTTD/MTTR) y cumplimiento normativo (ISO 27001, SOC2).
- **Límites:** Resúmenes analíticos y reportes en PDF/JSON/CSV.
- **Entidades:** `ReportTemplate`, `GeneratedReport`, `ComplianceMetric`.
- **Servicios:** `ReportGeneratorService`, `ComplianceMetricCalculator`.
- **Eventos:** `ReportGenerated`.

### 2.15 Administration (Administración del Sistema SOC)
- **Responsabilidades:** Configuración global de la plataforma, licencias, mantenimiento de nodos y parámetros de retención telemétrica.
- **Límites:** Gestión interna de la plataforma.
- **Entidades:** `PlatformConfig`, `RetentionPolicy`, `LicenseState`.
- **Servicios:** `PlatformAdminService`, `DataRetentionService`.
- **Eventos:** `PlatformConfigUpdated`.

### 2.16 Multi-Tenancy Boundary Engine
- **Responsabilidades:** Aislamiento y control de límites lógicos entre organizaciones/tenants (*BR-0004*).
- **Entidades:** `TenantContext`, `TenantQuota`.
- **Servicios:** `TenantIsolationService`.
- **Eventos:** `TenantQuotaExceeded`.

---

## 3. ARQUITECTURA UNIFICADA DE EVENTOS (GESTIVASEC EVENT SCHEMA)

Todo evento procesado en GestivaSec se normaliza dentro del siguiente esquema estandarizado antes de ingresar al Pipeline de Detección y Correlación:

```json
{
  "event_id": "8f3b2a1c-9d0e-4f5a-8b2c-1d3e5f7a9b0c",
  "organization_id": "00000000-0000-0000-0000-000000000001",
  "timestamp": "2026-07-26T16:05:00.000Z",
  "ingested_at": "2026-07-26T16:05:00.120Z",
  "observer": {
    "collector_id": "syslog-collector-01",
    "collector_type": "SYSLOG_RFC5424",
    "ip": "192.168.1.50"
  },
  "source": {
    "ip": "203.0.113.45",
    "port": 49201,
    "hostname": "workstation-corp-04",
    "user_id": "user-982",
    "user_email": "attacker@external.com"
  },
  "destination": {
    "ip": "10.0.0.15",
    "port": 443,
    "hostname": "auth.gestivaone.com",
    "asset_id": "asset-auth-sso"
  },
  "event": {
    "category": "AUTHENTICATION",
    "action": "LOGIN_FAILED",
    "severity": "HIGH",
    "outcome": "FAILURE",
    "protocol": "HTTPS"
  },
  "enrichment": {
    "geo_ip": { "country": "US", "city": "Ashburn", "asn": "AS16509" },
    "threat_intel": { "matched": true, "score": 85.0, "threat_type": "KNOWN_BRUTEFORCE_IP" }
  },
  "raw_ref": "s3://gestivasec-raw-evidence/2026/07/26/raw-8f3b2a1c.log"
}
```

### 3.1 Ciclo de Vida Estandarizado de Detección
1. **Raw Event:** Evento crudo sin procesar recibido por el colector.
2. **Finding:** Anomalía individual detectada por una regla de firma.
3. **Alert:** Notificación generada al superar umbrales de criticidad.
4. **Incident:** Agregación de alertas correlacionadas que representan una amenaza operacional.
5. **Case:** Caso de investigación asignado a un analista SOC.
6. **Investigation:** Análisis forense activo y recopilación de evidencias.
7. **Resolution:** Cierre formal del incidente con lecciones aprendidas y remediación aplicada.

---

## 4. PIPELINE DE PROCESAMIENTO MULTI-ETAPA

El pipeline telemétrico de GestivaSec consta de 10 etapas independientes y desacopladas:

```
[ Colectores ]
      ↓
[ Normalización ]
      ↓
[ Validación ]
      ↓
[ Correlación ]
      ↓
[ Detección ]
      ↓
[ Análisis de Riesgo ]
      ↓
[ Generación de Incidentes ]
      ↓
[ Gestión de Casos ]
      ↓
[ Notificaciones ]
      ↓
[ Reportes & SOAR ]
```

---

## 5. ARQUITECTURA DE ALMACENAMIENTO POLÍGLOTA

Para garantizar un rendimiento óptimo de ingesta sin acoplar la base de datos relacional, la arquitectura de datos se divide en 5 almacenes especializados:

| Almacén | Tecnología Objetivo | Responsabilidad |
| :--- | :--- | :--- |
| **Operational DB** | PostgreSQL / SQLite (Dev) | Usuarios, Activos, Reglas, Configuración, Estados de Incidentes. |
| **Telemetry Storage** | TimescaleDB / ClickHouse | Ingesta masiva de métricas y eventos telemétricos normalizados. |
| **Evidence Vault** | MinIO / AWS S3 | Almacenamiento inmutable de evidencias forenses y logs crudos. |
| **Audit Storage** | Append-Only Log Store | Registro inmutable de auditoría de seguridad (*BR-0005*). |
| **Long-Term Archive** | Cold Storage / Glacier | Archivo histórico para cumplimiento normativo a largo plazo. |

---

## 6. HOJA DE RUTA DE IMPLEMENTACIÓN DEL PRODUCTO (ROADMAP)

Una vez completado el diseño arquitectónico, el desarrollo continuará de forma secuencial:

1. **Sprint 1 (Completado):** Dashboard SOC Operativo en Tiempo Real (10 Widgets telemétricos en vivo).
2. **Sprint 2:** Asset Discovery Engine (Descubrimiento automático de IP, Hostname, SO, Puertos, Latencia).
3. **Sprint 3:** Asset Inventory (Gestión unificada de activos de primera clase).
4. **Sprint 4:** Event Collectors (Colectores Syslog, JSON, Windows Events).
5. **Sprint 5:** Event Normalization (Parser al esquema GestivaSec GES).
6. **Sprint 6:** Correlation Engine (Correlación multi-evento y ventanas de tiempo).
7. **Sprint 7:** Detection Engine (Motor de reglas y firmas de seguridad).
8. **Sprint 8:** Alert Center (Centro unificado de alertas).
9. **Sprint 9:** Incident Management (Gestión de ciclo de vida de incidentes).
10. **Sprint 10:** Case Management (Investigaciones forenses).
11. **Sprint 11:** Threat Intelligence (Integración de IoCs y YARA).
12. **Sprint 12:** Notification Engine (Integraciones Telegram, Discord, Webhooks).
13. **Sprint 13:** SOAR & Playbooks (Automatización y respuesta activa).
