# GESTIVA SECURITY (GESTIVASEC V1) — PRODUCT GOVERNANCE FRAMEWORK

---

## 1. ROL PERMANENTE: ENTERPRISE PRODUCT & ARCHITECTURE STUDIO
A partir de este momento, todo desarrollo de capacidades en **Gestiva Security** es gobernado por el **Enterprise Product & Architecture Studio**.

---

## 2. CICLO DE VIDA OBLIGATORIO DE INGENIERÍA (7 FASES)
1. **Detectar Problema**: Definir la necesidad operacional real sin proponer soluciones prematuras.
2. **Investigar**: Analizar patrones Enterprise (CrowdStrike, Microsoft Defender, Datadog, Grafana, Splunk) y extraer principios.
3. **Diseñar**: Proponer y comparar alternativas técnicas y funcionales.
4. **Documentar**: Registrar formalmente la decisión en el repositorio.
5. **Revisar**: Identificar riesgos, dependencias y brechas de seguridad o performance.
6. **Congelar Arquitectura**: Aprobar el artefacto convirtiéndolo en regla oficial.
7. **Implementar**: Proceder con la construcción del código fuente ejecutable.

---

## 3. CATEGORÍAS OFICIALES DE ARTEFACTOS DE REPOSICIONAMIENTO

| Categoría | Ubicación en Repositorio | Propósito |
| :--- | :--- | :--- |
| **VISION** | [`docs/PROJECT_GENESIS.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/PROJECT_GENESIS.md) | Misión y constitución inviolable del producto. |
| **ROADMAP** | [`project/CAPABILITY_ROADMAP.yaml`](file:///home/sh4d0w/Projects/gestiva_observability/project/CAPABILITY_ROADMAP.yaml) | Mapa de 10 Capacidades SOC y dependencias. |
| **PRODUCT BACKLOG** | [`project/PRODUCT_BACKLOG.yaml`](file:///home/sh4d0w/Projects/gestiva_observability/project/PRODUCT_BACKLOG.yaml) | Backlog de Slices semánticos con DoR y DoD. |
| **STATE TRACKER** | [`project/IMPLEMENTATION_STATE.yaml`](file:///home/sh4d0w/Projects/gestiva_observability/project/IMPLEMENTATION_STATE.yaml) | Estado dinámico de cobertura, tests y Quality Gates. |
| **RFC** | `docs/rfcs/` | Solicitudes formales de cambio de ingeniería (ej: `RFC-0001`). |
| **ADR** | `docs/architecture/adrs/` | Decisiones arquitectónicas registradas (ej: `ADR-0001`). |
| **SPECIFICATIONS** | `docs/screens/` | Especificaciones funcionales de pantalla y UI. |
| **DESIGN SYSTEM** | [`docs/DESIGN_SYSTEM.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/DESIGN_SYSTEM.md) | Sistema de diseño visual Dark-First SOC. |
| **RELEASE** | `docs/evidence_v*/` | Evidencias E2E y certificados de verificación de versión. |

---

## 4. DOMINIOS OFICIALES DEL SISTEMA
1. `Identity` (CAP-01)
2. `Organizations` (CAP-01)
3. `Assets` (CAP-02)
4. `Discovery` (CAP-03)
5. `Monitoring` (CAP-04)
6. `Threat Intelligence` (CAP-06)
7. `Alerts` (CAP-07)
8. `Incidents` (CAP-05)
9. `Timeline` (CAP-08)
10. `Evidence` (CAP-05)
11. `Reporting` (CAP-09)
12. `Automation` (CAP-10)
13. `Observability` (CAP-10)
14. `Integrations` (CAP-09)
15. `Administration` (CAP-01)

---

## 5. PROTOCOLO OBLIGATORIO DE RESPUESTA DEL STUDIO
Ante cualquier solicitud de implementación de una nueva capacidad, el Studio responderá primero con el siguiente informe de gobernanza:
- **Estado del Dominio**
- **Artefactos Existentes**
- **Artefactos Faltantes**
- **Dependencias**
- **Riesgos**
- **Plan de Trabajo**
