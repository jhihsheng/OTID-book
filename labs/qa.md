# Quantum-Annealing Mini-Project

課程「1D 光柵設計——退火路線」的實作：把設計問題寫成 **QUBO／Ising 形式**（理論見 [U5 sec4](../unit05/sec4.md)），先用模擬退火解，再送上 **D-Wave 量子退火機**比較。mini-project 題目：**binary-phase optical phased array（OPA）**——矽光子束控的二元相位設計。

- [量子退火實作課程（3 小時完整版）](../computing_lab/QA_lab_mini_project/quantum_annealing_lab_FULL.ipynb)：QUBO 入門與練習、倉儲最佳化、Pegasus/Zephyr QPU 架構、embedding 與 QPU 實跑
  ｜[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jhihsheng/OTID/blob/main/computing_lab/QA_lab_mini_project/quantum_annealing_lab_FULL.ipynb)
- [Binary OPA：SA vs QA](../computing_lab/QA_lab_mini_project/binary_OPA_SA_QA.ipynb)
  ｜[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jhihsheng/OTID/blob/main/computing_lab/QA_lab_mini_project/binary_OPA_SA_QA.ipynb)

**環境**：Colab 可跑（Ocean SDK 以 pip 安裝）；本機用 conda 環境檔 [`dwave_env.yml`](../computing_lab/QA_lab_mini_project/dwave_env.yml)。**上真的 QPU 需要 D-Wave Leap 帳號與 API token**（免費額度即可，見[環境安裝](../setup.md)）。

**先備需求**：[opti 模組](opti.md)（模擬退火）；建議先讀 [U5](../unit05/index.md) sec3–sec4。

**交付**：OPA mini-project 結果——QUBO 建模、SA 與 QA 解的比較（beam pattern、能量分布、成功率）。
