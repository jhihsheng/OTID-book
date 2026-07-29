# The Electromagnetic Adjoint

## Maxwell as $\boldsymbol{A}(\varepsilon)\boldsymbol{x}=\boldsymbol{b}$

In the frequency domain, the electric field of a linear device obeys

$$
\Bigl(\nabla\times\nabla\times\;-\;\omega^{2}\varepsilon(\boldsymbol{r})\Bigr)\boldsymbol{E}
=\mathrm{i}\omega\,\boldsymbol{J}_{\text{src}} ,
$$ (eq-u7-maxwell)

（units with $\mu=1,\ c=1$）. Discretized, this is precisely {eq}`eq-u7-state`: $\boldsymbol{x}\leftrightarrow\boldsymbol{E}$, $\boldsymbol{b}\leftrightarrow$ the source current, and the design enters through $\boldsymbol{A}(\varepsilon)$ — *linearly*, since $\varepsilon(\boldsymbol{r})$ sits in the diagonal term. A pixel's density changes only the $-\omega^2\varepsilon$ entries at that pixel, which is why $\partial\boldsymbol{A}/\partial p_i$ in {eq}`eq-u7-grad` is so sparse and the gradient assembly so cheap: the abstract machinery of sec 1 was custom-built for electromagnetics without knowing it.

## The adjoint simulation is just another simulation

What is the adjoint solve {eq}`eq-u7-adjoint`, physically? Two observations turn it from linear algebra into optics.

**The right-hand side is a source placed by the objective.** $\bigl(\partial J/\partial\boldsymbol{x}\bigr)^{\!\top}$ is nonzero only where $J$ actually reads the field — the output port's mode monitor, the focal point, the detector plane. So the adjoint equation is a Maxwell problem whose *current source sits at the measurement*, radiating backwards into the device（[](#fig-u7-sources)）. If $J$ is the power coupled into the output waveguide mode, the adjoint source is that mode, injected *from* the output port.

**Reciprocity makes $\boldsymbol{A}^{\!\top}$ harmless.** For the reciprocal materials of this course（no magneto-optics, no nonlinearity）, Lorentz reciprocity makes the Maxwell operator symmetric under the appropriate unconjugated inner product — transposing $\boldsymbol{A}$ gives back essentially the same physics. Practical consequence: **the adjoint solve is an ordinary forward simulation with a different source** — same solver, same mesh, same runtime, zero new solver code. This is why every FDTD/FEM package could grow an adjoint module（Meep's is the one the labs use）.

```{figure} ../assets/u07_adjoint_sources.png
:name: fig-u7-sources
:width: 96%

The two simulations of one gradient step. Forward: physical source at the input; the monitor defines $J$. Adjoint: the objective's derivative becomes a source at the monitor, radiating back through the same structure. The design gradient lives where the two fields overlap.
```

## The gradient as interference

Insert the Maxwell form into the gradient formula {eq}`eq-u7-grad`. Since $\partial\boldsymbol{A}/\partial\varepsilon(\boldsymbol{r})$ is（minus）$\omega^2$ times a delta at $\boldsymbol{r}$, the sum collapses to a *local product of the two fields*:

$$
\frac{\delta J}{\delta\varepsilon(\boldsymbol{r})}
\;\propto\;
\operatorname{Re}\bigl[\boldsymbol{E}_{\text{adj}}(\boldsymbol{r})\cdot\boldsymbol{E}_{\text{fwd}}(\boldsymbol{r})\bigr],
$$ (eq-u7-overlap)

up to constants and sign conventions fixed by the solver's definitions（the labs follow the Meep adjoint documentation's conventions — when in doubt, defer to them, because a sign error here silently inverts your optimizer）. Equation {eq}`eq-u7-overlap` has a beautiful reading: **the gradient is an interference pattern**. The forward field says where light actually is; the adjoint field says where light *would need to come from* to please the objective; where the two oscillate in phase, a grain of extra dielectric scatters forward light into objective-pleasing light — add material there. Where they are out of phase, material hurts — carve it away. The optimizer of sec 3 does nothing more than repeatedly develop this interference photograph and deposit material accordingly; watching `bend_waveguide.mp4` again after this section, you can almost see it thinking.

Two practical footnotes. First, the same two-solve accounting holds for *any number of objectives read from one field* but multiplies per **frequency**: a broadband design with $K$ frequencies needs $K$ forward＋adjoint pairs（or clever broadband sources — the labs' notebook 09 handles the multi-frequency case）. Second, in time-domain solvers（FDTD）the adjoint runs *backward in time*, which is why gradients of long simulations are memory-hungry — a story Unit 8 picks up under the name *checkpointing*.
