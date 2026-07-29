# The Density-Based Topology-Optimization Pipeline

## From raw densities to buildable devices

Sec 1 provides gradients; Unit 6 warned that raw pixel optimization produces unbuildable lace. The production pipeline（[](#fig-u7-pipeline); reference implementation: Hammond et al., *Opt. Express* **30**, 4467, 2022 — the Meep adjoint solver of the labs）threads fabrication awareness *into the differentiable chain itself*:

```{figure} ../assets/u07_to_loop.png
:name: fig-u7-pipeline
:width: 98%

One iteration of density-based topology optimization. Everything from $\rho$ to $J$ is differentiable, so the adjoint gradient flows back through the whole chain to the raw design variables.
```

**1. Filter（minimum feature size）.** Convolve the raw density with a smoothing kernel — conic or Gaussian — of radius $R$:$\ \tilde{\rho}=\boldsymbol{W}\rho$. No feature of $\tilde\rho$, solid or void, can be smaller than $R$; choose $R$ = your foundry's minimum feature, and the *entire search space* becomes manufacturable geometry.

**2. Project（binarization）.** Push the smoothed density toward 0/1 with a smooth threshold:

$$
\bar{\rho}
=\frac{\tanh(\beta\eta)+\tanh\bigl(\beta(\tilde{\rho}-\eta)\bigr)}
{\tanh(\beta\eta)+\tanh\bigl(\beta(1-\eta)\bigr)},
$$ (eq-u7-project)

with threshold $\eta=\tfrac12$ and sharpness $\beta$. Small $\beta$: nearly the identity（gentle, well-conditioned optimization）. Large $\beta$: a near-step function（nearly binary designs）. [](#fig-u7-filterproj) shows the chain acting on a 1-D profile — note how the sub-$R$ sliver survives filtering only as a low bump that projection then deletes.

**3. Interpolate materials.** Map density to permittivity, $\varepsilon(\bar{\rho})=\varepsilon_{\min}+\bar{\rho}\,(\varepsilon_{\max}-\varepsilon_{\min})$, then hand $\varepsilon(\boldsymbol{r})$ to the forward solve {eq}`eq-u7-maxwell`.

**4. Solve, score, differentiate.** Forward simulation → $J$; adjoint simulation → $\delta J/\delta\varepsilon$ {eq}`eq-u7-overlap`; then the chain rule pulls the gradient *back through* steps 3→2→1（all smooth maps with known derivatives — in the Meep stack this bookkeeping is done by `autograd`, Unit 8's subject）to give $\nabla_{\rho}J$ with respect to the raw variables.

**5. Update.** Feed $\nabla_{\rho}J$ to a bound-constrained optimizer — in practice **CCSA/MMA** or **L-BFGS** via `nlopt`, exactly as in notebooks 08–09 — respecting $\rho\in[0,1]$.

**6. $\beta$-continuation.** Solve a *sequence* of problems with increasing $\beta$（e.g. double it every few tens of iterations）. Low-$\beta$ rounds move freely through gray designs and find good topology; high-$\beta$ rounds harden the topology into binary geometry. Jumping straight to large $\beta$ is a classic failure — the landscape is then nearly piecewise-constant and the gradient nearly useless.

```{figure} ../assets/u07_filter_project.png
:name: fig-u7-filterproj
:width: 88%

The filter→project chain on a 1-D density（computed, not sketched: `figs_src/u07_filter_project.py`）. Filtering imposes the minimum feature $R$; projection with growing $\beta$ hardens the design toward 0/1 — together they turn「any pixels」into「buildable geometry」without leaving the differentiable world.
```

## Robust and multi-frequency formulations

A design that works only at exactly $1550.0$ nm, or only if the etch lands within a nanometer, is a simulation trophy. Two standard hardenings, both in the labs' reference stack:

- **Multi-frequency**: score the worst wavelength of a set, $J=\min_k J(\omega_k)$（or a smooth-min）, paying one forward＋adjoint pair per frequency — exactly notebook 09's setup, and the reason its runtime scales with the number of frequencies.
- **Robustness to fabrication**: optimize the worst case over eroded/nominal/dilated versions of the design（shifting $\eta$ in {eq}`eq-u7-project` mimics under/over-etching）. The design that survives is one the fab can actually deliver.

```{seealso}
Run it: [notebook 08](../labs/adjoint.md) builds this exact pipeline for the waveguide bend; notebook 09 adds the multi-frequency objective; the [Meep Adjoint Solver tutorial](https://meep.readthedocs.io/en/latest/Python_Tutorials/Adjoint_Solver/) documents the API and conventions. The mp4 films on the lab page are $\beta$-continuation in action.
```

## Exercises

以簡單與基礎為原則。

**Exercise 1（adjoint on a 2×2 system）.** Let $\boldsymbol{A}(p)=\begin{bmatrix}2&p\\p&1\end{bmatrix}$, $\boldsymbol{b}=(1,0)^{\!\top}$, and $J=x_1+x_2$. At $p=0$: solve the forward system, solve the adjoint system {eq}`eq-u7-adjoint`, and evaluate the gradient {eq}`eq-u7-grad`. Check by differentiating the closed-form solution.

```{dropdown} Solution
Forward: $\boldsymbol{A}(0)=\operatorname{diag}(2,1)$, so $\boldsymbol{x}=(\tfrac12,0)^{\!\top}$. Adjoint: $\partial J/\partial\boldsymbol{x}=(1,1)$, and $\boldsymbol{A}^{\!\top}=\boldsymbol{A}$, so $\boldsymbol{\lambda}=(\tfrac12,1)^{\!\top}$. With $\frac{\partial\boldsymbol{A}}{\partial p}=\bigl[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\bigr]$: $\frac{\mathrm{d}J}{\mathrm{d}p}=-\boldsymbol{\lambda}^{\!\top}\bigl[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\bigr]\boldsymbol{x}=-(\tfrac12,1)\cdot(0,\tfrac12)^{\!\top}=-\tfrac12$.
Check: $\boldsymbol{x}(p)=\frac{1}{2-p^2}(1,-p)^{\!\top}$, so $J(p)=\frac{1-p}{2-p^2}$ and $J'(0)=\frac{-(2)-0}{4}=-\tfrac12$. ✓
```

**Exercise 2（count the solves）.** A topology optimization has $10^4$ design pixels and each simulation takes one minute. Compare the cost of one full gradient by（a）finite differences and（b）the adjoint method, and give the wall-clock times.

```{dropdown} Solution
（a）Finite differences: one solve per parameter plus the baseline — $10^4+1$ simulations $\approx10^4$ minutes $\approx$ **7 days** per gradient.（b）Adjoint: forward + adjoint = $2$ simulations = **2 minutes**, plus a negligible sparse assembly. Ratio $\approx5000\times$; and the adjoint numbers are exact derivatives, free of finite-difference step-size error（Unit 8 sec 1 analyzes that error）. A 200-iteration design run: 2 years vs 7 hours.
```

**Exercise 3（read the interference photograph）.** Adopting the convention that $\delta J/\delta\varepsilon(\boldsymbol{r})=+\operatorname{Re}[\boldsymbol{E}_{\text{adj}}\cdot\boldsymbol{E}_{\text{fwd}}]$ and that we *maximize* $J$: at pixel $\boldsymbol{r}_1$ the two fields oscillate in phase; at $\boldsymbol{r}_2$ they are $180^{\circ}$ out of phase. What should the optimizer do at each pixel, and why does the answer flip if the pixel currently sits at $\rho=1$?

```{dropdown} Solution
In phase at $\boldsymbol{r}_1$ ⇒ $\delta J/\delta\varepsilon>0$ ⇒ raising $\varepsilon$ raises $J$ ⇒ **add material**（increase $\rho$）. Out of phase at $\boldsymbol{r}_2$ ⇒ derivative negative ⇒ **remove material**. If the pixel already has $\rho=1$, the「add」instruction hits the bound — the constrained optimizer simply keeps it at 1（an active bound, Unit 2's boundary FONC in action）; only the *interior* pixels move. This is all a topology optimizer does, thousands of pixels at a time, iteration after iteration.
```
