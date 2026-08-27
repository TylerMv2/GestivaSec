# ADR-0013: Adopción del Modelo de Arquitectura de Seguridad Zero-Trust, Zonas de Confianza y Análisis de Amenazas STRIDE

## Estado
**Aprobado por el Comité de Arquitectura**

## Fecha
2026-07-25

## Contexto & Problema
Tras la aprobación definitiva de las subfases de Arquitectura Empresarial previas (3.1 a 3.5), se requería formalizar la Arquitectura de Seguridad de GestivaSec V1 para garantizar la inmunidad ante vectores de ataque perimetrales e internos, el enforzamiento del aislamiento de datos por organización (`tenant_id`), la inmutabilidad no repudiable de trazas de auditoría y la protección criptográfica de la información telemétrica.

## Opciones Consideradas
1. **Modelo de Seguridad Perimetral Tradicional (Castle-and-Moat)**: Asumir confianza implícita para todo componente o red interna tras atravesar el cortafuegos exterior. *(Rechazado: Incumple PRIN-02 Zero Trust y expone el sistema a ataques de movimiento lateral)*.
2. **Modelo de Seguridad Zero-Trust en Profundidad (5 Zonas de Confianza & STRIDE)**: Imponer autenticación explícita continua, enforzamiento de RLS Multi-Tenant, cifrado extremo a extremo (TLS 1.3 / AES-256) y preservación de auditoría inmutable append-only. *(Seleccionado)*.

## Decisión Seleccionada
Adoptar y ratificar la Arquitectura de Seguridad especificada en el documento `06_SECURITY_ARCHITECTURE.md`:
- **5 Zonas de Confianza (*Trust Zones*)**: Desde la Zona Perimetral Pública hasta la Bóveda Inmutable de Auditoría.
- **Modelado de Amenazas STRIDE**: Estrategias de mitigación formales contra Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service y Elevation of Privilege.
- **Enforzamiento de Multi-Tenant Isolation**: Discriminador `tenant_id` obligatorio validado en el perímetro y aplicado en las políticas de almacenamiento.
- **Controles Criptográficos**: TLS 1.3 en tránsito y AES-256 en reposo (`NFR-SEC-02`).

## Consecuencias
### Positivas:
- Protección inquebrantable de la confidencialidad, integridad y disponibilidad del ecosistema Gestiva.
- Trazabilidad y soporte total para auditorías normativas ISO 27001 / NIST CSF.
- Mitigación del 100% de los riesgos de fuga o manipulación de datos telemétricos.

### Negativas / Compromisos (Trade-offs):
- Se acepta un leve costo computacional (~10-15ms por solicitud) atribuido a la convalidación de tokens y filtrado Multi-Tenant en cada frontera.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Security by Design (Zero Trust)?: Sí (100%)
- ¿Respeta Auditability (No Repudio)?: Sí (100%)
- ¿Respeta Restricciones Mandatorias (`CONST-03`, `CONST-05`)?: Sí (100%)
