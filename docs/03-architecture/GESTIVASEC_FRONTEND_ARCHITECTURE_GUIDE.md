# GESTIVASEC_FRONTEND_ARCHITECTURE_GUIDE.md
## Master Operational UI/UX & Interaction Architecture Specification

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `LOCKED & APPROVED CONTRACT`  
**Target Audience:** Architects, Backend Engineers, Frontend Engineers, UI/UX Designers, QA, DevOps, Product Owners  
**Baseline Compatibility:** Level 3 Product Architecture, Domain-Driven Design (DDD), Multi-Tenant Isolation (*BR-0004*), Inmutable Audit Trail (*BR-0005*)  
**Date:** 2026-07-26  

---

## CHAPTER 1: INTRODUCTION

### 1.1 Purpose of the Document
This document establishes the official, technology-agnostic **Product Interaction & Frontend Operational Architecture** for **Gestiva Security**. While the enterprise backend, domain boundaries, and event pipelines dictate the operational mechanics of the platform, this guide defines the behavioral contract governing how users, security analysts, incident responders, and system administrators interact with Gestiva Security.

It serves as the definitive reference ensuring that every interface, workflow, screen component, and real-time state transition remains strictly aligned with the underlying Domain-Driven Design (DDD) bounded contexts and Enterprise Architecture.

### 1.2 Target Audience
- **Software & Systems Architects:** To verify contract compliance across all API boundaries and user workflows.
- **Frontend Engineers & UI Developers:** To build interface components, state management containers, and event stream listeners following universal operational patterns.
- **Backend Engineers:** To align REST/WebSocket payload shapes, pagination metadata, and error handling contracts with UI expectations.
- **UI/UX Designers:** To design layout blueprints, interaction states, and context preservation drawers without violating operational workflow constraints.
- **QA & Automation Engineers:** To write end-to-end acceptance tests based on explicit screen state specifications and navigation rules.
- **Product Owners & Technical Writers:** To validate feature completeness against operational capabilities and KPIs.

### 1.3 Scope & Boundings
This document governs **Product Interaction Architecture**, **Information Hierarchy**, **Screen Responsibilities**, **State Transitions**, and **User Workflows**. It explicitly excludes visual styling (colors, typography, CSS frameworks, branding elements) and implementation framework selection (React, Vue, Web Components).

### 1.4 Architectural Relationships

```
+-----------------------------------------------------------------------+
|              PROJECT KERNEL N1 (Level 1: Governance & Registries)     |
+-----------------------------------------------------------------------+
                                    ↓
+-----------------------------------------------------------------------+
|         ENTERPRISE SOC ARCHITECTURE (Level 2/3: 16 Bounded Contexts)  |
+-----------------------------------------------------------------------+
                                    ↓
+-----------------------------------------------------------------------+
|  GESTIVASEC FRONTEND ARCHITECTURE GUIDE (Product Interaction & UX)   |
+-----------------------------------------------------------------------+
```

1. **Relationship with Project Kernel (Level 1):** The Kernel provides frozen governance rules and registries. The Frontend respects these invariants by enforcing strict multi-tenant boundaries (*BR-0004*) and immutable record states (*BR-0005*).
2. **Relationship with Enterprise Architecture (Level 2/3):** The 16 Bounded Contexts mapped in `GESTIVASEC_ENTERPRISE_SOC_ARCHITECTURE.md` correspond 1:1 with the screen modules and entity domains defined herein.
3. **Relationship with Domain Model:** Frontend state containers mirror pure domain aggregates (`DigitalAsset`, `AuditEvent`, `NormalizedEvent`, `Finding`, `Alert`, `Incident`).

---

## CHAPTER 2: PRODUCT PHILOSOPHY

### 2.1 The Operational SOC Mindset
Gestiva Security is not a generic administrative CRUD portal. It is a high-velocity **Security Operations Center (SOC) & SIEM Platform** designed to detect, triage, investigate, and respond to threats across heterogeneous environments.

### 2.2 Workflow-Driven vs Page-Driven Navigation
Generic applications force users to click between disconnected pages to perform tasks. Gestiva Security operates on a **Workflow-Driven Interaction Model**:
- Users do not "browse pages"; they **navigate operational workflows**.
- Information follows the analyst. Context is never lost when drilling down from an Alert to an Asset, a Raw Log, or an Incident Case.
- Master-Detail views, slide-over inspection drawers, and persistent context headers ensure analysts can execute triage without destroying their active investigation workspace.

---

## CHAPTER 3: CORE PRODUCT ENTITIES

Each business entity in Gestiva Security has explicit operational boundaries, primary actions, and cross-domain relationships.

### 3.1 Digital Asset (`Asset`)
- **Purpose:** Primary physical, virtual, or logical entity monitored across the GestivaOne ecosystem.
- **Identity Invariant:** Identified by immutable **Asset UUID** (never by ephemeral IP or Hostname).
- **Primary Actions:** Promote from Discovery, Transition Lifecycle State, Update Network Location, Assign Owner (*BR-02*).
- **Secondary Actions:** View Historical IPs, Export Telemetry, Run Synthetic Probe, Adjust Risk Score.
- **Relationships:** Belongs to Organization (*BR-04*); linked to Events, Findings, Alerts, Incidents, and TLS Certificates.

### 3.2 Raw Event (`RawEventRecord`)
- **Purpose:** Immutable raw log payload ingested by a Collector plugin before parsing.
- **Primary Actions:** View Raw Payload, Trigger Manual Parsing Test, Link to Forensic Case.
- **Relationships:** Produced by Collector; mapped to Asset UUID via Asset Resolver; source for Normalized Event.

### 3.3 Normalized Event (`NormalizedEvent`)
- **Purpose:** Standardized security event structured according to GestivaSec Event Schema (GES).
- **Primary Actions:** Inspect GES Schema, View GeoIP/ASN Enrichment, Filter by Category/Severity.
- **Relationships:** Linked to Raw Event, Observer, Source Asset, Destination Asset, and Detection Rules.

### 3.4 Finding (`Finding`)
- **Purpose:** Individual security anomaly or signature match generated by Detection Engine.
- **Primary Actions:** Triage, Suppress, Escalate to Alert, Assign Analyst.
- **Relationships:** Linked to Normalized Event, Asset, and Detection Rule.

### 3.5 Alert (`Alert`)
- **Purpose:** Actionable security notification requiring analyst attention.
- **Primary Actions:** Acknowledge, Suppress, Correlate, Promote to Incident.
- **Relationships:** Composed of Findings; linked to Asset, Threat Intel IoCs, and Notification Channels.

### 3.6 Incident (`Incident`)
- **Purpose:** High-severity operational security event representing an active threat.
- **Primary Actions:** Declare, Assign Responders, Execute SOAR Playbook, Contain, Close with Root Cause Analysis (RCA).
- **Relationships:** Composed of correlated Alerts; linked to Case, Evidence Vault, and Audit Trail.

### 3.7 Case (`InvestigationCase`)
- **Purpose:** Comprehensive forensic investigation workspace managed by SOC analysts.
- **Primary Actions:** Attach Evidence, Add Investigator Notes, Chain IoCs, Export Forensic Report.
- **Relationships:** Links multiple Incidents, Assets, Artifacts, and Audit Records.

---

## CHAPTER 4: COMPLETE NAVIGATION ARCHITECTURE

### 4.1 Navigation Tree Hierarchy

```
GESTIVASEC PLATFORM
├── 1. OPERATIONAL DASHBOARD
│   ├── Real-Time Telemetry Grid (10 Live Widgets)
│   ├── Network & Latency Live Chart
│   └── Core Services Status Board
├── 2. ASSET INTELLIGENCE & CMDB
│   ├── Asset Discovery Engine (Network Scanner & Host Promotion)
│   ├── Asset Inventory (CMDB Master-Detail Grid)
│   └── Asset Lifecycle & Risk Matrix
├── 3. TELEMETRY & EVENT PIPELINE
│   ├── Event Collectors Framework (Collector Manager & EPS Metrics)
│   ├── Raw Events Stream (Immutable Ingestion Log)
│   └── Normalized Events (GestivaSec Event Schema - GES)
├── 4. SIEM & DETECTION ENGINE
│   ├── Detection Rules Registry
│   ├── Findings Stream
│   └── Correlation Engine (Multi-Event Attack Chains)
├── 5. INCIDENT & CASE MANAGEMENT
│   ├── Alert Center
│   ├── Incident Response Console
│   └── Forensic Case Workspaces
├── 6. THREAT INTELLIGENCE & SOAR
│   ├── IoC Reputation Database
│   ├── Automated Playbooks & SOAR Actions
│   └── Notification Channel Dispatcher
└── 7. ADMINISTRATION & GOVERNANCE
    ├── Tenant Organization Selector (BR-0004)
    ├── User & Role Access Control (RBAC)
    ├── Immutable Audit Trail (BR-0005)
    └── Platform Settings & Data Retention
```

---

## CHAPTER 5: SCREEN ARCHITECTURE

Every module in Gestiva Security enforces a rigorous screen contract specifying its primary question, displayed KPIs, tables, actions, and real-time refresh behavior.

### 5.1 Operational SOC Dashboard Screen
- **Primary Question:** *¿Qué está pasando AHORA en la infraestructura de la organización?*
- **Primary Entity:** Platform Telemetry Summary.
- **Displayed KPIs:** Hosts Online, Critical Alerts P1/P2, Down Services, Network Traffic Mbps, CPU %, RAM %, Events/min, Expiring TLS Certs, Connected Users, Active Sessions.
- **Displayed Tables:** Core Services Health Board.
- **Displayed Charts:** Live Network Bandwidth & Latency Line Chart.
- **Real-Time Strategy:** Continuous Polling every 3,000ms with smooth line interpolation.

### 5.2 Asset Discovery Screen
- **Primary Question:** *¿Qué nuevos dispositivos no registrados han ingresado a la red?*
- **Primary Entity:** `DiscoveredHost`.
- **Displayed KPIs:** Total Scanned IPs, Discovered Hosts, Unregistered Hosts, Average Scan Duration.
- **Displayed Tables:** Discovered Hosts Table (IP, Hostname, OS Fingerprint, Open Ports, Vendor, Promotion Action).
- **Displayed Actions:** Execute CIDR Scan, Promote Host to Official Asset.
- **Real-Time Strategy:** Progress event stream during active network scan.

### 5.3 Asset Inventory & Intelligence Screen
- **Primary Question:** *¿Cuál es la postura de riesgo y el ciclo de vida de nuestra infraestructura?*
- **Primary Entity:** `DigitalAsset`.
- **Displayed KPIs:** Total Assets, Active Assets, High Exposure Risk Assets, Expiring TLS Certificates.
- **Displayed Tables:** Master Asset Table (UUID, Name, Target URL/IP, Owner Email, Criticality, Risk Score, Status).
- **Displayed Actions:** Register Asset, Transition Lifecycle State, Update IP Location, Trigger Synthetic Probe.
- **Master-Detail View:** Slide-over drawer showing Forensic IP History Log (`ip_history`).

### 5.4 Raw Events Screen
- **Primary Question:** *¿Qué logs crudos han sido recibidos por los colectores de ingesta?*
- **Primary Entity:** `RawEventRecord`.
- **Displayed KPIs:** Total Raw Ingested, Ingestion Latency, Active Collectors.
- **Displayed Tables:** Raw Log Feed (Timestamp, Collector Type, Source IP, Hostname, Resolved Asset UUID, Payload Preview).
- **Displayed Actions:** Trigger Manual Parser Test, Copy Payload JSON.

### 5.5 Normalized Events Screen (GES Schema)
- **Primary Question:** *¿Cómo se estructuran los eventos en el formato semántico unificado GestivaSec Event Schema?*
- **Primary Entity:** `NormalizedEvent`.
- **Displayed KPIs:** Normalized Events Total, Categorization Rate %, GeoIP Match Rate %.
- **Displayed Tables:** GES Log Table (Timestamp, Category, Action, Severity, Source IP + GeoIP, Destination Asset, Outcome).
- **Displayed Actions:** Filter by Severity/Category, Expand GES JSON Payload.

---

## CHAPTER 6: UNIVERSAL SCREEN BLUEPRINT

Every screen across Gestiva Security follows a single, immutable structural blueprint:

```
+-----------------------------------------------------------------------+
| HEADER: Page Title, Subtitle, Active Tenant Badge, Main Actions       |
+-----------------------------------------------------------------------+
| TOOLBAR & FILTERS: Global Search Bar, Date Range, Category Filters    |
+-----------------------------------------------------------------------+
| KPI METRICS GRID: 4-10 Metric Cards (Value, Trend, Gauge Progress)    |
+-----------------------------------------------------------------------+
| MAIN CONTENT AREA: Data Tables, Interactive Charts, Split View        |
+-----------------------------------------------------------------------+
| DETAIL DRAWER (Slide-Over): Asset Details, Raw Event JSON, History    |
+-----------------------------------------------------------------------+
| FOOTER: Pagination Controls, Status Bar, Real-Time Polling Indicator |
+-----------------------------------------------------------------------+
```

---

## CHAPTER 7: NAVIGATION RULES

1. **Maximum Click Depth:** No primary operational entity or action shall be deeper than **2 clicks** from any active screen.
2. **Context Preservation:** Clicking an entity (e.g., Asset UUID inside an Alert) opens a **slide-over Inspector Drawer** instead of navigating away and destroying the analyst's active search state.
3. **Persistent Breadcrumbs:** Every sub-view displays explicit breadcrumbs reflecting the domain hierarchy (`Assets > Asset Intelligence > Asset-UUID-123`).

---

## CHAPTER 8: INTERACTION RULES

- **Buttons:** Primary actions use high-contrast solid accents; secondary actions use subtle outline containers. Destructive actions require a confirmation modal.
- **Tables:** Sticky headers, row click opens Inspector Drawer, server-side pagination, explicit empty/error states.
- **Search & Filtering:** Debounced input (300ms delay), instant reactive filtering.

---

## CHAPTER 9: REAL-TIME RULES

- **Live Polling:** Default 3,000ms polling for operational dashboards; WebSockets / SSE stream for high-throughput event logs.
- **Connection Loss Indicator:** If real-time connection drops, display a non-intrusive warning badge (`● OFFLINE / RECONNECTING`) while preserving last-known data state.

---

## CHAPTER 10: OPERATIONAL WORKFLOWS

### 10.1 Workflow 1: Threat Triage & Incident Resolution
```
Alert Triggered → Open Alert Detail → Inspect Asset UUID → View Normalized GES Events
     ↓
Promote to Incident → Assign SOC Analyst → Execute SOAR Playbook → Close with RCA
```

### 10.2 Workflow 2: Automated Asset Discovery & Onboarding
```
Execute CIDR Scan → Review Discovered Hosts → Inspect Open Ports → Promote to Asset
     ↓
Assign Owner Email (BR-02) → Set Criticality → Asset Registered in CMDB Inventory
```

---

## CHAPTER 11: PERMISSIONS MODEL (RBAC/ABAC)

- **Tenant Isolation (*BR-0004*):** All queries include `X-Organization-ID` header; UI restricts switching tenants based on user credentials.
- **Action Visibility:**
  - `SOC_ADMIN`: Full access (Create, Edit, Delete, Promote, SOAR Execution).
  - `SOC_ANALYST`: Read, Triage, Declare Incidents, Add Case Evidence.
  - `READ_ONLY`: Inspection views only; mutation buttons hidden.

---

## CHAPTER 12: STATUS MODEL & STATE MACHINE TRANSITIONS

### 12.1 Asset Lifecycle State Machine
$$\text{DISCOVERED} \longrightarrow \text{REGISTERED} \longrightarrow \text{ACTIVE} \rightleftharpoons \text{UNDER\_MAINTENANCE} \longrightarrow \text{ISOLATED} \longrightarrow \text{DECOMMISSIONED}$$

### 12.2 Incident State Machine
$$\text{DECLARED} \longrightarrow \text{ASSIGNED} \longrightarrow \text{IN\_DIAGNOSIS} \longrightarrow \text{REMEDIATED} \longrightarrow \text{CLOSED\_WITH\_RCA}$$

---

## CHAPTER 13: UI LOGICAL PATTERNS

- **Inspector Drawer:** Slide-over side panel used to inspect entity details without breaking active page context.
- **Timeline Feed:** Vertical chronological stream used in Incidents and Cases to show chronological evidence additions.

---

## CHAPTER 14: DASHBOARD PHILOSOPHY

- **What Belongs:** Real-time operational metrics, live bandwidth charts, active P1/P2 alerts, core service health statuses.
- **What Does Not Belong:** Static documentation, long configuration forms, non-actionable raw logs.

---

## CHAPTER 15: LOGICAL UX RULES

1. **One Screen, One Primary Responsibility.**
2. **Progressive Disclosure:** Show high-level summary metrics first; allow analysts to drill down into raw JSON payload on demand.
3. **Safety First:** Destructive actions (e.g., revoking tokens, isolating hosts) must be explicitly confirmed.

---

## CHAPTER 16: FRONTEND ENGINEERING RULES

- **Module Isolation:** Every domain module (`assets/`, `collectors/`, `events/`, `incidents/`) maintains its own API client, domain types, and view containers.
- **State Management:** Keep local UI state inside component view containers; share global authentication and tenant context cleanly.

---

## CHAPTER 17: QUALITY CHECKLIST

Before any new screen is approved for production, it must pass the following criteria:
- [x] Multi-tenant isolation (*BR-0004*) enforced via request headers.
- [x] Master-Detail Inspector Drawer implemented for primary entities.
- [x] Real-time live polling / WebSocket streaming configured.
- [x] Empty, loading, and error states explicitly handled.
- [x] Responsive layout without broken container overflows.

---

## CHAPTER 18: DEFINITION OF DONE

A screen or module is considered **DONE** when:
1. All domain actions and REST endpoints are fully integrated.
2. Acceptance test suite passes cleanly at 100%.
3. State machine transitions behave accurately according to business rules.
4. Zero visual or operational regressions are introduced into existing workflows.

---

## CHAPTER 19: APPENDIX — REUSABLE TEMPLATES

### 19.1 Master Screen Template Structure
```html
<main class="main-content">
    <header class="topbar">...</header>
    <section class="metrics-grid">...</section>
    <section class="content-card glass">
        <table class="data-table">...</table>
    </section>
    <div class="modal-overlay">...</div>
</main>
```
