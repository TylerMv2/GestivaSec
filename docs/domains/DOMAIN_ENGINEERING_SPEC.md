# GESTIVA SECURITY (GESTIVASEC V1) — DOMAIN ENGINEERING SPECIFICATION

---

## 1. ESTADO DE GOBERNANZA DE DOMINIOS (GOVERNANCE AUDIT)

### 1.1 Estado del Dominio & Cobertura
Se auditan los 15 dominios funcionales del ecosistema **GestivaSec V1**:

| ID Dominio | Nombre del Dominio | Estado del Dominio | Dominio Puro | Adaptadores Infraestructura | Suite de Pruebas |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **DOM-01** | `Identity` | **`APPROVED`** | `backend/domain/auth.py` | `auth_repository.py` | `test_slice_001_login.py` |
| **DOM-02** | `Organizations` | **`APPROVED`** | `backend/domain/organization.py` | `organization_repository.py` | `test_slice_002_organizations.py` |
| **DOM-03** | `Users & Roles` | **`APPROVED`** | `backend/domain/user.py`, `role.py` | `user_repository.py`, `role_repository.py` | `test_slice_003_users.py`, `test_slice_004_roles.py` |
| **DOM-04** | `Permissions` | **`APPROVED`** | `backend/domain/permission.py` | Direct Evaluator | `test_slice_005_perms.py` |
| **DOM-05** | `OAuth SSO` | **`APPROVED`** | `backend/domain/oauth.py` | REST Token Exchange Adapter | `test_slice_006_oauth.py` |
| **DOM-06** | `Digital Assets` | **`APPROVED`** | `backend/domain/asset.py` | `asset_repository.py` | `test_assets_slice.py` |
| **DOM-07** | `Synthetic Probing`| **`APPROVED`** | `backend/domain/synthetic.py` | `synthetic_repository.py` | `test_synthetic_slice.py` |
| **DOM-08** | `Passive Discovery`| **`APPROVED`** | `backend/domain/passive_discovery.py` | `passive_discovery_engine.py` | `test_passive_discovery.py` |
| **DOM-09** | `SOC Scheduler` | **`APPROVED`** | `backend/domain/soc_scheduler.py` | `soc_scheduler_engine.py` | `test_soc_scheduler.py` |
| **DOM-10** | `Threat Intel` | **`APPROVED`** | `backend/domain/threat_intel.py` | `threat_intel_engine.py` | `test_threat_intel.py` |
| **DOM-11** | `Alert Engine` | **`APPROVED`** | `backend/domain/alert_engine.py` | `alert_repository.py` | `test_alert_engine.py` |
| **DOM-12** | `Timeline Stream` | **`APPROVED`** | `backend/domain/alert_engine.py` | `alert_repository.py` | `test_alert_engine.py` |
| **DOM-13** | `SOC Incidents` | **`APPROVED`** | `backend/domain/alert_engine.py` | `alert_repository.py` | `test_alert_engine.py` |
| **DOM-14** | `Telemetry` | **`APPROVED`** | `backend/domain/synthetic.py` | Prometheus / Healthcheck | `test_health.py` |
| **DOM-15** | `Quality & Fitness`| **`APPROVED`** | `tests/test_architecture_fitness.py` | Technical Debt Fitness | `test_technical_debt_fitness.py` |

---

## 2. ARTEFACTOS EXISTENTES VS. FALTANTES

### Artefactos Existentes:
- Modelo de Dominio Puro: `backend/domain/*.py` (100% aislado de dependencias externas).
- Repositorios e Infraestructura: `backend/infrastructure/*.py`.
- Servicios de Aplicación: `backend/application/*.py`.
- Controladores REST: `backend/api/*.py`.
- Pruebas Automatizadas: 56 Casos de prueba verdes (**100% PASS**).

### Artefactos Faltantes (Siguiente Capacidad):
- `FRONTEND-SPA-DESIGN-SYSTEM`: Componentes web reactivos en Javascript / CSS Vanilla aplicando `DESIGN_SYSTEM.md` e `INCIDENT_CENTER_SPEC.md`.

---

## 3. DEPENDENCIAS Y RIESGOS
- **Dependencias**: El Frontend depende estrictamente de las especificaciones congeladas (`DASHBOARD_SPEC.md`, `INCIDENT_CENTER_SPEC.md`) y las APIs creadas (`/api/v1/*`).
- **Riesgos**: Posible divergencia visual en navegadores si no se aplican los tokens oscuros `#0B0F17` y las variables CSS unificadas.

---

## 4. PLAN DE TRABAJO
1. Congelar la documentación de especificación de dominios en `docs/domains/DOMAIN_ENGINEERING_SPEC.md`.
2. Proceder a la implementación del sistema visual reactivo SPA respetando el Design System.
