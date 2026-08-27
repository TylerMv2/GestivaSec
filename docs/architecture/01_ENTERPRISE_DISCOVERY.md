# ENTERPRISE DISCOVERY & SCOPE — GESTIVASEC V1
> **Estado**: Especificación Oficial de Descubrimiento de Negocio  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fase Afectada**: Fase 1.1 Enterprise Discovery  
> **Fecha**: 2026-07-25  

---

## 1. Propósito & Alcance Empresarial

**GestivaSec V1** es la plataforma privada de alcance corporativo proyectada para convertirse en el **Centro Oficial de Operaciones Tecnológicas (SOC/NOC)** del ecosistema **Gestiva**.

Su misión fundamental no es presentar datos estáticos en pantallas, sino orquestar la observabilidad integral, la auditoría continua, el monitoreo sintético y la gestión reactiva/proactiva de la seguridad sobre infraestructuras heterogéneas (Cloud, Multi-Cloud, Edge y On-Premise).

---

## 2. Mapa de Capacidades Requeridas del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ PLATAFORMA GESTIVASEC V1 (SOC / NOC UNIFICADO)                                           │
├──────────────────────────────┬─────────────────────────────┬────────────────────────────┤
│ 1. OBSERVABILIDAD & TELEMETRÍA│ 2. INVENTARIO & ACTIVOS     │ 3. POSTURA DE SEGURIDAD    │
│    • Sondas Sintéticas       │    • Asset Discovery        │    • Vulnerabilidades OWASP│
│    • Ingesta de Logs/Métricas│    • Topología Lógica/Física│    • Matriz MITRE ATT&CK   │
├──────────────────────────────┼─────────────────────────────┼────────────────────────────┤
│ 4. GESTIÓN DE INCIDENTES     │ 5. GOBIERNO & CUMPLIMIENTO  │ 6. DEVSECOPS & PIPELINES   │
│    • Ciclo de Vida P1 - P4   │    • ISO 27001 / NIST CSF   │    • Observabilidad CI/CD  │
│    • RCA & Trazabilidad SLA  │    • Auditoría Inmutable RLS│    • Dependabot & Alerts   │
└──────────────────────────────┴─────────────────────────────┴────────────────────────────┘
```

---

## 3. Requisitos No Funcionales (NFR) & Restricciones Arquitectónicas Primarias

### 3.1 Disponibilidad & Rendimiento
- **Disponibilidad SLA**: Target de **99.99%** de tiempo de actividad operacional para componentes de recolección y alerta.
- **Resiliencia & Failover**: El sistema debe tolerar la pérdida temporal de conectividad WAN mediante almacenamiento local resiliente y resincronización eventual.

### 3.2 Preparación para Eventos, Mensajería y CQRS (Capacidad sin Adopción Prematura)
Conforme a la **Directiva de Arquitectura**, la plataforma debe ser diseñada con compatibilidad nativa para:
- **Event-Driven Architecture (EDA)**: Publicación y suscripción desacoplada de eventos de dominio (`DomainEvent`).
- **Mensajería Asíncrona**: Canalización distribuida de mensajes telemétricos.
- **CQRS (Command Query Responsibility Segregation)**: Separación estricta de modelos de comandos de escritura frente a vistas analíticas de lectura.
- **Procesamiento Asíncrono (Async Processing)**: Ejecución diferida de tareas de sondeo sintético y análisis heurístico.

> ⚠️ **RESTRICCIÓN DE DISCOVERY**: Ninguna tecnología específica de mensajería (Kafka, RabbitMQ, NATS, Redis Streams, SQS) será adoptada ni integrada en el código/infraestructura hasta que la fase de **Domain Discovery (Descubrimiento del Dominio)** concluya en su totalidad.
