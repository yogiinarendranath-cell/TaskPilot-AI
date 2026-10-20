from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StepStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Step:
    step_id: str
    action: str
    target: str | None = None
    args: dict[str, Any] = field(default_factory=dict)
    verify: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Plan:
    task_id: str
    goal: str
    steps: list[Step]


@dataclass
class StepResult:
    task_id: str
    step_id: str
    action: str
    target: str | None
    status: StepStatus
    verified: bool
    evidence: str
    error: str | None
    attempts: int
    duration_ms: int

    def to_row(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "step_id": self.step_id,
            "action": self.action,
            "target": self.target or "",
            "status": self.status.value,
            "verified": "true" if self.verified else "false",
            "evidence": self.evidence,
            "error": self.error or "",
            "attempts": str(self.attempts),
            "duration_ms": str(self.duration_ms),
        }