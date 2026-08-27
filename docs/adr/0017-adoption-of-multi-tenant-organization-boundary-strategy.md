# ADR-0017: Estrategia de Aislamiento de Organización Multi-Tenant (Organization Boundary)

## Estado
**Aceptado**

## Contexto
Se requiere formalizar la estrategia arquitectónica para garantizar que toda información y operación del sistema pertenezca y esté aislada dentro de la frontera de su Organización (`BR-04`).

## Problema
Garantizar la separación estricta de datos entre organizaciones sin permitir fugas accidentales o intencionales de información entre clientes.

## Alternativas Consideradas

### Alternativa 1: Filtro Manual no Enforzado
- Descripción: Confiar en la disciplina del programador para aplicar filtros por organización en cada consulta.
- Ventajas: Ninguna.
- Desventajas: Riesgo inaceptable de fuga de datos por omisión humana.

### Alternativa 2: Frontera Explícita de Organización en Entrada (Tenant Boundary Strategy)
- Descripción: Exigir y validar el contexto de Organización en toda frontera de entrada del software como precondición obligatoria.
- Ventajas: Cero tolerancia a fugas de datos, cumplimiento de Zero Trust y `BR-04`.
- Desventajas: Sobrecarga de validación inicial en la frontera del módulo.

### Matriz Comparativa

| Criterio de Evaluación | Filtro Manual | Frontera Explícita Multi-Tenant |
| :--- | :---: | :---: |
| **Garantía de Aislamiento** | Muy Baja | **Inviolable (100%)** |
| **Cumplimiento Zero Trust** | Nulo | **Total** |
| **Seguridad por Diseño** | Baja | **Alta** |

## Decisión
Adoptar la **Estrategia de Frontera Explícita de Organización**. Toda solicitud porta el contexto validado de Organización (`BR-04`), verificado antes de ejecutar cualquier regla del dominio.

## Justificación
Cumple rigurosamente con los principios de Security by Design, Privacy by Design y la regla de negocio `BR-04`.

## Consecuencias
- **Positivas**: Aislamiento total de información entre organizaciones.
- **Negativas**: Necesidad de pasar y evaluar el contexto organizativo en las entradas.

## Riesgos
- Intento de omisión del contexto en llamadas internas.

## Mitigaciones
- Enforzar la validación de contexto organizativo a través del módulo `MOD-07` / `COMP-07`.

## Impacto sobre Documentos Existentes
- Fundamenta la arquitectura de capas (6.2) y el control de fronteras.
