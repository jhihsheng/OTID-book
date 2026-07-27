# Mini-Project I: Multilayer Filters（TMM）

第一個 mini-project：**多層膜濾波器**。用 **Transfer Matrix Method（TMM）** 計算 10 層 ABAB 疊層的穿透頻譜（線性代數的實戰——對應 [U1](../unit01/index.md)），再把層厚當設計變數、用最佳化方法（[U3](../unit03/index.md)）逼近目標頻譜——課程「濾波器反向設計」應用主線的第一步。

- [Notebook 04：Transmittance Calculation for Multilayer Structure](../computing_lab/04_OTID_transmission_TMM.ipynb)
  ｜[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jhihsheng/OTID/blob/main/computing_lab/04_OTID_transmission_TMM.ipynb)

**下載**：[`04_OTID_trans_TMM_zoa.py`](../computing_lab/04_OTID_trans_TMM_zoa.py)（TMM 計算腳本）。

**先備需求**：[opti 模組](opti.md)。

**交付**：mini-project 報告——TMM 正向模型驗證＋一個濾波器設計結果（目標頻譜、最佳化過程、最終結構）。

```{seealso}
同一個濾波器問題的 adjoint／拓撲最佳化解法見 [adjoint 模組](adjoint.md)（影片 `filter_id.mp4`）。
```
