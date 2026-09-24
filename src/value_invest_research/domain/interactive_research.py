"""Question edits and their research blast radius. No UI, files or providers."""
from copy import deepcopy
import hashlib
import json


def tree_version(tree: dict) -> str:
    return hashlib.sha256(json.dumps(tree, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def propose_edit(tree: dict, edit: dict) -> dict:
    """Stable IDs; a changed question invalidates descendants and ancestor rollups."""
    result = deepcopy(tree)
    nodes = {n["id"]: n for n in result["nodes"]}
    nid = edit.get("node_id")
    if nid not in nodes:
        raise ValueError("问题不存在，请刷新问题树。")
    operation = edit.get("operation", "edit")
    question = str(edit.get("question", "")).strip()
    reason = str(edit.get("reason", "")).strip()
    if operation not in {"edit", "add", "remove", "rerun"}:
        raise ValueError("不支持的编辑类型。")
    if operation in {"edit", "add"} and not 2 <= len(question) <= 500:
        raise ValueError("问题需为 2–500 个字符。")
    if len(reason) > 2000:
        raise ValueError("研究要求不能超过 2000 个字符。")
    if operation == "edit" and question == nodes[nid]["question"]:
        raise ValueError("问题未变化；如需补充材料，请选择重新研究。")

    def descendants(root):
        found = {root}
        while True:
            expanded = found | {n["id"] for n in nodes.values() if n.get("parent_id") in found}
            if found == expanded:
                return found
            found = expanded

    affected = descendants(nid)
    if operation == "add":
        if nodes[nid]["level"] == 1:
            raise ValueError("这一版支持在现有 L2 及以下新增子问题；新 L2 主题需连同 L3 计划设计后接入。")
        if nodes[nid]["level"] >= 5:
            raise ValueError("最多展开到 L5。")
        if nodes[nid]["level"] >= 3 and not reason:
            raise ValueError("继续下钻需要说明当前问题的具体证据缺口。")
        suffix = 1
        while f"{nid}.u{suffix}" in nodes:
            suffix += 1
        child_id = f"{nid}.u{suffix}"
        child = deepcopy(nodes[nid])
        child.update(id=child_id, parent_id=nid, level=nodes[nid]["level"] + 1,
                     question=question, short=question, what=question, mode="leaf",
                     why_it_matters=reason or "用户指定的补充研究角度。", evidence=[], tables=[])
        result["nodes"].append(child)
        nodes[child_id] = child
        affected.add(child_id)
    elif operation == "remove":
        if not nodes[nid].get("parent_id"):
            raise ValueError("不能删除元问题。")
        # Removing one angle changes the parent's coverage, including its remaining children.
        parent = nodes[nid]["parent_id"]
        removed = descendants(nid)
        affected = descendants(parent)
        result["nodes"] = [n for n in result["nodes"] if n["id"] not in removed]
    elif operation == "edit":
        nodes[nid].update(question=question, short=question, what=question)
    cursor = nodes[nid].get("parent_id")
    while cursor:
        affected.add(cursor)
        cursor = nodes[cursor].get("parent_id")
    current = {n["id"]: n for n in result["nodes"]}
    if any(n["level"] < 3 and not any(c.get("parent_id") == n["id"] for c in current.values()) for n in current.values()):
        raise ValueError("不能移除 L1/L2 的全部子问题；至少保留一条可执行的 L3 研究路径。")
    for node in current.values():
        children = [n for n in current.values() if n.get("parent_id") == node["id"]]
        node["mode"] = "rollup" if children else "leaf"
        if node["id"] in affected:
            node.update(passed=False, evidence=[], tables=[], refutation="",
                        conclusion="问题范围已变化，等待本轮研究；旧结论不作为当前答案。",
                        analysis=[{"heading": "等待重新验证", "paragraphs": ["按新问题重新取证、分析并检查充分性，之后逐层汇总。"]}],
                        gaps=["当前版本尚未完成逐题研究。"], reasons=["编辑使旧答案失效。"],
                        next_actions=[reason or "针对当前问题收集支持与反向材料。"])
    leaves = [n["id"] for n in current.values() if n["id"] in affected and n["mode"] == "leaf"]
    rollups = sorted((n["id"] for n in current.values() if n["id"] in affected and n["mode"] == "rollup"),
                     key=lambda i: -current[i]["level"])
    return {"tree": result, "affected_ids": sorted(affected), "research_ids": leaves,
            "rollup_ids": rollups, "removed_ids": sorted(set(nodes) - set(current)),
            "edit": {"node_id": nid, "operation": operation, "question": question, "reason": reason}}


def validate_researched_tree(before: dict, proposal: dict, after: dict) -> None:
    from value_invest_research.domain.question_tree_report import validate_question_tree_report
    issues = validate_question_tree_report(after)
    if issues:
        raise ValueError("报告结构检查失败：" + "; ".join(issues))
    expected = {n["id"]: n for n in proposal["tree"]["nodes"]}
    actual = {n["id"]: n for n in after["nodes"]}
    if set(expected) != set(actual):
        raise ValueError("研究器不能擅自增删问题；新缺口需在下一轮确认下钻。")
    if before.get("as_of_date") != after.get("as_of_date"):
        raise ValueError("研究截面不可随编辑改变。")
    prior = {n["id"]: n for n in before["nodes"]}
    for nid, node in actual.items():
        if any(node.get(k) != expected[nid].get(k) for k in ("question", "parent_id", "level")):
            raise ValueError(f"{nid} 不符合已确认的问题范围。")
        if nid not in proposal["affected_ids"] and node != prior[nid]:
            raise ValueError(f"无关问题 {nid} 被修改。")
        if nid in proposal["affected_ids"] and node["conclusion"] == expected[nid]["conclusion"]:
            raise ValueError(f"{nid} 尚未产生本轮分析。")


def validate_research_state(state: dict, tree: dict, revision_id: str) -> None:
    """The skill's state snapshot must not become a second, contradictory answer."""
    if not isinstance(state, dict) or state.get("revision_id") != revision_id:
        raise ValueError("研究状态的版本与本轮不一致。")
    expected = {n["id"]: n for n in tree["nodes"]}
    nodes = state.get("nodes")
    if (not isinstance(nodes, list) or any(not isinstance(n, dict) for n in nodes)
            or len(nodes) != len(expected)
            or {n.get("question_id") for n in nodes} != set(expected)):
        raise ValueError("研究状态的节点覆盖与问题树不一致。")
    if state.get("current_node_id") not in expected:
        raise ValueError("研究状态的当前节点不存在。")
    if not all(n["passed"] for n in expected.values()) and state.get("research_status") != "partial_research":
        raise ValueError("研究状态不能将未充分的问题树标记为完成。")
    for node in nodes:
        question = expected[node["question_id"]]
        if any(node.get(k) != question.get(k) for k in ("parent_id", "level", "question", "conclusion")):
            raise ValueError(f"{question['id']} 的研究状态与问题树不一致。")
        sufficiency = node.get("sufficiency")
        if (not isinstance(sufficiency, dict) or sufficiency.get("passed") is not question["passed"]
                or sufficiency.get("gaps") != question.get("gaps", [])):
            raise ValueError(f"{question['id']} 的研究充分性与问题树不一致。")
        statuses = {"answered"} if question["passed"] else {"pending", "researching", "expanded", "blocked"}
        if node.get("status") not in statuses:
            raise ValueError(f"{question['id']} 的节点状态与充分性不一致。")
