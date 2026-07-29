# Steepest Descent

## The algorithm

Unit 1 proved that $-\nabla f$ is the locally fastest way down; Unit 2 built line searches. Compose them and you have the founding algorithm of the field — **steepest descent**（SD; C&Z Ch. 8）. With $\boldsymbol{g}^{(k)}=\nabla f(\boldsymbol{x}^{(k)})$,

$$
\boldsymbol{x}^{(k+1)}=\boldsymbol{x}^{(k)}-\alpha_k\,\boldsymbol{g}^{(k)},
$$ (eq-u3-sd)

where $\alpha_k$ comes from a line search — Armijo backtracking in practice, or, on problems where the minimization is explicit, the **exact** line search $\alpha_k=\arg\min_\alpha f(\boldsymbol{x}^{(k)}-\alpha\boldsymbol{g}^{(k)})$. Stop when $\|\boldsymbol{g}^{(k)}\|\le\varepsilon$（FONC, operationalized — Unit 2）.

To analyze SD we use the standard laboratory animal: the positive-definite quadratic

$$
f(\boldsymbol{x})=\tfrac12\,\boldsymbol{x}^{\!\top}\boldsymbol{Q}\boldsymbol{x}-\boldsymbol{b}^{\!\top}\boldsymbol{x},
\qquad \boldsymbol{Q}\succ0,
$$ (eq-u3-quad)

with gradient $\boldsymbol{g}=\boldsymbol{Q}\boldsymbol{x}-\boldsymbol{b}$ and minimizer $\boldsymbol{x}^{*}=\boldsymbol{Q}^{-1}\boldsymbol{b}$. Near any smooth minimum, Taylor's theorem {eq}`eq-u1-taylor` says *every* objective looks like {eq}`eq-u3-quad` with $\boldsymbol{Q}=\boldsymbol{F}(\boldsymbol{x}^{*})$ — so whatever we prove here is the asymptotic truth for smooth problems in general.

On {eq}`eq-u3-quad` the exact step has a closed form: minimizing the scalar quadratic $\alpha\mapsto f(\boldsymbol{x}-\alpha\boldsymbol{g})$ gives

$$
\alpha_k=\frac{\boldsymbol{g}^{(k)\top}\boldsymbol{g}^{(k)}}{\boldsymbol{g}^{(k)\top}\boldsymbol{Q}\,\boldsymbol{g}^{(k)}}.
$$ (eq-u3-sdstep)

## The zig-zag

Exact line search leaves a fingerprint: at the minimizing $\alpha$, $\frac{\mathrm{d}}{\mathrm{d}\alpha}f(\boldsymbol{x}-\alpha\boldsymbol{g})=-\boldsymbol{g}^{(k+1)\top}\boldsymbol{g}^{(k)}=0$ — **each new gradient is orthogonal to the previous one**. On an elongated valley the iterates therefore stitch a right-angled zig-zag across the floor（[](#fig-u3-sdcg)）, crossing the valley over and over instead of walking along it. The step direction is optimal *locally*; the trajectory is terrible *globally*.

```{figure} ../assets/u03_sdcg.png
:name: fig-u3-sdcg
:width: 95%

The signature picture of this unit. On $f=\frac12(x_1^2+9x_2^2)$（$\kappa=9$）from $(9,1)$: steepest descent（red）zig-zags — consecutive steps exactly orthogonal — while conjugate gradients（green）reaches the minimizer in two steps, the dimension of the space.
```

## The convergence rate, derived in full

How bad is the zig-zag? Measure progress by $V(\boldsymbol{x})=f(\boldsymbol{x})-f^{*}=\tfrac12(\boldsymbol{x}-\boldsymbol{x}^{*})^{\!\top}\boldsymbol{Q}(\boldsymbol{x}-\boldsymbol{x}^{*})$, and note the identity $V=\tfrac12\,\boldsymbol{g}^{\!\top}\boldsymbol{Q}^{-1}\boldsymbol{g}$（since $\boldsymbol{g}=\boldsymbol{Q}(\boldsymbol{x}-\boldsymbol{x}^{*})$）. One exact-line-search step maps $\boldsymbol{g}\mapsto\boldsymbol{g}^{+}=\boldsymbol{g}-\alpha\boldsymbol{Q}\boldsymbol{g}$, so

$$
2V^{+}=\boldsymbol{g}^{+\top}\boldsymbol{Q}^{-1}\boldsymbol{g}^{+}
=\boldsymbol{g}^{\!\top}\boldsymbol{Q}^{-1}\boldsymbol{g}
-2\alpha\,\boldsymbol{g}^{\!\top}\boldsymbol{g}
+\alpha^{2}\,\boldsymbol{g}^{\!\top}\boldsymbol{Q}\boldsymbol{g}
=\boldsymbol{g}^{\!\top}\boldsymbol{Q}^{-1}\boldsymbol{g}
-\frac{(\boldsymbol{g}^{\!\top}\boldsymbol{g})^{2}}{\boldsymbol{g}^{\!\top}\boldsymbol{Q}\boldsymbol{g}},
$$

substituting {eq}`eq-u3-sdstep` in the last equality. Dividing by $2V$:

$$
\frac{V^{+}}{V}
=1-\frac{(\boldsymbol{g}^{\!\top}\boldsymbol{g})^{2}}
{(\boldsymbol{g}^{\!\top}\boldsymbol{Q}\boldsymbol{g})\,(\boldsymbol{g}^{\!\top}\boldsymbol{Q}^{-1}\boldsymbol{g})}.
$$ (eq-u3-onestep)

The fraction on the right is bounded below by the **Kantorovich inequality**（for any $\boldsymbol{g}\neq\boldsymbol{0}$ and $\boldsymbol{Q}\succ0$ with extreme eigenvalues $\lambda_{\min},\lambda_{\max}$; proof in C&Z Ch. 8）:

$$
\frac{(\boldsymbol{g}^{\!\top}\boldsymbol{g})^{2}}
{(\boldsymbol{g}^{\!\top}\boldsymbol{Q}\boldsymbol{g})(\boldsymbol{g}^{\!\top}\boldsymbol{Q}^{-1}\boldsymbol{g})}
\;\ge\;\frac{4\lambda_{\min}\lambda_{\max}}{(\lambda_{\min}+\lambda_{\max})^{2}} .
$$

Insert this into {eq}`eq-u3-onestep` and simplify with $\kappa=\lambda_{\max}/\lambda_{\min}$:

$$
\frac{V^{+}}{V}\;\le\;1-\frac{4\lambda_{\min}\lambda_{\max}}{(\lambda_{\min}+\lambda_{\max})^{2}}
=\left(\frac{\lambda_{\max}-\lambda_{\min}}{\lambda_{\max}+\lambda_{\min}}\right)^{2}
=\left(\frac{\kappa-1}{\kappa+1}\right)^{2}.
$$ (eq-u3-rate)

```{important}
**Steepest descent converges linearly with rate $\bigl(\frac{\kappa-1}{\kappa+1}\bigr)^{2}$ — geometry is destiny.** For $\kappa=1$（spherical bowl）one step solves the problem. For $\kappa=9$ the rate is $0.8^{2}=0.64$ in $V$（$0.8$ in the error norm — the opening puzzle）. For $\kappa=100$ it is $0.96$: some $57$ iterations *per decimal digit*. The bound is tight — worst-case starting points achieve it — and no step-size trick escapes it, because the *direction* is the problem. Everything else in this unit is a smarter direction.
```

## Preconditioning: change the geometry, not the algorithm

If $\kappa$ is destiny, change $\kappa$. Substituting variables $\boldsymbol{y}=\boldsymbol{C}\boldsymbol{x}$ turns the Hessian into $\boldsymbol{C}^{-\top}\boldsymbol{Q}\boldsymbol{C}^{-1}$; the ideal $\boldsymbol{C}=\boldsymbol{Q}^{1/2}$ would make it the identity（$\kappa=1$, one step）— but computing it is as hard as the original problem. A **preconditioner** is any cheap approximation $\boldsymbol{M}\approx\boldsymbol{Q}$ whose inverse is easy to apply: iterate on the reshaped problem, i.e. take directions $-\boldsymbol{M}^{-1}\boldsymbol{g}$ instead of $-\boldsymbol{g}$. Even the humble diagonal $\boldsymbol{M}=\operatorname{diag}(\boldsymbol{Q})$ often collapses $\kappa$ by orders of magnitude. Keep this idea warm: in Unit 4, Adam — the default optimizer of deep learning — will turn out to be exactly steepest descent with an *adaptive diagonal preconditioner* estimated on the fly.

The zig-zag diagnosis also admits a cleverer cure than reshaping space: keep the cheap gradient, but forbid the new step from undoing the old ones. That idea — conjugacy — is [sec 3](sec3.md); first, [Newton's method](sec2.md) shows what the *ideal* direction looks like.
