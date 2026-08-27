# PROJECT GENESIS — GESTIVA SECURITY (GESTIVASEC V1) CONSTITUTION

---

## 1. VISIÓN DEL PRODUCTO (PRODUCT VISION)
Gestiva Security no es un SIEM, no es un NOC y no es un escáner intrusivo.
Es una plataforma corporativa de **Continuous Passive Security Observability** diseñada para proteger el ecosistema de **GestivaOne** mediante el monitoreo pasivo continuo de disponibilidad, certificados, DNS, cabeceras e inteligencia de amenazas.

---

## 2. REGLAS INVIOLABLES DE ARQUITECTURA (INVARIANTS)
- **`BR-0001`**: Cierre de incidentes P1 exige informe de causa raíz (`CLOSED_WITH_RCA`).
- **`BR-0002`**: Todo activo digital registrado exige un correo de propietario verificado (`owner_email`).
- **`BR-0003`**: Tres (3) fallas sintéticas consecutivas desencadenan automáticamente un Incidente Crítico P1.
- **`BR-0004`**: Frontera estricta de aislamiento multi-tenant por Organización (`X-Organization-ID`).
- **`BR-0005`**: Registro de auditoría *append-only* (no modificable ni eliminable).

---

## 3. ARQUITECTURA TÉCNICA (TECHNICAL ARCHITECTURE)
- **Core Backend**: Python 3.13, FastAPI, Asyncio, Pydantic V2, Bcrypt.
- **Frontend SPA**: HTML5, Vanilla CSS Design System (Dark-First SOC Aesthetics), JavaScript ES6.
- **Persistencia**: PostgreSQL (Esquema relacional y migraciones SQL) + Redis Cache.
- **Telemetría**: Prometheus Engine, Healthcheck endpoints.

---

## 4. SOC CAPABILITY ROADMAP (CAP-01 A CAP-10)
- **CAP-01 Identity & Access Management**: Login, JWT, Multi-Tenant Orgs, Users, RBAC, OAuth. *(DONE)*
- **CAP-02 Digital Asset Inventory**: Registro vivo de activos y verificación de propietarios. *(DONE)*
- **CAP-03 Passive Discovery Engine**: Descubrimiento de 10 vectores (DNS, Subdominios, ASN, WHOIS, CDN, TLS, Headers, Fingerprints). *(DONE)*
- **CAP-04 Continuous Monitoring Engine**: Scheduler distribuido (1m HTTP, 5m DNS, 1h TLS) y almacén de cambios. *(DONE)*
- **CAP-05 Incident Response & SOC Console**: Centro de gestión de incidentes y RCA.
- **CAP-06 Threat Intelligence Feed**: Enriquecimiento con VirusTotal, AbuseIPDB, GreyNoise, CISA KEV, NVD. *(DONE)*
- **CAP-07 Security Alert Engine**: Motor de correlación de reglas y severidad.
- **CAP-08 Timeline Engine**: Correlación cronológica de eventos del SOC.
- **CAP-09 SOC Executive Dashboard**: Consola operativa gráfica unificada.
- **CAP-10 Observability & Automation**: Prometheus, Loki, Workers y colas de tareas.

---

## 5. QUALITY GATES & FITNESS CRITERIA
- **Domain Purity**: Cero importaciones de infraestructura en módulos de dominio.
- **Circular Imports**: Cero importaciones circulares en el código backend.
- **Technical Debt Bounds**: 0 marcas `FIXME`, TODOs < 10, funciones < 150 líneas, clases < 300 líneas.
- **Test Cobertura**: Mínimo 80% de cobertura automatizada en Pytest.
- **Golden Demo**: Flujo End-to-End continuo verificado verde en cada cambio.
