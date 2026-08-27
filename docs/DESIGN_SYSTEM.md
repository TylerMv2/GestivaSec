# GESTIVA SECURITY (GESTIVASEC V1) — ENTERPRISE SOC DESIGN SYSTEM

---

## 1. FUNDAMENTOS VISUALES (FOUNDATION & TOKENS)

### 1.1 Palette de Colores Dark-First (Color Tokens)
- **Background Root (`--bg-root`)**: `#0B0F17` (Oscuro profundo tipo CrowdStrike / Datadog)
- **Background Surface (`--bg-surface`)**: `#111827` (Tarjetas y Paneles SOC)
- **Background Elevated (`--bg-elevated`)**: `#1F2937` (Dropdowns, Modales, Tooltips)
- **Border Subtle (`--border-subtle`)**: `rgba(255, 255, 255, 0.08)`
- **Border Active (`--border-active`)**: `rgba(59, 130, 246, 0.4)`

### 1.2 Severidad y Estados Operativos
- **Critical Severity (`--critical`)**: `#EF4444` (Red 500)
- **High Severity (`--high`)**: `#F97316` (Orange 500)
- **Warning / Medium (`--warning`)**: `#F59E0B` (Amber 500)
- **Healthy / Info (`--healthy`)**: `#10B981` (Emerald 500)
- **Primary Accent (`--accent-primary`)**: `#3B82F6` (Blue 500)

### 1.3 Tipografía (Typography)
- **Font Family**: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif.
- **Monospace Font (Code & Hash)**: "JetBrains Mono", Fira Code, monospace.
- **Scale**:
  - `Display / KPI`: 32px / Bold / Line Height 1.2
  - `Title H1`: 24px / SemiBold / Line Height 1.3
  - `Header H2`: 18px / Medium / Line Height 1.4
  - `Body Standard`: 14px / Regular / Line Height 1.5
  - `Caption / Monospace`: 12px / Medium / Line Height 1.4

---

## 2. ESPECIFICACIÓN DE COMPONENTES UI (COMPONENT MATRIX)

### 2.1 Metric Card (Tarjeta KPI de Salud y Amenazas)
- **Estructura**: Header con Label + Icono, Valor Display gigante, Badge de Severidad, Borde de estado sutil.
- **Micro-interacción**: Hover con elevación sutil (`transform: translateY(-2px)`) y resplandor de borde.

### 2.2 SOC DataGrid & Data Tables
- **Encabezado**: Fondo `#1F2937`, texto en mayúsculas pequeñas, alineación estricta.
- **Filas**: Intercalado sutil, celda de estado con indicador luminoso (*Status Pill*).
- **Acciones**: Botón de acción primaria (ej: `⚡ Sondear Ahora`) alineado a la derecha.

### 2.3 Status Pills & Risk Badges
- **Formato**: Fondo con opacidad 15%, texto en color sólido, icono integrado.
- **Estilos**:
  - `P1_CRITICAL`: Fondo `rgba(239, 68, 68, 0.15)`, Texto `#EF4444`.
  - `P2_HIGH`: Fondo `rgba(249, 115, 22, 0.15)`, Texto `#F97316`.
  - `P3_MEDIUM`: Fondo `rgba(245, 158, 11, 0.15)`, Texto `#F59E0B`.
  - `HEALTHY`: Fondo `rgba(16, 185, 129, 0.15)`, Texto `#10B981`.

---

## 3. EFECTOS GLASSMORPHISM Y MOVIMIENTO (MOTION & ELEVATION)

### 3.1 Transiciones Estándar
- `duration-fast`: `150ms ease-in-out` (Hover de botones y celdas).
- `duration-normal`: `250ms cubic-bezier(0.4, 0, 0.2, 1)` (Apertura de modales y drawers).

### 3.2 Glassmorphic Overlay
- `backdrop-filter: blur(12px)`
- `background: rgba(17, 24, 39, 0.75)`
- `border: 1px solid rgba(255, 255, 255, 0.1)`

---

## 4. RESPONSIVIDAD Y NAVEGACIÓN TECLADO (ACCESSIBILITY & RESPONSIVE)

- **Breakpoints**:
  - `Mobile`: `< 768px` (Sidebar colapsable a hamburguesa).
  - `Tablet`: `768px - 1024px` (Grid a 2 columnas).
  - `Desktop`: `> 1024px` (Grid completo a 4 columnas).
- **Navegación por Teclado**:
  - `Esc`: Cierra modales y paneles secundarios.
  - `Tab`: Focus ring visible en color `--accent-primary` con offset de 2px.
