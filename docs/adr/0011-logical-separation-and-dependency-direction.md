# ADR-0011: Especificación de Separación Lógica y Dirección de Dependencias de Arquitectura (Revision 3.1)

## Estado
**Aprobado por el Architecture Review Board (ARB)**

## Fecha
2026-07-25 (Revisión 3.1)

## Contexto & Problema
Atendiendo al aviso final de corrección emitido por el **Architecture Review Board (ARB)** sobre la Subfase 3.4 (Logical Architecture), se requería eliminar cualquier término de estructura o terminología de arquitectura e implementación (tales como capas, adaptadores, núcleo, contratos, componentes o repositorios) tanto del contenido como del nombre del archivo del ADR, garantizando una neutralidad **100% de tecnología, patrones, estilos e implementación**.

## Opciones Consideradas
1. **Mantener Nombres de Archivo o Términos Estructurales de Arquitectura**: Utilizar palabras como "clean", "hexagonal", "capas", "adaptadores" o "interfaces" en los títulos o nombres de archivo. *(Rechazado por el ARB)*.
2. **Especificación de Separación Lógica y Dirección de Dependencias Neutra (Revision 3.1)**: Asignar un nombre de archivo y un título completamente neutros (`0011-logical-separation-and-dependency-direction.md`) y definir formalmente la separación lógica de responsabilidades, la dirección inalterable de dependencias y las fronteras de información e interacción, difiriendo cualquier decisión técnica al Registro ADI mapeado a las Subfases 3.5 a 3.8 del Roadmap. *(Seleccionado)*.

## Decisión Seleccionada
Adoptar y ratificar la Especificación Oficial de Separación Lógica (Revisión 3.1) en el documento `04_LOGICAL_ARCHITECTURE.md`:
- **Dirección Lógica de Dependencias**: Las dependencias entre responsabilidades lógicas apuntan determinísticamente hacia las reglas fundamentales del negocio.
- **Fronteras Lógicas de Información e Interacción**: Autoridad exclusiva sobre la información y comunicación abstracta entre responsabilidades.
- **Registro ADI Mapeado al Roadmap Oficial**: Mapeo de las Entradas `ADI-LOG-01` a `ADI-LOG-04` hacia las Subfases 3.5, 3.6, 3.7 y 3.8.

## Consecuencias
### Positivas:
- Neutralidad tecnológica, de patrones, terminología e implementación del 100%.
- Cumplimiento 100% con los mandatos de la Revisión 3.1 del ARB.
- Consistencia total entre el título del documento, el título del ADR y el nombre del archivo del ADR.

### Negativas / Compromisos (Trade-offs):
- Ninguno.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Neutralidad Termonológica y Estructural?: Sí (100%)
- ¿Respeta Consistencia de ADR y Archivos?: Sí (100%)
- ¿Respeta las Directivas del ARB?: Sí (100%)
