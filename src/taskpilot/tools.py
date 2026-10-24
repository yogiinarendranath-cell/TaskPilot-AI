from __future__ import annotations

import csv
import subprocess
import sys
from typing import Any

from .safety import PathSandbox


class ToolRegistry:
    def __init__(self, sandbox: PathSandbox) -> None:
        self.sandbox = sandbox
        self._tools = {
            "list_dir": self._list_dir,
            "read_file": self._read_file,
            "write_file": self._write_file,
            "read_csv": self._read_csv,
            "write_csv": self._write_csv,
            "run_python": self._run_python,
            "llm_ask": self._llm_ask,
        }

    def call(self, action: str, target, args: dict[str, Any]):
        if action not in self._tools:
            raise PermissionError(f"Unknown or disallowed action: {action}")
        return self._tools[action](target, args)

    def _list_dir(self, target, args):
        path = self.sandbox.resolve(target or ".")
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Not a directory: {target}")
        return sorted(p.name for p in path.iterdir())

    def _read_file(self, target, args):
        if not target:
            raise ValueError("read_file requires a target")
        return self.sandbox.resolve(target).read_text(encoding=args.get("encoding", "utf-8"))

    def _write_file(self, target, args):
        if not target:
            raise ValueError("write_file requires a target")
        path = self.sandbox.resolve(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = args.get("content", "")
        path.write_text(content, encoding=args.get("encoding", "utf-8"))
        return len(content)

    def _read_csv(self, target, args):
        if not target:
            raise ValueError("read_csv requires a target")
        path = self.sandbox.resolve(target)
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def _write_csv(self, target, args):
        if not target:
            raise ValueError("write_csv requires a target")
        columns = args["columns"]
        rows = args["rows"]
        path = self.sandbox.resolve(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        return len(rows)

    def _run_python(self, target, args):
        script = args.get("script", target)
        if not script:
            raise ValueError("run_python requires a script path")
        script_path = self.sandbox.resolve(script)
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script}")
        timeout = args.get("timeout", 30)
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(self.sandbox.root),
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Script failed ({proc.returncode}): {proc.stderr.strip()}")
        return {"returncode": proc.returncode, "stdout": proc.stdout}

    def _llm_ask(self, target, args):
        prompt = args.get("prompt")
        if not prompt:
            raise ValueError("llm_ask requires a 'prompt' arg")
        from .llm import ask as _ask
        model = args.get("model", "llama-3.1-8b-instant")
        return _ask(prompt, model=model)