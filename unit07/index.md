# Adjoint Method and Density-Based Topology Optimization

**Unit 7**｜Reading: S. G. Johnson, *Notes on adjoint methods*（MIT 18.336）; Hammond et al., *Opt. Express* **30**, 4467–4491 (2022)｜進度以上課宣布為準

```{note} Learning objectives (Unit 7)
1. Derive the adjoint gradient formula for $J(\boldsymbol{x}(\boldsymbol{p}))$ under $\boldsymbol{A}(\boldsymbol{p})\boldsymbol{x}=\boldsymbol{b}$ two ways — by chain rule and by Lagrangian — and explain why the cost is two solves, independent of the number of parameters.
2. Describe the electromagnetic adjoint simulation: where its source sits, why reciprocity makes it an ordinary Maxwell solve, and what field overlap gives the design gradient.
3. Walk through the density-based topology-optimization pipeline — filter, project, interpolate, solve, adjoint, update, $\beta$-continuation — and state what each stage is for.
4. Count simulations honestly for a given design task（naive vs adjoint）and predict the sign of a density update from a given field overlap.
```

**Reading.** Johnson's *Notes on adjoint methods*（<https://math.mit.edu/~stevenj/18.336/adjoint.pdf>）is the cleanest derivation in existence and the source our sec 1 follows. Hammond, Oskooi, Chen, Lin, Johnson & Ralph（*Opt. Express* **30**, 4467, 2022）is the modern reference implementation — the Meep adjoint solver that [notebooks 08–09](../labs/adjoint.md) run.

**Opening puzzle.** A modest design region of $100\times100$ pixels has $10^4$ design parameters. To take one gradient step, finite differences need $10^4$ simulations — at a minute each, a *week per step*, months per design. Yet notebook 08 computes the **exact** gradient of exactly such a design in **two** simulations: one forward, one extra. Not an approximation — the same numbers finite differences would eventually produce, at a $5000\times$ discount. The discount is the adjoint method, and the suspicious part is the arithmetic: how can $10^4$ derivatives possibly cost two solves? The resolution（sec 1, derived twice in a page each way）is a regrouping of linear algebra so simple it feels like an accounting trick — the same trick that backpropagation plays for neural networks（Unit 4）, which is no coincidence（Unit 8 proves they are one theorem）. This is the unit the course has been building toward.
