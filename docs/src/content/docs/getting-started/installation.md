---
title: Installation
description: Install the LaTeX package and the optional documentation tools.
---

Download [`derham.sty`](https://github.com/max-models/derham/blob/main/derham.sty) and place it beside your `.tex` document, or install it in your local TeX tree. You also need a current LaTeX kernel plus `amsmath`, `amsfonts`, and `tikz-cd` (provided by `texlive-pictures` in TeX Live).

```latex
\documentclass{article}
\usepackage{derham}
\begin{document}
\[\derhamcomplex\]
\end{document}
```

Compile with `pdflatex`, `lualatex`, or `xelatex`. See the [PDF manual](https://github.com/max-models/derham/blob/main/derham.pdf) for a printable reference.

## Work from a checkout

```bash
pdflatex -interaction=nonstopmode -halt-on-error derham.tex
l3build check
```

To build the web guide, install Python 3.10+, Node 22.12+, a TeX Live installation, and the optional Python dependencies in `docs/requirements.txt`.
