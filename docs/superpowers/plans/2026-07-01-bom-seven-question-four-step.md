# BOM Seven-Question Four-Step Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every BOM seven-question card in the AI Factory report and future framework contract follow the metric -> historical chart -> future metric -> first-principles mechanism structure.

**Architecture:** Keep the existing BOM-first report shell. Add a small renderer path inside `tools/generate_ai_factory_scurve_report.js` that normalizes each seven-question row into a four-step public evidence card. Update framework docs so future reports preserve the same structure.

**Tech Stack:** Node.js static HTML generator, Python unittest/pytest-compatible regression tests, Markdown framework contracts.

---

### Task 1: Add Failing Report-Structure Test

**Files:**
- Create: `tests/test_ai_factory_bom_four_step.py`

- [x] **Step 1: Write the failing test**

```python
import re
import unittest
from pathlib import Path


REPORT = Path("research/qa_projects/ai_factory_industry_scurve_timeslice_20260302/professional_report.html")


class AiFactoryBomFourStepTests(unittest.TestCase):
    def test_every_bom_question_card_has_four_step_metric_structure(self):
        html = REPORT.read_text(encoding="utf-8")
        cards = re.findall(
            r'<details class="bom-question-card"[^>]*>.*?</details>',
            html,
            flags=re.DOTALL,
        )
        self.assertGreaterEqual(len(cards), 42)
        for index, card in enumerate(cards, start=1):
            with self.subTest(card=index):
                self.assertIn("bom-step-metrics", card)
                self.assertIn("bom-step-history", card)
                self.assertRegex(card, r"metric-trend-chart|metric-noncontinuous-chart|metric-trend-gap")
                self.assertIn("bom-step-future", card)
                self.assertIn("bom-step-mechanism", card)
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_ai_factory_bom_four_step.py -q`

Expected: FAIL because the current report has plain answer cards without the four step classes.

### Task 2: Implement Four-Step Renderer

**Files:**
- Modify: `tools/generate_ai_factory_scurve_report.js`

- [x] **Step 1: Add row normalization**

Create helper functions that derive metrics, history series/gap, future movements, and mechanism text from existing row and BOM node data when a row does not provide richer step data.

- [x] **Step 2: Update `renderBomQuestionCard`**

Render every card through the four step classes before the final answer and source chips.

- [x] **Step 3: Run generator**

Run: `node tools/generate_ai_factory_scurve_report.js`

Expected: rewrites the AI Factory project artifacts and `professional_report.html`.

- [x] **Step 4: Run report-structure test**

Run: `python -m pytest tests/test_ai_factory_bom_four_step.py -q`

Expected: PASS.

### Task 3: Update Persistent Framework Docs

**Files:**
- Modify: `AGENTS.md`
- Modify: `skills/value_invest_research/SKILL.md`
- Modify: `skills/value_invest_research/frameworks/research_goal_qa.md`
- Modify: `skills/value_invest_research/frameworks/research_report_contract.md`

- [x] **Step 1: Add the four-step BOM question contract**

Add the persistent rule that every BOM seven-question card must contain the four public steps and chart/gap handling.

- [x] **Step 2: Run framework quality tests**

Run: `python -m pytest tests/test_research_framework_quality.py -q`

Expected: PASS.

### Task 4: Final Verification

**Files:**
- Read/check only unless failures require a targeted fix.

- [x] **Step 1: Run targeted contract tests**

Run: `python -m pytest tests/test_ai_factory_bom_four_step.py tests/test_framework_contracts.py tests/test_research_framework_quality.py -q`

Expected: PASS.

- [x] **Step 2: Run DOM/browser smoke check**

Browser plugin access to the local `file://` report was blocked by URL policy, so verification used a local DOM smoke check for the same structure signals: BOM question card count, four-step classes, metric charts/gaps, industry-module `details`, and target action-state classes.
