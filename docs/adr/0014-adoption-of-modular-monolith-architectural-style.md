# ADR-0014: Adopción del Estilo Arquitectónico Monolito Modular (Modular Monolith)

## Estado
**Aceptado**

## Contexto
Para GestivaSec V1 se requiere seleccionar el estilo principal de arquitectura de software que soporte los Requisitos Funcionales, Atributos de Calidad y las restricciones de modularidad e independencia tecnológica (`CONST-04`).

## Problema
Se debe elegir un estilo arquitectónico que garantice una alta cohesión entre componentes relacionados y un bajo acoplamiento operacional, sin incurrir en la complejidad ni sobrecostos de red de una arquitectura distribuida prematura.

## Alternativas Consideradas

### Alternativa 1: Monolito Tradicional Monolítico
- Descripción: Ejecutable único sin separación estricta de módulos.
- Ventajas: Despliegue simple.
- Desventajas: Alto acoplamiento, degradación del mantenimiento, riesgo de acoplamiento cruzado de datos.

### Alternativa 2: Microservicios Granulares Distribuidos
- Descripción: Separación física de cada módulo funcional en un servicio de red independiente.
- Ventajas: Escalabilidad independiente.
- Desventajas: Complejidad operativa extrema, latencia de red, dificultad en el control transaccional de auditoría.

### Alternativa 3: Monolito Modular (Modular Monolith)
- Descripción: Despliegue unificado con fronteras modulares estrictas, aislamiento de código e interfaces formales.
- Ventajas: Alta cohesión, cero latencia de red inter-modular, simplicidad operativa, transición futura transparente.
- Desventajas: Exige enforzar reglas de dependencia estrictas para evitar el acoplamiento directo.

### Matriz Comparativa

| Criterio de Evaluación | Monolito Tradicional | Microservicios | Monolito Modular |
| :--- | :---: | :---: | :---: |
| **Simplicidad de Despliegue** | Alta | Baja | **Alta** |
| **Aisleamiento de Módulos** | Bajo | Alto | **Alto** |
| **Rendimiento e Intercomunicación**| Alto | Bajo (Latencia Red) | **Alto** |
| **Complejidad Operativa** | Baja | Muy Alta | **Baja** |

## Decisión
Adoptar el estilo **Monolito Modular (Modular Monolith)** como la arquitectura base de software para GestivaSec V1.

## Justificación
Ofrece el mejor balance para GestivaSec V1, garantizando aislamiento estricto por módulo sin la sobrecarga ni complejidad de microservicios distribuidos.

## Consecuencias
- **Positivas**: Simplicidad operativa, altísima cohesión, aislamiento de módulos.
- **Negativas**: Exige enforzar reglas de dependencia estrictas para evitar acoplamiento.

## Riesgos
- Riesgo de erosión modular si los desarrolladores importan clases internas entre módulos.

## Mitigaciones
- Establecer matrices de dependencia de código y verificaciones de fronteras modulares en CI/CD.

## Impacto sobre Documentos Existentes
- Fundamenta la Subfase 6.1 (Architecture Style) y los documentos modulares posteriores.
