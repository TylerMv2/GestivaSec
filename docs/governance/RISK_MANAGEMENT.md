# RISK MANAGEMENT — GESTIVASEC V1
> **Estado**: Borrador Oficial de Gobernanza  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Metodología de Gestión de Riesgos Técnicos

El proyecto **GestivaSec V1** clasifica y evalúa continuamente los riesgos arquitectónicos, operacionales y de seguridad mediante una matriz basada en **Probabilidad** e **Impacto**.

### 1.1 Matriz de Severidad
- **Crítico (P1)**: Bloquea la arquitectura central, compromete la seguridad del sistema o viola una directiva maestra.
- **Alto (P2)**: Degrada significativamente el rendimiento, la escalabilidad o la mantenibilidad.
- **Medio (P3)**: Afecta componentes secundarios o introduce deuda técnica menor si no se atiende a tiempo.
- **Bajo (P4)**: Inconvenientes menores de documentación o inconsistencias cosméticas.

---

## 2. Registro Inicial de Riesgos Identificados (Fase 0.1)

| ID | Riesgo Técnico | Impacto | Probabilidad | Severidad | Estrategia de Mitigación |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **RISK-01** | Intentar reutilizar código o esquemas SQL de los proyectos anteriores sin la debida depuración arquitectónica. | Alto | Media | **P2 (Alto)** | Prohibición explícita de copia. Exigencia de ADR justificado para cualquier adopción conceptual. |
| **RISK-02** | Definición prematura de tecnologías o lenguajes antes de completar la Fase 1 (Arquitectura) y Fase 2 (Dominio). | Alto | Media | **P2 (Alto)** | Congelamiento de implementación. No se escribirá código ni SQL en la Fase 0. |
| **RISK-03** | Ambigüedad en la terminología entre los equipos de desarrollo, redes y ciberseguridad. | Medio | Alta | **P2 (Alto)** | Creación y mantenimiento obligatorio del Glosario Oficial del Proyecto (`GLOSSARY.md`). |
| **RISK-04** | Falta de soporte offline o degradación ante fallos de red en entornos críticos de SOC/NOC. | Alto | Baja | **P2 (Alto)** | Incorporar la observabilidad y resiliencia offline en el diseño de arquitectura desde la Fase 1. |
