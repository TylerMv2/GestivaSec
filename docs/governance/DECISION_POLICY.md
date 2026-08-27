# DECISION POLICY — GESTIVASEC V1
> **Estado**: Borrador Oficial de Gobernanza  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Política de Registro de Decisiones de Arquitectura (ADR)

Toda decisión relevante sobre la estructura del sistema, lenguajes, frameworks, proveedores cloud, bases de datos, protocolos de seguridad o patrones de diseño **debe quedar documentada explícitamente mediante un ADR (Architecture Decision Record)**.

Está estrictamente prohibido realizar cambios estructurales basados en decisiones implícitas, conversaciones verbales o suposiciones no documentadas.

---

## 2. Estructura Estándar de un ADR

Cada archivo ADR se guardará en `docs/adr/` nombrado según la convención `NNNN-titulo-en-kebab-case.md` y utilizará la siguiente plantilla:

```markdown
# ADR-NNNN: [Título Conciso de la Decisión]

## Estado
[Propuesto | Aprobado | Reemplazado | Rechazado]

## Fecha
YYYY-MM-DD

## Contexto & Problema
[Descripción del escenario técnico, requisito o problema que requiere una decisión]

## Opciones Consideradas
1. Opción A
2. Opción B
3. Opción C

## Decisión Seleccionada
[Opción elegida y justificación técnica fundada]

## Consecuencias
### Positivas:
- [Beneficio 1]
### Negativas / Compromisos (Trade-offs):
- [Riesgo o costo 1]

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí/No
- ¿Respeta Security by Design?: Sí/No
```

---

## 3. Criterios para Exigir un ADR
Se requiere redactar un ADR obligatoriamente ante cualquiera de las siguientes circunstancias:
- Selección de un framework, biblioteca principal o lenguaje de programación.
- Elección del motor de base de datos o estrategia de persistencia.
- Cambio o adición de una norma de seguridad o protocolo de autenticación.
- Reorganización de la estructura de directorios o módulos del proyecto.
- Adopción de un patrón de comunicación entre servicios (gRPC, REST, GraphQL, WebSockets).
