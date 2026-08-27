# ADR-0010: Adopción Oficial de la Especificación de Restricciones de Arquitectura Tecnológicamente Neutra (Revision 2.0)

## Estado
**Aprobado por el Architecture Review Board (ARB)**

## Fecha
2026-07-25 (Revisión 2.0)

## Contexto & Problema
Atendiendo a la decisión `APPROVED WITH CONDITIONS` emitida por el **Architecture Review Board (ARB)**, se requería eliminar toda mención a decisiones de implementación, tecnologías, proveedores, frameworks o mecanismos específicos introducidos en la versión anterior de la Subfase 3.3, transformando todas las restricciones en declaraciones **100% neutras tecnológicamente** que definan exclusivamente qué límites debe respetar la arquitectura.

## Opciones Consideradas
1. **Conservar Nombres Propietarios y Mecanismos de Persistencia/Despliegue**: Incluir nombres de proveedores, lenguajes o tecnologías específicas en la especificación de restricciones. *(Rechazado por el ARB: Viola la neutralidad de la arquitectura empresarial)*.
2. **Especificación de Restricciones 100% Neutra Tecnológicamente (Revision 2.0)**: Redactar las restricciones en términos puros de fronteras de negocio, aislamiento organizacional, resiliencia y gobernanza, registrando todas las decisiones del *cómo* en las Entradas ADI mapeadas a las Subfases 3.4 a 3.8. *(Seleccionado)*.

## Decisión Seleccionada
Adoptar y ratificar la Especificación Oficial de Restricciones de Arquitectura (Revisión 2.0) en el documento `03_ARCHITECTURAL_CONSTRAINTS.md`:
- **CONST-01**: Restricción de Alcance de Activos (Monitoreo exclusivo sobre activos registrados y autorizados).
- **CONST-02**: Restricción de Entorno Distribuido Heterogéneo (Independencia del código respecto a nodos persistentes o edge).
- **CONST-03**: Restricción de Aislamiento Organizacional de Datos (Contexto discriminador inmutable obligatorio).
- **CONST-04**: Restricción de Observación No Disruptiva ni Degradante (Consumo de recursos insignificante sin afectar producción).
- **CONST-05**: Restricción de Traza de Auditoría Inmutable y No Repudiable (Registros append-only sin modificación o borrado).
- **Registro ADI Mapeado al Roadmap**: Mapeo estricto de las Entradas `ADI-ARCH-01` a `ADI-ARCH-04` hacia las Subfases 3.4 (Lógica), 3.7 (Persistencia) y 3.8 (Despliegue e Integración).

## Consecuencias
### Positivas:
- Neutralidad tecnológica absoluta en la capa de Arquitectura Empresarial.
- Cumplimiento 100% con los requerimientos mandatorios del ARB.
- Hoja de ruta limpia y estructurada para abordar inmediatamente la **Subfase 3.4 Logical Architecture**.

### Negativas / Compromisos (Trade-offs):
- Ninguno.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Neutralidad Tecnológica?: Sí (100%)
- ¿Respeta Aislamiento de Fases?: Sí (100%)
- ¿Respeta las Directivas del ARB?: Sí (100%)
