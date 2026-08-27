"""
Gestiva Security (GestivaSec V1) — Project Kernel Validation Engine
Multi-module architecture validation suite enforcing Kernel Invariants (INV-01 to INV-07).
"""
import os
import yaml
import pytest

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "project"))

# 1. STRUCTURAL VALIDATOR
def test_kernel_manifest_and_hierarchy():
    manifest_path = os.path.join(PROJECT_DIR, "PROJECT_MANIFEST.yaml")
    assert os.path.exists(manifest_path), "PROJECT_MANIFEST.yaml must exist as core authority"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "project" in data
    assert data["project"]["name"] == "Gestiva Security (GestivaSec V1)"
    assert "kernel" in data
    assert data["kernel"]["version"] == "1.0.0"

def test_seven_engines_existence():
    expected_engines = [
        "governance_engine",
        "policy_engine",
        "registry_engine",
        "knowledge_engine",
        "dependency_engine",
        "metrics_engine",
        "runtime_engine",
        "runtime_history_engine",
        "state_engine"
    ]
    for engine in expected_engines:
        engine_path = os.path.join(PROJECT_DIR, engine)
        assert os.path.exists(engine_path) and os.path.isdir(engine_path), f"Engine directory '{engine}' missing in project/"

# 2. REGISTRY VALIDATOR
def test_registries_integrity():
    registry_dir = os.path.join(PROJECT_DIR, "registry_engine")
    expected_registries = [
        "ARTIFACT_REGISTRY.yaml",
        "DOMAIN_REGISTRY.yaml",
        "CAPABILITY_REGISTRY.yaml",
        "SLICE_REGISTRY.yaml",
        "DECISION_REGISTRY.yaml",
        "ADR_REGISTRY.yaml",
        "RFC_REGISTRY.yaml",
        "RISK_REGISTRY.yaml",
        "TECHNICAL_DEBT_REGISTRY.yaml",
        "TEST_REGISTRY.yaml"
    ]
    for reg_file in expected_registries:
        reg_path = os.path.join(registry_dir, reg_file)
        assert os.path.exists(reg_path), f"Registry '{reg_file}' missing in project/registry_engine/"

# 3. TRACEABILITY & GOVERNANCE VALIDATOR
def test_governance_audit_log_and_migration_report():
    audit_log_path = os.path.join(PROJECT_DIR, "governance_engine", "GOVERNANCE_AUDIT_LOG.yaml")
    assert os.path.exists(audit_log_path), "GOVERNANCE_AUDIT_LOG.yaml missing in project/governance_engine/"
    
    with open(audit_log_path, "r", encoding="utf-8") as f:
        audit_data = yaml.safe_load(f)
    assert "governance_audit_log" in audit_data
    assert len(audit_data["governance_audit_log"]) >= 5

    migration_report_path = os.path.join(PROJECT_DIR, "MIGRATION_REPORT.yaml")
    assert os.path.exists(migration_report_path), "MIGRATION_REPORT.yaml missing in project/"
    
    with open(migration_report_path, "r", encoding="utf-8") as f:
        mig_data = yaml.safe_load(f)
    assert mig_data["metrics"]["moved_files"] == 23
    assert mig_data["metrics"]["validation_status"] == "PASS"

# 4. POLICY VALIDATOR
def test_technical_debt_categories():
    debt_path = os.path.join(PROJECT_DIR, "registry_engine", "TECHNICAL_DEBT_REGISTRY.yaml")
    with open(debt_path, "r", encoding="utf-8") as f:
        debt_data = yaml.safe_load(f)
    
    categories = debt_data["technical_debt"]
    expected_categories = [
        "architectural_debt",
        "documentation_debt",
        "security_debt",
        "performance_debt",
        "operational_debt",
        "ux_debt",
        "ui_debt",
        "dependency_debt",
        "deprecation_debt"
    ]
    for cat in expected_categories:
        assert cat in categories, f"Technical debt category '{cat}' missing"

# 5. SECURITY & CLEANLINESS VALIDATOR
def test_no_loose_specifications_in_root():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    root_files = os.listdir(root_dir)
    markdown_files = [f for f in root_files if f.endswith(".md") and f not in ["README.md", "CHANGELOG.md"]]
    assert len(markdown_files) == 0, f"Found loose markdown specifications in root: {markdown_files}"
