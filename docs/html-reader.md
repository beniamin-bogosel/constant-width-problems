# HTML reader

Open [../html/index.html](https://beniamin-bogosel.github.io/constant-width-problems/) directly in a browser. No server or Internet connection is needed: equations, fonts, figures, and reader code are included locally. External source links require Internet access.

The collection page links to eight chapters. Each chapter lists its problems; the sidebar also expands into a chapter-and-problem tree. On a phone, use the **Chapters** button to open the navigation. Search filters the tree by problem title, ID, chapter, and tags. Each chapter and problem has its own URL fragment, so bookmarks and browser back/forward navigation work.

Each problem has separate **Show hint** and **Show solution** buttons. Both panels start closed and operate independently. Switching problems or reloading closes them again. For open questions, these controls are labeled **Show starting point** and **Show background / partial results**; the latter contains discussion rather than a claimed solution. Hidden text is included in the HTML, so this is a reading aid, not access control.

## Edit and rebuild

Edit the canonical chapter JSON files in `data/chapters/`:

- `problems.json`: edit `statement_md` and `hint_md`, along with metadata and figure references.
- `solutions.json`: edit `body_md` in the entry with the matching `problem_id`.

See [authoring.md](authoring.md) for adding problems, review statuses, sources, and figures. Draft entries are excluded from the HTML reader. If a hint is empty, the reader displays a short placeholder when its panel is opened.

From the repository root, run:

```bash
python -m pip install -r requirements.txt
python scripts/build_html.py
python scripts/check_html.py
```

Building requires Python and Node.js. KaTeX is vendored in `web/vendor/katex/` with its MIT license and provenance; no npm installation or network access is needed. The builder validates the JSON and renders the mathematics before writing the HTML. Reading the resulting edition only requires a browser with JavaScript enabled.

The generated `html/` folder can be copied or served by any static web server. Copy the **whole folder**, including `assets/` and `figures/`. Rebuild after data edits; edits to generated files will be overwritten. The `.cwdata-html.json` manifest identifies a builder-owned output directory. An optional `--output PATH` chooses another output folder; a nonempty folder without this manifest is rejected.

Reader presentation lives in `web/reader.css`, interaction in `web/reader.js`, and page generation in `scripts/build_html.py`. The JSON remains independent of the presentation.

## Browser checks

An optional end-to-end check uses a locally installed Chromium and the Python `websocket-client` package:

```bash
python scripts/check_html_browser.py
```

It opens the local HTML with HTTP and HTTPS requests blocked, checks navigation, independent disclosure controls, reset behavior, search, deep links, and mobile layout, and saves screenshots in `/tmp/cw-html-preview/`.
