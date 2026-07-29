# Quantum Annealing

## The Ising language

Quantum annealers speak one language. The **Ising Hamiltonian** assigns an energy to $N$ spins $s_i\in\{-1,+1\}$:

$$
E(\boldsymbol{s})=\sum_i h_i\,s_i+\sum_{i<j}J_{ij}\,s_i s_j ,
$$ (eq-u5-ising)

with local fields $h_i$ and couplings $J_{ij}$. Its binary twin is the **QUBO**（quadratic unconstrained binary optimization）over $x_i\in\{0,1\}$: minimize $\sum_{i\le j}Q_{ij}x_ix_j$（diagonal terms are linear, since $x_i^2=x_i$）. The two forms are *exactly* interchangeable through $s_i=2x_i-1$: substituting and collecting terms maps any Ising instance to a QUBO and back, changing only an additive constant（Exercise 4 does one by hand）. Formulating your problem in this language is the entrance fee to the hardware — and often the most creative step.

**The course's own example（the [QA mini-project](../labs/qa.md)）.** A binary optical phased array: $N$ emitters, each phase restricted to $0$ or $\pi$, i.e. amplitude $s_n=\pm1$. The far-field amplitude toward angle $\theta$ is $\sum_n s_n e^{\,\mathrm{i}n\varphi}$ with phase increment $\varphi=kd\sin\theta$, so the intensity at the target angle is

$$
I(\theta_0)=\Bigl|\sum_n s_n e^{\,\mathrm{i}n\varphi_0}\Bigr|^2
=N+\sum_{n\neq m}\cos\bigl((n-m)\varphi_0\bigr)\,s_n s_m .
$$

Maximizing beam power at $\theta_0$ *is* minimizing an Ising energy {eq}`eq-u5-ising` with $J_{nm}=-2\cos((n-m)\varphi_0)$ and $h_n=0$ — the design problem native to the machine, no encoding tricks required.

## Adiabatic computation

A quantum annealer solves Ising problems by physics instead of iteration（Kadowaki & Nishimori, *Phys. Rev. E* **58**, 5355, 1998）. Implement the time-dependent Hamiltonian

$$
H(t)=A(t)\sum_i\sigma^x_i\;+\;B(t)\,H_{\text{problem}},
$$ (eq-u5-anneal)

where $H_{\text{problem}}$ is {eq}`eq-u5-ising` promoted to operators（$s_i\to\sigma^z_i$）and $\sum_i\sigma^x_i$ is the **transverse-field driver**, whose ground state — every spin along $x$, i.e. a uniform superposition of all $2^N$ configurations — is trivial to prepare. Start with $A$ dominant, end with $B$ dominant（[](#fig-u5-schedule)）. The **adiabatic theorem**（statement）: if the sweep is slow compared to the inverse square of the minimum energy gap between ground and first excited state, the system remains in its instantaneous ground state throughout — and the final state *is* the answer. The catch is in that gap: on hard instances it can close exponentially fast with $N$, demanding exponentially slow sweeps. Quantum annealing relocates the difficulty; it does not abolish it.

```{figure} ../assets/u05_schedule.png
:name: fig-u5-schedule
:width: 80%

Schematic annealing schedule for {eq}`eq-u5-anneal`. While $A$ dominates, quantum fluctuations（tunneling）keep the state delocalized; as $B$ takes over, the problem's landscape crystallizes and the state must settle — slowly enough, per the adiabatic theorem, to settle into the ground state.
```

The physical intuition that distinguishes QA from SA is the escape mechanism（sec 3's [](#fig-u5-landscape)）: thermal hopping pays $e^{-\Delta E/T}$ for barrier *height*; quantum tunneling instead penalizes barrier *width*. Landscapes with tall, thin barriers are where quantum annealing has the clearest mechanistic advantage — Kadowaki & Nishimori's original simulations showed exactly this regime.

## D-Wave practicalities

Real hardware（the D-Wave machines of the mini-project）adds engineering to the physics:

- **Connectivity and minor embedding.** Physical qubits couple only to graph neighbors（Pegasus/Zephyr topologies）. A problem whose $J_{ij}$ links non-neighbors must be *embedded*: one logical variable becomes a **chain** of physical qubits bound by a strong ferromagnetic coupling. Dense problems burn qubits fast — an all-to-all OPA problem of modest size can exhaust a machine of thousands of qubits.
- **Chain strength.** The chain coupling is a hyperparameter: too weak and chains *break*（qubits in one chain disagree — the sample is not even a valid assignment）; too strong and it drowns the problem's own energy scale, since $h,J$ have limited analog precision. Tune it, and monitor the chain-break fraction.
- **Annealing time and sampling.** One anneal takes microseconds and returns *one sample* — from a device that is partly thermal, partly quantum, wholly noisy. Practice: run thousands of anneals, keep the best sample, study the distribution. The output is a statistical object, not a certificate.

## QA versus SA, soberly

The honest scorecard, which the [mini-project](../labs/qa.md) asks you to fill in yourself for the OPA problem: quantum annealing offers a *different escape mechanism*（tunneling）with demonstrated advantages on engineered landscapes, microsecond-scale sampling, and steady hardware progress. Against that: embedding overhead, analog noise and precision limits, restricted connectivity — and the stubborn empirical fact that **no established general speedup over well-tuned classical methods exists to date**; a competently tuned SA（or DE, or a specialized classical solver）remains the benchmark to beat, and often does the beating. The scientifically defensible posture is the experimentalist's: formulate the QUBO, run both, measure. That is precisely what the course asks of you.

## Exercises

以簡單與基礎為原則。

**Exercise 1（max-cut as QUBO）.** For the 4-cycle graph with edges $(1,2),(2,3),(3,4),(4,1)$, write the max-cut problem（partition the vertices to cut as many edges as possible）as a QUBO in $x_i\in\{0,1\}$, and verify that $\boldsymbol{x}=(1,0,1,0)$ attains the optimum.

```{dropdown} Solution
An edge $(i,j)$ is cut iff $x_i\neq x_j$, i.e. its cut indicator is $x_i+x_j-2x_ix_j$. Maximizing the total cut is minimizing its negative:
$\min\;\sum_{(i,j)\in E}\bigl(2x_ix_j-x_i-x_j\bigr)$ — here
$2(x_1x_2+x_2x_3+x_3x_4+x_4x_1)-2(x_1+x_2+x_3+x_4)$（each vertex has degree 2）.
At $\boldsymbol{x}=(1,0,1,0)$: products all zero, sum $=0-2\cdot2=-4$ — one $-1$ per edge, so all four edges cut, the maximum possible. ✓
```

**Exercise 2（Metropolis arithmetic）.** A walker at energy $E=2.0$ proposes a move to $E'=2.7$, and the uniform draw is $u=0.35$. Is the move accepted at $T=1.0$? At $T=0.1$?

```{dropdown} Solution
$\Delta E=0.7$. At $T=1.0$: acceptance probability $e^{-0.7}\approx0.497$; since $u=0.35<0.497$, **accept**. At $T=0.1$: $e^{-7}\approx9\times10^{-4}$; $u=0.35$ far exceeds it — **reject**. The same uphill move is routine when hot and essentially forbidden when cold: that is the entire annealing dial.
```

**Exercise 3（one PSO step and one DE step by hand）.**
（a）PSO in 1-D with $w=0.5$, $c_1=c_2=1.5$: particle at $x=2$ with $v=1$, personal best $p=1$, global best $g=0$, draws $r_1=0.4$, $r_2=0.6$. Update $v$ and $x$ via {eq}`eq-u5-pso`.
（b）DE/rand/1 in 2-D with $F=0.8$: $\boldsymbol{x}_{r_1}=(1,2)$, $\boldsymbol{x}_{r_2}=(3,1)$, $\boldsymbol{x}_{r_3}=(2,0)$. Form the mutant {eq}`eq-u5-de`; then cross with target $\boldsymbol{x}_i=(0,1)$ using $CR=0.5$, coordinate draws $(0.3,\,0.7)$, forced coordinate $j_{\text{rand}}=1$.

```{dropdown} Solution
（a）$v\leftarrow0.5\cdot1+1.5\cdot0.4\,(1-2)+1.5\cdot0.6\,(0-2)=0.5-0.6-1.8=-1.9$; $x\leftarrow2+(-1.9)=0.1$. The social pull toward $g=0$ dominates and overshoots slightly — typical PSO dynamics.
（b）Mutant: $\boldsymbol{v}=(1,2)+0.8\,\bigl[(3,1)-(2,0)\bigr]=(1,2)+(0.8,0.8)=(1.8,\,2.8)$. Crossover: coordinate 1 has $0.3\le CR$（and is $j_{\text{rand}}$ anyway）→ take mutant $1.8$; coordinate 2 has $0.7>CR$ → keep target $1$. Trial $\boldsymbol{u}=(1.8,\,1)$; greedy selection then keeps $\boldsymbol{u}$ or $\boldsymbol{x}_i$, whichever has lower $f$.
```

**Exercise 4（Ising ↔ QUBO）.** Convert the two-spin Ising instance $E(\boldsymbol{s})=s_1-s_2+2s_1s_2$ to QUBO form via $s_i=2x_i-1$, and check one configuration in both languages.

```{dropdown} Solution
Substitute: $(2x_1-1)-(2x_2-1)+2(2x_1-1)(2x_2-1)=2x_1-2x_2+\bigl(8x_1x_2-4x_1-4x_2+2\bigr)$
$=8x_1x_2-2x_1-6x_2+2$. So the QUBO is $\min\;8x_1x_2-2x_1-6x_2$（constant $+2$ dropped）. Check $\boldsymbol{s}=(-1,+1)\Leftrightarrow\boldsymbol{x}=(0,1)$: Ising $-1-1-2=-4$; QUBO $0-0-6+2=-4$. ✓（This is also the ground state — verify the other three configurations if unconvinced.）
```

```{seealso}
[labs/qa](../labs/qa.md): the 3-hour quantum-annealing lab（QUBO drills, embedding, real QPU runs）and the binary-OPA mini-project — sec 4 run on real hardware. The classical half of the comparison uses the SA of sec 3.
```
