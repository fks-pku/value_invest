#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from value_invest_research.application.use_cases.build_bom_project_manifest import (
    build_bom_project_manifest,
)


def main() -> int:
    payload = json.load(sys.stdin)
    manifest = build_bom_project_manifest(
        str(payload.get("parent_project_id") or ""),
        payload.get("nodes") or [],
        research_run_node_ids=payload.get("research_run_node_ids") or [],
    )
    json.dump(manifest, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
