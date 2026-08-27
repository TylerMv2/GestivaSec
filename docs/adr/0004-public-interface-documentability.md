# ADR-0004: Obligatoriedad de Documentabilidad en Interfaces Públicas con Selección de Mecanismo Diferida

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
En plataformas SOC/NOC empresariales, las APIs e interfaces expuestas son consumidas por agentes de monitoreo, integraciones CI/CD, webhooks y tableros operativos. Si las interfaces públicas carecen de especificación rigurosa o su documentación queda obsoleta, se generan fallos de integración y vulnerabilidades de seguridad.

## Opciones Consideradas
1. **Documentación manual posterior**: Redactar documentación estática en archivos externos tras implementar las APIs. *(Rechazado: Alta probabilidad de desincronización y deuda técnica)*.
2. **Forzar una herramienta específica en Fase 1**: Adoptar prematuramente una versión exacta de OpenAPI/Swagger o gRPC sin conocer el modelo de comunicación de la Fase 5. *(Rechazado: Viola la directiva de diferir la herramienta hasta la Fase de APIs)*.
3. **Regla de Documentabilidad Obligatoria por Diseño**: Exigir que todo contrato de interfaz pública sea documentable por naturaleza, posponiendo la selección exacta de la herramienta generadora hasta la **Fase 5: APIs**. *(Seleccionado)*.

## Decisión Seleccionada
Ratificar el principio de que **toda interfaz pública de GestivaSec V1 debe ser documentable**, reservando la selección formal del estándar y herramienta de documentación (OpenAPI, AsyncAPI, etc.) para la **Fase 5: APIs**.

## Consecuencias
### Positivas:
- Integraciones transparentes, previsibles y seguras.
- Cero tolerancia a endpoints ocultos o contratos indocumentados.
- Flexibilidad para elegir la mejor herramienta generadora en la Fase 5.

### Negativas / Compromisos (Trade-offs):
- Los desarrolladores deben incluir metadatos de tipos y descripciones de parámetros en los tipos del dominio/aplicación.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Audit/Security by Design?: Sí
- ¿Respeta YAGNI / KISS?: Sí
