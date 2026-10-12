# derham

LaTeX package for de Rham complexes, commuting diagrams, and finite element exterior calculus (FEEC).

```latex
\usepackage{derham}

\[\derhamcomplex\]
\[\derhamcommuting\]
```

The package uses `tikz-cd` and requires a current LaTeX installation. Place `derham.sty` beside your document, or install it in a local TeX tree. Build the manual with `pdflatex derham.tex` (twice for the table of contents), or use `l3build doc`. The generated manual is available as [`output/pdf/derham.pdf`](output/pdf/derham.pdf).

Version 0.3 supports arbitrary positive dimensions for generic/forms notation, vector notation in dimensions 1–3, cross-degree named-row connections, scoped diagram and arrow styling, mapped-domain and coefficient-space diagrams, and generic primal/dual and broken layouts. Spaces, operators, and inter-row maps can be customized independently. See the [manual](derham.pdf), [manual source](derham.tex), and [specification](SPEC.md).

Additional one-command diagrams:

```latex
\[\derhammapped[dimension=2,notation=forms,spaces=sobolev]\]
\[\derhamcoefficients[dimension=3]\]
\[\derhamdual[dimension=2]\]
\[\derhambroken[dimension=2]\]
```

Run `l3build check` for regression tests. The [paper-based gallery PDF](output/pdf/paper-gallery.pdf), its [source](examples/paper-gallery.tex), and other examples are available here. Run `l3build ctan` to create a submission archive under `build/distrib/`; review the archive before uploading. Licensed under LPPL 1.3c or later.
