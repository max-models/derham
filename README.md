# derham

`derham` is a LaTeX package for de Rham complexes, commuting diagrams, and finite element exterior calculus (FEEC). It builds diagrams from spaces and maps using `tikz-cd`.

## Quick start

Place `derham.sty` beside your document, or install it in your local TeX tree. The package requires a current LaTeX installation with `amsmath` and `tikz-cd`.

```latex
\documentclass{article}
\usepackage{derham}
\begin{document}
\[\derhamcomplex\]
\[\derhamcommuting\]
\end{document}
```

## Examples

### A 3D vector-calculus complex

```latex
\[\derhamcomplex[dimension=3,notation=vector,spaces=sobolev]\]
```

![A de Rham sequence from H1 through H(curl) and H(div) to L2](docs/images/complex.png)

This uses the familiar grad, curl, and div labels. The [example source](examples/readme-complex.tex) compiles on its own.

### A continuous and discrete commuting diagram

```latex
\[\derhamcommuting[
  dimension=2,
  notation=forms,
  custom-spaces={H\Lambda^0(\Omega),H\Lambda^1(\Omega),H\Lambda^2(\Omega)},
  custom-discrete-spaces={V_h^0,V_h^1,V_h^2},
  maps={\Pi_h^0,\Pi_h^1,\Pi_h^2}
]\]
```

![Two aligned de Rham complexes joined by projection arrows](docs/images/commuting.png)

The spaces, horizontal operators, and vertical maps can be customized independently. A drawn square states the intended diagram; it does not prove that the chosen maps commute. See the [example source](examples/readme-commuting.tex).

### Physical and reference domains

```latex
\[\derhammapped[dimension=2,notation=forms,
                spaces=sobolev,pullback=F^*]\]
```

![Physical and reference de Rham complexes connected by pullback arrows](docs/images/mapped.png)

For `F: \widehat\Omega \to \Omega`, the pullback arrows point from physical to reference spaces. The [example source](examples/readme-mapped.tex) compiles on its own.

### Build a diagram from named rows

Use `derhamdiagram` when you need more than two rows or an arrow between different degrees:

```latex
\[
\begin{derhamdiagram}[dimension=2,notation=forms,row-sep=huge]
  \derhamrow[name=physical,kind=continuous]
  \derhamrow[name=reference,kind=reference]
  \derhamconnect[from=physical,to=reference,operator=F^*]
  \derhamconnect[from=physical,to=reference,
                 from-degree=0,to-degree=1,operator=T]
\end{derhamdiagram}
\]
```

The extra `T` arrow is illustrative; define its mathematical meaning for your application. The [manual](output/pdf/derham.pdf) documents the full API, including coefficient-space, dual, broken FEEC, and styling options.

## More examples and development

The [paper-based gallery PDF](output/pdf/paper-gallery.pdf) has diagrams adapted from FEEC sources, with [LaTeX source](examples/paper-gallery.tex). More compilable examples are in [`examples/`](examples/).

Run `l3build check` for regression tests, `l3build doc` to build the manual, or `l3build ctan` to prepare a CTAN submission archive. See the [specification](SPEC.md) and [changelog](CHANGELOG.md). Licensed under LPPL 1.3c or later.
