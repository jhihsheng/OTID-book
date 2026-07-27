# FDTD with Meep

進入電磁模擬：**Meep（FDTD）**是本課反向設計實作的正向求解器（forward solver）。先學基本操作（來源、邊界、flux 監測），再做第一個 forward-design 實驗——在波導彎折加 ring resonator，觀察穿透率變化（正向設計的手感，對應 [U6](../unit06/index.md) 的 forward vs inverse 概念）。

- [Notebook 05：Basic Usages of Meep](../computing_lab/05_OTID_meep_tutorial_1.ipynb)
- [Notebook 06：Meep Lab 1——waveguide bend ＋ ring resonator](../computing_lab/06_OTID_meep_lab_1.ipynb)

**輔助檔**：[`meep_plot_style.py`](../computing_lab/meep_plot_style.py)、[`mycmapls.py`](../computing_lab/mycmapls.py)（課程統一繪圖風格）。

**先備需求**：[env 模組](env.md)＋Meep 環境（見[環境安裝](../setup.md)）。

```{warning}
**Meep 系列 notebooks（05–09）沒有 Colab 連結**——Meep 只能經 conda-forge 安裝，Colab 上裝不了。請用本機 conda 環境或課程伺服器。
```

**交付**：notebook 06 的實驗結果（ring 參數 vs 穿透頻譜）。
