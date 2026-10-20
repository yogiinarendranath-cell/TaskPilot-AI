from __future__ import annotations

import csv
from pathlib import Path


SCHEMA = [
    "task_id", "step_id", "action", "target", "status",
    "verified", "evidence", "error", "attempts", "duration_ms",
]


class SchemaError(Exception):
    pass


def validate_rows(rows):
    if not rows:
        raise SchemaError("no rows to write")
    for row in rows:
        missing = set(SCHEMA) - row.keys()
        extra = set(row.keys()) - set(SCHEMA)
        if missing:
            raise SchemaError(f"row missing columns: {missing}")
        if extra:
            raise SchemaError(f"row has unexpected columns: {extra}")


def write_report(results, out_path: Path) -> None:
    rows = [r.to_row() for r in results]
    validate_rows(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(rows)