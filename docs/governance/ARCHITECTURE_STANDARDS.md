# ARCHITECTURE STANDARDS — GESTIVASEC V1
> **Estado**: Estándar Oficial de Arquitectura  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Modelo de Referencia C4

Toda la representación arquitectónica de **GestivaSec V1** debe seguir estrictamente la especificación **C4 Model** (Context, Containers, Components, Code):

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ NIVEL 1: CONTEXTO DEL SISTEMA (System Context Diagram)                                  │
│ Actores del SOC/NOC, Ecosistema GestivaOne e Infraestructuras Objetivo Externas          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ NIVEL 2: CONTENEDORES (Container Diagram)                                               │
│ Aplicación Web Frontend, Gateway API, Sondas Sintéticas, Engine Event Bus, DB PostgreSQL │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ NIVEL 3: COMPONENTES (Component Diagram)                                                │
│ Módulos Hexagonales (AssetCenter, IncidentManager, ThreatCorrelation, RLSGuard)          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ NIVEL 4: CÓDIGO (Code Diagram / UML)                                                    │
│ Interfaces de Puertos, Adaptadores, Entidades Puras del Dominio                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Límites Hexagonales & Reglas de Acoplamiento

1. **Capa de Dominio (`/domain`)**:
   - **Regla de Oro**: Contiene ÚNICAMENTE código nativo y tipos de dominio. Cero importaciones de bibliotecas web, frameworks, bases de datos o clientes HTTP.
2. **Capa de Aplicación (`/application`)**:
   - Contiene la orquestación de casos de uso (`Use Cases`), servicios del dominio y el bus de eventos en memoria.
3. **Capa de Infraestructura (`/infrastructure`)**:
   - Implementa las interfaces de los puertos definidos en el dominio (clientes PostgreSQL, sockets de red, integraciones AWS/GitHub, IndexedDB).
4. **Capa de Presentación (`/presentation`)**:
   - Controladores API, vistas UI y componentes gráficos.

---

## 3. Patrón Event-Driven & CQRS Lite

- **Inmutabilidad de Eventos**: Los eventos de dominio (`DomainEvent`) son hechos pasados inmutables (`AssetCreated`, `IncidentEscalated`, `VulnerabilityDetected`).
- **Desacoplamiento Lectura/Escritura (CQRS Lite)**: Las consultas complejas de dashboards analíticos deben consumir Vistas Materializadas o read-models dedicados, evitando sobrecargar el motor transaccional de comandos.
