# GESTIVA SECURITY (GESTIVASEC V1) — STRATEGIC CAPABILITY ROADMAP & MATURITY MATRIX

---

## 1. DEPENDS ON (UPSTREAM DEPENDENCIES)
- **`docs/00-governance/PRODUCT_VISION.md`** (Product Constitution & Business Invariants `BR-0001` to `BR-0005`)
- **`docs/00-governance/QUALITY_GATES.md`** (Fitness Criteria & Quality Rules)

---

## 2. PROBLEM STATEMENT & STRATEGIC PURPOSE
Las plataformas de monitoreo tradicional sufren de fragmentación de herramientas, alta latencia en la detección de caídas de servicio y falta de priorización de riesgo. El **Strategic Capability Roadmap** de Gestiva Security establece la hoja de ruta de ingeniería para evolucionar la plataforma desde la infraestructura base de identidad hasta un motor completo de observabilidad pasiva continua, asegurando que cada capacidad entregada incremente directamente la efectividad operacional del SOC para el ecosistema **GestivaOne**.

---

## 3. MATURITY MATRIX & CAPABILITY PHASES

### FASE 1: FOUNDATION & IAM (`CAP-01`) — STATUS: RELEASED (v0.1.0)
- **`IAM-LOGIN`**: Autenticación segura mediante contraseñas Bcrypt y emisión de firmas JWT.
- **`IAM-ORGS`**: Aislamiento estricto de frontera multi-tenant por Organización (`BR-0004`).
- **`IAM-USERS`**: Gestión de usuarios corporativos y asignación de perfiles SOC (`SOC_ADMIN`, `SOC_ANALYST`, `SOC_OPERATOR`, `AUDITOR`).
- **`IAM-ROLES`**: Matriz RBAC de roles y responsabilidades.
- **`IAM-PERMS`**: Motor granular de autorización de permisos.
- **`IAM-OAUTH`**: Integración de Single Sign-On (SSO) con proveedores externos (Google, GitHub, GestivaOne).

### FASE 2: ASSET INVENTORY & PASSIVE DISCOVERY (`CAP-02`, `CAP-03`) — STATUS: OPERATIONAL
- **`AST-INVENTORY`**: Inventario vivo de activos digitales con verificación obligatoria de correo de propietario (`BR-0002`).
- **`DISCOVERY-10VECTORS`**: Descubrimiento no intrusivo de 10 vectores:
  1. *DNS Resolution*: Registros A, AAAA, MX, TXT, NS, CNAME.
  2. *Subdomains*: Cert Transparency (CRT.sh) & Passive DNS (`api`, `app`, `auth`, `store`, `vpn`).
  3. *ASN Lookup*: Identificación de Sistema Autónomo (`AS13335 Cloudflare, Inc.`, US, `104.21.0.0/16`).
  4. *WHOIS Audit*: Fecha de registro, vencimiento de dominio y servidores NS.
  5. *TLS Certificate Inspection*: Conteo regresivo de días de expiración, Subject, CA Issuer y SANs.
  6. *Security Headers Audit*: Evaluación de HSTS, CSP, X-Frame-Options, X-Content-Type (Calificación A+ a F).
  7. *Technologies*: Detección de servidor web (Nginx), Framework (FastAPI / Python 3.13) y hash SHA-256 de Favicon.
  8. *CDN Detection*: Detección pasiva de Cloudflare CDN.
  9. *Metadata Fingerprinting*: Agregación pasiva de metadatos telemétricos.
  10. *Change Delta Engine*: Auditoría e historial de cambios en la infraestructura (`IP_CHANGED`, `NEW_SUBDOMAIN`).

### FASE 3: CONTINUOUS MONITORING & DISTRIBUTED SCHEDULER (`CAP-04`) — STATUS: OPERATIONAL
- **`1M-HTTP-PROBING`**: Cadencia cada 1 minuto para verificación de latencia (ms), disponibilidad y código HTTP.
- **`5M-DNS-AUDIT`**: Cadencia cada 5 minutos para auditoría DNS, registros MX, TXT, SPF (`v=spf1`), DKIM y DMARC.
- **`1H-TLS-AUDIT`**: Cadencia cada 1 hora para auditoría de protocolo TLS (`TLSv1.3`), suite de cifrado (`TLS_AES_256_GCM_SHA384`) y lista SAN.
- **`CHANGE-AUDIT-STORE`**: Almacén inmutable de auditoría de cambios de estado telemétrico (`GET /api/v1/soc/scheduler/changes`).

### FASE 4: THREAT INTELLIGENCE & CORRELATION (`CAP-06`) — STATUS: OPERATIONAL
- **`THREAT-FEEDS`**: Integración desacoplada con VirusTotal, AbuseIPDB, GreyNoise, CISA KEV y NVD CVEs.
- **`COMPOSITE-THREAT-SCORE`**: Algoritmo dinámico de calificación de amenaza (0 = Safe, 100 = Critical Risk).
- **`12H-TTL-CACHE`**: Almacén en memoria para evitar estrangulamiento de cuota en APIs públicas.

### FASE 5: ALERT ENGINE, TIMELINE & INCIDENT CONSOLE (`CAP-05`, `CAP-07`, `CAP-08`) — STATUS: OPERATIONAL
- **`ALERT-RULES`**: Motor configurable de reglas (`TLS_EXPIRATION` ➔ WARNING, `HTTP_500` ➔ CRITICAL, `NEW_SUBDOMAIN` ➔ INFO, `HEADER_REMOVED` ➔ HIGH).
- **`TIMELINE-STREAM`**: Transmisión unificada y cronológica de eventos telemétricos del SOC.
- **`INCIDENT-CONSOLE`**: Consola SOC con ciclo de vida completo (`NEW` ➔ `INVESTIGATING` ➔ `CONTAINED` ➔ `MITIGATED` ➔ `CLOSED_WITH_RCA`) y enforzamiento estricto de la regla **`BR-0001` (Informe RCA obligatorio)**.

---

## 4. DEFINITION OF READY (DoR)
- [x] Problema y propósito estratégico claramente definidos.
- [x] Fases de madurez y dependencias técnicas mapeadas.
- [x] Artefactos de los que depende citados explícitamente (`PRODUCT_VISION.md`, `QUALITY_GATES.md`).

---

## 5. DEFINITION OF DONE (DoD)
- [x] Documento redactado con profundidad Enterprise (100% libre de placeholders).
- [x] Autoevaluación ejecutada: Permite a un equipo diferente comprender exactamente la hoja de ruta y secuencia de capacidades.
- [x] Estado establecido en **`REVIEW`** (Pendiente de revisión del ARB).

---

## 6. OPEN QUESTIONS
1. *¿Se planea integrar soporte de colas distribuidas (Celery / Redis Queue) para escalado masivo en la Fase 6?*  
   **Respuesta**: Sí, la arquitectura distribuida del Scheduler en `soc_scheduler_engine.py` está desacoplada para permitir delegación a workers background.

---

## 7. ASSUMPTIONS & KNOWN RISKS
- **Asunción**: Todas las consultas pasivas de DNS y TLS se ejecutan dentro del tiempo límite de timeout de 4.0 segundos por socket.
- **Riesgo Conocido**: Exceder límites de tasa (*rate limiting*) en feeds públicos de Threat Intelligence si se deshabilita la caché TTL de 12 horas.

---

## 8. FUTURE EVOLUTION
- **Integración SIEM/SOAR**: Exportación de alertas en formato CEF/Syslog hacia soluciones externas.
- **Playbooks Automatizados**: Ejecución de acciones de mitigación preconfiguradas ante alertas Críticas P1.

---

## 9. TRACEABILITY MATRIX LINKAGE
- Cita descendente hacia: `project/PRODUCT_BACKLOG.yaml`, `docs/02-domain-model/*_DOMAIN.md`.
