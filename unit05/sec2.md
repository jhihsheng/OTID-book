# Population-Based Metaheuristics: GA, PSO, DE

Metropolis walks one configuration; the population family searches with a *crowd* whose members exchange information. Three algorithms are taught content here — not asides — because each embodies a different theory of how a crowd should share what it learns.

## Genetic algorithms: recombine what works

The **genetic algorithm**（C&Z Ch. 14; modern treatment in Kochenderfer & Wheeler）breeds designs. Its components, in the order they act each generation:

- **Encoding**: a design is a chromosome — a bit string for discrete problems, a real vector for continuous ones. The encoding *is* a modeling decision: neighborhoods in gene space should correspond to similar designs.
- **Fitness**: the objective, possibly rescaled（selection cares only about ranking）.
- **Selection**: choose parents preferentially by fitness — **roulette wheel**（probability $\propto$ fitness）or, more robustly, **tournament**（pick the best of a random handful; insensitive to fitness scaling）.
- **Crossover**: children inherit segments（bit strings）or blends（real vectors）from two parents — the distinctive move: it can combine a good left half with a good right half found by *different* lineages.
- **Mutation**: small random perturbations at low rate — the diversity tax that keeps the gene pool from collapsing.
- **Elitism**: copy the best individual unchanged, so progress never regresses.

Why should recombination work? The **schema intuition**, one paragraph: think of a chromosome as carrying short building blocks（*schemata* — patterns like「…101…」）. Selection multiplies blocks that correlate with fitness; crossover assembles blocks discovered separately into single individuals. GA thrives exactly when the problem *has* such separable building blocks, and flails when genes interact strongly — no-free-lunch, in concrete form.

## Particle swarm optimization: follow your memory and your neighbors

**PSO**（Kennedy & Eberhart, Proc. IEEE ICNN, 1995）flies a swarm of particles through continuous space. Particle $i$ carries position $\boldsymbol{x}_i$ and velocity $\boldsymbol{v}_i$, remembers its personal best $\boldsymbol{p}_i$, and sees the swarm's global best $\boldsymbol{g}$:

$$
\boldsymbol{v}_i\;\leftarrow\;
w\,\boldsymbol{v}_i
+c_1\boldsymbol{r}_1\odot(\boldsymbol{p}_i-\boldsymbol{x}_i)
+c_2\boldsymbol{r}_2\odot(\boldsymbol{g}-\boldsymbol{x}_i),
\qquad
\boldsymbol{x}_i\;\leftarrow\;\boldsymbol{x}_i+\boldsymbol{v}_i,
$$ (eq-u5-pso)

with $\boldsymbol{r}_1,\boldsymbol{r}_2$ fresh uniform random vectors in $[0,1]^n$. Three forces in {eq}`eq-u5-pso`: **inertia** $w$（≈0.7）keeps exploration alive; the **cognitive** pull $c_1$（≈1.5）draws each particle back toward its own best memory; the **social** pull $c_2$（≈1.5）draws it toward the crowd's best. One remark on topology: broadcasting one *global* best converges fast but can stampede the swarm into a mediocre valley; *local-best* variants（each particle sees only a few neighbors）trade speed for diversity.

## Differential evolution: let the population set its own step size

**DE**（Storn & Price, *J. Global Optim.* **11**, 341–359, 1997）is the most economical idea of the three. For each target $\boldsymbol{x}_i$, build a mutant from three distinct random members（the DE/rand/1 strategy）:

$$
\boldsymbol{v}=\boldsymbol{x}_{r_1}+F\,(\boldsymbol{x}_{r_2}-\boldsymbol{x}_{r_3}),
\qquad F\in(0,2],
$$ (eq-u5-de)

then **binomial crossover**: build a trial $\boldsymbol{u}$ by taking each coordinate from $\boldsymbol{v}$ with probability $CR$（and at least one coordinate from $\boldsymbol{v}$, guaranteed）, otherwise from $\boldsymbol{x}_i$; finally **greedy selection**: keep whichever of $\boldsymbol{u},\boldsymbol{x}_i$ is better. The genius is in {eq}`eq-u5-de`: the perturbation is a *difference of population members*, so its typical size and orientation automatically track the population's current spread — large and exploratory early, small and refining as the crowd contracts, anisotropic if the population has found a valley direction. DE self-scales with zero schedule, has only three hyperparameters（population size, $F$, $CR$）, and its reputation as a strong default for continuous black-box problems（Storn & Price's benchmarks and two decades of practice since）rests on that self-scaling.

## Choosing: mechanisms at a glance

| Method | Core mechanism | Continuous／discrete | Key hyperparameters | Reach for it when |
|---|---|---|---|---|
| Random search | independent samples | both | none | baseline; sanity check |
| GA | selection＋crossover＋mutation | both（encoding-dependent） | pop. size, crossover/mutation rates | building-block structure; discrete encodings |
| PSO | memory＋social attraction | continuous | $w,c_1,c_2$, pop. size | smooth-ish continuous, cheap $f$ |
| DE | population-difference mutation | continuous | pop. size, $F$, $CR$ | continuous black-box default |
| SA（sec 3） | Metropolis＋cooling | both | $T_0$, cooling rate, proposal size | discrete moves; single-thread simplicity |

```{figure} ../assets/u05_metaheuristics.png
:name: fig-u5-bench

The unit's signature experiment（`figs_src/u05_metaheuristics.py`, fixed seeds）: best-so-far on the 10-D Rastrigin function, equal budgets of 6000 evaluations, 20 runs each — median lines, interquartile bands. In *this* setup the GA's blend-crossover happens to suit Rastrigin's lattice of minima, PSO follows, and DE and SA lag at this budget with these hyperparameters — rerun with a larger budget, retuned $F/CR$, or a different test function and the ranking reshuffles. That instability *is* the lesson: with heuristics, benchmark on **your** problem; trust mechanisms, not league tables（no free lunch）.
```

```{seealso}
[labs/opti](../labs/opti.md): **notebook 03 implements PSO** with exercises — the direct hands-on companion of this section — plus simulated annealing ahead of sec 3. The discrete-design thread continues in [labs/qa](../labs/qa.md).
```
