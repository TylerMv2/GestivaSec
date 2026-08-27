# PUBLIC INTERFACE DOCUMENTABILITY — GESTIVASEC V1
> **Estado**: Especificación Oficial de Arquitectura  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fase Afectada**: Fase 1 (Arquitectura) & Fase 5 (APIs)  
> **Fecha**: 2026-07-25  

---

## 1. Directiva Maestra de Interfaz Pública

Toda interfaz expuesta por los módulos de **GestivaSec V1** (ya sean APIs HTTP/REST, endpoints gRPC, conexiones WebSocket, esquemas de eventos pub/sub o interfaces CLI) **debe ser 100% documentable de forma automatizada y autosostenible**.

---

## 2. Reglas de Documentabilidad por Diseño

1. **Cero Interfaces Indocumentadas**: Ningún endpoint o contrato de datos podrá desplegarse o considerarse listo sin su correspondiente especificación formal de interfaz.
2. **Especificación Declarativa**: La definición de contratos precederá o se derivará directamente de los tipos formales del código fuente (Self-Documenting Code).
3. **Selección Diferida del Mecanismo**: El mecanismo, formato y motor generador definitivo (ej. OpenAPI 3.1, AsyncAPI 3.0, Protobuf Schema, TypeSpec, Scalar, Redoc) **será seleccionado formalmente durante la Fase 5: APIs**.
