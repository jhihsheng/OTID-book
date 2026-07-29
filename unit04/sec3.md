# Optimizers: From SGD to Adam

## Stochastic gradients: noise by design

The empirical risk {eq}`eq-u4-erm` is a sum over $N$ examples, and $N$ may be billions. Computing the exact gradient per step is absurd when a cheap unbiased estimate exists: draw a **minibatch** $B$（typically $32$–$1024$ examples）and use

$$
\hat{\boldsymbol{g}}^{(k)}=\frac{1}{|B|}\sum_{i\in B}\nabla_{\boldsymbol{\theta}}\,\ell_i ,
\qquad
\boldsymbol{\theta}^{(k+1)}=\boldsymbol{\theta}^{(k)}-\alpha\,\hat{\boldsymbol{g}}^{(k)} .
$$ (eq-u4-sgd)

This is **stochastic gradient descent**（SGD）: the steepest-descent update {eq}`eq-u3-sd`, driven by a noisy compass. The step cost no longer depends on $N$ at all. The noise is partly a bug — near a minimum the iterates jitter instead of converging, which is why learning rates must eventually decay — but partly a feature: random kicks carry the iterate off saddle points and out of narrow, sharp valleys, and practice consistently finds that the minima SGD prefers generalize well. Treat that last clause as an empirical observation, not a theorem.

## Momentum

The zig-zag disease of Unit 3 sec 1 afflicts the SGD update {eq}`eq-u4-sgd` too, now with noise on top. **Momentum**（the heavy-ball idea; survey in Kochenderfer & Wheeler）treats the iterate as a ball with inertia — accumulate an exponential moving average of gradients and step along it:

$$
\boldsymbol{v}^{(k+1)}=\beta\,\boldsymbol{v}^{(k)}-\alpha\,\hat{\boldsymbol{g}}^{(k)},
\qquad
\boldsymbol{\theta}^{(k+1)}=\boldsymbol{\theta}^{(k)}+\boldsymbol{v}^{(k+1)},
$$ (eq-u4-mom)

with $\beta\approx0.9$. Components of the gradient that flip sign step to step（across the valley）cancel in the average; components that persist（along the valley）accumulate to an effective step up to $1/(1-\beta)=10\times$ larger. Momentum simultaneously damps oscillation, accelerates the useful direction, and averages out minibatch noise. **Nesterov's variant**（statement only）evaluates the gradient at the *look-ahead* point $\boldsymbol{\theta}+\beta\boldsymbol{v}$ rather than the current one, which yields provably better constants on convex problems and slightly better behaviour in practice.

## Adaptive scaling: from AdaGrad to Adam

Deep networks are wildly **anisotropic**: some parameters see large gradients, others tiny ones, and one global $\alpha$ cannot fit both. The adaptive family gives *each coordinate its own step size*, learned from the gradient history. **AdaGrad** divides by the root of the *accumulated* squared gradients — principled, but the accumulator only grows, so the learning rate decays to zero and training stalls. **RMSProp** repairs this with an exponential moving average instead of a sum. **Adam**（Kingma & Ba, ICLR 2015）combines RMSProp's second-moment scaling with a momentum-style first moment（compare {eq}`eq-u4-mom`）, plus one subtle fix. With $\odot$ elementwise:

$$
\begin{aligned}
\boldsymbol{m}^{(k)}&=\beta_1\,\boldsymbol{m}^{(k-1)}+(1-\beta_1)\,\hat{\boldsymbol{g}}^{(k)},
&\qquad
\hat{\boldsymbol{m}}&=\frac{\boldsymbol{m}^{(k)}}{1-\beta_1^{\,k}},\\[2pt]
\boldsymbol{v}^{(k)}&=\beta_2\,\boldsymbol{v}^{(k-1)}+(1-\beta_2)\,\hat{\boldsymbol{g}}^{(k)}\!\odot\hat{\boldsymbol{g}}^{(k)},
&\qquad
\hat{\boldsymbol{v}}&=\frac{\boldsymbol{v}^{(k)}}{1-\beta_2^{\,k}},\\[2pt]
\boldsymbol{\theta}^{(k+1)}&=\boldsymbol{\theta}^{(k)}
-\alpha\,\frac{\hat{\boldsymbol{m}}}{\sqrt{\hat{\boldsymbol{v}}}+\varepsilon}\,,
\end{aligned}
$$ (eq-u4-adam)

with defaults $\beta_1=0.9$, $\beta_2=0.999$, $\varepsilon=10^{-8}$. The **bias correction**（the $1-\beta^{k}$ divisions）exists because $\boldsymbol{m},\boldsymbol{v}$ start at zero and would otherwise underestimate the true moments for the first many steps; Exercise 2 shows the corrected first step has magnitude exactly $\alpha$ per coordinate. Practical relatives, briefly: **AdamW** decouples weight decay from the adaptive scaling（append $-\alpha\lambda\boldsymbol{\theta}$ to the update — the modern default）; and the learning rate $\alpha$ itself is usually **scheduled** — a short warmup from zero（the moment estimates need data before they can be trusted）, then a slow decay, cosine-shaped being the common choice.

```{important}
**Adam is steepest descent with an adaptive diagonal preconditioner.** Compare {eq}`eq-u4-adam` with Unit 3 sec 1: dividing coordinate-wise by $\sqrt{\hat{\boldsymbol{v}}}$ is applying $\boldsymbol{M}^{-1}$ with $\boldsymbol{M}=\operatorname{diag}(\sqrt{\hat{\boldsymbol{v}}})$ — a cheap, online-estimated stand-in for curvature that shrinks the effective condition number, exactly the cure sec 1 prescribed for the zig-zag disease. That is the honest one-line summary of a decade of optimizer research: *first-order cost, a poor man's second-order geometry.* Nothing here escapes Unit 3's theory; it industrializes it.
```

```{figure} ../assets/u04_optimizers.png
:name: fig-u4-optim

Full-batch GD, momentum, and Adam on the Rosenbrock valley（3000 iterations each, fixed hyperparameters）. GD creeps along the curved valley floor; momentum overshoots wildly at first, then rides the valley to machine precision; Adam takes the smoothest path and lands close. A deterministic 2-D toy — read it as intuition for the *mechanisms*（inertia, per-coordinate scaling）, not as a benchmark: with minibatch noise and $10^8$ dimensions the trade-offs shift, which is why Adam's robustness, not raw speed, made it the default.
```

## Exercises

以簡單與基礎為原則。

**Exercise 1（backprop by hand）.** For the one-hidden-unit network $h=\sigma(w_1x+b_1)$, $\hat{y}=w_2h+b_2$, $\ell=\tfrac12(\hat{y}-y)^2$ with sigmoid $\sigma$, take $x=1$, $y=1$, $w_1=0$, $b_1=0$, $w_2=1$, $b_2=0$. Compute the forward pass and all four gradients.

```{dropdown} Solution
Forward: $z_1=0$, $h=\sigma(0)=0.5$, $\hat{y}=0.5$, $\ell=\tfrac12(0.5-1)^2=0.125$. Backward（{eq}`eq-u4-bp2`–{eq}`eq-u4-bp1` with scalars）: $\delta_2=\hat{y}-y=-0.5$; $\partial\ell/\partial w_2=\delta_2 h=-0.25$; $\partial\ell/\partial b_2=\delta_2=-0.5$; $\sigma'(0)=\sigma(0)(1-\sigma(0))=0.25$, so $\delta_1=w_2\delta_2\sigma'(z_1)=1\cdot(-0.5)\cdot0.25=-0.125$; $\partial\ell/\partial w_1=\delta_1x=-0.125$; $\partial\ell/\partial b_1=\delta_1=-0.125$. One forward, one backward — four gradients.
```

**Exercise 2（one Adam step）.** A scalar parameter starts at $\theta=0$ with $m^{(0)}=v^{(0)}=0$; the first gradient is $\hat{g}^{(1)}=2$. With $\alpha=0.1$ and the defaults, compute the first Adam update, and compare with what would happen *without* bias correction.

```{dropdown} Solution
$m^{(1)}=0.1\cdot2=0.2$; $v^{(1)}=0.001\cdot4=0.004$. Corrections: $\hat{m}=0.2/(1-0.9)=2$; $\hat{v}=0.004/(1-0.999)=4$. Step: $\theta\leftarrow0-0.1\cdot2/(\sqrt4+10^{-8})=-0.1$. The corrected first step has magnitude exactly $\alpha$（in general, $\alpha\cdot\hat{g}/|\hat{g}|$ — a unit step in the natural per-coordinate scale）. Without correction: $-0.1\cdot0.2/\sqrt{0.004}\approx-0.316$ — three times too large, from moment estimates that are still mostly zeros. The $1-\beta^k$ factors exist precisely to make step one sane.
```

**Exercise 3（the residual highway）.** Caricature a deep network by scalars: plain layers $h_{l+1}=f(h_l)$ with $f'=0.1$ everywhere, versus residual layers $h_{l+1}=h_l+F(h_l)$ with $F'=0.1$. For $L=10$ layers, compare $\mathrm{d}h_{L}/\mathrm{d}h_{0}$.

```{dropdown} Solution
Plain: $\prod f'=0.1^{10}=10^{-10}$ — the input layer receives essentially no gradient. Residual（{eq}`eq-u4-res` in scalar form）: $\prod(1+F')=1.1^{10}\approx2.59$ — order one. The identity term turns a product of small numbers into a product of numbers near one: that is the entire trick, and why depth stopped being a barrier after 2016（He et al., CVPR 2016）.
```

```{seealso}
Where this unit points outward: the presentation-topic trends of the course — PINN（physics-informed neural networks）, FNO（Fourier neural operators）, Transformers — live on the [期末專題頁](../project.md). And the「cheap full gradient」economics of sec 2 returns as the adjoint method in Unit 7, driving real electromagnetic design in [labs/adjoint](../labs/adjoint.md).
```
