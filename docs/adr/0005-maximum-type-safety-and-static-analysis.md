# ADR-0005: Obligatoriedad de Máxima Seguridad de Tipos y Análisis Estático en Todos los Lenguajes

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
Los errores en tiempo de ejecución (`NullPointerException`, `TypeError: Cannot read properties of undefined`, conversiones implícitas no deseadas) y las vulnerabilidades de seguridad comunes son la causa principal de caídas en sistemas SOC/NOC. La detección temprana en tiempo de compilación/análisis estático es órdenes de magnitud más económica y segura que el parcheo en producción.

## Opciones Consideradas
1. **Tipado permisivo / estándar de los compiladores**: Permitir tipos dinámicos o aserciones sueltas (`any`, omitir type hints). *(Rechazado: Aumenta drásticamente el riesgo de bugs en tiempo de ejecución)*.
2. **Máxima Seguridad de Tipos y Análisis Estático Obligatorio**: Exigir configuraciones estrictas en compiladores (`tsconfig` estricto, `mypy --strict`, `golangci-lint`, `sqlfluff`) y bloquear el código que no cumpla. *(Seleccionado)*.

## Decisión Seleccionada
Adoptar la norma inmutable de que **todo lenguaje utilizado en GestivaSec V1 operará bajo su máximo nivel razonable de seguridad de tipos y análisis estático estricto**, prohibiendo tipos dinámicos sueltos (`any`), castings inseguros o el silenciamiento de linters.

## Consecuencias
### Positivas:
- Eliminación en tiempo de desarrollo de más del 90% de los errores típicos de runtime (null/undefined pointers).
- Código documentado nativamente mediante firmas de tipo explícitas.
- Integración automatizada en pipelines CI/CD.

### Negativas / Compromisos (Trade-offs):
- Se requiere mayor precisión y rigor inicial al escribir interfaces y modelos de datos.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Security by Design?: Sí
- ¿Respeta Audit by Design?: Sí
