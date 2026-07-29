# What Is Optimization?

## The standard form

Every problem in this course, from fitting a line to designing a photonic device, will be written in one standard form:

$$
\min_{\boldsymbol{x}\in\Omega} \; f(\boldsymbol{x}),
$$ (eq-u1-standard)

where $f:\mathbb{R}^n\to\mathbb{R}$ is the **objective function**（目標函數）, the vector $\boldsymbol{x}=(x_1,\dots,x_n)^{\top}$ collects the **decision variables**（設計變數）, and $\Omega\subseteq\mathbb{R}^n$ is the **feasible set**（可行集合）— the designs we are allowed to choose. Maximization is included for free: maximizing $f$ is minimizing $-f$. A point $\boldsymbol{x}^{*}$ solving {eq}`eq-u1-standard` is a **minimizer**; the value $f(\boldsymbol{x}^{*})$ is the minimum. C&Z Ch. 1 fixes this vocabulary and the vector notation we use throughout: vectors are bold lowercase columns, matrices bold uppercase, scalars italic.

Writing a real engineering wish in the form {eq}`eq-u1-standard` — choosing what $\boldsymbol{x}$, $f$, and $\Omega$ are — is itself a skill（最佳化問題建模, official course goal #2）, and Unit 2 opens with a worked modeling example. Here we survey the *kinds* of problems the form can hide, because the kind dictates the method.

## A taxonomy of problems

**Unconstrained vs constrained.** If $\Omega=\mathbb{R}^n$ the problem is unconstrained; otherwise constraints（bounds, equalities, inequalities）carve out $\Omega$. Most of this course lives in the unconstrained case or handles simple bounds; that is where the classic machinery is cleanest.

**Continuous vs discrete.** Layer thicknesses vary continuously; a phase shifter that must be $0$ or $\pi$ is binary. Discrete variables break the very idea of「move a little bit downhill」, and will demand entirely different tools（Unit 5）.

**Convex vs nonconvex.** In a convex problem every local valley is the global one; in a nonconvex landscape — the rule in photonics — many valleys coexist and a local method finds only one of them.

**Local vs global.** Do we want *a* good design nearby, or *the* best design anywhere? Local answers are cheap; global guarantees are expensive and usually replaced by restarts and heuristics.

```{important}
**The organizing fork of this course: gradient-based vs gradient-free.**
If $f$ is smooth, its gradient exists and can be computed at reasonable cost, gradient-based methods（Units 2–4, 7–8）are unbeatable: each evaluation tells you *which direction* to move. If the variables are discrete, the landscape rugged, or the simulator a black box, gradient-free and stochastic methods（Unit 5: Monte Carlo, GA/PSO/DE, simulated and quantum annealing）take over. Every design problem you meet later sorts itself onto one side of this fork — and the two Applications threads of the course（濾波器反向設計 → gradient route; 1D 光柵設計 → annealing route）are precisely its two branches.
```

## Three photonics problems to keep in mind

The following three running examples come from the course's own labs; we will formalize each one as theory arrives.

1. **Multilayer filter design（TMM）.** $\boldsymbol{x}\in\mathbb{R}^{10}$ = layer thicknesses; $f$ = mismatch between the transmission spectrum $T(\lambda;\boldsymbol{x})$, computed by the transfer-matrix method, and a target spectrum. Smooth, cheap to evaluate, moderate dimension — the perfect customer for the gradient family of Unit 3. This is [Mini-project I](../labs/tmm.md).
2. **EOT plasmonic lattice.** A silver film with a subwavelength hole array shows extraordinary optical transmission; $\boldsymbol{x}$ = a few lattice/geometry parameters, but each $f(\boldsymbol{x})$ costs a full FDTD simulation. Few parameters, expensive black-box evaluations — parameter scans and heuristics earn their keep. This is [Mini-project II](../labs/eot.md).
3. **Waveguide-bend topology optimization.** Every pixel of a design region carries a density $\rho\in[0,1]$: thousands of decision variables. Gradient methods seem hopeless — until the adjoint trick（Unit 7）delivers *all* thousands of partial derivatives for the price of two simulations. The result（watch `bend_waveguide.mp4` on the [adjoint module page](../labs/adjoint.md)）is a freeform structure no human would draw.

```{figure} ../assets/u01_roadmap.png
:name: fig-u1-roadmap
:width: 92%

How the theory units（Part I）feed the hands-on modules（Part II）. The three running examples above are the tmm, eot, and adjoint columns.
```

The rest of this unit rebuilds the two pieces of mathematics every branch of the roadmap relies on: [linear algebra](sec2.md) and [multivariable calculus with a little geometry](sec3.md).
