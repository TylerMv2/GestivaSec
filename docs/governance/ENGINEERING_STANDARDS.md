# ENGINEERING STANDARDS — GESTIVASEC V1
> **Estado**: Estándar Oficial de Ingeniería  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Propósito & Alcance
Este documento establece las normas técnicas universales de código, manejo de errores, inmutabilidad, tipado estricto y testing que deberán cumplir todos los lenguajes y módulos implementados en **GestivaSec V1**.

---

## 2. Normas de Calidad de Código (Clean Code)

### 2.1 Tipado Estricto & Cero Ambigüedad
- **Prohibición de Tipos Implícitos / Dynamic Typing Suelto**: Todo código fuente (TypeScript, Python, Go, Rust, SQL) debe implementar comprobación de tipos estricta (`strict: true`, type hints obligatorios, no `any`, no `interface{}`).
- **Inmutabilidad por Defecto**: Las variables, constantes y estructuras de datos deben declararse inmutables por defecto (`const`, `readonly`, `dataclass(frozen=True)`).

### 2.2 Principios Funcionales & Pura Lógica de Dominio
- **Funciones Puras**: La lógica dentro del dominio debe ser declarativa, determinista y libre de efectos secundarios (*side-effects*).
- **Manejo Explícito de Errores**: Prohibido silenciar excepciones con `try/catch` vacíos, retornos `null` silenciosos o respuestas con arreglos vacíos `[]` ante fallos de red.
- **Tipos de Resultado (Result Types / Either)**: Preferir retornos explícitos del tipo `Result<T, Error>` sobre el lanzamiento desenfrenado de excepciones no controladas.

---

## 3. Estándares de Prueba & Cobertura (Testing)

### 3.1 Pirámide de Pruebas Obligatoria
1. **Pruebas Unitarias (70%)**: Cobertura del 100% de las reglas de dominio puro sin dependencias de I/O ni bases de datos.
2. **Pruebas de Integración (20%)**: Verificación de conectores, repositorios y adaptadores de infraestructura contra instancias en contenedor/mock.
3. **Pruebas E2E / Contrato (10%)**: Validación de contratos API REST/gRPC y flujos de usuario críticos.

---

## 4. Convenciones de Nomenclatura Estándar

- **Archivos y Directorios**: `kebab-case` (ejemplo: `asset-repository.ts`, `domain-event-bus.py`).
- **Clases e Interfaces**: `PascalCase` (ejemplo: `AssetEntity`, `TelemetryService`).
- **Funciones y Métodos**: `camelCase` (ejemplo: `calculateSlaAvailability()`, `processSecurityFinding()`).
- **Constantes de Entorno / Enums**: `UPPER_SNAKE_CASE` (ejemplo: `MAX_SOCKET_TIMEOUT_MS`, `CRITICALITY_HIGH`).
