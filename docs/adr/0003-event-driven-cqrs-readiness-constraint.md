# ADR-0003: Restricción de Preparación para Eventos, Mensajería y CQRS sin Selección de Tecnologías Prematuras

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
La arquitectura de GestivaSec V1 requerirá procesar volúmenes continuos de telemetría, eventos de seguridad y sondeos asíncronos en tiempo real mediante patrones de mensajería, eventos y CQRS. Sin embargo, seleccionar o acoplar tempranamente un motor específico (ej. RabbitMQ, Kafka, Redis, NATS) antes de comprender el modelado exacto del dominio (Domain Discovery) arriesga sobre-ingeniería y acoplamiento prematuro.

## Opciones Consideradas
1. **Seleccionar un Message Broker desde la Fase 1**: Elegir Kafka o RabbitMQ inmediatamente. *(Rechazado: Incumple las reglas del Master Directive y fuerza decisiones de infraestructura sin entender el dominio)*.
2. **Ignorar Eventos y CQRS hasta la Fase de Backend**: Diseñar una arquitectura monolítica síncrona simple. *(Rechazado: No cumpliría con el requisito no funcional de procesar eventos asíncronos y CQRS)*.
3. **Diseño de Preparación Arquitectónica (Readiness) Abstraída**: Diseñar las interfaces del sistema para soportar Eventos, Mensajería, CQRS y Procesamiento Asíncrono a nivel de contratos de software, posponiendo la selección e implementación de la tecnología concreta hasta finalizar el Domain Discovery. *(Seleccionado)*.

## Decisión Seleccionada
Garantizar que los contratos y límites de la arquitectura soporten operaciones asíncronas, eventos y CQRS, pero congelar la elección del proveedor o broker tecnológico específico hasta concluir la fase de **Domain Discovery**.

## Consecuencias
### Positivas:
- Cero acoplamiento prematuro a brokers o middleware específico.
- Dominio limpio e independiente de la infraestructura subyacente.
- Flexibilidad para seleccionar la tecnología óptima una vez conocidos los volúmenes y patrones de eventos del negocio.

### Negativas / Compromisos (Trade-offs):
- Se deben definir abstracciones e interfaces neutras para la emisión de eventos y comandos.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta YAGNI / KISS?: Sí
- ¿Respeta Security by Design?: Sí
