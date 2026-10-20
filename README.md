# TaskPilot AI ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Autonomous Task Execution & Verification Agent

TaskPilot AI receives a task, plans it into verifiable steps, executes them through
allowlisted tools in a sandboxed workspace, and independently verifies every result
before claiming success.

The agent never trusts its own claim of success. Every step must pass deterministic
verification checks, and every failure is recorded with evidence.

Built for HackerRank Orchestrate (October Edition).

## Quickstart (Windows / PowerShell)

    py -3 -m venv .venv
    . .\.venv\Scripts\Activate.ps1
    python -m pip install -e . pytest
    .\verify.ps1

## Quickstart (macOS / Linux)

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e . pytest
    python -m taskpilot run --task examples/task_demo.json --workspace ./workspace --out ./output.csv --logs ./logs

## Architecture

    Task JSON -> Planner -> Executor -> Verifier -> Report Writer -> output.csv
                                  |
                                  +-> transcript.jsonl (audit trail)

1. Plan ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â reads a structured task definition
2. Execute ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â calls allowlisted tools with timeouts and bounded retries
3. Verify ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â runs deterministic checks (file exists, CSV schema, row count)
4. Report ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â emits a CSV with status, verified, evidence, and error per step

## CSV output schema

    task_id,step_id,action,target,status,verified,evidence,error,attempts,duration_ms

src/taskpilot/report_writer.py is the single source of truth.

## Safety model

- Path sandbox ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every file tool resolves under --workspace
- Tool allowlist ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â unknown actions fail with PermissionError
- Timeouts ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-step timeout (default 30s)
- Bounded retries ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â max 2 retries; exhaustion means status=failed
- Independent verifier ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â never asks the LLM "did this work?"

## Tests

    pytest -q

The test suite covers success, failure, retry exhaustion, unknown actions,
path escape prevention, CSV schema validation, and row count checks.

## Deliverables (Orchestrate)

| Requirement | Produced by |
|---|---|
| Code ZIP + README | This repo |
| Output CSV | report_writer.py -> output.csv |
| AI chat transcript | logs/transcript.jsonl |

## Verified output

    $ pytest -q
    ................                    [100%]
    16 passed

    $ python -m taskpilot run --task examples\task_demo.json ...
    [taskpilot] 3 steps, 0 failed. CSV: output.csv

    $ python -m taskpilot run --task examples\task_failure.json ...
    [taskpilot] 1 steps, 1 failed. CSV: output_fail.csv