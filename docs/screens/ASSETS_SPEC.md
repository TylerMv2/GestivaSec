# DIGITAL ASSETS INVENTORY SPECIFICATION (ASSETS_SPEC.md)

---

## 1. OBJETIVO DE LA PANTALLA
Gestionar el inventario vivo de activos digitales de la organización en **GestivaSec V1**. Garantizar el cumplimiento estricto de las reglas **`BR-0002` (Owner Email Obligatorio)** y **`BR-0004` (Frontera Multi-Tenant)**.

---

## 2. USUARIO OBJETIVO
- **SOC Analyst / Operator**: Registro de dominios y endpoints corporativos.
- **Admin**: Supervisión de asignación de propietarios y criticidad (P1 a P4).

---

## 3. WIREFRAME TEXTUAL ASCII COMPLETO

```
+---------------------------------------------------------------------------------------------------------+
| [NAV] Dashboard | Assets* | Passive Discovery | Threat Intel | Alerts | Incident Center | Audit Logs   |
+---------------------------------------------------------------------------------------------------------+
| BREADCRUMB: GestivaSec / Digital Asset Inventory                                                        |
+---------------------------------------------------------------------------------------------------------+
|                                                                                                         |
|  +---------------------------------------------------------------------------------------------------+  |
|  | DIGITAL ASSET INVENTORY (ORG: GestivaOne Corporation)                 [➕ Register New Asset]      |  |
|  +---------------------------------------------------------------------------------------------------+  |
|  | ASSET NAME                  | TARGET URL              | CRITICALITY | OWNER EMAIL (BR-02)  | ACTIONS  |  |
|  +-----------------------------+-------------------------+-------------+----------------------+---------+  |
|  | GestivaOne Core Web Portal  | https://gestivaone.com  | P1 CRITICAL | ops@gestivaone.com   | [Sondear]|  |
|  | GestivaOne E-Commerce Store | https://store.gestiva...| P2 HIGH     | devops@gestivaone.com| [Sondear]|  |
|  | Festa Event Platform        | https://festa.gestiva...| P2 HIGH     | festa@gestivaone.com | [Sondear]|  |
|  +---------------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 4. REGLAS INVIOLABLES DE NEGOCIO
- **`BR-0002`**: Todo activo digital nuevo debe tener el campo `owner_email` poblado con una dirección de correo electrónico válida.
- **`BR-0004`**: Todos los activos devueltos o creados pertenecen estrictamente a la organización del encabezado `X-Organization-ID`.
