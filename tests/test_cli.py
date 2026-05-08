import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from tests.helpers import project_tmp_dir
from value_invest_research.cli import main


class CliTests(unittest.TestCase):
    def test_init_stock_command(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["--root", str(tmp), "init-stock", "MSFT", "--company-name", "Microsoft Corporation"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "stocks" / "MSFT" / "investment_memo.md").exists())

    def test_init_event_command(self):
        with project_tmp_dir() as tmp:
            with redirect_stdout(StringIO()):
                exit_code = main(["--root", str(tmp), "init-event", "2026-05-06", "US Iran Conflict"])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "research" / "events" / "2026-05-06_us_iran_conflict").exists())


if __name__ == "__main__":
    unittest.main()
