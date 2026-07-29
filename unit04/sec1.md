# Architecture: From a Single Neuron to the MLP

## The neuron

The building block（C&Z Ch. 13）is almost embarrassingly simple: an affine map followed by a scalar nonlinearity,

$$
h=\sigma(\boldsymbol{w}^{\top}\boldsymbol{x}+b),
$$

with **weights** $\boldsymbol{w}$, **bias** $b$, and **activation function** $\sigma$. Without $\sigma$ a neuron is linear regression; the nonlinearity is what buys expressive power, because compositions of affine maps collapse back to one affine map, while compositions of *nonlinear* maps do not.

The classical activations are the **sigmoid** $\sigma(z)=1/(1+e^{-z})$ and $\tanh(z)$ — smooth, bounded, biologically flavored. Modern practice overwhelmingly uses the **ReLU**, $\sigma(z)=\max(0,z)$, and its variants. The reason is an optimization fact, not a modeling one: the sigmoid's derivative is at most $1/4$ and vanishes at both tails, so in deep compositions gradient signals shrink geometrically（sec 2 makes this precise）, while ReLU passes gradients through its active half at slope exactly $1$ and costs one comparison to evaluate. Why ReLU won is a preview of this unit's theme: **architectures are chosen for how well they *optimize*, not only for what they can represent.**

## The multilayer perceptron

Stack neurons into layers, feed each layer's output to the next, and you have the **multilayer perceptron**（MLP）. With $\boldsymbol{h}_0=\boldsymbol{x}$,

$$
\boldsymbol{h}_{l}=\sigma\!\bigl(\boldsymbol{W}_{l}\boldsymbol{h}_{l-1}+\boldsymbol{b}_{l}\bigr),
\quad l=1,\dots,L-1,
\qquad
\hat{\boldsymbol{y}}=\boldsymbol{W}_{L}\boldsymbol{h}_{L-1}+\boldsymbol{b}_{L},
$$ (eq-u4-mlp)

where $\sigma$ acts componentwise and the last layer is usually left linear. The **universal approximation theorem**（statement only）says that even $L=2$ — one hidden layer — can approximate any continuous function on a compact set to any accuracy, given enough hidden units. That settles expressiveness in principle and *nothing* in practice: the theorem is silent about how many units, and about whether any algorithm can find the right weights. Depth earns its keep empirically — deep-and-narrow beats shallow-and-astronomically-wide — which is why the trainability questions of sec 2 matter.

## Training is Unit 2's problem

Collect every weight and bias into one parameter vector $\boldsymbol{\theta}\in\mathbb{R}^{n}$, and let $f_{\boldsymbol{\theta}}$ denote the network as a function. Given data $\{(\boldsymbol{x}_i,\boldsymbol{y}_i)\}_{i=1}^{N}$, choose a per-example **loss** $\ell$ — squared error $\tfrac12\|\hat{\boldsymbol{y}}-\boldsymbol{y}\|^2$ for regression, cross-entropy for classification — and *train* by minimizing the empirical risk:

$$
\min_{\boldsymbol{\theta}\in\mathbb{R}^{n}}\;
J(\boldsymbol{\theta})=\frac{1}{N}\sum_{i=1}^{N}\ell\bigl(f_{\boldsymbol{\theta}}(\boldsymbol{x}_i),\,\boldsymbol{y}_i\bigr).
$$ (eq-u4-erm)

```{important}
**A neural network is a parametrized function; training is exactly the unconstrained problem $\min f(\boldsymbol{x})$ of Unit 2** — with $\boldsymbol{\theta}$ playing the role of $\boldsymbol{x}$ and {eq}`eq-u4-erm` the objective. Everything we proved carries over verbatim: FONC says train until $\|\nabla J\|$ is small; the landscape is spectacularly nonconvex, so what we find is a local valley; and the choice of method is governed by the same economics as always — except the dimension is now $10^{6}$–$10^{11}$, which shifts the economics violently toward cheap first-order methods（sec 3）. What is genuinely new is *how the gradient is computed*（sec 2）and *how noise enters the iteration*（sec 3）.
```

Two vocabulary notes before the machinery. The nonconvexity of {eq}`eq-u4-erm` is not a defect to fix but a fact to live with: symmetric weight permutations alone create exponentially many equivalent minima, and practice consistently finds *good* valleys rather than *the* valley — the local-vs-global distinction of Unit 2, made peace with. And the true objective is not {eq}`eq-u4-erm` itself but performance on *unseen* data（generalization）; regularization terms and early stopping modify the optimization problem for statistical reasons. This course stays on the optimization side of that boundary, flagging the crossings.
