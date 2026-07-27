# 環境安裝 Environment Setup

本課需要 **Python ＋ Linux ＋ 自備筆電**。以下是建議安裝順序；連線到課程伺服器的完整步驟見 [SSH 連線指引](computing_lab/00_connection_ssh.md)，第一次實作課的完整流程見 [Lab 0](computing_lab/00_OTID_lab1.ipynb)。

## 1. Linux 環境

- **Windows** 使用者：請在家先裝好 **WSL**（Windows Subsystem for Linux，建議 Ubuntu）。
- **macOS / Linux** 使用者：內建終端機即可。

## 2. Anaconda ＋ JupyterLab

安裝 [Anaconda](https://www.anaconda.com/download)（或 Miniconda），然後：

```bash
conda create -n otid python=3.11
conda activate otid
conda install jupyterlab numpy scipy matplotlib
```

## 3. MEEP（FDTD）

Meep 走 **conda-forge**（不支援 pip／Colab）：

```bash
conda create -n mp -c conda-forge pymeep pymeep-extras
conda activate mp
```

詳見 [Meep 官方安裝文件](https://meep.readthedocs.io/en/latest/Installation/)。裝不起來就先用課程伺服器（見連線指引）。

## 4. D-Wave Ocean（量子退火實作用）

QA labs 使用專屬 conda 環境檔 [`dwave_env.yml`](computing_lab/QA_lab_mini_project/dwave_env.yml)：

```bash
conda env create -f dwave_env.yml
```

要跑真的 QPU 需要 [D-Wave Leap](https://cloud.dwavesys.com/leap/) 帳號與 API token（免費額度即可）。

## 5. Julia（選配）

對高效能數值計算有興趣者可另裝 [Julia](https://julialang.org/)；非必要。

```{tip}
純 Python 的 notebooks（繪圖、scipy、TMM、QA）可以直接用 Google Colab 免安裝執行——各實作模組頁附有 Colab 連結；Meep 系列（FDTD、adjoint）為 conda-only，請用本機或課程伺服器。
```
