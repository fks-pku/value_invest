#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from value_invest_research.domain.bom_research_readiness import build_bom_completion_scoring_inputs
from value_invest_research.domain.target_scoring import score_and_rank_targets


def main() -> int:
    payload = json.load(sys.stdin)
    targets = payload.get("targets") or []
    workbench = payload.get("workbench") or {}
    scoring_inputs = build_bom_completion_scoring_inputs(targets, workbench)
    result = score_and_rank_targets(scoring_inputs, workbench=workbench)
    if not result.ok:
        json.dump({"ok": False, "issues": result.issues}, sys.stderr, ensure_ascii=False)
        return 1
    json.dump(result.ranked_targets, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
