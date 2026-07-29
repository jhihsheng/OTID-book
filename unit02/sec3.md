# Derivative-Based One-Dimensional Methods and Line Search

## Orders of convergence: the yardstick

To compare methods we grade how fast the error dies. A sequence $x^{(k)}\to x^{*}$ **converges with order $p$** if

$$
\lim_{k\to\infty}\frac{\bigl|x^{(k+1)}-x^{*}\bigr|}{\bigl|x^{(k)}-x^{*}\bigr|^{\,p}}=C
$$ (eq-u2-order)

for some finite $C>0$（C&Z Ch. 7）. Order $p=1$ with $C<1$ is **linear** convergence: each step multiplies the error by roughly $C$, one new correct digit every $\log(0.1)/\log C$ steps — the bracketing regime（$C=0.618$）. Order $p=2$ is **quadratic**: the error is squared each step, so correct digits *double* — from $10^{-2}$ to $10^{-4}$ to $10^{-8}$ in two steps. Between them, $1<p<2$ is superlinear. This yardstick is the entire justification for using derivatives.

## Bisection on $f'$

If $f$ is differentiable and unimodal, the minimizer is the zero crossing of $f'$: negative before, positive after. Evaluate $f'$ at the midpoint of a sign-bracketing interval, keep the half where the sign still changes, repeat. Each step costs one derivative evaluation and halves the interval — linear convergence with rate $C=\tfrac12$, already better than golden section's $0.618$, because a *sign of a derivative* carries more information than a *comparison of two values*.

## Newton's method: use the whole quadratic model

Why settle for the sign of $f'$ when we have $f''$ too? Around the current iterate, Taylor's theorem {eq}`eq-u1-taylor` builds a quadratic model of $f$:

$$
q(x)=f(x^{(k)})+f'(x^{(k)})(x-x^{(k)})+\tfrac12 f''(x^{(k)})(x-x^{(k)})^2 .
$$

Instead of inching downhill, jump straight to the model's minimizer: $q'(x)=0$ gives

$$
x^{(k+1)}=x^{(k)}-\frac{f'(x^{(k)})}{f''(x^{(k)})}.
$$ (eq-u2-newton)

Equivalently, {eq}`eq-u2-newton` is the tangent-line construction for solving $g(x)=0$ with $g=f'$: linearize $g$ at $x^{(k)}$, land where the tangent crosses zero（[](#fig-u2-newton), left）.

**Quadratic convergence（statement）.** If $f$ is smooth enough near $x^{*}$, $f''(x^{*})\neq0$, and $x^{(0)}$ starts *close enough* to $x^{*}$, the Newton iterates converge to $x^{*}$ with order $2$（precise hypotheses in C&Z Ch. 7）. Three digits become six become twelve: in practice Newton finishes in a handful of steps.

**What「close enough」hides.** Newton trusts its quadratic model globally, and the model is only local. Solve $g(x)=\arctan x=0$（the answer is $x^{*}=0$）starting from $x^{(0)}=1.5$: the tangent is so shallow out there that the iterate overshoots to $x^{(1)}\approx-1.69$, then $+2.32$, then $-5.11$ — each overshoot *worse*, a clean divergence（[](#fig-u2-newton), right）. The same iteration started at $x^{(0)}=1.0$ converges quadratically. Newton's speed is real, but it is a *local* promise; far from the solution it needs supervision — which is exactly what line searches（below）provide.

```{figure} ../assets/u02_newton.png
:name: fig-u2-newton
:width: 95%

Newton's tangent construction. Left: solving $x^3-2=0$ — each tangent lands closer, digits doubling（quadratic convergence）. Right: the same construction on $\arctan x$ from $x^{(0)}=1.5$ — the shallow tangents overshoot with growing amplitude and the iteration diverges.
```

## Secant method: Newton without $f''$

Second derivatives are often unavailable or costly. Replace $f''(x^{(k)})$ in {eq}`eq-u2-newton` by the finite difference built from the last two iterates, $\bigl(f'(x^{(k)})-f'(x^{(k-1)})\bigr)/\bigl(x^{(k)}-x^{(k-1)}\bigr)$: the **secant method**. It keeps most of Newton's speed at half the information: convergence order — in the sense of {eq}`eq-u2-order` — $p=(1+\sqrt5)/2\approx1.618$（the golden ratio again — the same quadratic equation $p^2=p+1$, C&Z Ch. 7）. One derivative per step, no second derivatives, superlinear: the secant idea, generalized to $n$ dimensions, becomes the quasi-Newton family that dominates practice（Unit 3）.

## Backtracking and the Armijo condition

In Unit 3, multidimensional methods will generate a *direction* $\boldsymbol{d}$ and then face a one-dimensional problem: how far to step? Solving it *exactly* with golden-section or Newton is wasted effort — the direction is already an approximation. Modern practice demands only a **sufficient decrease**: accept step size $\alpha$ if

$$
f(\boldsymbol{x}+\alpha\boldsymbol{d})\;\le\;f(\boldsymbol{x})+c\,\alpha\,\nabla f(\boldsymbol{x})^{\top}\boldsymbol{d},
$$ (eq-u2-armijo)

the **Armijo condition**: the achieved decrease must be at least a fraction $c$ of what the linear model promised（$c=10^{-4}$ is the standard choice; Kochenderfer & Wheeler, *Algorithms for Optimization*, MIT Press 2019）. **Backtracking** finds such an $\alpha$ by trial halving:

```python
def backtracking(f, x, d, grad_dot_d, alpha=1.0, c=1e-4, beta=0.5):
    while f(x + alpha * d) > f(x) + c * alpha * grad_dot_d:
        alpha = beta * alpha          # halve and retry
    return alpha
```

Because $c$ is tiny, almost any honest decrease passes; the condition exists to reject the one deadly failure mode — steps so long they *increase* $f$（the arctan overshoot, again）. Start from $\alpha=1$ so that when the full Newton-style step is good, it is taken and fast local convergence is preserved.

```{tip}
This is not textbook decoration: `scipy.optimize.minimize`（BFGS, CG, Newton-CG…）spends its inner loop in precisely such a line search — Armijo plus a curvature guard. When scipy prints `Linesearch failed`, equation {eq}`eq-u2-armijo` is the thing that could not be satisfied, usually because the supplied gradient is wrong.
```

**The bridge to Unit 3.** One dimension is now solved machinery: brackets when derivative-free, Newton/secant when smooth, Armijo backtracking when the 1-D problem is only a subroutine. Unit 3 asks the real question — in $\mathbb{R}^n$, *which direction* $\boldsymbol{d}$? — and every answer（steepest descent, Newton, conjugate gradients, BFGS）will delegate its step-size choice right back here.

## Exercises

以簡單與基礎為原則。

**Exercise 1（golden section by hand）.** Run two iterations of golden-section search on $f(x)=(x-1)^2$ over $[0,4]$（use $\rho=0.382$）. Give the interval of uncertainty after each iteration.

```{dropdown} Solution
Iteration 1: interior points $x_1=0+0.382\cdot4=1.528$, $x_2=0+0.618\cdot4=2.472$; $f(1.528)=0.279<f(2.472)=2.167$, so keep $[0,\,2.472]$. Iteration 2: new interval length $2.472$; interior points $0.382\cdot2.472=0.944$ and $0.618\cdot2.472=1.528$ — the second is the reused old point. $f(0.944)=0.003<f(1.528)=0.279$, so keep $[0,\,1.528]$. Uncertainty: $4\to2.472\to1.528$, a factor $0.618$ each time（and $x^{*}=1$ is indeed inside）.
```

**Exercise 2（Newton fast and slow）.** Apply Newton's method {eq}`eq-u2-newton` to $f(x)=x^2$ and to $f(x)=x^4$, both from $x^{(0)}=1$. Compute the first iterates, identify the convergence order in each case, and explain the difference.

```{dropdown} Solution
For $f=x^2$: $x^{(1)}=1-\frac{2\cdot1}{2}=0=x^{*}$ — done in **one step**, because the quadratic model *is* the function. For $f=x^4$: $x^{(k+1)}=x^{(k)}-\frac{4(x^{(k)})^3}{12(x^{(k)})^2}=\tfrac23x^{(k)}$, giving $1,\ \tfrac23,\ \tfrac49,\dots$ — only **linear** convergence with rate $C=2/3$. The quadratic-convergence theorem required $f''(x^{*})\neq0$; here $f''(0)=0$（a degenerate, flat-bottomed minimum）, so Newton loses its superpower.
```

**Exercise 3（Armijo check）.** Let $f(x)=x^2$, current point $x=2$, direction $d=-f'(2)=-4$, and $c=0.1$. Is the Armijo condition {eq}`eq-u2-armijo` satisfied for $\alpha=1$? For $\alpha=0.5$?

```{dropdown} Solution
Here $\nabla f^{\top}d = f'(2)\,d=4\cdot(-4)=-16$. For $\alpha=1$: left side $f(2-4)=f(-2)=4$; right side $4+0.1\cdot1\cdot(-16)=2.4$; $4>2.4$ — **rejected**（the full step overshoots the minimum at $0$）. For $\alpha=0.5$: left side $f(0)=0$; right side $4+0.1\cdot0.5\cdot(-16)=3.2$; $0\le3.2$ — **accepted**. Backtracking from $\alpha=1$ with halving would thus return $\alpha=0.5$（which here lands exactly on the minimizer）.
```

```{seealso}
[labs/opti](../labs/opti.md): notebook 02 drives `scipy.optimize` on problems like these — set `options={'disp': True}` and watch the line-search iterations of this section happen in real output.
```
