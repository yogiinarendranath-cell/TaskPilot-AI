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
    """Use the LLM to turn a natural-language goal into a Plan."""
    from .llm import ask_json

    prompt = f"""
You are a task planner for an autonomous agent.

Given a goal, produce a JSON plan with this exact shape:
{{
  "task_id": "{task_id}",
  "goal": "...",
  "steps": [
    {{
      "step_id": "s1",
      "action": "<one of: list_dir, read_file, write_file, read_csv, write_csv, run_python, llm_ask>",
      "target": "<file path or null>",
      "args": {{}},
      "verify": [{{"type": "file_exists", "path": "..."}}]
    }}
  ]
}}

Available verification types:
- {{"type": "file_exists", "path": "<path>"}}
- {{"type": "csv_schema", "path": "<path>", "columns": ["col1", "col2"]}}
- {{"type": "row_count_min", "path": "<path>", "min": <int>}}
- {{"type": "contains", "path": "<path>", "text": "<substring>"}}

Rules:
- Every step that writes a file MUST have at least one verify entry.
- If a step needs LLM reasoning, use action "llm_ask" with args.prompt.
- Keep the plan small: 3-6 steps maximum.
- Do not invent tools. Only use the actions listed above.

Goal: {goal}
"""
    data = ask_json(prompt, model="openai/gpt-oss-120b")
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
    return Plan(task_id=data.get("task_id", task_id), goal=goal, steps=steps)
