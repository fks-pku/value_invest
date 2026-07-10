# Adapters

Adapters implement ports at the system edge.

Inbound adapters parse external requests and call application use cases.
Outbound adapters talk to file systems, LLMs, DeepSeek, market data, SEC, search, or renderers.

Adapters may depend on application, ports, and domain. Domain and application must not depend on adapters.

Current outbound report adapters:

- `FileSystemResearchProjectRepository` loads report inputs from plain project files, including `investment_workbench.json` for structured industry-overview artifacts.
- `CanonicalHtmlReportRenderer` renders the locked four-section public report from `ReportViewModel`; drilldown QA remains an internal artifact unless explicitly requested.
- `report_sections/` contains the per-section HTML adapters used by `CanonicalHtmlReportRenderer`.
- `research_search_providers.py` contains provider-specific leaf source parsing/search adapters, including mock, Perplexity, Exa, and generic OpenAI-compatible providers.
- `source_material_parsers.py` contains deterministic and delegating adapters for L3 source extraction and review.

Changing the HTML look and interaction should create or update a renderer adapter,
not domain question planning or source parsing code.
