---
title: 【机器学习基础算法】第一节：滤波算法
published: 2025-11-08
description: 介绍机器学习常见的算法
tags: [Machine Learning, Course]
category: ML Algorithm
draft: false
---

# 贝叶斯滤波框架介绍

从现在开始，我们就正式来到了滤波算法的章节。提到滤波算法，我们就不得不先来讲解一下什么是 **贝叶斯滤波（Bayesian Filtering）** 。严格来说，贝叶斯滤波其实并不是一种具体的算法/模型，而是一种 **通用的思想框架** 。它告诉我们：如果我们知道系统是如何变化的，以及观测数据与真实状态之间的关系，那么就能通过 “更新信念” 的方式，不断修正对当前状态的估计。

但在正式讲解贝叶斯滤波之前，我们首先要了解什么是 **滤波算法（Filtering Algorithms）** 。

想象这样一个场景：

你正在研究一辆自动驾驶汽车。车上安装了 GPS、雷达、摄像头、惯性测量单元（IMU）等各种传感器。它们不停地输出关于车辆位置、速度、加速度的数据。

看起来数据很丰富对吧？但问题的关键是：这些观测都是 **带噪声的** 。GPS 信号会漂、雷达会反射错误、IMU 也会随着时间累积误差，每个时刻的观测都是不完美的。而我们真正关心的车辆状态（它到底在哪、速度是多少）是 **被噪声隐藏起来的** 。

于是问题来了：

> 当观测数据不可靠时，我们该如何尽可能准确地估计出系统的真实状态？

这正是滤波算法要解决的问题。

“滤波” 这个名字其实很形象：就像在嘈杂的信号中筛出干净的部分一样，滤波算法要在不确定的观测中 “过滤出” 最有可能的真实状态。直白地说，滤波就是 **去噪** ———— 而在随机过程理论中，这种 “去除噪声、提取真实信号” 的过程，就被称为 **滤波（Filtering）** 。

![滤波算法图像](src\content\posts\bayesian-filter\滤波算法1.jpg)

## 滤波的数学定义

我们已经知道，滤波的目标是：在存在噪声的观测中，尽可能准确地估计出系统的真实状态。那么从数学角度来看，这个问题该如何刻画呢？

假设系统的内部状态（例如位置、速度、温度等）可以用一个向量表示，记作 $x_t$ 。它描述了系统在时间 $t$ 的真实状态。此外，我们将能够观测到的传感器数据或测量值记作 $z_t$ 。它与真实状态有关，但通常带有噪声。

于是，一个典型的动态系统可以由两类方程来描述：

$$
\begin{cases}
x_t = f(x_{t-1}, v_{t-1}) & \text{（状态转移方程）} \\
z_t = h(x_t, w_t) & \text{（观测方程）}
\end{cases}
$$

其中：
- $f(\cdot)$ 描述系统状态如何随时间演化
- $h(\cdot)$ 描述状态如何映射为观测
- $v_t$ 和 $w_t$ 分别是系统噪声与观测噪声

换句话说，系统在每个时刻都会经历两个过程：

> 先变化（预测） $\longrightarrow$ 再被观测（更新）

给定一段时间内的观测序列：

# 参考文献

## 贝叶斯滤波

1. [Bayes Filter 算法介绍](https://aandds.com/blog/bayes-filter.html)

2. [从概率到贝叶斯滤波](https://zhuanlan.zhihu.com/p/268624245)

3. [从贝叶斯滤波到卡尔曼滤波](https://zhuanlan.zhihu.com/p/268632039)

4. [从贝叶斯滤波到扩展卡尔曼滤波](https://zhuanlan.zhihu.com/p/268635367)

5. [贝叶斯滤波器学习笔记](https://blog.csdn.net/jimmychao1982/article/details/149745121)

## 卡尔曼滤波

1. [卡尔曼滤波(Kalman Filter)概念介绍及详细公式推导](https://blog.csdn.net/qq_37214693/article/details/130927283)

2. [【万字长文】让你一文轻松掌握卡尔曼滤波](https://www.cnblogs.com/SkyXZ/p/18660856)

3. [滤波笔记一：卡尔曼滤波（Kalman Filtering）详解](https://blog.csdn.net/ouok000/article/details/125578636)

4. [Kalman滤波器的原理与实现](https://www.cnblogs.com/CrescentWind/p/18132934)

5. [卡尔曼滤波（DezemingFamily）](https://zhengyu.tech/upload/2023/08/Kalman%20Filter.pdf)

6. [从贝叶斯到卡尔曼滤波](https://www.cnblogs.com/ishen/p/14987878.html)

7. [从贝叶斯估计到卡尔曼滤波（详细推导）](https://zhuanlan.zhihu.com/p/521538539)

## 粒子滤波

1. [【滤波】粒子滤波（PF）](https://blog.csdn.net/qq_38410730/article/details/131214213)

2. [【维基百科】Particle Filter](https://en.wikipedia.org/wiki/Particle_filter)

3. [粒子滤波器解读](https://blog.csdn.net/qq_44648285/article/details/148074482)

4. [粒子滤波理论、方法及其在多目标跟踪中的应用](https://www.researchgate.net/publication/292354427_Particle_filtering_Theory_approach_and_application_for_multitarget_tracking)

5. [粒子滤波 particle filter 的理论及实践（matlab版）](https://blog.csdn.net/weixin_44044161/article/details/125445579)