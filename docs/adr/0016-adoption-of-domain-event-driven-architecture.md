# ADR-0016: Adopción de Comunicación Basada en Eventos del Dominio (Domain Events)

## Estado
**Aceptado**

## Contexto
Se requiere establecer el mecanismo de comunicación e interacción entre módulos para reaccionar ante cambios de estado operacionales (ej. declaración de incidentes o captura de auditoría).

## Problema
Evitar llamadas síncronas acopladas entre módulos que generen dependencias circulares o bloqueos en la ejecución del negocio.

## Alternativas Consideradas

### Alternativa 1: Invocación Síncrona Directa Inter-Modular
- Descripción: Un módulo llama directamente a métodos de otro módulo.
- Ventajas: Simplicidad inicial.
- Desventajas: Acoplamiento fuerte, dependencias circulares, propagación de fallas.

### Alternativa 2: Comunicación Basada en Eventos del Dominio (Domain Event-Driven)
- Descripción: Publicación de eventos semánticos del dominio cuando ocurren cambios de estado; suscripción desacoplada.
- Ventajas: Desacoplamiento temporal y espacial, facilidad para la traza de auditoría (`BR-05`).
- Desventajas: Gestión de consistencia eventual entre módulos.

### Matriz Comparativa

| Criterio de Evaluación | Invocación Síncrona Directa | Eventos del Dominio |
| :--- | :---: | :---: |
| **Desacoplamiento entre Módulos** | Bajo | **Alto** |
| **Extensibilidad de Reacciones** | Compleja | **Simple** |
| **Facilidad para Auditoría** | Media | **Excelente** |

## Decisión
Adoptar la comunicación basada en **Eventos del Dominio (Domain Events)** para la interacción inter-modular desacoplada.

## Justificación
Permite a los módulos publicar cambios de estado del negocio y reaccionar de forma autónoma sin acoplar la ejecución.

## Consecuencias
- **Positivas**: Modulos desacoplados, extensible, compatible con auditoría inalterable.
- **Negativas**: Necesidad de modelar formalmente los eventos del dominio en la subfase 6.8.

## Riesgos
- Publicación de eventos con granularidad inadecuada.

## Mitigaciones
- Especificar eventos del dominio puramente semánticos en la Subfase 6.8.

## Impacto sobre Documentos Existentes
- Fundamenta la Arquitectura de Eventos (6.8).
