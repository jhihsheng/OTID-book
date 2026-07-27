# Hands-On Labs and Mini-Projects 實作總覽

Part II 收錄 [`jhihsheng/OTID`](https://github.com/jhihsheng/OTID) 的全部實作教材（notebooks 原檔渲染；可執行檔請從該 repo 取得或用各頁 Colab 連結）。

官方課綱的 **Applications** 由兩條應用主線構成：

1. **濾波器反向設計——梯度／adjoint 路線**：[tmm](tmm.md)（TMM 正向模型）→ [meep](meep.md)（FDTD）→ [adjoint](adjoint.md)（adjoint 梯度＋拓撲最佳化）。
2. **1D 光柵設計——退火路線**：[opti](opti.md)（metaheuristics）→ [qa](qa.md)（模擬退火 vs 量子退火、binary OPA）。

加上 **Projects（最佳化方法實作）**：兩個 mini-projects（[tmm](tmm.md)、[eot](eot.md)）與期末專題（規則見[期末專題與報告](../project.md)）。

## 模組 ↔ 理論單元對照

| 模組 | 內容 | 對應理論單元 |
|------|------|------|
| [env](env.md) | 環境建置：VPN/SSH、conda、JupyterLab | — |
| [python](python.md) | matplotlib 科學繪圖 | — |
| [opti](opti.md) | scipy 最佳化＋metaheuristics 實作 | U2, U3, U5 |
| [tmm](tmm.md) | Mini-project I：多層膜濾波器（TMM） | U1, U3 |
| [meep](meep.md) | FDTD with Meep 入門與實驗 | U6 |
| [eot](eot.md) | Mini-project II：EOT 電漿子晶格 | U6 |
| [adjoint](adjoint.md) | Adjoint 反向設計實作（含多頻） | U7, U8 |
| [qa](qa.md) | QA mini-project：量子退火與 binary OPA | U5 |

```{tip}
純 Python 模組（python、opti、tmm、qa）附 **Colab 連結**可免安裝執行；Meep 系列（meep、eot、adjoint）為 conda-only，請用本機環境或課程伺服器（見[環境安裝](../setup.md)）。
```
