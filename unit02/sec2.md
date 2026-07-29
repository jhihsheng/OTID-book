# Bracketing Methods

## Unimodality, and what bracketing can promise

Suppose all we can do is *evaluate* $f$ — no derivatives, perhaps not even a formula, just a slow simulator. On an interval $[a_0,b_0]$ we call $f$ **unimodal** if it has a single minimizer $x^{*}$ there, with $f$ strictly decreasing before $x^{*}$ and strictly increasing after. Unimodality is the license for bracketing: it lets *two* interior evaluations discard a guaranteed-loser piece of the interval.

Place $x_1<x_2$ inside $[a_0,b_0]$. If $f(x_1)<f(x_2)$, the minimizer cannot lie right of $x_2$（walking right from $x_1$ we already saw $f$ go up — past the valley）, so $x^{*}\in[a_0,x_2]$. If $f(x_1)>f(x_2)$, symmetrically $x^{*}\in[x_1,b_0]$. Either way the **interval of uncertainty** shrinks, and we repeat. The whole design question of this section is: *where should $x_1,x_2$ sit?*

## Golden-section search: the ratio derives itself

Two principles fix the answer uniquely.

**Symmetry.** Neither outcome should be luckier than the other, so place the points symmetrically: on a normalized interval $[0,1]$, at $\rho$ and $1-\rho$ with $\rho<\tfrac12$. Both outcomes then leave an interval of the same length $\tau=1-\rho$.

**Reuse.** After the reduction — say we kept $[0,1-\rho]$ — one old evaluation（the point $\rho$）survives inside the new interval. If it happens to sit *exactly where the next iteration needs an interior point*, each subsequent iteration costs only **one** new evaluation instead of two. The new interval has length $\tau$, so its own interior points must sit at $\tau\rho$ and $\tau(1-\rho)=\tau^2$. The surviving point $\rho=1-\tau$ must be one of them, and matching it to the deeper one gives the self-similarity condition

$$
\tau^{2}=1-\tau
\quad\Rightarrow\quad
\tau=\frac{\sqrt{5}-1}{2}\approx0.618,
\qquad
\rho=1-\tau=\frac{3-\sqrt{5}}{2}\approx0.382.
$$ (eq-u2-golden)

The positive root of $\tau^2+\tau-1=0$ is the reciprocal of the golden ratio — hence the name **golden-section search**（C&Z Ch. 7）. Every iteration multiplies the uncertainty by $\tau\approx0.618$ at the price of one evaluation（after the first iteration's two）, so $N$ evaluations leave an uncertainty of $\tau^{N-1}$ of the original interval. The opening puzzle's numbers: $N=20$ gives $0.618^{19}\approx1.1\times10^{-4}$. [](#fig-u2-golden) shows the shrinkage and the reused point.

```{figure} ../assets/u02_golden.png
:name: fig-u2-golden
:width: 88%

Golden-section search on $f(x)=(x-1)^2$ over $[0,4]$. Each bar is one iteration's interval of uncertainty（grey = discarded）; dots are the two interior evaluations, and one of them is always inherited from the previous iteration — the reuse that forces the ratio $0.618$.
```

## Fibonacci search: the optimal budget

If the evaluation budget $N$ is fixed *in advance*, one can do slightly better by letting the placement ratio vary from step to step. The optimal schedule uses the Fibonacci numbers $F_1=F_2=1$, $F_{k+2}=F_{k+1}+F_k$: successive ratios $\rho_k=1-F_{N-k+1}/F_{N-k+2}$, and the final uncertainty is essentially $1/F_{N+1}$ of the initial interval（exactly $(1+2\varepsilon)/F_{N+1}$ with a small guard $\varepsilon$ separating the last two points; statement and proof in C&Z Ch. 7）. This is **provably optimal**: no bracketing strategy with $N$ evaluations can guarantee better. Since $F_{N+1}\sim\tau^{-(N+1)}/\sqrt5$, golden-section is its fixed-ratio limit — asymptotically within a constant factor, which is why in practice the simpler golden-section is the default and Fibonacci is reserved for genuinely precious evaluations.

## Scorecard

| Method | Cost per iteration | Uncertainty after $N$ evaluations | Notes |
|---|---|---|---|
| Uniform grid | $N$ upfront | $\approx 2/(N+1)$ | no adaptivity — pays linearly |
| Trisection（no reuse）| 2 evaluations | $(2/3)^{N/2}\approx0.816^{N}$ | symmetric but wasteful |
| **Golden section** | 1 evaluation（after first） | $0.618^{\,N-1}$ | fixed ratio, simplest adaptive |
| **Fibonacci** | 1 evaluation（after first） | $\approx 1/F_{N+1}$ | optimal for fixed budget（C&Z Ch. 7） |

Two caveats worth stating plainly. Bracketing pays *per digit*: by {eq}`eq-u2-golden`, every extra digit of accuracy costs $\log(0.1)/\log(0.618)\approx4.8$ evaluations — linear convergence in the language of [the next section](sec3.md), which derivative methods will beat spectacularly. But bracketing never asked for derivatives, never needed smoothness beyond unimodality, and is immune to the noise that wrecks finite-difference derivatives — which is why 「when the simulator is expensive, noisy, or a black box, bracket; when derivatives are cheap and trustworthy, differentiate」 is the practical rule, and why the derivative-free half of this course（Unit 5）exists at all.
