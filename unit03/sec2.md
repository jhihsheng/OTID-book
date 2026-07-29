# Newton's Method in n Dimensions

## The ideal direction

Steepest descent fails because it ignores curvature: it treats every direction as equally priced when the Hessian says otherwise. Newton's method prices them correctly. Expand $f$ about the current iterate with Taylor's theorem {eq}`eq-u1-taylor` and *minimize the model itself*: the quadratic model

$$
q(\boldsymbol{x}^{(k)}+\boldsymbol{d})
=f(\boldsymbol{x}^{(k)})+\boldsymbol{g}^{(k)\top}\boldsymbol{d}
+\tfrac12\,\boldsymbol{d}^{\!\top}\boldsymbol{F}(\boldsymbol{x}^{(k)})\,\boldsymbol{d}
$$

has（for $\boldsymbol{F}>0$）the unique minimizer where $\nabla q=\boldsymbol{g}^{(k)}+\boldsymbol{F}\boldsymbol{d}=\boldsymbol{0}$. The **Newton step** solves that linear system:

$$
\boldsymbol{F}(\boldsymbol{x}^{(k)})\,\boldsymbol{d}^{(k)}=-\boldsymbol{g}^{(k)},
\qquad
\boldsymbol{x}^{(k+1)}=\boldsymbol{x}^{(k)}+\boldsymbol{d}^{(k)} .
$$ (eq-u3-newton)

This is the $n$-dimensional version of Unit 2's $x^{+}=x-f'/f''$, and it inherits the same reward（C&Z Ch. 9）: **quadratic convergence** — if $f$ is smooth enough near a minimizer with $\boldsymbol{F}(\boldsymbol{x}^{*})>0$ and $\boldsymbol{x}^{(0)}$ is close enough, the number of correct digits doubles per iteration. On the quadratic {eq}`eq-u3-quad` the model is exact and Newton lands on $\boldsymbol{x}^{*}$ in **one step**, regardless of $\kappa$（[](#fig-u3-convergence) in sec 3 shows all methods side by side）. Newton is, in the language of sec 1, steepest descent with the *perfect* preconditioner $\boldsymbol{M}=\boldsymbol{F}$.

## What breaks

Away from the asymptotic paradise, three things go wrong（C&Z Ch. 9）:

1. **Wrong-way steps.** If $\boldsymbol{F}(\boldsymbol{x}^{(k)})$ is indefinite — routine in the nonconvex landscapes of photonics and deep learning — the model has no minimum, and the Newton「step」may head for a *saddle* or *maximum*: $\boldsymbol{d}^{(k)}$ need not even be a descent direction.
2. **Overconfidence far from $\boldsymbol{x}^{*}$.** Like its 1-D parent（the arctan divergence of Unit 2）, a full Newton step can overshoot badly. The standard repair is a **damped** Newton method: use the Newton *direction* but choose the step length by Armijo backtracking {eq}`eq-u2-armijo`, so the fast local behaviour is kept（$\alpha=1$ is accepted near the solution）while global sanity is enforced.
3. **Cost.** Each iteration must form the $n\times n$ Hessian（$O(n^2)$ storage）and solve {eq}`eq-u3-newton`（$O(n^3)$ work）. For the $10^4$–$10^6$ design variables of topology optimization or neural networks this is simply unaffordable — the opening for the methods of sec 3.

## Levenberg–Marquardt: one knob from gradient to Newton

Problems 1 and 2 share an elegant fix. Shift the Hessian before solving:

$$
\bigl(\boldsymbol{F}(\boldsymbol{x}^{(k)})+\mu_k\boldsymbol{I}\bigr)\,\boldsymbol{d}^{(k)}=-\boldsymbol{g}^{(k)},
\qquad \mu_k\ge0 .
$$ (eq-u3-lm)

The **Levenberg–Marquardt modification** {eq}`eq-u3-lm`（C&Z Ch. 9）interpolates continuously between the two poles of this unit: $\mu_k\to0$ recovers pure Newton, while $\mu_k$ large makes $\boldsymbol{d}^{(k)}\approx-\boldsymbol{g}^{(k)}/\mu_k$ — a short steepest-descent step. Choosing $\mu_k>-\lambda_{\min}(\boldsymbol{F})$ also forces the shifted matrix positive definite, so the step is a guaranteed descent direction even where the raw Hessian is indefinite. Practical logic: try a step; if it reduces $f$, shrink $\mu$（trust the model more）; if not, grow $\mu$（retreat toward gradient descent）.

For **nonlinear least squares** $f(\boldsymbol{x})=\tfrac12\sum_i r_i(\boldsymbol{x})^2$ — spectrum fitting, for instance — the Gauss–Newton approximation replaces $\boldsymbol{F}$ by $\boldsymbol{J}^{\!\top}\boldsymbol{J}$（$\boldsymbol{J}$ the Jacobian of the residuals）, getting Newton-like steps from first derivatives only; Levenberg–Marquardt applied to it is the classic workhorse behind `scipy.optimize.least_squares`. We leave it at this one-line pointer.

## The scoreboard so far

Steepest descent: cheap iterations（a gradient）, condition-number-limited linear convergence. Newton: expensive iterations（a Hessian and a solve）, quadratic convergence when it works, repairs needed when it does not. The obvious question —「can we get Newton-like directions for gradient-like prices?」— has two classical answers, and both are in [the next section](sec3.md).
