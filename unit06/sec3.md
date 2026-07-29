# Method Families and Exemplars

## The loop, and three ways to drive it

Every inverse-design method is the same closed loop（[](#fig-u6-loop)）: parametrize, simulate, score, update, repeat. The families differ only in the **update** box.

```{figure} ../assets/u06_loop.png
:name: fig-u6-loop
:width: 85%

The inverse-design loop. All methods share the structure; they differ in how the update step uses the information a simulation produces.
```

**Adjoint-based topology optimization** — the gradient route at full power. Density parameterization, adjoint gradients（two simulations per iteration, regardless of parameter count）, a quasi-Newton or CCSA optimizer, fabrication filters in the loop. This is the current mainstream of photonic inverse design and the entire subject of Unit 7; the waveguide bend and the freeform filter of [labs/adjoint](../labs/adjoint.md) are its outputs.

**Heuristic pipelines** — the gradient-free route. Discrete or few-parameter designs driven by the Unit 5 toolbox: SA/QA on binary gratings and phase arrays, GA/PSO/DE on few-parameter geometries with expensive black-box solvers. Slower per digit, but indifferent to discreteness, noise, and non-differentiable objectives — and often the only option when the design variables are genuinely binary（[labs/qa](../labs/qa.md)）.

**ML-assisted approaches** — in brief, with the *Photonics Research* **9**(5), B182–B200 (2021) review as the entry point. Three recurring patterns: **surrogate models**（train a network to imitate the solver, then optimize the cheap imitation — with the obvious caveat that the optimizer will exploit surrogate errors as happily as physics）; **tandem networks**（learn an inverse map response→structure directly, dodging non-uniqueness by pairing it with a forward network）; **generative models**（learn a distribution over good structures, then sample）. The sober summary: ML shines where *many related designs* are needed — amortizing solver cost across a family — while for a single one-off design, adjoint TO remains the benchmark to beat.

## What makes a figure of merit good

The FoM is where design intent is encoded, and badly written FoMs are the field's leading cause of garbage-in-garbage-out. A good $J$:

- **is differentiable**（for the gradient route）: smooth surrogates — $\sum_k|T_k-T^{\text{tgt}}_k|^2$ — over hard indicators; if the true goal is worst-case, use a smooth-max, not a literal $\max$;
- **is well-scaled**: comparable terms in comparable units, weights chosen so no single term's gradient drowns the rest（recall $\kappa$, Unit 3 — bad scaling *is* ill-conditioning）;
- **is physically meaningful**: optimize the quantity you will actually measure — a mode overlap, a power ratio — not a numerical proxy that can be gamed（maximizing field intensity at a point, for instance, famously invites the optimizer to build a resonator that helps no device）.

## Local minima, and the working attitude

$J$ is nonconvex; the gradient route lands in a local minimum, full stop（Unit 2's local-vs-global, at industrial scale）. The field's empirical peace with this: in $10^4$-dimensional freeform spaces, *good* local minima are plentiful — different restarts yield different geometries with similar excellent performance（non-uniqueness working *for* you）. Standard hygiene: multistart from varied initial densities（Unit 5 sec 1）, keep the best; treat run-to-run spread as information about the landscape. What the local optimum leaves on the table is bounded by physics, not folklore — performance-bound research（part of the Molesky et al. survey's agenda）quantifies how much better *any* design could possibly do.

**Exemplars.** The course reading list（[resources](../resources.md)）carries the syllabus-chosen examples: an application in *Phys. Rev. Lett.* **122**, 213902 (2019) and one in antenna engineering, *IEEE Trans. Antennas Propag.* **70**(4), 2841–2854 (2022) — the same loop, different wave equation — plus the two Stanford theses（Petykiewicz; Su, 2020）for complete pipelines told start to finish. For this course, the canonical exemplars are the ones you will run yourself: the two threads of the official Applications — 濾波器反向設計 by the gradient route（[labs/tmm](../labs/tmm.md) → [labs/adjoint](../labs/adjoint.md)）and 1D 光柵設計 by the annealing route（[labs/qa](../labs/qa.md)）.

## Exercises

以簡單與基礎為原則。

**Exercise 1（write a FoM）.** A notch filter should transmit $T\ge0.95$ for $1500\text{–}1540$ nm and $1560\text{–}1600$ nm, and block $T\le0.01$ at $1550$ nm. Write a differentiable figure of merit $J(\boldsymbol{p})$ for the gradient route, and point out one deliberate choice you made.

```{dropdown} Solution
One good answer, sampling the bands at wavelengths $\{\lambda_k\}$ and the notch at $\lambda_0=1550$ nm:
$J=w_0\,T(\lambda_0;\boldsymbol{p})^2+\dfrac{w_1}{K}\sum_{k}\bigl(1-T(\lambda_k;\boldsymbol{p})\bigr)^2$.
Deliberate choices worth naming: squared（smooth）penalties rather than hard thresholds — differentiability; averaging over the band（the $1/K$）and weights $w_0,w_1$ balancing one notch term against many band terms — scaling; targeting $T=1$ in the passband rather than exactly $0.95$ — optimize the physical quantity, treat the spec as a check. A minimax variant（optimize the worst wavelength）is legitimate but needs a smooth-max to stay differentiable.
```

**Exercise 2（classify the parameterization — and hence the method）.** For each device, name the parameterization family and the optimization route it calls for:（a）an anti-reflection stack of five layers with adjustable thicknesses;（b）a $2\,\mu\text{m}\times2\,\mu\text{m}$ silicon region whose permittivity is free per $10$-nm pixel;（c）a 1-D grating of 64 cells, each etched or not etched.

```{dropdown} Solution
（a）Few-parameter shape（$\boldsymbol{p}\in\mathbb{R}^5$）: any method works; quasi-Newton with numerical or TMM-analytic gradients is natural（this is Mini-project I）.（b）Density/freeform（$200\times200=4\times10^4$ pixels）: gradient route mandatory — adjoint + L-BFGS/CCSA with filtering and projection（Unit 7; labs/adjoint）.（c）Binary, 64 bits: no gradients exist — heuristic route; encode as Ising/QUBO and anneal, classically or quantumly（Unit 5; labs/qa）. Together the three answers *are* the course's organizing fork.
```

**Exercise 3（concepts, short answers）.**（a）Give two distinct reasons the inverse problem has no well-defined solution map.（b）Why is non-uniqueness an advantage for a designer?（c）A colleague proposes maximizing $|E|^2$ at one point as the FoM for a focusing device — name the risk.

```{dropdown} Solution
（a）Non-uniqueness — many structures share a response（the forward map discards detail）; and infeasibility — the target may be outside what physics/materials permit, so *no* structure maps to it.（b）Among the many near-optimal structures, the designer is free to select for secondary virtues: manufacturability, robustness, footprint — extra optima are extra options.（c）The optimizer can game the proxy: a high-Q resonance at that point boosts $|E|^2$ without focusing anything useful（narrowband, misaligned with the actual application）. Optimize the measurable objective — e.g. power coupled into the intended mode or focal spot integral — not a point value that can be inflated.
```

```{seealso}
The concepts of this unit become hands-on immediately: the loop with a TMM solver in [labs/tmm](../labs/tmm.md), with FDTD in [labs/meep](../labs/meep.md) and [labs/eot](../labs/eot.md), with adjoint gradients in [labs/adjoint](../labs/adjoint.md), and with an annealer in [labs/qa](../labs/qa.md).
```
