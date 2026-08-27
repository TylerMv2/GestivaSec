# PROJECT STRUCTURE — GESTIVASEC V1
> **Estado**: Especificación de Organización sin Código  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Topología del Monorepo / Repositorio Principal

Esta estructura define la organización conceptual y física de los archivos del sistema. En esta fase de gobernanza, **no contiene archivos de código**, únicamente la jerarquía de directorios declarada.

```
GestivaSec_V1/
├── .github/                     # Workflows CI/CD, templates de PRs e issues (Futuro)
├── docs/                        # Documentación Oficial de Gobernanza y Arquitectura
│   ├── governance/              # Constitución y Reglas (Fase 0.1)
│   │   ├── ENGINEERING_PRINCIPLES.md
│   │   ├── DEVELOPMENT_WORKFLOW.md
│   │   ├── GOVERNANCE_MODEL.md
│   │   ├── PROJECT_STRUCTURE.md
│   │   ├── DECISION_POLICY.md
│   │   ├── RISK_MANAGEMENT.md
│   │   ├── ASSUMPTIONS.md
│   │   └── GLOSSARY.md
│   ├── adr/                     # Architectural Decision Records (ADRs)
│   │   └── 0001-project-governance-constitution.md
│   ├── architecture/            # Diagramación C4, Topologías y Contratos (Fase 1)
│   └── domain/                  # Especificación de Entidades y Contextos Delimitados (Fase 2)
├── infrastructure/              # Terraform / CloudFormation / Helm / SQL Schemas (Sin código por ahora)
├── backend/                     # Capas Hexagonales del Servidor (Sin código por ahora)
│   ├── domain/                  # Lógica pura del negocio y entidades
│   ├── application/             # Casos de uso y bus de eventos
│   └── infrastructure/          # Conectores, repositorios y adaptadores
├── frontend/                    # Aplicación Web SOC/NOC Enterprise (Sin código por ahora)
│   ├── src/
│   │   ├── domain/
│   │   ├── application/
│   │   └── presentation/
└── tests/                       # Suites de Pruebas Automatizadas (Unit, Integration, E2E)
```

---

## 2. Reglas de Organización

1. **Separación Estricta**: La documentación arquitectónica reside en `docs/`. Los contratos de interfaz o esquemas no deben mezclarse directamente con el código fuente hasta las fases correspondientes.
2. **Directorios de Trabajo**: Cada paquete o capa responderá directamente a la arquitectura hexagonal (Dominio ➔ Aplicación ➔ Infraestructura ➔ Presentación).
