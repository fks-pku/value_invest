# Value Invest Research

File-system-first US equity research assistant. Plain files are the source of truth; Python code validates contracts, scaffolds research objects, ingests public data, and creates LLM research drafts.

## Module Index

| Module | Path | Purpose |
|------|------|------|
| Core package | `src/value_invest_research/` | CLI, schemas, scaffolding, ingestion, run logs, and LLM research workflows. |
| Tests | `tests/` | unittest coverage for schemas, CLI, scaffolding, ingestion, and research workflow prompt/output behavior. |
| Research skill | `skills/value_invest_research/` | Operating protocol, frameworks, prompts, and evidence checklists. |
| Config | `config/` | Watchlist, source priority, research object registry, and event playbooks. |
| Stock objects | `stocks/` | Stock memos, evidence logs, structured data, run logs, and proposals. |
| Research objects | `research/` | Sector/theme/event memos, evidence, candidate screens, and run logs. |

## Commands

```powershell
python tools/run_tests.py
$env:PYTHONPATH = "src"; python -m value_invest_research --help
value-invest-research --help
```

## Key Constraints

- Do not issue final trading instructions.
- Keep material claims tied to evidence IDs.
- Separate facts, inferences, and judgments.
- Keep low-reliability evidence as research leads only.
- Preserve existing research history; proposals are safer than silent memo overwrites.
- Optional integrations must fail with clear install guidance when dependencies are missing.
