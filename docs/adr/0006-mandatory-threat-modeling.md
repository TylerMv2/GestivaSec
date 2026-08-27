# ADR-0006: Adopción del Modelado de Amenazas Obligatorio (STRIDE) para Todo Componente y Flujo de Datos

## Estado
**Aprobado**

## Fecha
2026-07-25

## Contexto & Problema
Las plataformas de seguridad y observabilidad (SOC/NOC) son objetivos prioritarios de ciberataques. Descubrir fallos de diseño de seguridad (by-pass de RLS, suplantación de sondas, manipulación de logs) en fases tardías de código o producción genera costos prohibitivos e impactos graves a la reputación y confianza.

## Opciones Consideradas
1. **Revisiones de Seguridad Ad-Hoc / Pentesting posterior**: Evaluar la seguridad únicamente al finalizar el desarrollo del frontend/backend. *(Rechazado: Incumple el principio de Security by Design)*.
2. **Modelado de Amenazas STRIDE Obligatorio Previo al Diseño**: Exigir un archivo `THREAT_MODEL.md` con DFD y matriz de mitigaciones para cada módulo antes de escribir código. *(Seleccionado)*.

## Decisión Seleccionada
Hacer obligatorio el **Modelado de Amenazas (Threat Modeling)** basado en **STRIDE** y diagramas DFD en Mermaid.js con desgloses de límites de confianza para todo módulo, API o arquitectura de GestivaSec V1.

## Consecuencias
### Positivas:
- Identificación y neutralización de vectores de ataque desde la fase de diseño conceptual.
- Documentación clara de fronteras de confianza y controles de seguridad exigidos.
- Cumplimiento estricto del principio de Security by Design.

### Negativas / Compromisos (Trade-offs):
- Se añade un paso formal de modelado antes de validar arquitecturas o APIs.

## Matriz de Cumplimiento con los Principios de Ingeniería
- ¿Respeta Clean Architecture?: Sí
- ¿Respeta Security by Design?: Sí
- ¿Respeta Audit by Design?: Sí
