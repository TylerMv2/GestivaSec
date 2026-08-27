# ADR-0007: Adopción del Modelo de Dominio DDD, Bounded Contexts, Agregados y Capa Anti-Corrupción

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
Tras finalizar el Enterprise Discovery (Fase 1), se requería formalizar la estructura del dominio de negocio para GestivaSec V1 bajo los principios de Domain-Driven Design (DDD). Era necesario evitar que los modelos de APIs externas (Vercel, Cloudflare, Supabase) o las preocupaciones de base de datos contaminen la lógica central de observabilidad (NOC), ciberseguridad (SOC), inventario y gestión de incidentes.

## Opciones Consideradas
1. **Modelado centrado en Tablas/CRUD**: Diseñar directamente esquemas relacionales y tablas SQL. *(Rechazado: Produce acoplamiento rígido, viola las directivas maestras y degrada la mantenibilidad)*.
2. **Modelo Anémico / Monolítico**: Crear clases de datos sin comportamiento ni invariantes claras. *(Rechazado: Incumple los principios de Clean Architecture y DDD)*.
3. **Modelo de Dominio Puro DDD con 7 Bounded Contexts, 5 Agregados y Capa Anti-Corrupción (ACL)**: Delimitar explícitamente fronteras conceptuales, aislar la lógica con invariantes estrictas en los agregados y traducir modelos externos mediante adaptadores ACL. *(Seleccionado)*.

## Decisión Seleccionada
Ratificar el modelo de dominio DDD consolidado en la Fase 2:
- **7 Bounded Contexts**: `BC-01` a `BC-07`.
- **5 Agregados de Dominio**: `AssetAggregate`, `SyntheticProbeAggregate`, `IncidentAggregate`, `SecurityFindingAggregate`, `AuditLogAggregate`.
- **8 Objetos de Valor**: `AssetId`, `TargetUrl`, `TenantId`, `LatencyMs`, `CertValidityWindow`, `Priority`, `SlaDeadline`, `OwaspCategory`.
- **5 Servicios de Dominio**: `SVC-01` a `SVC-05`.
- **Capa Anti-Corrupción (ACL)**: `ACL-01` y `ACL-02`.

## Consecuencias
### Positivas:
- Modelo de negocio robusto, mantenible, testeable al 100% y desacoplado de la infraestructura.
- Protección total de las invariantes de consistencia (ej. no cerrar incidentes P1 sin informe RCA).
- Preparación nativa para la arquitectura limpia Hexagonal en la Fase 3.

### Negativas / Compromisos (Trade-offs):
- Se requiere mayor número de mapeadores y traductores en la frontera del sistema para convertir tipos externos a Value Objects.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Domain-Driven Design?: Sí
- ¿Respeta Security by Design?: Sí
