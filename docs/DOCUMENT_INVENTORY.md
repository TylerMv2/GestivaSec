# GESTIVA SECURITY (GESTIVASEC V1) — DOCUMENT INVENTORY & LIFECYCLE TRACKER

---

## 1. ESTADOS DEL CICLO DE VIDA DOCUMENTAL
Todo documento en el repositorio debe encontrarse exactamente en uno de los siguientes estados:
- **`DRAFT`**: Documento en elaboración inicial.
- **`REVIEW`**: Documento sometido a revisión técnica o arquitectónica.
- **`APPROVED`**: Documento oficialmente congelado y aprobado.
- **`DEPRECATED`**: Documento sustituido por una versión más reciente.
- **`ARCHIVED`**: Documento histórico conservado para trazabilidad.

---

## 2. INVENTARIO COMPLETO DE ARTEFACTOS

| Documento | Dominio / Categoría | Responsable | Estado | Versión | Dependencias |
| :--- | :--- | :--- | :---: | :---: | :--- |
| [`docs/PROJECT_GENESIS.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/PROJECT_GENESIS.md) | VISION / Constitution | Lead Architect | **`APPROVED`** | v1.0 | N/A |
| [`docs/PRODUCT_GOVERNANCE_FRAMEWORK.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/PRODUCT_GOVERNANCE_FRAMEWORK.md) | GOVERNANCE | Studio Lead | **`APPROVED`** | v1.0 | `PROJECT_GENESIS.md` |
| [`docs/DOCUMENT_INVENTORY.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/DOCUMENT_INVENTORY.md) | INVENTORY | Documentation Lead | **`APPROVED`** | v1.0 | `README.md` |
| [`docs/KNOWLEDGE_GRAPH.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/KNOWLEDGE_GRAPH.md) | KNOWLEDGE_GRAPH | Architecture Studio | **`APPROVED`** | v1.0 | All Documents |
| [`docs/TRACEABILITY_MATRIX.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/TRACEABILITY_MATRIX.md) | TRACEABILITY | Quality Lead | **`APPROVED`** | v1.0 | `PRODUCT_BACKLOG.yaml` |
| [`docs/DESIGN_SYSTEM.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/DESIGN_SYSTEM.md) | DESIGN SYSTEM | UX Lead | **`APPROVED`** | v1.0 | `PROJECT_GENESIS.md` |
| [`docs/SOC_PRODUCT_BLUEPRINT.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/SOC_PRODUCT_BLUEPRINT.md) | UX ARCHITECTURE | Product Architect | **`APPROVED`** | v1.0 | `DESIGN_SYSTEM.md` |
| [`docs/rfcs/RFC-0001-SOC-DASHBOARD-UX.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/rfcs/RFC-0001-SOC-DASHBOARD-UX.md) | RFC | Product Architect | **`APPROVED`** | v1.0 | `SOC_PRODUCT_BLUEPRINT.md` |
| [`docs/screens/DASHBOARD_SPEC.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/screens/DASHBOARD_SPEC.md) | SPECIFICATIONS | Lead Frontend Eng | **`APPROVED`** | v1.0 | `RFC-0001` |
| [`docs/screens/INCIDENT_CENTER_SPEC.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/screens/INCIDENT_CENTER_SPEC.md) | SPECIFICATIONS | Lead Frontend Eng | **`APPROVED`** | v1.0 | `RFC-0001` |
| [`docs/screens/ASSETS_SPEC.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/screens/ASSETS_SPEC.md) | SPECIFICATIONS | Lead Frontend Eng | **`APPROVED`** | v1.0 | `RFC-0001` |
| [`docs/screens/THREAT_INTEL_SPEC.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/screens/THREAT_INTEL_SPEC.md) | SPECIFICATIONS | Lead Frontend Eng | **`APPROVED`** | v1.0 | `RFC-0001` |
| [`docs/INSTALLATION_GUIDE.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/INSTALLATION_GUIDE.md) | RELEASE | DevOps Lead | **`APPROVED`** | v1.0 | `docker-compose.yml` |
| [`docs/USER_MANUAL.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/USER_MANUAL.md) | PLAYBOOKS | SOC Operations | **`APPROVED`** | v1.0 | `SOC_PRODUCT_BLUEPRINT.md` |
| [`docs/ADMIN_MANUAL.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/ADMIN_MANUAL.md) | RUNBOOKS | Systems Admin | **`APPROVED`** | v1.0 | `INSTALLATION_GUIDE.md` |
| [`docs/RELEASE_NOTES_v0.1.0.md`](file:///home/sh4d0w/Projects/gestiva_observability/docs/RELEASE_NOTES_v0.1.0.md) | RELEASE | Release Authority | **`APPROVED`** | v1.0 | All Evidences |
