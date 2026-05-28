import unittest
from pathlib import Path
from unittest.mock import MagicMock

from tests.helpers import project_tmp_dir
from value_invest_research.sector_researcher import SectorResearcher, _build_system_prompt, _build_user_prompt, _ensure_sector_dir


class SectorResearcherTests(unittest.TestCase):
    def test_build_user_prompt_includes_value_chain(self):
        prompt = _build_user_prompt("Semiconductors", "sector", "AI chip demand and supply chain")
        self.assertIn("Semiconductors", prompt)
        self.assertIn("Current Research Goal", prompt)
        self.assertIn("Research Execution Plan", prompt)
        self.assertIn("QA Drilldown", prompt)
        self.assertIn("Specific Target Observation List", prompt)

    def test_system_prompt_uses_research_goal_qa_framework(self):
        prompt = _build_system_prompt()
        self.assertIn("Research Goal QA Framework", prompt)

    def test_build_user_prompt_theme_type(self):
        prompt = _build_user_prompt("AI Infrastructure", "theme", "Data center buildout")
        self.assertIn("Theme", prompt)

    def test_ensure_sector_dir_creates_structure(self):
        with project_tmp_dir() as tmp:
            sector_dir = _ensure_sector_dir(tmp, "sector", "semiconductors")
            self.assertTrue(sector_dir.exists())
            self.assertTrue((sector_dir / "sector_memo.md").exists())
            self.assertTrue((sector_dir / "data").exists())

    def test_run_sector_research_creates_analysis(self):
        with project_tmp_dir() as root:
            mock_client = MagicMock()
            mock_client.chat.return_value = "# Semiconductor Sector Analysis\n\nIndustry structure analysis here."

            researcher = SectorResearcher(mock_client)
            result = researcher.run_sector_research(
                root, "Semiconductors", "sector",
                research_focus="AI chip demand and supply chain dynamics",
                tickers_to_include=["NVDA", "AMD", "INTC"],
            )

            self.assertIn("analysis_path", result)
            self.assertTrue(Path(result["analysis_path"]).exists())
            self.assertEqual(result["sector_type"], "sector")

    def test_run_theme_research(self):
        with project_tmp_dir() as root:
            mock_client = MagicMock()
            mock_client.chat.return_value = "# AI Infrastructure Theme Analysis"

            researcher = SectorResearcher(mock_client)
            result = researcher.run_sector_research(
                root, "AI Infrastructure", "theme",
                research_focus="Data center buildout and power demand",
            )

            self.assertEqual(result["sector_type"], "theme")
            theme_dir = Path(result["sector_dir"])
            self.assertTrue((theme_dir / "theme_memo.md").exists())


if __name__ == "__main__":
    unittest.main()
