# Ports

Ports define what the application needs from the outside world.

Examples:

- repositories for research artifacts
- source parsing artifact writers
- leaf research workflow seams during migration
- leaf research providers and raw provider response stores
- leaf research result repositories for merged results and source indexes
- leaf research artifact repositories for task, result, answer, and rollup files
- research project repositories for project metadata, QA trees, source indexes, and target lists
- research plan repositories for immutable parent/L3 plan versions and append-only step events
- LLM/source parser interfaces
- source material parser and extraction reviewer interfaces
- market data interfaces
- report renderer interfaces, including the canonical report renderer
- search/fetch interfaces

Ports are protocols or abstract contracts. They must not import adapters.
