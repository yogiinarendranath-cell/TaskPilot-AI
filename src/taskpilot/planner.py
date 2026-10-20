from __future__ import annotations

import json
from pathlib import Path

from .models import Plan, Step


def load_plan_from_json(path: Path) -> Plan:
    data = json.loads(path.read_text(encoding="utf-8"))
    steps = [
        Step(
            step_id=s["step_id"],
            action=s["action"],
            target=s.get("target"),
            args=s.get("args", {}),
            verify=s.get("verify", []),
        )
        for s in data["steps"]
    ]
    return Plan(task_id=data["task_id"], goal=data.get("goal", ""), steps=steps)


def plan_from_goal(goal: str, task_id: str = "llm-task") -> Plan:
    raise NotImplementedError("LLM planner not wired yet.")