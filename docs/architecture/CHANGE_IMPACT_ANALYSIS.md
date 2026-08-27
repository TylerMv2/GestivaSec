> **Artifact ID**: `SA-0008`  
> **Artifact Name**: Change Impact Analysis Framework  
> **Artifact Type**: Architecture Governance Framework  
> **Version**: 1.0  
> **Status**: Approved  
> **Owner**: Architecture Review Board (ARB)  
> **Created**: 2026-07-25  
> **Last Updated**: 2026-07-25  
> **Last Review**: 2026-07-25  
> **Review Due**: 2026-08-25  
> **Depends On**: `TRACEABILITY_MATRIX`, `ARTIFACT_CATALOG`  
> **Referenced By**: `SA-0001`, `SA-0007`  
> **Produces**: `IMPACT_REPORT`  
> **Consumes**: `TRACEABILITY_MATRIX`  
> **Supersedes**: NONE  
> **Superseded By**: NONE  
> **Related Artifacts**: `TRACEABILITY_MATRIX.md`, `ARTIFACT_CATALOG.md`  

---

# CHANGE IMPACT ANALYSIS FRAMEWORK — GESTIVA SECURITY (GESTIVASEC V1)

---

## 1. Resumen Ejecutivo
El **Change Impact Analysis Framework** provee el protocolo formal de evaluación del impacto de cambios para cualquier modificación en el **Enterprise Architecture Repository (EAR)**. Todo artefacto expuesto a cambio debe someterse a este análisis cuádruple antes de ser sometido a consideración del ARB.

---

## 2. Preguntas Fundamentales de Evaluación de Impacto

1. **¿Qué artefactos afecta la modificación propuesta?** *(Impacto Aguas Abajo / Downstream)*
2. **¿Qué artefactos afectan al elemento modificado?** *(Impacto Aguas Arriba / Upstream)*
3. **¿Qué componentes o módulos de software dependen de él?** *(Impacto de Software)*
4. **¿Qué requisitos o reglas de negocio dejarían de cumplirse si el artefacto desaparece o se altera?** *(Impacto de Negocio)*

---

## 3. Ejemplo de Evaluación de Impacto (Demostración de Protocolo)

### Evaluación de Modificación sobre `BR-0004` (Aislamiento por Organización)
- **Artefactos Afectados Aguas Abajo**: `QA-0001`, `QA-0008`, `AC-0005`, `AP-0002`, `ADR-0017`, `SA-0002` (Architecture Style).
- **Artefactos que lo Afectan Aguas Arriba**: `BO-0001` (Monitoreo de Activos).
- **Componentes / Módulos Dependientes**: `COMP-0007` (Organization Boundary Component), `MOD-0007`.
- **Requisitos de Negocio Incumplidos si se Elimina**: `REQ-0008` (Gestión de Contexto de Organización). Fuga de aislamiento multi-tenant e incumplimiento normativo de privacidad por diseño (`PRIN-02`).

---

## 4. Protocolo de Aprobación por el ARB
Ninguna modificación en un artefacto con estado `Approved` podrá aplicarse sin la presentación formal de este informe de impacto y la aprobación del ARB.
