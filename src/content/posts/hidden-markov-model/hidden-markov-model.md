---
title: 【机器学习基本模型】第七节：隐马尔可夫模型
published: 2025-10-30
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

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

- 概率计算问题：给定模型 $\lambda = (A, B, \pi)$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，计算在模型 $\lambda$ 下观测序列 $O$ 出现的概率 $P(O|\lambda)$

- 学习问题：已知观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，估计模型 $\lambda = (A, B, \pi)$ 参数，使得在该模型下观测序列概率 $P(O|\lambda)$ 最大，即用极大似然估计的方法估计参数

- 预测问题（也称解码问题）：已知模型 $\lambda = (A, B, \pi)$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，求对给定观测序列条件概率 $P(I|O)$ 最大的状态序列 $I = (i_1, i_2, \ldots, i_T)$ ，即给定观测序列，求最有可能的对应状态序列

这三个问题解决起来都非常复杂，就让我们逐个解决吧。

## 概率计算问题

> 只看下面的讲解理解起来可能较为困难，请自行结合概率图状态转移的思路进行理解（最好画图理解），也可以辅助其他博客进行学习。

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
\Gamma_t(i) = P(i_t = q_i|O, \lambda)
$$

可以通过前向概率和后向概率进行计算，推导如下：

$$
\Gamma_t(i) = P(i_t = q_i|O, \lambda) = \frac{P(i_t = q_i, O|\lambda)}{P(O|\lambda)}
$$

又由前向概率和后向概率的定义可知：

$$
\alpha_t(i) \beta_t(i) =  P(i_t = q_i, O|\lambda)
$$

因此有：

$$
\Gamma_t(i) = \frac{P(i_t = q_i, O|\lambda)}{P(O|\lambda)} = \frac{P(i_t = q_i, O|\lambda)}{\sum_{j=1}^{N} P(i_t = q_j, O|\lambda)} = \frac{\alpha_t(i) \beta_t(i)}{\sum_{j=1}^{N} \alpha_t(j) \beta_t(j)}
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

> Baum-Welch 算法需要用到 EM 算法，如果不知道什么是 EM 算法可以到本系列的上一篇博客进行学习（直接看 EM 算法的部分即可）。而且 Baum-Welch 算法也非常复杂，可以结合其他的博客辅助理解。

[隐马尔可夫模型之Baum-Welch算法详解](https://blog.csdn.net/u014688145/article/details/53046765)

[隐马尔可夫模型（HMM）三大基础问题之——学习问题](https://blog.csdn.net/qq_44648285/article/details/146015483)

[HMM的Baum-Welch算法和Viterbi算法公式推导细节](https://blog.csdn.net/xmu_jupiter/article/details/50965039)

[Derivation of Baum-Welch Algorithm for Hidden Markov Models](https://people.csail.mit.edu/stephentu/writeups/hmm-baum-welch-derivation.pdf)

[Python 机器学习 维特比算法和鲍姆-韦尔奇算法](https://zhuanlan.zhihu.com/p/688555596)

> Viterbi 算法则是动态规划算法，比较简单，本篇博客不做介绍，需要的读者自行观看视频讲解。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=596607341&bvid=BV1ZB4y1y7gC&cid=720556511&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=511741950&bvid=BV1kg411d7qk&cid=725097082&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

### 监督学习方法

假设已给出训练数据包含 $$ 个长度相同的观测序列和对应的状态序列 $$ ，那么可以利用极大似然估计法来估计隐马尔可夫模型的参数。

- 转移概率 $$ 的估计：

$$

$$

其中 $$ 为样本中时刻 $$ 处于状态 $$ 而到时刻 $$ 转移到状态 $$ 的频数。

- 观测概率 $$ 的估计：

$$

$$

其中 $$ 为样本中状态为 $$ ，其对应观测为 $$ 的频数。

- 初始状态概率 $$ 的估计：

$$

$$



# 参考文献

1. [机器学习-12-隐马尔可夫模型HMM](https://www.cnblogs.com/Cnoized/p/18916857)

2. [隐马尔可夫模型](https://zhuanlan.zhihu.com/p/28412002248)

3. [马尔可夫模型 and 隐马尔可夫模型](https://blog.csdn.net/xiang_gina/article/details/148400775)

4. [概率图模型系列（3）：隐马尔可夫模型（HMM）](https://allenwind.github.io/blog/7681/)

5. [马尔可夫模型及其应用](http://www.mselab.cn/media/files/B03.马尔可夫模型.pdf)

6. [机器学习：隐马尔可夫模型(HMM)](https://zhuanlan.zhihu.com/p/1893730053705138991)

7. [【机器学习】马尔可夫模型与隐马尔科夫模型](https://blog.csdn.net/m0_53700832/article/details/140442722)

8. [隐马尔可夫模型（HMM）及其三个基本问题](https://sm1les.com/2019/04/10/hidden-markov-model/)