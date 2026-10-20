from __future__ import annotations

import csv


def test_file_exists_pass(verifier, sandbox):
    sandbox.resolve("x.txt").write_text("hi")
    assert verifier.check({"type": "file_exists", "path": "x.txt"}).ok


def test_file_exists_fail(verifier):
    assert not verifier.check({"type": "file_exists", "path": "nope.txt"}).ok


def test_csv_schema_pass(verifier, sandbox):
    p = sandbox.resolve("d.csv")
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["a", "b"])
        w.writerow([1, 2])
    result = verifier.check({"type": "csv_schema", "path": "d.csv", "columns": ["a", "b"]})
    assert result.ok


def test_csv_schema_mismatch(verifier, sandbox):
    p = sandbox.resolve("d.csv")
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y"])
    result = verifier.check({"type": "csv_schema", "path": "d.csv", "columns": ["a", "b"]})
    assert not result.ok
    assert "schema mismatch" in result.evidence


def test_row_count_min(verifier, sandbox):
    p = sandbox.resolve("d.csv")
    p.write_text("a,b\n1,2\n3,4\n")
    assert verifier.check({"type": "row_count_min", "path": "d.csv", "min": 2}).ok
    assert not verifier.check({"type": "row_count_min", "path": "d.csv", "min": 5}).ok