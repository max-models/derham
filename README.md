# derham

LaTeX package for de Rham complexes, commuting diagrams, and finite element exterior calculus (FEEC).

```latex
\usepackage{derham}

\[\derhamcomplex\]
\[\derhamcommuting\]
```

The package uses `tikz-cd` and requires a current LaTeX installation. Place `derham.sty` beside your document, or install it in a local TeX tree. Build the manual with `pdflatex derham.tex` (twice for the table of contents), or use `l3build doc`. The generated manual is available as [`output/pdf/derham.pdf`](output/pdf/derham.pdf).

Version 0.2 supports dimensions 1–3, generic/forms/vector notation, continuous and discrete rows, mapped-domain and coefficient-space diagrams, generic primal/dual and broken layouts, and a compositional API for named multilevel diagrams. Spaces, operators, and inter-row maps can be customized independently. See the [manual source](derham.tex) and [specification](SPEC.md) for details and planned features.

Additional one-command diagrams:

```latex
\[\derhammapped[dimension=2,notation=forms,spaces=sobolev]\]
\[\derhamcoefficients[dimension=3]\]
\[\derhamdual[dimension=2]\]
\[\derhambroken[dimension=2]\]
```

Run `l3build check` for regression tests. Examples are in [`examples/`](examples/). Licensed under LPPL 1.3c or later.
