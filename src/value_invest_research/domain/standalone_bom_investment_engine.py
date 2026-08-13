from __future__ import annotations

from datetime import date
import hashlib
from typing import Any, Iterable

from value_invest_research.domain.standalone_bom_timeline import (
    STANDALONE_LENSES,
    build_standalone_timeline_view,
)


LOGIC_STATES = (
    "unresolved",
    "weak",
    "strengthening",
    "confirmed",
    "weakening",
    "refuted",
)
MAPPING_DIRECTIONS = (
    "support",
    "refute",
    "boundary",
    "constraint",
    "new_branch",
    "conflict",
    "unresolved",
    "neutral",
    "unmapped",
)
MAPPING_ROLES = ("primary", "secondary")
NODE_FITS = ("direct", "proxy", "contextual", "unmapped")
RULE_MATCHES = ("support_rule", "refute_rule", "neither")
PRESENTATION_ROLES = ("causal_node", "derived_view")
EVIDENCE_NATURES = ("fact", "forecast", "opinion", "lead")
NOVELTY_LEVELS = ("new", "confirming", "repeated")
MATERIALITY_LEVELS = ("thesis_change", "high", "medium", "low")
EXPECTATION_DELTAS = ("positive", "negative", "neutral", "unknown")
ENTITY_INVESTMENT_EFFECTS = ("positive", "negative", "mixed", "unclear")
ACTION_STATES = ("actionable_long", "watch_only", "no_action")
REQUIRED_ACTIONABLE_GATES = (
    "logic_coverage",
    "company_financial_bridge",
    "valuation",
    "refutation",
    "risk_control",
)
GATE_PUBLIC_NAMES = {
    "logic_coverage": "逻辑覆盖",
    "company_financial_bridge": "公司财务桥",
    "valuation": "估值",
    "refutation": "反证",
    "risk_control": "风险控制",
}
ACTION_PUBLIC_NAMES = {
    "actionable_long": "可行动观察",
    "watch_only": "观察",
    "no_action": "不行动",
}


def validate_standalone_bom_playbook(profile: dict[str, Any]) -> dict[str, Any]:
    """Validate a structured five-lens BOM playbook and return lookup indexes."""

    research_model = str(profile.get("research_model") or "").strip()
    logic_chain_centered = research_model == "logic_chain_centered"
    if logic_chain_centered and not str(
        profile.get("logic_chain_version") or ""
    ).strip():
        raise ValueError(
            "logic_chain_centered playbooks require logic_chain_version"
        )

    expected_lenses = [lens_id for lens_id, _ in STANDALONE_LENSES]
    profile_lenses = [
        row for row in profile.get("lenses") or [] if isinstance(row, dict)
    ]
    actual_lenses = [str(row.get("lens_id") or "") for row in profile_lenses]
    if actual_lenses != expected_lenses:
        raise ValueError(
            "Standalone BOM playbook must define the five lenses in canonical order"
        )

    nodes: dict[str, dict[str, Any]] = {}
    lens_nodes: dict[str, list[dict[str, Any]]] = {}
    public_lens_nodes: dict[str, list[dict[str, Any]]] = {}
    for lens in profile_lenses:
        lens_id = str(lens.get("lens_id") or "")
        if logic_chain_centered and not str(lens.get("logic_chain") or "").strip():
            raise ValueError(f"{lens_id} requires a first-principles logic_chain")
        logic_nodes = [
            row for row in lens.get("logic_nodes") or [] if isinstance(row, dict)
        ]
        if not logic_nodes:
            raise ValueError(f"{lens_id} must define structured logic_nodes")
        lens_nodes[lens_id] = logic_nodes
        for node in logic_nodes:
            node_id = str(node.get("logic_node_id") or "").strip()
            if not node_id or not node_id.startswith(f"{lens_id}."):
                raise ValueError(
                    f"logic_node_id={node_id!r} must be namespaced by {lens_id}"
                )
            if node_id in nodes:
                raise ValueError(f"Duplicate logic_node_id={node_id}")
            for field in ("title", "question", "support_rule", "refute_rule"):
                if not str(node.get(field) or "").strip():
                    raise ValueError(f"{node_id} requires {field}")
            render_mode = str(node.get("render_mode") or "").strip()
            presentation_role = str(
                node.get("presentation_role")
                or ("derived_view" if render_mode else "causal_node")
            ).strip()
            if presentation_role not in PRESENTATION_ROLES:
                raise ValueError(
                    f"{node_id} uses unsupported presentation_role="
                    f"{presentation_role!r}"
                )
            if render_mode and presentation_role != "derived_view":
                raise ValueError(
                    f"{node_id} render_mode requires presentation_role=derived_view"
                )
            if render_mode:
                if render_mode not in (
                    "demand_party_list",
                    "demand_quantity_matrix",
                ):
                    raise ValueError(
                        f"{node_id} uses unsupported render_mode={render_mode!r}"
                    )
                if lens_id != "demand":
                    raise ValueError(
                        f"{render_mode} is only valid for a demand logic node"
                    )
                if render_mode == "demand_party_list":
                    demand_parties = node.get("demand_parties")
                    if not isinstance(demand_parties, dict):
                        raise ValueError(f"{node_id} requires demand_parties")
                    if list(demand_parties) != ["current", "potential_future"]:
                        raise ValueError(
                            f"{node_id} demand_parties must use current then "
                            "potential_future"
                        )
                    for group_id in ("current", "potential_future"):
                        parties = demand_parties.get(group_id)
                        if not isinstance(parties, list) or not parties:
                            raise ValueError(
                                f"{node_id} demand_parties.{group_id} must be non-empty"
                            )
                        if any(not str(party).strip() for party in parties):
                            raise ValueError(
                                f"{node_id} demand_parties.{group_id} has empty party"
                            )
                if render_mode == "demand_quantity_matrix" and not str(
                    node.get("classification_node_id") or ""
                ).strip():
                    raise ValueError(
                        f"{node_id} requires classification_node_id"
                    )
            nodes[node_id] = {
                **node,
                "lens_id": lens_id,
                "presentation_role": presentation_role,
            }

        if logic_chain_centered and not any(
            str(nodes[str(node.get("logic_node_id") or "")].get("presentation_role"))
            == "causal_node"
            for node in logic_nodes
        ):
            raise ValueError(f"{lens_id} requires at least one causal node")

    for node_id, node in nodes.items():
        if str(node.get("render_mode") or "") == "demand_quantity_matrix":
            classification_node_id = str(
                node.get("classification_node_id") or ""
            )
            classification_node = nodes.get(classification_node_id)
            if not classification_node or str(
                classification_node.get("render_mode") or ""
            ) != "demand_party_list":
                raise ValueError(
                    f"{node_id} must reference a demand_party_list classification node"
                )
        for downstream_id in node.get("downstream_node_ids") or []:
            if str(downstream_id) not in nodes:
                raise ValueError(
                    f"{node_id} references unknown downstream node={downstream_id}"
                )
    for lens_id, logic_nodes in lens_nodes.items():
        lens = next(row for row in profile_lenses if row["lens_id"] == lens_id)
        public_node_ids = lens.get("public_logic_node_ids")
        if public_node_ids is None:
            public_lens_nodes[lens_id] = logic_nodes
            continue
        if not isinstance(public_node_ids, list) or not public_node_ids:
            raise ValueError(
                f"{lens_id} public_logic_node_ids must be a non-empty list"
            )
        normalized_public_ids = [str(node_id).strip() for node_id in public_node_ids]
        if any(not node_id for node_id in normalized_public_ids):
            raise ValueError(
                f"{lens_id} public_logic_node_ids cannot contain empty node IDs"
            )
        if len(normalized_public_ids) != len(set(normalized_public_ids)):
            raise ValueError(
                f"{lens_id} public_logic_node_ids cannot contain duplicates"
            )
        logic_node_ids = [str(node["logic_node_id"]) for node in logic_nodes]
        unknown_ids = [
            node_id
            for node_id in normalized_public_ids
            if node_id not in logic_node_ids
        ]
        if unknown_ids:
            raise ValueError(
                f"{lens_id} public_logic_node_ids references unknown nodes={unknown_ids}"
            )
        public_id_set = set(normalized_public_ids)
        canonical_public_ids = [
            node_id for node_id in logic_node_ids if node_id in public_id_set
        ]
        if normalized_public_ids != canonical_public_ids:
            raise ValueError(
                f"{lens_id} public_logic_node_ids must preserve logic-node order"
            )
        for node_id in normalized_public_ids:
            node = nodes[node_id]
            if str(node.get("render_mode") or "") != "demand_quantity_matrix":
                continue
            classification_node_id = str(node.get("classification_node_id") or "")
            if classification_node_id not in normalized_public_ids:
                raise ValueError(
                    f"{node_id} public rendering requires classification node="
                    f"{classification_node_id}"
                )
        public_lens_nodes[lens_id] = [
            nodes[node_id] for node_id in normalized_public_ids
        ]
        if logic_chain_centered:
            public_causal_ids = {
                str(node["logic_node_id"])
                for node in public_lens_nodes[lens_id]
                if str(node.get("presentation_role") or "") == "causal_node"
            }
            all_causal_ids = {
                str(node["logic_node_id"])
                for node in logic_nodes
                if str(nodes[str(node["logic_node_id"])].get("presentation_role") or "")
                == "causal_node"
            }
            if public_causal_ids != all_causal_ids:
                raise ValueError(
                    f"{lens_id} public rendering must preserve all causal nodes"
                )
    return {
        "lenses": {str(row["lens_id"]): row for row in profile_lenses},
        "nodes": nodes,
        "lens_nodes": lens_nodes,
        "public_lens_nodes": public_lens_nodes,
    }


def normalize_claim_mapping(
    raw: dict[str, Any],
    *,
    claims_by_id: dict[str, dict[str, Any]],
    profile: dict[str, Any],
    mapped_at: str,
) -> dict[str, Any]:
    index = validate_standalone_bom_playbook(profile)
    claim_id = str(raw.get("claim_id") or "").strip()
    claim = claims_by_id.get(claim_id)
    if claim is None:
        raise ValueError(f"Unknown claim_id={claim_id!r}")
    logic_node_id = str(raw.get("logic_node_id") or "").strip()
    node = index["nodes"].get(logic_node_id)
    if node is None:
        raise ValueError(f"Unknown logic_node_id={logic_node_id!r}")
    role = _choice(raw, "mapping_role", MAPPING_ROLES, "primary")
    if role == "primary" and str(claim.get("lens_id") or "") != node["lens_id"]:
        raise ValueError(
            f"Primary mapping lens mismatch for claim={claim_id}, node={logic_node_id}"
        )
    direction = _choice(raw, "direction", MAPPING_DIRECTIONS, "neutral")
    evidence_nature = _choice(
        raw, "evidence_nature", EVIDENCE_NATURES, "opinion"
    )
    directness = _choice(raw, "directness", ("direct", "indirect"), "indirect")
    node_fit = _choice(
        raw,
        "node_fit",
        NODE_FITS,
        (
            "unmapped"
            if direction == "unmapped"
            else "direct"
            if direction in ("support", "refute")
            else "proxy"
        ),
    )
    rule_match = _choice(
        raw,
        "rule_match",
        RULE_MATCHES,
        (
            "support_rule"
            if direction == "support"
            else "refute_rule"
            if direction == "refute"
            else "neither"
        ),
    )
    novelty = _choice(raw, "novelty", NOVELTY_LEVELS, "new")
    materiality = _choice(raw, "materiality", MATERIALITY_LEVELS, "medium")
    expectation_delta = _choice(
        raw, "expectation_delta", EXPECTATION_DELTAS, "unknown"
    )
    rationale = str(raw.get("rationale") or "").strip()
    if not rationale:
        raise ValueError("Claim mappings require a question-specific rationale")
    normalized_mapped_at = _require_date(
        str(raw.get("mapped_at") or mapped_at), "mapped_at"
    )
    presentation_role = str(node.get("presentation_role") or "causal_node")
    strict_from = str(profile.get("strict_mapping_effects_from") or "").strip()
    strict_effects = not strict_from or normalized_mapped_at >= strict_from
    if presentation_role == "causal_node" and strict_effects:
        if direction == "support" and (
            node_fit != "direct"
            or rule_match != "support_rule"
            or directness != "direct"
        ):
            raise ValueError(
                "Causal support mappings require direct node fit, directness, "
                "and an explicit support_rule match"
            )
        if direction == "refute" and (
            node_fit != "direct"
            or rule_match != "refute_rule"
            or directness != "direct"
        ):
            raise ValueError(
                "Causal refute mappings require direct node fit, directness, "
                "and an explicit refute_rule match"
            )
        if direction not in ("support", "refute") and rule_match != "neither":
            raise ValueError(
                "Boundary, constraint, lead, unresolved, new-branch, conflict, "
                "and unmapped relations must not claim a support/refute rule match"
            )
        if direction == "unmapped" and node_fit != "unmapped":
            raise ValueError("Unmapped relations require node_fit=unmapped")
        if direction != "unmapped" and node_fit == "unmapped":
            raise ValueError("Only unmapped relations may use node_fit=unmapped")
    mapping_id = str(raw.get("mapping_id") or "").strip() or _mapping_id(
        claim_id, logic_node_id
    )
    raw_entities = raw.get("entities") or []
    if not raw_entities and raw.get("entity"):
        raw_entities = [raw.get("entity")]
    entities = _unique_strings(raw_entities)
    if not entities:
        entities = ["行业 / 多主体"]
    return {
        "mapping_id": mapping_id,
        "claim_id": claim_id,
        "source_id": str(claim.get("source_id") or ""),
        "logic_node_id": logic_node_id,
        "mapping_role": role,
        "direction": direction,
        "node_fit": node_fit,
        "rule_match": rule_match,
        "evidence_nature": evidence_nature,
        "directness": directness,
        "novelty": novelty,
        "materiality": materiality,
        "rationale": rationale,
        "entity": entities[0],
        "entities": entities,
        "metric_id": str(raw.get("metric_id") or "").strip(),
        "expectation_delta": expectation_delta,
        "downstream_impacts": _unique_strings(
            raw.get("downstream_impacts") or []
        ),
        "supersedes_mapping_id": str(
            raw.get("supersedes_mapping_id") or ""
        ).strip(),
        "mapped_at": normalized_mapped_at,
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def _active_claim_mappings(
    mappings: Iterable[dict[str, Any]], *, as_of_date: str
) -> list[dict[str, Any]]:
    """Resolve append-only mapping corrections reproducibly for one cutoff."""

    visible = sorted(
        (
            dict(row)
            for row in mappings
            if str(row.get("mapped_at") or "") <= as_of_date
        ),
        key=lambda row: (
            str(row.get("mapped_at") or ""),
            str(row.get("mapping_id") or ""),
        ),
    )
    active: dict[str, dict[str, Any]] = {}
    for row in visible:
        superseded_id = str(row.get("supersedes_mapping_id") or "").strip()
        if superseded_id:
            active.pop(superseded_id, None)
        active[str(row.get("mapping_id") or "")] = row
    return list(active.values())


def normalize_entity_state(
    raw: dict[str, Any],
    *,
    profile: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    """Normalize one company/entity snapshot inside a logic node."""

    index = validate_standalone_bom_playbook(profile)
    logic_node_id = str(raw.get("logic_node_id") or "").strip()
    if logic_node_id not in index["nodes"]:
        raise ValueError(f"Unknown logic_node_id={logic_node_id!r}")
    entity_name = str(
        raw.get("entity_name") or raw.get("entity") or ""
    ).strip()
    if not entity_name:
        raise ValueError("Entity states require entity_name")
    assessment = str(raw.get("assessment") or "").strip()
    if not assessment:
        raise ValueError("Entity states require assessment")
    support_claim_ids = _verified_claim_ids(
        raw.get("support_claim_ids") or [], claims_by_id
    )
    refute_claim_ids = _verified_claim_ids(
        raw.get("refute_claim_ids") or [], claims_by_id
    )
    if set(support_claim_ids) & set(refute_claim_ids):
        raise ValueError(
            "One claim cannot support and refute the same entity state"
        )
    return {
        "logic_node_id": logic_node_id,
        "entity_id": str(raw.get("entity_id") or "").strip()
        or _entity_id(entity_name),
        "entity_name": entity_name,
        "as_of_date": _require_date(
            str(raw.get("as_of_date") or as_of_date), "as_of_date"
        ),
        "assessment": assessment,
        "change_summary": str(raw.get("change_summary") or "").strip()
        or "当前为该实体的首个结构化截面。",
        "investment_effect": _choice(
            raw,
            "investment_effect",
            ENTITY_INVESTMENT_EFFECTS,
            "unclear",
        ),
        "support_claim_ids": support_claim_ids,
        "refute_claim_ids": refute_claim_ids,
        "evidence_gaps": _unique_strings(raw.get("evidence_gaps") or []),
        "next_validation": str(raw.get("next_validation") or "").strip(),
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def normalize_logic_state(
    raw: dict[str, Any],
    *,
    profile: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    index = validate_standalone_bom_playbook(profile)
    logic_node_id = str(raw.get("logic_node_id") or "").strip()
    if logic_node_id not in index["nodes"]:
        raise ValueError(f"Unknown logic_node_id={logic_node_id!r}")
    conclusion = str(raw.get("conclusion") or "").strip()
    if not conclusion:
        raise ValueError("Logic states require conclusion")
    support_claim_ids = _verified_claim_ids(
        raw.get("support_claim_ids") or [], claims_by_id
    )
    refute_claim_ids = _verified_claim_ids(
        raw.get("refute_claim_ids") or [], claims_by_id
    )
    if set(support_claim_ids) & set(refute_claim_ids):
        raise ValueError("One claim cannot support and refute the same logic state")
    node = index["nodes"][logic_node_id]
    return {
        "logic_node_id": logic_node_id,
        "as_of_date": _require_date(
            str(raw.get("as_of_date") or as_of_date), "as_of_date"
        ),
        "state": _choice(raw, "state", LOGIC_STATES, "unresolved"),
        "conclusion": conclusion,
        "previous_state": _optional_choice(
            raw, "previous_state", LOGIC_STATES
        ),
        "change_summary": str(raw.get("change_summary") or "").strip(),
        "support_claim_ids": support_claim_ids,
        "refute_claim_ids": refute_claim_ids,
        "key_metrics": [
            row for row in raw.get("key_metrics") or [] if isinstance(row, dict)
        ],
        "demand_quantity_rows": _normalize_demand_quantity_rows(
            raw.get("demand_quantity_rows") or [],
            node=node,
            index=index,
            claims_by_id=claims_by_id,
        ),
        "evidence_gaps": _unique_strings(raw.get("evidence_gaps") or []),
        "next_validation": str(raw.get("next_validation") or "").strip(),
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def _normalize_demand_quantity_rows(
    raw_rows: Iterable[dict[str, Any]],
    *,
    node: dict[str, Any],
    index: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if str(node.get("render_mode") or "") != "demand_quantity_matrix":
        return []
    raw_rows = list(raw_rows)
    if not raw_rows:
        return []
    classification_node = index["nodes"][
        str(node.get("classification_node_id") or "")
    ]
    current_parties = [
        str(party).strip()
        for party in dict(classification_node.get("demand_parties") or {}).get(
            "current"
        )
        or []
    ]
    potential_future_parties = [
        str(party).strip()
        for party in dict(classification_node.get("demand_parties") or {}).get(
            "potential_future"
        )
        or []
    ]
    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            continue
        forecast_group = _choice(
            raw,
            "forecast_group",
            ("classified", "potential_future", "other"),
            "classified",
        )
        demand_party = str(raw.get("demand_party") or "").strip()
        if forecast_group == "classified" and demand_party not in current_parties:
            raise ValueError(
                "Classified demand quantity rows must use a current Q1 demander"
            )
        if (
            forecast_group == "potential_future"
            and demand_party not in potential_future_parties
        ):
            raise ValueError(
                "Potential-future demand quantity rows must use a potential Q1 demander"
            )
        if forecast_group == "other" and demand_party:
            raise ValueError("Other forecasts must not claim a Q1 demander mapping")
        metric = str(raw.get("metric") or "").strip()
        quantity = str(raw.get("quantity") or "").strip()
        target_period = str(raw.get("target_period") or "").strip()
        caveat = str(raw.get("caveat") or "").strip()
        if not metric or not quantity or not target_period or not caveat:
            raise ValueError(
                "Demand quantity rows require metric, quantity, target_period, and caveat"
            )
        mapping_quality = _choice(
            raw,
            "mapping_quality",
            ("direct", "proxy", "sample", "gap", "unmapped"),
            "proxy",
        )
        claim_ids = _verified_claim_ids(
            raw.get("claim_ids") or [], claims_by_id
        )
        if mapping_quality not in ("gap", "unmapped") and not claim_ids:
            raise ValueError(
                "Non-gap demand quantity rows require at least one verified claim"
            )
        rows.append(
            {
                "forecast_group": forecast_group,
                "demand_party": demand_party,
                "metric": metric,
                "quantity": quantity,
                "target_period": target_period,
                "mapping_quality": mapping_quality,
                "claim_ids": claim_ids,
                "caveat": caveat,
            }
        )
    covered_parties = {
        str(row.get("demand_party") or "")
        for row in rows
        if row.get("forecast_group") == "classified"
    }
    if covered_parties != set(current_parties):
        raise ValueError(
            "Classified demand quantity rows must cover every current Q1 demander"
        )
    if not any(row.get("forecast_group") == "other" for row in rows):
        raise ValueError("Demand quantity matrix requires at least one other forecast")
    return rows


def normalize_thesis_revision(
    raw: dict[str, Any],
    *,
    profile: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    index = validate_standalone_bom_playbook(profile)
    logic_node_id = str(raw.get("logic_node_id") or "").strip()
    if logic_node_id not in index["nodes"]:
        raise ValueError(f"Unknown logic_node_id={logic_node_id!r}")
    revision_type = _choice(raw, "revision_type", ("baseline", "change"), "baseline")
    previous_state = _optional_choice(raw, "previous_state", LOGIC_STATES)
    if revision_type == "change" and not previous_state:
        raise ValueError("A change revision requires previous_state")
    new_state = _choice(raw, "new_state", LOGIC_STATES, "unresolved")
    trigger_claim_ids = _verified_claim_ids(
        raw.get("trigger_claim_ids") or [], claims_by_id
    )
    conflicting_claim_ids = _verified_claim_ids(
        raw.get("conflicting_claim_ids") or [], claims_by_id
    )
    rationale = str(raw.get("rationale") or "").strip()
    if not rationale:
        raise ValueError("Thesis revisions require rationale")
    revision_date = _require_date(
        str(raw.get("as_of_date") or as_of_date), "as_of_date"
    )
    revision_id = str(raw.get("revision_id") or "").strip() or _revision_id(
        logic_node_id, revision_date
    )
    return {
        "revision_id": revision_id,
        "revision_type": revision_type,
        "logic_node_id": logic_node_id,
        "as_of_date": revision_date,
        "previous_state": previous_state,
        "new_state": new_state,
        "change_direction": _choice(
            raw,
            "change_direction",
            ("up", "down", "unchanged"),
            "unchanged",
        ),
        "magnitude": _choice(
            raw, "magnitude", ("high", "medium", "low"), "low"
        ),
        "rationale": rationale,
        "trigger_claim_ids": trigger_claim_ids,
        "conflicting_claim_ids": conflicting_claim_ids,
        "downstream_impacts": _unique_strings(
            raw.get("downstream_impacts") or []
        ),
        "next_validation": str(raw.get("next_validation") or "").strip(),
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def normalize_investment_snapshot(
    raw: dict[str, Any],
    *,
    profile: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    index = validate_standalone_bom_playbook(profile)
    action_state = _choice(
        raw, "action_state", ACTION_STATES, "watch_only"
    )
    gate_results = {
        gate: bool((raw.get("gate_results") or {}).get(gate, False))
        for gate in REQUIRED_ACTIONABLE_GATES
    }
    kill_tests = [
        {
            "metric": str(row.get("metric") or "").strip(),
            "threshold": str(row.get("threshold") or "").strip(),
            "cadence": str(row.get("cadence") or "").strip(),
            "downgrade_action": str(
                row.get("downgrade_action") or ""
            ).strip(),
        }
        for row in raw.get("kill_tests") or []
        if isinstance(row, dict)
    ]
    valid_kill_tests = [
        row for row in kill_tests if all(str(value).strip() for value in row.values())
    ]
    if action_state == "actionable_long":
        failed = [gate for gate, passed in gate_results.items() if not passed]
        if failed or not valid_kill_tests:
            raise ValueError(
                "actionable_long requires all semantic gates and quantitative kill tests"
            )
    positive_node_ids = _verified_node_ids(
        raw.get("positive_node_ids") or [], index["nodes"]
    )
    negative_node_ids = _verified_node_ids(
        raw.get("negative_node_ids") or [], index["nodes"]
    )
    company_impacts = [
        _normalize_company_impact(row, claims_by_id)
        for row in raw.get("company_impacts") or []
        if isinstance(row, dict)
    ]
    summary = str(raw.get("summary") or "").strip()
    if not summary:
        raise ValueError("Investment snapshots require summary")
    return {
        "as_of_date": _require_date(
            str(raw.get("as_of_date") or as_of_date), "as_of_date"
        ),
        "action_state": action_state,
        "summary": summary,
        "fundamental_delta": str(raw.get("fundamental_delta") or "").strip(),
        "consensus_delta": str(raw.get("consensus_delta") or "").strip(),
        "priced_in_delta": str(raw.get("priced_in_delta") or "").strip(),
        "positive_node_ids": positive_node_ids,
        "negative_node_ids": negative_node_ids,
        "company_impacts": company_impacts,
        "gate_results": gate_results,
        "kill_tests": valid_kill_tests,
        "next_catalysts": _unique_strings(raw.get("next_catalysts") or []),
        "review_status": str(
            raw.get("review_status") or "gpt_verified"
        ).strip(),
    }


def build_standalone_investment_view(
    *,
    project: dict[str, Any],
    profile: dict[str, Any],
    claims: Iterable[dict[str, Any]],
    conclusions: Iterable[dict[str, Any]],
    claim_mappings: Iterable[dict[str, Any]],
    logic_states: Iterable[dict[str, Any]],
    entity_states: Iterable[dict[str, Any]],
    thesis_revisions: Iterable[dict[str, Any]],
    investment_snapshots: Iterable[dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    """Assemble one reproducible five-lens investment snapshot."""

    base = build_standalone_timeline_view(
        project=project,
        profile=profile,
        claims=claims,
        conclusions=conclusions,
        as_of_date=as_of_date,
    )
    if not _profile_has_logic_nodes(profile):
        return base
    index = validate_standalone_bom_playbook(profile)
    mappings = _active_claim_mappings(claim_mappings, as_of_date=as_of_date)
    mappings_by_claim: dict[str, list[dict[str, Any]]] = {}
    for mapping in mappings:
        mappings_by_claim.setdefault(str(mapping.get("claim_id") or ""), []).append(
            mapping
        )
    state_rows = [
        dict(row)
        for row in logic_states
        if str(row.get("as_of_date") or "") <= as_of_date
    ]
    entity_state_rows = [
        dict(row)
        for row in entity_states
        if str(row.get("as_of_date") or "") <= as_of_date
    ]
    revisions = [
        dict(row)
        for row in thesis_revisions
        if str(row.get("as_of_date") or "") <= as_of_date
    ]
    snapshots = sorted(
        (
            dict(row)
            for row in investment_snapshots
            if str(row.get("as_of_date") or "") <= as_of_date
        ),
        key=lambda row: str(row.get("as_of_date") or ""),
        reverse=True,
    )

    for lens in base["lenses"]:
        for claim in lens["claims"]:
            claim["logic_mappings"] = [
                {
                    **mapping,
                    "logic_node_title": str(
                        index["nodes"]
                        .get(str(mapping.get("logic_node_id") or ""), {})
                        .get("title")
                        or mapping.get("logic_node_id")
                        or ""
                    ),
                }
                for mapping in mappings_by_claim.get(str(claim.get("claim_id") or ""), [])
            ]
            claim["logic_mappings"].sort(
                key=lambda mapping: (
                    0
                    if str(mapping.get("mapping_role") or "primary") == "primary"
                    else 1,
                    str(mapping.get("logic_node_id") or ""),
                )
            )
    claims_by_id = {
        str(claim.get("claim_id") or ""): claim
        for lens in base["lenses"]
        for claim in lens["claims"]
        if str(claim.get("claim_id") or "")
    }
    for lens in base["lenses"]:
        lens_id = str(lens["lens_id"])
        lens["logic_nodes"] = [
            _build_logic_node_view(
                node=node,
                nodes_by_id=index["nodes"],
                state_rows=state_rows,
                entity_state_rows=entity_state_rows,
                revisions=revisions,
                mappings=mappings,
                claims_by_id=claims_by_id,
            )
            for node in index["public_lens_nodes"][lens_id]
        ]
        lens["causal_nodes"] = [
            node
            for node in lens["logic_nodes"]
            if str(node.get("presentation_role") or "causal_node")
            == "causal_node"
        ]
        lens["derived_views"] = [
            node
            for node in lens["logic_nodes"]
            if str(node.get("presentation_role") or "") == "derived_view"
        ]

    base["investment_engine_version"] = str(
        profile.get("schema_version") or "2.0"
    )
    base["research_model"] = str(profile.get("research_model") or "")
    base["logic_chain_version"] = str(
        profile.get("logic_chain_version") or ""
    )
    base["decision"] = snapshots[0] if snapshots else {
        "as_of_date": as_of_date,
        "action_state": "watch_only",
        "summary": "逻辑节点已建立，但尚未形成经过门槛验证的投资快照。",
        "fundamental_delta": "待验证",
        "consensus_delta": "待验证",
        "priced_in_delta": "待验证",
        "company_impacts": [],
        "gate_results": {
            gate: False for gate in REQUIRED_ACTIONABLE_GATES
        },
        "kill_tests": [],
        "next_catalysts": [],
    }
    if base["research_model"] == "logic_chain_centered":
        base["logic_chain_judgment"] = _build_logic_chain_judgment(
            decision=base["decision"],
            nodes_by_id=index["nodes"],
        )
    base["engine_coverage"] = {
        "logic_nodes": len(index["nodes"]),
        "public_logic_nodes": sum(
            len(rows) for rows in index["public_lens_nodes"].values()
        ),
        "mapped_claims": len(
            {
                str(mapping.get("claim_id") or "")
                for mapping in mappings
                if str(mapping.get("direction") or "") != "unmapped"
            }
        ),
        "unmapped_relations": sum(
            str(mapping.get("direction") or "") == "unmapped"
            for mapping in mappings
        ),
        "total_claims": sum(len(lens["claims"]) for lens in base["lenses"]),
        "state_nodes": len(
            {
                str(row.get("logic_node_id") or "")
                for row in state_rows
                if str(row.get("logic_node_id") or "")
            }
        ),
        "entity_states": len(
            {
                (
                    str(row.get("logic_node_id") or ""),
                    str(row.get("entity_id") or ""),
                )
                for row in entity_state_rows
                if str(row.get("logic_node_id") or "")
                and str(row.get("entity_id") or "")
            }
        ),
    }
    return base


def _build_logic_chain_judgment(
    *,
    decision: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
) -> str:
    """Roll node effects and failed gates into one evidence-bounded judgment."""

    def causal_titles(node_ids: Iterable[Any]) -> list[str]:
        titles: list[str] = []
        for raw_node_id in node_ids:
            node_id = str(raw_node_id or "")
            node = nodes_by_id.get(node_id) or {}
            if str(node.get("presentation_role") or "causal_node") != "causal_node":
                continue
            title = str(node.get("title") or node_id).strip()
            if title and title not in titles:
                titles.append(title)
        return titles

    positive_titles = causal_titles(decision.get("positive_node_ids") or [])
    negative_titles = causal_titles(decision.get("negative_node_ids") or [])
    failed_gates = [
        GATE_PUBLIC_NAMES.get(gate, gate)
        for gate, passed in (decision.get("gate_results") or {}).items()
        if not bool(passed)
    ]
    action_state = str(decision.get("action_state") or "watch_only")
    action_label = ACTION_PUBLIC_NAMES.get(action_state, action_state)

    parts = []
    if positive_titles:
        parts.append(f"逻辑链当前相对增强的环节是：{'、'.join(positive_titles)}")
    if negative_titles:
        parts.append(f"主要断点或约束环节是：{'、'.join(negative_titles)}")
    if not parts:
        parts.append("现有节点证据尚未形成可区分的增强与削弱环节")
    if failed_gates:
        parts.append(
            f"由于{'、'.join(failed_gates)}尚未通过，当前投资动作维持{action_label}"
        )
    else:
        parts.append(f"全部语义门槛已通过，当前投资动作是{action_label}")
    return "；".join(parts) + "。"


def validate_standalone_bom_investment_bundle(
    *,
    project: dict[str, Any],
    profile: dict[str, Any],
    claims: Iterable[dict[str, Any]],
    claim_mappings: Iterable[dict[str, Any]],
    logic_states: Iterable[dict[str, Any]],
    entity_states: Iterable[dict[str, Any]],
    thesis_revisions: Iterable[dict[str, Any]],
    investment_snapshots: Iterable[dict[str, Any]],
    as_of_date: str,
) -> dict[str, Any]:
    """Run cross-ledger semantic checks for one standalone BOM snapshot."""

    issues: list[dict[str, str]] = []
    try:
        index = validate_standalone_bom_playbook(profile)
    except ValueError as exc:
        return {
            "ok": False,
            "issues": [{"severity": "error", "code": "playbook", "message": str(exc)}],
            "summary": {},
        }
    if str(project.get("report_scope") or "") != "standalone-bom":
        _bundle_issue(issues, "project_scope", "project must use standalone-bom")
    if str(project.get("bom_node_id") or "") != str(
        profile.get("bom_node_id") or ""
    ):
        _bundle_issue(
            issues,
            "bom_identity",
            "project and playbook must use the same bom_node_id",
        )
    claim_rows = [dict(row) for row in claims]
    claims_by_id = {
        str(row.get("claim_id") or ""): row
        for row in claim_rows
        if str(row.get("claim_id") or "")
    }
    mapping_rows = [dict(row) for row in claim_mappings]
    normalized_mapping_history = []
    for row in mapping_rows:
        try:
            normalized_mapping_history.append(
                normalize_claim_mapping(
                    row,
                    claims_by_id=claims_by_id,
                    profile=profile,
                    mapped_at=as_of_date,
                )
            )
        except ValueError as exc:
            _bundle_issue(issues, "claim_mapping", str(exc))
    normalized_mappings = _active_claim_mappings(
        normalized_mapping_history,
        as_of_date=as_of_date,
    )
    primary_counts = {
        claim_id: sum(
            row.get("claim_id") == claim_id
            and row.get("mapping_role") == "primary"
            for row in normalized_mappings
        )
        for claim_id in claims_by_id
    }
    for claim_id, count in primary_counts.items():
        if count != 1:
            _bundle_issue(
                issues,
                "primary_mapping",
                f"{claim_id} requires exactly one primary mapping, found {count}",
            )
    state_rows = []
    for row in logic_states:
        try:
            state = normalize_logic_state(
                dict(row),
                profile=profile,
                claims_by_id=claims_by_id,
                as_of_date=as_of_date,
            )
            state_rows.append(state)
            node_id = str(state["logic_node_id"])
            state_mapping_directions = {
                (
                    str(mapping.get("claim_id") or ""),
                    str(mapping.get("logic_node_id") or ""),
                ): str(mapping.get("direction") or "")
                for mapping in _active_claim_mappings(
                    normalized_mapping_history,
                    as_of_date=str(state.get("as_of_date") or as_of_date),
                )
            }
            for claim_id in state["support_claim_ids"]:
                if state_mapping_directions.get((claim_id, node_id)) != "support":
                    _bundle_issue(
                        issues,
                        "state_support_mapping",
                        f"{claim_id} is support evidence for {node_id} without a support mapping",
                    )
            for claim_id in state["refute_claim_ids"]:
                if state_mapping_directions.get((claim_id, node_id)) != "refute":
                    _bundle_issue(
                        issues,
                        "state_refute_mapping",
                        f"{claim_id} is refute evidence for {node_id} without a refute mapping",
                    )
        except ValueError as exc:
            _bundle_issue(issues, "logic_state", str(exc))
    covered_nodes = {
        str(row.get("logic_node_id") or "")
        for row in state_rows
        if str(row.get("as_of_date") or "") <= as_of_date
    }
    missing_states = sorted(set(index["nodes"]) - covered_nodes)
    if missing_states:
        _bundle_issue(
            issues,
            "logic_state_coverage",
            f"missing as-of logic states for {missing_states}",
        )
    for node_id, node in index["nodes"].items():
        if str(node.get("render_mode") or "") != "demand_quantity_matrix":
            continue
        candidates = sorted(
            (
                row
                for row in state_rows
                if str(row.get("logic_node_id") or "") == node_id
                and str(row.get("as_of_date") or "") <= as_of_date
            ),
            key=lambda row: str(row.get("as_of_date") or ""),
            reverse=True,
        )
        if not candidates or not candidates[0].get("demand_quantity_rows"):
            _bundle_issue(
                issues,
                "demand_quantity_matrix",
                f"latest as-of state for {node_id} requires demand quantity rows",
            )

    entity_state_rows = []
    mapped_entity_coordinates: set[tuple[str, str]] = set()
    for mapping in normalized_mappings:
        if str(mapping.get("direction") or "") == "unmapped":
            continue
        node_id = str(mapping.get("logic_node_id") or "")
        claim_id = str(mapping.get("claim_id") or "")
        for entity_name in mapping.get("entities") or []:
            entity_id = _entity_id(str(entity_name))
            mapped_entity_coordinates.add((node_id, entity_id))
    for row in entity_states:
        try:
            state = normalize_entity_state(
                dict(row),
                profile=profile,
                claims_by_id=claims_by_id,
                as_of_date=as_of_date,
            )
            entity_state_rows.append(state)
            coordinate = (
                str(state["logic_node_id"]),
                str(state["entity_id"]),
            )
            state_mapping_coordinate_directions: dict[
                tuple[str, str, str], str
            ] = {}
            state_mapped_entity_coordinates: set[tuple[str, str]] = set()
            for mapping in _active_claim_mappings(
                normalized_mapping_history,
                as_of_date=str(state.get("as_of_date") or as_of_date),
            ):
                if str(mapping.get("direction") or "") == "unmapped":
                    continue
                mapping_node_id = str(mapping.get("logic_node_id") or "")
                mapping_claim_id = str(mapping.get("claim_id") or "")
                for entity_name in mapping.get("entities") or []:
                    mapping_coordinate = (
                        mapping_node_id,
                        _entity_id(str(entity_name)),
                    )
                    state_mapped_entity_coordinates.add(mapping_coordinate)
                    state_mapping_coordinate_directions[
                        (*mapping_coordinate, mapping_claim_id)
                    ] = str(mapping.get("direction") or "")
            if coordinate not in state_mapped_entity_coordinates:
                _bundle_issue(
                    issues,
                    "entity_state_mapping",
                    (
                        f"{state['entity_name']} has an entity state for "
                        f"{state['logic_node_id']} without mapped material"
                    ),
                )
            for claim_id in state["support_claim_ids"]:
                if state_mapping_coordinate_directions.get(
                    (*coordinate, claim_id)
                ) != "support":
                    _bundle_issue(
                        issues,
                        "entity_state_support_mapping",
                        (
                            f"{claim_id} is support evidence for "
                            f"{state['logic_node_id']} / {state['entity_name']} "
                            "without a matching support mapping"
                        ),
                    )
            for claim_id in state["refute_claim_ids"]:
                if state_mapping_coordinate_directions.get(
                    (*coordinate, claim_id)
                ) != "refute":
                    _bundle_issue(
                        issues,
                        "entity_state_refute_mapping",
                        (
                            f"{claim_id} is refute evidence for "
                            f"{state['logic_node_id']} / {state['entity_name']} "
                            "without a matching refute mapping"
                        ),
                    )
        except ValueError as exc:
            _bundle_issue(issues, "entity_state", str(exc))
    covered_entity_coordinates = {
        (
            str(row.get("logic_node_id") or ""),
            str(row.get("entity_id") or ""),
        )
        for row in entity_state_rows
        if str(row.get("as_of_date") or "") <= as_of_date
    }
    missing_entity_states = sorted(
        mapped_entity_coordinates - covered_entity_coordinates
    )
    if missing_entity_states:
        _bundle_issue(
            issues,
            "entity_state_coverage",
            f"missing as-of entity states for {missing_entity_states}",
        )

    revision_rows = []
    for row in thesis_revisions:
        try:
            revision_rows.append(
                normalize_thesis_revision(
                    dict(row),
                    profile=profile,
                    claims_by_id=claims_by_id,
                    as_of_date=as_of_date,
                )
            )
        except ValueError as exc:
            _bundle_issue(issues, "thesis_revision", str(exc))
    revised_nodes = {
        str(row.get("logic_node_id") or "")
        for row in revision_rows
        if str(row.get("as_of_date") or "") <= as_of_date
    }
    missing_revisions = sorted(set(index["nodes"]) - revised_nodes)
    if missing_revisions:
        _bundle_issue(
            issues,
            "revision_coverage",
            f"missing baseline/change revisions for {missing_revisions}",
        )

    snapshot_rows = []
    for row in investment_snapshots:
        try:
            snapshot_rows.append(
                normalize_investment_snapshot(
                    dict(row),
                    profile=profile,
                    claims_by_id=claims_by_id,
                    as_of_date=as_of_date,
                )
            )
        except ValueError as exc:
            _bundle_issue(issues, "investment_snapshot", str(exc))
    visible_snapshots = [
        row
        for row in snapshot_rows
        if str(row.get("as_of_date") or "") <= as_of_date
    ]
    if not visible_snapshots:
        _bundle_issue(
            issues,
            "investment_snapshot",
            "one reviewed investment snapshot is required",
        )

    return {
        "ok": not any(row["severity"] == "error" for row in issues),
        "issues": issues,
        "summary": {
            "claims": len(claims_by_id),
            "mappings": len(normalized_mappings),
            "mapping_history": len(normalized_mapping_history),
            "unmapped_relations": sum(
                str(row.get("direction") or "") == "unmapped"
                for row in normalized_mappings
            ),
            "logic_nodes": len(index["nodes"]),
            "state_nodes": len(covered_nodes),
            "entity_states": len(covered_entity_coordinates),
            "revision_nodes": len(revised_nodes),
            "investment_snapshots": len(visible_snapshots),
            "as_of_date": as_of_date,
        },
    }


def _build_logic_node_view(
    *,
    node: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
    state_rows: list[dict[str, Any]],
    entity_state_rows: list[dict[str, Any]],
    revisions: list[dict[str, Any]],
    mappings: list[dict[str, Any]],
    claims_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    node_id = str(node.get("logic_node_id") or "")
    candidates = sorted(
        (
            row
            for row in state_rows
            if str(row.get("logic_node_id") or "") == node_id
        ),
        key=lambda row: str(row.get("as_of_date") or ""),
        reverse=True,
    )
    revision_candidates = sorted(
        (
            row
            for row in revisions
            if str(row.get("logic_node_id") or "") == node_id
        ),
        key=lambda row: str(row.get("as_of_date") or ""),
        reverse=True,
    )
    revisions_by_claim: dict[str, list[dict[str, Any]]] = {}
    for revision in revision_candidates:
        for claim_id in revision.get("trigger_claim_ids") or []:
            revisions_by_claim.setdefault(str(claim_id), []).append(
                {**revision, "revision_claim_role": "trigger"}
            )
        for claim_id in revision.get("conflicting_claim_ids") or []:
            revisions_by_claim.setdefault(str(claim_id), []).append(
                {**revision, "revision_claim_role": "conflict"}
            )
    node_mappings = [
        row
        for row in mappings
        if str(row.get("logic_node_id") or "") == node_id
        and str(row.get("direction") or "") != "unmapped"
    ]
    claim_events = []
    for mapping in node_mappings:
        claim_id = str(mapping.get("claim_id") or "")
        claim = claims_by_id.get(claim_id)
        if claim is None:
            continue
        claim_events.append(
            {
                **claim,
                "direction": str(mapping.get("direction") or "neutral"),
                "node_fit": str(mapping.get("node_fit") or "proxy"),
                "rule_match": str(mapping.get("rule_match") or "neither"),
                "rationale": str(mapping.get("rationale") or ""),
                "mapping_role": str(mapping.get("mapping_role") or "primary"),
                "evidence_nature": str(
                    mapping.get("evidence_nature") or "opinion"
                ),
                "directness": str(mapping.get("directness") or "indirect"),
                "novelty": str(mapping.get("novelty") or "new"),
                "entities": _unique_strings(
                    mapping.get("entities")
                    or [mapping.get("entity") or "行业 / 多主体"]
                ),
                "downstream_impacts": list(
                    mapping.get("downstream_impacts") or []
                ),
                "triggered_revisions": list(
                    revisions_by_claim.get(claim_id) or []
                ),
            }
        )
    claim_events.sort(
        key=lambda row: (
            str(row.get("published_at") or ""),
            str(row.get("source_id") or ""),
            str(row.get("claim_id") or ""),
        ),
        reverse=True,
    )
    entity_claims: dict[str, dict[str, Any]] = {}
    for mapping in node_mappings:
        claim_id = str(mapping.get("claim_id") or "")
        claim = claims_by_id.get(claim_id)
        if claim is None:
            continue
        for entity_name in mapping.get("entities") or [
            mapping.get("entity") or "行业 / 多主体"
        ]:
            name = str(entity_name).strip() or "行业 / 多主体"
            entity_id = _entity_id(name)
            entity = entity_claims.setdefault(
                entity_id,
                {
                    "entity_id": entity_id,
                    "entity_name": name,
                    "claims": {},
                },
            )
            entity["claims"][claim_id] = {
                **claim,
                "logic_mappings": [
                    {
                        **mapping,
                        "logic_node_title": str(node.get("title") or node_id),
                    }
                ],
            }
    entities = []
    for entity_id, entity in entity_claims.items():
        state_candidates = sorted(
            (
                row
                for row in entity_state_rows
                if str(row.get("logic_node_id") or "") == node_id
                and str(row.get("entity_id") or "") == entity_id
            ),
            key=lambda row: str(row.get("as_of_date") or ""),
            reverse=True,
        )
        entity_state = state_candidates[0] if state_candidates else {}
        claims = sorted(
            entity["claims"].values(),
            key=lambda row: (
                str(row.get("published_at") or ""),
                str(row.get("source_id") or ""),
            ),
            reverse=True,
        )
        entities.append(
            {
                "entity_id": entity_id,
                "entity_name": entity["entity_name"],
                "assessment": str(
                    entity_state.get("assessment")
                    or "该实体已有映射材料，但尚未形成独立截面评估。"
                ),
                "change_summary": str(
                    entity_state.get("change_summary")
                    or "当前为该实体的首个结构化截面。"
                ),
                "investment_effect": str(
                    entity_state.get("investment_effect") or "unclear"
                ),
                "evidence_gaps": list(
                    entity_state.get("evidence_gaps") or []
                ),
                "next_validation": str(
                    entity_state.get("next_validation") or ""
                ),
                "claims": claims,
                "material_count": len(
                    {
                        str(claim.get("source_id") or "")
                        for claim in claims
                        if str(claim.get("source_id") or "")
                    }
                ),
                "claim_count": len(claims),
            }
        )
    entities.sort(
        key=lambda row: (
            -int(row.get("claim_count") or 0),
            str(row.get("entity_name") or ""),
        )
    )
    current = candidates[0] if candidates else {}
    revisions_by_date: dict[str, list[dict[str, Any]]] = {}
    for revision in revision_candidates:
        revisions_by_date.setdefault(
            str(revision.get("as_of_date") or ""), []
        ).append(revision)
    state_history = []
    for state_row in reversed(candidates):
        snapshot_date = str(state_row.get("as_of_date") or "")
        state_revisions = revisions_by_date.get(snapshot_date) or []
        state_history.append(
            {
                "as_of_date": snapshot_date,
                "state": str(state_row.get("state") or "unresolved"),
                "previous_state": str(
                    state_row.get("previous_state") or ""
                ),
                "conclusion": str(state_row.get("conclusion") or ""),
                "change_summary": str(
                    state_row.get("change_summary") or ""
                ),
                "revision_type": str(
                    (state_revisions[0] if state_revisions else {}).get(
                        "revision_type"
                    )
                    or ("baseline" if not state_history else "change")
                ),
                "change_direction": str(
                    (state_revisions[0] if state_revisions else {}).get(
                        "change_direction"
                    )
                    or "unchanged"
                ),
                "revision_rationale": str(
                    (state_revisions[0] if state_revisions else {}).get(
                        "rationale"
                    )
                    or ""
                ),
                "trigger_claim_ids": _unique_strings(
                    claim_id
                    for revision in state_revisions
                    for claim_id in revision.get("trigger_claim_ids") or []
                ),
            }
        )
    event_history_groups = _build_event_history_groups(
        claim_events=claim_events,
        revisions=revision_candidates,
    )
    demand_parties: dict[str, list[str]] = dict(
        node.get("demand_parties") or {}
    )
    if str(node.get("render_mode") or "") == "demand_quantity_matrix":
        classification_node = nodes_by_id.get(
            str(node.get("classification_node_id") or ""), {}
        )
        demand_parties = dict(classification_node.get("demand_parties") or {})
    demand_quantity_rows = []
    for row in current.get("demand_quantity_rows") or []:
        sources: dict[str, dict[str, Any]] = {}
        for claim_id in row.get("claim_ids") or []:
            claim = claims_by_id.get(str(claim_id) or "")
            if not claim:
                continue
            source_id = str(claim.get("source_id") or "")
            if source_id and source_id not in sources:
                sources[source_id] = {
                    "source_id": source_id,
                    "source_title": str(
                        claim.get("source_title") or source_id
                    ),
                    "source_url": str(claim.get("source_url") or ""),
                    "published_at": str(claim.get("published_at") or ""),
                    "material_class": str(claim.get("material_class") or "other"),
                }
        demand_quantity_rows.append(
            {**row, "sources": list(sources.values())}
        )
    return {
        **node,
        "state": str(current.get("state") or "unresolved"),
        "conclusion": str(
            current.get("conclusion")
            or "当前没有足够的经过映射和复核的证据形成节点结论。"
        ),
        "change_summary": str(
            current.get("change_summary")
            or "当前为首个结构化研究截面。"
        ),
        "evidence_gaps": list(current.get("evidence_gaps") or []),
        "next_validation": str(current.get("next_validation") or ""),
        "support_count": sum(
            str(row.get("direction") or "") == "support"
            for row in node_mappings
        ),
        "refute_count": sum(
            str(row.get("direction") or "") == "refute"
            for row in node_mappings
        ),
        "mapped_claim_count": len(
            {
                str(row.get("claim_id") or "")
                for row in node_mappings
                if str(row.get("claim_id") or "")
            }
        ),
        "entities": entities,
        "claim_events": claim_events,
        "state_history": state_history,
        "event_history_groups": event_history_groups,
        "demand_quantity_rows": demand_quantity_rows,
        "demand_parties": demand_parties,
        "latest_revision": revision_candidates[0] if revision_candidates else {},
    }


def _build_event_history_groups(
    *,
    claim_events: list[dict[str, Any]],
    revisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Group immutable claim events by market-known month, then by source."""

    groups: list[dict[str, Any]] = []
    groups_by_key: dict[str, dict[str, Any]] = {}
    source_indexes: dict[str, dict[str, dict[str, Any]]] = {}
    for event in claim_events:
        published_at = str(event.get("published_at") or "")
        period_key = published_at[:7] if len(published_at) >= 7 else "date-unknown"
        if period_key == "date-unknown":
            period_label = "日期未明"
        else:
            year, month = period_key.split("-", 1)
            period_label = f"{year}年{month}月"
        if period_key not in groups_by_key:
            group = {
                "period_key": period_key,
                "period_label": period_label,
                "claim_count": 0,
                "sources": [],
                "state_revisions": [
                    revision
                    for revision in revisions
                    if str(revision.get("as_of_date") or "").startswith(
                        period_key
                    )
                ],
            }
            groups_by_key[period_key] = group
            source_indexes[period_key] = {}
            groups.append(group)
        group = groups_by_key[period_key]
        group["claim_count"] += 1
        source_id = str(event.get("source_id") or "")
        source_key = "|".join(
            (
                published_at,
                source_id,
                str(event.get("source_title") or ""),
            )
        )
        source = source_indexes[period_key].get(source_key)
        if source is None:
            source = {
                "source_id": source_id,
                "source_title": str(
                    event.get("source_title") or source_id or "来源"
                ),
                "source_url": str(event.get("source_url") or ""),
                "published_at": published_at,
                "material_class": str(
                    event.get("material_class") or "other"
                ),
                "claim_count": 0,
                "events": [],
            }
            source_indexes[period_key][source_key] = source
            group["sources"].append(source)
        source["claim_count"] += 1
        source["events"].append(event)
    return groups


def _normalize_company_impact(
    row: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    company = str(row.get("company") or "").strip()
    if not company:
        raise ValueError("Company impacts require company")
    return {
        "company": company,
        "ticker": str(row.get("ticker") or "").strip(),
        "exposure": str(row.get("exposure") or "").strip(),
        "earnings_bridge": str(row.get("earnings_bridge") or "").strip(),
        "priced_in": str(row.get("priced_in") or "").strip(),
        "conclusion": str(row.get("conclusion") or "").strip(),
        "source_ids": _verified_claim_ids(
            row.get("source_ids") or [], claims_by_id, accept_source_ids=True
        ),
        "action_state": _choice(
            row, "action_state", ACTION_STATES, "watch_only"
        ),
    }


def _profile_has_logic_nodes(profile: dict[str, Any]) -> bool:
    return any(
        isinstance(lens, dict) and lens.get("logic_nodes")
        for lens in profile.get("lenses") or []
    )


def _verified_claim_ids(
    values: Iterable[Any],
    claims_by_id: dict[str, dict[str, Any]],
    *,
    accept_source_ids: bool = False,
) -> list[str]:
    ids = _unique_strings(values)
    if accept_source_ids:
        known_sources = {
            str(row.get("source_id") or "") for row in claims_by_id.values()
        }
        unknown = [item for item in ids if item not in known_sources]
    else:
        unknown = [item for item in ids if item not in claims_by_id]
    if unknown:
        noun = "source" if accept_source_ids else "claim"
        raise ValueError(f"Unknown {noun} ids={unknown}")
    return ids


def _verified_node_ids(
    values: Iterable[Any],
    nodes: dict[str, dict[str, Any]],
) -> list[str]:
    ids = _unique_strings(values)
    unknown = [item for item in ids if item not in nodes]
    if unknown:
        raise ValueError(f"Unknown logic node ids={unknown}")
    return ids


def _choice(
    raw: dict[str, Any],
    field: str,
    allowed: Iterable[str],
    default: str,
) -> str:
    value = str(raw.get(field) or default).strip()
    if value not in set(allowed):
        raise ValueError(f"Invalid {field}={value!r}")
    return value


def _optional_choice(
    raw: dict[str, Any],
    field: str,
    allowed: Iterable[str],
) -> str:
    value = str(raw.get(field) or "").strip()
    if value and value not in set(allowed):
        raise ValueError(f"Invalid {field}={value!r}")
    return value


def _unique_strings(values: Iterable[Any]) -> list[str]:
    return list(
        dict.fromkeys(
            str(value).strip() for value in values if str(value).strip()
        )
    )


def _mapping_id(claim_id: str, logic_node_id: str) -> str:
    digest = hashlib.sha256(
        f"{claim_id}|{logic_node_id}".encode("utf-8")
    ).hexdigest()[:20]
    return f"MAP-{digest.upper()}"


def _entity_id(entity_name: str) -> str:
    digest = hashlib.sha256(entity_name.strip().encode("utf-8")).hexdigest()[:16]
    return f"ENT-{digest.upper()}"


def _revision_id(logic_node_id: str, as_of_date: str) -> str:
    digest = hashlib.sha256(
        f"{logic_node_id}|{as_of_date}".encode("utf-8")
    ).hexdigest()[:20]
    return f"REV-{digest.upper()}"


def _require_date(value: str, field_name: str) -> str:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must use YYYY-MM-DD") from exc
    return value


def _bundle_issue(
    issues: list[dict[str, str]],
    code: str,
    message: str,
) -> None:
    issues.append({"severity": "error", "code": code, "message": message})
