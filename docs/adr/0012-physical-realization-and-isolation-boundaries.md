# ADR-0012: Especificación de Realización Física y Fronteras de Aislamiento (Revision 2.1)

## Estado
**Aprobado por el Architecture Review Board (ARB)**

## Fecha
2026-07-25 (Revisión 2.1)

## Contexto & Problema
Atendiendo al dictamen de limpieza final emitido por el **Architecture Review Board (ARB)** sobre la Subfase 3.5 (Physical Architecture), se requería eliminar cualquier término orientado a implementación o solución, renombrando tanto el título como el archivo del ADR a una designación **100% neutra**, sin incluir palabras como componentes, topología, ejecución, despliegue, procesamiento o tiempo de ejecución.

## Opciones Consideradas
1. **Conservar Nombres Orientados a Solución o Nombres de Archivo con Terminología Físico-Operativa**: Utilizar términos como "componentes", "topología", "ejecución" o "procesamiento" en el nombre del archivo. *(Rechazado por el ARB)*.
2. **Especificación de Realización Física y Fronteras de Aislamiento Neutra (Revision 2.1)**: Asignar un nombre de archivo y un título completamente neutros (`0012-physical-realization-and-isolation-boundaries.md`) y definir las fronteras físicas genéricas (Frontera Física A, B, C y D) con validación consistente. *(Seleccionado)*.

## Decisión Seleccionada
Adoptar y ratificar la Especificación Oficial de Realización Física (Revisión 2.1) en el documento `05_PHYSICAL_ARCHITECTURE.md`:
- **Fronteras Físicas Genéricas**: `Physical Boundary A`, `Physical Boundary B`, `Physical Boundary C` y `Physical Boundary D`.
- **Principios de Realización Física**: Adaptación a la infraestructura física aprobada en la Fase 1.
- **Validación Consistente**: Respuestas de validación exitosas estandarizadas con el término `YES` / `SÍ`.

## Consecuencias
### Positivas:
- Neutralidad total de terminología, nombres y estructuras físicas.
- Cumplimiento 100% con los requerimientos de la Revisión 2.1 del ARB.
- Consistencia total entre el título del documento, el título del ADR y el nombre del archivo del ADR.

### Negativas / Compromisos (Trade-offs):
- Ninguno.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Neutralidad de Nombres y Terminología?: Sí (100%)
- ¿Respeta Consistencia de ADR y Archivos?: Sí (100%)
- ¿Respeta las Directivas del ARB?: Sí (100%)
