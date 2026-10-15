# Adding and editing problems

The JSON files are the authoritative content. Generated reading copies can be overwritten by the exporter. Use a permanent descriptive ID such as `cw-new-arc-inequality`; do not change IDs when rearranging chapters. `order` controls display order within a chapter.

## Add an exercise without JSON escaping

Write the statement and solution as UTF-8 text files containing ordinary Markdown and LaTeX, then run:

```bash
python scripts/new_problem.py \
  --chapter 02-reuleaux-polygons \
  --slug new-arc-inequality \
  --title 'An inequality for circular arcs' \
  --statement-file /tmp/statement.md \
  --solution-file /tmp/solution.md \
  --source editorial
```

This inserts a matched problem and solution as a **draft**, with status `exercise`. It refuses duplicate IDs. Supplying files is optional; without them it creates editing prompts. Use `--source <bibliography-id> --locator 'Chapter ..., Proposition ...'` for an existing source, or register a new source in `data/sources.json` first. This command does not turn unreviewed text into a solved problem automatically.

Edit the two files printed by the command:

1. Make the statement self-contained: dimension, width normalization, regularity, and every hypothesis that affects the result. A short application of a substantial theorem is fine if the allowed theorem is stated.
2. Write the proof in `body_md`, including equality cases only when actually justified. Name dependencies using permanent IDs in `prerequisites`; do not use an open question as an assumed theorem.
3. Choose tags, difficulty, and a short hint in the problem's `hint_md` field. This field accepts Markdown and LaTeX, just like the statement. Suggest the key construction or first step without giving away the proof. For open questions, use it for a starting point. Difficulty describes the proof background, not the visual complexity of the shape.
4. When the proof has been checked, set `status: "solved"`, `proof_status: "checked-draft"`, and `editorial_status: "ready-for-review"`. Record the checker in `checked_by`. After human review, use `editorial_status: "reviewed"` and `proof_status: "human-reviewed"`.
5. Run `python scripts/build_html.py` to validate the data and rebuild the HTML reader. Use the Markdown exporter below if you also want an updated Markdown reading copy.

If directly editing JSON, use `\\` for each LaTeX backslash. For example `"Show $h(\\theta)+h(\\theta+\\pi)=1$."` represents the ordinary mathematical string. Newlines inside JSON strings are `\n`; the CLI handles this serialization for you.

## Add an open question

Use the same command with `--open` and chapter `08-open-problems`. It creates a draft local-research question and a discussion, never a solution. Before including it in the reading copy:

- State the problem in understandable language, followed by precise mathematics if necessary.
- Set `open_status.scope` to `literature` or `local-research`.
- Record the actual last-check date, explicit evidence, source version, and the limits of the check. Update `data/catalog.json.updated` when adding new dated material.
- Search for subsequent resolutions; do not infer current open status from a decades-old book or a failed computation.
- Keep `kind: "discussion"` and `proof_status: "not-applicable"` in the paired solutions file. Explain partial results and known traps there.

A local research question can be worth collecting without claiming that its novelty or literature-wide status is established. If an open question is solved later, keep its ID, replace the discussion with the proof and its source, remove `open_status`, and update its status and possibly its chapter.

## Add figures

Use the drawing skill at [../skills/constant-width-geometry/SKILL.md](../skills/constant-width-geometry/SKILL.md). For a scene already in this repository:

```bash
python skills/constant-width-geometry/scripts/draw.py \
  figures/scenes/irregular-pentagon.json \
  --output /tmp/irregular-pentagon.svg
```

For a maintained collection figure, add its scene, caption, alt text, and problem IDs to `scripts/make_figures.py`, then run it. That script rebuilds `figures/manifest.json` and replaces each problem's `figures` list from the manifest; manual attachments should therefore also be registered there. Use `python scripts/validate.py` to catch missing assets. Mathematical diagrams should show actual constructed shapes, and captions should identify approximations or assumed constructions.

The two topology plots (`distance-functions` and `grid-domain-topologies`) use `scripts/make_topology_figures.py`; edit their definitions there. Their scene JSON records that renderer. The main `make_figures.py` command rebuilds these plots along with the geometric scenes.

The Blaschke proof-route diagrams use `scripts/make_blaschke_figures.py`, which imports the drawing skill and records its construction parameters in scene JSON. Edit their definitions there; the main `make_figures.py` rebuild includes them.

The review diagrams (curved caps, switching intervals, and curvature aliasing) use `scripts/make_review_figures.py`; the segment-sweep diagram uses `scripts/make_mixed_review_figure.py`. Both are included in the main rebuild. Each accepts `--output-dir /tmp/cw-preview --preview` to create SVG and PNG previews without replacing published figures. Inspect previews and geometry diagnostics before rebuilding the reader.

## Review and export

Start each review pass with:

```bash
python scripts/review_status.py              # list only new or changed items
python scripts/review_status.py --all --json  # all items and their effective flags
```

The ledger in `data/reviews.json` is keyed by permanent problem ID. Each completed review has `reviewed: true`, a reviewer, date, `review_kind` (`ai` or `human`), report path, and content fingerprint. The command derives three states: `current` (the reviewed content still matches), `new` (no review record), and `changed` (the saved review covers an older version). In its JSON output, the effective `reviewed` flag is true only for `current` items. All 127 entries in the 15 October 2026 pass have current AI review records.

Editing a statement, hint, solution, prerequisite, source reference, figure attachment/caption, or open-status claim makes the item pending again. Chapter order, approval labels, and regenerated image bytes are excluded. Changes inside an existing figure asset or a bibliography entry are not detected by this fingerprint; check affected illustrations and references when reviewing those assets. Pending reviews do not block normal validation or export, and the AI flag does not confer human approval.

After actually reviewing selected items, write a short report in `docs/reviews/` and record them explicitly. For example, replacing the ID and metadata with your own:

```bash
python scripts/review_status.py \
  --record cw-my-new-problem \
  --reviewer 'Your name' \
  --date 2026-10-15 \
  --review-kind human \
  --report docs/reviews/my-review.md
```

The report must exist. Multiple IDs can follow `--record`. Use `--review-kind ai` for an AI pass; the command does not alter `editorial_status` or `proof_status`. Do not refresh fingerprints merely to clear the pending list.

```bash
python scripts/validate.py             # structural and reference checks
python scripts/validate.py --strict    # additionally requires human editorial review
python scripts/review_status.py --self-test  # check review tracking in a temporary copy
python scripts/export.py              # statements and portable site data, no solutions
python scripts/export.py --include-solutions
python scripts/build_html.py          # offline HTML with hidden hints and solutions
python scripts/check_html.py          # check generated HTML and local assets
```

The first collection intentionally does not pass `--strict`: its proofs are checked drafts, not signed-off human review. Draft additions are excluded from exports. `ready-for-review` entries are included and visibly labeled. The exporter puts statements and solutions in separate directories and creates a metadata-only search index with no proofs.

No source text or statement supplied to the CLI is executed as Python or shell code. Keep local book files outside the public export; put portable bibliographic information in `data/sources.json` and machine-specific file locations in `sources/local-inventory.json`.
