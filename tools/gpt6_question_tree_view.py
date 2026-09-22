"""Project-specific projection of existing research into the shared reading template.

No searches, ledger writes, answer changes, or sufficiency decisions happen here.
"""
from copy import deepcopy

# Editorial question relationships only; no new facts, evidence or gate decisions.
QUESTION_PURPOSES = {
    "Q1.1": "先确认实际可用能力与完成任务的成本变化，确定行业影响的起点。",
    "Q1.2": "检验能力改善能否转成客户付费，而不是把技术进步直接当作需求增长。",
    "Q1.4": "把任务增长与单位算力消耗、存量利用率联系起来，判断资源需求。",
    "Q1.3": "沿价值归属和盈利兑现两条线，判断需求能否变成供应商利润。",
    "Q1.1.2.1": "检验评测提升能否用于真实工作，为比较任务全成本提供能力边界。",
    "Q1.1.2.2": "比较可验收任务的总成本，识别模型溢价被效率收益抵消的条件。",
    "Q1.2.2.1": "建立任务量、单任务算力和硬件效率的关系，确定算力增长门槛。",
    "Q1.2.2.2": "检验用量变化是否已转成新增采购，区分机制可能性和实际订单。",
}


def build_question_tree_view(vm, qa, states, brief, extracts):
    syn = vm.project["synthesis"]
    leaf = {r["id"]: r for r in vm.qa_roots}
    rollups = {r["id"]: r for r in syn["nodes"]}
    initial = {q["id"]: q for q in brief["questions"]}
    extraction_by_pair = {(x["question_node_id"], x["source_id"]): x for x in extracts if "_leaf_" in x["extraction_id"]}
    nodes = []
    for q in qa["nodes"]:
        nid = q["id"]
        state = states[nid]
        child_ids = q.get("next_question_ids", [])
        row = leaf.get(nid) or rollups.get(nid) or {}
        analysis = deepcopy(row.get("analysis") or [{"heading": "子结论如何汇总", "paragraphs": row.get("paragraphs") or syn["root_paragraphs"]}])
        data = initial.get(nid, {}).get("data") or q.get("required_data") or ["直接子问题的结论、通过状态、反向证据和未闭环缺口"]
        question = q.get("display_question") or q["question"]
        node = dict(id=nid, parent_id=q.get("parent_id") or "", level=q["level"], question=question,
                    short=question, what=q["question"], data_required=data,
                    why_it_matters=q.get("why_it_matters") or QUESTION_PURPOSES.get(nid) or q.get("decision_use", ""),
                    acceptance_rule=("所有必要子问题充分回答，综合分析处理相互制约及实质缺口；有未通过的必要子节点，本层不得通过。" if child_ids else "核心事实可追溯，研究对象与期间口径可比，反向证据已处理；剩余缺口不实质改变本题答案。"),
                    mode="rollup" if child_ids else "leaf", conclusion=state["conclusion"], passed=state["passed"],
                    gaps=state["gaps"], was_expanded=nid in {"Q1.1.2", "Q1.2.2"}, analysis=analysis,
                    reasons=[row.get("gate_reason") or ("必要子结论与当前判断的边界已经明确。" if state["passed"] else "必要下层问题仍未充分回答，父节点继承其缺口。")],
                    next_actions=row.get("next_actions") or [syn["next_validation"]], evidence=[], refutation=row.get("refutation", ""), tables=[])
        for pair in row.get("evidence", []):
            x = extraction_by_pair[(nid, pair["source"])]
            node["evidence"].append({**pair, "trace": x["extraction_id"] + " · " + x["source_review_id"]})
        if row.get("scenario_table"):
            node["tables"].append({**row["scenario_table"], "caption": "机制情景 · 全部为假设，不是预测"})
        if nid == "Q1":
            node["analysis"].append({"heading": "研究边界与资料限制", "paragraphs": [syn["boundary"], syn["research_limit"]]})
            node["tables"].append({"headers": ["传导环节", "当前证据状态"], "rows": syn["causal_chain"], "caption": "能力到投资判断的传导链"})
        if nid == "Q1.3.1":
            node["analysis"].append({"heading": "观察对象，不作标的推荐", "paragraphs": [syn["target_boundary"], syn["next_validation"]]})
            node["tables"].append({"headers": ["观察对象／状态", "已验证的业务敞口", "升级判断前必须验证", "反向风险"], "rows": [
                [f"{t['company']} · {t['ticker']} / no_action", t["exposure"], t["needed"], t["risk"]] for t in vm.targets]})
        nodes.append(node)
    return dict(template_version="question-tree-v1", title=vm.project["title"], as_of_date=vm.project["as_of_date"],
                subtitle="左侧选择问题；非叶子查看子问题、核心结论与欠缺方向，叶子查看核心观点、关键论证与数据列表。",
                status_label=f"阶段性研究 · {sum(not n['passed'] and n['mode'] == 'leaf' for n in nodes)} 个终端问题仍有缺口", nodes=nodes, sources=vm.sources,
                source_note=vm.project.get("source_note") or "下列均为本轮实际打开并核读的来源。S04、S05 为评测作者原文；其他为官方资料或厂商刊载客户案例。事实、研究者推导与假设情景分别表述；来源链接会随网站更新，摘录、定位与逐题复核记录保存在项目审计文件中。",
                attachments=[{"label": "研究计划", "href": "research_plan.md"}, {"label": "完整 Markdown", "href": "professional_report.md"},
                             {"label": "来源登记", "href": "sources.jsonl"}, {"label": "复核记录", "href": "source_reviews.jsonl"}])
