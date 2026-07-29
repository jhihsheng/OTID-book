# The Discrete Adjoint Method

## The setting

Discretize any linear physics — Maxwell, acoustics, heat — and a simulation is a linear solve:

$$
\boldsymbol{A}(\boldsymbol{p})\,\boldsymbol{x}=\boldsymbol{b},
$$ (eq-u7-state)

where $\boldsymbol{x}\in\mathbb{R}^{N}$ holds the field degrees of freedom（$N\sim10^{6}$）, $\boldsymbol{b}$ the sources, and the system matrix $\boldsymbol{A}$ depends on the design $\boldsymbol{p}\in\mathbb{R}^{n_p}$（each $p_i$ a pixel density or thickness）. The figure of merit reads off the field: $J=J(\boldsymbol{x}(\boldsymbol{p}))$. We want the full gradient $\mathrm{d}J/\mathrm{d}\boldsymbol{p}$ — every component — to feed the optimizers of Unit 3.

**Why the naive route drowns.** Differentiate {eq}`eq-u7-state` with respect to one parameter $p_i$（product rule; $\boldsymbol{b}$ independent of $\boldsymbol{p}$）:

$$
\boldsymbol{A}\,\frac{\partial\boldsymbol{x}}{\partial p_i}
=-\frac{\partial\boldsymbol{A}}{\partial p_i}\,\boldsymbol{x}
\qquad\Rightarrow\qquad
\frac{\partial\boldsymbol{x}}{\partial p_i}
=-\boldsymbol{A}^{-1}\frac{\partial\boldsymbol{A}}{\partial p_i}\,\boldsymbol{x}.
$$ (eq-u7-dxdp)

Each parameter demands its own solve with the right-hand side $\frac{\partial\boldsymbol{A}}{\partial p_i}\boldsymbol{x}$: the gradient costs $n_p$ simulations — the week-per-step of the opening puzzle.

## Derivation one: regroup the chain rule

Chain rule plus {eq}`eq-u7-dxdp`:

$$
\frac{\mathrm{d}J}{\mathrm{d}p_i}
=\frac{\partial J}{\partial\boldsymbol{x}}\,\frac{\partial\boldsymbol{x}}{\partial p_i}
=-\underbrace{\frac{\partial J}{\partial\boldsymbol{x}}\,\boldsymbol{A}^{-1}}_{\text{does not depend on }i}\;
\frac{\partial\boldsymbol{A}}{\partial p_i}\,\boldsymbol{x}.
$$

There is the trick, sitting in plain sight: the expensive factor $\frac{\partial J}{\partial\boldsymbol{x}}\boldsymbol{A}^{-1}$ — a *row* vector — is the **same for every parameter**. Compute it once, by one linear solve: name it $\boldsymbol{\lambda}^{\!\top}=\frac{\partial J}{\partial\boldsymbol{x}}\boldsymbol{A}^{-1}$, i.e.

$$
\boldsymbol{A}^{\!\top}\boldsymbol{\lambda}
=\Bigl(\frac{\partial J}{\partial\boldsymbol{x}}\Bigr)^{\!\!\top}
$$ (eq-u7-adjoint)

— the **adjoint system**: same matrix（transposed）, new right-hand side supplied by the *objective* instead of the physical source. Then every component of the gradient is an inexpensive inner product:

$$
\frac{\mathrm{d}J}{\mathrm{d}p_i}
=-\,\boldsymbol{\lambda}^{\!\top}\,
\frac{\partial\boldsymbol{A}}{\partial p_i}\,\boldsymbol{x},
\qquad i=1,\dots,n_p .
$$ (eq-u7-grad)

Each $\frac{\partial\boldsymbol{A}}{\partial p_i}$ is sparse — pixel $i$ touches only its own matrix entries — so assembling all $n_p$ components of {eq}`eq-u7-grad` costs about as much as one matrix–vector product.

```{important}
**Two solves, total: one forward（$\boldsymbol{A}\boldsymbol{x}=\boldsymbol{b}$）, one adjoint（{eq}`eq-u7-adjoint`）— independent of the number of design parameters.** The naive count was $n_p+1$. Choosing whether to differentiate *the solution*（$n_p$ solves for $\partial\boldsymbol{x}/\partial p_i$）or *the objective*（one solve for $\boldsymbol{\lambda}$）is the entire content of the method; everything else is bookkeeping. This is the enabling economics of freeform design — the same「all gradients for the price of two evaluations」that backpropagation gave neural networks in Unit 4, and Unit 8 will state the equivalence as a theorem: **the adjoint method is reverse-mode automatic differentiation applied to a linear solver.**
```

## Derivation two: the Lagrangian（Johnson's route）

The regrouping can be made systematic instead of clever — useful when the setting grows hairier（nonlinear physics, time-dependence, multiple constraints）. Append the constraint with a multiplier（Johnson, *Notes on adjoint methods*）:

$$
\mathcal{L}(\boldsymbol{x},\boldsymbol{p},\boldsymbol{\lambda})
=J(\boldsymbol{x})+\boldsymbol{\lambda}^{\!\top}\bigl(\boldsymbol{b}-\boldsymbol{A}(\boldsymbol{p})\boldsymbol{x}\bigr).
$$

Whenever $\boldsymbol{x}$ solves {eq}`eq-u7-state`, the parenthesis vanishes and $\mathcal{L}=J$ for *any* $\boldsymbol{\lambda}$ — so we may differentiate $\mathcal{L}$ instead of $J$ and *choose* $\boldsymbol{\lambda}$ to our convenience:

$$
\frac{\mathrm{d}J}{\mathrm{d}p_i}
=\underbrace{\Bigl(\frac{\partial J}{\partial\boldsymbol{x}}-\boldsymbol{\lambda}^{\!\top}\boldsymbol{A}\Bigr)}_{\text{kill this by choosing }\boldsymbol{\lambda}}
\frac{\partial\boldsymbol{x}}{\partial p_i}
\;-\;\boldsymbol{\lambda}^{\!\top}\frac{\partial\boldsymbol{A}}{\partial p_i}\boldsymbol{x}.
$$

The first bracket multiplies the unknown, expensive $\partial\boldsymbol{x}/\partial p_i$; annihilate it by demanding $\boldsymbol{\lambda}^{\!\top}\boldsymbol{A}=\partial J/\partial\boldsymbol{x}$ — which is exactly the adjoint system {eq}`eq-u7-adjoint` — and what survives is exactly the gradient formula {eq}`eq-u7-grad`. Same two equations, now derived by design rather than by inspection: *choose the multiplier so that the sensitivity of the state never needs computing.* Nothing here used linearity of $J$（only its differentiability）, and the pattern generalizes: nonlinear state equations, time-stepping（where the adjoint runs *backward* in time）, PDE-constrained control — all one Lagrangian away.

The formula {eq}`eq-u7-grad` is abstract linear algebra; [the next section](sec2.md) reads it physically, where $\boldsymbol{A}$ is Maxwell's operator and $\boldsymbol{\lambda}$ turns out to be a second electromagnetic field with a story of its own.
