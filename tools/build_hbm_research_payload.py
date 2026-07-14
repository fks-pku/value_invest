#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from value_invest_research.application.use_cases.build_bom_node_research_payload import (
    build_bom_node_research_payload,
)
from value_invest_research.domain.bom_node_playbooks import get_bom_node_playbook


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: build_hbm_research_payload.py RESEARCH_RUN.json", file=sys.stderr)
        return 2
    run_path = Path(sys.argv[1])
    research_run = json.loads(run_path.read_text(encoding="utf-8"))
    payload = build_bom_node_research_payload(
        get_bom_node_playbook(str(research_run.get("node_id") or "")),
        research_run,
    )
    json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
