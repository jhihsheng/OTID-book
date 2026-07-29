# Geometry and Calculus

## Segments, hyperplanes, convex sets

The **line segment** between $\boldsymbol{x}$ and $\boldsymbol{y}$ is the set $\{\alpha\boldsymbol{x}+(1-\alpha)\boldsymbol{y}:\alpha\in[0,1]\}$. A **hyperplane** $\{\boldsymbol{x}:\boldsymbol{a}^{\top}\boldsymbol{x}=b\}$ generalizes a line/plane to $\mathbb{R}^n$; it splits space into two **half-spaces** $\boldsymbol{a}^{\top}\boldsymbol{x}\le b$ and $\boldsymbol{a}^{\top}\boldsymbol{x}\ge b$. A set $C$ is **convex** if for *every* pair of its points the whole segment stays inside（[](#fig-u1-convex)）. Half-spaces are convex, intersections of convex sets are convex — which is why the feasible polytopes of linear programming（Unit 3 sec 4）are convex.

```{figure} ../assets/u01_convex.png
:name: fig-u1-convex
:width: 92%

The chord test. (a) In a convex set every chord stays inside. (b) One escaping chord（red portion）is enough to disqualify the set.
```

## Level sets

The **level set** of $f$ at height $c$ is $S_c=\{\boldsymbol{x}:f(\boldsymbol{x})=c\}$ — the contour lines of a topographic map. For the quadratic $f(\boldsymbol{x})=\tfrac12\boldsymbol{x}^{\top}\boldsymbol{Q}\boldsymbol{x}$ with $\boldsymbol{Q}>0$, the level sets are concentric ellipses whose axes point along the eigenvectors of $\boldsymbol{Q}$, with lengths $\propto1/\sqrt{\lambda_i}$（[](#fig-u1-levelsets); this is {eq}`eq-u1-qform` drawn as a picture）. Two things to notice now and remember in Unit 3: the gradient is everywhere **perpendicular to the level set**, and the more elongated the ellipses（large $\kappa=\lambda_{\max}/\lambda_{\min}$）, the more misleading「straight downhill」becomes.

```{figure} ../assets/u01_levelsets.png
:name: fig-u1-levelsets
:width: 78%

Level sets of $f=\frac12\boldsymbol{x}^{\top}\boldsymbol{Q}\boldsymbol{x}$, $\boldsymbol{Q}=\bigl[\begin{smallmatrix}3&1\\1&2\end{smallmatrix}\bigr]$, with the gradient field $\nabla f=\boldsymbol{Q}\boldsymbol{x}$（orange）and the eigenvector axes（green）. Gradients are orthogonal to contours and grow with distance from the minimizer.
```

Why perpendicular? Move along any curve lying inside $S_c$: $f$ is constant on it, so by the chain rule below, $\nabla f^{\top}(\text{tangent vector})=0$.

## Limits and continuity（briskly）

A sequence $\boldsymbol{x}^{(k)}\to\boldsymbol{x}^{*}$ if $\|\boldsymbol{x}^{(k)}-\boldsymbol{x}^{*}\|\to0$; $f$ is continuous if it commutes with limits. We need this vocabulary for exactly one purpose: optimization algorithms *produce sequences of iterates*, and「the method converges」means precisely $\boldsymbol{x}^{(k)}\to\boldsymbol{x}^{*}$. Orders of convergence（how *fast*）are defined in Unit 2.

## Derivatives in several variables

For $f:\mathbb{R}^n\to\mathbb{R}$, the **gradient** collects the partials into a column vector, and the **Hessian** collects the second partials into a symmetric matrix（symmetric whenever $f$ is twice continuously differentiable）:

$$
\nabla f(\boldsymbol{x})=\begin{bmatrix}\dfrac{\partial f}{\partial x_1}\\[2pt]\vdots\\[2pt]\dfrac{\partial f}{\partial x_n}\end{bmatrix},
\qquad
\boldsymbol{F}(\boldsymbol{x})=\left[\frac{\partial^2 f}{\partial x_i\,\partial x_j}\right]_{i,j=1}^{n}.
$$

For a vector-valued $\boldsymbol{h}:\mathbb{R}^n\to\mathbb{R}^m$ the derivative is the $m\times n$ **Jacobian** $\mathrm{D}\boldsymbol{h}$, whose rows are the gradients（transposed）of the components. Notation follows C&Z: we write $\boldsymbol{F}$ for the Hessian of the objective.

**Chain rule.** If $\boldsymbol{x}(t)$ is a differentiable curve, then $\dfrac{\mathrm{d}}{\mathrm{d}t}f(\boldsymbol{x}(t))=\nabla f(\boldsymbol{x}(t))^{\top}\,\boldsymbol{x}'(t)$. Composed maps multiply Jacobians — the fact that Unit 4's backpropagation and Unit 8's automatic differentiation exploit systematically.

**Directional derivative.** Fix a direction $\boldsymbol{d}$ and apply the chain rule to $g(\alpha)=f(\boldsymbol{x}+\alpha\boldsymbol{d})$:

$$
\left.\frac{\mathrm{d}}{\mathrm{d}\alpha}f(\boldsymbol{x}+\alpha\boldsymbol{d})\right|_{\alpha=0}
=\boldsymbol{d}^{\top}\nabla f(\boldsymbol{x}).
$$ (eq-u1-dirderiv)

Over unit vectors $\|\boldsymbol{d}\|=1$, Cauchy–Schwarz {eq}`eq-u1-cs` bounds {eq}`eq-u1-dirderiv` by $\|\nabla f\|$, with equality exactly at $\boldsymbol{d}=\nabla f/\|\nabla f\|$. **The gradient is the direction of steepest ascent, and $-\nabla f$ of steepest descent** — the founding observation of Unit 3.

## Taylor's theorem to second order

The single most-used result of this unit（C&Z Ch. 5）. If $f$ is twice continuously differentiable, then for a step $\boldsymbol{d}$,

$$
f(\boldsymbol{x}+\boldsymbol{d})
= f(\boldsymbol{x})
+ \nabla f(\boldsymbol{x})^{\top}\boldsymbol{d}
+ \tfrac12\,\boldsymbol{d}^{\top}\boldsymbol{F}(\boldsymbol{x})\,\boldsymbol{d}
+ o\!\left(\|\boldsymbol{d}\|^{2}\right),
$$ (eq-u1-taylor)

and in mean-value form the remainder can be written exactly by evaluating $\boldsymbol{F}$ at an intermediate point $\boldsymbol{x}+\gamma\boldsymbol{d}$, $\gamma\in(0,1)$.

```{important}
**Taylor's theorem {eq}`eq-u1-taylor` is the engine of the whole course.** Near any design, the landscape *is*（to second order）a quadratic: a linear tilt $\nabla f^{\top}\boldsymbol{d}$ plus a curvature term $\frac12\boldsymbol{d}^{\top}\boldsymbol{F}\boldsymbol{d}$. Optimality conditions（Unit 2）read the tilt and the curvature's sign; Newton's method（Units 2–3）minimizes the quadratic model outright; convergence rates（Unit 3）come from how good the model is; even the adjoint method（Unit 7）is the linear term computed cleverly. Whenever a later unit says「expand and keep two orders」, it is citing this equation.
```

## Exercises

以簡單與基礎為原則——each solution is one short computation.

**Exercise 1（definiteness）.** Determine whether $\boldsymbol{Q}=\begin{bmatrix}4&1&0\\1&3&1\\0&1&2\end{bmatrix}$ is positive definite.

```{dropdown} Solution
Leading principal minors: $\Delta_1=4>0$; $\Delta_2=4\cdot3-1=11>0$; $\Delta_3=\det\boldsymbol{Q}=4(3\cdot2-1\cdot1)-1(1\cdot2-1\cdot0)+0=20-2=18>0$. By Sylvester's criterion $\boldsymbol{Q}>0$.
```

**Exercise 2（gradient and Hessian）.** For $f(\boldsymbol{x})=3x_1^2+2x_1x_2+x_2^2-4x_1+2$, compute $\nabla f$ and $\boldsymbol{F}$.

```{dropdown} Solution
$\nabla f(\boldsymbol{x})=\begin{bmatrix}6x_1+2x_2-4\\ 2x_1+2x_2\end{bmatrix}$, $\qquad \boldsymbol{F}=\begin{bmatrix}6&2\\2&2\end{bmatrix}$（constant — $f$ is quadratic）.
```

**Exercise 3（Taylor expansion）.** Expand $f(\boldsymbol{x})=e^{x_1}\sin x_2$ to second order about $\boldsymbol{0}$.

```{dropdown} Solution
$f(\boldsymbol{0})=0$; $\nabla f=(e^{x_1}\sin x_2,\; e^{x_1}\cos x_2)^{\top}\big|_{\boldsymbol{0}}=(0,1)^{\top}$; Hessian entries $f_{11}=e^{x_1}\sin x_2\to0$, $f_{12}=e^{x_1}\cos x_2\to1$, $f_{22}=-e^{x_1}\sin x_2\to0$, so $\boldsymbol{F}(\boldsymbol{0})=\bigl[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\bigr]$. By {eq}`eq-u1-taylor`, $f(\boldsymbol{d})\approx d_2+d_1d_2$.
```

**Exercise 4（stationary point）.** Find the stationary point of the $f$ in Exercise 2 and classify it.

```{dropdown} Solution
$\nabla f=\boldsymbol{0}$: from $2x_1+2x_2=0$, $x_2=-x_1$; substituting, $6x_1-2x_1=4\Rightarrow x_1=1$, $x_2=-1$. The Hessian $\bigl[\begin{smallmatrix}6&2\\2&2\end{smallmatrix}\bigr]$ has $\Delta_1=6>0,\ \Delta_2=8>0$, hence $\boldsymbol{F}>0$: $(1,-1)^{\top}$ is a strict local minimizer — and, since a PD quadratic is convex, the global one, with $f(1,-1)=0$.（Unit 2 turns this two-step check into the formal FONC/SOSC conditions.）
```

```{seealso}
Hands-on companions: [labs/python](../labs/python.md) plots level sets and vector fields exactly like [](#fig-u1-levelsets); [labs/tmm](../labs/tmm.md) is where the linear algebra of [the previous section](sec2.md) designs a real filter.
```
