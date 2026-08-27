# ADR-0015: Adopción del Patrón de Arquitectura Hexagonal (Ports & Adapters)

## Estado
**Aceptado**

## Contexto
Se requiere definir el patrón de diseño interno para aislar la lógica del dominio puro (Fase 5) de cualquier detalle técnico de infraestructura, interfaces de usuario o persistencia de datos.

## Problema
Evitar que las decisiones tecnológicas (frameworks, bases de datos o servicios de comunicación) contaminen o modifiquen la especificación pura del dominio de negocio (`BR-01` a `BR-05`).

## Alternativas Consideradas

### Alternativa 1: Arquitectura N-Capas Tradicional (Acoplada a Persistencia)
- Descripción: Capa de Presentación ➔ Capa de Negocio ➔ Capa de Datos con dependencia directa de la base de datos.
- Ventajas: Estructura convencional conocida.
- Desventajas: Acoplamiento de la lógica del dominio a esquemas y ORMs de persistencia.

### Alternativa 2: Arquitectura Hexagonal (Ports & Adapters)
- Descripción: Dominio en el centro expuesto a través de interfaces puras (Puertos), e infraestructura implementada en adaptadores externos.
- Ventajas: Aislamiento 100% puro del dominio, testabilidad sin infraestructura real, cumplimiento de `C-02`.
- Desventajas: Mayor cantidad inicial de interfaces y objetos de transferencia.

### Matriz Comparativa

| Criterio de Evaluación | N-Capas Tradicional | Arquitectura Hexagonal |
| :--- | :---: | :---: |
| **Independencia del Dominio** | Baja | **Absoluta (100%)** |
| **Desacoplamiento Tecnológico** | Medio | **Alto** |
| **Testabilidad sin BD** | Compleja | **Directa** |

## Decisión
Adoptar el patrón de **Arquitectura Hexagonal (Puertos y Adaptadores)** dentro de cada módulo del sistema.

## Justificación
Garantiza el desacoplamiento total exigido por los principios de la plataforma, asegurando que la lógica del negocio no dependa de librerías ni tecnologías de infraestructura.

## Consecuencias
- **Positivas**: Dominio puro e independiente, alta testabilidad, sustitución transparente de tecnología.
- **Negativas**: Mayor número de abstracciones iniciales.

## Riesgos
- Curva de aprendizaje para desarrolladores no familiarizados con el desacoplamiento por puertos.

## Mitigaciones
- Especificación clara de contratos de servicios y puertos de interfaz en la Fase 6.11.

## Impacto sobre Documentos Existentes
- Fundamenta la estructura de capas (6.2) y los contratos de servicio (6.11).
