---
title: Mathematical conventions
description: What the diagram presets label and what they leave to the author.
---

The default generic sequence is $V^0 \xrightarrow{d^0} V^1 \to \cdots \xrightarrow{d^{n-1}} V^n$. The discrete row uses $V_h^k$ and $d_h^k$; the default inter-row maps are $\pi_h^k$. These are labels. The package does not define the spaces, verify that $d^{k+1}d^k=0$, or prove a diagram commutes.

With `notation=forms,spaces=sobolev`, continuous spaces are $H\Lambda^k(\Omega)$. In vector notation, the three-dimensional preset is $H^1(\Omega) \xrightarrow{\operatorname{grad}} H(\operatorname{curl};\Omega) \xrightarrow{\operatorname{curl}} H(\operatorname{div};\Omega) \xrightarrow{\operatorname{div}} L^2(\Omega)$. The two-dimensional curl convention is scalar valued. Supply explicit labels for other vector proxies or boundary conditions.

For a geometric map $F:\widehat\Omega\to\Omega$, the pullback $F^*$ maps forms on $\Omega$ to forms on $\widehat\Omega$. The mapped preset follows this contravariant direction. If you reverse the geometric map, the pullback arrow reverses accordingly. A pushforward is a different operation and needs its own explicitly defined label and hypotheses.

The coefficient diagram uses degree-of-freedom labels and incidence operators as defaults. No orthonormal basis or identity mass matrix is implied. The dual and broken diagrams are editable algebraic layouts; their weak operators, projections, and pairings depend on the author's discretization.

Adding zero objects changes the drawing, not the mathematical status of the sequence. Exactness and commutativity require separate arguments in the paper.
