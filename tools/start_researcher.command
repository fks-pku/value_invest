#!/bin/bash
# Double-click on macOS, or run with bash. The service is accessible only on this Mac.
set -euo pipefail
research_repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$research_repo"
export PYTHONPATH="$research_repo/src${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m value_invest_research.adapters.inbound.researcher_server "${1:-research/events/gpt6_ai_industry_impact_20260910}" --port 8765
