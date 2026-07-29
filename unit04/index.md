# Neural Networks and Optimization for Deep Learning

**Unit 4**｜Reading: C&Z Ch. 13 + modern supplements｜進度以上課宣布為準

```{note} Learning objectives (Unit 4)
1. Describe the multilayer perceptron as a parametrized function and training as the unconstrained optimization problem of Units 2–3.
2. Derive backpropagation for a two-layer network by hand, and explain why one backward sweep prices *all* parameter gradients at a small constant multiple of one forward evaluation.
3. Explain vanishing/exploding gradients and how ReLU, careful initialization, and residual connections keep deep networks trainable.
4. Write down the SGD, momentum, and Adam update rules（with bias correction）, execute one Adam step numerically, and interpret Adam as steepest descent with an adaptive diagonal preconditioner.
```

**Reading.** C&Z Ch. 13（single neuron, the multilayer feedforward network, and the backpropagation algorithm）. The optimizer landscape moved on after 2008, so sec 3 supplements the textbook with the two primary sources of modern practice: Kingma & Ba（ICLR 2015, Adam）and He et al.（CVPR 2016, residual networks）.

**Opening puzzle.** The largest models in use today have on the order of $10^{11}$ trainable parameters. Newton's method would need a Hessian with $10^{22}$ entries — thousands of exabytes, more numbers than there are grains of sand on Earth — and even *storing one extra vector* is a memory decision. Yet these models are trained, successfully, by the humblest algorithm in this course: steepest descent, lightly dressed up. Two questions should bother you. *How is the gradient of a function with $10^{11}$ inputs computed at all* — surely not by $10^{11}$ finite differences? And *why does the method that Unit 3 proved slowest win at the largest scale*? The answers — backpropagation's two-pass economics, and the fact that at $10^{11}$ parameters the per-iteration price of being clever exceeds the price of being patient — are this unit, and they preview the same economics that will make photonic inverse design possible in Unit 7.
