# Domain Layer

The domain layer contains research meaning and pure rules.

Allowed:

- dataclasses and value objects
- information category policies
- QA, source, scoring, target, and validation rules
- deterministic calculations

Current domain-owned research objects:

- `ResearchGoal`: the user objective, research type, run mode, and decision boundary.
- `DomainPlaybook`: the domain-specific adapter that decides what Q1-Q4 mean and how L2/L3 questions are shaped.
- `QuestionArchitecture`: the adaptive QA tree, with L3 decision questions and L4/L5 child-plan depth.
- `ResearchPlan`: immutable parent L3 rollups plus dependency-aware L5 execution steps.
- `research_plan`: pure step-event normalization, projection, and evidence/dependency completion gates.
- `l3_research_plan`: one independent plan per L3, canonical L4 research units, finest-leaf source contracts, and exact coverage validation.
- `ReportViewModel`: presentation-neutral public report data assembled from verified project artifacts.
- `leaf_research_tasks`: pure leaf task construction, skill dispatch selection, source-search plan, and extraction schema design from a QA tree.
- `leaf_answer_synthesis`: pure conversion from normalized provider results to leaf answers and parent rollup rows.

Forbidden:

- file-system access
- network access
- CLI parsing
- LLM or DeepSeek calls
- HTML rendering
- imports from `application`, `ports`, or `adapters`
