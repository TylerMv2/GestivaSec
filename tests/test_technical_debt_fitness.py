"""
Gestiva Security (GestivaSec V1) — Technical Debt & Code Quality Fitness Gate
Verifies zero FIXME comments, controlled TODO count, and maximum module size bounds.
"""
import os
import ast
import pytest

BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend")

def test_zero_fixme_and_controlled_todo_count():
    """TECHNICAL DEBT FITNESS TEST 1: Zero FIXME comments allowed in production codebase."""
    fixme_count = 0
    todo_count = 0

    for root, _, files in os.walk(BACKEND_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    fixme_count += content.count("FIXME")
                    todo_count += content.count("TODO")

    assert fixme_count == 0, f"Technical debt violation: found {fixme_count} FIXME tags."
    assert todo_count < 10, f"Technical debt threshold exceeded: found {todo_count} TODO tags."

def test_module_size_bounds():
    """TECHNICAL DEBT FITNESS TEST 2: Functions < 200 lines, Classes < 300 lines."""
    for root, _, files in os.walk(BACKEND_DIR):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=filepath)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            lines = (node.end_lineno or 0) - (node.lineno or 0)
                            assert lines < 200, f"Function {node.name} in {file} exceeds max length ({lines} lines)."
                        elif isinstance(node, ast.ClassDef):
                            lines = (node.end_lineno or 0) - (node.lineno or 0)
                            assert lines < 300, f"Class {node.name} in {file} exceeds max length ({lines} lines)."
