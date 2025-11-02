---
title: 【机器学习基本模型】第八节：最大熵马尔可夫模型
published: 2025-11-02
description: 介绍机器学习常见的算法模型
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

![最大熵马尔可夫模型图像](src\content\posts\maximum-entropy-markov-model\最大熵马尔可夫模型1.jpg)

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

在最大熵模型中，我们通过一组特征函数 $f(x,y)$ 描述输入 $x$ 和输出 $y$ 之间的关系：

$$
f(x,y) = 
\begin{cases} 
1 & \text{if certain condition between } x \text{ and } y \text{ holds} \\
0 & \text{otherwise}
\end{cases}
$$

每个特征函数对应一个可能的关系（或约束），不同的训练样本可能激活不同的特征函数。同一个样本也可能激活多个特征函数。

特征函数 $f(x,y)$ 关于经验分布 $\bar{P}(X, Y)$ 的期望值，用 $\mathbb{E}_{\bar{P}}\big[ f \big]$ 表示:

$$
\mathbb{E}_{\bar{P}}\big[ f \big] = \sum_{x, y} \bar{P}(x, y)f(x, y) = \frac{1}{N} \sum_{x, y} f(x, y)
$$

由于特征函数是对建立概率模型有益的特征，所以应该让 MaxEnt 模型来满足这一约束，所以模型 $P(Y|X)$ 关于函数 $f$ 的期望应该等于经验分布关于 $f$ 的期望，模型 $P(Y|X)$ 关于 $f$ 的期望为：

$$
\mathbb{E}_{P}\big[ f \big] = \sum_{x, y} P(x, y)f(x, y) ≈ \sum_{x, y} \bar{P}(x)P(y|x)f(x, y)
$$

经验分布与特征函数结合便能代表概率模型需要满足的约束，只需让 $\mathbb{E}_{\bar{P}}\big[ f \big] = \mathbb{E}_{P}\big[ f \big]$ ：

$$
\sum_{x, y} \bar{P}(x)P(y|x)f(x, y) = \sum_{x, y} \bar{P}(x, y)f(x, y)
$$

上式便为 MaxEnt 中需要满足的约束，给定 $n$ 个特征函数 $f_i(x, y)$ ，则有 $n$ 个约束条件，用 $C$ 表示满足约束的模型集合：

$$
C = \{ P|\mathbb{E}_{P}(f_i) = \mathbb{E}_{\bar{P}}(_i), I = 1, 2, \ldots, n \}
$$

从满足约束的模型集合 $C$ 中找到使得 $P(Y|X)$ 的熵最大的即为 MaxEnt 模型了。

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
\min_{P \in C} \sum_{x,y} \bar{P}(x) P(y|x) \log P(y|x)
$$

$$
\begin{align*}
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

将 $P_w(y|x)$ 带入上述公式可得：

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

$O$ 是长度为 $T$ 的观测序列， $I$ 是对应的状态序列：

$$
O = \{ o_1, o_2, \ldots, o_T \}, I = \{ i_1, i_2, \ldots, i_T \}
$$

在已知观测序列 $O$ 的条件下，状态序列为 $I$ 的概率为：

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



# 最大熵马尔可夫模型代码讲解



# 深层问题思考



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