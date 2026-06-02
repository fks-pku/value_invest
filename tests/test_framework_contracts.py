import json
import unittest
from copy import deepcopy
from pathlib import Path

from value_invest_research.framework_contracts import (
    QA_BLOCK_TITLES,
    REPORT_SECTIONS,
    TARGET_SCORE_DIMENSIONS,
    attach_forward_return_labels,
    audit_time_slice_sources,
    build_internal_workbench,
    build_prediction_review,
    build_training_sample,
    freeze_recommendations,
    get_domain_playbook,
    rank_target_observations,
    score_target_observation,
    validate_leaf_source_review_schema,
    validate_backtest_leakage_controls,
    validate_source_extraction_schema,
    validate_qa_tree_schema,
    validate_report_contract_html,
    validate_target_observation_contract,
)


class FrameworkContractsTests(unittest.TestCase):
    def test_report_and_qa_contracts_enforce_hierarchy_label_boundary_and_cards(self):
        goal_title, chain_title, qa_title, target_title, source_title = REPORT_SECTIONS
        block_one, block_two, block_three = QA_BLOCK_TITLES
        html = f"""
        <main>
          <header class="hero"></header>
          <nav class="top-nav"></nav>
          <section id="goal"><h2>{goal_title}</h2><div class="goal-card"></div></section>
          <section id="chain" class="supply-chain-section"><h2>{chain_title}</h2>
            <div class="chain-explain">
              <p class="chain-plain-summary">一句话看懂：需求从客户进入链条，经由上中下游交付产品，利润集中在稀缺卡点。</p>
              <ol class="chain-flow-steps"><li>客户提出需求</li><li>平台和设备商组织供给</li><li>稀缺节点捕获利润</li></ol>
              <div class="chain-layer-grid"><article class="chain-layer-card">上游负责关键输入</article></div>
              <div class="chain-chokepoints">关键卡点：认证、产能、软件生态。</div>
              <div class="chain-target-links">对应标的：Q2/Q4 继续验证。</div>
            </div>
            <div class="chain-map">
              <table class="chain-table"><tr><th>上游</th><th>中游</th><th>下游</th><th>关键玩家</th><th>价值关系</th></tr></table>
            </div>
          </section>
          <section id="qa"><h2>{qa_title}</h2><div class="qa-body"></div>
            <details class="qa-card level-1" id="q1" open>
              <summary><h3>Q1 demand</h3><span class="qa-count">1</span><span class="chevron">›</span></summary>
              <div class="qa-body">
                <section class="qa-block"><h4 class="block-title">{block_one}</h4></section>
                <section class="qa-block"><h4 class="block-title">{block_two}</h4>
                  <details class="qa-card level-2" id="q1-1" open>
                    <summary><h3>Q1.1 mechanism</h3><span class="qa-count">1</span><span class="chevron">›</span></summary>
                    <section class="qa-block"><h4 class="block-title">{block_one}</h4></section>
                    <section class="qa-block"><h4 class="block-title">{block_two}</h4>
                      <details class="qa-card level-3" id="q1-1-1" open>
                        <summary><h3>Q1.1.1 leaf</h3><span class="qa-count">leaf</span><span class="chevron">›</span></summary>
                        <section class="qa-block"><h4 class="block-title">{block_one}</h4>
                          <div class="l3-meta">
                            <span class="l3-skill">financial-statement-analysis</span>
                            <span class="l3-execution-status">deepseek_mcp_completed</span>
                            <span class="l3-score-component">future_space</span>
                            <span class="l3-decision-use">changes target ranking</span>
                          </div>
                          <div class="artifact-card"></div>
                        </section>
                        <section class="qa-block"><h4 class="block-title">{block_two}</h4></section>
                        <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
                      </details>
                    </section>
                    <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
                  </details>
                </section>
                <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
              </div>
            </details>
            <details class="qa-card level-1" id="q4" open>
              <summary><h3>Q4 target selection</h3><span class="qa-count">1</span><span class="chevron">›</span></summary>
              <details class="qa-card level-2" id="q4-1" open>
                <summary><h3>Q4.1 ranking</h3><span class="qa-count">1</span><span class="chevron">›</span></summary>
                <details class="qa-card level-3" id="q4-1-1" open>
                  <summary><h3>Q4.1.1 target</h3><span class="qa-count">leaf</span><span class="chevron">›</span></summary>
                  <section class="qa-block"><h4 class="block-title">{block_one}</h4>
                    <div class="l3-meta">
                      <span class="l3-skill">target-recommendation-analysis</span>
                      <span class="l3-execution-status">deepseek_mcp_completed</span>
                      <span class="l3-score-component">target_ranking</span>
                      <span class="l3-decision-use">changes action state</span>
                    </div>
                  </section>
                </details>
              </details>
            </details>
          </section>
          <section class="target-section" id="targets"><h2>{target_title}</h2>
            <table class="target-table"><tr><th>forward_3m_return</th></tr></table>
          </section>
          <details class="source-collapse" id="sources"><summary><h2>{source_title}</h2></summary></details>
        </main>
        """

        result = validate_report_contract_html(html, mode="historical_backtest", require_l3=True)

        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual(result["summary"]["top_level_sections"], REPORT_SECTIONS)
        self.assertEqual(result["summary"]["supply_chain_sections"], 1)
        self.assertEqual(result["summary"]["level3_cards"], 2)
        self.assertEqual(result["summary"]["interactive_level3_cards"], 2)

        no_chain_result = validate_report_contract_html(
            html.replace(
                f"""
          <section id=\"chain\" class=\"supply-chain-section\"><h2>{chain_title}</h2>
            <div class=\"chain-explain\">
              <p class=\"chain-plain-summary\">一句话看懂：需求从客户进入链条，经由上中下游交付产品，利润集中在稀缺卡点。</p>
              <ol class=\"chain-flow-steps\"><li>客户提出需求</li><li>平台和设备商组织供给</li><li>稀缺节点捕获利润</li></ol>
              <div class=\"chain-layer-grid\"><article class=\"chain-layer-card\">上游负责关键输入</article></div>
              <div class=\"chain-chokepoints\">关键卡点：认证、产能、软件生态。</div>
              <div class=\"chain-target-links\">对应标的：Q2/Q4 继续验证。</div>
            </div>
            <div class=\"chain-map\">
              <table class=\"chain-table\"><tr><th>上游</th><th>中游</th><th>下游</th><th>关键玩家</th><th>价值关系</th></tr></table>
            </div>
          </section>""",
                "",
            ),
            mode="historical_backtest",
            require_l3=True,
        )
        self.assertFalse(no_chain_result["ok"])
        self.assertIn("missing_supply_chain_section", {issue["code"] for issue in no_chain_result["issues"]})

        invalid = html.replace("<table class=\"target-table\"><tr><th>forward_3m_return</th></tr></table>", "").replace(
            f"<section class=\"qa-block\"><h4 class=\"block-title\">{block_one}</h4></section>",
            f"<section class=\"qa-block\"><h4 class=\"block-title\">{block_one}</h4>forward_3m_return</section>",
            1,
        )
        invalid_result = validate_report_contract_html(invalid, mode="historical_backtest", require_l3=True)
        self.assertFalse(invalid_result["ok"])
        self.assertIn("label_outside_final_targets", {issue["code"] for issue in invalid_result["issues"]})

        static_invalid = html.replace(
            '<details class="qa-card level-1" id="q1" open>',
            '<article class="qa-card level-1" id="q1">',
            1,
        )
        static_result = validate_report_contract_html(static_invalid, mode="historical_backtest", require_l3=True)
        self.assertFalse(static_result["ok"])
        self.assertIn("missing_interactive_qa_cards", {issue["code"] for issue in static_result["issues"]})

        uncolored_action_state = html.replace(
            '<table class="target-table"><tr><th>forward_3m_return</th></tr></table>',
            '<table class="target-table"><tr><th>forward_3m_return</th><td>watch_only</td></tr></table>',
        )
        uncolored_result = validate_report_contract_html(uncolored_action_state, mode="historical_backtest", require_l3=True)
        self.assertFalse(uncolored_result["ok"])
        self.assertIn("missing_action_state_color_class", {issue["code"] for issue in uncolored_result["issues"]})

        no_beginner_chain = html.replace('class="chain-explain"', 'class="chain-explain-missing"', 1)
        no_beginner_result = validate_report_contract_html(no_beginner_chain, mode="historical_backtest", require_l3=True)
        self.assertFalse(no_beginner_result["ok"])
        self.assertIn("missing_beginner_chain_explainer", {issue["code"] for issue in no_beginner_result["issues"]})

        meta_drift_invalid = html.replace(
            f"<section id=\"goal\"><h2>{goal_title}</h2><div class=\"goal-card\"></div></section>",
            f"<section id=\"goal\"><h2>{goal_title}</h2><div class=\"goal-card\"></div><p>本轮升级了机制深度映射。</p></section>",
        )
        meta_result = validate_report_contract_html(meta_drift_invalid, mode="historical_backtest", require_l3=True)
        self.assertFalse(meta_result["ok"])
        self.assertIn("public_meta_drift", {issue["code"] for issue in meta_result["issues"]})

    def test_adaptive_drilldown_allows_l4_l5_but_rejects_l6(self):
        goal_title, chain_title, qa_title, target_title, source_title = REPORT_SECTIONS
        block_one, block_two, block_three = QA_BLOCK_TITLES
        html = f"""
        <main>
          <header class="hero"></header>
          <nav class="top-nav"></nav>
          <section id="goal"><h2>{goal_title}</h2><div class="goal-card"></div></section>
          <section id="chain" class="supply-chain-section"><h2>{chain_title}</h2>
            <div class="chain-explain">
              <p class="chain-plain-summary">一句话看懂链条。</p>
              <ol class="chain-flow-steps"><li>需求</li><li>供给</li><li>瓶颈</li></ol>
              <div class="chain-layer-grid"><article class="chain-layer-card">上游</article></div>
              <div class="chain-chokepoints">卡点</div>
              <div class="chain-target-links">标的</div>
              <div class="chain-map"><table class="chain-table"><tr><th>层级</th></tr></table></div>
            </div>
          </section>
          <section id="qa"><h2>{qa_title}</h2><div class="qa-body"></div>
            <details class="qa-card level-1" id="q1" open>
              <summary><span>Q1</span><span class="qa-count">1</span><span class="chevron">›</span></summary>
              <section class="qa-block"><h4 class="block-title">{block_one}</h4><div class="artifact-card"></div></section>
              <section class="qa-block"><h4 class="block-title">{block_two}</h4>
                <details class="qa-card level-2" id="q1-1" open>
                  <summary><span>Q1.1</span><span class="qa-count">1</span><span class="chevron">›</span></summary>
                  <section class="qa-block"><h4 class="block-title">{block_one}</h4><div class="artifact-card"></div></section>
                  <section class="qa-block"><h4 class="block-title">{block_two}</h4>
                    <details class="qa-card level-3" id="q1-1-1" open>
                      <summary><span>Q1.1.1</span><span class="qa-count">1</span><span class="chevron">›</span></summary>
                      <section class="qa-block"><h4 class="block-title">{block_one}</h4>{_l3_meta_html()}<div class="artifact-card"></div></section>
                      <section class="qa-block"><h4 class="block-title">{block_two}</h4>
                        <details class="qa-card level-4" id="q1-1-1-1" open>
                          <summary><span>Q1.1.1.1</span><span class="qa-count">1</span><span class="chevron">›</span></summary>
                          <section class="qa-block"><h4 class="block-title">{block_one}</h4>{_l3_meta_html()}<div class="artifact-card"></div></section>
                          <section class="qa-block"><h4 class="block-title">{block_two}</h4>
                            <details class="qa-card level-5" id="q1-1-1-1-1" open>
                              <summary><span>Q1.1.1.1.1</span><span class="qa-count">0</span><span class="chevron">›</span></summary>
                              <section class="qa-block"><h4 class="block-title">{block_one}</h4>{_l3_meta_html()}<div class="artifact-card"></div></section>
                              <section class="qa-block"><h4 class="block-title">{block_two}</h4></section>
                              <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
                            </details>
                          </section>
                          <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
                        </details>
                      </section>
                      <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
                    </details>
                  </section>
                  <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
                </details>
              </section>
              <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
            </details>
            <details class="qa-card level-1" id="q4" open>
              <summary><span>Q4</span><span class="qa-count">0</span><span class="chevron">›</span></summary>
              <section class="qa-block"><h4 class="block-title">{block_one}</h4><div class="artifact-card"></div></section>
              <section class="qa-block"><h4 class="block-title">{block_two}</h4></section>
              <section class="qa-block"><h4 class="block-title">{block_three}</h4></section>
            </details>
          </section>
          <section id="targets" class="target-section"><h2>{target_title}</h2>
            <table class="target-table"><tr><td><span class="state-pill state-watch_only">watch_only</span></td></tr></table>
          </section>
          <section id="sources"><h2>{source_title}</h2><details class="source-collapse"><summary>sources</summary></details></section>
        </main>
        """

        html_result = validate_report_contract_html(html, mode="live_prediction", require_l3=True)
        self.assertTrue(html_result["ok"], html_result["issues"])
        self.assertEqual(html_result["summary"]["level4_cards"], 1)
        self.assertEqual(html_result["summary"]["level5_cards"], 1)

        qa_tree = {"nodes": _adaptive_depth_nodes()}
        qa_result = validate_qa_tree_schema(qa_tree, require_l3=True)
        self.assertTrue(qa_result["ok"], qa_result["issues"])
        self.assertEqual(qa_result["summary"]["max_depth"], 5)

        too_deep = deepcopy(qa_tree)
        too_deep["nodes"].append({**_complete_research_node("Q1.1.1.1.1.1", 6), "parent_id": "Q1.1.1.1.1"})
        too_deep_result = validate_qa_tree_schema(too_deep, require_l3=True)
        self.assertFalse(too_deep_result["ok"])
        self.assertIn("qa_depth_exceeds_max", {issue["code"] for issue in too_deep_result["issues"]})

    def test_qa_schema_time_slice_scoring_freeze_labels_samples_and_review(self):
        qa_tree = {
            "run_mode": "historical_backtest",
            "as_of_date": "2026-02-28",
            "anti_leakage_controls": {
                "anti_leakage_level": "source_pack_grounded",
                "as_of_date": "2026-02-28",
                "cutoff_source_pack_policy": "all_thesis_sources_visible_on_or_before_as_of_date",
                "llm_prior_policy": "model_prior_is_not_evidence",
                "question_tree_policy": "questions_may_use_playbook_but_strength_requires_cutoff_sources",
                "supply_chain_policy": "supply_chain_claims_require_cutoff_source_ids",
                "scoring_policy": "target_scores_require_verified_leaf_reviews_or_cutoff_sources",
                "label_isolation_policy": "labels_attached_after_frozen_recommendations_only",
            },
            "nodes": [
                {"id": "root", "level": 0, "question": "Research AI hardware", "next_question_ids": ["q1"]},
                {"id": "q1", "level": 1, "question": "Q1 demand", "parent_id": "root", "next_question_ids": ["q1-1"]},
                {
                    "id": "q1-1",
                    "level": 2,
                    "question": "Q1.1 cloud budgets",
                    "parent_id": "q1",
                    "next_question_ids": ["q1-1-1"],
                },
                {
                    "id": "q1-1-1",
                    "level": 3,
                    "question": "Q1.1.1 budget conversion",
                    "parent_id": "q1-1",
                    "materiality": "changes target strength",
                    "decision_use": "decides whether AI demand can strengthen target ranking",
                    "support_evidence": ["capex guide supports AI hardware demand"],
                    "refute_evidence": ["capex cuts or weak ROI would refute demand durability"],
                    "target_implications": "raises demand visibility if verified",
                    "score_component": "future_space",
                    "minimum_evidence_gate": "primary source visible before cutoff",
                    "refuting_source_plan": ["search for customer ROI or capex cuts"],
                    "source_plan": [{"source_id": "ev1", "source_visible_at": "2026-02-20", "allowed_usage": "thesis"}],
                    "skill_dispatch": {
                        "task_family": "financial_statement",
                        "selected_skill": "financial-statement-analysis",
                        "concrete_materials": ["ev1"],
                        "extraction_schema": ["revenue", "capex", "margin"],
                        "source_extraction_ids": ["se-q1-1-1-ev1"],
                        "leaf_source_review_ids": ["review-q1-1-1-ev1"],
                        "skill_output_status": "complete",
                        "fallback_used": False,
                        "gpt_verification_status": "verified",
                    },
                    "fact": ["capex guide visible before cutoff"],
                    "inference": ["demand is real"],
                    "judgment": "support",
                    "gap": ["customer ROI"],
                    "trigger": ["capex cuts"],
                    "source_links": ["ev1"],
                    "backtest_grounding": {
                        "allowed_source_ids": ["ev1"],
                        "model_prior_policy": "hypothesis_only_not_scoring_evidence",
                        "post_cutoff_knowledge_policy": "forbidden_except_final_label",
                        "non_source_claims": [],
                    },
                },
            ]
        }
        schema_result = validate_qa_tree_schema(qa_tree, require_l3=True)
        self.assertTrue(schema_result["ok"], schema_result["issues"])
        self.assertEqual(schema_result["summary"]["l3_nodes"], 1)

        undifferentiated_tree = deepcopy(qa_tree)
        undifferentiated_leaf = undifferentiated_tree["nodes"][-1]
        undifferentiated_leaf["fact"] = "same repeated answer"
        undifferentiated_leaf["inference"] = "same repeated answer"
        undifferentiated_leaf["judgment"] = "same repeated answer"
        undifferentiated_result = validate_qa_tree_schema(undifferentiated_tree, require_l3=True)
        self.assertFalse(undifferentiated_result["ok"])
        self.assertIn("l3_undifferentiated_logic", {issue["code"] for issue in undifferentiated_result["issues"]})

        weak_question_tree = deepcopy(qa_tree)
        weak_leaf = weak_question_tree["nodes"][-1]
        weak_leaf.pop("decision_use")
        weak_leaf["source_plan"] = "read filings and reports"
        weak_leaf["skill_dispatch"] = "financial-statement-analysis"
        weak_result = validate_qa_tree_schema(weak_question_tree, require_l3=True)
        self.assertFalse(weak_result["ok"])
        issue_codes = {issue["code"] for issue in weak_result["issues"]}
        self.assertIn("l3_missing_field", issue_codes)
        self.assertIn("l3_source_plan_not_structured", issue_codes)
        self.assertIn("l3_skill_dispatch_not_structured", issue_codes)

        sources = [
            {
                "source_id": "ev1",
                "source_visible_at": "2026-02-20",
                "allowed_usage": "thesis",
                "used_in": ["q1-1-1"],
                "availability_proof": {"proof_type": "publisher_date", "proof_value": "2026-02-20"},
            },
            {"source_id": "label_prices", "source_visible_at": "2026-05-29", "allowed_usage": "label_only", "used_in": ["final_label"]},
            {"source_id": "future_report", "source_visible_at": "2026-04-01", "allowed_usage": "thesis", "used_in": ["q4-1"]},
        ]
        audit = audit_time_slice_sources(sources, as_of_date="2026-02-28")
        self.assertFalse(audit["ok"])
        self.assertEqual(audit["summary"]["post_cutoff_non_label_count"], 1)
        self.assertIn("source_missing_availability_proof", {issue["code"] for issue in audit["issues"]})

        extraction_schema_result = validate_source_extraction_schema(
            [
                {
                    "extraction_id": "se-q1-1-1-ev1",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                    "source_title": "Visible evidence",
                    "source_bucket": "evidence",
                    "parser": "deepseek_mcp",
                    "parser_status": "ok",
                    "schema_fields": {
                        "revenue": {"value": "capex guide visible before cutoff", "evidence_ids": ["ev1"]},
                        "capex": {"value": "AI budget conversion", "evidence_ids": ["ev1"]},
                        "margin": {"value": "not disclosed", "evidence_ids": ["ev1"], "status": "not_available"},
                    },
                    "key_facts": ["capex guide visible before cutoff"],
                    "inference": "AI budget can convert into hardware demand.",
                    "support_refute_or_lead": "support",
                    "uncertainties": ["customer ROI"],
                    "follow_up_data": ["next capex guide"],
                    "created_at": "2026-02-20T00:00:00Z",
                }
            ],
            qa_tree,
        )
        self.assertTrue(extraction_schema_result["ok"], extraction_schema_result["issues"])

        review_schema_result = validate_leaf_source_review_schema(
            [
                {
                    "review_id": "review-q1-1-1-ev1",
                    "extraction_id": "se-q1-1-1-ev1",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                    "gpt_verification_status": "verified",
                    "adopted_facts": ["capex guide visible before cutoff"],
                    "corrections": [],
                    "rejected_claims": [],
                    "final_bucket": "evidence",
                    "final_support_refute_or_lead": "support",
                    "allowed_to_strengthen_conclusion": True,
                }
            ],
            [
                {
                    "extraction_id": "se-q1-1-1-ev1",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                }
            ],
            qa_tree,
        )
        self.assertTrue(review_schema_result["ok"], review_schema_result["issues"])

        bad_review_schema_result = validate_leaf_source_review_schema(
            [
                {
                    "review_id": "review-q1-1-1-ev1",
                    "extraction_id": "missing-extraction",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                    "gpt_verification_status": "needs_review",
                    "adopted_facts": ["capex guide visible before cutoff"],
                    "corrections": [],
                    "rejected_claims": [],
                    "final_bucket": "evidence",
                    "final_support_refute_or_lead": "support",
                    "allowed_to_strengthen_conclusion": True,
                }
            ],
            [],
            qa_tree,
        )
        self.assertFalse(bad_review_schema_result["ok"])
        bad_review_codes = {issue["code"] for issue in bad_review_schema_result["issues"]}
        self.assertIn("leaf_source_review_unknown_extraction", bad_review_codes)
        self.assertIn("leaf_source_review_allows_unverified_extraction", bad_review_codes)

        bad_extraction_schema_result = validate_source_extraction_schema(
            [
                {
                    "extraction_id": "se-q1-1-1-ev1",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                    "parser": "deepseek_mcp",
                    "parser_status": "ok",
                }
            ],
            qa_tree,
        )
        self.assertFalse(bad_extraction_schema_result["ok"])
        self.assertIn("source_extraction_missing_schema_fields", {issue["code"] for issue in bad_extraction_schema_result["issues"]})

        score = score_target_observation(
            {
                "ticker": "MU",
                "chokepoint_strength": 3,
                "future_space": 5,
                "valuation_odds": 3,
                "evidence_quality": 4,
                "disconfirming_risk_control": 3,
                "monitorability": 5,
                "payoff_convexity": 5,
                "valuation_tolerance": 3,
                "downside_fragility": 2,
                "catalyst_proximity": 4,
                "score_subcomponents": {
                    "chokepoint_strength": [
                        {"name": "demand_flow", "score": 4.5, "weight": 0.5, "evidence_ids": ["ev1"], "review_ids": ["review-q1-1-1-ev1"]},
                        {"name": "substitution_barrier", "score": 3.5, "weight": 0.5, "evidence_ids": ["ev1"], "review_ids": ["review-q1-1-1-ev1"]},
                    ]
                },
            }
        )
        self.assertGreater(score["total_score"], 0)
        self.assertIn("thesis_confidence", score)
        self.assertIn("payoff_convexity", score)
        self.assertNotEqual(score["thesis_confidence"], score["payoff_convexity"])
        self.assertIn("action_state", score)
        self.assertIn("opportunity_fit", score)
        self.assertEqual(score["score_components"]["chokepoint_strength"], 4.0)
        self.assertEqual(set(score["score_dimensions"]), set(TARGET_SCORE_DIMENSIONS))
        self.assertEqual(score["score_dimensions"]["scarcity_or_monopoly"], 4.0)
        self.assertIn("mispricing", score["score_dimensions"])
        self.assertIn("earnings_elasticity", score["score_dimensions"])
        self.assertIn("risk_control", score["score_dimensions"])
        self.assertIn("score_subcomponents", score)

        theme_only_score = score_target_observation(
            {
                "ticker": "THEME",
                "chokepoint_strength": 2,
                "future_space": 5,
                "valuation_odds": 2,
                "evidence_quality": 4,
                "disconfirming_risk_control": 3,
                "monitorability": 5,
                "payoff_convexity": 5,
                "valuation_tolerance": 4,
                "downside_fragility": 2,
                "catalyst_proximity": 4,
                "demand_visibility": 5,
                "irreplaceability": 2,
                "market_underpricing": 2,
            }
        )
        self.assertEqual(theme_only_score["action_state"], "no_action")
        self.assertLessEqual(theme_only_score["total_score"], 2.69)
        self.assertIn("scarcity_or_irreplaceability_below_gate", theme_only_score["gate_reasons"])
        self.assertIn("market_underpricing_below_gate", theme_only_score["gate_reasons"])
        self.assertLess(theme_only_score["score_dimensions"]["scarcity_or_monopoly"], 3.0)

        scarce_underpriced_score = score_target_observation(
            {
                "ticker": "SCARCE",
                "chokepoint_strength": 5,
                "future_space": 4.5,
                "valuation_odds": 4,
                "evidence_quality": 4,
                "disconfirming_risk_control": 4,
                "monitorability": 4,
                "payoff_convexity": 4,
                "valuation_tolerance": 4,
                "downside_fragility": 2,
                "catalyst_proximity": 4,
                "demand_visibility": 4.5,
                "irreplaceability": 5,
                "market_underpricing": 4,
                "expected_excess_return": 0.18,
                "evidence_ids": ["ev1"],
                "review_ids": ["review-q1-1-1-ev1"],
            }
        )
        self.assertEqual(scarce_underpriced_score["action_state"], "actionable_long")
        self.assertGreaterEqual(scarce_underpriced_score["opportunity_fit"], 4.0)
        self.assertGreaterEqual(scarce_underpriced_score["score_dimensions"]["scarcity_or_monopoly"], 4.0)
        self.assertGreaterEqual(scarce_underpriced_score["score_dimensions"]["mispricing"], 4.0)
        self.assertNotIn("market_underpricing_below_gate", scarce_underpriced_score["gate_reasons"])

        ranked = rank_target_observations(
            [
                {"ticker": "WATCH", "score": theme_only_score, "rank": 1},
                {"ticker": "ACTION", "score": scarce_underpriced_score, "rank": 2},
            ]
        )
        self.assertEqual([target["ticker"] for target in ranked], ["ACTION", "WATCH"])
        self.assertEqual([target["rank"] for target in ranked], [1, 2])

        target_contract = validate_target_observation_contract(
            [
                {
                    "ticker": "ACTION",
                    "rank": 1,
                    "score": scarce_underpriced_score,
                    "score_subcomponents": scarce_underpriced_score["score_subcomponents"],
                    "thesis_kill_tests": [
                        {
                            "test": "HBM demand fails to convert",
                            "evidence_needed": "customer capex cuts",
                            "downgrade_action": "downgrade to watch_only",
                            "source_plan": ["ev1"],
                        }
                    ],
                }
            ]
        )
        self.assertTrue(target_contract["ok"], target_contract["issues"])

        leakage_result = validate_backtest_leakage_controls(
            qa_tree,
            [
                {
                    "extraction_id": "se-q1-1-1-ev1",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                }
            ],
            [
                {
                    "review_id": "review-q1-1-1-ev1",
                    "extraction_id": "se-q1-1-1-ev1",
                    "l3_question_id": "q1-1-1",
                    "source_id": "ev1",
                    "allowed_to_strengthen_conclusion": True,
                }
            ],
            [
                {
                    "ticker": "ACTION",
                    "score": scarce_underpriced_score,
                    "score_subcomponents": scarce_underpriced_score["score_subcomponents"],
                }
            ],
            sources[:2],
        )
        self.assertTrue(leakage_result["ok"], leakage_result["issues"])

        leaky_tree = deepcopy(qa_tree)
        leaky_tree["nodes"][-1]["backtest_grounding"]["non_source_claims"] = ["post-cutoff winner knowledge"]
        leaky_result = validate_backtest_leakage_controls(leaky_tree, [], [], [], sources[:2])
        self.assertFalse(leaky_result["ok"])
        self.assertIn("l3_backtest_has_non_source_claims", {issue["code"] for issue in leaky_result["issues"]})

        weak_score = deepcopy(scarce_underpriced_score)
        weak_score.pop("score_subcomponents", None)
        weak_target_contract = validate_target_observation_contract(
            [{"ticker": "ACTION", "rank": 1, "score": weak_score}]
        )
        self.assertFalse(weak_target_contract["ok"])
        weak_target_issue_codes = {issue["code"] for issue in weak_target_contract["issues"]}
        self.assertIn("target_missing_score_subcomponents", weak_target_issue_codes)
        self.assertIn("actionable_target_missing_kill_tests", weak_target_issue_codes)

        frozen = freeze_recommendations(
            [
                {
                    "ticker": "MU",
                    "name": "Micron",
                    "rank": 1,
                    "rationale": "HBM chokepoint exposure",
                    "score": score,
                    "forward_3m_return": 0.99,
                }
            ],
            as_of_date="2026-02-28",
            frozen_at="2026-02-28T23:59:00Z",
        )
        self.assertNotIn("forward_3m_return", frozen["targets"][0])
        self.assertEqual(frozen["targets"][0]["rank"], 1)

        labeled = attach_forward_return_labels(
            frozen,
            {
                "MU": {
                    "evaluation_date": "2026-05-29",
                    "label_window": "three_month_forward",
                    "start_price": 92.0,
                    "end_price": 118.0,
                    "forward_3m_return": 0.2826,
                    "benchmark_return": 0.12,
                    "excess_return": 0.1626,
                    "price_source": "Nasdaq",
                    "label_status": "verified",
                }
            },
            attached_at="2026-05-29T12:00:00Z",
        )
        self.assertEqual(labeled["targets"][0]["label"]["forward_3m_return"], 0.2826)
        self.assertEqual(labeled["targets"][0]["rationale"], "HBM chokepoint exposure")

        sample = build_training_sample(labeled, research_goal="Semiconductor hardware", benchmark="SMH")
        self.assertEqual(sample["research_goal"], "Semiconductor hardware")
        self.assertEqual(sample["targets"][0]["label"]["forward_3m_return"], 0.2826)
        self.assertIn("score_components", sample["targets"][0])

        review = build_prediction_review(
            labeled,
            {"MU": {"status": "supported", "notes": ["HBM demand remained visible"], "failed_l3": []}},
        )
        self.assertEqual(review["targets"][0]["current_status"], "supported")
        self.assertIn("evidence_or_weight_error", review["review_questions"])

        workbench = build_internal_workbench(
            source_extractions=[{"extraction_id": "ex1"}],
            leaf_source_reviews=[{"review_id": "rv1"}],
            scoring_worksheet=[score],
            validator_output={"ok": True},
            rejected_future_sources=[{"source_id": "future_report"}],
            frozen_recommendations=frozen,
            label_attach=labeled["label_attach"],
        )
        self.assertIn("source_extractions", workbench)
        self.assertIn("rejected_future_sources", workbench)

        playbook = get_domain_playbook("semiconductor_hardware")
        self.assertIn("demand reality", playbook["q_map"]["Q1"].lower())
        self.assertIn("HBM", " ".join(playbook["mechanism_buckets"]))

        memory_playbook = get_domain_playbook("memory_industry")
        self.assertIn("Demand-supply slope mismatch", memory_playbook["mechanism_buckets"])
        self.assertIn("memory_unit_economics", memory_playbook["required_extraction_schemas"])
        self.assertIn("model_reconciliation", memory_playbook["mechanism_depth_blocks"])
        self.assertEqual(get_domain_playbook("storage")["q_map"]["Q1"], memory_playbook["q_map"]["Q1"])

        event_playbook = get_domain_playbook("gtc")
        self.assertIn("Fact boundary", event_playbook["q_map"]["Q1"])
        self.assertIn("conference_claim_quality", event_playbook["required_extraction_schemas"])
        self.assertIn("company_exposure_and_financial_conversion", event_playbook["mechanism_buckets"])

    def test_gold_research_fixture_satisfies_full_quality_gate(self):
        fixture_dir = Path(__file__).parent / "fixtures" / "research_quality_gold"
        html = (fixture_dir / "professional_report.html").read_text(encoding="utf-8")
        qa_tree = json.loads((fixture_dir / "qa_tree.json").read_text(encoding="utf-8"))
        source_extractions = _read_jsonl(fixture_dir / "source_extractions.jsonl")
        leaf_source_reviews = _read_jsonl(fixture_dir / "leaf_source_reviews.jsonl")
        workbench = json.loads((fixture_dir / "investment_workbench.json").read_text(encoding="utf-8"))

        report_result = validate_report_contract_html(html, require_l3=True)
        self.assertTrue(report_result["ok"], report_result["issues"])
        qa_result = validate_qa_tree_schema(qa_tree, require_l3=True)
        self.assertTrue(qa_result["ok"], qa_result["issues"])
        extraction_result = validate_source_extraction_schema(source_extractions, qa_tree)
        self.assertTrue(extraction_result["ok"], extraction_result["issues"])
        review_result = validate_leaf_source_review_schema(leaf_source_reviews, source_extractions, qa_tree)
        self.assertTrue(review_result["ok"], review_result["issues"])
        target_result = validate_target_observation_contract(workbench["scoring_worksheet"])
        self.assertTrue(target_result["ok"], target_result["issues"])


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _l3_meta_html() -> str:
    return """
    <div class="l3-meta">
      <span class="l3-skill">financial-statement-analysis</span>
      <span class="l3-execution-status">verified_with_caveats</span>
      <span class="l3-score-component">future_space</span>
      <span class="l3-decision-use">changes target ranking</span>
    </div>
    """


def _adaptive_depth_nodes() -> list[dict]:
    return [
        {"id": "Q1", "level": 1, "question": "L1", "parent_id": "", "next_question_ids": ["Q1.1"]},
        {"id": "Q1.1", "level": 2, "question": "L2", "parent_id": "Q1", "next_question_ids": ["Q1.1.1"]},
        {**_complete_research_node("Q1.1.1", 3), "parent_id": "Q1.1", "next_question_ids": ["Q1.1.1.1"]},
        {**_complete_research_node("Q1.1.1.1", 4), "parent_id": "Q1.1.1", "next_question_ids": ["Q1.1.1.1.1"]},
        {**_complete_research_node("Q1.1.1.1.1", 5), "parent_id": "Q1.1.1.1", "next_question_ids": []},
    ]


def _complete_research_node(node_id: str, level: int) -> dict:
    return {
        "id": node_id,
        "level": level,
        "question": f"{node_id} adaptive research unit",
        "parent_id": "",
        "next_question_ids": [],
        "decision_use": "changes target ranking",
        "materiality": "material to score",
        "support_evidence": "support evidence",
        "refute_evidence": "refute evidence",
        "target_implications": "target implications",
        "score_component": "future_space",
        "minimum_evidence_gate": "minimum gate",
        "refuting_source_plan": "refuting source plan",
        "source_plan": [{"source_id": "SRC-1", "source_bucket": "evidence", "allowed_usage": "thesis"}],
        "skill_dispatch": {
            "task_family": "adaptive_depth_test",
            "selected_skill": "financial-statement-analysis",
            "concrete_materials": ["SRC-1"],
            "extraction_schema": ["field"],
            "source_extraction_ids": [f"EX-{node_id}"],
            "leaf_source_review_ids": [f"RV-{node_id}"],
            "skill_output_status": "complete",
            "fallback_used": "none",
            "gpt_verification_status": "verified",
        },
        "fact": f"{node_id} fact",
        "inference": f"{node_id} inference",
        "judgment": f"{node_id} judgment",
        "gap": "gap",
        "trigger": "trigger",
        "source_links": ["SRC-1"],
    }


if __name__ == "__main__":
    unittest.main()
