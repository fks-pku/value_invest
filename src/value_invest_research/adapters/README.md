# Adapters

Adapters implement ports at the system edge.

Inbound adapters parse external requests and call application use cases.
Outbound adapters talk to file systems, LLMs, DeepSeek, market data, SEC, search, or renderers.

Adapters may depend on application, ports, and domain. Domain and application must not depend on adapters.

Current outbound report adapters:

- `FileSystemResearchProjectRepository` loads report inputs from plain project files, including `investment_workbench.json` for structured industry-overview artifacts.
- `CanonicalMarkdownReportRenderer` renders the canonical four-section public report from `ReportViewModel`.
- `CanonicalHtmlReportRenderer` and `report_sections/` remain compatibility adapters for browser views.
- `research_search_providers.py` contains provider-specific leaf source parsing/search adapters, including mock, Perplexity, Exa, and generic OpenAI-compatible providers.
- `source_material_parsers.py` contains deterministic and delegating adapters for L3 source extraction and review.

Changing the public text structure belongs in the Markdown renderer and report contract. Changing compatibility HTML look and interaction should create or update an HTML renderer adapter,
not domain question planning or source parsing code.
