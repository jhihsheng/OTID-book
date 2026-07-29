# Automatic Differentiation and Modern Numerical Computing

**Unit 8**｜Reading: whitelist references（autograd／JAX／Meep adjoint docs）｜進度以上課宣布為準

```{note} Learning objectives (Unit 8)
1. Differentiate a small program by hand in forward mode（dual numbers）and reverse mode（adjoints）, and choose the right mode from the input/output counts.
2. Reproduce the finite-difference total-error analysis — truncation vs roundoff — and explain why automatic differentiation escapes it entirely.
3. State the equivalence between the adjoint method of Unit 7 and reverse-mode AD applied to a solver, and explain checkpointing for time-stepping codes.
4. Diagnose the standard numerical failure modes — catastrophic cancellation, non-differentiable operations, loosely converged inner solvers — and write vectorized, reproducible scientific code.
```

**Reading.** No textbook chapter matches this unit; the working references are the tools' own documentation — [autograd](https://github.com/HIPS/autograd), the [Meep adjoint solver](https://meep.readthedocs.io/en/latest/Python_Tutorials/Adjoint_Solver/) built on it, and the JAX/PyTorch docs for the wider ecosystem.

**Opening puzzle.** You need $f'(1)$ for $f=\sin$, so you write the obvious finite difference and, being careful, make $h$ *very* small: $h=10^{-16}$. The computer returns **exactly zero** — not approximately, exactly. Make $h$ bigger, $10^{-8}$, and you get eight correct digits; bigger still and accuracy *falls* again. Smaller was supposed to be better; instead there is a forbidden zone on both sides（sec 1's [](#fig-u8-fderror), computed live）. Meanwhile `autograd.grad(np.sin)(1.0)` returns $\cos(1)$ to all sixteen digits, with no $h$ anywhere in sight. Two mysteries, one resolution: the anatomy of a floating-point number（sec 3）, and the realization that differentiation-by-program — neither symbolic nor numerical — is *exact*（sec 1）. That third way of differentiating, scaled up, is how neural networks train（Unit 4）and how Meep computes the adjoint gradients of Unit 7 — a claim this unit sharpens into a theorem, closing the circle of Part I.
