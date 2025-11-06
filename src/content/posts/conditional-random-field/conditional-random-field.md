---
title: 【机器学习基本模型】第九节：条件随机场
published: 2025-11-05
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

> 写在前面：本篇延续上一篇的 MEMM 进行拓展，CRF 本质上就是为了解决 MEMM 的痛点而产生的。还有要补充的是：虽然 CRF 来源于 MRF（CRF 本质上是条件化后的 MRF），但理解 CRF 并不需要完全了解 MRF 是什么。因此本篇博客不会介绍 MRF 的相关知识，具体会在后续的算法篇进行介绍。

# 条件随机场基本原理

由于 MEMM 存在标注偏置问题，为此 Lafferty J、 Mccallum A 和 Pereira F C N 三人在 2001 年提出了一种 **线性链条件随机场** （Conditional Random Fields，简称 CRF）模型，该模型拥有 MEMM 的所有优点，同时还 **不存在标注偏置问题** 。条件随机场的一般定义如下：

设 $X$ 与 $Y$ 是随机变量， $P(Y|X)$ 是在给定 $X$ 的条件下 $Y$ 的条件概率分布。若随机变量 $Y$ 构成一个由无向图 $G = (V, E)$ 表示的马尔可夫随机场，即 $P(Y_v \mid X, Y_w, w \neq v) = P(Y_v \mid X, Y_w, w \sim v)$ 对任意结点 $v$ 成立，则称条件概率分布 $P(Y|X)$ 为条件随机场。

式中 $w \sim v$ 表示在图 $G = (V, E)$ 中与结点 $v$ 有边连接的所有结点 $w$ ， $w \neq v$ 表示结点 $v$ 以外的所有结点， $Y_v$ 、 $Y_w$ 为结点 $v$ 、 $w$ 对应的随机变量。

在条件随机场的一般定义中并没有要求 $X$ 和 $Y$ 具有相同的图结构，但是实际运用中一般假设 $X$ 和 $Y$ 具有相同的图结构，并且线性链条件随机场也同样作此假设。线性链条件随机场的定义如下：

![条件随机场图像](src\content\posts\conditional-random-field\条件随机场1.png)

## 基本形式定义

设 $X = (x_1, x_2, \ldots, x_n)$ 和 $Y = (y_1, y_2, \ldots, y_n)$ 均为线性链表示的随机变量序列，若在给定随机量序列 $X$ 的条件下，随机变量序列 $Y$ 的条件概率分布 $P(Y|X)$ 构成条件随机场，即满足马尔可夫性（在 $i = 1$ 和 $n$ 时只考虑单边）：

$$
P(y_i \mid X, y_1, \cdots, y_{i-1}, y_{i+1}, \cdots, y_n) = P(y_i \mid X, y_{i-1}, y_{i+1}) \quad i = 1, 2, \ldots, n
$$

则称 $P(Y|X)$ 为线性链条件随机场。线性链条件随机场通常用来对序列标注问题进行建模，在序列标注问题中， $X$ 可以看作 **观测序列** ， $Y$ 可以看做对应的 **状态序列** 。

根据线性链条件随机场的定义可知，此时由 $Y$ 构成的马尔可夫随机场的最大团为相邻两个结点的集合，那么由 Hammersley-Clifford 定理可知，线性链条件随机场 $P(Y|X)$ 的表达式可以写为如下形式：

$$
P(Y|X) = \frac{1}{Z(X)} \exp \left( \sum_{i,k} \lambda_k t_k(y_{i-1}, y_i, X, i) + \sum_{i,l} \mu_i s_l(y_i, X, i) \right)
$$

$$
Z(X) = \sum_Y \exp \left( \sum_{i,k} \lambda_k t_k(y_{i-1}, y_i, X, i) + \sum_{i,l} \mu_l s_l(y_i, X, i) \right)
$$

其中 $Z(X)$ 是 **规范化因子** ，求和是在所有可能的输出序列上进行的。 $t_k$ 是定义在边上的特征函数，称为 **转移特征** ，依赖于当前和前一个位置； $s_l$ 是定义在结点上的特征函数，称为 **状态特征** ，依赖于当前位置。 $t_k$ 和 $s_l$ 都依赖于位置，是 **局部特征函数** 。线性链条件随机场完全由特征函数 $t_k$ 、 $s_l$ 和对应的权值 $\lambda_k$ 、 $\mu_i$ 确定（通常特征函数是事先人为设定好的超参数，而权值则是通过学习得到）。

观察上式易知：线性链条件随机场为判别式模型，同时也实现了用特征对观测序列参数化，而且状态转移概率采用的是全局归一化来计算。所以线性链条件随机场拥有 MEMM 的所有优点，而且还不存在标注偏置问题。

## 向量形式定义

根据特征函数的性质可知，状态特征函数 $s_l$ 可以看做是只提取当前位置特征的转移特征函数，即 $s_l(y_i, X, i) = s_l(y_{i - 1}, X, i)$ 。因此 $P(X|Y)$ 表达式中的转移特征和状态特征及其权值可以用统一的符号表示。不妨设有 $K_1$ 个转移特征， $K_2$ 个状态特征，则 $K = K_1 + K_2$ 。若序列长度为 $n$ ，则 $P(Y|X)$ 可以简写为：

$$
\begin{align*}
P(Y|X) &= \frac{1}{Z(X)} \exp \left( \sum_{i,k} \lambda_k t_k(y_{i-1}, y_i, X, i) + \sum_{i,l} \mu_i s_l(y_i, X, i) \right) \\
&= \frac{1}{Z(X)} \exp \left( \sum_i \sum_{k=1}^{K_1} \lambda_k t_k(y_{i-1}, y_i, X, i) + \sum_i \sum_{l=1}^{K_2} \mu_i s_l(y_i, X, i) \right) \\
&= \frac{1}{Z(X)} \exp \left( \sum_i \sum_{k=1}^{K_1} \lambda_k t_k(y_{i-1}, y_i, X, i) + \sum_i \sum_{l=1}^{K_2} \mu_i s_l(y_{i-1}, y_i, X, i) \right) \\
&= \frac{1}{Z(X)} \exp \left( \sum_i \sum_{k=1}^{K_1+K_2} w_k f_k(y_{i-1}, y_i, X, i) \right) \\
&= \frac{1}{Z(X)} \exp \left( \sum_i \sum_{k=1}^{K} w_k f_k(y_{i-1}, y_i, X, i) \right)
\end{align*}
$$

不妨设：

$$
f_k(Y, X) = \sum_i f_k(y_{i-1}, y_i, X, i) \quad k = 1, 2, \ldots, K
$$

$$
F(Y, X) = (f_1(Y, X), f_2(Y, X), \ldots, f_K(Y, X)) \in \mathbb{R}^{K \times 1}
$$

$$
w = (w_1, w_2, \ldots, w_k) \in \mathbb{R}^{K \times 1}
$$

那么 $P(Y|X)$ 可以进一步简写为如下向量化形式：

$$
\begin{align*}
P(Y|X) &= \frac{1}{Z(X)} \exp \left( \sum_i \sum_{k=1}^K w_k f_k(y_{i-1}, y_i, X, i) \right) \\
&= \frac{1}{Z(X)} \exp \left( \sum_{k=1}^K w_k \sum_i f_k(y_{i-1}, y_i, X, i) \right) \\
&= \frac{\exp(w^{\rm T} F(Y, X))}{Z(X)}
\end{align*}
$$

$$
\text{where } Z(X) = \sum_Y \exp(w^{\rm T} F(Y, X))
$$

# 条件随机场实现难点

与前面两个模型一样，要想构建出 CRF，就必须解决以下三个问题：

- 计算问题：在给定模型参数 $w_k(k = 1, 2, \ldots, K)$ 、观测序列 $X = (x_1, x_2, \ldots, x_n)$ 和状态序列 $Y = (y_1, y_2, \ldots, y_n)$ 的条件下，计算条件概率 $P(Y|X)$ 、 $P(y_i, X)$ 和 $P(y_{i-1}, y_i|X)$ 以及一些数学期望

- 学习问题：在给定观测序列 $X = (x_1, x_2, \ldots, x_n)$ 和状态序列 $Y = (y_1, y_2, \ldots, y_n)$ 的条件下，估计模型参数 $w_k(k = 1, 2, \ldots, K)$ ，使得条件概率 $P(Y|X)$ 达到最大

- 预测问题：已知模型参数 $w_k(k = 1, 2, \ldots, K)$ 和观测序列 $X = (x_1, x_2, \ldots, x_n)$ ，求条件概率 $P(Y|X)$ 达到最大的状态序列 $Y = (y_1, y_2, \ldots, y_n)$ ，即给定观测序列，求最有可能的对应状态序列

下面就详细讲解一下这三个问题的解决方案。

## 计算问题

### 计算条件概率

1. 由 $P(Y|X)$ 的表达式可知，要想计算出条件概率 $P(Y|X)$ 则需要计算出给定状态序列 $Y$ 的非规范化概率 $exp(w^{\rm T}F(Y, X))$ 和规范化因子 $Z(X)$ ，由于在已知观测序列 $X$ 和模型参数 $w_k(k = 1, 2, \ldots, K)$ 的条件下，只要知道状态的取值范围，无论对应状态序列 $Y$ 是否已知，均能求出规范化因子 $Z(X)$ 。

所以下面考虑对 $exp(w^{\rm T}F(Y, X))$ 和 $Z(X)$ 分别进行求解。

- 首先考虑求解 $Z(X)$ ：

设状态的取值范围为 $Q = \{ q_1, q_2, \ldots, q_m \}$ ，将所有状态序列前后都各填充一个 $y_0 = start$ 和 $y_{n+1} = stop$ 。对观测序列 $X$ 的每一个位置 $i = 1, 2, \ldots, n+1$ 来说， $y_{i-1}$ 和 $y_i$ 都有 $m$ 种可能的取值，因此，对于每一个位置来说都可以定义一个 $m \times m$ 的 **转移势矩阵** ：

$$
\mathbf{M}_i(X) = \Big[ M_i(y_{i-1}, y_i | X) \Big] = \begin{bmatrix}
M_1(q_1, q_1 | X) & M_1(q_1, q_2 | X) & \ldots & M_1(q_1, q_m | X) \\
M_1(q_2, q_1 | X) & M_1(q_2, q_2 | X) & \ldots & M_1(q_2, q_m | X) \\
\vdots & \vdots & \ddots & \vdots \\
M_1(q_m, q_1 | X) & M_1(q_m, q_2 | X) & \ldots & M_1(q_m, q_m | X)
\end{bmatrix}
$$

$$
\text{where } M_i(y_{i-1}, y_i | X) = \exp \left( \sum_{k=1}^{K} w_k f_k(y_{i-1}, y_i, X, i) \right)
$$

特别地，对于起始位置 $i = 1$ 和结束位置 $i = n + 1$ 的矩阵定义为（确保初始位置和结尾位置的状态是确定的）：

$$
\mathbf{M}_1(X) = \Big[ M_1(y_0, y_1 | X) \Big] = 
\begin{bmatrix}
M_1(start, q_1 | X) & M_1(start, q_2 | X) & \ldots & M_1(start, q_m | X) \\
0 & 0 & \ldots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \ldots & 0
\end{bmatrix}
$$

$$
\mathbf{M}_{n+1}(X) = \Big[ M_{n+1}(y_n, y_{n+1} | X) \Big] = 
\begin{bmatrix}
M_{n+1}(q_1, stop | X) = 1 & 0 & \ldots & 0 \\
M_{n+1}(q_2, stop | X) = 1 & 0 & \ldots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
M_{n+1}(q_m, stop | X) = 1 & 0 & \ldots & 0
\end{bmatrix}
$$

此时 $Z(X)$ 为 $\mathbf{M}_i(X)$ 这 $n+1$ 个矩阵的乘积的第 1 行第 1 列元素：

$$
Z(X) = \left[ \prod_{i=1}^{n+1} \mathbf{M}_i(X) \right]_{(1,1)}
$$

根据矩阵相乘的性质，所有 $\mathbf{M}_i(X)$ 相乘的最终结果就是初始位置的状态到结尾位置的状态的所有路径的权重之积再求和。因此 $Z(X)$ 的表达式为 $n+1$ 个矩阵的乘积的第 1 行第 1 列元素。

- 然后考虑 $exp(w^{\rm T}F(Y, X))$ ：

在对应状态序列 $Y$ 也已知的条件下，则可以通过 $M_i(X)$ 这 $n+1$ 个矩阵的适当元素的乘积来表示：

$$
\begin{align*}
\exp(w^{\rm T} F(Y, X)) &= \exp \left( \sum_{k=1}^K w_k \sum_{i=1}^{n+1} f_k(y_{i-1}, y_i, X, i) \right) \\
&= \exp \left( \sum_{i=1}^{n+1} \sum_{k=1}^K w_k f_k(y_{i-1}, y_i, X, i) \right) \\
&= \prod_{i=1}^{n+1} \exp \left( \sum_{k=1}^K w_k f_k(y_{i-1}, y_i, X, i) \right) \\
&= \prod_{i=1}^{n+1} M_i(y_{i-1}, y_i | X)
\end{align*}
$$

首先我们要知道的是，非规范化概率在概率图中表示的是一个具体的路径。所以 $exp(w^{\rm T}F(Y, X))$ 的表达式自然是上面这个公式。

2. 首先我们来定义一下前/后向向量（与 HMM 的前/后向概率相似，这里给出的是向量形式）

对每个位置 $i = 1, 2, \ldots, n+1$ 定义前向向量 $\boldsymbol{\alpha}_i(X) \in \mathbb{R}^{m \times 1}$ ：

$$
\boldsymbol{\alpha}_0(X) = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix} \quad \boldsymbol{\alpha}_i(X) = \begin{bmatrix} \alpha_i(y_i = q_1 | X) \\ \alpha_i(y_i = q_2 | X) \\ \vdots \\ \alpha_i(y_i = q_m | X) \end{bmatrix}
$$

其中 $\alpha_i(y_i = q_j|X)(j = 1, 2, \ldots, m)$ 表示在位置 $i$ 的状态是 $q_j$ 并且从 1 到 $i$ 的状态序列的非规范化概率。根据前向向量的定义易得递推公式：

$$
\boldsymbol{\alpha}_i(X)^{\rm T} = \boldsymbol{\alpha}_{i-1}(X)^{\rm T} \Big[ M_i(y_{i-1}, y_i | X) \Big] = \boldsymbol{\alpha}_{i-1}(X)^{\rm T} \mathbf{M}_i(X)
$$

同理，对每个位置 $i = 1, 2, \ldots, n+1$ 定义后向向量 $\boldsymbol{\beta}_i(x) \in \mathbb{R}^{m \times 1}$

$$
\boldsymbol{\beta}_i(X) = \begin{bmatrix} \beta_i(y_i = q_1 | X) \\ \beta_i(y_i = q_2 | X) \\ \vdots \\ \beta_i(y_i = q_m | X) \end{bmatrix}, \quad \boldsymbol{\beta}_{n+1}(X) = \begin{bmatrix} 1 \\ 0 \\ \vdots \\ 0 \end{bmatrix}
$$

其中 $\beta_i(y_i = q_j|X)(j = 1, 2, \ldots, m)$ 表示在位置 $i$ 的状态是 $q_j$ 并且从 $i+1$ 到最后的状态序列的非规范化概率。根据后向向量的定义易得递推公式：

$$
\boldsymbol{\beta}_i(X) = \Big[ M_{i+1}(y_i, y_{i+1} | X) \Big] \boldsymbol{\beta}_{i+1}(X) = \mathbf{M}_i(X) \boldsymbol{\beta}_{i+1}(X)
$$

定义完前向向量和后向向量，接下来便可以很容易地计算出在位置 $i$ 的状态是 $q_j$ 的条件概率和在位置 $i-1$ 是状态 $q_j$ 且在位置 $i$ 是状态 $q_k$ 的条件概率：

$$
P(y_i | X) = P(y_i = q_j | X) = \frac{\alpha_i(y_i = q_j | X) \beta_i(y_i = q_j | X)}{Z(X)}
$$

$$
P(y_{i-1}, y_i | X) = P(y_{i-1} = q_j, y_i = q_k | X) = \frac{\alpha_{i-1}(y_{i-1} = q_j | X) M_i(q_j, q_k | X) \beta_i(y_i = q_k | X)}{Z(X)}
$$

$$
\text{where } Z(X) = \boldsymbol{\alpha}_n(X)^{\rm T} \mathbf{I} = \boldsymbol{\alpha}_{n+1}(X)^{\rm T} \mathbf{I} = \mathbf{I}^{\rm T} \boldsymbol{\beta}_0(X) \quad \mathbf{I} = (1, \ldots, 1) \in \mathbb{R}^{m \times 1}
$$

### 计算期望值

利用前面定义的前向向量和后向向量，可以计算特征函数关于联合分布 $P(X, Y)$ 和条件分布 $P(Y|X)$ 的数学期望。

- 特征函数 $f_k(Y, X) = \sum_{i=1}^{n}f_k(y_{i-1}, y_i, X, i)$ 关于条件分布 $P(Y|X)$ 的数学期望是：

$$
\begin{align*}
&\mathbb{E}_{P(Y|X)} \Big[ f_k(Y, X) \Big] \\
= &\sum_Y P(Y|X) f_k(Y, X) = \sum_Y \left[ P(Y|X) \sum_{i=1}^{n+1} f_k(y_{i-1}, y_i, X, i) \right] \\
= &\sum_Y \sum_{i=1}^{n+1} P(Y|X) f_k(y_{i-1}, y_i, X, i) = \sum_{i=1}^{n+1} \sum_Y P(Y|X) f_k(y_{i-1}, y_i, X, i) \\
= &\sum_{i=1}^{n+1} \sum_{j=1}^m \sum_{k=1}^m \Big[ f_k(y_{i-1} = q_j, y_i = q_k, X, i) P(y_{i-1} = q_j, y_i = q_k | X) \Big] \\
= &\sum_{i=1}^{n+1} \sum_{j=1}^m \sum_{k=1}^m \left[ f_k(y_{i-1} = q_j, y_i = q_k, X, i) \cdot \frac{\alpha_{i-1}(y_{i-1} = q_j | X) \, M_i(q_j, q_k | X) \, \beta_i(y_i = q_k | X)}{Z(X)} \right]
\end{align*}
$$

$$
\text{where } Z(X) = \boldsymbol{\alpha}_n(X)^{\rm T} \mathbf{I} = \boldsymbol{\alpha}_{n+1}(X)^{\rm T} \mathbf{I} = \mathbf{I}^{\rm T} \boldsymbol{\beta}_0(X) \quad \mathbf{I} = (1, \ldots, 1) \in \mathbb{R}^{m \times 1}
$$

- 假设经验分布为 $\bar{P}(X)$ ，则特征函数 $f_k(Y, X) = \sum_{i=1}^{n}f_k(y_{i-1}, y_i, X, i)$ 关于联合分布 $P(X, Y)$ 的数学期望是：

$$
\begin{align*}
&\mathbb{E}_{P(X,Y)} \Big[ f_k(Y, X) \Big] \\ 
= &\sum_{X,Y} P(X,Y) f_k(Y, X) = \sum_{X,Y} \bar{P}(X) P(Y|X) f_k(Y, X) \\
= &\sum_X \bar{P}(X) \sum_Y P(Y|X) f_k(Y, X) = \sum_X \bar{P}(X) \mathbb{E}_{P(Y|X)} \Big[ f_k(Y, X) \Big]
\end{align*}
$$

综上，对于在给定模型参数 $w_k(k = 1, 2, \ldots, K)$ 、观测序列 $X = (x_1, x_2, \ldots, x_n)$ 和状态序列 $Y = (y_1, y_2, \ldots, y_n)$ 的条件下，只需前向扫描计算和后向扫描计算一次 $\boldsymbol{\alpha}_i(X)$ 和 $\boldsymbol{\beta}_i(X)$ ，规范化因子 $Z(X)$ 和条件概率 $P(y_i|X)$ 、 $P(y_{i-1}, y_i|X)$ 以及一些数学期望都可以被计算出来。

## 学习问题

在给定观测序列 $X = (x_1, x_2, \ldots, x_n)$ 和对应状态序列 $Y = (y_1, y_2, \ldots, y_n)$ 的条件下，可以通过极大似然估计法来估计模型的参数。由于线性链条件随机场类似于最大熵模型，所以用于求解最大熵模型参数的 GIS、IIS、梯度下降、牛顿法和拟牛顿法均可用于线性链条件随机场。

## 预测问题

线性链条件随机场的预测问题是在给定模型参数 $w_k(k = 1, 2, \ldots, K)$ 、观测序列 $X = (x_1, x_2, \ldots, x_n)$ 的条件下，求条件概率最大的状态序列 $Y^* = (y_1^*, y_2^*, \ldots, y_n^*)$ ，即对观测序列进行标注。线性链条件随机场解决预测问题所采用的算法和 HMM 和 MEMM 一样，采用的都是经典的 Viterbi 算法。具体如下：

$$
\begin{align*}
Y^* &= \arg\max_Y P(Y|X) \\
&= \arg\max_Y \frac{\exp(\boldsymbol{w}^T F(Y, X))}{Z(X)} \\
&= \arg\max_Y \exp(\boldsymbol{w}^T F(Y, X)) \\
&= \arg\max_Y (\boldsymbol{w}^T F(Y, X))
\end{align*}
$$

于是，线性链条件随机场的预测问题转化为了求非规范化概率最大的最优路径问题，其中路径表示的是状态序列。为了求解最优路径，将上式作如下恒等变形：

$$
\begin{align*}
Y^* &= \arg\max_Y  \boldsymbol{w}^T F(Y, X) \\
&= \arg\max_Y \sum_{k=1}^K w_k \sum_i f_k(y_{i-1}, y_i, X, i) \\
&= \arg\max_Y \sum_i \sum_{k=1}^K w_k f_k(y_{i-1}, y_i, X, i) \\
&= \arg\max_Y \sum_i \boldsymbol{w}^T F_i(y_{i-1}, y_i, X)
\end{align*}
$$

$$
\text{where } F_i(y_{i-1}, y_i, X) = (f_1(y_{i-1}, y_i, X, i), f_2(y_{i-1}, y_i, X, i), \ldots, f_K(y_{i-1}, y_i, X, i)) \in \mathbb{R}^{K \times 1}
$$

首先求出位置 1 的各个标记 $y_1 = q_1, q_2, \ldots, q_m$ 的非规范化概率：

$$
\delta_1(j) = w^{\rm T} F_1(y_0 = start, y_1 = q_j, X) \quad j = 1, 2, \ldots, m
$$

接着由递推公式，求出到位置 $i$ 的各个标记 $l = 1, 2, \ldots, m$ 的非规范化概率的最大值，同时记录非规范化概率最大值的路径：

$$
\delta_i(l) = \max_{1 \leq j \leq m} \left\{ \delta_{i-1}(j) + w^{\rm T} F_i(y_{i-1} = q_j, y_i = q_l, X) \right\} \quad l = 1, 2, \ldots, m
$$

$$
\Psi_i(l) = \arg\max_{1 \leq j \leq m} \left\{ \delta_{i-1}(j) + w^{\rm T} F_i(y_{i-1} = q_j, y_i = q_l, X) \right\} \quad l = 1, 2, \ldots, m
$$

直到 $i = n$ 时终止，此时求得的非规范化概率的最大值为：

$$
\max_Y w^{\rm T} F(Y, X) = \max_{1 \leq j \leq m} \delta_n(j)
$$

最优路径的终点为：

$$
y_n^* = \arg\max_{1 \leq j \leq m} \delta_n(j)
$$

接着从最优路径的终点回溯即可求得最优路径。

# 条件随机场代码讲解

下面给出 CRF 的代码，具体原理自行观看上述证明。

```py frame="code" title="main.py"
import numpy as np
from collections import defaultdict
train_data = [
    (['The', 'capital', 'of', 'France'], ['B-LOC', 'O', 'O', 'B-LOC']),
    (['The', 'president', 'of', 'USA'], ['B-LOC', 'O', 'O', 'B-LOC']),
    (['I', 'love', 'Paris'], ['O', 'O', 'B-LOC'])
]


# 特征提取函数
def extract_features(sentence, index):
    features = {
        'word': sentence[index],
        'is_capitalized': sentence[index][0].isupper(),
        'is_digit': sentence[index].isdigit(),
        'word[-3:]': sentence[index][-3:],
    }
    # 上一个词
    if index > 0:
        features['prev_word'] = sentence[index - 1]
    # 下一个词
    if index < len(sentence) - 1:
        features['next_word'] = sentence[index + 1]
    return features

class CRF:
    def __init__(self):
        self.weights = defaultdict(float)
        self.transition_weights = defaultdict(float)
    
    def _features_to_key(self, features):
        return tuple(sorted(features.items()))
    
    def _get_feature_score(self, features):
        feature_key = self._features_to_key(features)
        return self.weights.get(feature_key, 0)

    def train(self, data, epochs=10, learning_rate=0.1):
        for epoch in range(epochs):
            for sentence, labels in data:
                # 计算每个单词的特征和标签得分
                for i in range(len(sentence)):
                    features = extract_features(sentence, i)
                    feature_score = self._get_feature_score(features)
                    feature_key = self._features_to_key(features)
                    # 计算特征的得分并更新权重
                    self.weights[feature_key] += learning_rate
                # 更新转移权重
                for i in range(1, len(labels)):
                    transition_key = (labels[i-1], labels[i])
                    self.transition_weights[transition_key] += learning_rate
            # 打印当前轮次的训练进度
            print(f'Epoch {epoch + 1} complete.')

    def viterbi_decode(self, sentence):
        n = len(sentence)
        dp = np.zeros((n, len(self.transition_weights)))
        backpointer = np.zeros((n, len(self.transition_weights)), dtype=int)
        # 初始化第一列：根据特征和初始转移权重
        for i in range(len(self.transition_weights)):
            features = extract_features(sentence, 0)
            dp[0][i] = self._get_feature_score(features) + self.transition_weights.get(('<START>', i), 0)
        # 动态规划：计算每个位置的最优标签路径
        for i in range(1, n):
            for j in range(len(self.transition_weights)):
                max_score = -float('inf')
                max_index = -1
                for k in range(len(self.transition_weights)):
                    features = extract_features(sentence, i)
                    score = dp[i-1][k] + self.transition_weights.get((k, j), 0) + self._get_feature_score(features)
                    if score > max_score:
                        max_score = score
                        max_index = k
                dp[i][j] = max_score
                backpointer[i][j] = max_index
        # 回溯：找到最优标签序列
        best_path = []
        best_state = np.argmax(dp[n-1])
        best_path.append(best_state)
        for i in range(n-2, -1, -1):
            best_state = backpointer[i+1][best_state]
            best_path.insert(0, best_state)
        return best_path

    def predict(self, sentence):
        predictions = []
        for i in range(len(sentence)):
            features = extract_features(sentence, i)
            score = self._get_feature_score(features)
            predictions.append(score)
        return predictions


# 执行代码
if __name__ == "__main__":
    crf_model = CRF()
    crf_model.train(train_data, epochs=10)

    test_sentence = ['I', 'love', 'Paris']
    predictions = crf_model.predict(test_sentence)
    print(f'Predictions: {predictions}')

    # 使用 Viterbi 解码获取标签序列
    best_path = crf_model.viterbi_decode(test_sentence)
    print(f'Predicted path (labels): {best_path}')
```

## 学习问题

这个部分的代码可以观看[上面的讲解](#学习问题)对照学习。

```py showLineNumbers
def _features_to_key(self, features):
    return tuple(sorted(features.items()))

def _get_feature_score(self, features):
    feature_key = self._features_to_key(features)
    return self.weights.get(feature_key, 0)

def train(self, data, epochs=10, learning_rate=0.1):
    for epoch in range(epochs):
        for sentence, labels in data:
            # 计算每个单词的特征和标签得分
            for i in range(len(sentence)):
                features = extract_features(sentence, i)
                feature_score = self._get_feature_score(features)
                feature_key = self._features_to_key(features)
                # 计算特征的得分并更新权重
                self.weights[feature_key] += learning_rate
            # 更新转移权重
            for i in range(1, len(labels)):
                transition_key = (labels[i-1], labels[i])
                self.transition_weights[transition_key] += learning_rate
        # 打印当前轮次的训练进度
        print(f'Epoch {epoch + 1} complete.')
```

## 预测问题

这个部分的代码可以观看[上面的讲解](#预测问题)对照学习。

```py showLineNumbers
def viterbi_decode(self, sentence):
    n = len(sentence)
    dp = np.zeros((n, len(self.transition_weights)))
    backpointer = np.zeros((n, len(self.transition_weights)), dtype=int)
    # 初始化第一列：根据特征和初始转移权重
    for i in range(len(self.transition_weights)):
        features = extract_features(sentence, 0)
        dp[0][i] = self._get_feature_score(features) + self.transition_weights.get(('<START>', i), 0)
    # 动态规划：计算每个位置的最优标签路径
    for i in range(1, n):
        for j in range(len(self.transition_weights)):
            max_score = -float('inf')
            max_index = -1
            for k in range(len(self.transition_weights)):
                features = extract_features(sentence, i)
                score = dp[i-1][k] + self.transition_weights.get((k, j), 0) + self._get_feature_score(features)
                if score > max_score:
                    max_score = score
                    max_index = k
            dp[i][j] = max_score
            backpointer[i][j] = max_index
    # 回溯：找到最优标签序列
    best_path = []
    best_state = np.argmax(dp[n-1])
    best_path.append(best_state)
    for i in range(n-2, -1, -1):
        best_state = backpointer[i+1][best_state]
        best_path.insert(0, best_state)
    return best_path
```

# 参考文献

1. [机器学习——条件随机场(CRF)原理](https://blog.csdn.net/hei653779919/article/details/104227606)

2. [NLP —— 图模型（二）条件随机场](https://www.cnblogs.com/Determined22/p/6915730.html)

3. [【深度学习】条件随机场（CRF）深度解析](https://blog.csdn.net/weixin_43988131/article/details/148777675)

4. [条件随机场之基本概念与模型](https://starmaye.github.io/NLP/条件随机场之基本概念与模型/)

5. [条件随机场（CRF）及其三个基本问题](https://sm1les.com/2019/08/27/conditional-random-fields/)