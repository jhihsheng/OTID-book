# Parameterizations of the Design Space

## The decision that shapes everything

The rule $\boldsymbol{p}\mapsto\varepsilon(\boldsymbol{r})$ — how numbers become geometry — is the most consequential modeling choice in inverse design. It fixes the dimension of the search space, the smoothness of $J(\boldsymbol{p})$, which optimizers are even admissible, and how manufacturable the result will be. Three families cover the practice（[](#fig-u6-param)）:

```{figure} ../assets/u06_parameterizations.png
:name: fig-u6-param
:width: 98%

The three parameterization families:（a）a handful of physical shape parameters,（b）an implicit boundary — the zero level set of a function $\phi$,（c）a material density per pixel.
```

**（a）Few-parameter / shape parameterization.** The design is a known topology with adjustable dimensions: layer thicknesses of a stack, radius and gap of a ring, period and fill factor of a grating. Dimensions: a handful. The geometry stays interpretable and manufacturable by construction, and any optimizer works — including the bracketing and quasi-Newton methods of Units 2–3 and the metaheuristics of Unit 5. The ceiling is imagination: the optimizer can only tune *your* idea, never propose a better topology.

**（b）Level-set parameterization.** Represent the material boundary implicitly as $\{\boldsymbol{r}:\phi(\boldsymbol{r})=0\}$, material where $\phi<0$; optimize the function $\phi$. Boundaries stay *sharp*（binary structures at every iteration — a fabrication virtue）, yet the topology may change as $\phi$ develops new zero crossings: islands can appear and merge. The cost is machinery: evolving $\phi$ needs shape-derivative calculus, and the method sits between the extremes in both power and complexity. In this course we name it and move on.

**（c）Density-based / freeform topology optimization.** The design region becomes a grid; each pixel carries a density $\rho_i\in[0,1]$ interpolating between the two materials. Dimensions: $10^3$–$10^6$. Nothing about the final topology is presupposed — this is the parameterization that *discovers* the archipelago-like bends of the opening puzzle. Two consequences follow immediately. Only gradient methods can move in a million-dimensional space, and only the adjoint trick makes those gradients affordable（Unit 7）. And intermediate densities $\rho=0.4$ are physically meaningless（「40% silicon」is not a material）, so the pipeline must *push* designs toward binary — the filtering/projection machinery of Unit 7 sec 3.

## Fabrication constraints

An unconstrained optimizer will happily produce single-pixel islands, knife-edge features, and checkerboards — unbuildable, and often numerical artifacts exploiting the discretization. Real pipelines impose:

- **Minimum feature size**: no solid or void feature below the lithography limit（imposed by *filtering* the density with a kernel of that radius — Unit 7）;
- **Binarization**: final $\rho\in\{0,1\}$（imposed by *projection* with increasing sharpness）;
- **Connectivity / no floating islands**: material that nothing supports cannot be fabricated in many platforms（handled by constraints or post-selection）.

A design that ignores these is not a design; it is a simulation curiosity. Constraint handling is not a footnote to inverse design — it is half the engineering.

```{important}
**The organizing fork of the course, now in design language.** Choose a *continuous* parameterization（thicknesses, densities）and $J(\boldsymbol{p})$ is differentiable: the gradient route applies — adjoint gradients（Unit 7）feeding L-BFGS or CCSA（Unit 3）. Choose a *discrete/binary* parameterization（etched/not-etched cells, binary phases）and there is no gradient to take: the heuristic route applies — SA and QA（Unit 5）on an Ising/QUBO encoding. The two Applications threads of the official syllabus are exactly the two tines: 濾波器反向設計 walks the gradient route（[labs/tmm](../labs/tmm.md) → [labs/adjoint](../labs/adjoint.md)）; 1D 光柵設計 walks the annealing route（[labs/qa](../labs/qa.md)）. Parameterization choice *is* method choice.
```
