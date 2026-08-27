# GESTIVA SECURITY (GESTIVASEC V1) — MANUAL DEL USUARIO ANALISTA SOC (RELEASE V0.1.0)

---

## 1. Inicio de Sesión y Autenticación
1. Acceda a la plataforma web en `http://localhost:8000`.
2. Haga clic en el botón **🔐 Login SOC** ubicado en la esquina superior derecha.
3. Ingrese su correo corporativo (`admin@gestivaone.com`) y su contraseña (`GestivaSec2026!`).
4. Al autenticarse, obtendrá un **Token JWT** seguro guardado en la sesión.

---

## 2. Gestión del Inventario de Activos Digitales
1. En el menú lateral izquierdo, seleccione **Activos Digitales**.
2. Para registrar un nuevo activo, presione **➕ Registrar Nuevo Activo**.
3. Diligencie el Nombre del Activo, la URL de Destino, la Criticidad (P1 a P4) y el **Correo del Propietario Asignado (Regla BR-02)**.
4. Haga clic en **Registrar Activo**. El activo aparecerá de inmediato en la tabla interactiva.

---

## 3. Ejecución de Observabilidad Sintética en Tiempo Real
1. En la tabla de activos, ubique el activo deseado y haga clic en **⚡ Sondear Ahora**.
2. El sistema ejecutará un sondeo HTTP en tiempo real, registrando la latencia en milisegundos y el código de respuesta HTTP.
3. Para consultar el historial de sondeos y evidencias telemétricas, acceda a la pestaña **Observabilidad Sintética** en la barra lateral.
4. **Regla Inviolable BR-03**: Si un activo acumula 3 fallas sintéticas consecutivas, el sistema emitirá automáticamente una **Alerta de Incidente Crítico P1**.
