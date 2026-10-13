---
title: Building the docs
description: Run the notebook and build the Starlight site locally.
---

The web documentation uses hand-written Starlight pages, executable notebooks in `guides/`, a converter that publishes each notebook as MDX, and a GitHub Pages build. The notebook diagrams are compiled from package commands by `tikzfigure` and `pdflatex`.

Requirements: Python 3.10+, Node 22.12+, `pdflatex`, `standalone`, `tikz-cd`, and a local copy of `derham.sty` in this repository.

```bash
python3 -m pip install -r docs/requirements.txt
python3 docs/tools/notebooks.py execute
python3 docs/tools/notebooks.py convert --strict
cd docs
npm ci
npm run check:mdx
npm run build
```

`npm run build` also executes and converts changed notebooks. `npm run dev` converts the last executed notebook without rerunning it, so edits to prose appear quickly. `DOCS_PYTHON=/path/to/python` selects the interpreter used by the Node scripts. Run `python3 docs/tools/notebooks.py clean` to delete generated pages, images, and notebook caches.

The printable LaTeX manual remains in `derham.tex`; compile it with `pdflatex derham.tex`. Keep web examples aligned with the package and with this manual.
