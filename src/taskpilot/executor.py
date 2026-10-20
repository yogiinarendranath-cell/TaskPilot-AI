from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

from .config import Settings
from .models import Plan, Step, StepResult, StepStatus
from .tools import ToolRegistry
from .verifier import Verifier


class Executor:
    def __init__(self, tools, verifier, settings):
        self.tools = tools
        self.verifier = verifier
        self.settings = settings
        self._pool = ThreadPoolExecutor(max_workers=1)

    def run(self, plan):
        return [self._run_step(plan.task_id, step) for step in plan.steps]

    def _run_step(self, task_id, step):
        attempts = 0
        last_error = None
        started = time.monotonic()

        for attempt in range(1, self.settings.max_step_retries + 2):
            attempts = attempt
            try:
                self._call_with_timeout(step)
                verification = self.verifier.check_all(step.verify or [])
                if not verification.ok:
                    last_error = verification.evidence
                    if attempt <= self.settings.max_step_retries:
                        continue
                    return self._result(task_id, step, StepStatus.FAILED, False,
                                        verification.evidence, last_error, attempts, started)
                return self._result(task_id, step, StepStatus.SUCCESS, True,
                                    verification.evidence, None, attempts, started)
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt <= self.settings.max_step_retries:
                    continue
                return self._result(task_id, step, StepStatus.FAILED, False,
                                    "no verification (execution failed)", last_error,
                                    attempts, started)

        return self._result(task_id, step, StepStatus.FAILED, False,
                            "no verification", last_error, attempts, started)

    def _call_with_timeout(self, step):
        future = self._pool.submit(self.tools.call, step.action, step.target, step.args)
        try:
            future.result(timeout=self.settings.step_timeout_seconds)
        except FutureTimeout as exc:
            raise TimeoutError(
                f"step {step.step_id} exceeded {self.settings.step_timeout_seconds}s"
            ) from exc

    def _result(self, task_id, step, status, verified, evidence, error, attempts, started):
        return StepResult(
            task_id=task_id,
            step_id=step.step_id,
            action=step.action,
            target=step.target,
            status=status,
            verified=verified,
            evidence=evidence,
            error=error,
            attempts=attempts,
            duration_ms=int((time.monotonic() - started) * 1000),
        )