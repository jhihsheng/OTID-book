# Heuristic Methods: Monte Carlo, Population-Based Algorithms, SA and QA

**Unit 5**｜Reading: C&Z Ch. 14 + supplements（Aarts & Korst 1989；Kochenderfer & Wheeler 2019）｜進度以上課宣布為準

```{note} Learning objectives (Unit 5)
1. Explain why gradient-based methods fail on discrete or rugged landscapes, and state the Metropolis acceptance rule and what distribution it samples.
2. Execute one iteration of GA, PSO, and DE by hand, and choose among them（and simulated annealing）for a given problem using their mechanisms and hyperparameters.
3. Write down the simulated-annealing algorithm — Metropolis plus a cooling schedule — and set its initial temperature and stopping rule from acceptance statistics.
4. Convert between Ising and QUBO forms, formulate a design problem（the binary optical phased array）as a QUBO, and describe how a quantum annealer attempts to solve it, including its practical limitations.
```

**Reading.** C&Z Ch. 14（global search algorithms）; Aarts & Korst, *Simulated Annealing and Boltzmann Machines*（1989）for the SA theory; Kochenderfer & Wheeler, *Algorithms for Optimization*（2019）for the modern population-methods view. Primary sources cited in place: Metropolis et al.（1953）, Kirkpatrick et al.（1983）, Kennedy & Eberhart（1995）, Storn & Price（1997）, Kadowaki & Nishimori（1998）.

**Opening puzzle.** Design a beam-steering array of $64$ phase shifters, each restricted to $0$ or $\pi$ — the [QA mini-project](../labs/qa.md). The design space has $2^{64}\approx1.8\times10^{19}$ configurations: brute force at a billion per second needs six centuries, and *no gradient exists* — the variables are bits, and「move a little downhill」is meaningless. Greedy bit-flipping gets trapped in the nearest local optimum within milliseconds. The escape, discovered in 1953 for simulating matter and repurposed in 1983 for optimization, sounds like a bug report:**deliberately accept moves that make the design worse**, with a probability tuned by a fictitious temperature. Why making the algorithm locally worse makes it globally better — and how far that idea stretches, all the way to hardware that tunnels through barriers instead of hopping over them — is this unit.
