# Optimization in Practice: scipy and Metaheuristics

理論單元的方法在這裡動手跑：先用 **scipy.optimize** 操作梯度法家族（對應 [U2](../unit02/index.md)、[U3](../unit03/index.md)），再實作 **metaheuristics**——模擬退火與 particle swarm（對應 [U5](../unit05/index.md)；notebook 03 實作 **PSO**，是 [U5 sec2](../unit05/sec2.md) 的直接姊妹篇）。

- [Notebook 02：Optimization Using scipy](../computing_lab/02_OTID_opti_tutorial_1.ipynb)
  ｜[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jhihsheng/OTID/blob/main/computing_lab/02_OTID_opti_tutorial_1.ipynb)
- [Notebook 03：Metaheuristic Algorithms](../computing_lab/03_OTID_opti_tutorial_2.ipynb)
  ｜[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jhihsheng/OTID/blob/main/computing_lab/03_OTID_opti_tutorial_2.ipynb)

**先備需求**：[python 模組](python.md)；U2–U3 讀過更好。

**交付**：兩本 notebooks 的練習題；能對同一個測試函數比較梯度法與 metaheuristic 的行為。

```{seealso}
[NLopt](https://nlopt.readthedocs.io/) 收錄大量現成演算法——之後 adjoint 模組的外層 optimizer 也是它。
```
