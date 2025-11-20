---
title: 【机器学习基本模型】第八节：最大熵马尔可夫模型
published: 2025-11-02
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

> 写在前面：本篇延续上一篇的 HMM 进行拓展，MEMM 本质上就是为了解决 HMM 的痛点而产生的。

# 最大熵马尔可夫模型基本原理

最大熵马尔可夫模型（Maximum-entropy Markov model，简称 MEMM）由 Andrew McCallum、Dayne Freitag 和 Fernando Pereira 三人于 2000 年提出。它结合了隐马尔可夫模型（HMM）和最大熵模型（MEM），被广泛应用于处理序列标注问题。文献认为在HMM中主要存在以下两个问题：

- 无法用特征对观测序列参数化：在很多序列标注任务中，尤其当不能枚举所有观测序列时，通常需要用大量的特征来刻画观测序列。比如在文本中识别一个未见过的公司名字时，通常需要用到很多特征信息，如大写字母、结尾词、词性、格式、在文本中的位置等。

- 判别式模型比生成式模型更适合处理序列标注问题：HMM 多被用在处理序列标注问题，序列标注问题的目标是求出状态相对于观测的条件概率 $P(state|observation)$ ，而 HMM 是对状态和观测的联合概率 $P(state, observation)$ 进行建模的生成式模型，相对于直接对 $P(state|observation)$ 进行建模的判别式模型来说，显然判别式模型更适合处理虚了标注问题。

MEMM 的具体定义如下：

![最大熵马尔可夫模型图像](src\content\posts\maximum-entropy-markov-model\最大熵马尔可夫模型1.png)

若想知道什么是最大熵马尔可夫模型，我们就必须先弄清楚什么是最大熵模型。

## 理论基础

**最大熵模型** （maximum entropy model，简称 MaxEnt）是典型的分类算法，和逻辑回归同属于 **对数线性分类模型** 。在损失函数优化的过程中，使用了与支持向量机相类似的凸优化技术。

最大熵模型由最大熵原理推导实现，做法是在给定一些约束条件的情况下，找到一个模型，使得这个模型输出分布的熵（不确定性）最大。

### 最大熵原理

最大熵原理是概率模型学习的一个准则。最大熵原理认为：学习概率模型时，在所有可能的概率模型/分布中， **熵最大的模型是最好的模型** 。通常用约束条件来确定概率模型的集合，所以，最大熵原理也可以表述为在满足约束条件的模型集合中选取熵最大的模型。

假设离散随机变量 $X$ 的概率分布是 $P(X)$ ，则其熵是：

$$
H(P) = - \sum_x P(x) \log P(x)
$$

而熵满足以下不等式：

$$
0 \leq H(P) \leq \log |X|
$$

其中 $|X|$ 是 $X$ 的取值个数，当且仅当 $X$ 的分布是均匀分布时右边的等号成立。也就是说，当 $X$ 服从均匀分布时熵最大：

$$
H(P) = -\sum_x \frac{1}{|X|} \log \frac{1}{|X|} = - \log \frac{1}{|X|} = \log |X|
$$

直观地说：最大熵原理认为要选择的概率模型首先必须满足已有的事实，即约束条件。在没有更多信息的情况下，那些不确定的部分都是 “等可能的” 。最大熵原理通过 **熵的最大化来表示等可能性** 。这是因为 “等可能” 不容易操作，而熵则是一个可优化的数值指标。

将最大熵原理应用到分类即可得到最大熵模型。

### 最大熵模型

最大熵模型假设分类模型是一个条件概率分布 $P(Y|X)$， $X$ 为特征， $Y$ 为输出。

给定一个训练集 $S = \{ (x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), \ldots, (x^{(m)}, y^{(m)}) \}$ 其中 $x$ 为 $n$ 维特征向量， $y$ 为类别输出。我们的目标就是用最大熵模型选择一个最好的分类类型。

在给定训练集的情况下，我们可以得到总体联合分布 $P(X,Y)$ 的经验分布 $\bar{P}(X, Y)$ 和边缘分布 $P(X)$ 的经验分布 $\bar{P}(X)$ 。

其中 $\bar{P}(X, Y)$ 通过训练集中 $X$ 、 $Y$ 同时出现的次数除以样本总数 $m$ 来计算， $\bar{P}(X)$ 通过训练集中 $X$ 出现的次数除以样本总数 $m$ 来计算：

$$
\bar{P}(X = x, Y = y) = \frac{\text{count}(X = x, Y = y)}{N}
$$

$$
\bar{P}(X = x) = \frac{\text{count}(X = x)}{N}
$$

> 特征函数与约束条件

在最大熵模型中，我们通过一组特征函数 $f(x,y)$ 描述输入 $x$ 和输出 $y$ 之间的关系。其形式如下：

$$
f(x,y) = 
\begin{cases} 
1 & \text{if certain condition between } x \text{ and } y \text{ holds} \\
0 & \text{otherwise}
\end{cases}
$$

每个特征函数对应一个可能的输入输出关系或约束，不同的训练样本可能激活不同的特征函数，并且同一个样本可能激活多个特征函数。

特征函数 $f(x,y)$ 关于经验分布 $\bar{P}(X, Y)$ 的期望值，用 $\mathbb{E}_{\bar{P}}\big[ f \big]$ 表示:

$$
\mathbb{E}_{\bar{P}}\big[ f \big] = \sum_{x, y} \bar{P}(x, y)f(x, y) = \frac{1}{N} \sum_{x, y} f(x, y)
$$

由于特征函数在构建概率模型时扮演重要角色，我们希望最大熵模型能满足这些约束条件。因此我们要求模型 $P(Y|X)$ 关于函数 $f$ 的期望应该等于经验分布关于 $f$ 的期望。模型 $P(Y|X)$ 关于 $f$ 的期望为：

$$
\mathbb{E}_{P}\big[ f \big] = \sum_{x, y} P(x, y)f(x, y) ≈ \sum_{x, y} \bar{P}(x)P(y|x)f(x, y)
$$

因此我们需要使得模型的期望满足以下约束（确保模型的特征函数期望与训练数据一致）：

$$
\sum_{x, y} \bar{P}(x)P(y|x)f(x, y) = \sum_{x, y} \bar{P}(x, y)f(x, y)
$$

上述式子便是最大熵模型中所要求满足的约束条件。给定 $n$ 个特征函数 $f_i(x, y)$ ，则有 $n$ 个约束条件。用 $C$ 表示满足约束的模型集合：

$$
C = \{ P|\mathbb{E}_{P}\big[f_i\big] = \mathbb{E}_{\bar{P}}\big[f_i\big], I = 1, 2, \ldots, n \}
$$

我们通过从满足约束的模型集合 $C$ 中选出熵最大的模型，就可以得到最终的最大熵模型。

> 最大熵模型定义

关于条件分布 $P(Y|X)$ 的熵为：

$$
H(P) = - \sum_{x, y} P(x, y) \log P(y|x) = - \sum_{x, y} \bar{P}(x)P(y|x) \log P(y|x)
$$

满足约束条件后使得该熵最大，由此可得 MaxEnt 模型 $P^*$ 为：

$$
P^* = \arg \max_{P \in C}H(P)
$$

给定数据集 $\{(x_i, y_i)\}_{i=1}^N$ ，特征函数 $f_i(x, y) \quad (i = 1, 2 \ldots, n)$ ，根据经验分布得到满足约束集的模型集合：

$$
\begin{align*}
\min_{P \in C} \quad & \sum_{x,y} \bar{P}(x) P(y|x) \log P(y|x) \\
\text{s.t.} \quad & \mathbb{E}_p\big[f_i\big] = \mathbb{E}_{\bar{P}}\big[f_i\big] \\
& \sum_y P(y|x) = 1
\end{align*}
$$

### 模型求解

MaxEnt 模型最后被形式化为带有约束条件的最优化问题，可以通过拉格朗日乘子法将其转为无约束优化的问题，引入拉格朗日乘子 $w_i$ ，定义朗格朗日函数 $L(P, w)$ ：

$$
L(P, w) = -H(P) + w_0 \left[ 1 - \sum_y P(y|x) \right] + \sum_{i=1}^n w_i \Big(\mathbb{E}_{\bar{P}}\big[f_i\big] - \mathbb{E}_p\big[f_i\big]\Big)
$$

> 拉格朗日对偶问题求解最优化问题

根据拉格朗日对偶问题（如果不知道什么是拉格朗日对偶问题可以看本系列的第五节，只需要看拉格朗日对偶问题相关的介绍即可），我们可以得到下面这个优化问题：

$$
\max_w \min_{P \in C} L(P, w)
$$

我们可以先求解内部的极小值问题，记作 $\Psi(w)$ ：

$$
\Psi(w) = \min_{P \in C} L(P, w) = L(P_w, w)
$$

上式中得到的 $P_w$ 可以记作：

$$
P_w = \arg \min_{P \in C} L(P, w) = P_w(y|x)
$$

由于求解 $P$ 的最小值 $P_w$ ,只需对于 $P(y|x)$ 求导即可,令导数等于 0 即可得到 $P_w(y|x)$ ：

$$
\begin{align*}
\frac{\partial L(P, w)}{\partial P(y|x)} &= \sum_{x,y} \bar{P}(x) (\log P(y|x) + 1) - \sum_y w_0 - \sum_{x,y} \bar{P}(x) \sum_{i=1}^n w_i f_i(x, y) \\
&= \sum_{x,y} \bar{P}(x) \left[ \log P(y|x) + 1 - w_0 - \sum_{i=1}^n w_i f_i(x, y) \right]
\end{align*}
$$

令导数为 0 可得：

$$
P(y|x) = \exp\left(\sum_{i=1}^{n} w_i f_i(x, y) + w_0 - 1\right) = \frac{\exp\Big(\sum_{i=1}^{n} w_i f_i(x, y)\Big)}{\exp(1 - w_0)}
$$

又因为 $\sum_y P(y|x) = 1$ ，可得：

$$
\frac{1}{\exp(1 - w_0)} \sum_y \exp\left(\sum_{i=1}^{n} w_i f_i(x, y)\right) = 1
$$

进而可以得到：

$$
\exp(1 - w_0) = \sum_{y} \exp\left(\sum_{i=1}^{n} w_i f_i(x, y)\right)
$$

这里 $\exp(1 - w_0)$ 起到了归一化的作用。

令 $Z_w(x)$ 表示 $\exp(1 - w_0)$ ，便得到了 MaxEnt 模型：

$$
P_w(y|x) = \frac{1}{Z_w(x)} \exp\left(\sum_{i=1}^{n} w_i f_i(x, y)\right)
$$

$$
Z_w(x) = \sum_{y} \exp\left(\sum_{i=1}^{n} w_i f_i(x, y)\right)
$$

这里 $f_i(x, y)$ 代表特征函数， $w_i$ 代表特征函数的权值， $P_w(y|x)$ 即为 MaxEnt 模型，现在内部的极小化求解得到关于 $w$ 的函数，现在求其对偶问题的外部极大化即可，将最优解记做 $w^*$ ：

$$
w^* = \arg\max_{w} \Psi(w)
$$

所以现在最大上模型转为求解 $\Psi(w)$ 的极大化问题，求解最优的 $w^*$ 后， 便得到了所要求的MaxEnt 模型，将 $P_w(y|x)$ 带入 $\Psi(w)$ ，可得：

$$
\begin{align*}
\Psi(w) &= \sum_{x,y} \bar{P}(x) P_w(y|x) \log P_w(y|x) + \sum_{i=1}^{n} w_i \left[ \sum_{x,y} \bar{P}(x,y) f(x,y) - \sum_{x,y} \bar{P}(x) P_w(y|x) f(x,y) \right] \\
&= \sum_{x,y} \bar{P}(x,y) \sum_{i=1}^{n} w_i f_i(x,y) + \sum_{x,y} \bar{P}(x) P_w(y|x) \left[ \log P_w(y|x) - \sum_{i=1}^{n} w_i f_i(x,y) \right]
\end{align*}
$$

又因为下述结论：

$$
P_w(y|x) = \frac{1}{Z_w(x)} \exp\left(\sum_{i=1}^{n} w_i f_i(x, y)\right) \Rightarrow \log P_w(y|x) = \sum_{i=1}^{n} w_i f_i(x, y) - \log Z_w(x)
$$

因此可以得到：

$$
\begin{align*}
\Psi(w) &= \sum_{x,y} \bar{P}(x,y) \sum_{i=1}^{n} w_i f_i(x,y) - \sum_{x,y} \bar{P}(x) P_w(y|x) \log Z_w(x) \\
&= \sum_{x, y} \bar{P}(x, y) \sum_{i=1}^{n}w_if_i(x, y) - \sum_x \bar{P}(x)\log Z_w(x) 
\sum_y P_w(y|x)
\end{align*}
$$

再根据 $\sum_y P_w(y|x) = 1$ 可得最后的优化问题为：

$$
\max_{w} \Psi(w) = \max_{w} \sum_{x, y} \bar{P}(x, y) \sum_{i=1}^{n}w_if_i(x, y) - \sum_x \bar{P}(x) \log Z_w(x)
$$

> 极大似然估计求解最优化问题

其实我们还可以用极大似然估计的方法求解优化函数，先写出对数似然函数：

$$
L_{\bar{P}}(P_w) = \sum_{x, y} \bar{P}(x, y) \log P(y|x)
$$

将上文得到的 $P_w(y|x)$ 的表达式带入对数似然函数可得：

$$
L_{\bar{P}}(P_w) = \sum_{x, y} \bar{P}(x, y) \sum_{i=1}^{n}w_if_i(x, y) - \sum_x \bar{P}(x) \log Z_w(x)
$$

显而易见，拉格朗日对偶得到的结果与极大似然得到的结果时等价的。

## 概念介绍

设 $V$ 是所有可能的 **观测集合** ， $Q$ 是所有可能的 **状态集合** ：

$$
V = \{ v_1, v_2, \ldots, v_M \}, Q = \{ q_1, q_2, \ldots, q_N \}
$$

其中 $N$ 式可能的状态数， $M$ 是可能的观测数。

$O$ 是长度为 $T$ 的 **观测序列** ， $I$ 是对应的 **状态序列** ：

$$
O = \{ o_1, o_2, \ldots, o_T \}, I = \{ i_1, i_2, \ldots, i_T \}
$$

在已知观测序列 $O$ 的条件下，状态序列为 $I$ 的概率为（下面用到了最大熵模型的结论）：

$$
\begin{align*}
P(I|O) &= P(i_1, i_2, \ldots, i_T | O) \\
&= P(i_1 | O) \prod_{t=2}^T P(i_t | i_{t-1}, O) \\
&= P(i_1 | O) \prod_{t=2}^T \frac{1}{Z(i_{t-1}, O)} \exp\left(\sum_{k=1}^K w_k f_k(i_t, i_{t-1}, O)\right)
\end{align*}
$$

其中 $Z(i_{t-1}, O) = \sum_{i_t} \exp\left( \sum_{k=1}^{K} w_kf_k(i_t, i_{t-1}, O) \right)$ 、 $f_k(i_t, i_{t-1}, O)$ 和 $w_k$ 分别对应于最大熵模型中的归一化因子、特征函数和特征函数的权重。

在 $i_1$ 前添加一个恒为常量 0 的状态 $i_0$ ，则上式可化简为：

$$
\begin{align*}
P(I|O) &= P(i_1, i_2, \ldots, i_T | O) \\
&= \prod_{t=2}^T P(i_t | i_{t-1}, O) \\
&= \prod_{t=2}^T \frac{1}{Z(i_{t-1}, O)} \exp\left(\sum_{k=1}^K w_k f_k(i_t, i_{t-1}, O)\right)
\end{align*}
$$

# 最大熵马尔可夫模型实现难点

与 HMM 相同，要想构建出 MEMM，就必须要解决以下三个问题：

- 计算问题：在给定模型参数 $w_k(k = 1, 2, \ldots, K)$ 、观测序列 $O = (o_1, o_2, \ldots, o_T)$ 和状态序列 $I = (i_1, i_2, \ldots, i_T)$ 的条件下，计算条件概率 $P(I|O)$

- 学习问题：在给定观测序列 $O = (o_1, o_2, \ldots, o_T)$ 和状态序列 $I = (i_1, i_2, i_T)$ 的条件下，估计模型参数 $w_k(k = 1, 2, \ldots, K)$ ，使得条件概率 $P(I|O)$ 达到最大

- 预测问题：已知模型参数 $w_k(k = 1, 2, \ldots, K)$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，求条件概率 $P(I|O)$ 达到最大的状态序列

下面就详细讲解一下这三个问题的解决方案。

## 计算问题

由于 MEMM 属于判别式模型，对于判别式模型来说，给定了模型参数 $w_k(k = 1, 2, \ldots, K)$ 和观测序列 $O = (o_1, o_2, \ldots, o_T)$ ，直接套用模型的定义就可以计算出条件概率 $P(I|O)$ 。

## 学习问题

- 既有观测序列 $O = (o_1, o_2, \ldots, o_T)$ 也有状态序列 $I = (i_1, i_2, \ldots, i_T)$ 时：

此时 MEMM 类似于最大熵模型，所以能用于估计最大熵模型参数的策略和算法均可用于 MEMM。

- 只有观测序列 $O = (o_1, o_2, \ldots, o_T)$ 而没有状态序列 $I = (i_1, i_2, \ldots, i_T)$ 时：

此时 MEMM 是一个含有隐变量的模型，对于含有隐变量的模型，则可以使用 EM 算法对其进行参数估计。

## 预测问题

我们在上一篇文章中说到的 Viterbi 算法一样可以用在 MEMM 的预测问题中，具体算法如下：

定义在时刻 $t$ 状态为 $q_i$ 的所有单个路径 $(i_1, i_2, \ldots, i_t)$ 中概率最大值为：

$$
\delta_t(i) = \max_{i_1, i_2, \ldots, i_{t-1}} P(i_1, \ldots, i_{t-1}, i_t = q_i | O) \quad i = 1, 2, \ldots, N
$$

由此定义可推得：

$$
\delta_1(i) = P(i_1 = q_i|i_0 = 0, O)
$$

$$
\delta_2(i) = \max_{1 \leq j \leq N} \big[\delta_1(j) \cdot P(i_2 = q_i|i_1 = q_j, O)\big]
$$

$$
\delta_3(i) = \max_{1 \leq j \leq N} \big[\delta_2(j) \cdot P(i_3 = q_i|i_2 = q_j, O)\big]
$$

依次此类推可得如下递推公式：

$$
\delta_t(i) = \max_{1 \leq j \leq N} \big[\delta_{t-1}(j) \cdot P(i_t = q_i|i_{t-1} = q_j, O)\big]
$$

同样再定义在时刻 $t$ 状态为 $q_i$ 的所有单个路径 $(i_1, i_2, \ldots, i_t)$ 中概率最大的路径的第 $t-1$ 个节点为：

$$
\Psi_t(i) = \arg\max_{1 \leq j \leq N} \big[\delta_{t-1}(j) \cdot P(i_t = q_i | i_{t-1} = q_j, O)\big]
$$

令 $i_T^* = \arg \max_{1 \leq i \leq N} \delta_T(i)$ 可得：

$$
i_{T-1}^* = \Psi_T(i_T^*), i_{T-2}^* = \Psi_{T-1}(i_{T-1}^*), \ldots, i_1^* = \Psi_2(i_2^*)
$$

由于 MEMM 模型本身的问题，用维特比算法求出来的最优序列 $I^* = (i_1^*, i_2^*, \ldots, i_T^*)$ **并不是真正意义上的最优状态序列** ，下面举例说明。

假设已知的观测序列为 $O = (o_1, o_2, o_3, o_4)$ ，所有可能的状态的集合为 $O = (1, 2, 3, 4, 5)$ ，各个时刻之间的状态转移概率如下图所示：

![最大熵马尔可夫模型图像](src\content\posts\maximum-entropy-markov-model\最大熵马尔可夫模型2.png)

由维特比算法易算得最优状态序列 $I^* = (1, 1, 1, 1)$ ，但是结合的实际情形可知，状态序列 $\bar{I} = (1, 2, 2, 2)$ 显然比 $I^*$ 更加合理，这是因为 $\bar{I}$ 每个时刻之间的状态转移都比 $I^*$ 更加 **自信** 。

因此 $I^*$ 并不一定是真正意义上的最优状态序列，而这就是 MEMM 的 **标注偏置问题** （The Label Bias Problem）。

导致标注偏置问题的主要原因是 MEMM 对各个时刻的状态取值的概率 $P(i_t|i_{t-1}, o_t)$ 都进行了局部归一化，也就是：

$$
\sum_{i_t} P(i_t | i_{t-1}, O) = \sum_{i_t} \frac{1}{Z(i_{t-1}, O)} \exp\left(\sum_{k=1}^K w_k f_k(i_t, i_{t-1}, O)\right) = 1
$$

显然进行局部归一化后，对于那些可转移状态较少的状态来说，它们转移到下一个状态的概率通常都会比那些可转移状态多的状态转到下一个状态的概率要高，因此可转移状态较少的状态更可能被算法选中。如果要解决标注偏置问题，只需取消局部归一化或者换成全局归一化即可解决。

# 最大熵马尔可夫模型代码讲解

下面给出 MEMM 的代码，具体原理自行观看上述证明。

```py frame="code" title="main.py"
from typing import List
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
train_sents = [
    ['John', 'loves', 'Mary'],
    ['Mary', 'hates', 'Bob'],
    ['Bob', 'likes', 'Alice'],
]
train_tags = [
    ['NNP', 'VBZ', 'NNP'],
    ['NNP', 'VBZ', 'NNP'],
    ['NNP', 'VBZ', 'NNP'],
]


def default_feature_extractor(sentence: List[str], i: int, prev_tag: str) -> dict:
    token = sentence[i]
    features = {}
    features[f"word={token}"] = 1
    features[f"word_lower={token.lower()}"] = 1
    if len(token) >= 3:
        features[f"suffix3={token[-3:]}"] = 1
    features[f"is_title={token[0].isupper()}"] = 1
    features[f"is_digit={token.isdigit()}"] = 1
    # 前后词
    if i > 0:
        features[f"prev_word={sentence[i-1]}"] = 1
    else:
        features["BOS"] = 1
    if i < len(sentence)-1:
        features[f"next_word={sentence[i+1]}"] = 1
    else:
        features["EOS"] = 1
    # 把前一标签也作为一个特征（MEMM 的关键点）
    features[f"prev_tag={prev_tag}"] = 1
    return features

class MEMM:
    def __init__(self, feature_extractor=default_feature_extractor, solver='lbfgs', max_iter=200):
        self.feature_extractor = feature_extractor
        self.vec = DictVectorizer(sparse=True)
        self.clf = LogisticRegression(multi_class='multinomial', solver=solver, max_iter=max_iter)
        self.label_to_index = {}
        self.index_to_label = []
        self.fitted = False

    def _gather_training_instances(self, sents: List[List[str]], tags: List[List[str]]):
        X_dicts = []; y = []
        for sent, tag_seq in zip(sents, tags):
            for i in range(len(sent)):
                prev_tag = tag_seq[i-1] if i > 0 else '<START>'
                feats = self.feature_extractor(sent, i, prev_tag)
                X_dicts.append(feats)
                y.append(tag_seq[i])
        return X_dicts, y

    # 既有观测序列也有状态序列
    def fit(self, sents: List[List[str]], tags: List[List[str]]):
        X_dicts, y = self._gather_training_instances(sents, tags)
        # 记录标签映射
        labels = sorted(set(y))
        self.index_to_label = labels
        self.label_to_index = {lab: i for i, lab in enumerate(labels)}
        # vectorize
        X = self.vec.fit_transform(X_dicts)
        y_idx = np.array([self.label_to_index[lab] for lab in y])
        # 训练分类器
        self.clf.fit(X, y_idx)
        self.fitted = True
        return self

    def _local_log_probs(self, sentence: List[str], position: int, prev_tag: str) -> np.ndarray:
        feats = self.feature_extractor(sentence, position, prev_tag)
        X = self.vec.transform([feats])
        logp = self.clf.predict_log_proba(X)[0]
        return logp

    def viterbi(self, sentence: List[str]) -> List[str]:
        assert self.fitted, "模型尚未训练，请先调用 fit()"
        n_tags = len(self.index_to_label)
        T = len(sentence)
        # dp[t, j] = 最佳路径到位置 t 且标签为 j 的对数概率
        dp = np.full((T, n_tags), -np.inf)
        backptr = np.zeros((T, n_tags), dtype=int)
        # 初始步 t=0，prev_tag = '<START>'
        for j in range(n_tags):
            cur_tag = self.index_to_label[j]
            logp = self._local_log_probs(sentence, 0, '<START>')
            dp[0, j] = logp[j]
            backptr[0, j] = -1

        # 递推
        for t in range(1, T):
            for j in range(n_tags):
                cur_tag = self.index_to_label[j]
                best_score = -np.inf
                best_prev = 0
                # 对每个可能的前一标签 i
                for i in range(n_tags):
                    prev_tag = self.index_to_label[i]
                    # 计算在 prev_tag 下转移到 cur_tag 的 log 概率
                    logp = self._local_log_probs(sentence, t, prev_tag)
                    score = dp[t-1, i] + logp[j]
                    if score > best_score:
                        best_score = score
                        best_prev = i
                dp[t, j] = best_score
                backptr[t, j] = best_prev

        # 回溯
        best_last = int(np.argmax(dp[T-1]))
        tags_idx = [best_last]
        for t in range(T-1, 0, -1):
            best_prev = backptr[t, tags_idx[-1]]
            tags_idx.append(int(best_prev))
        tags_idx.reverse()
        return [self.index_to_label[i] for i in tags_idx]

    def predict(self, sentence: List[str]) -> List[str]:
        return self.viterbi(sentence)


# 执行代码
if __name__ == '__main__':
    memm = MEMM()
    memm.fit(train_sents, train_tags)

    test = ['Alice', 'loves', 'Bob']
    print('Test sentence:', test)
    pred = memm.predict(test)
    print('Predicted tags:', pred)
```

## 学习问题

这个部分的代码可以观看[上面的讲解](#学习问题)对照学习。

```py showLineNumbers
def default_feature_extractor(sentence: List[str], i: int, prev_tag: str) -> dict:
    token = sentence[i]
    features = {}
    features[f"word={token}"] = 1
    features[f"word_lower={token.lower()}"] = 1
    if len(token) >= 3:
        features[f"suffix3={token[-3:]}"] = 1
    features[f"is_title={token[0].isupper()}"] = 1
    features[f"is_digit={token.isdigit()}"] = 1
    # 前后词
    if i > 0:
        features[f"prev_word={sentence[i-1]}"] = 1
    else:
        features["BOS"] = 1
    if i < len(sentence)-1:
        features[f"next_word={sentence[i+1]}"] = 1
    else:
        features["EOS"] = 1
    # 把前一标签也作为一个特征（MEMM 的关键点）
    features[f"prev_tag={prev_tag}"] = 1
    return features

def _gather_training_instances(self, sents: List[List[str]], tags: List[List[str]]):
    X_dicts = []; y = []
    for sent, tag_seq in zip(sents, tags):
        for i in range(len(sent)):
            prev_tag = tag_seq[i-1] if i > 0 else '<START>'
            feats = self.feature_extractor(sent, i, prev_tag)
            X_dicts.append(feats)
            y.append(tag_seq[i])
    return X_dicts, y

# 既有观测序列也有状态序列
def fit(self, sents: List[List[str]], tags: List[List[str]]):
    X_dicts, y = self._gather_training_instances(sents, tags)
    # 记录标签映射
    labels = sorted(set(y))
    self.index_to_label = labels
    self.label_to_index = {lab: i for i, lab in enumerate(labels)}
    # vectorize
    X = self.vec.fit_transform(X_dicts)
    y_idx = np.array([self.label_to_index[lab] for lab in y])
    # 训练分类器
    self.clf.fit(X, y_idx)
    self.fitted = True
    return self
```

## 预测问题

这个部分的代码可以观看[上面的讲解](#预测问题)对照学习。

```py showLineNumbers
def _local_log_probs(self, sentence: List[str], position: int, prev_tag: str) -> np.ndarray:
    feats = self.feature_extractor(sentence, position, prev_tag)
    X = self.vec.transform([feats])
    logp = self.clf.predict_log_proba(X)[0]
    return logp

def viterbi(self, sentence: List[str]) -> List[str]:
    assert self.fitted, "模型尚未训练，请先调用 fit()"
    n_tags = len(self.index_to_label)
    T = len(sentence)
    # dp[t, j] = 最佳路径到位置 t 且标签为 j 的对数概率
    dp = np.full((T, n_tags), -np.inf)
    backptr = np.zeros((T, n_tags), dtype=int)
    # 初始步 t=0，prev_tag = '<START>'
    for j in range(n_tags):
        cur_tag = self.index_to_label[j]
        logp = self._local_log_probs(sentence, 0, '<START>')
        dp[0, j] = logp[j]
        backptr[0, j] = -1

    # 递推
    for t in range(1, T):
        for j in range(n_tags):
            cur_tag = self.index_to_label[j]
            best_score = -np.inf
            best_prev = 0
            # 对每个可能的前一标签 i
            for i in range(n_tags):
                prev_tag = self.index_to_label[i]
                # 计算在 prev_tag 下转移到 cur_tag 的 log 概率
                logp = self._local_log_probs(sentence, t, prev_tag)
                score = dp[t-1, i] + logp[j]
                if score > best_score:
                    best_score = score
                    best_prev = i
            dp[t, j] = best_score
            backptr[t, j] = best_prev

    # 回溯
    best_last = int(np.argmax(dp[T-1]))
    tags_idx = [best_last]
    for t in range(T-1, 0, -1):
        best_prev = backptr[t, tags_idx[-1]]
        tags_idx.append(int(best_prev))
    tags_idx.reverse()
    return [self.index_to_label[i] for i in tags_idx]

def predict(self, sentence: List[str]) -> List[str]:
    return self.viterbi(sentence)
```

# 深层问题思考

1. 为什么最大熵模型最大化的是条件熵？

    问题引用自该话题：[最大熵模型，为什么最大的是条件熵？](https://www.zhihu.com/question/35295907)

    最大熵原理的目标是选择一个 **不做额外假设、不偏不倚** 的模型，在给定已知条件下，保留最大的不确定性。

    最大熵模型的核心是让模型在已知输入 $X$ 的条件下，尽可能保持 **最大的不确定性** 。这就意味着，给定输入 $X$ ，我们不希望模型对输出 $Y$ 做出过于确定的猜测，除非有足够的证据支持某些标签。

    条件熵 $H(Y|X)$ 衡量的是：在给定 $X$ 的条件下， $Y$ 的不确定性。通过最大化条件熵，我们实际上是在 **最大化所有可能输出 $Y$ 的不确定性** ，并且通过约束条件来确保它符合训练数据中的真实模式。

    最大化条件熵能保证我们选择的模型在已知信息的条件下保持最小的偏向性，从而避免引入不必要的假设。

# 参考文献

## 最大熵模型

1. [最大熵模型原理小结](https://www.cnblogs.com/pinard/p/6093948.html)

2. [【maxENT】最大熵模型（Maximum Entropy Model）介绍与使用](https://blog.csdn.net/weixin_43764974/article/details/147196896)

3. [最大熵模型 Maximum Entropy Model](https://www.cnblogs.com/ooon/p/5677098.html)

4. [最大熵模型-Max Entropy Model](https://zhuanlan.zhihu.com/p/136710858)

5. [最大熵模型（Maximum Entropy Model, MaxEnt）](https://zhuanlan.zhihu.com/p/717650932)

6. [机器学习——最大熵模型](https://www.cnblogs.com/BlairGrowing/p/14906291.html)

7. [最大熵模型](https://blog.csdn.net/qq_47190374/article/details/136971135)

## 最大熵马尔可夫模型

1. [最大熵模型（ME）和最大熵马尔可夫模型（MEMM）](https://blog.csdn.net/sinat_34072381/article/details/107279644)

2. [最大熵马尔可夫模型（MEMM）及其三个基本问题](https://sm1les.com/2019/07/26/maximum-entropy-markov-model/)

3. [最大熵模型（ME）和最大熵马尔可夫模型（MEMM）](https://blog.csdn.net/sinat_34072381/article/details/107279644)

4. [最大熵模型（Maximum Entropy Model, MaxEnt）](https://zhuanlan.zhihu.com/p/717650932)

5. [最大熵马尔可夫模型](https://zhuanlan.zhihu.com/p/113187662)

6. [序列标注：从HMM、MEMM到CRF](https://allenwind.github.io/blog/13551)

7. [概率图模型系列（4）：MEMM](https://allenwind.github.io/blog/7694)

8. [【归纳综述】马尔可夫、隐马尔可夫 HMM 、条件随机场 CRF](https://zhuanlan.zhihu.com/p/259660645)