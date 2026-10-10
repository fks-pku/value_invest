#!/bin/bash
set -euo pipefail
research_project="$(cd "$(dirname "$0")" && pwd)"
research_repo="$(cd "$research_project/../../.." && pwd)"
research_python="${RESEARCH_PYTHON:-python3}"
if [[ -z "${RESEARCH_PYTHON:-}" && -x /Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 ]]; then
  research_python=/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
fi
cd "$research_repo"
export PYTHONPATH="$research_repo/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1
exec "$research_python" -m value_invest_research.adapters.inbound.researcher_server "$research_project" --port 8765
