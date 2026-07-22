import unittest

from value_invest_research.domain.bom_project_layout import build_bom_project_layout


class BomProjectLayoutTests(unittest.TestCase):
    def test_builds_one_child_project_per_canonical_node(self):
        manifest = build_bom_project_layout(
            "ai_factory",
            [
                {"id": "compute", "name": "计算加速器"},
                {"id": "memory", "name": "HBM"},
            ],
            research_run_node_ids=["compute"],
        )

        self.assertEqual(manifest["project_scope"], "industry_chain")
        self.assertEqual([node["node_id"] for node in manifest["nodes"]], ["compute", "memory"])
        self.assertEqual(manifest["nodes"][0]["report_path"], "boms/compute/professional_report.html")
        self.assertEqual(manifest["nodes"][0]["research_run_path"], "boms/compute/research_run.json")
        self.assertEqual(manifest["nodes"][0]["ledger_directory"], "boms/compute/ledger")
        self.assertEqual(
            manifest["nodes"][0]["temporal_manifest_path"],
            "boms/compute/temporal_manifest.json",
        )
        self.assertIsNone(manifest["nodes"][1]["research_run_path"])

    def test_rejects_unsafe_duplicate_and_unknown_run_nodes(self):
        with self.assertRaises(ValueError):
            build_bom_project_layout("p", [{"id": "../compute", "name": "Compute"}])
        with self.assertRaises(ValueError):
            build_bom_project_layout(
                "p",
                [{"id": "compute", "name": "A"}, {"id": "compute", "name": "B"}],
            )
        with self.assertRaises(ValueError):
            build_bom_project_layout(
                "p",
                [{"id": "compute", "name": "Compute"}],
                research_run_node_ids=["memory"],
            )


if __name__ == "__main__":
    unittest.main()
