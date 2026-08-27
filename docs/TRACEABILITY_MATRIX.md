# GESTIVA SECURITY (GESTIVASEC V1) — END-TO-END TRACEABILITY MATRIX

---

## 1. CADENA DE TRAZABILIDAD COMPLETA (VISION ➔ CODE ➔ RELEASE ➔ RUNBOOK)

| Capability ID | Visión / Regla | Slice Semántico | RFC / ADR | Especificación | Módulo Backend | Suite de Pruebas | Evidencia Release |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CAP-01** | `BR-0004` (Multi-Tenant) | `IAM-LOGIN` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/auth_router.py` | `test_slice_001_login.py` | `e2e_results.log` |
| **CAP-01** | `BR-0004` | `IAM-ORGS` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/organizations_router.py` | `test_slice_002_organizations.py` | `e2e_results.log` |
| **CAP-01** | RBAC Roles | `IAM-USERS` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/users_router.py` | `test_slice_003_users.py` | `e2e_results.log` |
| **CAP-01** | Permissions | `IAM-ROLES` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/roles_router.py` | `test_slice_004_roles.py` | `e2e_results.log` |
| **CAP-01** | Enforcer | `IAM-PERMS` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/permissions_router.py` | `test_slice_005_perms.py` | `e2e_results.log` |
| **CAP-01** | OAuth SSO | `IAM-OAUTH` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/oauth_router.py` | `test_slice_006_oauth.py` | `e2e_results.log` |
| **CAP-02** | `BR-0002` (Owner Email) | `AST-INVENTORY` | `RFC-0001` | `ASSETS_SPEC.md` | `backend/api/assets_router.py` | `test_assets_slice.py` | `e2e_results.log` |
| **CAP-03** | Passive Inspection | `DISCOVERY-ENGINE`| `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/passive_discovery_router.py` | `test_passive_discovery.py` | `e2e_results.log` |
| **CAP-04** | Continuous Monitoring | `SOC-SCHEDULER` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/soc_scheduler_router.py` | `test_soc_scheduler.py` | `e2e_results.log` |
| **CAP-05** | `BR-0001` (RCA Enforcer) | `INCIDENT-CONSOLE`| `RFC-0001` | `INCIDENT_CENTER_SPEC.md` | `backend/api/alert_router.py` | `test_alert_engine.py` | `e2e_results.log` |
| **CAP-06** | Threat Intel | `THREAT-INTEL` | `RFC-0001` | `THREAT_INTEL_SPEC.md` | `backend/api/threat_intel_router.py` | `test_threat_intel.py` | `e2e_results.log` |
| **CAP-07** | Alert Rules | `ALERT-ENGINE` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/alert_router.py` | `test_alert_engine.py` | `e2e_results.log` |
| **CAP-08** | Timeline Stream | `TIMELINE-ENGINE` | `RFC-0001` | `DASHBOARD_SPEC.md` | `backend/api/alert_router.py` | `test_alert_engine.py` | `e2e_results.log` |

---

## 2. REGLA INVIOLABLE DE TRAZABILIDAD
Queda prohibido subir o fusionar código a la rama principal si falta cualquier eslabón de la cadena de trazabilidad anterior.
