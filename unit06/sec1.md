# Forward versus Inverse

## Two directions through Maxwell's equations

The **forward problem** is the physics you know: given a structure — a permittivity distribution $\varepsilon(\boldsymbol{r})$ — solve Maxwell's equations and report the response: a transmission spectrum, a far-field pattern, a mode overlap. Every solver in this course（the TMM of [Mini-project I](../labs/tmm.md), the FDTD of [labs/meep](../labs/meep.md)）computes this map. It is deterministic, single-valued, and — for the linear optics of this course — linear in the *fields*, though emphatically not in the *geometry*.

The **inverse problem** reverses the arrow: given a *desired* response, find a structure that produces it. And here the mathematics turns hostile（[](#fig-u6-fwdinv)）: the inverse assignment is **ill-posed**. It is **non-unique** — wildly different structures can produce indistinguishable spectra（the forward map ignores most microstructural detail, so it cannot be inverted from its output）. And it may be **infeasible** — nothing guarantees any structure achieves your target exactly; the dream spectrum may violate a physical bound or simply lie outside what the allowed materials can do（recall Unit 2's AR coating, whose ideal index did not exist as a material）.

```{figure} ../assets/u06_forward_inverse.png
:name: fig-u6-fwdinv
:width: 95%

Forward: one structure, one response — a function, computed by a Maxwell solver. Inverse: one target, many candidate structures（or none exactly）— not a function, hence not directly computable.
```

## Optimization dissolves the ill-posedness

The field's founding move is to stop asking「which structure has this response?」and ask instead「which structure comes *closest*?」Fix three objects:

1. a **design space** — a parameter vector $\boldsymbol{p}\in\mathbb{R}^{n}$（or $\{0,1\}^n$）and a rule $\boldsymbol{p}\mapsto\varepsilon(\boldsymbol{r})$（sec 2 is entirely about this choice）;
2. a **figure of merit（FoM）** $J(\boldsymbol{p})$ — one number scoring the simulated response against the target, e.g. $J=\sum_k\bigl|T(\lambda_k;\boldsymbol{p})-T^{\text{tgt}}(\lambda_k)\bigr|^2$;
3. **constraints** — material bounds, geometry bounds, and the fabrication rules of sec 2.

Then *inverse design is nothing but* $\min_{\boldsymbol{p}}J(\boldsymbol{p})$ — the standard form of Unit 1, with a Maxwell solve buried inside the objective. Non-uniqueness stops being a paradox and becomes a gift（many optima ⇒ many acceptable designs ⇒ freedom to prefer the manufacturable one）; infeasibility stops being a failure and becomes a number（the residual $J^{*}>0$ tells you *how far* physics is from your wish）. The price: $J$ is nonconvex, every evaluation costs a simulation, and the loop of [](#fig-u6-loop)（sec 3）must be driven by the machinery of Units 2–5.

## Why photonics, why now

Inverse design matured in photonics earlier and harder than in most fields — Molesky et al.（2018）trace the reasons, worth internalizing because they predict where the method travels well:

1. **The physics is linear and exact.** Maxwell's equations in linear media have no turbulence, no chaos: the forward model is *trustworthy*, so an optimizer exploiting it ruthlessly is exploiting truth, not model error.
2. **Fast accurate solvers exist.** Decades of TMM/FDTD/FEM engineering made a single evaluation of $J$ affordable.
3. **Adjoint efficiency.** One pair of simulations yields the gradient with respect to *every* design pixel（Unit 7）— the same two-pass economics that powers deep learning（Unit 4）, available for electromagnetics.
4. **Fabrication caught up.** Nanolithography can now *build* the freeform geometries optimizers propose, closing the loop with experiment.

Where these conditions weaken — strongly nonlinear physics, unreliable models, unmanufacturable outputs — inverse design gets correspondingly harder; knowing the checklist tells you when to trust it.
