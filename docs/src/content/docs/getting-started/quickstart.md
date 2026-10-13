---
title: Quickstart
description: Draw a complex and a FEEC commuting diagram.
---

After `\usepackage{derham}`, put diagrams in math mode:

```latex
\[\derhamcomplex[dimension=3,notation=vector,spaces=sobolev]\]
\[\derhamcommuting[dimension=3,notation=forms,spaces=sobolev]\]
```

The first is the Sobolev sequence from $H^1(\Omega)$ through $H(\operatorname{curl};\Omega)$ and $H(\operatorname{div};\Omega)$ to $L^2(\Omega)$. The second aligns continuous $H\Lambda^k(\Omega)$ and discrete $V_h^k$ spaces with projection arrows $\pi_h^k$.

Change labels independently:

```latex
\[\derhamcommuting[
  dimension=2,
  custom-spaces={X^0,X^1,X^2},
  operators={D_0,D_1},
  maps={P_0,P_1,P_2}
]\]
```

The [executable tutorial](/derham/guides/derham-tutorial/) shows the resulting diagrams alongside the source. The [options reference](/derham/reference/options/) lists all supported keys.
