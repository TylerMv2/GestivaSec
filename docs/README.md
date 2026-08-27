# GESTIVA SECURITY (GESTIVASEC V1) — ENTERPRISE DOCUMENTATION REPOSITORY

Bienvenido al repositorio documental oficial de **Gestiva Security**. Toda la arquitectura, visión, modelo de dominio, especificaciones y decisiones están organizadas según la metodología estándar Enterprise (carpetas numeradas `00-governance` a `10-release`).

---

## 📌 ÍNDICE MAESTRO Y ESTRUCTURA DE REPOSITORIO (00-10)

```
gestiva-security/docs/
├── 📁 00-governance/            # Reglas del proyecto, Visión y Quality Gates
│   ├── 📄 PRODUCT_VISION.md
│   └── 📄 QUALITY_GATES.md
│
├── 📁 01-product/               # Hoja de ruta y mapa de capacidades
│   ├── 📄 PRODUCT_ROADMAP.md
│   └── 📄 CAPABILITY_MAP.md
│
├── 📁 02-domain-model/          # Modelado de dominio del negocio (Dominio Puro)
│   ├── 📄 IDENTITY_DOMAIN.md
│   ├── 📄 ASSET_DOMAIN.md
│   ├── 📄 DISCOVERY_DOMAIN.md
│   ├── 📄 MONITORING_DOMAIN.md
│   ├── 📄 THREAT_INTELLIGENCE_DOMAIN.md
│   ├── 📄 ALERT_DOMAIN.md
│   └── 📄 INCIDENT_DOMAIN.md
│
├── 📁 03-architecture/          # Arquitectura técnica del sistema
│   ├── 📄 SYSTEM_CONTEXT.md
│   └── 📄 CONTAINER_ARCHITECTURE.md
│
├── 📁 04-decisions/             # RFC (Propuestas) y ADR (Decisiones Congeladas)
│   ├── 📁 rfc/
│   │   └── 📄 RFC-0001-SOC-DASHBOARD-UX.md
│   └── 📁 adr/
│       └── 📄 ADR-0001-FASTAPI-FAST-PROBING.md
│
├── 📁 05-specifications/        # Especificaciones de experiencia de usuario y pantallas
│   ├── 📄 DASHBOARD_SPEC.md
│   ├── 📄 INCIDENT_CENTER_SPEC.md
│   ├── 📄 ASSETS_SPEC.md
│   └── 📄 THREAT_INTELLIGENCE_SPEC.md
│
├── 📁 06-design-system/         # Design System visual Dark-First SOC
│   └── 📄 DESIGN_PRINCIPLES.md
│
├── 📁 07-api/                   # Guías y convenciones de API REST
│   └── 📄 API_GUIDELINES.md
│
├── 📁 08-testing/               # Estrategias de prueba automatizadas
│   └── 📄 TEST_STRATEGY.md
│
├── 📁 09-operations/            # Playbooks del SOC y Runbooks operacionales
│   ├── 📄 SOC_PLAYBOOKS.md
│   └── 📄 RUNBOOKS.md
│
└── 📁 10-release/               # Proceso de releases y notas de versión
    ├── 📄 RELEASE_PROCESS.md
    └── 📄 RELEASE_NOTES_v0.1.0.md
```

---

## 🔄 FLUJO DE INGENIERÍA COMPLETO

```
Idea ──► Problema ──► Capability ──► Dominio (*_DOMAIN.md) ──► RFC ──► ADR (ADR-XXXX.md)
                                                                            │
                                                                            ▼
Runbook ◄── Playbook ◄── Release ◄── Testing ◄── Implementation ◄── Specification (*_SPEC.md)
```

---

## 🏛️ ESTADO DE GOBERNANZA
- **Estructura Documental**: 100% Organizada y Congelada.
- **Trazabilidad**: 100% Eslabones Vinculados.
- **Quality Gate**: **PASS (56/56 Tests - 98.1% Coverage)**.
