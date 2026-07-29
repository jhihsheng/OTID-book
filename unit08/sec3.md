# Numerical-Computing Literacy

## Floating point: the numbers inside the machine

A float64 spends its 64 bits as sign（1）, exponent（11）, and mantissa（52）: about sixteen significant digits over a huge dynamic range. Two consequences run this course's numerics. **Machine epsilon** $\varepsilon_{\text{mach}}=2^{-52}\approx2.2\times10^{-16}$ is the relative graininess of arithmetic: near $1.0$, representable numbers are $\sim10^{-16}$ apart — which is why $\sin(1+10^{-16})$ *equals* $\sin(1)$ and the opening puzzle's difference was exactly zero.

**Catastrophic cancellation**, one worked example. Compute $1-\cos x$ at $x=10^{-8}$. Mathematically the answer is $\tfrac{x^2}{2}=5\times10^{-17}$. But $\cos(10^{-8})=1-5\times10^{-17}$ rounds to exactly $1.0$（the true value sits within half a grain of $1$）, so the subtraction returns **$0$ — a $100\%$ relative error** from two individually perfect evaluations. The information was destroyed by subtracting nearly equal numbers, not by any single rounding. The repair is algebraic, not arithmetic: the identity $1-\cos x=2\sin^{2}(x/2)$ computes $5.0\times10^{-17}$ flawlessly. Moral: **when a formula subtracts nearly equal quantities, rewrite the formula** — the FD roundoff wall of sec 1 was exactly this phenomenon, and so is the numerical noise in badly scaled FoMs（Unit 6）.

## Vectorization, GPUs, reproducibility

**Vectorization.** A Python `for` loop pays interpreter overhead per element; `numpy` executes whole-array operations in compiled loops — routinely one to two orders of magnitude faster, and the difference between a mini-project that runs in minutes and one that runs overnight. This is why the [lab notebooks](../labs/python.md) are written in array style（`x**2 - 10*np.cos(2*np.pi*x)` on whole populations at once — see `figs_src/u05_metaheuristics.py` for the course's own example）, and it is a *readability* discipline too: array code states the mathematics, loops state the bookkeeping.

**GPUs**, one paragraph: a GPU trades a few fast cores for thousands of slow ones — throughput hardware for uniform array operations. Everything vectorized is a candidate; deep learning（Unit 4）and FDTD both live there. The practical entry today is simply running the same array code on an accelerator via JAX/PyTorch（sec 2）.

**Reproducibility.** Stochastic methods（Unit 5）and stochastic training（Unit 4）must be rerunnable: seed explicitly（`rng = np.random.default_rng(seed)`; never rely on global state）, log the seed with the result, and when claiming「method A beats B」, run *many* seeds and show the spread — the honest error bars of [](#fig-u5-bench) are course policy, not decoration.

## The course's software stack, mapped

| Tool | Role | Where you meet it |
|---|---|---|
| `numpy` | arrays, linear algebra | everywhere（U1 math → lab code） |
| `scipy.optimize` | line searches, CG/BFGS/L-BFGS | U2–U3; [labs/opti](../labs/opti.md) |
| `matplotlib` | every figure in this book and your reports | [labs/python](../labs/python.md) |
| `autograd` | reverse-mode AD over numpy | U8; inside the adjoint labs |
| `nlopt` | CCSA/MMA, L-BFGS with bounds | U3, U7; [labs/adjoint](../labs/adjoint.md) |
| Meep | FDTD forward + adjoint solver | U7; [labs/meep](../labs/meep.md)–[adjoint](../labs/adjoint.md) |
| D-Wave Ocean | QUBO tools + quantum annealer access | U5; [labs/qa](../labs/qa.md) |

## Part I, in one picture

```{figure} ../assets/u08_stack.png
:name: fig-u8-stack
:width: 88%

The modern inverse-design stack — Part I's eight units as one working machine.
```

The synthesis, in a paragraph. Fast, trustworthy **forward solvers** rest on **numerical foundations**（this unit）. From there the road forks — the fork first drawn in Unit 1. On the **continuous route**, the **adjoint method**（U7）— which is reverse-mode **AD**（U8）aimed at Maxwell — delivers exact full gradients for two solves, and the **quasi-Newton machinery**（U3, with U2's line searches and optimality certificates）climbs with them, through the fabrication-aware pipeline, to freeform devices. On the **discrete route**, designs that admit no gradient are encoded as **Ising/QUBO problems**（U5, framed by U6）and attacked by **global search** — simulated annealing, quantum hardware, population methods — with U5's honesty about what heuristics do and do not guarantee. Neural networks（U4）sit on both routes: as the largest optimization problems ever solved, and increasingly as surrogates inside the loop. Every box is now yours; **Part II is where you drive the machine** — [the labs](../labs/index.md) await.

## Exercises

以簡單與基礎為原則。

**Exercise 1（dual numbers by hand）.** Using dual arithmetic（$\epsilon^2=0$）, evaluate $f(x)=x\sin x$ at $x=\tfrac{\pi}{2}+1\cdot\epsilon$ and read off $f(\tfrac{\pi}{2})$ and $f'(\tfrac{\pi}{2})$. Check against calculus.

```{dropdown} Solution
$\sin(\tfrac{\pi}{2}+\epsilon)=\sin\tfrac{\pi}{2}+\cos\tfrac{\pi}{2}\,\epsilon=1+0\epsilon$. Product: $(\tfrac{\pi}{2}+\epsilon)(1+0\epsilon)=\tfrac{\pi}{2}+1\cdot\epsilon$. So $f=\tfrac{\pi}{2}$, $f'=1$. Calculus: $f'=\sin x+x\cos x=1+\tfrac{\pi}{2}\cdot0=1$. ✓ The product rule happened by itself — that is the whole point of the algebra $\epsilon^2=0$.
```

**Exercise 2（choose the mode, count the cost）.** Simulations cost one minute each.（a）Gradient of one scalar FoM with respect to $10^4$ design densities: compare finite differences, forward mode, reverse mode.（b）Sensitivity of a full field map（$10^6$ values）with respect to $3$ geometry parameters: which mode now?

```{dropdown} Solution
（a）$n=10^4,\ m=1$. Finite differences: $10^4{+}1$ evaluations $\approx7$ days, half precision. Forward mode: $10^4$ sweeps — same week, exact. **Reverse mode: $\sim2$–$3$ evaluations $\approx2$–$3$ minutes, exact** — the adjoint economics of Unit 7.（b）$n=3,\ m=10^6$: reverse mode would need $10^6$ sweeps; **forward mode needs $3$** — minutes again. The rule is mechanical: count inputs vs outputs, run the sweep along the small side.
```

**Exercise 3（diagnose the pipeline）.** Two colleagues report bugs.（a）「I binarize with `np.round(rho)` before the FDTD call; `autograd` runs fine but every gradient is exactly zero.」（b）「My inner linear solver uses CG with tolerance $10^{-2}$; the adjoint gradient disagrees with a finite-difference check in the third digit, and the optimizer stalls.」Name each failure mode and the standard fix.

```{dropdown} Solution
（a）**Non-differentiable operation**: `round` is piecewise-constant — derivative zero almost everywhere, so zero gradients are the *correct* derivative of the wrong pipeline. Fix: the smooth tanh projection {eq}`eq-u7-project` with $\beta$-continuation（Unit 7）.（b）**Truncated inner iteration**: the gradient faithfully differentiates a solution that is itself only $10^{-2}$-accurate. Fix: tighten the inner tolerance well below the accuracy you need from gradients, or attach the implicit-function（adjoint）rule at the converged solution. In both cases the AD was flawless — the *model handed to it* was the bug, which is the diagnostic mindset to internalize.
```
