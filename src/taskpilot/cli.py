from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import Settings
from .executor import Executor
from .planner import load_plan_from_json
from .report_writer import write_report
from .safety import PathSandbox
from .tools import ToolRegistry
from .transcript import TranscriptLogger
from .verifier import Verifier


def _build_parser():
    parser = argparse.ArgumentParser(prog="taskpilot")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Execute a task plan")
    run.add_argument("--task", required=True, type=Path)
    run.add_argument("--workspace", required=True, type=Path)
    run.add_argument("--out", required=True, type=Path)
    run.add_argument("--logs", required=True, type=Path)
    return parser


def main(argv=None):
    args = _build_parser().parse_args(argv)
    if args.cmd != "run":
        return 2

    settings = Settings.from_env()
    sandbox = PathSandbox(args.workspace)
    tools = ToolRegistry(sandbox)
    verifier = Verifier(sandbox)
    executor = Executor(tools, verifier, settings)

    with TranscriptLogger(args.logs) as transcript:
        try:
            plan = load_plan_from_json(args.task)
        except Exception as exc:
            transcript.log("plan_error", error=str(exc))
            print(f"[taskpilot] failed to load plan: {exc}", file=sys.stderr)
            return 1

        transcript.log("plan_loaded", task_id=plan.task_id, steps=len(plan.steps))
        results = executor.run(plan)
        for r in results:
            transcript.log("step_result", **r.to_row())

        write_report(results, args.out)
        transcript.log("report_written", path=str(args.out))

        failed = sum(1 for r in results if r.status.value == "failed")
        print(f"[taskpilot] {len(results)} steps, {failed} failed. CSV: {args.out}")
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())