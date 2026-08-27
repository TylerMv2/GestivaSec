# Gestiva Security — Security Architecture & RBAC Policy

## Multi-Tenant Security (`BR-0004`)
Every database query, API router, report job, and SOAR execution inspects tenant authorization via `X-Organization-ID` or authenticated user context. Cross-tenant access is strictly forbidden and rejected at the router boundary.

## Role-Based Access Control (RBAC)
- **SUPER_ADMIN**: Full system administration, organization management, role assignment.
- **SOC_ADMIN**: Full operational control over detection rules, playbooks, incident lifecycle, and reporting.
- **SOC_ANALYST**: Triage findings, assign incidents, request SOAR execution approvals, add evidence.
- **READ_ONLY**: View-only access to dashboards and reports.

## SOAR Safety Controls
- **Action Risk Allowlist**: Only explicitly registered adapters (`MockEDRAdapter`, `MockFirewallAdapter`, `MockIdentityAdapter`, `MockNotificationAdapter`) may execute actions.
- **Approval Gates**: Actions classified as `HIGH` or `CRITICAL` risk pause execution until approved by a SOC Lead.
- **Rollback Engine**: Integrated reversal handlers permit instant undo of host isolation or block rules.
