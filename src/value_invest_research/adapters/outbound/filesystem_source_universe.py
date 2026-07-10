from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileSystemSourceUniverseRepository:
    """Resolve domain source universes from the project JSON catalog."""

    def __init__(self, path: Path):
        self.path = path

    def resolve_for_research(self, qa_tree: dict) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        domains = payload.get("domains") if isinstance(payload, dict) else {}
        if not isinstance(domains, dict):
            return {}

        haystack = " ".join(
            str(qa_tree.get(key) or "")
            for key in ("project_id", "domain_playbook", "title", "topic", "research_type")
        ).lower()
        best: tuple[int, str, dict[str, Any]] | None = None
        for domain_id, raw in domains.items():
            if not isinstance(raw, dict):
                continue
            aliases = [str(domain_id), *[str(item) for item in raw.get("aliases", []) or []]]
            score = sum(1 for alias in aliases if alias.lower() in haystack)
            candidate = (score, str(domain_id), raw)
            if best is None or candidate[0] > best[0]:
                best = candidate
        if best is None or best[0] == 0:
            return {}
        return {"domain_id": best[1], **best[2]}
