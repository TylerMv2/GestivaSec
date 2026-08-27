# ADR-0009: Adopción Oficial de la Especificación de Principios de Arquitectura Empresarial (TOGAF)

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
En el desarrollo de la Fase 3 (Enterprise Architecture), se requería definir los principios inmutables que gobernarán la toma de todas las decisiones futuras de arquitectura, diseño lógico, topología física, persistencia y seguridad de GestivaSec V1. Sin principios formales, los equipos corren el riesgo de introducir inconsistencias, acoplamiento rígido o violaciones de seguridad durante el desarrollo.

## Opciones Consideradas
1. **Toma de Decisiones Ad-Hoc / Discrecional**: Permitir que cada arquitecto o desarrollador decida patrones y estructuras según su criterio individual durante la implementación. *(Rechazado: Alta probabilidad de deuda técnica y fallos de gobernanza)*.
2. **Especificación Formal de Principios de Arquitectura (TOGAF 10 / SEI)**: Establecer un catálogo inmutable de principios etiquetados como Mandatory/Recommended con matriz de gobernanza, políticas de excepción y trazabilidad estricta. *(Seleccionado)*.

## Decisión Seleccionada
Adoptar y ratificar los 6 Principios de Arquitectura especificados en el documento `02_ARCHITECTURAL_PRINCIPLES.md`:
- **PRIN-01 (Mandatory)**: Domain-Driven Architecture (DDD First).
- **PRIN-02 (Mandatory)**: Zero Trust & Security by Design (Multi-Tenant RLS).
- **PRIN-03 (Mandatory)**: Immutable Auditability & Non-Repudiation (Append-Only).
- **PRIN-04 (Mandatory)**: Loose Coupling & Event Awareness (EDA / Bus Asíncrono).
- **PRIN-05 (Mandatory)**: Infrastructure Agnostic & Vendor Neutrality (Adaptadores ACL Hexagonales).
- **PRIN-06 (Recommended)**: Configuration over Code & Automation First.

## Consecuencias
### Positivas:
- Criterio unificado e inalterable para evaluar toda propuesta técnica, ADR o diseño futuro.
- Prohibición estricta de excepciones para los principios Mandatory (`PRIN-01` a `PRIN-05`).
- Trazabilidad total entre los objetivos de negocio del ecosistema Gestiva y las decisiones de arquitectura.

### Negativas / Compromisos (Trade-offs):
- Requiere mayor disciplina de ingeniería al obligar a traducir datos externos mediante la Capa Anti-Corrupción (ACL) y pasar por el proceso formal de gobernanza.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Security by Design?: Sí
- ¿Respeta Audit by Design?: Sí
