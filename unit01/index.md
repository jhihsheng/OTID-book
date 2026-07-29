# Mathematical Preliminaries 數學複習

**Unit 1**｜Reading: C&Z Ch. 1–5｜進度以上課宣布為準

```{note} Learning objectives (Unit 1)
1. Formulate an engineering design task in the standard form $\min f(\boldsymbol{x})$ subject to $\boldsymbol{x}\in\Omega$, and identify the objective, the decision variables, and the feasible set.
2. Test a symmetric matrix for positive (semi)definiteness by the eigenvalue test and by Sylvester's leading-principal-minor test.
3. Compute gradients, Hessians, and directional derivatives, and expand a function of several variables to second order with Taylor's theorem.
4. Recognize convex sets and level sets, and sketch the level sets of a quadratic function from the eigenstructure of its matrix.
```

**Reading.** Chong & Zak, *An Introduction to Optimization*, 3rd ed., Ch. 1–5（Part I of the book — the mathematical-review chapters）. This unit condenses them to what the rest of the course actually uses.

**Opening puzzle.** A coating designer wants a 10-layer stack that transmits green and blocks blue（the [TMM mini-project](../labs/tmm.md)）. The design space is a point $\boldsymbol{x}\in\mathbb{R}^{10}$ of layer thicknesses. A crude grid with just ten samples per thickness already costs $10^{10}$ spectrum evaluations — decades of compute. Yet a laptop finds an excellent design in minutes. It never *searches* the space at all: at each design it asks one local question —「which infinitesimal change improves the spectrum fastest?」— and moves that way. For that question to make sense, and for its answer to be trustworthy, we need exactly the mathematics of this unit: gradients and Hessians（the local model）, positive definiteness（when「flat」means「minimum」）, and Taylor's theorem（why a local model predicts anything at all）. That is why a math review opens an optimization course.
