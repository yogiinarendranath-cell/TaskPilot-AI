from __future__ import annotations

from pathlib import Path


class SandboxViolation(Exception):
    pass


class PathSandbox:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative):
        candidate = (self.root / relative).resolve()
        if self.root != candidate and self.root not in candidate.parents:
            raise SandboxViolation(
                f"Path {relative} escapes workspace {self.root}"
            )
        return candidate


ALLOWED_ACTIONS = frozenset(
    {"list_dir", "read_file", "write_file", "read_csv", "write_csv", "run_python", "llm_ask"}
)


def ensure_allowed(action: str) -> None:
    if action not in ALLOWED_ACTIONS:
        raise PermissionError(f"Action {action} is not in the allowlist")