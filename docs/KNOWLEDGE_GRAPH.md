# GESTIVA SECURITY (GESTIVASEC V1) — DOCUMENT KNOWLEDGE GRAPH

---

## 1. RELACIONES ENTRE ARTEFACTOS ARQUITECTÓNICOS

```mermaid
graph TD
    VISION["PROJECT_GENESIS.md (Constitution)"] --> GOV["PRODUCT_GOVERNANCE_FRAMEWORK.md"]
    VISION --> ROADMAP["CAPABILITY_ROADMAP.yaml"]
    ROADMAP --> BACKLOG["PRODUCT_BACKLOG.yaml"]
    BACKLOG --> STATE["IMPLEMENTATION_STATE.yaml"]

    VISION --> DESIGN["DESIGN_SYSTEM.md"]
    DESIGN --> BLUEPRINT["SOC_PRODUCT_BLUEPRINT.md"]
    BLUEPRINT --> RFC0001["RFC-0001-SOC-DASHBOARD-UX.md"]

    RFC0001 --> SPEC_DASH["DASHBOARD_SPEC.md"]
    RFC0001 --> SPEC_INC["INCIDENT_CENTER_SPEC.md"]
    RFC0001 --> SPEC_AST["ASSETS_SPEC.md"]
    RFC0001 --> SPEC_INTEL["THREAT_INTEL_SPEC.md"]

    SPEC_DASH --> CODE["Backend FastAPI & Frontend SPA"]
    SPEC_INC --> CODE
    SPEC_AST --> CODE
    SPEC_INTEL --> CODE

    CODE --> TESTS["Pytest Automated Test Suites (56/56 PASS)"]
    TESTS --> EVIDENCE["tests/evidence_v0.1.0/ RELEASE VERIFIED"]
    EVIDENCE --> RELEASE["RELEASE_NOTES_v0.1.0.md"]

    RELEASE --> USER_MANUAL["USER_MANUAL.md"]
    RELEASE --> ADMIN_MANUAL["ADMIN_MANUAL.md"]
```

---

## 2. REGLAS DE IMPACTO EN EL KNOWLEDGE GRAPH
1. Un cambio en `PROJECT_GENESIS.md` invalida automáticamente los RFCs activos si viola una regla invariante (`BR-0001` a `BR-0005`).
2. Una actualización en `DESIGN_SYSTEM.md` requiere una revisión inmediata de `DASHBOARD_SPEC.md` e `INCIDENT_CENTER_SPEC.md`.
3. Ningún código fuente en `backend/` o `frontend/` puede existir sin estar enlazado a un RFC y una Especificación.
