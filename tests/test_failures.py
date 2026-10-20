from __future__ import annotations

from taskpilot.config import Settings
from taskpilot.executor import Executor
from taskpilot.models import Plan, Step, StepStatus


def test_retries_exhausted(tools, verifier):
    plan = Plan(
        task_id="t", goal="missing",
        steps=[Step(step_id="s", action="read_file", target="nope.txt")],
    )
    results = Executor(tools, verifier, Settings(max_step_retries=2)).run(plan)
    r = results[0]
    assert r.status == StepStatus.FAILED
    assert r.attempts == 3
    assert r.error is not None


def test_unknown_action_is_failed(tools, verifier):
    plan = Plan(
        task_id="t", goal="bogus",
        steps=[Step(step_id="s", action="rm_rf", target="/")],
    )
    results = Executor(tools, verifier, Settings(max_step_retries=0)).run(plan)
    assert results[0].status == StepStatus.FAILED
    assert "disallowed" in (results[0].error or "").lower()