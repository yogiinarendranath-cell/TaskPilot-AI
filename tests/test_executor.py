from __future__ import annotations

from taskpilot.config import Settings
from taskpilot.executor import Executor
from taskpilot.models import Plan, Step, StepStatus


def test_successful_step(tools, verifier, sandbox):
    sandbox.resolve("a.txt").write_text("hello")
    plan = Plan(
        task_id="t1",
        goal="read a file",
        steps=[Step(
            step_id="s1",
            action="read_file",
            target="a.txt",
            verify=[{"type": "file_exists", "path": "a.txt"}],
        )],
    )
    results = Executor(tools, verifier, Settings()).run(plan)
    assert len(results) == 1
    assert results[0].status == StepStatus.SUCCESS
    assert results[0].verified is True
    assert results[0].attempts == 1


def test_failed_verification_marks_failed(tools, verifier):
    plan = Plan(
        task_id="t2",
        goal="missing file",
        steps=[Step(
            step_id="s1",
            action="read_file",
            target="ghost.txt",
            verify=[{"type": "file_exists", "path": "ghost.txt"}],
        )],
    )
    results = Executor(tools, verifier, Settings(max_step_retries=0)).run(plan)
    assert results[0].status == StepStatus.FAILED
    assert results[0].verified is False
    assert results[0].error is not None