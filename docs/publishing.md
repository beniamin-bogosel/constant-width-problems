# Publishing the collection

The source repository is [beniamin-bogosel/constant-width-problems](https://github.com/beniamin-bogosel/constant-width-problems). The rendered reader is published at:

**[Explore Constant Width Problems](https://beniamin-bogosel.github.io/constant-width-problems/)**

GitHub's repository file view displays source code. GitHub Pages serves the built `index.html` as a website. A project repository can publish beneath the same domain as the author's homepage, so the homepage can link directly to this reader without copying its files into the homepage repository. See [GitHub's Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Deployment

The repository's Pages setting uses **GitHub Actions**. The workflow in [`.github/workflows/pages.yml`](../.github/workflows/pages.yml) runs on pushes to `main`, pull requests, and manual dispatches. It installs Python dependencies and Node.js, validates the data and review tracker, checks formulas, then builds and checks the HTML reader. Successful `main` runs publish the generated `html/` directory as the site root; pull requests only run checks.

All reader assets and equations are local to the artifact. Relative paths work under `/constant-width-problems/`, and problem links use hash fragments, for example [Pál's theorem](https://beniamin-bogosel.github.io/constant-width-problems/#cw-pal-hexagon). No server application or extra domain configuration is needed.

## Publish an update

Edit the canonical chapter JSON and any relevant source figures. Check pending reviews and build locally:

```bash
python scripts/review_status.py
python scripts/validate.py
python scripts/build_html.py
python scripts/check_html.py
git status
```

Stage the intended source changes, commit them, and push `main`. GitHub Actions rebuilds and deploys automatically. Generated `html/` and `build/` directories are ignored; the published artifact is built from the committed source. The draft book outline, source books, private manuscripts, local source inventory, and environment directories are not included in the public repository.

Inspect deployments in the repository's [Actions tab](https://github.com/beniamin-bogosel/constant-width-problems/actions). A failed build does not replace the last successful publication. The workflow can also be rerun manually there.

## Homepage link

The author's homepage repository contains this link directly below Teaching resources:

```html
<p><strong>Constant Width Problems:</strong>
  <a class="but3" href="https://beniamin-bogosel.github.io/constant-width-problems/">Explore problems</a>
</p>
```

The button reuses the homepage's existing styling. Updating the collection requires pushing only this repository; the homepage link remains stable.
