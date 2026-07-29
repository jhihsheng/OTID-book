# Linear Algebra Review

Optimization meets linear algebra through one object above all: the **symmetric matrix**. Gradients are vectors, but curvature — the thing that decides whether a flat point is a minimum — is a symmetric matrix（the Hessian, [next section](sec3.md)）. This section is a brisk review of exactly the linear algebra that curvature analysis needs（C&Z Ch. 2–3）.

## Vectors, independence, rank

$\mathbb{R}^n$ with componentwise addition and scaling is our vector space. Vectors $\boldsymbol{a}_1,\dots,\boldsymbol{a}_k$ are **linearly independent** if $\sum_i c_i\boldsymbol{a}_i=\boldsymbol{0}$ forces every $c_i=0$; the **rank** of a matrix is the number of linearly independent columns（equivalently rows）. An $n\times n$ matrix is invertible iff its rank is $n$, iff its determinant is nonzero. In this course rank appears mostly as a health check: a design parameterization with dependent columns is wasting variables, and a rank-deficient Hessian signals a flat direction of the landscape.

## Inner product and norm

The **inner product** and the **Euclidean norm**

$$
\langle\boldsymbol{x},\boldsymbol{y}\rangle=\boldsymbol{x}^{\!\top}\boldsymbol{y}=\sum_{i=1}^{n}x_i y_i,
\qquad
\|\boldsymbol{x}\|=\sqrt{\boldsymbol{x}^{\!\top}\boldsymbol{x}},
$$

give length and angle: $\boldsymbol{x}^{\!\top}\boldsymbol{y}=\|\boldsymbol{x}\|\,\|\boldsymbol{y}\|\cos\theta$. The workhorse inequality is **Cauchy–Schwarz**,

$$
|\boldsymbol{x}^{\!\top}\boldsymbol{y}|\;\le\;\|\boldsymbol{x}\|\,\|\boldsymbol{y}\|,
$$ (eq-u1-cs)

with equality iff one vector is a scalar multiple of the other. Keep {eq}`eq-u1-cs` in your pocket: in the [next section](sec3.md) it is a one-line proof that the gradient is the steepest-ascent direction.

## Symmetric matrices and orthogonal diagonalization

A real symmetric matrix $\boldsymbol{Q}=\boldsymbol{Q}^{\!\top}$ has two golden properties（C&Z Ch. 3）: all its eigenvalues $\lambda_1,\dots,\lambda_n$ are **real**, and eigenvectors of distinct eigenvalues are **orthogonal**. One can always choose an orthonormal eigenbasis $\boldsymbol{u}_1,\dots,\boldsymbol{u}_n$, collect it in $\boldsymbol{U}=[\boldsymbol{u}_1\;\cdots\;\boldsymbol{u}_n]$ with $\boldsymbol{U}^{\!\top}\boldsymbol{U}=\boldsymbol{I}$, and write

$$
\boldsymbol{Q}=\boldsymbol{U}\boldsymbol{\Lambda}\boldsymbol{U}^{\!\top},
\qquad \boldsymbol{\Lambda}=\operatorname{diag}(\lambda_1,\dots,\lambda_n).
$$ (eq-u1-diag)

Geometrically: in the right rotated coordinates, a symmetric matrix is just $n$ independent scalings.

## Quadratic forms and definiteness

A **quadratic form** is $f(\boldsymbol{x})=\boldsymbol{x}^{\!\top}\boldsymbol{Q}\boldsymbol{x}$ with $\boldsymbol{Q}$ symmetric（any square matrix can be symmetrized without changing $f$）. Substituting {eq}`eq-u1-diag` and $\boldsymbol{y}=\boldsymbol{U}^{\!\top}\boldsymbol{x}$（a rotation, so $\boldsymbol{y}$ ranges over all of $\mathbb{R}^n$ as $\boldsymbol{x}$ does）:

$$
\boldsymbol{x}^{\!\top}\boldsymbol{Q}\boldsymbol{x}
=\boldsymbol{y}^{\!\top}\boldsymbol{\Lambda}\boldsymbol{y}
=\sum_{i=1}^{n}\lambda_i\,y_i^{2}.
$$ (eq-u1-qform)

The sign behaviour of $f$ is therefore read off the eigenvalues. We say $\boldsymbol{Q}$ is

- **positive definite**（$\boldsymbol{Q}>0$）if $\boldsymbol{x}^{\!\top}\boldsymbol{Q}\boldsymbol{x}>0$ for all $\boldsymbol{x}\neq\boldsymbol{0}$;
- **positive semidefinite**（$\boldsymbol{Q}\ge 0$）if $\boldsymbol{x}^{\!\top}\boldsymbol{Q}\boldsymbol{x}\ge0$ for all $\boldsymbol{x}$;

and negative (semi)definite with the inequalities reversed; anything else is **indefinite**.（Notation follows C&Z: $\boldsymbol{Q}>0$ and $\boldsymbol{Q}\ge 0$ are statements about the *quadratic form*, not elementwise inequalities.） From {eq}`eq-u1-qform`:

**Eigenvalue test.** $\boldsymbol{Q}>0$ if and only if all $\lambda_i>0$; $\boldsymbol{Q}\ge 0$ if and only if all $\lambda_i\ge0$; a mix of signs means indefinite.

**Sylvester's criterion.** $\boldsymbol{Q}>0$ iff all $n$ **leading principal minors** are positive, $\Delta_1=q_{11}>0$, $\Delta_2=\det\begin{bmatrix}q_{11}&q_{12}\\ q_{21}&q_{22}\end{bmatrix}>0,\;\dots,\;\Delta_n=\det\boldsymbol{Q}>0$ — no eigenvalues needed.

```{warning}
Sylvester's criterion with $\ge$ does **not** test semidefiniteness. $\boldsymbol{Q}=\begin{bmatrix}0&0\\0&-1\end{bmatrix}$ has $\Delta_1=0,\ \Delta_2=0$, yet it is negative semidefinite, not PSD. Semidefiniteness requires *all* principal minors（not just leading ones）to be $\ge0$ — or simply use the eigenvalue test.
```

### Worked examples

**A $2\times2$ case.** $\boldsymbol{Q}=\begin{bmatrix}2&1\\1&3\end{bmatrix}$: $\Delta_1=2>0$, $\Delta_2=6-1=5>0$, so $\boldsymbol{Q}>0$. Check by eigenvalues: $\lambda=\tfrac{5\pm\sqrt{5}}{2}\approx 3.62,\ 1.38$, both positive. ✓

**A $3\times3$ case.** $\boldsymbol{Q}=\begin{bmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{bmatrix}$: $\Delta_1=2$, $\Delta_2=4-1=3$, $\Delta_3=\det\boldsymbol{Q}=2(4-1)-(-1)(-2-0)=6-2=4$. All positive $\Rightarrow \boldsymbol{Q}>0$.

## Why we care（forward pointers）

- **Unit 2:** at an interior stationary point, Hessian $\ge 0$ is *necessary* for a minimum and Hessian $>0$ is *sufficient* for a strict one — the definiteness tests above are literally the second-order optimality check.
- **Unit 3:** for a PD quadratic, the level sets of $f=\tfrac12\boldsymbol{x}^{\!\top}\boldsymbol{Q}\boldsymbol{x}$ are ellipsoids with axes along the $\boldsymbol{u}_i$ and lengths $\propto1/\sqrt{\lambda_i}$; the **condition number** $\kappa=\lambda_{\max}/\lambda_{\min}$ measures their elongation and will *exactly* govern how fast steepest descent converges.

```{seealso}
The TMM mini-project（[labs/tmm](../labs/tmm.md)）is linear algebra at work: each layer of a multilayer filter is a $2\times2$ transfer matrix, and the whole stack is their product.
```
