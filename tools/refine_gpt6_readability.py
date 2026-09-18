"""Apply an authored, presentation-only revision without re-researching or changing gates."""
from copy import deepcopy
from datetime import datetime, timezone
import json

from gpt6_impact_research import PROJECT, append_unique, write_json
from refine_gpt6_report import digest, refresh_report

FOLDER = PROJECT / "research_revisions/20260918_readability"


def apply_revision():
    revision = json.loads((FOLDER / "editorial_revision.json").read_text())
    done = FOLDER / "completed.json"
    if done.exists():
        if json.loads(done.read_text())["input_sha256"] != digest(revision):
            raise ValueError("Applied editorial inputs are immutable; create a new revision")
        refresh_report()
        return
    chapters_path = PROJECT / "research_chapters.json"
    before = FOLDER / "before_chapters.json"
    if not before.exists():
        write_json(before, json.loads(chapters_path.read_text()))
    baseline = json.loads(before.read_text())
    chapters = deepcopy(baseline)
    chapter = next(c for c in chapters if c["id"] == revision["question_id"])
    old = chapter["analysis"]
    main = deepcopy(revision["main_analysis"])
    main[2]["tables"] = deepcopy(old[3]["tables"])
    supplements = [dict(deepcopy(old[i]), supplementary=True) for i in revision["supporting_section_indices"]]
    chapter["analysis"] = main + supplements
    for previous, current in zip(baseline, chapters):
        assert {k: v for k, v in previous.items() if k != "analysis"} == {k: v for k, v in current.items() if k != "analysis"}
        if previous["id"] != revision["question_id"]:
            assert previous == current
    write_json(chapters_path, chapters)
    append_unique(PROJECT / "research_events.jsonl", [{
        "event_id": revision["revision_id"], "event_type": "presentation_revised",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "question_node_id": revision["question_id"], "scope": revision["scope"],
        "input_sha256": digest(revision),
        "artifact": str((FOLDER / "editorial_revision.json").relative_to(PROJECT)),
        "new_evidence": False, "gate_changes": False,
    }], "event_id")
    refresh_report()
    write_json(done, {"input_sha256": digest(revision), "research_state_changed": False,
                      "change": "authored prose and main/supporting order only"})


if __name__ == "__main__":
    apply_revision()
