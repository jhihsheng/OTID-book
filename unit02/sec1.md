# Problem Formulation and Optimality Conditions

## From an engineering wish to $\min f$

Optimization begins before any algorithm: someone must decide *what is being minimized over what*（最佳化問題建模 — official course goal #2）. The decisions are always the same three:

1. **Decision variables** $\boldsymbol{x}$ — what are we free to change?
2. **Objective** $f(\boldsymbol{x})$ — one number that says how good a choice is（smaller = better）.
3. **Constraints** $\Omega$ — which choices are physically or economically admissible?

**Worked example（single-layer antireflection coating）.** The wish:「make a glass surface reflect as little as possible at $\lambda_0=550\,$nm.」We may deposit one thin film, choosing its refractive index $n$ and thickness $t$: so $\boldsymbol{x}=(n,t)^{\!\top}$, two variables. The objective is the reflectance at the design wavelength, $f(n,t)=R(n,t;\lambda_0)$, computed from thin-film interference（by the same transfer-matrix method as [Mini-project I](../labs/tmm.md)）. Constraints: coating materials only exist with $n\in[1.38,\,2.4]$, and $t>0$; hence $\Omega=[1.38,2.4]\times(0,\infty)$. The model is now the standard form of Unit 1:

$$
\min_{(n,t)\in\Omega}\; R(n,t;\lambda_0).
$$

This particular problem is famous because the answer is analytic: reflection at the two interfaces cancels when the amplitudes match and the round-trip phase is half a wave — $n=\sqrt{n_s}$（for glass $n_s\approx1.5$, $n\approx1.22$）and the quarter-wave thickness $t=\lambda_0/4n$. Two modeling lessons hide here. First, the *analytic* optimum $n\approx1.22$ is **infeasible** — no such solid material exists — so the constrained optimum sits on the boundary $n=1.38$（MgF₂, the real-world coating choice）: constraints changed the answer, not just the search. Second, the moment the wish becomes realistic —「reflect little over the *whole visible band*」— the objective becomes an integral of $R$ over $\lambda$ with no closed form, and only the numerical machinery of this course remains. Modeling choices（one wavelength or a band? minimize average or worst case?）are design decisions, not mathematical ones.

## Minimizers and feasible directions

A point $\boldsymbol{x}^{*}\in\Omega$ is a **local minimizer** if $f(\boldsymbol{x}^{*})\le f(\boldsymbol{x})$ for all feasible $\boldsymbol{x}$ in some neighborhood of $\boldsymbol{x}^{*}$; **strict** if the inequality is strict for $\boldsymbol{x}\neq\boldsymbol{x}^{*}$; **global** if the neighborhood is all of $\Omega$. A vector $\boldsymbol{d}\neq\boldsymbol{0}$ is a **feasible direction** at $\boldsymbol{x}$ if a small step that way stays in the set: $\boldsymbol{x}+\alpha\boldsymbol{d}\in\Omega$ for all sufficiently small $\alpha>0$. At an interior point every direction is feasible; at a boundary point（like $n=1.35$ above）only inward ones are.

## First-order necessary condition（FONC）

Take Taylor's theorem {eq}`eq-u1-taylor` to first order along a feasible direction:
$f(\boldsymbol{x}^{*}+\alpha\boldsymbol{d})=f(\boldsymbol{x}^{*})+\alpha\,\boldsymbol{d}^{\!\top}\nabla f(\boldsymbol{x}^{*})+o(\alpha)$.
If $\boldsymbol{d}^{\!\top}\nabla f(\boldsymbol{x}^{*})<0$, then for small $\alpha$ the right side dips below $f(\boldsymbol{x}^{*})$ — contradicting minimality. Hence（C&Z Ch. 6）:

$$
\boldsymbol{d}^{\!\top}\nabla f(\boldsymbol{x}^{*})\;\ge\;0
\quad\text{for every feasible direction }\boldsymbol{d}.
$$ (eq-u2-fonc)

At an **interior** point all $\pm\boldsymbol{d}$ are feasible, so {eq}`eq-u2-fonc` forces both signs and collapses to the familiar

$$
\nabla f(\boldsymbol{x}^{*})=\boldsymbol{0}.
$$ (eq-u2-fonc-int)

Points satisfying {eq}`eq-u2-fonc-int` are **stationary points** — candidates, not winners: maxima and saddles pass the same test.

## Second-order conditions（SONC and SOSC）

Push the same Taylor argument one order further. Along a feasible $\boldsymbol{d}$ with $\boldsymbol{d}^{\!\top}\nabla f(\boldsymbol{x}^{*})=0$, minimality forces the quadratic term to be nonnegative（C&Z Ch. 6）— at an interior stationary point:

**SONC.** $\boldsymbol{F}(\boldsymbol{x}^{*})\succeq0$（Hessian positive semidefinite）.

Necessary is not sufficient, but a small strengthening is（C&Z Ch. 6）:

**SOSC.** If $\nabla f(\boldsymbol{x}^{*})=\boldsymbol{0}$ and $\boldsymbol{F}(\boldsymbol{x}^{*})\succ0$, then $\boldsymbol{x}^{*}$ is a **strict local minimizer**.

The definiteness tests of [Unit 1](../unit01/sec2.md)（eigenvalues, Sylvester）are exactly how SONC/SOSC are checked in practice.

**Worked example（a saddle: FONC passes, SONC fails）.** $f(\boldsymbol{x})=x_1^2-x_2^2$: $\nabla f=(2x_1,-2x_2)^{\!\top}=\boldsymbol{0}$ at the origin, so FONC holds. But $\boldsymbol{F}=\operatorname{diag}(2,-2)$ has eigenvalues of both signs — indefinite, SONC fails — and indeed the origin is a saddle: $f$ increases along $x_1$, decreases along $x_2$.

**A sharper warning（SONC passes, still no minimum）.** $f(\boldsymbol{x})=x_1^2-x_2^4$: at the origin $\nabla f=\boldsymbol{0}$ and $\boldsymbol{F}=\operatorname{diag}(2,0)\succeq0$, so FONC *and* SONC both hold. Yet $f(0,\varepsilon)=-\varepsilon^4<0=f(\boldsymbol{0})$ for every $\varepsilon\neq0$: the origin is not a local minimizer. Necessary conditions filter candidates; only SOSC certifies（and here SOSC correctly refuses: $\boldsymbol{F}$ is not positive *definite*）.

```{important}
**Optimality conditions are the termination contract of every algorithm in this course.** When scipy, nlopt, or your own gradient loop（Unit 3）declares success, the test it ran is $\|\nabla f(\boldsymbol{x}^{(k)})\|\le\varepsilon$ — FONC {eq}`eq-u2-fonc-int`, operationalized with a tolerance — optionally plus a curvature check, which is SONC. An optimizer never certifies「global minimum」; it certifies「no first-order descent direction remains」. Understanding exactly what has been proven when an optimizer stops is the difference between using these tools and trusting them blindly.
```

With the *what* settled — what a minimizer is and how to recognize one — the rest of the unit builds the first *how*: locating the minimizer of a one-dimensional function, first [without derivatives](sec2.md), then [with them](sec3.md).
