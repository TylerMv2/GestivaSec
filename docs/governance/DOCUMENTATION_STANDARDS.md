# DOCUMENTATION STANDARDS — GESTIVASEC V1
> **Estado**: Estándar Oficial de Documentación  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Reglas de Documentación Viva (Living Documentation)

1. **Markdown GitHub-Flavored (GFM)**: Toda la documentación arquitectónica debe redactarse en archivos `.md` formateados con encabezados semánticos, tablas explicativas y bloques de alerta.
2. **Diagramas Mermaid & C4**: Prohibido el uso de imágenes binarias estáticas (PNG/JPG) no editables para arquitectura. Todo diagrama de secuencia, flujo o topología debe definirse mediante código **Mermaid.js** declarativo dentro de Markdown.
3. **Contratos API**:
   - APIs REST: Especificación obligatoria **OpenAPI 3.1.0 (Swagger)** en formato YAML/JSON.
   - Eventos asíncronos: Especificación obligatoria **AsyncAPI 3.0.0**.

---

## 2. Encabezado Estándar en Todos los Documentos

Todo documento de ingeniería en GestivaSec V1 debe incluir en sus primeras líneas el bloque de metadatos oficial:

```markdown
# [TÍTULO EN MAYÚSCULAS] — GESTIVASEC V1
> **Estado**: [Borrador | En Revisión | Aprobado | Deprecado]  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fase Afectada**: [Fase X.Y]  
> **Fecha**: YYYY-MM-DD  
```
