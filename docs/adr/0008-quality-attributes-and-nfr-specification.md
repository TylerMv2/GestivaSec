# ADR-0008: Adopción de la Especificación Oficial de Atributos de Calidad y Requisitos No Funcionales (NFRs)

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
Al dar inicio a la Fase 3 (Enterprise Architecture), se requería formalizar la especificación inmutable de Atributos de Calidad y Requisitos No Funcionales (NFRs) que actuarán como restricciones de diseño obligatorias para todas las decisiones futuras de arquitectura, topología, seguridad y despliegue de GestivaSec V1.

## Opciones Consideradas
1. **Requisitos No Funcionales Implícitos o Generales**: Asumir expectativas de rendimiento y disponibilidad sin escenarios de calidad medibles ni restricciones formales. *(Rechazado: Alta probabilidad de derivas arquitectónicas y fallos en producción)*.
2. **Especificación Formal basada en Marcos SEI / TOGAF**: Definir formalmente un catálogo NFR con métricas de disponibilidad (99.99%), tiempo de detección (MTTD < 60s), aislamiento estricto Multi-Tenant, auditoría inmutable append-only y análisis de trade-offs. *(Seleccionado)*.

## Decisión Seleccionada
Aprobar y ratificar el documento de especificación de la subfase 3.1 (`01_QUALITY_ATTRIBUTES_AND_NFRS.md`), estableciendo los siguientes NFRs innegociables:
- **NFR-AVA-01**: Disponibilidad Uptime ≥ 99.99% para el núcleo de sondas sintéticas.
- **NFR-PER-01**: Tiempo medio de detección de indisponibilidad (MTTD) < 60 segundos.
- **NFR-SEC-01**: Aislamiento Multi-Tenant inquebrantable a nivel de almacenamiento y acceso.
- **NFR-AUD-01**: Inmutabilidad de registros de auditoría append-only sin permisos de modificación ni eliminación.

## Consecuencias
### Positivas:
- Base de restricciones arquitectónicas clara y medible para todas las fases subsiguientes (Topologías, Seguridad, Persistencia, Deployment).
- Trazabilidad 100% garantizada entre los hallazgos de las Fases 1/2 y los requisitos de calidad de la Fase 3.
- Cero ambiguidades sobre las prioridades y compromisos (*Trade-offs*) del sistema.

### Negativas / Compromisos (Trade-offs):
- Se acepta un overhead razonable de latencia (~10-15ms por consulta) a cambio de garantizar el filtrado RLS Multi-Tenant y la traducción ACL en cada petición.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Security by Design?: Sí
- ¿Respeta Audit by Design?: Sí
