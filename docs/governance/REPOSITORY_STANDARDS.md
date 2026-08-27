# REPOSITORY STANDARDS — GESTIVASEC V1
> **Estado**: Estándar Oficial de Repositorio & Git  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Estrategia de Ramificación (Git Branching Model)

Se adopta una estrategia basada en **Trunk-Based Development** con ramas cortas de características (*Feature Branches*):

- `main`: Rama de producción inmutable y siempre desplegable.
- `feature/FASE-N-nombre-descriptivo`: Rama temporal para desarrollo por sub-fases autorizadas.
- `hotfix/descripcion`: Rama prioritaria para parches de seguridad críticos.

---

## 2. Convención de Commits (Conventional Commits 1.0.0)

Todo mensaje de commit debe estructurarse obligatoriamente bajo el siguiente formato:

```
<tipo>(<alcance>): <descripción concisa en imperativo>

[cuerpo opcional detallando la motivación técnica]

[pie opcional de referencia a ADRs o tareas]
```

### Tipos Permitidos:
- `docs`: Modificación exclusivamente en documentación o gobernanza.
- `feat`: Nueva característica funcional en una fase aprobada.
- `fix`: Corrección de un error comprobado con prueba unitaria.
- `refactor`: Cambio de código que no altera la funcionalidad ni añade características.
- `test`: Adición o corrección de suites de pruebas.
- `chore`: Tareas de mantenimiento de build o scripts auxiliares.

### Ejemplo Oficial:
```
docs(governance): add engineering and architecture standards specification

Incorporate ENGINEERING_STANDARDS.md and ARCHITECTURE_STANDARDS.md for Phase 0.
Refs: ADR-0002
```
