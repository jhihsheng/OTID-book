# Inverse Design: Concepts and Landscape

**Unit 6**｜Reading: Molesky et al., *Nature Photonics* **12**, 659–670 (2018)＋課程閱讀清單（見[資源頁](../resources.md)）｜進度以上課宣布為準

```{note} Learning objectives (Unit 6)
1. Distinguish the forward and inverse problems, and explain why the inverse map is ill-posed（non-unique, possibly infeasible）and how optimization resolves the ill-posedness.
2. Define design space, figure of merit, and constraints for a given design task, and state what makes a figure of merit *good*.
3. Classify a device parameterization as shape-based, level-set, or density-based, and predict which optimization family（gradient/adjoint vs heuristic）it calls for.
4. Describe the closed inverse-design loop and the main method families — adjoint-based topology optimization, heuristic pipelines, and ML-assisted approaches — with one exemplar each.
```

**Reading.** This unit has no textbook — the field is younger than the course's books, which is itself a lesson（最新的發展通常沒有教科書！）. The framing survey is Molesky, Lin, Piggott, Jin, Vucković & Rodriguez,「Inverse design in nanophotonics,」*Nature Photonics* **12**, 659–670 (2018); the remaining references live on the [course reading list](../resources.md).

**Opening puzzle.** Watch `bend_waveguide.mp4` on the [adjoint lab page](../labs/adjoint.md): a silicon waveguide bend that outperforms the textbook design, shaped like nothing in any textbook — an irregular archipelago of blobs no engineer would draw. Nobody did draw it. The only human input was a sentence:「maximize transmission from this port to that one」— the *structure* was produced by an optimizer conversing with Maxwell's equations. This inverts the workflow you were trained in: analysis starts from a structure you guessed and computes its performance; design-by-optimization starts from the performance and computes the structure. But there is a puzzle in that inversion: Maxwell's equations map each structure to *one* response — a function — while the reverse assignment is one-to-many where it exists at all（[](#fig-u6-fwdinv) in sec 1）. How do you compute with a map that is not a function? The answer that built a field: don't invert — *optimize*. This unit is the conceptual map; Unit 7 supplies the engine.
