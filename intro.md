---
exports:
  - format: typst
    template: plain_typst_book
    output: exports/otid_book.pdf
    id: otid-book
    articles:
      - intro.md
      - syllabus.md
      - unit01/index.md
      - unit01/sec1.md
      - unit01/sec2.md
      - unit01/sec3.md
      - unit02/index.md
      - unit02/sec1.md
      - unit02/sec2.md
      - unit02/sec3.md
      - unit03/index.md
      - unit03/sec1.md
      - unit03/sec2.md
      - unit03/sec3.md
      - unit03/sec4.md
      - unit04/index.md
      - unit04/sec1.md
      - unit04/sec2.md
      - unit04/sec3.md
      - unit05/index.md
      - unit05/sec1.md
      - unit05/sec2.md
      - unit05/sec3.md
      - unit05/sec4.md
      - unit06/index.md
      - unit06/sec1.md
      - unit06/sec2.md
      - unit06/sec3.md
      - unit07/index.md
      - unit07/sec1.md
      - unit07/sec2.md
      - unit07/sec3.md
      - unit08/index.md
      - unit08/sec1.md
      - unit08/sec2.md
      - unit08/sec3.md
downloads:
  - id: otid-book
    title: 整本課程書 PDF（Part I 理論篇）
---

# 最佳化理論與反向設計 Optimization Theory and Inverse Design

NYCU 光電碩選修（114-2，當期課號 535417，永久課號 EEEO30135）｜授課教師：吳致盛 Jhih-Sheng Wu

反向設計（inverse design）近年在量子、光學、電子元件領域受到重視，其核心即**最佳化理論**——古典與量子、梯度法與非梯度法。本課程重理論與實戰並行：目標是紮實的理論基礎、上手的 coding skills、以及追上研究前沿的能力。

**三大主軸**：Optimization Theory（最佳化理論）／Inverse Design（反向設計）／Hands-on（coding、mini-projects、口頭報告）。

**三個目標**：

1. 掌握常見最佳化方法與其性質（common methods and their properties）；
2. 在光學問題上取得實作經驗（hands-on experience in optics）；
3. 學會抓研究趨勢（catch the research trends）。

## Part I — 理論單元總覽

理論篇採**單元制**，不綁週次——進度以上課宣布為準（滾動式調整）；正式每週進度表見[課程綱要](syllabus.md)。

| 單元 | 主題 | C&Z 章節 | 頁面 |
|----|--------------------------------------------|--------|--------|
| U1 | Mathematical preliminaries 數學複習 | 1–5 | [unit01](unit01/index.md) |
| U2 | Optimization basics & one-dimensional search | 6–7 | [unit02](unit02/index.md) |
| U3 | Gradient, Newton, CG & quasi-Newton（＋LP 簡介） | 8–11, 15 | [unit03](unit03/index.md) |
| U4 | Neural networks & optimization for deep learning | 13 | [unit04](unit04/index.md) |
| U5 | Heuristics: Monte Carlo, GA/PSO/DE, simulated & quantum annealing | 14 | [unit05](unit05/index.md) |
| U6 | Inverse design: concepts and landscape | — | [unit06](unit06/index.md) |
| U7 | Adjoint method & density-based topology optimization | — | [unit07](unit07/index.md) |
| U8 | Automatic differentiation & modern numerical computing | — | [unit08](unit08/index.md) |

## Part II — 實作模組總覽

實作篇整合 [`jhihsheng/OTID`](https://github.com/jhihsheng/OTID) 的 notebooks，依模組編排（總覽見 [labs](labs/index.md)）：

| 模組 | 內容 | 對應理論單元 |
|------|------|------|
| [env](labs/env.md) | 環境建置：VPN/SSH、conda、JupyterLab | — |
| [python](labs/python.md) | matplotlib 科學繪圖 | — |
| [opti](labs/opti.md) | scipy 最佳化＋metaheuristics 實作 | U2, U3, U5 |
| [tmm](labs/tmm.md) | Mini-project I：多層膜濾波器（TMM） | U1, U3 |
| [meep](labs/meep.md) | FDTD with Meep 入門與實驗 | U6 |
| [eot](labs/eot.md) | Mini-project II：EOT 電漿子晶格 | U6 |
| [adjoint](labs/adjoint.md) | Adjoint 反向設計實作（含多頻） | U7, U8 |
| [qa](labs/qa.md) | QA mini-project：量子退火與 binary OPA | U5 |

## 關鍵日期

- **2026-02-23**（一）開學
- **2026-04-20**（一）期中考（Week 9）
- **2026-06-08**（一）期末專題報告

官方每週進度見[課程綱要](syllabus.md)；實際進度以上課宣布為準。

## 評量

平時作業 40%｜期中考 30%｜Mini-Projects 15%｜期末報告 Presentation 15%（＋課堂參與 bonus）。
註明：官方課綱之「期末專題 30%」＝ Mini-Projects 15% ＋ Presentation 15%。

學到的能力才是重點！作業與考試以簡單與基礎為原則。期末專題規則見[期末專題與報告](project.md)；期中題庫公布於[題庫頁](question_bank.md)。

## 聯絡與晤談

- 上課：週一 5–7 節（M567），光復校區 EO115。
- Office hour：週一 10:00–12:00，EO413（田家炳大樓）；其他時間請 email 預約。
- Email：<jwu@nycu.edu.tw>
