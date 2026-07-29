# Monte Carlo Methods and Global Search

## Where Units 2–4 stop working

Everything so far assumed a gradient worth following. Two situations void that assumption. **Discrete variables** — binary phases, material choices, on/off pixels — have no infinitesimal neighborhoods, so $\nabla f$ does not exist. And **rugged landscapes** — many local minima separated by barriers — make the gradient worse than useless: it works flawlessly, delivering you to the *nearest* valley and holding you there（Unit 2's local-vs-global distinction, now with teeth）. The official course fork（Unit 1）branches here: this unit is the gradient-free branch, and its engine is randomness.

## Random search and multistart

The bluntest instrument: sample $\boldsymbol{x}$ uniformly, keep the best — **naive random search**. It is unbiased, trivially parallel, assumption-free, and slow: in $n$ dimensions the volume within distance $\varepsilon$ of the optimum shrinks like $\varepsilon^{n}$, so expected hitting time grows exponentially（the curse of dimensionality, from Unit 1's opening puzzle, now as a lower bound on ignorance）. One notch smarter is **multistart**: run a fast local method（Unit 3）from many random initializations and keep the best valley found — the workhorse compromise in photonics practice, where local minima are plentiful but decent ones are common. Both serve as the *baselines every heuristic must beat*; the grey dotted line in sec 2's benchmark figure keeps them honest.

## Monte Carlo as a computational principle

「Monte Carlo」names an idea bigger than optimization: **replace an intractable computation by the statistics of random samples**. To estimate an integral or an average over a huge space, draw samples and average; the error shrinks like $1/\sqrt{N_{\text{samples}}}$ *independent of dimension* — precisely where deterministic grids die. The same principle powers both uses in this course: sampling for *estimation*（averages over configurations — this is also the minibatch idea of Unit 4 in disguise）and sampling for *search*（this unit）. The official course topic「Monte Carlo method」is exactly this section's content.

The refinement that changed computational science is *importance*: do not sample uniformly, sample preferentially where it matters. For a physical system at temperature $T$, configurations should appear with Boltzmann weight $\propto e^{-E(\boldsymbol{x})/T}$ — overwhelmingly concentrated near low energies, unreachable by uniform sampling.

## The Metropolis algorithm

Metropolis, Rosenbluth, Rosenbluth, Teller and Teller（*J. Chem. Phys.* **21**, 1087, 1953）showed how to generate exactly that distribution without ever normalizing it. From the current configuration $\boldsymbol{x}$, propose a small random change $\boldsymbol{x}'$ and compute $\Delta E=E(\boldsymbol{x}')-E(\boldsymbol{x})$; then

$$
\text{accept }\boldsymbol{x}'\text{ with probability }
\;\min\!\bigl\{1,\;e^{-\Delta E/T}\bigr\}
$$ (eq-u5-metropolis)

— downhill moves always, uphill moves sometimes, exponentially penalized by their cost. Why this works（detailed-balance intuition, one paragraph）: in the long run, the rate of hopping $\boldsymbol{x}\to\boldsymbol{x}'$ balances the reverse rate $\boldsymbol{x}'\to\boldsymbol{x}$ precisely when the occupation probabilities are Boltzmann — the acceptance rule {eq}`eq-u5-metropolis` is engineered so that the ratio of forward and reverse acceptances equals $e^{-\Delta E/T}$, which forces the chain's stationary distribution to be the Boltzmann distribution. Chains of such moves — **Markov chain Monte Carlo**（MCMC）— are how statistical physics, Bayesian statistics, and half of computational science explore spaces too vast to enumerate.

For optimization, read {eq}`eq-u5-metropolis` as a knob. At $T\to\infty$ every move is accepted: pure random walk, sees everything, prefers nothing. At $T\to0$ only downhill survives: pure greedy descent, efficient and trapped. At intermediate $T$ the walker *equilibrates across valleys*, spending most time in deep ones yet still hopping barriers of height $\sim T$. The suspicion that one should *start hot and finish cold* is exactly simulated annealing — [sec 3](sec3.md) — but first we meet the other family that turns randomness into search: populations（[sec 2](sec2.md)）.

One sentence of humility to carry through the unit: the **no-free-lunch theorems** say that averaged over all possible objective functions, every search strategy performs identically — a heuristic only wins by matching the *structure* of your problem class, never universally.
