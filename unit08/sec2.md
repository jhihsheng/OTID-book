# Automatic Differentiation Through Physics

## Differentiating through a linear solve

A simulation is not a chain of `sin` and `exp` — its heart is `x = solve(A(p), b)`. What should AD do when it meets a solver? The naive answer — trace *into* the solver and differentiate every LU pivot or CG iteration — is legal but awful: the tape is enormous, and if the solver is iterative and stopped at tolerance, AD faithfully differentiates the *truncated iteration* rather than the mathematical solution.

The right answer treats the solve as a single primitive with a *custom derivative rule*, derived from the **implicit-function-theorem view**: the output $\boldsymbol{x}(\boldsymbol{p})$ is defined implicitly by $\boldsymbol{A}(\boldsymbol{p})\boldsymbol{x}=\boldsymbol{b}$, so differentiating the *defining equation*（exactly Unit 7's {eq}`eq-u7-dxdp`）gives the exact sensitivity of the exact solution — regardless of how the solver found it. The reverse-mode（VJP）rule that falls out is precisely: solve one transposed system, then form sparse inner products.

```{important}
**Theorem（the course's loop, closed）.** *Reverse-mode automatic differentiation, applied to a program containing a linear solve equipped with its implicit-function derivative rule, produces exactly the adjoint method of Unit 7: the VJP of the solve is the adjoint solve $\boldsymbol{A}^{\top}\boldsymbol{\lambda}=(\partial J/\partial\boldsymbol{x})^{\top}$, and the resulting parameter gradient is {eq}`eq-u7-grad`.* The adjoint method is not a separate technique to memorize — it is what the chain rule *does* to a solver when run backwards. Backpropagation（Unit 4）, the adjoint method（Unit 7）, and reverse-mode AD（this unit）are one algorithm wearing three costumes.
```

## Time-stepping and checkpointing

Reverse mode must *cache the forward pass*. For an FDTD simulation with $10^5$ time steps over a $10^6$-cell grid, storing every intermediate field means terabytes — the honest reason「just autograd the simulator」fails for time-domain solvers. **Checkpointing** is the standard trade: store snapshots only at selected steps, and *recompute* the forward segments between them during the reverse sweep — memory drops dramatically for a modest factor of extra compute, tunable along a memory↔time curve. This is why Meep's adjoint solver is engineered the way it is（recall also Unit 7 sec 2: the adjoint field propagates *backward in time*）, and why FDTD gradients are memory-hungry even with good engineering.

## The ecosystem the labs actually use

- **`autograd`**: reverse-mode AD over plain NumPy code. Small, transparent — and the layer that lets [notebooks 08–09](../labs/adjoint.md) write the FoM *as an ordinary Python function* of the fields: **Meep's adjoint solver** computes $\delta J/\delta\varepsilon$ through the simulation, `autograd` differentiates your FoM code and the filter/project chain of Unit 7 sec 3, and the chain rule glues them.
- **`nlopt`**: consumes those gradients — CCSA/MMA and L-BFGS（Unit 3）with bound constraints.
- **JAX**, in one paragraph: autograd's industrial successor — same functional style plus `jit` compilation, `vmap` batching, and GPU/TPU execution; increasingly the substrate for differentiable-physics research.
- **PyTorch**, in one paragraph: dynamic-graph reverse mode built for deep learning（Unit 4）; the right tool when your design problem *contains* a neural network（surrogates and generative models, Unit 6 sec 3）.

## Failure modes（read before debugging）

- **Non-differentiable operations.** `round`, `argmax`, thresholds: derivative zero almost everywhere — the optimizer receives silence, not guidance. Remedy: smooth surrogates（the tanh projection {eq}`eq-u7-project` exists precisely to replace a hard threshold）.
- **Truncated inner iterations.** An inner solver converged to $10^{-2}$ gives gradients wrong at $10^{-2}$ — AD differentiates what you computed, not what you meant. Tighten tolerances, or use the implicit rule at the converged solution.
- **Hidden randomness.** A stochastic simulation differentiated naively differentiates *one noise draw*; fix the seed（sec 3）or use dedicated stochastic-gradient machinery.
```{tip}
The universal sanity check, used by every practitioner and by Meep's own test suite: compare the AD/adjoint gradient against a central finite difference at $h\approx10^{-5}$ for a *few random parameters*. Agreement to $\sim10^{-6}$: trust the gradient. Disagreement: one of the failure modes above, almost always. Two minutes of checking saves days of optimizing in the wrong direction.
```
