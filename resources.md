# 教科書與資源 Textbooks & Resources

## 教科書 Textbooks

1. **Edwin K. P. Chong and Stanislaw H. Zak, *An Introduction to Optimization*, 3rd ed., Wiley-Interscience, 2008.** —— 主課本。閱讀範圍 Ch. 1–15（跳過 Ch. 12；Ch. 15 簡要帶過）。NYCU 圖書館有電子書。作者課程網站（含講義與習題資源）：<https://www.engr.colostate.edu/~echong/ece520/>。
2. **Aarts, Emile and Korst, Jan, *Simulated Annealing and Boltzmann Machines: A Stochastic Approach to Combinatorial Optimization and Neural Computing*, Chichester / John Wiley & Sons, 1989.** —— 模擬退火經典專書（U5 參考）。
3. **Mykel J. Kochenderfer and Tim A. Wheeler, *Algorithms for Optimization*, MIT Press, 2019.** —— 現代演算法視角，population-based 方法（GA/PSO/DE）的好參考。

## 反向設計閱讀清單 Inverse-Design Reading List

**最新的發展通常沒有教科書！**需要自己整理脈絡：論文、講義、線上資源——這是高手必經之路（well-known 的知識代表落後）。

- **Molesky, Lin, Piggott, Jin, Vucković & Rodriguez, "Inverse design in nanophotonics," *Nature Photonics* 12, 659–670 (2018).** —— 本領域的定調綜述：為什麼光子學反向設計成熟得早、adjoint 為何是核心引擎。U6 的主要參考。
- **S. G. Johnson, "Notes on adjoint methods," MIT 18.336.** <https://math.mit.edu/~stevenj/18.336/adjoint.pdf> —— adjoint 方法最乾淨的推導（chain rule 與 Lagrangian 兩條路），U7 sec1 直接對應。
- **Hammond, Oskooi, Chen, Lin, Johnson & Ralph, "High-performance hybrid time/frequency-domain topology optimization for large-scale photonics inverse design," *Opt. Express* 30, 4467–4491 (2022).** —— Meep adjoint solver 的現代參考實作；labs/adjoint 兩本 notebooks 的理論後盾。
- **"Deep learning for inverse design" review, *Photonics Research* 9(5), B182–B200 (2021).** —— ML 路線（surrogate、tandem、generative）的入口綜述。
- **PhD theses**：Jan Petykiewicz (Stanford), *Active nanophotonics*；Logan W. Su (Stanford), *Computational nanophotonic design* (2020). —— 想看完整 pipeline 細節（從 FoM 到 fabrication constraints）就讀學位論文。
- **應用範例**：*Phys. Rev. Lett.* 122, 213902 (2019)；*IEEE Trans. Antennas Propag.* 70(4), 2841–2854 (2022). —— 反向設計輸出「非直覺結構」而效能勝過人工設計的代表作。

## 軟體 Software

- **MEEP**（FDTD）：<https://meep.readthedocs.io> —— 本課實作主力；含 [Adjoint Solver tutorial](https://meep.readthedocs.io/en/latest/Python_Tutorials/Adjoint_Solver/)。
- **spins-b**：<https://github.com/stanfordnqp/spins-b> —— Stanford 反向設計框架。
- **angler**：<https://github.com/fancompute/angler> —— FDFD 反向設計。
- **scipy.optimize / NLopt**：通用最佳化程式庫（labs/opti 使用；NLopt 亦為 Meep adjoint 常用外層）。
- **D-Wave Ocean SDK**：<https://docs.ocean.dwavesys.com> —— 量子退火（labs/qa 使用）。

## 如何找論文 How to Find Papers

1. **關鍵字**下手 → Google Scholar／Web of Science。
2. **判斷期刊**：影響係數（IF）、老字號期刊、專家推薦。
3. **判斷文章**：先讀摘要 → 介紹 → 結論，最後才讀方法。
