# Gradient, Newton, CG and Quasi-Newton Methods

**Unit 3**｜Reading: C&Z Ch. 8–11, 15（Ch. 12 skipped）｜進度以上課宣布為準

```{note} Learning objectives (Unit 3)
1. Implement steepest descent with exact or backtracking line search, and *predict* its convergence rate from the condition number $\kappa$ of the Hessian.
2. Derive the multidimensional Newton step from Taylor's theorem, explain when and why it breaks, and repair it with the Levenberg–Marquardt modification.
3. Explain $\boldsymbol{Q}$-conjugacy, run the conjugate-gradient algorithm, and account for its $n$-step exact termination on quadratics.
4. State the secant condition, perform one BFGS update by hand, and describe the standard form of a linear program and where its optimum must lie.
```

**Reading.** C&Z Ch. 8（gradient methods）, Ch. 9（Newton's method）, Ch. 10（conjugate direction methods）, Ch. 11（quasi-Newton methods）; Ch. 15（introduction to linear programming）is touched briefly in [sec 4](sec4.md). Ch. 12 is deliberately skipped.

**Opening puzzle.** Take the most innocent problem imaginable — a quadratic bowl in just *two* variables, $f=\tfrac12(x_1^2+9x_2^2)$ — and run gradient descent with a *perfect* line search from $(9,1)$. Every step is locally optimal, yet the error shrinks by only $0.8$ per iteration: about ten iterations *per digit*, forever, in a zig-zag that never learns from its own history（and for a realistic $\kappa=100$, nearer sixty iterations per digit）. Now change one line of the code — make each new direction $\boldsymbol{Q}$-*conjugate* to the previous one instead of merely downhill — and the same problem finishes **exactly, in two steps**. Locally optimal moves are globally naive; this unit is about what the fast methods（conjugate gradients, Newton, BFGS）know that the gradient alone does not, and what each one pays for that knowledge.
