# Automatic Differentiation Fundamentals

## Three ways to differentiate a program

**Symbolic** differentiation manipulates formulas; applied to a thousand-line simulation it produces expression swell and demands the program *be* a formula, which it is not. **Numerical** differentiation（finite differences）only needs function values — and pays for that convenience with an accuracy ceiling analyzed below. **Automatic differentiation**（AD）is the third way: a program is a *composition of elementary operations*, each with a known exact derivative, so the chain rule can be applied mechanically to the program itself. AD evaluates derivatives — not approximations of them — at a small constant multiple of the cost of the original program.

## The finite-difference error budget（and why it matters here）

Before praising AD, be quantitative about what it replaces. The forward difference $D_h f=\bigl(f(x+h)-f(x)\bigr)/h$ carries two errors. Taylor's theorem {eq}`eq-u1-taylor` gives the **truncation error** $\tfrac{h}{2}|f''|$ — shrinking with $h$. But the computer evaluates $f$ only to relative precision $\varepsilon_{\text{mach}}\approx2.2\times10^{-16}$（sec 3）, so the *subtraction* carries absolute noise $\sim\varepsilon_{\text{mach}}|f|$, and dividing by $h$ amplifies it: **roundoff error** $\sim\varepsilon_{\text{mach}}|f|/h$ — *growing* as $h$ shrinks. The total, $\sim\tfrac{h}{2}|f''|+\varepsilon_{\text{mach}}|f|/h$, is V-shaped with its optimum near $h^{*}\sim\sqrt{\varepsilon_{\text{mach}}}\approx10^{-8}$, where the error is $\sim\sqrt{\varepsilon_{\text{mach}}}$: **half your digits are gone, at the best possible $h$**. Central differences improve the exponents（optimum $h\sim\varepsilon_{\text{mach}}^{1/3}$, error $\sim\varepsilon_{\text{mach}}^{2/3}$）but not the story. [](#fig-u8-fderror) shows the real, computed curves — including the cliff at $h=10^{-16}$ where $x+h$ rounds back to $x$ and the difference is exactly zero（the opening puzzle）.

```{figure} ../assets/u08_fd_error.png
:name: fig-u8-fderror
:width: 88%

The finite-difference error budget, computed in float64（`figs_src/u08_fd_error.py`）: truncation falls with $h$, roundoff grows as $\varepsilon_{\text{mach}}/h$, and the best achievable error is $\sim10^{-8}$（forward）or $\sim10^{-11}$（central）. AD sits on the green line: exact to machine precision, no $h$ to tune.
```

Add the cost dimension and finite differences lose twice: $n$ parameters require $n{+}1$ evaluations（Unit 7's week-per-gradient）*and* each derivative is half-precision. AD fixes both.

## Forward mode: dual numbers

Attach to every value a tangent — implement arithmetic on pairs $(v,\dot v)$, or equivalently on **dual numbers** $v+\dot v\,\epsilon$ with the algebraic rule $\epsilon^2=0$. Then

$$
(u+\dot u\epsilon)(v+\dot v\epsilon)=uv+(u\dot v+\dot u v)\,\epsilon,
\qquad
\sin(v+\dot v\epsilon)=\sin v+\cos v\,\dot v\,\epsilon
$$

— the product rule and chain rule *emerge from the algebra*. Seed an input with $\dot x=1$, run the program once, and every intermediate carries its exact derivative along; the output's tangent is $\mathrm{d}y/\mathrm{d}x$. One sweep yields the derivative with respect to **one input**（a Jacobian–vector product, JVP）; the full gradient of an $n$-input function costs $n$ sweeps.

## Reverse mode: adjoints

Run the program forward once, *caching* intermediates; then sweep the computational graph **backwards**, propagating adjoints $\bar v=\partial y/\partial v$ from the output toward the inputs（a vector–Jacobian product, VJP）. One reverse sweep yields the derivative of **one output with respect to every input**. [](#fig-u8-modes) walks both sweeps over the same small graph. You have met reverse mode twice already: applied to a neural network's loss it *is* backpropagation（Unit 4, error signals = adjoints）; applied to a PDE solve it will turn out to be the adjoint method（[sec 2](sec2.md)）— the shared name is not an accident.

```{figure} ../assets/u08_modes.png
:name: fig-u8-modes
:width: 95%

One computational graph（$y=\sin(x_1x_2)+x_1$）, two sweeps. Forward mode pushes tangents with the values — cheap per *input*. Reverse mode caches values, then pulls adjoints backwards — cheap per *output*.
```

```{important}
**The cost asymmetry is the whole game.** For $f:\mathbb{R}^{n}\to\mathbb{R}^{m}$, forward mode costs $\sim n$ program evaluations; reverse mode costs $\sim m$（plus the memory to cache the forward pass）. Optimization objectives are $m=1$ with $n$ huge — so **reverse mode computes the entire gradient for a small constant multiple of one evaluation**, whatever $n$ is. That constant-versus-$n$ gap is the same economics that made backprop（$n\sim10^{11}$, Unit 4）and adjoint design（$n\sim10^{4}$, Unit 7）possible. Forward mode still wins in the opposite regime（few inputs, many outputs）— parameter sensitivity of a whole field map, for instance.
```
