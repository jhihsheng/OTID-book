# Conjugate Gradient and Quasi-Newton Methods

## Conjugate directions: don't undo your work

The zig-zag of sec 1 wastes effort because each step partially *undoes* the previous ones. Fix the waste by construction. Directions $\boldsymbol{d}^{(0)},\dots,\boldsymbol{d}^{(n-1)}$ are **$\boldsymbol{Q}$-conjugate** if

$$
\boldsymbol{d}^{(i)\top}\boldsymbol{Q}\,\boldsymbol{d}^{(j)}=0
\qquad\text{for all } i\neq j
$$ (eq-u3-conj)

— orthogonality, but measured in the geometry of the quadratic（stretch space by $\boldsymbol{Q}^{1/2}$ and conjugate directions become literally perpendicular）. Conjugate nonzero directions are linearly independent, so $n$ of them span $\mathbb{R}^n$.

**Why $n$ steps suffice.** Expand the displacement to the solution in that basis: $\boldsymbol{x}^{*}-\boldsymbol{x}^{(0)}=\sum_j c_j\boldsymbol{d}^{(j)}$. Conjugacy makes the quadratic $f$ *separable* in these coordinates — the objective splits into $n$ independent one-dimensional quadratics, one per direction — so minimizing exactly along each $\boldsymbol{d}^{(j)}$ once, in any order, nails its coefficient $c_j$ permanently: later line searches cannot disturb earlier ones（that is precisely what {eq}`eq-u3-conj` forbids）. After $n$ exact line searches the quadratic is solved — **exactly, not asymptotically**（C&Z Ch. 10）.

## The conjugate-gradient algorithm

The magic of CG（Hestenes–Stiefel; C&Z Ch. 10）is that the conjugate basis need not be known in advance: each new direction is the current negative gradient, minimally corrected to stay conjugate to the *previous* direction —

$$
\boldsymbol{d}^{(k+1)}=-\boldsymbol{g}^{(k+1)}+\beta_k\,\boldsymbol{d}^{(k)},
$$ (eq-u3-cgdir)

and on a quadratic the single correction in {eq}`eq-u3-cgdir` automatically yields conjugacy to *all* earlier directions. One iteration: exact line search $\alpha_k=-\boldsymbol{g}^{(k)\top}\boldsymbol{d}^{(k)}/\boldsymbol{d}^{(k)\top}\boldsymbol{Q}\boldsymbol{d}^{(k)}$; step; new gradient; then

$$
\beta_k^{\mathrm{FR}}=\frac{\boldsymbol{g}^{(k+1)\top}\boldsymbol{g}^{(k+1)}}{\boldsymbol{g}^{(k)\top}\boldsymbol{g}^{(k)}}
\qquad\text{or}\qquad
\beta_k^{\mathrm{PR}}=\frac{\boldsymbol{g}^{(k+1)\top}\bigl(\boldsymbol{g}^{(k+1)}-\boldsymbol{g}^{(k)}\bigr)}{\boldsymbol{g}^{(k)\top}\boldsymbol{g}^{(k)}} .
$$

On a quadratic, **Fletcher–Reeves** and **Polak–Ribière** coincide. On general $f$ they differ: PR is usually more robust, because when progress stalls（$\boldsymbol{g}^{(k+1)}\approx\boldsymbol{g}^{(k)}$）it gives $\beta\approx0$ and quietly *restarts* from steepest descent, while FR can keep pushing a stale direction. For nonquadratics the standard practice is an explicit **restart**（set $\beta=0$）every $n$ iterations or whenever conjugacy has visibly decayed; between restarts CG behaves locally like its quadratic self on the Taylor model.

The price list is remarkable: CG stores three vectors, needs one gradient per iteration, never touches a matrix — and solves an $n$-dimensional quadratic in at most $n$ iterations（often far fewer when eigenvalues cluster）. It is *the* method for huge sparse systems.

## Quasi-Newton: learn the Hessian as you go

CG refuses to build a Hessian; quasi-Newton methods *reconstruct* one from data the iteration produces anyway. Each step yields a displacement and a gradient change,

$$
\Delta\boldsymbol{x}^{(k)}=\boldsymbol{x}^{(k+1)}-\boldsymbol{x}^{(k)},
\qquad
\Delta\boldsymbol{g}^{(k)}=\boldsymbol{g}^{(k+1)}-\boldsymbol{g}^{(k)},
$$

and for a quadratic these satisfy $\boldsymbol{Q}\,\Delta\boldsymbol{x}^{(k)}=\Delta\boldsymbol{g}^{(k)}$ — each pair is one「measurement」of the Hessian. A quasi-Newton method maintains an approximation $\boldsymbol{H}_k\approx\boldsymbol{F}^{-1}$, takes damped-Newton-style steps $\boldsymbol{d}^{(k)}=-\boldsymbol{H}_k\boldsymbol{g}^{(k)}$ with a line search, and after each step updates $\boldsymbol{H}$ so that it *explains the newest measurement* — the **secant condition**（C&Z Ch. 11）:

$$
\boldsymbol{H}_{k+1}\,\Delta\boldsymbol{g}^{(k)}=\Delta\boldsymbol{x}^{(k)} .
$$ (eq-u3-secant)

This is Unit 2's secant method grown up: $n$ unknowns per row, rank-limited corrections, no second derivatives ever computed.

The classic updates（all satisfy {eq}`eq-u3-secant`; formulas as in C&Z Ch. 11, superscripts $(k)$ suppressed）:

**Rank one（SR1）:**

$$
\boldsymbol{H}_{k+1}=\boldsymbol{H}_k+
\frac{(\Delta\boldsymbol{x}-\boldsymbol{H}_k\Delta\boldsymbol{g})(\Delta\boldsymbol{x}-\boldsymbol{H}_k\Delta\boldsymbol{g})^{\top}}
{(\Delta\boldsymbol{x}-\boldsymbol{H}_k\Delta\boldsymbol{g})^{\top}\Delta\boldsymbol{g}}
$$

— minimal and symmetric, but the denominator can vanish or flip sign, wrecking positive definiteness.

**DFP（rank two）:**

$$
\boldsymbol{H}_{k+1}=\boldsymbol{H}_k
+\frac{\Delta\boldsymbol{x}\,\Delta\boldsymbol{x}^{\top}}{\Delta\boldsymbol{x}^{\top}\Delta\boldsymbol{g}}
-\frac{\boldsymbol{H}_k\Delta\boldsymbol{g}\,(\boldsymbol{H}_k\Delta\boldsymbol{g})^{\top}}{\Delta\boldsymbol{g}^{\top}\boldsymbol{H}_k\Delta\boldsymbol{g}} .
$$ (eq-u3-dfp)

**BFGS（rank two, the workhorse）:**

$$
\boldsymbol{H}_{k+1}=\boldsymbol{H}_k
+\Bigl(1+\frac{\Delta\boldsymbol{g}^{\top}\boldsymbol{H}_k\Delta\boldsymbol{g}}{\Delta\boldsymbol{g}^{\top}\Delta\boldsymbol{x}}\Bigr)
\frac{\Delta\boldsymbol{x}\,\Delta\boldsymbol{x}^{\top}}{\Delta\boldsymbol{x}^{\top}\Delta\boldsymbol{g}}
-\frac{\Delta\boldsymbol{x}\,\Delta\boldsymbol{g}^{\top}\boldsymbol{H}_k+\boldsymbol{H}_k\Delta\boldsymbol{g}\,\Delta\boldsymbol{x}^{\top}}{\Delta\boldsymbol{g}^{\top}\Delta\boldsymbol{x}} .
$$ (eq-u3-bfgs)

Both rank-two updates {eq}`eq-u3-dfp`–{eq}`eq-u3-bfgs` **preserve positive definiteness** whenever $\Delta\boldsymbol{g}^{\top}\Delta\boldsymbol{x}>0$ — a condition a proper line search guarantees — so every direction $-\boldsymbol{H}_k\boldsymbol{g}^{(k)}$ is a certified descent direction. On quadratics with exact line searches both reach the exact solution in $n$ steps（they secretly generate conjugate directions）; on general problems both converge superlinearly, and decades of practice crowned **BFGS** the default: it self-corrects bad Hessian information where DFP lets it linger. When even storing the $n\times n$ matrix $\boldsymbol{H}$ is too much, **L-BFGS** keeps only the last $m\approx5$–$20$ pairs $(\Delta\boldsymbol{x},\Delta\boldsymbol{g})$ and applies $\boldsymbol{H}_k$ implicitly — this is the `L-BFGS-B` of scipy and the workhorse inside `nlopt` that will drive the adjoint-based photonics designs of Unit 7.

```{figure} ../assets/u03_convergence.png
:name: fig-u3-convergence
:width: 88%

One quadratic（$n=20$, $\kappa=100$）, identical exact line searches — only the directions differ. Steepest descent grinds at rate $\bigl(\frac{\kappa-1}{\kappa+1}\bigr)^2\approx0.96$; CG and BFGS terminate at essentially step $n$（their curves coincide — with exact line searches they generate the same conjugate directions; floating-point roundoff delays CG's final plunge by a few iterations）; Newton lands in one step. The vertical axis spans sixteen orders of magnitude.
```

```{seealso}
[labs/opti](../labs/opti.md): notebook 02 runs `scipy.optimize.minimize` with `method='CG'` and `'BFGS'` on test functions — watch the iteration counts reproduce [](#fig-u3-convergence). The L-BFGS driver reappears inside [labs/adjoint](../labs/adjoint.md), wrapped by nlopt, as the outer loop of real inverse design.
```
