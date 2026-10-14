"""A bounded research follow-up anchored to one authored answer paragraph."""
from __future__ import annotations

from datetime import date
import re
from urllib.parse import urlsplit

from value_invest_research.domain.interactive_research import tree_version


MATERIAL_CLASSES = {"official_filing", "official_company", "sell_side_research",
                    "authoritative_third_party", "market_news", "expert_opinion", "other"}
EFFECTS = {"support", "refute", "boundary", "constraint", "unresolved", "conflict", "neutral", "new_branch"}


def _visible_text(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", value)
    return re.sub(r"\s+", " ", value.replace("**", "").replace("__", "")).strip()


def propose_passage_comment(tree: dict, request: dict) -> dict:
    if request.get("version") != tree_version(tree):
        raise ValueError("报告已更新，请重新选中段落后追问。")
    node_id = str(request.get("node_id", ""))
    node = next((n for n in tree["nodes"] if n["id"] == node_id), None)
    if not node or node["mode"] != "leaf" or node["level"] < 3:
        raise ValueError("请选中 L3–L5 问题关键论证中的一个段落。")
    section, paragraph = request.get("section"), request.get("paragraph")
    if not isinstance(section, int) or isinstance(section, bool) or not isinstance(paragraph, int) or isinstance(paragraph, bool):
        raise ValueError("段落定位无效，请重新选中。")
    try:
        original = node["analysis"][section]["paragraphs"][paragraph]
    except (IndexError, KeyError, TypeError):
        raise ValueError("段落已变化，请重新选中。") from None
    if section < 0 or paragraph < 0 or not isinstance(original, str) or not original.strip():
        raise ValueError("段落定位无效，请重新选中。")
    quote = re.sub(r"\s+", " ", str(request.get("quote", ""))).strip()
    if not 2 <= len(quote) <= 1200 or quote not in _visible_text(original):
        raise ValueError("选中文字与当前段落不一致，请重新选中。")
    question = str(request.get("comment", "")).strip()
    if not 2 <= len(question) <= 1000:
        raise ValueError("追问需为 2–1000 个字符。")
    return {"kind": "passage_comment", "tree": tree, "affected_ids": [node_id],
            "research_ids": [node_id], "rollup_ids": [], "removed_ids": [],
            "target": {"node_id": node_id, "section": section, "paragraph": paragraph,
                       "original": original, "quote": quote, "comment": question},
            "edit": {"operation": "passage_comment", "node_id": node_id, "question": node["question"],
                     "reason": question}}


def validate_passage_result(result: dict, *, original: str, as_of_date: str) -> dict:
    if not isinstance(result, dict) or result.get("status") not in {"ready", "insufficient", "needs_full_research"}:
        raise ValueError("局部研究结果格式无效。")
    if result["status"] != "ready":
        if not str(result.get("reason", "")).strip():
            raise ValueError("未更新原因不能为空。")
        return result
    replacement = result.get("replacement")
    if (not isinstance(replacement, str) or not 10 <= len(replacement.strip()) <= 12000
            or replacement == original or "\n\n" in replacement):
        raise ValueError("新段落为空、未变化或过长。")
    if any(token in replacement for token in ("本轮补充", "本报告此前", "我检索了")):
        raise ValueError("新段落应直接回答追问，不写研究过程。")
    sources = result.get("sources")
    if not isinstance(sources, list) or not 1 <= len(sources) <= 8:
        raise ValueError("局部更新至少需要一份可复核来源。")
    if not isinstance(result.get("search_queries"), list) or not result["search_queries"] or not all(isinstance(q, str) and q.strip() for q in result["search_queries"]):
        raise ValueError("缺少本轮检索记录。")
    if not str(result.get("refutation_result", "")).strip():
        raise ValueError("缺少反向检索结论。")
    markers = {int(n) for n in re.findall(r"\[(\d+)\]", replacement)}
    if markers != set(range(1, len(sources) + 1)):
        raise ValueError("新段落必须逐一引用本轮核查的来源。")
    cutoff = date.fromisoformat(as_of_date)
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("来源格式无效。")
        url = str(source.get("url", ""))
        parsed = urlsplit(url)
        if (parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username or parsed.password
                or any(ord(ch) < 32 for ch in url)):
            raise ValueError("来源必须是可公开访问的 HTTP(S) 原文链接。")
        published_text = str(source.get("published_at", ""))
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", published_text):
                raise ValueError
            published = date.fromisoformat(published_text)
        except ValueError:
            raise ValueError("来源须有可核查的完整发布日期。") from None
        if published > cutoff:
            raise ValueError("来源晚于研究截止日，不能用于当前报告。")
        for field in ("title", "publisher", "locator", "fact", "boundary", "review"):
            if not str(source.get(field, "")).strip():
                raise ValueError(f"来源缺少 {field}。")
        if source.get("material_class") not in MATERIAL_CLASSES or source.get("effect") not in EFFECTS:
            raise ValueError("来源分类或证据作用无效。")
    return result
