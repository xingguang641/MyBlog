---
title: 【机器学习基础算法】第三节：近似推断算法
published: 2025-11-17
description: 介绍机器学习常见的算法
tags: [Machine Learning, Course]
category: ML Algorithm
draft: false
---

# 近似推断算法背景介绍

**近似推断**（Approximate Inference）算法是在概率模型中用于计算难以直接求解的后验概率分布、边缘概率分布或函数期望等推断任务的一类方法。

在许多复杂的模型中（例如具有高维隐变量的贝叶斯模型或深度学习模型），精确推断（Exact Inference）往往因为涉及到复杂的积分或求和运算而 **计算代价高昂** ，甚至是 **难以计算** 。近似推断的目的就是在 **计算精度和计算资源之间进行权衡** ，以便在有限的时间内获得一个足够好的近似解 。

## 近似推断概览

近似推断方法主要分为两大类：

1. **随机/采样方法（Stochastic/Sampling Methods）**：

    *   **核心思想**：通过 **大量采样** 来近似目标分布（通常是真实的后验分布）。
    *   **代表算法**：**马尔可夫链蒙特卡洛 (MCMC)** 方法，如 Gibbs 采样。
    *   **特点**：理论上，随着采样数量的增加，可以得到 **更精确** 的近似结果，但收敛速度可能较慢，且难以判断何时收敛。

2.  **确定性近似方法（Deterministic Approximation Methods）**：
    *   **核心思想**：将推断问题转化为一个 **优化问题** ，通过寻找一个 **形式简单、易于处理的近似分布** $q$ 来逼近真实的后验分布 $p$ 。
    *   **代表算法**：**变分推断**（Variational Inference，简称 VI），特别是变分贝叶斯推断（Variational Bayesian Inference）。
    *   **特点**：通常具有 **解析解**（或可通过迭代优化求解），**计算开销小、速度快** ，易于应用于大规模问题，但其近似能力受限于所选近似分布 $q$ 的形式（例如平均场假设）。

**总的来说**： 当精确推断不可行时，近似推断提供了一种实用的解决方案，它通过随机采样或构造优化目标（如变分推断中的变分下界）来高效地估计复杂的概率分布。

接下来我们就按顺序讲解马尔科夫蒙特卡洛、重要性采样、变分推断和期望传播四个算法。

# 马尔科夫蒙特卡洛



# 参考文献

## 马尔科夫蒙特卡洛

1. [机器学习-11-马尔科夫链蒙特卡洛MCMC](https://www.cnblogs.com/Cnoized/p/18913687)

2. [马尔可夫蒙特卡罗 MCMC 原理及经典实现](https://zhuanlan.zhihu.com/p/392917306)

## 重要性采样

1. [采样（三）：重要性采样与接受拒绝采样](https://allenwind.github.io/blog/10466/)

2. [重要性采样(Importance Sampling)](https://zhuanlan.zhihu.com/p/695130713)

3. [【Ugly Garden】重要性采样](https://baileyswu.github.io/2019/03/importance-sampling/)

## 变分推断

1. [一文搞懂变分推断（Variational inference）](https://zhuanlan.zhihu.com/p/682453554)

2. [VI、SGVI/SGVB、VAE串讲](https://www.cnblogs.com/tshaaa/p/18651129)

3. [变分推断详细推导](https://zhuanlan.zhihu.com/p/1893801387277648020)

4. [机器学习-10-变分推断VI](https://www.cnblogs.com/Cnoized/p/18910930)

5. [【PRML】如何简单易懂地理解变分推断](https://blog.yokumi.cn/2025/07/02/%E3%80%90PRML%E3%80%91%E5%A6%82%E4%BD%95%E7%AE%80%E5%8D%95%E6%98%93%E6%87%82%E5%9C%B0%E7%90%86%E8%A7%A3%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD%EF%BC%88Variational%20Inference%EF%BC%89/)

6. [变分推断与ELBO](https://zhuanlan.zhihu.com/p/1890718815135974325)

7.  [变分推断基础教程](https://zhuanlan.zhihu.com/p/1938261633504895739)

## 期望传播

1. [基于期望传播的活跃用户检测和信道估计](https://just.ustc.edu.cn/article/pdf/preview/1643455321968-20539875.pdf)

2. [基于期望传播的低复杂度高性能 EP-SU 大规模 MIMO 检测](http://scis.scichina.com/cn/2019/N112018-00160.pdf)