---
title: 【机器学习基本模型】第六节：高斯混合模型
published: 2025-10-27
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 高斯混合模型基本原理

前面我们讲到了诸多的 **分类算法** （Classification Algorithm），虽然它们的数学原理差别很大，但它们其实都属于 **有监督学习** （Supervised Learning）这一个类别当中。也就是说：它们在训练过程中需要数据拥有自己对应的标签。

而我们今天要讲的 **高斯混合模型** （Gaussian Mixture Model，简称 GMM），它是一个 **聚类算法** （Clustering Algorithm），而聚类算法不同于分类算法，它们属于 **无监督学习** （Unsupervised Learning）这一类别。也就是说：高斯混合模型不要求数据有自己的标签，高斯混合模型会自动地将数据分为不同的类别。

我们来思考一个简单的问题：如果给你一些数据，你想用什么模型去拟合这些数据的分布呢？可能很多人的第一想法就是用正态分布去拟合，毕竟正态分布是生活中最为常见的分布。其实这个想法是正确的，但仍有缺陷：虽然正态分布是最常见的分布，但现实世界太过于复杂，我们不能确保一个正态分布就能拟合出所有的数据集。对此，我们可以试着想一想：如果用多个正态分布去拟合，效果会不会更好？没错，这正是高斯混合模型的出发点。

## 高斯加权混合

为了解决高斯模型的单峰性的问题，我们引入多个高斯模型的加权平均来拟合多峰数据：

$$
P(x) = \sum_{k=1}^K \alpha_k \mathcal{N}(\mu_k, \Sigma_k)
$$

由于我们只能观察到每个样本 $x$ 的信息，而无法了解每个样本究竟属于哪个高斯分布，因此我们可以引入一个隐变量 $z$ （ $z = k$ 表示样本属于第 K 个高斯分布）来辅助我们的推导：

$$
P(z = i) = p_i \quad \sum_{i=1}^{k} P(z = i) = 1
$$

于是 $P(x)$ 可以写成：

$$
P(x) = \sum_z P(x,z) = \sum_{k=1}^K P(x,z=k) = \sum_{k=1}^K P(z=k) P(x|z=k)
$$

最后可以得到：

$$
P(x) = \sum_{k=1}^K p_k \mathcal{N}(x|\mu_k,\Sigma_k)
$$

值得注意的是：高斯混合模型并不在意每个数据点究竟属于哪个类别（只是推导过程关注于单个数据点）。它想要做的事情是让多个高斯模型去拟合整个数据集，从而去预测新数据属于哪哪个高斯分布。

## 梯度下降的局限

写出高斯混合模型的对数似然函数：

$$
\begin{align*}
L(\theta) &= \sum_{i=1}^{N} \log p(x_i) = \sum_{i=1}^{N} \log \sum_{k=1}^{K} p_k \mathcal{N}(x_i \mid \mu_k, \Sigma_k)
\end{align*}
$$

其中 $\theta = \{p_1, p_2, \dots, p_K, \mu_1, \mu_2, \dots, \mu_K, \Sigma_1, \Sigma_2, \dots, \Sigma_K\}$

对这个表达式直接通过求导，由于连加号的存在，会无法得到解析解。因此我们无法直接根据极大似然估计的原理对这个式子使用常见的梯度下降算法。

# EM 算法

由于无法直接对含有隐变量的似然函数求导，所以梯度下降无法求解出 GMM 的极大似然估计。对此我们引入一个专门解决此类问题的算法：EM 算法。

![高斯混合模型图像](src\content\posts\gaussian-mixture-module\EM算法1.jpg)

## 证据下界

我们可以先假设 $Z$ 服从的分布为 $Z \sim q(Z \mid \theta)$ ，于是有：

$$
\begin{align*}
\log P(X | \theta) &= \log P(X, Z | \theta) - \log P(Z | X, \theta) \\
&= \log \frac{P(X, Z | \theta)}{q(Z | \theta)} - \log \frac{P(Z | X, \theta)}{q(Z | \theta)}
\end{align*}
$$

两边同时关于 $Z \sim q(Z \mid \theta)$ 同时计算期望：

$$
\begin{align*}
\log P(X | \theta) &= \sum_{Z} q(Z | \theta) \log \frac{P(X, Z | \theta)}{q(Z | \theta)} - \sum_{Z} q(Z | \theta) \log \frac{P(Z | X, \theta)}{q(Z | \theta)} \\
&= \mathbb{E}_{Z \sim P(Z|X,\theta^{(t)})} [\log P(X, Z | \theta)] - \sum_{Z} q(Z | \theta) \log q(Z | \theta) + \operatorname{KL}(q(Z | \theta) \parallel P(Z | X, \theta)) \\
&= \mathbb{E}_{Z \sim P(Z|X,\theta^{(t)})} [\log P(X, Z | \theta)] + H(q(Z | \theta)) + \operatorname{KL}(q(Z | \theta) \parallel P(Z | X, \theta)) \\
&= ELBO(q, \theta | X) + \operatorname{KL}(q(Z | \theta) \parallel P(Z | X, \theta))
\end{align*}
$$

由于 KL 散度始终大于 0 ，因此 **ELBO** （Evidence Lower Bound Optimization，中文译名为 **证据下界** ）是 $L(\theta)$ 的一个下界（至于什么是 KL 散度可以参考下面这个视频）。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114558102410096&bvid=BV1r6jHzpE1J&cid=30166354742&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 流程介绍

EM 算法本质上是通过最大化 ELBO 来间接最大化对数似然函数。具体步骤分为 E-step 和 M-step。

- 寻找使得 KL 散度最小的 $q^{(t)}(Z) = P\left( Z | X, \theta^{(t)} \right)$ ，使得 ELBO 进一步逼近 $L(\theta)$
- 寻找 $ELBO(\theta | q^{(t)}, X)$ 的极大值点作为新参数 $\theta^{(t+1)}$

两者交替迭代，最终收敛到局部最优解。

### E-step

$$
L(\theta) - \text{ELBO}(q,\theta | X) = \text{KL}(q \parallel P(Z | X,\theta))
$$

要使 ELBO 逼近 $L(\theta)$ ，就要让 KL 散度最小，先通过当前参数 $\theta^{(t)}$ 估计 $q^{(t)}$ ，得 $q^{(t)}(Z) = P\left(Z | X, \theta^{(t)}\right)$ ，于是有：

$$
\begin{align*}
L(\theta) &= \log P(X | \theta) = \mathbb{E}_{Z \sim P(Z | X, \theta^{(t)})} \left[ \log P(X | \theta) \right] \\
&= Q(\theta; \theta^{(t)}) + \text{KL}(P(Z | X, \theta^{(t)}) \parallel P(Z | X, \theta))
\end{align*}
$$

这里我们将 $ELBO(\theta | q^{(t)}, X)$ 记为 $Q(\theta; \theta^{(t)})$ ：

$$
Q(\theta; \theta^{(t)}) = \mathbb{E}_{Z \sim P(Z | X,\theta^{(t)})} \left[ \log P(X,Z | \theta) \right] + H(P(Z | X,\theta^{(t)}))
$$

### M-step

由于信息熵为常数项，因此最大化 $Q(\theta; \theta^{(t)})$ 等价于将对数似然 $\log P(X, Z | \theta)$ 的期望最大化：

$$
\theta^{(t+1)} = \arg \max_{\theta} Q(\theta; \theta^{(t)}) = \arg \max_{\theta} \mathbb{E}_{Z \sim P(Z|X,\theta^{(t)})} \left[ \log P(X, Z | \theta) \right]
$$

## 流程解析

> 以下推导部分参考自该视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1400527903&bvid=BV1Q6421u7qb&cid=1448856301&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>



## 收敛性证明

EM 算法的流程并不复杂，但是还有两个问题需要我们思考：

- EM 算法能保证收敛吗？
- EM 算法如果收敛，那能保证收敛到全局最大值吗？

首先我们来看第一个问题：要证明 EM 算法收敛，我们则需要证明对数似然函数在迭代的过程中一直在增大。形式地说：



# 代码实现



# 参考文献

## 高斯混合模型

1. [高斯混合模型（GMM）](https://zhuanlan.zhihu.com/p/30483076)

2. [【维基百科】高斯混合模型](https://en.wikipedia.org/wiki/Mixture_model#Gaussian_mixture_model)

3. [高斯混合模型 GMM计算方法](https://www.cnblogs.com/conpi/p/18956198)

4. [机器学习-09-高斯混合模型GMM](https://www.cnblogs.com/Cnoized/p/18897547)

5. [GMM：高斯混合模型原理实现与应用](https://zhuanlan.zhihu.com/p/619191372)

6. [混合高斯模型](https://blog.csdn.net/u013172930/article/details/144853287)

7. [高斯混合模型的数学基础与理论分析](https://juejin.cn/post/7321778862785544202)

8. [高斯混合模型(Gaussian Mixture Model)与EM算法原理(一)](https://zhuanlan.zhihu.com/p/60649774)

9. [高斯混合模型(Gaussian Mixture Model)与EM算法原理(二)](https://zhuanlan.zhihu.com/p/61103099)

10. [GMM (Gaussian Mixture Model)](https://aandds.com/blog/gmm.html)

11. [【ScikitLearn】高斯混合模型](https://scikit-learn.cn/stable/modules/mixture.html)

## EM 算法

1. [EM算法的理解和详细推导](https://jaredddddd.github.io/2024/01/01/EM/)

2. [深入理解EM算法（ELBO+KL形式）](https://zhuanlan.zhihu.com/p/365641813)

3. [深入剖析EM算法：原理、推导与应用](https://blog.csdn.net/2501_90186640/article/details/147234092)

4. [EM算法详解](https://luyiyun.github.io/2020/12/08/methods/methods-em/)

5. [EM（最大期望）算法推导、GMM的应用与代码实现](https://www.cnblogs.com/qizhou/p/13100817.html)