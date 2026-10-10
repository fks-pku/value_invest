#!/bin/bash
# Run with an explicit project; never silently open an unrelated past study.
set -euo pipefail
research_repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$research_repo"
if [[ $# -eq 0 ]]; then
  echo '用法：bash tools/start_researcher.command <项目目录> [--port 8765]'
  exit 2
fi
research_project="$1"
shift
research_python="${RESEARCH_PYTHON:-python3}"
if [[ -z "${RESEARCH_PYTHON:-}" && -x "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" ]]; then
  research_python="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
fi
export PYTHONPATH="$research_repo/src${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1
exec "$research_python" -m value_invest_research.adapters.inbound.researcher_server "$research_project" "$@"
