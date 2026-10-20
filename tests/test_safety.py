from __future__ import annotations

import pytest

from taskpilot.safety import SandboxViolation


def test_path_escape_blocked(sandbox):
    with pytest.raises(SandboxViolation):
        sandbox.resolve("../escape.txt")


def test_inside_ok(sandbox):
    p = sandbox.resolve("sub/file.txt")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("ok")
    assert p.read_text() == "ok"


def test_unknown_tool(tools):
    with pytest.raises(PermissionError):
        tools.call("format_disk", None, {})