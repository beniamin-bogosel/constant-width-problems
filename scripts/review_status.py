#!/usr/bin/env python3
"""List new/changed problems, or deliberately record completed selected reviews.

Read-only examples:
  python scripts/review_status.py
  python scripts/review_status.py --all --json

Record only after reviewing the selected current contents:
  python scripts/review_status.py --record cw-example --reviewer 'Reviewer name' \
    --date 2026-10-15 --review-kind ai --report docs/reviews/example.md

The ledger records completed reviews of a particular content hash. It does not
grant human approval, modify chapter data, or silently review new additions.
"""

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FINGERPRINT_VERSION = "cw-content-v1"
PROBLEM_FIELDS = (
    "id", "title", "statement_md", "hint_md", "status", "open_status",
    "prerequisites", "sources", "figures",
)
SOLUTION_FIELDS = ("problem_id", "kind", "body_md", "sources")


def content_sha256(problem, solution):
    """Hash reviewable JSON content; ignore approvals, ordering, and asset bytes."""
    payload = {
        "fingerprint_version": FINGERPRINT_VERSION,
        "problem": {key: problem[key] for key in PROBLEM_FIELDS if key in problem},
        "solution": {key: solution[key] for key in SOLUTION_FIELDS if key in solution},
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def relative_path(root, value):
    """Resolve a portable repository-relative path without allowing escapes."""
    path = Path(value)
    if not value or path.is_absolute() or "\\" in value or ".." in path.parts:
        raise ValueError(f"expected a portable repository-relative path: {value}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes root: {value}")
    return resolved


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_content(root):
    """Read chapter pairs in catalogue order, rejecting incomplete ID pairing."""
    root = Path(root)
    catalog = read_json(root / "data/catalog.json")
    problems, solutions = {}, {}
    for chapter in sorted(catalog["chapters"], key=lambda item: item["order"]):
        problem_doc = read_json(relative_path(root / "data", chapter["problems"]))
        solution_doc = read_json(relative_path(root / "data", chapter["solutions"]))
        for problem in sorted(problem_doc["problems"], key=lambda item: item["order"]):
            if problem["id"] in problems:
                raise ValueError(f"duplicate problem: {problem['id']}")
            problems[problem["id"]] = problem
        for solution in solution_doc["solutions"]:
            if solution["problem_id"] in solutions:
                raise ValueError(f"duplicate solution: {solution['problem_id']}")
            solutions[solution["problem_id"]] = solution
    if problems.keys() != solutions.keys():
        raise ValueError("problem and solution IDs do not match")
    return problems, solutions


def load_ledger(root):
    path = Path(root) / "data/reviews.json"
    if not path.exists():
        return {"schema_version": "1.0", "fingerprint_version": FINGERPRINT_VERSION,
                "reviews": {}}
    ledger = read_json(path)
    if ledger.get("schema_version") != "1.0":
        raise ValueError("unsupported review ledger schema_version")
    if ledger.get("fingerprint_version") != FINGERPRINT_VERSION:
        raise ValueError("unsupported review fingerprint_version; migrate deliberately")
    if not isinstance(ledger.get("reviews"), dict):
        raise ValueError("review ledger reviews must be an object keyed by problem ID")
    required = {"reviewed", "reviewer", "date", "review_kind", "report", "content_sha256"}
    for problem_id, record in ledger["reviews"].items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", problem_id):
            raise ValueError(f"invalid review problem ID: {problem_id}")
        if not isinstance(record, dict) or set(record) != required:
            raise ValueError(f"{problem_id}: malformed review record")
        if record["reviewed"] is not True or record["review_kind"] not in ("ai", "human"):
            raise ValueError(f"{problem_id}: invalid review flag or kind")
        if not isinstance(record["reviewer"], str) or not record["reviewer"].strip():
            raise ValueError(f"{problem_id}: reviewer must not be empty")
        if date.fromisoformat(record["date"]).isoformat() != record["date"]:
            raise ValueError(f"{problem_id}: invalid review date")
        relative_path(Path(root), record["report"])
        if not isinstance(record["content_sha256"], str) or not re.fullmatch(
                r"[a-f0-9]{64}", record["content_sha256"]):
            raise ValueError(f"{problem_id}: invalid SHA256 fingerprint")
    return ledger


def build_snapshot(problems, solutions, ledger):
    """Return all effective states; an old reviewed flag alone is insufficient."""
    records = ledger["reviews"]
    items = []
    for problem_id, problem in problems.items():
        if problem_id not in solutions:
            continue  # The main validator reports missing solution pairs separately.
        digest = content_sha256(problem, solutions[problem_id])
        record = records.get(problem_id)
        if record is None:
            state = "new"
        elif record.get("reviewed") is True and record.get("content_sha256") == digest:
            state = "current"
        else:
            state = "changed"
        items.append({
            "problem_id": problem_id,
            "chapter_id": problem["chapter_id"],
            "title": problem["title"],
            "state": state,
            "reviewed": state == "current",
            "content_sha256": digest,
            "review": record,
        })
    counts = Counter(item["state"] for item in items)
    summary = {"total": len(items), "current": counts["current"],
               "new": counts["new"], "changed": counts["changed"],
               "pending": counts["new"] + counts["changed"]}
    return {"fingerprint_version": FINGERPRINT_VERSION, "summary": summary,
            "items": items, "orphaned_review_ids": sorted(records.keys() - problems.keys())}


def review_snapshot(root=ROOT):
    """Read-only API for a future website or other tooling."""
    problems, solutions = load_content(Path(root))
    return build_snapshot(problems, solutions, load_ledger(Path(root)))


def record_reviews(root, problem_ids, *, reviewer, reviewed_on, review_kind, report):
    """Explicitly record completed reviews of selected current problem/solution pairs."""
    root = Path(root)
    ids = list(dict.fromkeys(problem_ids))
    if not ids:
        raise ValueError("at least one explicit problem ID is required")
    if not reviewer or not reviewer.strip():
        raise ValueError("reviewer must not be empty")
    if date.fromisoformat(reviewed_on).isoformat() != reviewed_on:
        raise ValueError("date must use YYYY-MM-DD")
    if review_kind not in ("ai", "human"):
        raise ValueError("review_kind must be ai or human")
    if not relative_path(root, report).is_file():
        raise ValueError(f"review report does not exist: {report}")
    problems, solutions = load_content(root)
    missing = set(ids) - problems.keys()
    if missing:
        raise ValueError("unknown problem IDs: " + ", ".join(sorted(missing)))
    ledger = load_ledger(root)
    for problem_id in ids:
        ledger["reviews"][problem_id] = {
            "reviewed": True,
            "reviewer": reviewer.strip(),
            "date": reviewed_on,
            "review_kind": review_kind,
            "report": report,
            "content_sha256": content_sha256(problems[problem_id], solutions[problem_id]),
        }
    path = root / "data/reviews.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".reviews-", suffix=".json", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return ids


def self_test():
    """Exercise review transitions and recording isolation in a temporary repository."""
    from copy import deepcopy

    with tempfile.TemporaryDirectory(prefix="cw-review-status-") as directory:
        root = Path(directory)
        chapter = root / "data/chapters/test"
        chapter.mkdir(parents=True)
        report = root / "docs/reviews/test.md"
        report.parent.mkdir(parents=True)
        report.write_text("Test review record.\n", encoding="utf-8")
        figure = root / "figures/test.svg"
        figure.parent.mkdir()
        figure.write_text("<svg/>\n", encoding="utf-8")
        catalog = {"chapters": [{"id": "test", "order": 1,
                                 "problems": "chapters/test/problems.json",
                                 "solutions": "chapters/test/solutions.json"}]}
        (root / "data/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
        problem = {"id": "cw-test", "chapter_id": "test", "order": 1,
                   "title": "Test", "status": "solved", "editorial_status": "reviewed",
                   "statement_md": "A statement", "hint_md": "A hint", "prerequisites": [],
                   "sources": [{"source_id": "test", "locator": "p. 1", "relationship": "adapted"}],
                   "figures": [{"figure_id": "test", "path": "figures/test.svg",
                                "caption_md": "A caption", "alt": "Description"}]}
        solution = {"problem_id": "cw-test", "kind": "proof", "body_md": "A proof",
                    "sources": deepcopy(problem["sources"]), "proof_status": "human-reviewed",
                    "checked_by": "Existing human reviewer"}

        def write_pair(problems, solutions):
            for filename, key, values in (("problems.json", "problems", problems),
                                           ("solutions.json", "solutions", solutions)):
                (chapter / filename).write_text(json.dumps({key: values}), encoding="utf-8")

        def state():
            return review_snapshot(root)["items"][0]["state"]

        metadata = dict(reviewer="Test reviewer", reviewed_on="2026-10-15",
                        review_kind="ai", report="docs/reviews/test.md")
        write_pair([problem], [solution])
        assert state() == "new" and not (root / "data/reviews.json").exists()
        originals = [(chapter / filename).read_bytes() for filename in ("problems.json", "solutions.json")]
        record_reviews(root, ["cw-test"], **metadata)
        assert state() == "current"
        assert originals == [(chapter / filename).read_bytes() for filename in ("problems.json", "solutions.json")]

        changed = deepcopy(problem)
        changed["statement_md"] += " Revised."
        write_pair([changed], [solution])
        assert state() == "changed"
        changed_solution = deepcopy(solution)
        changed_solution["body_md"] += " Revised."
        write_pair([problem], [changed_solution])
        assert state() == "changed"

        baseline = content_sha256(problem, solution)
        for field, value in (("title", "Another title"), ("hint_md", "Another hint"),
                             ("status", "exercise"), ("open_status", {"last_checked": "2026-10-15"}),
                             ("prerequisites", ["cw-dependency"])):
            changed = deepcopy(problem)
            changed[field] = value
            assert content_sha256(changed, solution) != baseline, field
        for key in ("figure_id", "path", "caption_md", "alt"):
            changed = deepcopy(problem)
            changed["figures"][0][key] += " revised"
            assert content_sha256(changed, solution) != baseline, key
        for target in ("problem", "solution"):
            changed, changed_solution = deepcopy(problem), deepcopy(solution)
            (changed if target == "problem" else changed_solution)["sources"][0]["locator"] = "p. 2"
            assert content_sha256(changed, changed_solution) != baseline, target
        changed_solution = deepcopy(solution)
        changed_solution["kind"] = "discussion"
        assert content_sha256(problem, changed_solution) != baseline

        changed, changed_solution = deepcopy(problem), deepcopy(solution)
        changed.update(order=50, editorial_status="draft", level="graduate", tags=["metadata"])
        changed_solution.update(checked_by="Another reviewer", proof_status="checked-draft")
        write_pair([changed], [changed_solution])
        figure.write_text("<svg><!-- regenerated bytes --></svg>\n", encoding="utf-8")
        assert state() == "current"
        reordered = dict(reversed(list(problem.items())))
        assert content_sha256(reordered, solution) == baseline

        new_problem, new_solution = deepcopy(problem), deepcopy(solution)
        new_problem.update(id="cw-new", order=2)
        new_solution["problem_id"] = "cw-new"
        write_pair([problem, new_problem], [solution, new_solution])
        snapshot = review_snapshot(root)
        assert snapshot["summary"] == {"total": 2, "current": 1, "new": 1, "changed": 0, "pending": 1}
        record_reviews(root, ["cw-test"], **metadata)
        assert review_snapshot(root)["summary"]["new"] == 1

        ledger_bytes = (root / "data/reviews.json").read_bytes()
        for ids, changes in ((["cw-test", "cw-missing"], {}),
                              (["cw-new"], {"report": "docs/reviews/missing.md"}),
                              (["cw-new"], {"report": "../escape.md"})):
            try:
                record_reviews(root, ids, **(metadata | changes))
            except ValueError:
                pass
            else:
                raise AssertionError("invalid recording request was accepted")
            assert (root / "data/reviews.json").read_bytes() == ledger_bytes
    print("Review tracking checks passed: new/changed/current states, semantic fields, "
          "metadata and SVG stability, selective recording, preserved human approval, and atomic rejection.")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--all", action="store_true", help="include current items in the output")
    parser.add_argument("--json", action="store_true", help="emit machine-readable status")
    parser.add_argument("--record", nargs="+", metavar="ID", help="record completed selected reviews")
    parser.add_argument("--reviewer")
    parser.add_argument("--date", dest="reviewed_on", help="review completion date, YYYY-MM-DD")
    parser.add_argument("--review-kind", choices=("ai", "human"))
    parser.add_argument("--report", help="existing repository-relative review report path")
    parser.add_argument("--self-test", action="store_true", help="test tracking using a temporary repository")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    metadata = (args.reviewer, args.reviewed_on, args.review_kind, args.report)
    if args.record and not all(metadata):
        parser.error("--record requires --reviewer, --date, --review-kind, and --report")
    if not args.record and any(value is not None for value in metadata):
        parser.error("review metadata requires explicit --record IDs")
    try:
        recorded = []
        if args.record:
            recorded = record_reviews(args.root, args.record, reviewer=args.reviewer,
                                      reviewed_on=args.reviewed_on, review_kind=args.review_kind,
                                      report=args.report)
        snapshot = review_snapshot(args.root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Review status error: {exc}\n")
    if not args.all:
        snapshot["items"] = [item for item in snapshot["items"] if not item["reviewed"]]
    if recorded:
        snapshot["recorded_ids"] = recorded
    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        return
    if recorded:
        print("Recorded completed reviews: " + ", ".join(recorded))
    summary = snapshot["summary"]
    print(f"Review status: {summary['current']}/{summary['total']} current; "
          f"{summary['new']} new, {summary['changed']} changed, {summary['pending']} pending.")
    for item in snapshot["items"]:
        print(f"{item['state']:7} {item['problem_id']} — {item['title']}")
    if snapshot["orphaned_review_ids"]:
        print("Ledger IDs absent from the collection: " + ", ".join(snapshot["orphaned_review_ids"]))


if __name__ == "__main__":
    main()
