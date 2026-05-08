import unittest

from tests.helpers import project_tmp_dir
from value_invest_research.runlog import RunLog, RunStatus


class RunLogTests(unittest.TestCase):
    def test_append_and_read_entries(self):
        with project_tmp_dir() as tmp:
            log = RunLog(tmp)
            log.append("test_pipeline", RunStatus.SUCCESS, tickers=["AAPL"], records_fetched=5)
            entries = log.read()
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["pipeline"], "test_pipeline")
            self.assertEqual(entries[0]["status"], "success")
            self.assertEqual(entries[0]["records_fetched"], 5)

    def test_logs_failed_run_with_error(self):
        with project_tmp_dir() as tmp:
            log = RunLog(tmp)
            log.append("bad_pipeline", RunStatus.FAILURE, error="timeout")
            entries = log.read()
            self.assertEqual(entries[0]["error"], "timeout")

    def test_is_content_hash_new(self):
        with project_tmp_dir() as tmp:
            log = RunLog(tmp)
            self.assertTrue(log.is_content_new("hash123"))
            log.record_content_hash("hash123")
            self.assertFalse(log.is_content_new("hash123"))


if __name__ == "__main__":
    unittest.main()
