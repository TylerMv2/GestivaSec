# GESTIVASEC_USER_PERSONAS.md — OPERATIONAL USER PERSONAS & USER JOURNEYS

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `APPROVED & LOCKED GOVERNANCE SPECIFICATION`  
**Target Audience:** UI/UX Designers, Product Owners, Frontend Engineers, QA Engineers  
**Date:** 2026-07-26  

---

## 1. EXECUTIVE SUMMARY

This document defines the 9 operational user personas within **Gestiva Security**. Each persona represents a specific operational role within a modern Security Operations Center (SOC) and enterprise IT organization.

---

## 2. OPERATIONAL PERSONAS SPECIFICATION

### 2.1 SOC Tier 1 Analyst (Triage & Incident Detection)
- **Objectives:** Fast triage of incoming alerts, suppression of false positives, rapid escalation of P1/P2 incidents.
- **Responsibilities:** Monitor live telemetry grid, triage alerts, inspect raw/normalized logs, verify asset context.
- **Daily Tasks:** Review P1 alert queues, validate GES normalized events, escalate active threats.
- **Pain Points:** Alert fatigue, slow query performance, lost context during screen navigation.
- **Critical KPIs:** Mean Time to Detect (MTTD), Triage Rate per hour, False Positive Ratio.
- **Navigation Priorities:** Operational SOC Dashboard, Alert Center, Normalized Events.
- **Required Permissions:** `alerts:read`, `alerts:triage`, `events:read`, `incidents:create`.
- **Frequently Used Modules:** Dashboard, Alert Center, Normalized Events (GES), Asset Intelligence Drawer.
- **Primary Operational Workflow:** Alert Triggered $\rightarrow$ Open Inspector Drawer $\rightarrow$ Verify Asset UUID $\rightarrow$ Promote to Incident.

### 2.2 SOC Tier 2 Analyst (Incident Response & Remediation)
- **Objectives:** In-depth investigation of complex security incidents, containment of compromised hosts, execution of SOAR playbooks.
- **Responsibilities:** Manage Incident lifecycles, execute SOAR isolation playbooks, conduct root cause analysis.
- **Pain Points:** Lack of asset owner contact details (*BR-02*), disjointed forensic tools.
- **Navigation Priorities:** Incident Console, SOAR Playbooks, Asset Intelligence.
- **Required Permissions:** `incidents:write`, `soar:execute`, `assets:isolate`.

### 2.3 SOC Tier 3 Analyst / Threat Hunter
- **Objectives:** Proactive threat hunting, hypothesis testing, identifying APT presence without existing signatures.
- **Responsibilities:** Query normalized event streams, create custom correlation rules, analyze threat intelligence IoCs.
- **Navigation Priorities:** Threat Intelligence, Correlation Engine, Detection Rules Registry.

### 2.4 SOC Manager
- **Objectives:** Oversight of SOC operational performance, team workload balancing, SLA compliance.
- **Navigation Priorities:** Dashboard SOC Operativo, Incidents Overview, Reports Engine.

### 2.5 Platform Administrator
- **Objectives:** System health, tenant management (*BR-0004*), user RBAC roles, collector ingestion maintenance.
- **Navigation Priorities:** Collector Manager, Organization Selector, User/Role RBAC, Audit Logs (*BR-0005*).

### 2.6 Security Engineer
- **Objectives:** Maintaining ingestion pipelines, configuring log collectors, tuning detection rules.
- **Navigation Priorities:** Collectors Framework, Detection Rules, System Settings.

### 2.7 Compliance Auditor
- **Objectives:** Audit log verification (*BR-0005*), regulatory compliance (ISO 27001, SOC2), access policy verification.
- **Navigation Priorities:** Audit Trail, RBAC Governance, Asset Inventory Reports.

### 2.8 CISO / Executive
- **Objectives:** Strategic risk visualization, organizational security posture, executive reporting.
- **Navigation Priorities:** Dashboard Operational Telemetry, Asset Exposure Risk Matrix, Executive Reports.

---

## 3. USER JOURNEY MAP: P1 INCIDENT TRIAGE & REMEDIATION

```
[SOC Tier 1] Alert P1 Triggered in Operational Dashboard
     ↓
[SOC Tier 1] Opens Inspector Drawer → Inspects Asset UUID & Owner Email (BR-02)
     ↓
[SOC Tier 1] Validates Normalized GES Events → Escalates to Incident P1
     ↓
[SOC Tier 2] Receives Incident → Triggers Automated SOAR Host Isolation Playbook
     ↓
[SOC Tier 2] Resolves Threat → Updates Incident to CLOSED_WITH_RCA
```
