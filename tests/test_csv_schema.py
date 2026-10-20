from __future__ import annotations

import pytest

from taskpilot.models import StepResult, StepStatus
from taskpilot.report_writer import SCHEMA, SchemaError, validate_rows, write_report


def _row(**overrides):
    base = {
        "task_id": "t", "step_id": "s", "action": "a", "target": "",
        "status": "success", "verified": "true", "evidence": "",
        "error": "", "attempts": "1", "duration_ms": "10",
    }
    base.update(overrides)
    return base


def test_schema_validation_passes():
    validate_rows([_row()])


def test_schema_missing_column():
    bad = _row()
    bad.pop("verified")
    with pytest.raises(SchemaError):
        validate_rows([bad])


def test_schema_extra_column():
    bad = _row(extra="oops")
    with pytest.raises(SchemaError):
        validate_rows([bad])


def test_write_report_roundtrip(tmp_path):
    result = StepResult(
        task_id="t", step_id="s", action="a", target=None,
        status=StepStatus.SUCCESS, verified=True, evidence="ok",
        error=None, attempts=1, duration_ms=5,
    )
    out = tmp_path / "out.csv"
    write_report([result], out)
    header = out.read_text(encoding="utf-8").splitlines()[0]
    assert header.split(",") == SCHEMA