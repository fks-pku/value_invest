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
The baseline is now implemented by the versioned `logic_chain_centered` profile.
As of `2026-08-12.v2`, claim-to-node review distinguishes direct support/refute
from boundaries, constraints, leads, unresolved relations, new branches, and
explicitly rejected `unmapped` relations. The executable framework contracts,
validators, ledgers, and generated reports are authoritative when this earlier
discussion note differs from the implementation.
