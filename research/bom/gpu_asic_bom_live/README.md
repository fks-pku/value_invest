# GPU / ASIC BOM project

This directory is the complete, portable research project for the GPU / ASIC BOM.

```text
project.json              project identity, mode, questions, and relevance profile
professional_report.md    canonical public research report
timeline_profile.json     five-lens logic definitions
sources.jsonl             reviewed source index
source/                   canonical original materials
material_intake/          discovery, relevance, scan, and deduplication ledgers
inbox/                    source-by-question parsing queue
ledger/                   reviewed atomic claims and current conclusions
```

Original IMA reports live only under `source/ima/YYYY/MM/DD/`. Files in this
project use project-relative links so the whole directory can be moved or
archived as one research unit.

## Design discussion

The 2026-08-07 discussion about moving from table-centered demand research to a
logic-chain-centered, temporal atomic-claim model is preserved in
[`docs/superpowers/specs/2026-08-07-logic-chain-centered-bom-research.md`](../../../docs/superpowers/specs/2026-08-07-logic-chain-centered-bom-research.md).
It is a discussion baseline, not an implemented framework contract.
