# CHANGELOG — GESTIVA SECURITY (GESTIVASEC V1)

---

## [Unreleased] - 2026-07-25

### Added
- **Adopción del Sistema de Gobernanza de Ingeniería Empresarial**:
  - Creados los archivos estructurados de control de estado en [`project/`](file:///home/sh4d0w/Projects/gestiva_observability/project/):
    - [`project/CAPABILITY_ROADMAP.yaml`](file:///home/sh4d0w/Projects/gestiva_observability/project/CAPABILITY_ROADMAP.yaml): Mapeo de la Visión en 10 Capacidades del producto.
    - [`project/PRODUCT_BACKLOG.yaml`](file:///home/sh4d0w/Projects/gestiva_observability/project/PRODUCT_BACKLOG.yaml): Backlog oficial con IDs semánticos y verificación obligatoria de Definition of Ready (DoR).
    - [`project/IMPLEMENTATION_STATE.yaml`](file:///home/sh4d0w/Projects/gestiva_observability/project/IMPLEMENTATION_STATE.yaml): Registro del estado vivo de métricas de cobertura y tests.

- **CAP-01 Identity & Access Management (IAM)**:
  - **`IAM-LOGIN` (STATUS: DONE)**: Dominio `auth.py`, firma JWT, Bcrypt, endpoint `/login` y suite de pruebas (`tests/test_slice_001_login.py`).
  - **`IAM-ORGS` (STATUS: DONE)**: Dominio `organization.py`, migración SQL, aislamiento `BR-04`, endpoint `/organizations` y suite (`tests/test_slice_002_organizations.py`).
  - **`IAM-USERS` (STATUS: DONE)**:
    - Modelo de Dominio (`backend/domain/user.py`) para agregados de usuarios y validación de roles (`SOC_ADMIN`, `SOC_ANALYST`, `SOC_OPERATOR`, `AUDITOR`).
    - Adaptador de Persistencia (`backend/infrastructure/user_repository.py`).
    - Servicio de Aplicación (`backend/application/user_service.py`).
    - Controlador REST API (`backend/api/users_router.py`) exponiendo `POST /api/v1/users` y `GET /api/v1/users`.
    - Suite de Pruebas Unitarias e Integración (`tests/test_slice_003_users.py`).

- **CAP-02 Asset Management**:
  - **`AST-INVENTORY` (STATUS: DONE)**: Dominio `asset.py`, enforzamiento `BR-02` (correo del propietario) y `BR-04`.

- **CAP-03 Monitoring Engine**:
  - **`MON-SYNTHETIC` (STATUS: DONE)**: Dominio `synthetic.py`, enforzamiento `BR-03` (3 fallas sintéticas consecutivas desencadenan P1).

---

### Coverage & Backlog Progress Metrics
- **Completed Slices**: 5 / 59 Semantic Slices (8.4% Total Backlog Completed).
- **Active Tests**: 22 Test Cases (100% Passed).
- **Repository Status**: Gobernado bajo YAML, ejecutable, cero código muerto, 100% verde en pruebas.
