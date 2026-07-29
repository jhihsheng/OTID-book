# Backpropagation and Depth

## The forward pass is a computational graph

Evaluating {eq}`eq-u4-mlp` is a left-to-right sweep through a **computational graph**: nodes hold intermediate quantities（$\boldsymbol{z}_l$, $\boldsymbol{h}_l$）, edges carry them into the next operation, and the loss $\ell$ sits at the far right（[](#fig-u4-mlp)）. The observation that powers all of deep learning — and, in Unit 8, all of automatic differentiation — is that the same graph traversed *right to left* computes every derivative the training loop needs, in one sweep, reusing the intermediates stored on the way forward.

```{figure} ../assets/u04_mlp_graph.png
:name: fig-u4-mlp
:width: 92%

A two-layer MLP as a computational graph. Forward（blue）: evaluate and cache $\boldsymbol{z}_1,\boldsymbol{h},\hat{y}$. Backward（red）: one right-to-left sweep of the chain rule delivers $\partial\ell/\partial$(every weight)—the gradient's cost is a small constant times the forward cost, independent of the parameter count.
```

## Backprop on a two-layer network, in full

Take the two-layer regression network of the figure: $\boldsymbol{z}_1=\boldsymbol{W}_1\boldsymbol{x}+\boldsymbol{b}_1$, $\boldsymbol{h}=\sigma(\boldsymbol{z}_1)$, $\hat{y}=\boldsymbol{w}_2^{\!\top}\boldsymbol{h}+b_2$, $\ell=\tfrac12(\hat{y}-y)^2$. We want $\partial\ell/\partial$ everything. Work backwards with the chain rule（Unit 1）, defining at each stage the **error signal** $\delta=\partial\ell/\partial(\text{that stage's preactivation})$.

**Output stage.** $\displaystyle \delta_2=\frac{\partial\ell}{\partial\hat{y}}=\hat{y}-y$. Since $\hat{y}$ is linear in $\boldsymbol{w}_2$ and $b_2$:

$$
\frac{\partial\ell}{\partial\boldsymbol{w}_2}=\delta_2\,\boldsymbol{h},
\qquad
\frac{\partial\ell}{\partial b_2}=\delta_2 .
$$ (eq-u4-bp2)

**Hidden stage.** Push $\delta_2$ one layer back. First to $\boldsymbol{h}$: $\partial\ell/\partial\boldsymbol{h}=\delta_2\,\boldsymbol{w}_2$. Then through the elementwise $\sigma$, which multiplies componentwise by $\sigma'(\boldsymbol{z}_1)$:

$$
\boldsymbol{\delta}_1=\frac{\partial\ell}{\partial\boldsymbol{z}_1}
=\bigl(\delta_2\,\boldsymbol{w}_2\bigr)\odot\sigma'(\boldsymbol{z}_1),
\qquad\text{whence}\qquad
\frac{\partial\ell}{\partial\boldsymbol{W}_1}=\boldsymbol{\delta}_1\,\boldsymbol{x}^{\!\top},
\quad
\frac{\partial\ell}{\partial\boldsymbol{b}_1}=\boldsymbol{\delta}_1 .
$$ (eq-u4-bp1)

That is the whole algorithm — **backpropagation**（C&Z Ch. 13）is the chain rule, organized so that each layer's error signal is computed once and shared by all that layer's parameters. Count the work: the backward sweep does one matrix–vector product per layer, the same shape of work as the forward sweep. So the *full gradient* — every entry of $\nabla_{\boldsymbol{\theta}}\ell$, be there $10^3$ or $10^{11}$ parameters — costs **a small constant multiple（≈2–3×）of one forward evaluation**, plus the memory to cache the forward intermediates. Compare finite differences: $n+1$ forward passes. This ratio, forward-cost-to-gradient-cost independent of $n$, is *the* enabling economics of deep learning; hold onto it, because the adjoint method of Unit 7 delivers the identical bargain for Maxwell's equations, and Unit 8 shows both are one theorem.

## Why depth is hard: vanishing and exploding gradients

Backprop through $L$ layers multiplies $L$ Jacobians: schematically, the error signal at layer $l$ is $\boldsymbol{\delta}_l\sim\bigl(\prod_{j>l}\boldsymbol{W}_j^{\!\top}\operatorname{diag}\sigma'(\boldsymbol{z}_j)\bigr)\boldsymbol{\delta}_L$. A product of $L$ factors each of typical size $\gamma$ scales like $\gamma^{L}$: for $\gamma<1$ the signal **vanishes** exponentially（early layers stop learning）; for $\gamma>1$ it **explodes**（training blows up）. Sigmoid networks vanish almost by decree — $\sigma'\le\tfrac14$ — which is the honest reason deep learning stalled for two decades. Three modern repairs:

**ReLU**（sec 1）passes slope exactly $1$ on its active half, removing the systematic $\le\tfrac14$ shrinkage.

**Initialization.** Draw initial weights with variance tuned so each layer preserves signal magnitude: $\operatorname{Var}(w)=1/n_{\text{in}}$（Xavier, for tanh）or $2/n_{\text{in}}$（He, for ReLU — the factor 2 compensates the half of the units that are off）. One paragraph, but load-bearing in practice: bad initialization loses the game before the first step.

**Residual connections.** The decisive fix（He et al., CVPR 2016）: instead of $\boldsymbol{h}_{l+1}=F_l(\boldsymbol{h}_l)$, let each block learn only a *correction to the identity*,

$$
\boldsymbol{h}_{l+1}=\boldsymbol{h}_l+F_l(\boldsymbol{h}_l)
\qquad\Longrightarrow\qquad
\frac{\partial\boldsymbol{h}_{l+1}}{\partial\boldsymbol{h}_l}=\boldsymbol{I}+\frac{\partial F_l}{\partial\boldsymbol{h}_l}.
$$ (eq-u4-res)

Multiply the per-layer factors {eq}`eq-u4-res` and expand: the product contains a pure-identity term plus corrections. The identity term is a **gradient highway** — a path along which the error signal reaches layer 1 *unattenuated*, no matter the depth. Networks jumped from tens to hundreds of layers essentially overnight; Exercise 3 quantifies the difference on a scalar caricature.

**Batch normalization**, in one paragraph: normalize each unit's preactivations to zero mean and unit variance over the current minibatch（then rescale by learned parameters）. It keeps activations in the responsive region of $\sigma$, makes the loss landscape smoother and less sensitive to the learning rate, and in practice permits larger steps — an optimization aid wearing a statistics costume.

The remaining question — given a gradient this cheap, *which first-order update rule to run* — is [sec 3](sec3.md).
