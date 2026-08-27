# RISK FRAMEWORK & THREAT MODELING — GESTIVASEC V1
> **Estado**: Marco Oficial de Gestión de Riesgos & Amenazas  
> **Comité**: Comité Permanente de Arquitectura de GestivaSec V1  
> **Fecha**: 2026-07-25  

---

## 1. Integración con Modelado de Amenazas STRIDE

Todo diseño de componente, API o topología de red en GestivaSec V1 debe evaluarse activamente contra el modelo **STRIDE**:

| Amenaza | Propiedad de Ciberseguridad Comprometida |
| :--- | :--- |
| **Spoofing (Suplantación)** | Autenticación (`Authenticity`) |
| **Tampering (Manipulación)** | Integridad (`Integrity`) |
| **Repudiation (Repudio)** | No Repudio / Auditoría (`Non-repudiation`) |
| **Information Disclosure (Fuga de Información)** | Confidencialidad (`Confidentiality`) |
| **Denial of Service (Denegación de Servicio)** | Disponibilidad (`Availability`) |
| **Elevation of Privilege (Elevación de Privilegios)** | Autorización (`Authorization`) |

---

## 2. Umbral de Tolerancia al Riesgo (Risk Appetite)

- **Cero Tolerancia (Zero Risk Appetite)**: Para vulnerabilidades de Elevación de Privilegios (EoP), Fuga de Datos sensibles sin cifrar y By-pass de Row Level Security (RLS).
- **Tolerancia Controlada**: Para problemas de degradación cosmética de interfaz o latencias mínimas no operativas.
