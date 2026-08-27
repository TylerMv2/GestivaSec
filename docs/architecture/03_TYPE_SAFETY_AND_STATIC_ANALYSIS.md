# MAXIMUM TYPE SAFETY & STATIC ANALYSIS — GESTIVASEC V1
> **Estado**: Especificación Oficial de Arquitectura  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fase Afectada**: Fase 1 (Arquitectura) & Fase 6/7 (Backend/Frontend)  
> **Fecha**: 2026-07-25  

---

## 1. Directiva Maestra de Seguridad de Tipos & Análisis Estático

Todo lenguaje de programación, motor de plantillas, esquema de base de datos o script de infraestructura utilizado en **GestivaSec V1** **deberá configurarse y utilizarse bajo su máximo nivel razonable de seguridad de tipos (Type Safety) y análisis estático de código (SAST & AST Analysis)**.

---

## 2. Requisitos por Lenguaje / Dominio Tecnológico

### 2.1 TypeScript (Frontend / Node.js)
- **Modo Estricto Máximo**: Archivo `tsconfig.json` configurado con:
  - `"strict": true`
  - `"noImplicitAny": true`
  - `"strictNullChecks": true`
  - `"noUncheckedIndexedAccess": true`
  - `"exactOptionalPropertyTypes": true`
- **Prohibición de Cargas Sueltas**: Prohibido el uso del tipo `any`, aserciones de tipo inseguras `as any` o ignorar comprobaciones con `@ts-ignore` (salvo excepción justificada por ADR).

### 2.2 Python (Backend / Sondas)
- **Comprobación de Tipos Estática Obligatoria**: Uso de `mypy --strict` en el 100% del código fuente. Todo argumento y valor de retorno de función debe poseer Type Hints explícitos.
- **Análisis Estático (SAST)**: Integración obligatoria de `ruff` (linter hiper-rápido) y `bandit` para análisis de seguridad del AST.

### 2.3 Rust / Go / C++ (Componentes de Alto Rendimiento)
- **Rust**: Prohibición de bloques `unsafe` sin aprobación expresa del Comité de Arquitectura; `clippy --deny warnings`.
- **Go**: `golangci-lint` con linters estrictos habilitados (`errcheck`, `gosec`, `staticcheck`).

### 2.4 SQL & Schemas de Base de Datos
- Análisis estático de esquemas mediante linters como `sqlfluff` y validadores estrictos de tipos en columnas (`NOT NULL` por defecto, enums fuertemente tipados o dominios).

---

## 3. Integración en el Pipeline CI/CD

El pipeline de integración continua rechazará automáticamente cualquier Pull Request que contenga advertencias o fallos de tipos en los linters y analizadores estáticos.
