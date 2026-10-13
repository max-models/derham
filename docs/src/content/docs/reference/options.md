---
title: Commands and options
description: Public commands, composition API, and configuration keys.
---

All diagram commands are math objects. Use them in `\[...\]` or another math environment; do not put them inside a `tikzcd` environment.

| Command | Result |
| --- | --- |
| `\derhamcomplex[options]` | One continuous or discrete row |
| `\derhamcommuting[options]` | Continuous and discrete rows with vertical maps |
| `\derhammapped[options]` | Physical and reference rows with pullbacks |
| `\derhamcoefficients[options]` | Discrete function and coefficient rows |
| `\derhamdual[options]` | Primal and dual complexes |
| `\derhambroken[options]` | Conforming and broken complexes |
| `\derhamsetup{options}` | Global defaults; local command options override them |

## Common keys

| Key | Meaning |
| --- | --- |
| `dimension=3` | Positive number of differential steps. Vector notation is supported only in 1–3D. |
| `from=0`, `to=dimension` | Shown degree range; at least one arrow is required. |
| `notation=generic|forms|vector` | Labels for the differentials. |
| `spaces=generic|sobolev` | Continuous-space labels. |
| `discrete=true|false` | Draw the discrete row with `\derhamcomplex`. |
| `zero-start`, `zero-end` | Add endpoint zero objects. These do not assert exactness. |
| `custom-spaces`, `custom-discrete-spaces` | Comma lists with `dimension+1` math labels. |
| `operators`, `discrete-operators` | Comma lists with `dimension` arrow labels. |
| `maps` | Comma list with `dimension+1` vertical-map labels. |
| `space-k`, `discrete-space-k`, `operator-k`, `discrete-operator-k`, `map-k` | Replace a single degree `k`. |
| `projection=\pi_h` | Base label for automatically indexed projection maps. |
| `vertical-direction=down|up` | Direction of inter-row arrows. |
| `map-direction-k=down|up` | Direction override for a single map. |
| `row-sep`, `column-sep` | `tikz-cd` separation values, for example `large`. |
| `arrow-style`, `diagram-style`, `font`, `baseline` | Local rendering options. |

An indexed override takes priority over a list, which takes priority over a preset. A list item containing a comma needs its own braces. Unknown keys, invalid dimensions, bad degree ranges, and wrong list lengths raise package errors.

## Specialized keys

| Diagram | Keys |
| --- | --- |
| Mapped | `geometry-direction=reference-to-physical|physical-to-reference`, `pullback`, `reference-spaces`, `reference-operators` |
| Coefficients | `coefficient-spaces`, `coefficient-operators`, `dof` |
| Dual | `dual-spaces`, `dual-operators`, `duality` |
| Broken | `broken-spaces`, `broken-operators`, `conforming-projection` |

## Compose rows

```latex
\[\begin{derhamdiagram}[dimension=2]
  \derhamrow[name=physical,kind=continuous]
  \derhamrow[name=reference,kind=reference]
  \derhamconnect[from=physical,to=reference,operator=F^*]
\end{derhamdiagram}\]
```

Each `\derhamrow` needs a unique `name`. Its `kind` can be `continuous`, `discrete`, `reference`, `coefficients`, `conforming`, `dual`, or `broken`; `spaces` and `operators` override its labels. `\derhamconnect` accepts `from`, `to`, `operator`, and optional `degree` for one corresponding column. Use both `from-degree` and `to-degree` to connect different columns. Invalid row references are reported.

For detailed rendered examples, see the [tutorial](/derham/guides/derham-tutorial/) and the repository's [`derham.pdf`](https://github.com/max-models/derham/blob/main/derham.pdf).
