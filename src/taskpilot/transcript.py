from __future__ import annotations

import json
import time
from pathlib import Path


class TranscriptLogger:
    def __init__(self, log_dir: Path) -> None:
        log_dir.mkdir(parents=True, exist_ok=True)
        self.path = log_dir / "transcript.jsonl"
        self._fh = self.path.open("w", encoding="utf-8")

    def log(self, event, **fields):
        record = {"ts": time.time(), "event": event, **fields}
        self._fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self):
        self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()