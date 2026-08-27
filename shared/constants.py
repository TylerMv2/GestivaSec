"""
Gestiva Security (GestivaSec V1) — Shared Kernel Domain Constants & Enums
Strictly compliant with Ubiquitous Language (Subphase 5.0) and Business Rules (BR-01..BR-05).
"""
from enum import Enum

class AssetStatus(str, Enum):
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    DECOMMISSIONED = "DECOMMISSIONED"

class IncidentPriority(str, Enum):
    P1_CRITICAL = "P1_CRITICAL"
    P2_HIGH = "P2_HIGH"
    P3_MEDIUM = "P3_MEDIUM"
    P4_LOW = "P4_LOW"

class IncidentStatus(str, Enum):
    DECLARED = "DECLARED"
    ASSIGNED = "ASSIGNED"
    IN_DIAGNOSIS = "IN_DIAGNOSIS"
    REMEDIATED = "REMEDIATED"
    CLOSED_WITH_RCA = "CLOSED_WITH_RCA"

class CredentialStatus(str, Enum):
    VALID = "VALID"
    WARNING_EXPIRING_SOON = "WARNING_EXPIRING_SOON"
    CRITICAL_EXPIRING = "CRITICAL_EXPIRING"
    EXPIRED = "EXPIRED"
    RENEWED = "RENEWED"

class FindingStatus(str, Enum):
    DETECTED = "DETECTED"
    TRIAGED = "TRIAGED"
    IN_REMEDIATION = "IN_REMEDIATION"
    RESOLVED = "RESOLVED"
    RISK_ACCEPTED = "RISK_ACCEPTED"

class RaciRole(str, Enum):
    RESPONSIBLE = "RESPONSIBLE"   # Operations Lead
    ACCOUNTABLE = "ACCOUNTABLE"   # Technical Director / CISO
    CONSULTED = "CONSULTED"       # SOC / Security Specialist
    INFORMED = "INFORMED"         # Stakeholders

# Business Rules Invariant Constants
BR01_RCA_REQUIRED_FOR_P1_CLOSED = True
BR02_OWNER_REQUIRED_FOR_ASSET = True
BR03_FAILED_SYNTHETIC_THRESHOLD = 3  # 3 consecutive synthetic failures trigger automatic P1
BR04_TENANT_ISOLATION_REQUIRED = True
BR05_AUDIT_LOG_APPEND_ONLY = True
