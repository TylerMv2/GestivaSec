# 00_READ_FIRST.md — GESTIVASEC PLATFORM ONBOARDING & GOVERNANCE MANUAL

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `APPROVED & MANDATORY READ ONBOARDING MANUAL`  
**Target Audience:** Architects, Software Engineers, UI/UX Designers, Product Managers, QA Engineers, DevOps  
**Baseline Compatibility:** Level 3 Product Implementation, Kernel v1.0 (LOCKED), Enterprise Architecture (LOCKED)  
**Date:** 2026-07-26  

---

## 1. WHAT IS GESTIVASEC SECURITY?

**Gestiva Security** is the continuous security observability, threat detection, correlation, and automated incident response (SIEM / SOAR) platform built for the **GestivaOne Ecosystem**.

Unlike traditional administrative platforms, Gestiva Security is an **operational Security Operations Center (SOC) platform**. It enables security analysts, incident responders, and CISOs to monitor live telemetry, discover unregistered infrastructure, ingest and normalize heterogeneous security events, detect active threats, and orchestrate automated containment.

---

## 2. THE PRODUCT & SOC PHILOSOPHY

### 2.1 Analysts Investigate Workflows, Not Static Pages
Gestiva Security is engineered on a **Workflow-Driven Interaction Model**:
- Users do not browse disconnected pages. They navigate high-velocity operational security workflows.
- Context is immutable. When drilling down from a high-severity alert to an asset or raw log, the analyst's active search workspace is preserved using slide-over **Inspector Drawers**.

### 2.2 Domain-Driven & Governance First
The platform enforces strict invariants across all execution paths:
1. **Asset Identity Invariant:** Every monitored asset is identified by an immutable **Asset UUID** (never by ephemeral IP addresses).
2. **Owner Email Assignment (BR-02):** Unowned devices are forbidden upon asset registration or promotion.
3. **Multi-Tenant Isolation (BR-0004):** Every API request and database query enforces strict organization boundary scoping via the `X-Organization-ID` header.
4. **Immutable Audit Trail (BR-0005):** Security events and audit logs are append-only.

---

## 3. MANDATORY READING ORDER FOR NEW TEAM MEMBERS

Every new engineer, designer, or product manager joining Gestiva Security MUST read the documentation repository in the following sequential order:

```
1. 00_READ_FIRST.md (This Onboarding Manual)
                    ↓
2. GESTIVASEC_ENTERPRISE_SOC_ARCHITECTURE.md (16 Bounded Contexts)
                    ↓
3. GESTIVASEC_FRONTEND_ARCHITECTURE_GUIDE.md (Master Interaction Guide)
                    ↓
4. GESTIVASEC_UI_DDR.md (Design Decision History & Rationale)
                    ↓
5. GESTIVASEC_UI_ANTI_PATTERNS.md (Forbidden UI/UX Practices)
                    ↓
6. GESTIVASEC_USER_PERSONAS.md (Operational Personas & Journeys)
                    ↓
7. GESTIVASEC_UI_STATE_MACHINES.md (12 Mandatory Screen States)
                    ↓
8. GESTIVASEC_FRONTEND_QUALITY_STANDARD.md (Quality Gates & DoD)
                    ↓
9. GESTIVASEC_DESIGN_HANDOFF.md (Official Design Package)
                    ↓
10. GESTIVASEC_ARCHITECTURE_FREEZE.md (Architecture Freeze Declaration)
```

---

## 4. ARCHITECTURE GOVERNANCE & ARB RESPONSIBILITIES

The **Architecture Review Board (ARB)** oversees all platform changes:
- **Kernel & Enterprise Architecture Freeze:** The Kernel and 16 Bounded Contexts are **ARCHITECTURALLY FROZEN**.
- **Proposal Process for Changes:** Any structural change to domain contracts, REST APIs, or UI interaction rules must submit a formal Design Decision Record (DDR) for ARB review and explicit approval.
