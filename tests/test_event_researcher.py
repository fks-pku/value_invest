import unittest
from pathlib import Path
from unittest.mock import MagicMock

from tests.helpers import project_tmp_dir
from value_invest_research.event_researcher import EventResearcher, _build_system_prompt, _build_user_prompt


class EventResearcherTests(unittest.TestCase):
    def test_build_user_prompt_includes_research_goal_qa(self):
        prompt = _build_user_prompt("US-Iran Conflict", "2026-05-06", "Military escalation in the Persian Gulf")
        self.assertIn("US-Iran Conflict", prompt)
        self.assertIn("Current Research Goal", prompt)
        self.assertIn("Research Execution Plan", prompt)
        self.assertIn("QA Drilldown", prompt)
        self.assertIn("Specific Target Observation List", prompt)

    def test_system_prompt_uses_research_goal_qa_framework(self):
        prompt = _build_system_prompt()
        self.assertIn("Research Goal QA Framework", prompt)

    def test_build_user_prompt_includes_playbook(self):
        playbook = {"first_questions": ["What happened?"], "transmission_channels": ["oil_prices"]}
        prompt = _build_user_prompt("Test Event", "2026-05-06", "desc", playbook=playbook)
        self.assertIn("Applicable Playbook", prompt)
        self.assertIn("oil_prices", prompt)

    def test_run_event_research_creates_analysis(self):
        with project_tmp_dir() as root:
            mock_client = MagicMock()
            mock_client.chat.return_value = "# Event Analysis\n\nConfirmed facts here.\n\n### 4. Candidate Screen\n\nTier 1 candidates."

            researcher = EventResearcher(mock_client)
            result = researcher.run_event_research(
                root, "2026-05-06", "Oil Price Shock",
                event_description="Crude oil surged 15% after supply disruption",
            )

            self.assertIn("analysis_path", result)
            self.assertTrue(Path(result["analysis_path"]).exists())
            content = Path(result["analysis_path"]).read_text(encoding="utf-8")
            self.assertIn("Confirmed facts", content)


if __name__ == "__main__":
    unittest.main()
