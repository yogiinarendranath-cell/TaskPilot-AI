from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    max_step_retries: int = 2
    step_timeout_seconds: int = 30
    model: str = "gpt-4o-mini"
    openai_api_key: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            max_step_retries=int(os.getenv("TASKPILOT_MAX_STEP_RETRIES", "2")),
            step_timeout_seconds=int(os.getenv("TASKPILOT_STEP_TIMEOUT_SECONDS", "30")),
            model=os.getenv("TASKPILOT_MODEL", "gpt-4o-mini"),
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        )