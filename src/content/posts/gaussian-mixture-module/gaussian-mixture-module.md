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

我们来思考一个简单的问题：如果给你一些数据，你想用什么模型去拟合这些数据的分布呢？可能很多人的第一想法就是用正态分布去拟合，毕竟正态分布是生活中最为常见的分布。其实这个想法是正确的，但仍有缺陷：虽然正态分布是最常见的分布，但现实世界实在是太过于复杂，我们不能确保一个正态分布就能拟合出所有的数据集。对此，我们可以试着想一想，如果用多个正态分布去拟合，效果会不会更好？没错，这正是高斯混合模型的出发点。

## 高斯加权混合

为了解决高斯模型的单峰性的问题，我们引入多个高斯模型的加权平均来拟合多峰数据：

$$
p(x) = \sum_{k=1}^K \alpha_k \mathcal{N}(\mu_k, \Sigma_k)
$$

由于我们只能观察到每个样本 $x$ 的信息，而无法了解每个样本究竟属于哪个高斯分布，因此我们可以引入一个隐变量 $z$ （ $z = k$ 表示样本属于第 K 个高斯分布）来辅助我们的推导：

$$
p(z = i) = p_i, \quad \sum_{i=1}^{k} p(z = i) = 1
$$

于是对 $P(x)$

值得注意的是：高斯混合模型并不在意每个数据点究竟属于哪个类别，它想要做的事情是让多个高斯模型去拟合整个数据集，从而去预测新数据属于哪朵高斯云。

# 参考文献

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