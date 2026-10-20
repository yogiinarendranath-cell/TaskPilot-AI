from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@pytest.fixture
def sandbox(tmp_path):
    from taskpilot.safety import PathSandbox
    return PathSandbox(tmp_path)


@pytest.fixture
def tools(sandbox):
    from taskpilot.tools import ToolRegistry
    return ToolRegistry(sandbox)


@pytest.fixture
def verifier(sandbox):
    from taskpilot.verifier import Verifier
    return Verifier(sandbox)