# Gestiva Security (GestivaSec V1) Enterprise SOC & Observability Platform

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-blue.svg)](https://gestivaone.com)
[![Architecture: Self-Hosted](https://img.shields.io/badge/Architecture-Self--Hosted-green.svg)](#architecture)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://python.org)

**Gestiva Security** is an enterprise-grade, cloud-agnostic, self-hosted Continuous Observability and SOC (Security Operations Center) Platform. Built for total infrastructure portability, GestivaSec runs on local Linux servers, virtual machines, Docker containers, or bare-metal environments without any mandatory cloud provider lock-in.

---

## 🚀 Key Features & Capabilities

- **Stage 1 — Live SOC Operational Dashboard**: Real-time telemetry, risk posture scores, and system vitals.
- **Stage 2 — Asset Discovery Engine**: Autonomous active & passive domain, sub-domain, and IP discovery.
- **Stage 3 — Asset Intelligence & CMDB**: Lifecycle state tracking, vulnerability scoring, and asset fingerprinting.
- **Stage 4 — Event Collectors Framework**: Multi-protocol log collection (Syslog, NetFlow, Webhooks, API).
- **Stage 5 — Event Normalization & GES**: Canonical GestivaSec Event Schema (GES) normalization.
- **Stage 6 — Detection Engine**: High-speed security rule matching and anomaly detection.
- **Stage 7 — Correlation Engine**: Temporal and spatial attack chain generation across telemetry sources.
- **Stage 8 — Incident & Case Management**: SLA tracking, investigation workspaces, and mandatory Root Cause Analysis (RCA).
- **Stage 9 — Threat Intelligence Engine**: Observable matching, deterministic indicator normalization, and enrichment.
- **Stage 10 — SOAR Engine**: Controlled, policy-driven automated response playbooks with human approval gates and rollback handlers.
- **Stage 11 — Enterprise Reporting & Audit Export**: Executive PDF/CSV/JSON report generation and compliance audit log exports.

---

## 🛠 Quick Start (Local & Self-Hosted)

### Prerequisites
- Linux Server (Ubuntu 20.04/22.04/24.04, Debian, Kali, CentOS, RHEL)
- Python 3.10+
- PostgreSQL 15+ (or built-in SQLite for local dev)

### Installation
```bash
git clone https://github.com/gestivaone/gestiva_observability.git
cd gestiva_observability
sudo ./install.sh
```

### Docker Deployment
```bash
docker compose up -d
```

Access the SOC Console at `http://localhost:8000`.

---

## 📚 Documentation Sitemap

- [DEPLOYMENT.md](file:///home/sh4d0w/Projects/gestiva_observability/docs/DEPLOYMENT.md) — Production deployment guides for Nginx, Systemd, and Docker.
- [INSTALLATION.md](file:///home/sh4d0w/Projects/gestiva_observability/docs/INSTALLATION.md) — Step-by-step installation instructions for Linux and bare-metal servers.
- [CONFIGURATION.md](file:///home/sh4d0w/Projects/gestiva_observability/docs/CONFIGURATION.md) — Centralized environment variables (`.env`) reference guide.
- [ARCHITECTURE.md](file:///home/sh4d0w/Projects/gestiva_observability/docs/ARCHITECTURE.md) — Frozen Enterprise Architecture and Kernel v1.0 specifications.
- [SECURITY.md](file:///home/sh4d0w/Projects/gestiva_observability/docs/SECURITY.md) — Multi-tenant security (`BR-0004`), RBAC rules, and safety models.
- [TROUBLESHOOTING.md](file:///home/sh4d0w/Projects/gestiva_observability/docs/TROUBLESHOOTING.md) — Diagnostic guides and common error resolutions.
