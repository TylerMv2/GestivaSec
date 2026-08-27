# GESTIVA SECURITY — QUALITY GATES & GOVERNANCE RULES

---

## 1. REGLA INVIOLABLE DE APROBACIÓN POR EL ARB (ARB APPROVAL RULE)
Queda estrictamente prohibido que el autor de cualquier documento de ingeniería o especificación asigne el estado `APPROVED`, `COMPLETED`, `LOCKED` o `FREEZED`.

### Estados Permitidos para el Autor:
- **`DRAFT`**: Documento en elaboración inicial.
- **`IN_PROGRESS`**: Documento activo en desarrollo (máximo UN solo documento activo simultáneamente en todo el proyecto).
- **`REVIEW`**: Documento completo que ha superado la autoevaluación de calidad y aguarda revisión formal.

### Estado Exclusivo del ARB:
- **`APPROVED`**: Asignado **única y exclusivamente** por el **Architecture Review Board (ARB)** tras auditoría formal de arquitectura.

---

## 2. QUALITY GATES AUTOMATIZADOS DE CÓDIGO
- **Domain Purity**: Cero importaciones de infraestructura en `backend/domain/`.
- **Circular Imports**: Cero importaciones circulares en el paquete backend.
- **Technical Debt Bounds**: 0 marcas `FIXME`, TODOs < 10, funciones < 150 líneas, clases < 300 líneas.
- **Coverage**: Cobertura de pruebas automatizadas en Pytest >= 80% (Actual: **98.1%**).
- **Golden Demo**: Flujo E2E continuo verificado 100% PASS (39/39 E2E tests).
