from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path


class RunStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


class RunLog:
    def __init__(self, log_dir: Path) -> None:
        self._log_dir = log_dir
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._log_path = log_dir / "runs.jsonl"
        self._hashes_path = log_dir / "content_hashes.jsonl"

    def append(
        self,
        pipeline: str,
        status: RunStatus,
        tickers: list[str] | None = None,
        records_fetched: int = 0,
        records_new: int = 0,
        error: str | None = None,
    ) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline": pipeline,
            "status": status.value,
            "tickers": tickers or [],
            "records_fetched": records_fetched,
            "records_new": records_new,
        }
        if error is not None:
            entry["error"] = error
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def read(self) -> list[dict]:
        if not self._log_path.exists():
            return []
        lines = self._log_path.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line.strip()]

    def is_content_new(self, content_hash: str) -> bool:
        if not self._hashes_path.exists():
            return True
        known = {
            json.loads(line)["hash"]
            for line in self._hashes_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        return content_hash not in known

    def record_content_hash(self, content_hash: str) -> None:
        with open(self._hashes_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"hash": content_hash, "ts": datetime.now(timezone.utc).isoformat()}) + "\n")
