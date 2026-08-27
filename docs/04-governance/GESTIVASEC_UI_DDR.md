# GESTIVASEC_UI_DDR.md — UI DESIGN DECISION RECORDS (DDR) REPOSITORY

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `APPROVED & ARCHITECTURALLY FROZEN`  
**Target Audience:** Software Architects, UI/UX Designers, Frontend Engineers, Product Owners  
**Baseline Alignment:** Enterprise SOC Architecture, Governance Sprint 5.5  
**Date:** 2026-07-26  

---

## 1. EXECUTIVE SUMMARY

This document records the official Design Decision Records (DDR) for **Gestiva Security**. Every record documents the problem statement, context, alternatives evaluated, selected solution, architectural rationale, consequences, and domain entity relationships for interface interaction decisions.

---

## 2. DESIGN DECISION RECORDS

### DDR-001: Persistent Workflow-Driven Navigation Architecture
- **Decision ID:** DDR-001
- **Title:** Non-Destructive Master-Detail & Inspector Drawer Navigation
- **Status:** `APPROVED`
- **Context:** Security analysts perform high-velocity triage across alerts, hosts, and raw logs.
- **Problem:** Full page browser reloads destroy analyst search queries and active filter states.
- **Alternatives Considered:** 
  1. Multi-page routing (Full browser reloads).
  2. Tabbed sub-views inside page.
  3. Master-Detail split views with slide-over Inspector Drawers (Selected).
- **Selected Solution:** Implement non-destructive slide-over Inspector Drawers over master data tables.
- **Rationale:** Preserves the underlying investigation workspace while enabling deep entity inspection.
- **Consequences:** Lower analyst fatigue; requires clean drawer state management.
- **Related Modules:** All 21 Frontend Modules.
- **Related Domain Entities:** `Asset`, `Alert`, `Incident`, `NormalizedEvent`.

---

### DDR-002: Master Asset Identity via Immutable Asset UUID vs Ephemeral IP
- **Decision ID:** DDR-002
- **Title:** Asset Identification by Immutable UUID with Forensic IP History Tracing
- **Status:** `APPROVED`
- **Context:** Network devices change IP addresses dynamically (DHCP, cloud autoscaling, K8s pods).
- **Problem:** Using IP address as primary key causes broken asset histories during incidents.
- **Alternatives Considered:** 
  1. IP Address as Identity.
  2. Hostname as Identity.
  3. Immutable Asset UUID + `ip_history` log (Selected).
- **Selected Solution:** Primary identity is an immutable Asset UUID. Ephemeral IPs are pushed into `ip_history`.
- **Rationale:** Incident evidence remains tethered to the physical/logical asset regardless of network moves.
- **Related Domain Entities:** `DigitalAsset`, `IPHistoryRecord`.

---

### DDR-003: Mandatory Owner Email Assignment on Asset Promotion (BR-02)
- **Decision ID:** DDR-003
- **Title:** Enforcement of Owner Email Assignment on Asset Promotion
- **Status:** `APPROVED`
- **Context:** Unowned devices in CMDB delay incident containment.
- **Selected Solution:** Enforce rule **`BR-02`**: Every promoted asset must have a valid owner email assigned.
- **Rationale:** Ensures immediate accountability during critical P1 security incidents.
- **Related Domain Entities:** `DigitalAsset`, `Organization`.

---

### DDR-004: Multi-Tenant Header Scope & Organization Isolation (BR-0004)
- **Decision ID:** DDR-004
- **Title:** Global Organization Scope Header Ingestion
- **Status:** `APPROVED`
- **Context:** Gestiva Security operates in multi-tenant mode across enterprise clients (*BR-0004*).
- **Selected Solution:** Ingest `X-Organization-ID` HTTP header in every API call; display organization badge in global UI topbar.
- **Rationale:** Guarantees strict multi-tenant isolation at network and UI boundaries.
- **Related Domain Entities:** `Organization`.

---

### DDR-005: 3-Second Reactive Polling for Real-Time Telemetry
- **Decision ID:** DDR-005
- **Title:** Continuous 3000ms Polling Loop for Operational Dashboard
- **Status:** `APPROVED`
- **Context:** SOC dashboards require real-time visibility into infrastructure health.
- **Selected Solution:** 3000ms reactive polling loop with Chart.js line interpolation.
- **Rationale:** Provides low-overhead real-time telemetry updates.
- **Related Domain Entities:** Platform Telemetry Summary.

---

### DDR-006: Sliding Inspector Drawer for Entity Deep-Dives
- **Decision ID:** DDR-006
- **Title:** Slide-Over Right Panel Inspector Drawer
- **Status:** `APPROVED`
- **Context:** Analysts need to view raw JSON logs, asset risk scores, and IoC reputation without navigating away.
- **Selected Solution:** Slide-over Inspector Drawer appearing on the right 40% of the screen.
- **Rationale:** Keeps 60% of the screen on the primary grid, preserving navigation state.

---

### DDR-007: GestivaSec Event Schema (GES) Unified Visualization
- **Decision ID:** DDR-007
- **Title:** Standardized Event Viewer for Normalized Telemetry
- **Status:** `APPROVED`
- **Context:** Heterogeneous raw logs (Syslog, Windows, CloudTrail) confuse analysts during triage.
- **Selected Solution:** Render all normalized events in unified GES format (Observer, Source + GeoIP, Destination + Asset UUID, Classification).
- **Related Domain Entities:** `NormalizedEvent`, `RawEventRecord`.
