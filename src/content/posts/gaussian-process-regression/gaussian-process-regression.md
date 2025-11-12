---
title: 【机器学习基本模型】第十节：高斯过程回归
published: 2025-11-10
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 高斯过程回归基本原理

在传统的机器学习中， **线性回归** 是最基础的监督学习模型之一。它通过一条直线（或超平面）去拟合数据的整体趋势，从而建立输入与输出之间的关系。

然而在很多复杂任务中，现实世界的数据往往呈现出 **非线性、不确定性强** 的特征，此时单纯的线性假设已无法很好地刻画真实关系。

为了解决这个问题，人们引入了 **概率建模** 的思想 ———— 我们不仅希望得到一个预测值，还希望能够衡量模型预测的不确定性，即给出预测结果的 **置信度** 。

在这一思路下， **高斯过程回归** （Gaussian Process Regression，简称 GPR） 便应运而生。它是一种以概率论为基础的非参数方法，能够在建模复杂函数的同时，对预测结果的不确定性进行定量刻画。

然而我们要真正理解高斯过程回归的思想，首先需要从它的简化形式出发，也就是 **贝叶斯线性回归** （Bayesian Linear Regression）。高斯过程回归正是基于贝叶斯回归思想的一种推广与扩展。

## 贝叶斯线性回归

在线性回归中，我们假设输入特征 $x$ 与输出 $y$ 之间满足线性关系：

$$
y = w^{\rm T} x + \epsilon
$$

其中 $\epsilon \sim \mathcal{N}(0, \beta^{-1})$ 表示高斯噪声。

传统的最小二乘回归（OLS）会通过最小化均方误差（MSE）来估计参数：

$$
\hat{w} = \arg \min_w \sum_i (y_i - w^{\rm T} x_i)^2
$$

这种方法得到的是参数 $w$ 的 **点估计** （point estimate），这是一个确定的结果。然而在现实中，训练数据往往 **有限、带噪声甚至存在异常点** ，因此我们在对参数估计时应该要参杂一点 “不确定性” 。

### 贝叶斯思想

在贝叶斯线性回归中，我们引入一个重要的思想：

> 我们不把参数 $w$ 看作确定值，而是把它当作一个 **随机变量** ，用概率分布来描述我们对它的信念。

也就是说，我们要建模的是 $P(w|\mathcal{D})$ 。即给定数据集 $\mathcal{D} = \{ (x_i, y_i) \}_{i=1}^N$ 的条件下，参数 $w$ 的 **后验分布** 。

这个分布告诉我们：在观察到数据之后，哪些 $w$ 是更可能的，哪些是不太可能的。这样我们不仅能够得到预测结果，还能量化预测的 “置信度” 。

为了得到这个后验分布，我们需要先引入两个概念：

- **先验分布（Prior）**

在未观察到任何数据之前，我们对参数 $w$ 的可能取值有一个先验假设。最常见的假设是各维度相互独立、均值为 0 的高斯分布：

$$
P(w) = \mathcal{N}(w | 0, \alpha^{-1} \mathbf{I})
$$

其中 $\alpha$ 表示先验分布的精度。

- **似然函数（Likelihood）**

假设观测数据由参数 $w$ 生成，并受到高斯噪声的影响：

$$
P(y | x, w) = \mathcal{N}(y | w^{\rm T} x, \beta^{-1})
$$

对于整个数据集 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ ，若假设样本独立同分布，则整体似然为：

$$
P(y | X, w) = \prod_{i=1}^{N} \mathcal{N}(y_i | w^{\rm T} \mathbf{x}_i, \beta^{-1})
$$

其中 $X$ 是特征矩阵， $y$ 是观测输出， $\beta$ 表示观测噪声的精度。

### 学习问题

正如上面所说：在贝叶斯线性回归中，我们的目标不再是寻找一个最优参数 $\hat{w}$ ，而是希望通过数据推断出参数的后验分布：

$$
P(w | X, y) = \frac{P(y | X, w) P(w)}{P(y | X)}
$$

由于我们假设先验与似然均为高斯分布，它们的乘积仍为高斯分布，因此后验分布 $P(w | X, y)$ 也服从高斯形式：

$$
P(w | X, y) = \mathcal{N}(w | \mathbf{m}_N, \mathbf{S}_N)
$$

将先验分布和似然函数带入贝叶斯公式后，可以得到后验分布的参数解析式：

$$
\mathbf{m}_N = \beta \mathbf{S}_N X^{\rm T} y \quad \mathbf{S}_N = (\alpha \mathbf{I} + \beta X^{\rm T} X)^{-1}
$$

其中 $\mathbf{m}_N$ 表示后验分布的均值，可视作参数 $w$ 的 “最有可能值” ； $\mathbf{S}_N$ 表示后验分布的协方差矩阵，反映了我们对参数不确定性的估计。

直观上看： $\mathbf{S}_N$ 的第一项 $\alpha \mathbf{I}$ 来源于先验，对参数起到正则化作用；第二项 $\beta X^{\rm T} X$ 来源于数据。因此当样本数量增加或噪声变小（ $\beta$ 变大）时，模型会更信任数据，后验分布变得更 “尖锐” 。

### 预测问题

在获得参数的后验分布 $P(w | X, y)$ 后，我们就可以对新样本 $x_*$ 进行预测。与传统线性回归直接使用单一参数 $\hat{w}$ 不同，贝叶斯线性回归会综合考虑所有可能的参数值，并按照其后验概率加权平均：

$$
P(y_* | x_*, X, y) = \int P(y_* | x_*, w) \, P(w | X, y) \, dw
$$

这一积分表达了核心的贝叶斯思想：

> 预测不仅依赖模型的结构，还依赖我们对参数不确定性的认知。

由于被积函数的两项（条件分布和后验分布）均为高斯形式，积分结果仍为高斯分布：

$$
P(y_* | x_*, X, y) = \mathcal{N}(y_* | \mu_*, \sigma_*^2)
$$

将后验分布（我们学习得到的模型）和似然函数带入积分后，可以得到预测分别的参数解析式：

$$
\mu_* = \mathbf{m}_N^{\rm T} x_* \quad \sigma_*^2 = \frac{1}{\beta} + x_*^{\rm T} \mathbf{S}_N x_*
$$

$\mu_*$ 表示模型的期望预测结果， $\sigma_*^2$ 则量化预测的不确定性。

直观上看： $\sigma_*^2$ 的第一项 $\displaystyle \frac{1}{\beta}$ 来自观测噪声，第二项 $x_*^{\rm T} \mathbf{S}_N x_*$ 来自参数的不确定性。因此当 $x_*$ 位于训练样本较密集的区域时 $\mathbf{S}_N$ 较小，模型预测更自信；在数据稀疏或未观测的区域时 $\mathbf{S}_N$ 较大，模型会自动 “变得谨慎” 。

## 理论基础

通过贝叶斯线性回归，我们学会了如何在参数层面引入不确定性：我们不再寻找单一的参数向量 $w$ ，而是对其建立一个概率分布 $P(w|X, y)$ 。这使得模型能够在预测时量化不确定性，从而变得更稳健、更可信。然而线性模型本身仍然受到 **特征空间的限制** 。

在贝叶斯线性回归中，即使我们对参数 $w$ 进行了概率建模，模型仍然只能表达输入 $x$ 的线性组合形式。

为了表达非线性关系，我们可以通过引入 **特征映射函数** $\phi(x)$ ，将输入投影到更高维的空间：

$$
f(x) = w^{\rm T} \phi(x)
$$

但这样一来，模型的复杂度和参数数量会急剧增加，计算和存储都变得困难。

于是我们换一种视角：

> 与其对参数 $w$ 进行建模，不如直接对函数 $f(x)$ 本身建模。

也就是说，我们不再假设存在某个确定的 $w$ ，而是假设所有可能的函数 $f(x)$ 构成了一个分布。而 **高斯过程** （Gaussian Process，简称 GP）就是这样一种 “对函数分布建模” 的方法。

高斯过程回归可以被看作是贝叶斯线性回归的 **无限维扩展** ：当特征映射 $\phi(x)$ 的维度趋于无穷时，贝叶斯线性回归自然地收敛为高斯过程回归。

### 高斯过程

从上面的讲解可以看出，我们要想弄懂什么是高斯过程回归，首先要弄懂什么是高斯过程。

高斯过程可以认为是一个 **对函数的分布** 。在贝叶斯线性回归中，我们通过参数 $w$ 的分布间接地对函数建模。而在高斯过程中，我们直接对函数 $f(x)$ 本身建模。

形式化地，我们假设：

$$
f(x) \sim \mathcal{GP}(m(x), k(x, x'))
$$

- $\displaystyle m(x) = \mathbb{E}\Big[f(x)\Big]$ 为 **均值函数** ，描述函数在输入空间的平均趋势
- $\displaystyle k(x, x') = \mathbb{E}\Big[(f(x) - m(x))(f(x') - m(x'))\Big]$ 为 **核函数** ，刻画任意两个输入点之间的相关性

为了理解高斯过程的由来，我们可以从贝叶斯线性回归出发。

回忆贝叶斯线性回归中的预测函数：

$$
f(x) = w^{\rm T} \phi(x)
$$

假设参数具有高斯先验：

$$
P(w) = \mathcal{N}(0, \alpha^{-1} \mathbf{I})
$$

那么我们可以计算出函数值的期望与协方差：

$$
\mathbb{E}\Big[f(x)\Big] = 0 \quad \text{Cov}\Big(f(x), f(x')\Big) &= \alpha^{-1} \phi(x)^{\rm T} \phi(x')
$$

说明在这种假设下， $f(x)$ 本身服从一个高斯过程，其协方差函数为：

$$
k(x, x') = \alpha^{-1} \phi(x)^{\rm T} \phi(x')
$$

也就是说，贝叶斯线性回归天然地隐含了一个高斯过程假设。如果我们令特征映射 $\phi(x)$ 的维度趋于无穷，并用核函数直接定义 $k(x, x')$ ，就得到了 **高斯过程回归** ———— 贝叶斯线性回归的无限维形式。

# 参考文献

## 贝叶斯线性回归

1. [贝叶斯线性回归（Bayesian Linear Regression）](https://blog.csdn.net/daunxx/article/details/51725086)

2. [浅入浅出贝叶斯线性回归 (Bayesian Linear Regression)](https://zhuanlan.zhihu.com/p/130974579)

3. [如何通俗地解释贝叶斯线性回归的基本原理？](https://www.zhihu.com/question/22007264/answers/updated)

4. [浅述贝叶斯线性回归](https://zhuanlan.zhihu.com/p/305042203)

5. [多元线性回归贝叶斯模型](https://andrewwang.rbind.io/courses/bayesian_statistics/notes/Ch7_h.pdf)

6. [贝叶斯数据分析(七)——贝叶斯线性回归](https://blog.vicayang.cc/Note-Bayesian-Linear-Regression/)

7. [贝叶斯线性回归与贝叶斯逻辑回归](https://weirping.github.io/blog/Bayesian-Probabilities-in-ML.html)

## 高斯过程回归

1. [高斯过程回归(Gaussian Processes Regression, GPR)简介](https://blog.csdn.net/HelloWorldTM/article/details/126980872)

2. [【ScikitLearn】高斯过程用于机器学习](https://scikit-learn.cn/stable/auto_examples/gaussian_process/index.html)

3. [【ScikitLearn】高斯过程回归与高斯过程分析](https://scikit-learn.cn/stable/modules/gaussian_process.html)

4. [高斯过程回归【详细数学推导】](https://blog.csdn.net/v20000727/article/details/138086802)

5. [高斯过程 Gaussian Processes 原理、可视化及代码实现](https://zhuanlan.zhihu.com/p/75589452)

6. [贝叶斯建模-高斯过程回归](https://bookdown.org/xiangyun/masr/gaussian-processes-regression.html)

7. [高斯过程回归（GPR）原理与实现](https://zhuanlan.zhihu.com/p/697071644)

8. [深度学习基础（高斯过程）](https://sirlis.cn/posts/deep-learning-gaussian-process/)

9. [Gaussian Processes](https://borgwang.github.io/ml/2019/07/28/gaussian-processes.html)