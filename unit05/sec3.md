# Simulated Annealing

## The metallurgical metaphor, taken literally

To remove defects from a metal, you do not hammer it at room temperature; you **anneal** it — heat until atoms hop freely, then cool *slowly* so the lattice settles into a low-energy crystal. Quench it too fast and defects freeze in: a glass, a local minimum of the atomic arrangement. Kirkpatrick, Gelatt and Vecchi（*Science* **220**, 671, 1983）read this as an algorithm: an objective function is an energy landscape, and the Metropolis walker of sec 1, cooled slowly, is a general-purpose global optimizer. **Simulated annealing = Metropolis {eq}`eq-u5-metropolis` + a cooling schedule.**

## The algorithm

```python
def simulated_annealing(E, x0, propose, T0, alpha, n_steps, rng):
    x, Ex = x0, E(x0)
    best, Ebest = x, Ex
    T = T0
    for k in range(n_steps):
        y  = propose(x, rng)              # small random move
        Ey = E(y)
        if Ey < Ex or rng.random() < exp(-(Ey - Ex) / T):
            x, Ex = y, Ey                 # Metropolis accept
            if Ex < Ebest:
                best, Ebest = x, Ex
        T = alpha * T                     # geometric cooling, alpha ~ 0.95-0.999
    return best, Ebest
```

Early（$T$ large）: the walker roams almost freely, surveying the landscape's gross geography. Late（$T\to0$）: it hardens into greedy descent inside whichever basin it occupies. In between, at each temperature it can cross barriers up to height $\sim T$ — the annealing *sequence* matters because each temperature equilibrates the walker across structures of the corresponding energy scale, coarse to fine.

## What theory promises vs what practice does

The honest statement of the theory（Aarts & Korst, 1989, where the Markov-chain analysis lives）: with cooling **slow enough** — logarithmically slow, $T_k\sim c/\log k$ with $c$ tied to the largest barrier — simulated annealing converges to the global optimum with probability one. The catch: logarithmic cooling from $T_0$ down through four orders of magnitude takes $e^{10^4}$-ish steps — the guarantee is real and useless. Practice universally runs **geometric cooling** $T_{k+1}=\alpha T_k$, surrendering the guarantee for a schedule that finishes this year and, on problems with reasonable structure, lands in excellent（not certified-optimal）basins. Know which trade you are making.

```{warning}
The classic SA failure is a *quench in disguise*: $T_0$ too low or $\alpha$ too aggressive, and your expensive「annealer」is a greedy descender with noise — it inherits SA's cost and greedy descent's traps. The symptom is an acceptance ratio that collapses within the first few percent of the run. Log the acceptance ratio; it is the algorithm's thermometer.
```

## Setting the knobs

- **Initial temperature $T_0$**: choose it *from data*, not folklore — sample some random moves, then set $T_0$ so the initial acceptance ratio is high（say $\approx0.8$）: $T_0\approx\overline{\Delta E}_{+}/\ln(1/0.8)\approx4.5\,\overline{\Delta E}_{+}$, where $\overline{\Delta E}_{+}$ is the mean uphill move size.
- **Cooling rate $\alpha$**: as slow as the budget allows; $0.95$–$0.999$ typical. Better budgets buy slower cooling, not more restarts, up to the point of diminishing returns.
- **Proposal size**: tune so mid-run acceptance hovers near $0.4$–$0.6$ — too-large proposals are always rejected（wasted evaluations）, too-small ones explore nothing.
- **Stopping**: freeze detection — stop when the best-so-far has not improved for several temperature stages, or when acceptance falls below a floor（$\sim10^{-3}$）.

For discrete problems — bit flips on the binary OPA, swaps on a tour — SA is often the *first* serious method to try: proposals are natural（flip a bit）, no encoding gymnastics, one walker, four knobs. That simplicity, plus the physics costume, made SA the most-used metaheuristic of the last four decades and the classical benchmark that any「quantum」claim must beat — which is precisely how [sec 4](sec4.md) will frame quantum annealing, where the temperature knob is replaced by a tunneling knob（[](#fig-u5-landscape) previews the picture）.

```{figure} ../assets/u05_landscape.png
:name: fig-u5-landscape
:width: 88%

Two escape routes from a local minimum. Simulated annealing hops *over* the barrier with probability $\sim e^{-\Delta E/T}$ — tall barriers are exponentially expensive, whatever their width. Quantum annealing（sec 4）tunnels *through*; tunneling cares about barrier width more than height. Which mechanism wins depends on the landscape's barrier geometry.
```
