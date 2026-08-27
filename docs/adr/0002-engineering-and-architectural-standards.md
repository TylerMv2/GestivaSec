# ADR-0002: Adopción de Estándares de Ingeniería, Arquitectura, Repositorio, Documentación y Riesgos (Fase 0.2-0.7)

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
Tras completar la gobernanza constitucional (Fase 0.1), se requiere formalizar los estándares operacionales de ingeniería de código, modelado C4, estrategia de ramas Git, convenciones de commits, formato de documentación y marco de riesgos STRIDE para asegurar la máxima calidad técnica antes de iniciar la Fase 1.

## Opciones Consideradas
1. **Reglas implícitas o flexibles**: Dejar a discreción de cada desarrollador la estructura de commits, tipos y documentación. *(Rechazado: Produce inconsistencias y dificulta la mantenibilidad)*.
2. **Adopción de Marcos Estándar Formales (C4, SemVer, Conventional Commits, STRIDE, Clean Code)**: Definir especificaciones rigurosas y vinculantes en el repositorio. *(Seleccionado)*.

## Decisión Seleccionada
Aprobar y ratificar los documentos de estándares correspondientes a las sub-fases 0.2 a 0.7:
- `ENGINEERING_STANDARDS.md` (Fase 0.2)
- `ARCHITECTURE_STANDARDS.md` (Fase 0.3)
- `REPOSITORY_STANDARDS.md` (Fase 0.4)
- `DOCUMENTATION_STANDARDS.md` (Fase 0.5)
- `ADR_FRAMEWORK.md` (Fase 0.6)
- `RISK_FRAMEWORK.md` (Fase 0.7)

## Consecuencias
### Positivas:
- Homogeneidad absoluta en el código, documentación y diagramación.
- Integración nativa de ciberseguridad mediante modelado STRIDE desde las fases de diseño.
- Registro inmutable y claro del histórico del proyecto.

### Negativas / Compromisos (Trade-offs):
- Mayor rigor requerido al redactar mensajes de commit y especificaciones arquitectónicas.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Security by Design?: Sí
- ¿Respeta Audit by Design?: Sí
