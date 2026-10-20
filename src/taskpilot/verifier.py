from __future__ import annotations

import csv

from .safety import PathSandbox


class VerificationResult:
    def __init__(self, ok: bool, evidence: str) -> None:
        self.ok = ok
        self.evidence = evidence

    def __bool__(self):
        return self.ok


class Verifier:
    def __init__(self, sandbox: PathSandbox) -> None:
        self.sandbox = sandbox

    def check(self, spec):
        kind = spec.get("type")
        if kind == "file_exists":
            return self._file_exists(spec["path"])
        if kind == "csv_schema":
            return self._csv_schema(spec["path"], spec["columns"])
        if kind == "row_count_min":
            return self._row_count_min(spec["path"], int(spec["min"]))
        if kind == "contains":
            return self._contains(spec["path"], spec["text"])
        return VerificationResult(False, f"unknown check type: {kind}")

    def check_all(self, specs):
        for spec in specs:
            result = self.check(spec)
            if not result.ok:
                return result
        return VerificationResult(True, f"{len(specs)} checks passed")

    def _file_exists(self, rel):
        if self.sandbox.resolve(rel).exists():
            return VerificationResult(True, f"file exists: {rel}")
        return VerificationResult(False, f"file missing: {rel}")

    def _csv_schema(self, rel, columns):
        path = self.sandbox.resolve(rel)
        if not path.exists():
            return VerificationResult(False, f"file missing: {rel}")
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                return VerificationResult(False, f"empty csv: {rel}")
        if header != columns:
            return VerificationResult(False, f"schema mismatch in {rel}: expected {columns}, got {header}")
        return VerificationResult(True, f"schema ok: {columns}")

    def _row_count_min(self, rel, minimum):
        path = self.sandbox.resolve(rel)
        if not path.exists():
            return VerificationResult(False, f"file missing: {rel}")
        with path.open("r", encoding="utf-8", newline="") as f:
            rows = sum(1 for _ in csv.reader(f)) - 1
        if rows >= minimum:
            return VerificationResult(True, f"{rows} rows >= {minimum}")
        return VerificationResult(False, f"{rows} rows < {minimum}")

    def _contains(self, rel, text):
        path = self.sandbox.resolve(rel)
        if not path.exists():
            return VerificationResult(False, f"file missing: {rel}")
        if text in path.read_text(encoding="utf-8"):
            return VerificationResult(True, f"contains: {text!r}")
        return VerificationResult(False, f"does not contain: {text!r}")