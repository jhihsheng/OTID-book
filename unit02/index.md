# Optimization Basics and One-Dimensional Search

**Unit 2**｜Reading: C&Z Ch. 6–7｜進度以上課宣布為準

```{note} Learning objectives (Unit 2)
1. Translate an engineering wish into the standard form $\min f(\boldsymbol{x})$, $\boldsymbol{x}\in\Omega$ — choose the decision variables, the objective, and the constraints, and defend the choices.
2. State the first- and second-order optimality conditions（FONC, SONC, SOSC）and apply them to classify a given stationary point.
3. Run golden-section search by hand, and explain where the ratio $0.618$ comes from and why Fibonacci search is optimal for a fixed evaluation budget.
4. Define order of convergence, derive Newton's one-dimensional iteration from Taylor's theorem, and check an Armijo backtracking condition numerically.
```

**Reading.** C&Z Ch. 6（basics of set-constrained and unconstrained optimization — the optimality conditions）and Ch. 7（one-dimensional search methods）. This unit is where the course stops *describing* optimization and starts *doing* it.

**Opening puzzle.** Your simulator takes an hour per run, and you may afford exactly $N=20$ evaluations of an unknown unimodal $f$ on an interval. How tightly can those twenty evaluations pin down the minimizer? Naive answers waste badly: an evenly spaced grid of 20 points narrows the uncertainty only to $2/21\approx10\%$ of the interval. The right strategy places each new evaluation so that *one of the two points it needs is already there from the previous step* — a self-similarity requirement whose unique solution is the golden ratio, shrinking the interval by $0.618$ per step and reaching $0.618^{19}\approx10^{-4}$ of the original length: a thousand times better than the grid, from the same budget. And a Fibonacci-number refinement is provably the best possible. The derivation — three lines of algebra — is in [Bracketing Methods](sec2.md). First, though, we must settle what「found the minimum」even certifies: the optimality conditions of [sec 1](sec1.md).
