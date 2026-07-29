# A Glance at Linear Programming

## When everything is linear

This unit assumed smooth nonlinear objectives. The opposite extreme — objective and constraints all *linear* — is its own discipline with its own geometry, and deserves a course of its own（C&Z devotes Part III to it）. Here we take only a glance. A **linear program**（LP）in standard form is

$$
\min_{\boldsymbol{x}}\;\boldsymbol{c}^{\!\top}\boldsymbol{x}
\qquad\text{subject to}\qquad
\boldsymbol{A}\boldsymbol{x}=\boldsymbol{b},\quad \boldsymbol{x}\ge\boldsymbol{0},
$$ (eq-u3-lp)

with inequality constraints handled by slack variables（$\boldsymbol{a}^{\!\top}\boldsymbol{x}\le b \Leftrightarrow \boldsymbol{a}^{\!\top}\boldsymbol{x}+s=b,\ s\ge0$）. Note what disappeared: a linear $f$ has $\nabla f=\boldsymbol{c}$ everywhere and no interior stationary points, so the FONC machinery of Unit 2 finds nothing inside — **the constraints do all the work**.

## Geometry: optima live at vertices

The feasible set of an LP is a **polytope** — an intersection of half-spaces, convex by Unit 1. Sliding the level sets of $\boldsymbol{c}^{\!\top}\boldsymbol{x}$（parallel hyperplanes）as far as feasibility allows, the last contact happens at a face, and always includes a **vertex**（[](#fig-u3-lp)）. That is the fundamental theorem of LP: *if a finite optimum exists, some vertex attains it*. An $n$-variable, $m$-constraint polytope has finitely many vertices, so LP is a finite search — the source of its remarkable tractability.

```{figure} ../assets/u03_lp.png
:name: fig-u3-lp
:width: 72%

Maximizing $2x_1+3x_2$ over a polytope. Dashed lines are iso-cost levels; pushing them up, the last feasible touch is the vertex $(2,3)$. Optima of an LP always include a vertex.
```

Two algorithm families exploit this（names only — C&Z Ch. 15 ff.）. The **simplex method** walks edge-to-edge from vertex to better vertex until no improving edge remains — exponential in contrived worst cases, superbly fast in practice. **Interior-point methods** cut through the middle of the polytope along a smooth central path, reaching provably polynomial complexity; their machinery is, pleasingly, Newton's method of sec 2 applied to a sequence of barrier problems.

LP is worth recognizing in the wild: production and power scheduling, network flows, $\ell_1$-norm fitting and sparse recovery（$|r|$ splits into two nonnegative variables）, and filter design with linear magnitude constraints all reduce to {eq}`eq-u3-lp`. When a problem *can* be written as an LP, solvers handle millions of variables routinely — always worth checking before reaching for the nonlinear toolbox.

```{note}
C&Z Ch. 12（solving systems of linear equations／least squares）is deliberately **skipped** in this course（老師裁定）; Ch. 15 is covered only to the depth of this section. Readers who want the full story — duality, simplex mechanics, interior-point theory — should continue into C&Z Part III.
```

## Exercises

以簡單與基礎為原則。

**Exercise 1（two steepest-descent steps）.** For $f(\boldsymbol{x})=\tfrac12(x_1^2+9x_2^2)$, run two exact-line-search SD steps from $\boldsymbol{x}^{(0)}=(9,1)^{\!\top}$（use {eq}`eq-u3-sdstep`）. Verify that $\boldsymbol{g}^{(1)}\perp\boldsymbol{g}^{(0)}$ and that the error shrinks by the factor predicted by {eq}`eq-u3-rate`.

```{dropdown} Solution
$\boldsymbol{Q}=\operatorname{diag}(1,9)$, $\boldsymbol{g}^{(0)}=(9,9)^{\!\top}$. $\alpha_0=\frac{81+81}{81+9\cdot81}=\frac{162}{810}=0.2$, so $\boldsymbol{x}^{(1)}=(9,1)^{\!\top}-0.2\,(9,9)^{\!\top}=(7.2,\,-0.8)^{\!\top}$. Then $\boldsymbol{g}^{(1)}=(7.2,\,-7.2)^{\!\top}$ and $\boldsymbol{g}^{(1)\top}\boldsymbol{g}^{(0)}=64.8-64.8=0$ ✓. Next, $\alpha_1=\frac{2\cdot51.84}{51.84+9\cdot51.84}=0.2$ and $\boldsymbol{x}^{(2)}=(5.76,\,0.64)^{\!\top}=0.64\,(9,1)^{\!\top}$. The error contracts by exactly $0.8=(\kappa-1)/(\kappa+1)$ per step（$\kappa=9$）— the bound {eq}`eq-u3-rate` is tight here: this zig-zag is the red path of [](#fig-u3-sdcg).
```

**Exercise 2（conjugacy is not orthogonality）.** Let $\boldsymbol{Q}=\begin{bmatrix}3&1\\1&2\end{bmatrix}$（Unit 1's matrix）. Show that $\boldsymbol{d}^{(1)}=(1,0)^{\!\top}$ and $\boldsymbol{d}^{(2)}=(1,-3)^{\!\top}$ are $\boldsymbol{Q}$-conjugate but not orthogonal, and that the orthogonal pair $(1,0)^{\!\top},(0,1)^{\!\top}$ is *not* $\boldsymbol{Q}$-conjugate.

```{dropdown} Solution
$\boldsymbol{d}^{(1)\top}\boldsymbol{Q}=(3,1)$, so $\boldsymbol{d}^{(1)\top}\boldsymbol{Q}\boldsymbol{d}^{(2)}=3\cdot1+1\cdot(-3)=0$ ✓ conjugate; but $\boldsymbol{d}^{(1)\top}\boldsymbol{d}^{(2)}=1\neq0$, not orthogonal. For $(0,1)^{\!\top}$: $\boldsymbol{d}^{(1)\top}\boldsymbol{Q}\,(0,1)^{\!\top}=1\neq0$ — orthogonal in the Euclidean sense, yet not conjugate. Conjugacy is orthogonality in the metric of $\boldsymbol{Q}$, not of the identity.
```

**Exercise 3（one BFGS update）.** Let $f(\boldsymbol{x})=\tfrac12\boldsymbol{x}^{\!\top}\!\operatorname{diag}(2,1)\,\boldsymbol{x}$, start $\boldsymbol{x}^{(0)}=(1,1)^{\!\top}$, $\boldsymbol{H}_0=\boldsymbol{I}$, and take the full step $\boldsymbol{x}^{(1)}=\boldsymbol{x}^{(0)}-\boldsymbol{H}_0\boldsymbol{g}^{(0)}$. Compute $\boldsymbol{H}_1$ from {eq}`eq-u3-bfgs` and verify the secant condition {eq}`eq-u3-secant`.

```{dropdown} Solution
$\boldsymbol{g}^{(0)}=(2,1)^{\!\top}$, so $\boldsymbol{x}^{(1)}=(-1,0)^{\!\top}$, $\boldsymbol{g}^{(1)}=(-2,0)^{\!\top}$, giving $\Delta\boldsymbol{x}=(-2,-1)^{\!\top}$, $\Delta\boldsymbol{g}=(-4,-1)^{\!\top}$. Then $\Delta\boldsymbol{g}^{\!\top}\Delta\boldsymbol{x}=9$ and $\Delta\boldsymbol{g}^{\!\top}\boldsymbol{H}_0\Delta\boldsymbol{g}=17$. Plugging into {eq}`eq-u3-bfgs`:
$\boldsymbol{H}_1=\boldsymbol{I}+\frac{26}{9}\cdot\frac{1}{9}\begin{bmatrix}4&2\\2&1\end{bmatrix}-\frac{1}{9}\begin{bmatrix}16&6\\6&2\end{bmatrix}
=\frac{1}{81}\begin{bmatrix}41&-2\\-2&89\end{bmatrix}$.
Secant check: $\boldsymbol{H}_1\Delta\boldsymbol{g}=\frac{1}{81}\begin{bmatrix}41&-2\\-2&89\end{bmatrix}\begin{pmatrix}-4\\-1\end{pmatrix}=\frac{1}{81}\begin{pmatrix}-164+2\\8-89\end{pmatrix}=\begin{pmatrix}-2\\-1\end{pmatrix}=\Delta\boldsymbol{x}$ ✓. The updated $\boldsymbol{H}_1$ has already learned to shrink the stiff $x_1$ direction（$41/81\approx0.51\approx1/2$）— it is estimating $\boldsymbol{Q}^{-1}=\operatorname{diag}(\tfrac12,1)$ from a single measurement.
```
