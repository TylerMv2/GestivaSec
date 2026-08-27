# ADR FRAMEWORK & DECISION LIFECYCLE — GESTIVASEC V1
> **Estado**: Marco Oficial de ADRs  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Ciclo de Vida de una Decisión de Arquitectura

Todo ADR atravesará por los siguientes estados controlados:

```
 ┌──────────┐     ┌──────────┐     ┌────────────┐
 │ Proposed │ ──► │ Accepted │ ──► │ Superceded │
 └────┬─────┘     └──────────┘     └────────────┘
      │           ┌──────────┐
      └─────────► │ Rejected │
                  └──────────┘
```

1. **Proposed (Propuesto)**: ADR presentado por un miembro del comité en la sub-fase correspondiente.
2. **Accepted (Aprobado)**: Revisado y ratificado por el Director del Proyecto / Usuario.
3. **Rejected (Rechazado)**: Evaluado pero descartado por inviabilidad o violación de directiva maestra.
4. **Superceded (Reemplazado)**: Una decisión histórica sustituida formalmente por un ADR posterior.

---

## 2. Índice Central de ADRs (ADR Register)

El archivo `docs/adr/README.md` mantendrá la lista secuencial inmutable de todas las decisiones aprobadas en el proyecto.
