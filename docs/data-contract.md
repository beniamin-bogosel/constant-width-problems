# Data contract for a future website

The canonical format is UTF-8 JSON, schema version `1.0`. `data/catalog.json` lists chapters and paths **relative to `data/`**. Figure paths in problem records are relative to the repository or exported site root. Problem IDs are globally unique and permanent; filenames, chapter order, and display order are not identifiers.

| Object | Identity | Main content |
| --- | --- | --- |
| Catalog | schema version | Title, notation, ordered chapters |
| Chapter | `id` | Title, order, statement and solution paths |
| Problem | `id` | Statement, hint, level, tags, prerequisites, sources, figures |
| Solution | `problem_id` | `kind: proof` or `discussion`, body, review state |
| Source | `id` | Bibliographic title, authors, year, URL or null, provenance notes |
| Figure | `figure_id` | Asset path, caption, alt text; full scene in figure manifest |
| Review record | problem ID as ledger key | Review flag, reviewer, date, review kind, report, content fingerprint |

A chapter has exactly one problems envelope and one solutions envelope, each containing `schema_version` and `chapter_id`. Each problem has exactly one paired solution record. An open problem's paired record is background, explicitly **not** a proof. The original outline's ninth chapter, Solutions, is represented by these separate files rather than a ninth subject chapter.

## Rendering

Render `statement_md`, `hint_md`, `body_md`, and `caption_md` as Markdown with mathematical delimiters `$...$` and `$$...$$`. A future browser renderer can use KaTeX or MathJax. Escape/sanitize Markdown output before inserting HTML, and keep externally supplied links as data. No HTML or browser script is required in the canonical problem text.

Load the chapter's `problems.json` initially and fetch its `solutions.json` only when the reader asks to reveal a proof. Open problems should show an “Open question” badge and “Background / partial results” instead of “Show solution.” Display `last_checked`, scope, and qualification for open-status claims. The search index is derived metadata; statements and source JSON remain authoritative.

`prerequisites` forms a directed acyclic graph. It can support suggested reading paths, but it does not mean the proof is unconditionally elementary: some statements explicitly allow a named theorem. Difficulty is `undergraduate`, `advanced-undergraduate`, or `graduate`.

## Statuses

- `solved`: a proof is present; its review state is separate.
- `exercise`: a draft exercise still awaiting a completed/checkable proof.
- `open`: an unresolved question with dated evidence or local-research qualification.

`editorial_status` is `draft`, `ready-for-review`, or `reviewed`. `proof_status` is `incomplete`, `checked-draft`, `human-reviewed`, or `not-applicable`. Structural validation cannot certify a theorem. The supplied material is predominantly `ready-for-review` / `checked-draft`.

`data/reviews.json` is a separate authoring ledger for completed review passes. Its review flag records a review of a specific content fingerprint; it does not grant human approval or change either status above. Use `python scripts/review_status.py --all --json` to derive all current review states and effective flags. An item without a record is `new`; an item whose fingerprint no longer matches is `changed` and needs another review; matching content is `current`. Reordering chapters or rebuilding the figures does not by itself invalidate a review. The fingerprint covers the problem/solution JSON fields listed in `scripts/review_status.py`, not asset bytes or the full bibliography; see [the review workflow](authoring.md#review-and-export).

## Export boundary

`python scripts/export.py --include-solutions` writes `build/reading/site-data/` with `data/` and `figures/`. This contains no local filesystem inventory, book PDFs, temporary OCR, or private research manuscripts. Plain export omits solution files and removes their pointers from the **exported** catalog. Thus that statement-only catalog is a delivery variant; it intentionally does not satisfy the canonical catalog schema, whose paired solution paths are required. The exporter refreshes stale solution files when switching back to statement-only output.

No license is assigned to the user's existing texts or figures. Before public release, review the newly written adaptations and choose an appropriate license for the collection. Bibliographic links and facts do not transfer a source book's redistribution rights.

The authoring review ledger is not copied into reading exports. A future website can consume `python scripts/review_status.py --all --json` when review information is wanted, without changing the public proof or editorial statuses.

The optional catalog field `credits_md` records the collection credit and is preserved in website exports and displayed in the HTML footer and Markdown index.
