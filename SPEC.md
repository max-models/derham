# derham development specification

## 1. Goal

Build `derham`, a LaTeX package for de Rham complexes, commuting diagrams, and finite element exterior calculus (FEEC). Its main use cases include structure-preserving numerical methods, electromagnetic and plasma simulations, compatible finite elements and splines, and geometric particle-in-cell methods. The diagrams used in published FEEC and geometric PIC papers, especially work in the tradition of Eric Sonnendrücker, should guide examples and visual regression checks.

| Item | Decision |
| --- | --- |
| GitHub repository | `derham` |
| CTAN package | `derham` |
| Package file | `derham.sty` |
| Manual | `derham.pdf`, built from `derham.tex` |
| License | LPPL 1.3c |
| Main dependencies | `tikz-cd`, `amsmath`, and LaTeX3 facilities in the current LaTeX kernel |
| Build and regression testing | `l3build` |

Package description: **LaTeX package for de Rham complexes, commuting diagrams, and finite element exterior calculus (FEEC).**

The package is a semantic layer over `tikz-cd`. Users name spaces, operators, maps, and their relationships; the package handles diagram layout. It must not claim mathematical exactness, invertibility, or commutativity merely because arrows were drawn.

## 2. Design rules

1. A standard three-dimensional complex and commuting diagram each require one command.
2. Every mathematical label can be replaced independently, including each space, horizontal arrow, vertical arrow, and coefficient-space map.
3. Shared diagram data and rendering logic power both presets and the compositional API. Avoid separate hard-coded diagrams for every command.
4. Local options override global settings. Invalid values and unknown keys produce actionable package errors.
5. Defaults must be mathematically stated in the manual; where conventions vary, expose them as explicit presets or user-supplied labels.
6. Keep the initial implementation in one `.sty` file unless splitting it clearly reduces complexity. Do not alter global TikZ settings or common user macros.
7. Preserve normal math fonts and readable sizing. Do not silently scale an oversized diagram.

## 3. Release plan

### Phase 1: first working release

Implement `\derhamsetup`, `\derhamcomplex`, and `\derhamcommuting`, with:

- dimensions 1, 2, and 3;
- generic, differential-form, and vector-calculus notation where mathematically defined;
- continuous and discrete complexes;
- per-position spaces and horizontal operators, plus per-column vertical maps;
- optional initial and terminal zero objects and truncated subsequences;
- configurable spacing and basic arrow styling;
- examples, a manual, `l3build` regression tests, and CI.

The first release must be a usable package, not a demonstration of raw TikZ code. Arbitrary finite dimensions are required for the generic/forms representation in the longer-term API; the implementation may initially limit the public dimension key to 1–3 if the limitation is documented and the internal representation is dimension-independent.

### Phase 2: compositional diagram engine

Add named rows and named connections, then build mapped-domain and coefficient-space diagrams through the same engine. Refactor Phase 1 commands to use it without changing their documented behavior.

### Phase 3: specialized FEEC presets

Add primal/dual, strong/weak, broken FEEC, and multipatch diagrams only after each preset's mathematical convention and a representative published example are recorded in the manual and tests.

Advanced possibilities such as DEC, Hodge duality, boundary complexes, Beamer highlighting, notation legends, and externalization are outside the initial release.

## 4. Public interface

### 4.1 Configuration and simple commands

```latex
\usepackage{derham}

\derhamsetup{
  dimension=3,
  notation=vector,
  spaces=generic,
  row-sep=large,
  column-sep=large
}

\derhamcomplex
\derhamcommuting
\derhamcomplex[notation=forms,spaces=sobolev]
```

All public commands accept local key-value options. Define and document the valid values and precedence for each key. `spaces=generic` and `spaces=sobolev` are named presets; a custom list of spaces must have a distinct, unambiguous syntax. The exact list syntax can be chosen during implementation, but it must be concise, robust with braced math expressions, and documented with examples.

Useful customizations should look approximately like:

```latex
\derhamcomplex[
  dimension=3,
  spaces={V^0,V^1,V^2,V^3},
  operators={d^0,d^1,d^2}
]

\derhamcommuting[
  dimension=3,
  notation=forms,
  projection=\pi_h
]
```

Define individual override keys (for example, indexed space, row operator, and vertical-map keys) so users can replace one label without supplying a whole list. Validate list lengths and indices, and report the expected count in errors. A shorthand such as `projection=\pi_h` may generate indexed labels, but a custom vertical-map list or individual overrides must always be available.

### 4.2 Continuous complexes

For the three-dimensional Sobolev/vector preset, render:

```text
H^1(Ω) --grad--> H(curl; Ω) --curl--> H(div; Ω) --div--> L^2(Ω)
```

For forms, render spaces of differential forms joined by exterior derivatives. Do not assume that the usual three-dimensional vector sequence applies unchanged in dimensions 1 or 2; define each preset explicitly and document the adopted identification. Generic notation may use `V^k` and `d^k` without assigning analytic meaning.

Optional zero objects and truncated degree ranges must not silently imply exactness. If any future option visually marks exactness, it must require an explicit user request.

### 4.3 Commuting diagrams

The default form diagram has two aligned rows:

```text
V^0  ----d^0----> V^1  ----d^1----> V^2  ----d^2----> V^3
 |                |                |                |
π_h^0           π_h^1           π_h^2           π_h^3
 |                |                |                |
 v                v                v                v
V_h^0 --d_h^0--> V_h^1 --d_h^1--> V_h^2 --d_h^2--> V_h^3
```

Support independently configured top-row and bottom-row operators, vertical maps, and individual arrow directions. Include projection, interpolation, restriction, inclusion, and custom-map notation without treating their names as mathematical guarantees. A `\derhamcommuting` call communicates the author's intended commutative structure; the package does not verify the identities.

### 4.4 Compositional API, Phase 2

Provide an interface resembling:

```latex
\begin{derhamdiagram}
  \derhamrow[name=physical,kind=continuous]
  \derhamrow[name=reference,kind=reference]
  \derhamconnect[from=physical,to=reference,operator=pullback]
\end{derhamdiagram}
```

The exact syntax may change if TeX parsing or `tikz-cd` rendering calls for it. Requirements are stable unique row IDs, named connections, per-column and individual connections, actionable errors for unknown or duplicate IDs, and layout that does not depend on connection declaration order. Preset commands and this API must share the same row/arrow representation and renderer.

## 5. Phase 2 diagram families

### 5.1 Physical and reference domains

Target command: `\derhammapped`. Support physical domain `\Omega`, reference domain `\widehat\Omega`, corresponding continuous or discrete spaces, exterior derivatives, and configurable geometric mappings. Expose the direction of the geometric map and render pullback arrows in the mathematically correct contravariant direction. Never substitute a pushforward for a pullback by styling alone.

### 5.2 Coefficient spaces

Target command: `\derhamcoefficients`. Relate discrete function spaces to finite-dimensional coefficient spaces using degree-of-freedom and reconstruction maps. Support independently named incidence or discrete derivative operators (`G`, `C`, `D`, or custom labels), arbitrary coefficient dimensions, and different coefficient bases. Do not imply orthonormality or identity mass matrices.

### 5.3 Multilevel diagrams

Allow combinations of physical continuous, reference continuous, physical discrete, reference discrete, and coefficient-space rows. Connections can link corresponding columns or selected individual objects. Permit projection, pullback, degree-of-freedom, reconstruction, and custom maps in the same diagram.

## 6. Phase 3 diagram families

- `\derhamdual`: primal and dual complexes, strong and weak sequences, mass matrices, duality pairings, Hodge maps, configurable indexing and arrow directions.
- Broken FEEC and multipatch presets: conforming and broken spaces, conforming projections, broken operators, patchwise mappings, interpatch continuity, jumps, and traces.

These are configurable *families*, not claims that one convention is universal. Validate presets against representative publications before finalizing them. Keep custom spaces and operators available at every level.

## 7. Layout and compatibility

Use `tikz-cd` as the renderer. Expose row and column separation, node and arrow styles, arrow tips, labels, colors, font size, baseline alignment, and diagram orientation where feasible. Document which commands produce a math object and how to use them in display math, `equation`, and Beamer. Avoid unexpectedly nesting math environments.

Check compilation with pdfLaTeX, LuaLaTeX, and XeLaTeX. Diagrams should align across rows, have legible arrow labels, and fit ordinary paper and presentation layouts with sensible defaults. A wide custom diagram may require user-specified spacing or line layout; explain this in the manual.

## 8. Project files

```text
derham.sty
derham.tex
README.md
LICENSE
CHANGELOG.md
build.lua
examples/
  basic.tex
  continuous.tex
  commuting.tex
  mapped.tex                 # Phase 2
  coefficients.tex           # Phase 2
  primal-dual.tex            # Phase 3
  plasma-feec.tex
testfiles/
  basic.lvt
  basic.tlg
  invalid-options.lvt
  invalid-options.tlg
.github/workflows/ci.yml
```

Add later-phase files when their features are implemented; do not include non-compiling placeholder examples in CI.

## 9. Tests and documentation

Use `l3build` to test the default complex, dimensions 1–3, all supported notation presets, discrete and commuting diagrams, custom spaces and operators, vertical-map overrides, truncation and zero objects, invalid options and references, multiple diagrams, math-environment use, and coexistence with common math packages. Keep expected logs independent of unstable PDF metadata.

Compile representative example PDFs and inspect their visual layout. Published FEEC and geometric PIC diagrams should become regression examples when their notation and source can be reproduced faithfully. Compare mathematical labels, arrow directions, and alignment, not just whether TeX compiles.

The manual must contain installation instructions, a five-minute quick start, an API reference, default conventions, customization, full FEEC commuting examples, mapped-domain and plasma examples as those features land, limitations, and a changelog. Show both LaTeX source and rendered output for every major feature. Provide an example gallery that can be viewed without installing the package.

CI should run `l3build check` and compile the manual and all implemented examples using a suitable TeX Live installation.

## 10. Definition of done for the first release

1. `\usepackage{derham}` loads without errors in supported engines.
2. `\derhamcomplex` and `\derhamcommuting` each produce a useful three-dimensional diagram with one command.
3. Dimensions 1–3 and generic, forms, and applicable vector presets render correctly.
4. Every space, every horizontal operator on either row, and every vertical map can be changed independently.
5. Optional zero objects and partial complexes work and are documented.
6. Standard diagrams take materially less source than equivalent hand-written `tikz-cd`.
7. `l3build check`, manual compilation, and implemented example compilation pass in CI.
8. Rendered examples have been inspected for labels, arrow directions, alignment, clipping, and readability.
9. The public keys, math-mode behavior, and notation conventions are documented.
10. The internal representation can accommodate additional rows and maps without replacing the rendering layer.

## 11. Instructions to the coding agent

1. Inspect the repository and current implementation before editing.
2. Write down the row, object, and arrow representation and the public key schema. Resolve list syntax and math-mode behavior before expanding the API.
3. Implement Phase 1 in small, compiling increments. Keep the public interface consistent.
4. Add examples and meaningful `l3build` tests alongside the features.
5. Compile and visually inspect the manual and example PDFs; correct spacing, labels, directions, and warnings.
6. Record the convention and published source used for any specialized preset.
7. Finish with a concise summary of implemented capabilities, verification performed, and remaining phases.

Prefer mathematical fidelity and consistent alignment over adding presets. In particular, complex arrows, projection arrows, and coefficient-space maps must be independently customizable.
