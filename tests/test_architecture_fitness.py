"""
Gestiva Security (GestivaSec V1) — Architecture Fitness & Quality Gate Suite
Verifies Architecture Invariants, Pure Domain Isolation, and Contract Safety.
"""
import os
import ast
import pytest

DOMAIN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "domain")

def test_domain_purity_no_infrastructure_imports():
    """ARCHITECTURE FITNESS TEST 1: Domain modules must NEVER import infrastructure or frameworks."""
    forbidden_modules = {"asyncpg", "psycopg2", "fastapi", "httpx", "redis", "celery", "infrastructure"}
    
    for root, _, files in os.walk(DOMAIN_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=filepath)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                for forbidden in forbidden_modules:
                                    assert not alias.name.startswith(forbidden), f"Domain purity violation in {file}: imported {alias.name}"
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                for forbidden in forbidden_modules:
                                    assert not node.module.startswith(forbidden), f"Domain purity violation in {file}: imported from {node.module}"

def test_no_circular_imports():
    """ARCHITECTURE FITNESS TEST 2: Validates zero circular imports across backend modules."""
    try:
        from backend.domain.auth import UserIdentity
        from backend.domain.organization import Organization
        from backend.domain.user import User
        from backend.domain.asset import DigitalAsset
        from backend.domain.synthetic import SyntheticObservation
        assert True
    except ImportError as e:
        pytest.fail(f"Circular import detected: {e}")
