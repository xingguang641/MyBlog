---
title: 【机器学习基本模型】第七节：隐马尔可夫模型
published: 2025-10-30
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

> 写在前面：隐马尔可夫模型是机器学习基本模型中的第二个大难点，也是我们讲到的第一个概率图模型。

# 隐马尔可夫模型基本原理

隐马尔可夫模型（Hidden Markov Model，简称 HMM）是一种用于时序数据分析的 **概率图模型** 。它刻画了一个由隐藏状态组成的马尔可夫链，这个链在时间上生成一个不可直接观测的 **状态序列** ，并且每个状态都会根据一定的概率分布产生一个可观测的输出，从而形成 **观测序列** 。换句话说：HMM 描述了隐藏的状态在时间上按马尔可夫过程演化，而每个时刻的观测值则由对应的隐藏状态随机生成。其形式定义如下：

![隐马尔可夫模型1](src\content\posts\hidden-markov-model\隐马尔可夫模型1.jpg)

## 概念介绍

$Q$ 是所有可能的 **状态集合** ， $V$ 是所有可能的 **观测集合** ：

$$
Q = \{ q_1, q_2, \ldots, q_N \} \quad V = \{ v_1, v_2, \ldots, v_M \}
$$

其中 $N$ 是可能的状态数， $M$ 是可能的观测数。

$I$ 是长度为 $T$ 的 **状态序列** ， $O$ 是对应的 **观测序列** ：

$$
I = \{ i_1, i_2, \ldots, i_T \} \quad O = \{ o_1, o_2, \ldots, o_T \}
$$

$A$ 是 **状态转移概率矩阵** ：

$$
A = [a_{ij}]_{N \times N}
$$

$$
\text{where } a_{ij} = P(i_{t+1} = q_j|i_t = q_i) \quad i = 1, 2, \ldots, N \quad j = 1, 2,  \ldots, N
$$

表示在时刻 $t$ 处于状态 $q_i$ 的条件下在时刻 $t+1$ 转移到状态 $q_j$ 的概率。

$B$ 是 **观测概率矩阵** ：

$$
B = [a_{jk}]_{N \times M}
$$

$$
\text{where } b_{jk} = P(o_t = v_k|i_t = q_j) \quad j = 1, 2, \ldots, N \quad k = 1, 2,  \ldots, M
$$

表示在时刻 $t$ 处于状态 $q_j$ 的条件下生成观测 $v_k$ 的概率。

$\pi$ 是 **初始状态概率向量** ：

$$
\pi = (\pi_1, \pi_2, \ldots, \pi_N)
$$

$$
\text{where } \pi_i = P(i_1 = q_i) \quad i = 1, 2, \ldots, N
$$

表示时刻 $t = 1$ 时处于状态 $q_i$ 的概率。

隐马尔可夫模型由初始状态概率向量 $\pi$ 、状态转移概率矩阵 $A$ 和观测概率矩阵 $B$ 决定。 $\pi$ 和 $A$ 决定状态序列， $B$ 决定观测序列。因此，隐马尔可夫模型 $\lambda$ 可以用三元符号表示：

$$
\lambda = (A, B, \pi)
$$

从定义可知，隐马尔可夫模型作了两个 **基本假设** ：

- 齐次马尔可夫性假设，即假设隐藏的马尔可夫链在任意时刻 $t$ 的状态只依赖于其前一时刻的状态，与其他时刻的状态及观测无关，也与时刻 $t$ 无关：

$$
P(i_t|i_{t-1}, o_{t-1}, \ldots, i_1, o_1) = P(i_t|i_{t-1})
$$

- 观测独立性假设，即假设任意时刻的观测只依赖于该时刻的马尔可夫链的状态，与其他观测及状态无关：

$$
P(o_t|i_T, o_T, \ldots, i_t, i_{t-1}, o_{t-1} \ldots, i_1, o_1) = P(o_t|i_t)
$$

这两个假设都可以通过[上面](#隐马尔可夫模型基本原理)的概率图来理解（同时也是概率图的作用），每一个条 **有向边** 表示一个依赖关系，只有箭头尾部的状态会影响箭头头部的状态/观测。

# 隐马尔可夫模型实现难点

要想构建出 HMM，就必须解决以下三个问题：

- 计算问题：给定模型 $\lambda = (A, B, \pi)$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，计算在模型 $\lambda$ 下观测序列 $O$ 出现的概率 $P(O|\lambda)$

- 学习问题：已知观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，估计模型 $\lambda = (A, B, \pi)$ 参数，使得在该模型下观测序列概率 $P(O|\lambda)$ 最大，即用极大似然估计的方法估计参数

- 预测问题（也称解码问题）：已知模型 $\lambda = (A, B, \pi)$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，求对给定观测序列条件概率 $P(I|O)$ 最大的状态序列 $I = (i_1, i_2, \ldots, i_T)$ ，即给定观测序列，求最有可能的对应状态序列

下面就详细讲解一下这三个问题的解决方案。

## 计算问题

> 对于前/后向算法来说，只看下面的讲解理解起来可能会较为困难，请自行结合概率图状态转移的思路进行理解（最好画图），也可以辅助其他博客进行学习。值得注意的是，前/后向算法本质是一个动态规划算法，因此了解动态规划对理解前/后向算法有帮助。

[隐马尔可夫模型（HMM）三大基础问题之——评估问题](https://blog.csdn.net/qq_44648285/article/details/146015265)

[HMM 隐马尔可夫模型（概率计算算法）](https://zhuanlan.zhihu.com/p/144448849)

### 直接计算

对于求 $P(O|\lambda)$ 最直接的方法就是按照概率公式直接计算：

$$
P(O|\lambda) = \sum_{I} P(O, I|\lambda) = \sum_{I} P(O|I, \lambda)P(I|\lambda)
$$

$P(I|\lambda)$ 表示给定模型参数时，产生状态序列 $I = (i_1, i_2, \ldots, i_T)$ 的概率：

$$
P(I|\lambda) = \pi_{i_1} \prod_{t=1}^{T-1} a_{i_t i_{t+1}}
$$

$P(O|I, \lambda)$ 表示给定模型参数且产生状态序列 $I = (i_1, i_2, \ldots, i_T)$ 时，产生观测序列 $O = (o_1, o_2, \ldots, o_T)$ 的概率：

$$
P(O|I, \lambda) = \prod_{t=1}^{T} b_{i_to_t}
$$

综上可得：

$$
P(O|\lambda) = \sum_{I} P(O|I, \lambda)P(I|\lambda) = \sum_{i_1, i_2, \ldots, i_T} \pi_{i_1} \left( \prod_{t=1}^{T-1} b_{i_to_t}a_{i_ti_{t+1}} \right) b_{i_To_T}
$$

其中 $T$ 重循环的时间复杂度为 $O(N^T)$ ，每次循环又要花费 $O(T)$ 的时间计算 $T$ 重循环中的内容，因此总复杂度为 $O(TN^T)$ ，显然这在实际运用中是无法接受的。

### 前向算法

首先定义 **前向概率** ：给定隐马尔可夫模型 $\lambda$ ，定义到时刻 $t$ 部分观测序列 $O = (o_1, o_2, \ldots, o_t)$ 且状态为 $q_i$ 的概率为前向概率，记作：

$$
\alpha_t(i) = P(o_1, o_2, \ldots, o_t, i_t = q_i|\lambda)
$$

![前向算法图像](src\content\posts\hidden-markov-model\前向算法1.jpg)

根据前向概率的定义可推得：

$$
P(O|\lambda) = \sum_{i=1}^{N} P(o_1, o_2, \ldots, o_T, i_T = q_i | \lambda) = \sum_{i=1}^{N} \alpha_T(i)
$$

于是求解 $P(O|\lambda)$ 的问题被转化为了求解前向概率 $\alpha_T(i)$ 的问题。

由前向概率的定义可知：

$$
\alpha_1(i) = \pi_1b_{io_1}
$$

$$
\alpha_2(i) = \left[ \sum_{j=1}^{N} \alpha_1(j)a_{ji} \right] b_{io_2}
$$

$$
\alpha_3(i) = \left[ \sum_{j=1}^{N} \alpha_2(j)a_{ji} \right] b_{io_3}
$$

依次此类推可得如下递推公式：

$$
\alpha_{t+1}(i) = \left[ \sum_{j=1}^{N} \alpha_t(j)a_{ji} \right]j b_{io_{t+1}}
$$

### 后向算法

同前向算法一样，首先定义 **后向概率** ：给定隐马尔可夫模型 $\lambda$ ，定义在时刻 $t$ 状态为 $q_i$ 的条件下，从 $t+1$ 到 $T$ 的部分观测序列为 $O = (o_{t+1}, o_{t+2}, \ldots, o_T)$ 的概率为后向概率，记作：

$$
\beta_t(i) = P(o_{t+1}, o_{t+2}, \ldots, o_T|i_t = q_i, \lambda)
$$

![后向算法图像](src\content\posts\hidden-markov-model\后向算法1.jpg)

根据后向概率的定义可推得（将后向概率转为前向概率后带入前向概率的公式）：

$$
P(O|\lambda) = \sum_{i=1}^{N} \pi_i b_{io_1} \beta_1(i)
$$

由后向概率的定义可知：

$$
\beta_T(i) = 1
$$

$$
\beta_{T-1}(i) = \sum_{j=1}^{N} a_{ij}b_{jo_{T}} \beta_T(j)
$$

$$
\beta_{T-2}(i) = \sum_{j=1}^{N} a_{ij}b_{jo_{T-1}} \beta_{T-1}(j)
$$

依次此类推可得如下递推公式：

$$
\beta_t(i) = \sum_{j=1}^{N} a_{ij}b_{jo_{t+1}} \beta_{t+1}(j)
$$

综上可以看出前向算法和后向算法都是先计算局部概率，然后递推到全局，每一时刻的概率计算都会用上前一时刻计算出的结果，整体的时间复杂度大约为 O(TN^2) ，明显优于暴力计算的时间复杂度。

### 算法推广

利用前向概率和后向概率，可以得到关于单个状态和两个状态概率的一些计算公式。

1. 给定模型参数 $\lambda$ 和观测 $O$ ，在时刻 $t$ 处于状态 $q_i$ 的概率，记：

$$
\gamma_t(i) = P(i_t = q_i|O, \lambda)
$$

可以通过前向概率和后向概率进行计算，推导如下：

$$
\gamma_t(i) = P(i_t = q_i|O, \lambda) = \frac{P(i_t = q_i, O|\lambda)}{P(O|\lambda)}
$$

又由前向概率和后向概率的定义可知：

$$
\alpha_t(i) \beta_t(i) =  P(i_t = q_i, O|\lambda)
$$

因此有：

$$
\gamma_t(i) = \frac{P(i_t = q_i, O|\lambda)}{P(O|\lambda)} = \frac{P(i_t = q_i, O|\lambda)}{\sum_{j=1}^{N} P(i_t = q_j, O|\lambda)} = \frac{\alpha_t(i) \beta_t(i)}{\sum_{j=1}^{N} \alpha_t(j) \beta_t(j)}
$$

2. 给定模型参数 $\lambda$ 和观测 $O$ ，在时刻 $t$ 处于状态 $q_i$ 且在时刻 $t+1$ 处于状态 $q_j$ 的概率，记:

$$
\xi_t(i, j) = P(i_t = q_i, i_{t+1} = q_j|O,\lambda)
$$

可以通过前向后向概率进行计算，推导如下：

$$
\xi_t(i, j) = \frac{P(i_t = q_i, i_{t+1} = q_j, O|\lambda)}{P(O|\lambda)} = \frac{P(i_t = q_i, i_{t+1} = q_j, O|\lambda)}{\sum_{i=1}^{N} \sum_{j=1}^{N} P(i_t = q_i, i_{t+1} = q_j, O|\lambda)}
$$

其中：

$$
P(i_t = q_i, i_{t+1} = q_j, O|\lambda) = \alpha_t(i) a_{ij} b_{jo_{t+1}} \beta_{t+1}(j)
$$

因此有：

$$
\xi_t(i, j) = \frac{\alpha_t(i) a_{ij} b_{jo_{t+1}} \beta_{t+1}(j)}{\sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_t(i) a_{ij} b_{jo_{t+1}} \beta_{t+1}(j)}
$$

## 学习问题

> 学习 Baum-Welch 算法需要用到 EM 算法的知识，如果不知道什么是 EM 算法可以到本系列的上一篇博客进行学习（直接看 EM 算法的部分即可）。而且 Baum-Welch 算法本身也非常复杂，可以结合其他的博客辅助理解。

[隐马尔可夫模型之Baum-Welch算法详解](https://blog.csdn.net/u014688145/article/details/53046765)

[隐马尔可夫模型（HMM）三大基础问题之——学习问题](https://blog.csdn.net/qq_44648285/article/details/146015483)

[HMM的Baum-Welch算法和Viterbi算法公式推导细节](https://blog.csdn.net/xmu_jupiter/article/details/50965039)

[Derivation of Baum-Welch Algorithm for Hidden Markov Models](https://people.csail.mit.edu/stephentu/writeups/hmm-baum-welch-derivation.pdf)

[Python 机器学习 维特比算法和鲍姆-韦尔奇算法](https://zhuanlan.zhihu.com/p/688555596)

### 监督学习方法

我们有 $N$ 个隐状态 $S = \{ S_1, S_2, \ldots, S_N \}$ ，观测符号集合 $V = \{ v_1, v_2, \ldots, v_M \}$ 。

训练集中包含 $K$ 条样本序列，每条样本包含一个 **状态序列** 和对应的 **观测序列**：

$$
I^{(k)} = (i_1^{(k)}, i_2^{(k)}, \ldots, i_{T_k}^{(k)}) \quad O^{(k)} = (o_1^{(k)}, o_2^{(k)}, \ldots, o_{T_k}^{(k)})
$$

**初始状态概率** 的极大似然估计为：

$$
\pi_i = P(i_1 = S_1) = \frac{\sum_{k = 1}^{K} \mathbb{I} (i_1^{(k)} = S_i)}{K}
$$

> 统计所有序列的第一个状态是 $S_i$ 的频率。

**状态转移概率** 的极大似然估计为：

$$
a_{ij} = P(i_{t+1} = S_j|i_t = S_i) = \frac{\sum_{k=1}^{K} \sum_{t=1}^{T_k-1} \mathbb{I} (i_t^{(k)} = S_i, i_{t+1}^{(k)} = S_j)}{\sum_{k=1}^{K} \sum_{t=1}^{T_k-1} \mathbb{I} (i_t^{(k)} = S_i)}
$$

> 从 $S_i$ 转移到 $S_j$ 的次数除以从 $S_i$ 转移出去的总次数。

**观测（发射）概率** 的极大似然估计：

$$
b_i(k) = P(O_t = v_k|i_t = S_i) = \frac{\sum_{k`=1}^{K} \sum_{t=1}^{T_{k`}} \mathbb{I} (i_t^{k`} = S_i, o_t^{(k`)} = v_k)}{\sum_{k`=1}^{K} \sum_{t=1}^{T_{k`}} \mathbb{I} (i_t^{(k`)} = S_i)}
$$

> 在状态 $S_i$ 下观测到符号 $v_k$ 的次数除以状态 $S_i$ 出现的总次数。

显然此训练数据中的状态序列数据通常是需要人工标注出来的，因此代价较高，所以非监督学习的方法更为实用。

### Baum-Welch 算法

如果只有观测序列数据 $O = (o_1, o_2, \ldots, o_T)$ ，而没有状态序列数据 $I = (i_1, i_2, \ldots, i_T)$ ，那么隐马尔可夫模型就是一个含有隐藏变量的概率模型：

$$
P(O|\lambda) = \sum_I P(O|I, \lambda)P(I|\lambda)
$$

如果要对它进行参数估计，可以采用 **EM 算法** 来实现，具体步骤如下：

1. 确定完全数据的对数似然函数

此时观测数据为 $O = (o_1, o_2, \ldots, o_T)$ ，未观测数据为 $I = (i_1, i_2, \ldots, i_T)$ ，则完全数据为 $(O, I) = (o_1, o_2, \ldots, o_T, i_1, i_2, \ldots, i_T)$ ，完全数据的对数似然函数为：

$$
\log P(O, I|\lambda) = \log \left[ \pi_{i_1} \left( \prod_{t=1}^{T-1} b_{i_to_t}a_{i_ti_{t+1}} \right) b_{i_To_T} \right] = \log \pi_{i_1} + \sum_{t=1}^{T-1} \log a_{i_ti_{t+1}} + \sum_{t=1}^{T} \log b_{i_to_t}
$$

2. EM 算法 E 步：求解 $Q$ 函数

写出对完整数据的 **条件期望对数似然函数** ：

$$
Q(\lambda, \bar{\lambda}) = \sum_I P(I|O, \bar{\lambda}) \log P(O, I|\lambda)
$$

其中 $\bar{\lambda}$ 是隐马尔可夫模型参数的当前估计值， $\lambda$ 是要极大化的隐马尔可夫模型参数。为了便于后续计算， $Q$ 函数还可以作如下恒等变形：

$$

\begin{align*}
Q(\lambda, \bar{\lambda}) &= \sum_{I} P(I|O, \bar{\lambda}) \log P(O, I|\lambda) \\
&= \sum_{I} \frac{P(I|O, \bar{\lambda})P(O|\bar{\lambda})}{P(O|\bar{\lambda})} \log P(O, I|\lambda) \\
&= \sum_{I} \frac{P(O, I|\bar{\lambda})}{P(O|\bar{\lambda})} \log P(O, I|\lambda)
\end{align*}
$$

由于接下来仅极大化 $\lambda$ ，所以 $P(O|\bar{\lambda})$ 可以看做常数项进行略去，所以 $Q$ 函数可以进一步化简：

$$
\begin{aligned}
Q(\lambda, \bar{\lambda}) &= \sum_{I} P(O, I| \bar{\lambda}) \log P(O, I|\lambda) = \sum_{I} P(O, I| \bar{\lambda}) \left( \log \pi_{i_1} + \sum_{t=1}^{T-1} \log a_{i_t i_{t+1}} + \sum_{t=1}^{T} \log b_{i_t o_t} \right) \\
&= \sum_{I} P(O, I| \bar{\lambda}) \log \pi_{i_1} + \sum_{I} P(O, I| \bar{\lambda}) \left( \sum_{t=1}^{T-1} \log a_{i_t i_{t+1}} \right) + \sum_{I} P(O, I| \bar{\lambda}) \left( \sum_{t=1}^{T} \log b_{i_t o_t} \right)
\end{aligned}
$$

3. EM 算法 M 步：极大化 $Q$ 函数

由于要极大化的三个参数在上式中单独地出现在每个项中，所以只需对各项分别极大化。

- 求解 **初始状态概率**

上述 $Q$ 函数的第一项可以写成：

$$
\begin{aligned}
\sum_I P(O, I|\bar{\lambda}) \log \pi_{i_1} &= \sum_{i=1}^{N} \log \pi_i \left[ \sum_{i_2, i_3, \ldots, i_T} P(O, i_1 = q_1, i_2, i_3, \ldots, i_T|\bar{\lambda}) \right] \\
&= \sum_{i=1}^{N} \log \pi_i P(O, i_1 = q_1|\bar{\lambda}) = \sum_{i=1}^{N} \log \pi_i P(O, i_1 = q_i|\bar{\lambda})
\end{aligned}
$$

由于 $\pi_i$ 需要满足约束 $\sum_{i=1}^{N} \pi_i = 1$ ，利用拉格朗日乘数法，写出拉格朗日函数：

$$
L(\pi_i, \eta) = \sum_{i=1}^N \log \pi_i P(O,i_1 = q_i|\bar{\lambda}) + \eta \left( \sum_{i=1}^N \pi_i - 1 \right)
$$

对其关于 $\pi_i$ 偏导并令其结果为 0 可得:

$$
\frac{\partial}{\partial \pi_i} \left[ \sum_{i=1}^N \ln \pi_i P(O, i_1 = q_i | \bar{\lambda}) + \eta \left( \sum_{i=1}^N \pi_i - 1 \right) \right] = 0
$$

$$
P(O, i_1 = q_i|\bar{\lambda}) + \eta \pi_i = 0
$$

对上式关于 $i$ 求和可得：

$$
\sum_{i=1}^{N} P(O, i_1 = q_i|\bar{\lambda}) + \sum_{i=1}^{N} \eta \pi_i = 0
$$

$$
P(O|\bar{\lambda}) + \eta = 0
$$

将 $\eta$ 代回原式可得：

$$
P(O, i_1 = q_i|\bar{\lambda}) - P(O|\bar{\lambda}) \pi_i = 0
$$

$$
\pi_i = \frac{P(O, i_1 = q_i|\bar{\lambda})}{P(O|\bar{\lambda})}
$$

$$
\pi_i = \gamma_1(i)
$$

其中 $\gamma$ 就是[算法推广](#算法推广)中求解的 $\gamma$ 。

- 求解 **状态转移概率**

上述 $Q$ 函数的第二项可以写成：

$$
\begin{aligned}
&\sum_I P(O,I|\bar{\lambda}) \left( \sum_{t=1}^{T-1} \log a_{i_t i_{t+1}} \right) \\
= &\sum_{t=1}^{T-1} \sum_{i=1}^N \sum_{j=1}^N \log a_{ij} \left[ \sum_{(i_1,\ldots,i_{t-1},i_{t+2},\ldots,i_T)} P(O, i_1, \ldots, i_t = q_i, i_{t+1} = q_j, \ldots, i_T|\bar{\lambda}) \right] \\
= &\sum_{t=1}^{T-1} \sum_{i=1}^N \sum_{j=1}^N \log a_{ij} P(O,i_t = q_i,i_{t+1} = q_j | \bar{\lambda})
\end{aligned}
$$

由于 $a_{ij}$ 满足约束 $\sum_{j=1}^{N} a_{ij} = 1$ ，同样利用拉格朗日乘数法，写出拉格朗日函数：

$$
L(a_{ij}, \eta) = \sum_{t=1}^{T-1} \sum_{i=1}^{N} \sum_{j=1}^{N} \log a_{ij} P(O, i_t = q_i, i_{t+1} = q_j|\bar{\lambda}) + \eta \left( \sum_{j=1}^{N} a_{ij} - 1 \right)
$$

对其关于 $a_{ij}$ 偏导并令其结果为 0 可得:

$$
\frac{\partial}{\partial a_{ij}} \left[ \sum_{t=1}^{T-1} \sum_{i=1}^{N} \sum_{j=1}^{N} \log a_{ij} P(O, i_t = q_i, i_{t+1} = q_j | \bar{\lambda}) + \eta \left( \sum_{j=1}^{N} a_{ij} - 1 \right) \right] = 0
$$

$$
\sum_{t=1}^{T-1} P(O, i_t = q_i, i_{t+1} = q_j | \bar{\lambda}) + \eta a_{ij} = 0
$$

对上式关于 $j$ 求和可得：

$$
\sum_{j=1}^{N} \sum_{t=1}^{T-1} P(O, i_t = q_i, i_{t+1} = q_j | \bar{\lambda}) + \sum_{j=1}^{N} \eta a_{ij} = 0
$$

$$
\sum_{t=1}^{T-1} P(O, i_t = q_i|\bar{\lambda}) + \eta = 0
$$

将 $\eta$ 代回原式可得：

$$
\sum_{t=1}^{T-1} P(O, i_t = q_i, i_{t+1} = q_j | \bar{\lambda}) - \sum_{t=1}^{T-1} P(O, i_t = q_i | \bar{\lambda}) \cdot a_{ij} = 0
$$

$$
a_{ij} = \frac{\sum_{t=1}^{T-1} P(O, i_t = q_i, i_{t+1} = q_j | \bar{\lambda})}{\sum_{t=1}^{T-1} P(O, i_t = q_i | \bar{\lambda})}
$$

分子分母同时除以 $P(O|\bar{\lambda})$ 可得：

$$
a_{ij} = \frac{\displaystyle\frac{\sum_{t=1}^{T-1} P(O, i_t = q_i, i_{t+1} = q_j | \bar{\lambda})}{P(O|\bar{\lambda})}}{\displaystyle\frac{\sum_{t=1}^{T-1} P(O, i_t = q_i | \bar{\lambda})}{P(O|\bar{\lambda})}} = \frac{\sum_{t=1}^{T-1} P(i_t = q_i, i_{t+1} = q_j | O, \bar{\lambda})}{\sum_{t=1}^{T-1} P(i_t = q_i | O, \bar{\lambda})} = \frac{\sum_{t=1}^{T-1} \xi_t(i, j)}{\sum_{t=1}^{T-1} \gamma_t(i)}
$$

其中 $\gamma$ 和 $\xi$ 就是[算法推广](#算法推广)中求解的 $\gamma$ 和 $\xi$ 。

- 求解 **观测（发射）概率**

上述 $Q$ 函数的第三项可以写成：

$$
\begin{aligned}
\sum_{I} P(O, I|\bar{\lambda}) \left( \sum_{t=1}^{T} \log b_{i_t o_t} \right) &= \sum_{t=1}^{T} \sum_{j=1}^{N} \log b_{j o_t} \left[ \sum_{i_1, \ldots, i_{t-1}, i_{t+1}, \ldots, i_T} P(O, i_1, \ldots, i_t = q_j, \ldots, i_T|\bar{\lambda}) \right] \\
&= \sum_{t=1}^{T} \sum_{j=1}^{N} \log b_{j o_t} P(O, i_t = q_j|\bar{\lambda})
\end{aligned}
$$

由于 $b_{jk}$ 满足约束 $\sum_{k=1}^{M} b_{jk} = 1$ ，同样利用拉格朗日乘数法，写出拉格朗日函数：

$$
L(b_{jk}, \eta) = \sum_{t=1}^{T} \sum_{j=1}^{N} \ln b_{j o_t} P(O, i_t = q_j | \bar{\lambda}) + \eta \left( \sum_{k=1}^{M} b_{jk} - 1 \right)
$$

对其关于 $b_{jk}$ 偏导并令其结果为 0 可得:

$$
\frac{\partial}{\partial b_{jk}} \left[ \sum_{t=1}^{T} \sum_{j=1}^{N} \ln b_{j o_t} P(O, i_t = q_j | \bar{\lambda}) + \eta \left( \sum_{k=1}^{M} b_{jk} - 1 \right) \right] = 0
$$

$$
\sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda}) \mathbb{I}(o_t = v_k) + \eta b_{jk} = 0
$$

对上式关于 $k$ 求和可得：

$$
\sum_{k=1}^{M} \sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda}) \mathbb{I}(o_t = v_k) + \sum_{k=1}^{M} \eta b_{jk} = 0
$$

$$
\sum_{t=1}^{T} P(O, i_t = q_j|\bar{\lambda}) + \eta = 0
$$

将 $\eta$ 代回原式可得：

$$
\sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda}) \mathbb{I}(o_t = v_k) - \sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda}) \cdot b_{jk} = 0
$$

$$
b_{jk} = \frac{\sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda}) \mathbb{I}(o_t = v_k)}{\sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda})}
$$

分子分母同时除以 $P(O|\bar{\lambda})$ 可得：

$$
b_{jk} = \frac{\displaystyle\frac{\sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda}) \mathbb{I}(o_t = v_k)}{P(O|\bar{\lambda})}}{\displaystyle\frac{\sum_{t=1}^{T} P(O, i_t = q_j | \bar{\lambda})}{P(O|\bar{\lambda})}} = \frac{\sum_{t=1}^{T} P(i_t = q_j | O, \bar{\lambda}) \mathbb{I}(o_t = v_k)}{\sum_{t=1}^{T} P(i_t = q_j | O, \bar{\lambda})} = \frac{\sum_{t=1, o_t = v_k}^{T} \gamma_t(j)}{\sum_{t=1}^{T} \gamma_t(j)}
$$

其中 $\gamma$ 就是[算法推广](#算法推广)中求解的 $\gamma$ 。

## 预测问题

> Viterbi 算法也是一个动态规划算法，熟悉动态规划的读者理解起来会比较轻松。如果不了解什么是动态规划的话可以观看下列视频后再来看详细推导。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=596607341&bvid=BV1ZB4y1y7gC&cid=720556511&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=511741950&bvid=BV1kg411d7qk&cid=725097082&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

### 近似算法

近似算法思想：在每个时刻 $t$ 选择在该时刻最有可能出现的状态 $i_t^*$ ，从而得到一个状态序列 $I^* = (i_1^*, i_2^*, \ldots, i_T^*)$ ，将它作为预测的结果。具体算法如下：

给定隐马尔可夫模型 $\lambda$ 和观测序列 $O$ ，在时刻 $t$ 处于状态 $q_i$ 的概率$\gamma_t(i)$ 为：

$$
\gamma_t(i) = \frac{\alpha_t(i) \beta_t(i)}{\sum_{j=1}^{N} \alpha_t(j) \beta_t(j)}
$$

在每一时刻 $t$ 最有可能的状态 $i_t^*$ 为：

$$
i_t^* = \arg \max_{1 \leq i \leq N} [\gamma_t(i)] \quad t = 1, 2, \ldots, T
$$

从而得到状态序列 $I^* = (i_1^*, i_2^*, \ldots, i_T^*)$ 。

近似算法的优点是计算简单，其缺点是 **不能保证** 预测的状态序列整体是 **最有可能** 的状态序列，因为预测的序列可能有实际不发生的部分，也即可能存在状态转移概率 $a_{i^*j^*} = 0$ 的相邻状态 $i^*$ 和 $j^*$ 出现。尽管如此，近似算法仍然是 **有用的** 。

### Viterbi 算法

Viterbi 算法实际是用 **动态规划** 解隐马尔可夫模型预测问题，即用动态规划求概率最大路径，这时一条路径对应着一个状态序列。具体算法如下：

定义在时刻 定义在时刻 $t$ 状态为 $q_i$ 的所哟单个路径 $(i_1, i_2, \ldots, i_t)$ 中概率最大值为：

$$
\delta_t(i) = \max_{i_1, i_2, \ldots, i_{t-1}} P(o_1, \ldots, o_t, i_1, \ldots, i_{t-1}, i_t = q_i) \quad i = 1, 2, \ldots, N
$$

由此定义可推得：

$$
\delta_1(i) = \pi_i b_{i o_1}
$$

$$
\delta_2(i) = \max_{1 \leq j \leq N} [\delta_1(j) a_{ji}] b_{i o_2}
$$

$$
\delta_3(i) = \max_{1 \leq j \leq N} [\delta_2(j) a_{ji}] b_{i o_3}
$$

依次此类推可得如下递推公式：

$$
\delta_t(i) = \max_{1 \leq j \leq N} [\delta_{t-1}(j) a_{ji}] b_{i o_t}
$$

同时再定义在时刻 $t$ 状态为 $q_i$ 的所有单个路径 $(i_1, i_2, \ldots, i_t)$ 中概率最大的路径的第 $t-1$ 个结点为：

$$
\psi_t(i) = \arg \max_{1 \leq j \leq N} \delta_{t-1}(j) a_{ji}
$$

令 $i_T^* = \arg \max_{1 \leq i \leq N} \delta_T(i)$ 可得：

$$
i_{T-1}^* = \psi_T(i_T^*), i_{T-2}^* = \psi_{T-1}(i_{T-1}^*), \ldots, i_1^* = \psi_2(i_2^*)
$$

# 隐马尔可夫模型代码讲解

虽然 HMM 的代码比之前所有模型都要长，但其实就是一些简单的函数，原理已在上文中讲过。

```py frame="code" title="main.py"
import numpy as np
rng = np.random.RandomState(0)
obs_seq = np.random.randint(0, 3, size=50)


def _normalize(arr, axis=None, eps=1e-12):
    s = arr.sum(axis=axis, keepdims=True)
    s = np.maximum(s, eps)
    return arr / s

def _logsumexp(a, axis=None):
    a_max = np.max(a, axis=axis, keepdims=True)
    res = a_max + np.log(np.sum(np.exp(a - a_max), axis=axis, keepdims=True))
    if axis is None:
        return res.squeeze()
    return res

class HMM:
    def __init__(self, n_states, n_obs, seed=None):
        rng = np.random.RandomState(seed)
        self.n_states = n_states
        self.n_obs = n_obs
        # 初始化参数 π, A, B
        self.pi = _normalize(rng.rand(n_states))
        self.A = _normalize(rng.rand(n_states, n_states), axis=1)
        self.B = _normalize(rng.rand(n_states, n_obs), axis=1)

    # 发射概率
    def _emission_logprob(self, obs):
        assert obs.dtype.kind in 'iu', "Discrete observations must be integer dtype"
        logB = np.log(self.B[:, obs].T + 1e-12)
        return logB

    # 前向算法
    def _forward_log(self, obs):
        logA = np.log(self.A + 1e-12)
        logpi = np.log(self.pi + 1e-12)
        logB = self._emission_logprob(obs)
        T, S = logB.shape
        alpha = np.zeros((T, S))
        alpha[0] = logpi + logB[0]
        for t in range(1, T):
            a = alpha[t - 1][:, None] + logA
            alpha[t] = _logsumexp(a, axis=0).ravel() + logB[t]
        return alpha

    # 后向算法
    def _backward_log(self, obs):
        logA = np.log(self.A + 1e-12)
        logB = self._emission_logprob(obs)
        T, S = logB.shape
        beta = np.zeros((T, S))
        beta[T - 1] = 0.0
        for t in range(T - 2, -1, -1):
            b = logA + (logB[t + 1] + beta[t + 1])[None, :]
            beta[t] = _logsumexp(b, axis=1).ravel()
        return beta

    # 前后向算法（得到 gamma）
    def forward_backward(self, obs):
        alpha = self._forward_log(obs)
        beta = self._backward_log(obs)
        loggamma = alpha + beta
        loggamma -= _logsumexp(loggamma, axis=1)
        return np.exp(loggamma)

    # 计算对数似然
    def score(self, obs):
        alpha = self._forward_log(obs)
        return float(_logsumexp(alpha[-1]))

    # Viterbi 算法
    def viterbi(self, obs):
        logA = np.log(self.A + 1e-12)
        logpi = np.log(self.pi + 1e-12)
        logB = self._emission_logprob(obs)
        T, S = logB.shape
        delta = np.zeros((T, S))
        psi = np.zeros((T, S), dtype=int)
        delta[0] = logpi + logB[0]
        for t in range(1, T):
            val = delta[t - 1][:, None] + logA
            psi[t] = np.argmax(val, axis=0)
            delta[t] = np.max(val, axis=0) + logB[t]
        states = np.zeros(T, dtype=int)
        states[T - 1] = np.argmax(delta[T - 1])
        for t in range(T - 2, -1, -1):
            states[t] = psi[t + 1, states[t + 1]]
        return states

    # Baum-Welch 算法（EM算法）
    def fit(self, sequences, max_iter=100, tol=1e-4, verbose=False):
        prev_ll = None
        for it in range(max_iter):
            pi_count = np.zeros(self.n_states)
            A_count = np.zeros((self.n_states, self.n_states))
            B_count = np.zeros((self.n_states, self.n_obs))
            total_ll = 0.0
            # E-step: compute posteriors of hidden states
            for obs in sequences:
                T = len(obs)
                alpha = self._forward_log(obs)
                beta = self._backward_log(obs)
                loggamma = alpha + beta
                loggamma -= _logsumexp(loggamma, axis=1)
                gamma = np.exp(loggamma)
                total_ll += _logsumexp(alpha[-1])
                logA = np.log(self.A + 1e-12)
                logB = self._emission_logprob(obs)
                xi_sum = np.zeros((self.n_states, self.n_states))
                for t in range(T - 1):
                    l = alpha[t][:, None] + logA + (logB[t + 1] + beta[t + 1])[None, :]
                    l -= _logsumexp(l)
                    xi_sum += np.exp(l)
                pi_count += gamma[0]
                A_count += xi_sum
                for t in range(T):
                    B_count[:, obs[t]] += gamma[t]
            # M-step: update parameters
            self.pi = _normalize(pi_count)
            self.A = _normalize(A_count, axis=1)
            self.B = _normalize(B_count, axis=1)
            total_ll = float(total_ll)
            if verbose:
                print(f"Iter {it+1}: log-likelihood = {total_ll:.6f}")
            if prev_ll is not None and abs(total_ll - prev_ll) < tol:
                break
            prev_ll = total_ll
        return self


# 执行代码
if __name__ == '__main__':
    model = HMM(n_states=2, n_obs=3, seed=0)
    model.fit([obs_seq], max_iter=50, verbose=True)

    print('Trained pi:', model.pi)
    print('Trained A :', model.A)
    print('Trained B :', model.B)
    print('Viterbi   :', model.viterbi(obs_seq)[:20])
    print('Log-lik   :', model.score(obs_seq))
```

## 计算问题

这个部分的代码可以观看[上面的讲解](#计算问题)对照学习。

```py showLineNumbers
# 发射概率
def _emission_logprob(self, obs):
    assert obs.dtype.kind in 'iu', "Discrete observations must be integer dtype"
    logB = np.log(self.B[:, obs].T + 1e-12)
    return logB

# 前向算法
def _forward_log(self, obs):
    logA = np.log(self.A + 1e-12)
    logpi = np.log(self.pi + 1e-12)
    logB = self._emission_logprob(obs)
    T, S = logB.shape
    alpha = np.zeros((T, S))
    alpha[0] = logpi + logB[0]
    for t in range(1, T):
        a = alpha[t - 1][:, None] + logA
        alpha[t] = _logsumexp(a, axis=0).ravel() + logB[t]
    return alpha

# 后向算法
def _backward_log(self, obs):
    logA = np.log(self.A + 1e-12)
    logB = self._emission_logprob(obs)
    T, S = logB.shape
    beta = np.zeros((T, S))
    beta[T - 1] = 0.0
    for t in range(T - 2, -1, -1):
        b = logA + (logB[t + 1] + beta[t + 1])[None, :]
        beta[t] = _logsumexp(b, axis=1).ravel()
    return beta

# 前后向算法（得到 gamma）
def forward_backward(self, obs):
    alpha = self._forward_log(obs)
    beta = self._backward_log(obs)
    loggamma = alpha + beta
    loggamma -= _logsumexp(loggamma, axis=1)
    return np.exp(loggamma)

# 计算对数似然
def score(self, obs):
    alpha = self._forward_log(obs)
    return float(_logsumexp(alpha[-1]))
```

## 学习问题

这个部分的代码可以观看[上面的讲解](#baum-welch-算法)对照学习。

```py showLineNumbers
def fit(self, sequences, max_iter=100, tol=1e-4, verbose=False):
    prev_ll = None
    for it in range(max_iter):
        pi_count = np.zeros(self.n_states)
        A_count = np.zeros((self.n_states, self.n_states))
        B_count = np.zeros((self.n_states, self.n_obs))
        total_ll = 0.0
        # E-step: compute posteriors of hidden states
        for obs in sequences:
            T = len(obs)
            alpha = self._forward_log(obs)
            beta = self._backward_log(obs)
            loggamma = alpha + beta
            loggamma -= _logsumexp(loggamma, axis=1)
            gamma = np.exp(loggamma)
            total_ll += _logsumexp(alpha[-1])
            logA = np.log(self.A + 1e-12)
            logB = self._emission_logprob(obs)
            xi_sum = np.zeros((self.n_states, self.n_states))
            for t in range(T - 1):
                l = alpha[t][:, None] + logA + (logB[t + 1] + beta[t + 1])[None, :]
                l -= _logsumexp(l)
                xi_sum += np.exp(l)
            pi_count += gamma[0]
            A_count += xi_sum
            for t in range(T):
                B_count[:, obs[t]] += gamma[t]
        # M-step: update parameters
        self.pi = _normalize(pi_count)
        self.A = _normalize(A_count, axis=1)
        self.B = _normalize(B_count, axis=1)
        total_ll = float(total_ll)
        if verbose:
            print(f"Iter {it+1}: log-likelihood = {total_ll:.6f}")
        if prev_ll is not None and abs(total_ll - prev_ll) < tol:
            break
        prev_ll = total_ll
    return self
```

## 预测问题

这个部分的代码可以观看[上面的讲解](#viterbi-算法)对照学习。

```py showLineNumbers
def viterbi(self, obs):
    logA = np.log(self.A + 1e-12)
    logpi = np.log(self.pi + 1e-12)
    logB = self._emission_logprob(obs)
    T, S = logB.shape
    delta = np.zeros((T, S))
    psi = np.zeros((T, S), dtype=int)
    delta[0] = logpi + logB[0]
    for t in range(1, T):
        val = delta[t - 1][:, None] + logA
        psi[t] = np.argmax(val, axis=0)
        delta[t] = np.max(val, axis=0) + logB[t]
    states = np.zeros(T, dtype=int)
    states[T - 1] = np.argmax(delta[T - 1])
    for t in range(T - 2, -1, -1):
        states[t] = psi[t + 1, states[t + 1]]
    return states
```

# 深层问题思考

1. HMM 中用到的 BW 算法是特殊的 EM 算法，它究竟特殊在哪里？

HMM 的 Baum–Welch 算法是 **EM 算法的一个特例** ，它特殊的地方在于它的 **隐变量结构** 和 **E 步的计算方式** 。

- 特殊的隐变量结构 ———— 马尔可夫链

普通 EM 假设隐藏变量是独立的或结构简单的，而 HMM 的隐藏变量 $I$ 是一个马尔可夫链。它的依赖关系是：

$$
P(I) = P(i_1) \prod_{t=2}^{T} P(i_t \mid i_{t-1})
$$

- E 步可解析计算 ———— 不用采样或者积分

在一般 EM 中，E步往往要对所有隐变量求期望，复杂度极高。但在 HMM 中，隐状态间满足 **马尔可夫性** ，因此可以用 **前向-后向算法** 高效求解期望。

# 参考文献

1. [机器学习-12-隐马尔可夫模型HMM](https://www.cnblogs.com/Cnoized/p/18916857)

2. [隐马尔可夫模型](https://zhuanlan.zhihu.com/p/28412002248)

3. [马尔可夫模型 and 隐马尔可夫模型](https://blog.csdn.net/xiang_gina/article/details/148400775)

4. [概率图模型系列（3）：隐马尔可夫模型（HMM）](https://allenwind.github.io/blog/7681/)

5. [马尔可夫模型及其应用](http://www.mselab.cn/media/files/B03.马尔可夫模型.pdf)

6. [机器学习：隐马尔可夫模型(HMM)](https://zhuanlan.zhihu.com/p/1893730053705138991)

7. [【机器学习】马尔可夫模型与隐马尔科夫模型](https://blog.csdn.net/m0_53700832/article/details/140442722)

8. [隐马尔可夫模型（HMM）及其三个基本问题](https://sm1les.com/2019/04/10/hidden-markov-model/)