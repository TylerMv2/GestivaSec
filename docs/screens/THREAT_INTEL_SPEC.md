# THREAT INTELLIGENCE ENRICHMENT SPECIFICATION (THREAT_INTEL_SPEC.md)

---

## 1. OBJETIVO DE LA PANTALLA
Consolidar e inspeccionar de forma pasiva la inteligencia de amenazas pública para los activos de **GestivaOne**, correlacionando feudo de indicadores de VirusTotal, AbuseIPDB, GreyNoise, CISA KEV y NVD CVE.

---

## 2. WIREFRAME TEXTUAL ASCII COMPLETO

```
+---------------------------------------------------------------------------------------------------------+
| [NAV] Dashboard | Assets | Passive Discovery | Threat Intel* | Alerts | Incident Center | Audit Logs   |
+---------------------------------------------------------------------------------------------------------+
| BREADCRUMB: GestivaSec / Threat Intelligence / gestivaone.com                                           |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  +---------------------------------------------------------------------------------------------------+  |
|  | THREAT INTEL REPORT: gestivaone.com (Resolved IP: 104.21.55.12 - AS13335 Cloudflare, Inc.)         |  |
|  | Composite Threat Score: [ 10 / 100 ] Grade: [ SAFE ] | Status: [ Cached (12h TTL) ]                |  |
|  +---------------------------------------------------------------------------------------------------+  |
|                                                                                                         |
|  +-----------------------+ +-----------------------+ +-----------------------+ +---------------------+  |
|  | VIRUSTOTAL            | | ABUSEIPDB             | | GREYNOISE             | | CISA KEV CATALOG    |  |
|  | Malicious Votes: 0    | | Confidence Score: 0%  | | Malicious Noise: False| | Known Exploited: No |  |
|  | Reputation: +100      | | Reports: 0            | | Tags: Benign Crawler| | CVEs Matched: 0     |  |
|  +-----------------------+ +-----------------------+ +-----------------------+ +---------------------+  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. FUENTES DE DATOS & DESACOPLAMIENTO
- **VirusTotal**: Análisis reputacional de dominios.
- **AbuseIPDB**: Puntuación de confianza de abuso sobre la dirección IP.
- **GreyNoise**: Clasificación de tráfico benigno vs scanners maliciosos.
- **CISA KEV**: Catálogo de Vulnerabilidades Conocidas y Explotadas.
- **NVD CVE**: Gravedad CVSS v3.1.
