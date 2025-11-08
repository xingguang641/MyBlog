---
title: 【机器学习基础算法】第一节：滤波算法
published: 2025-11-08
description: 介绍机器学习常见的算法
tags: [Machine Learning, Course]
category: ML Algorithm
draft: false
---

# 贝叶斯滤波框架介绍

从这一节开始，我们正式进入 **滤波算法** （Filtering Algorithms） 的章节。提到滤波算法，就不得不先讲讲它的理论核心 ———— **贝叶斯滤波（Bayesian Filtering）** 。严格来说，贝叶斯滤波其实并不是一种具体的算法/模型，而是一种 **通用的思想框架** 。它告诉我们：如果我们知道系统是如何变化的，以及观测数据与真实状态之间的关系，那么就能通过 “更新信念” 的方式，不断修正对当前状态的估计。

但在正式讲解贝叶斯滤波之前，我们首先要了解什么是 **滤波算法（Filtering Algorithms）** 。

想象这样一个场景：

你正在研究一辆自动驾驶汽车。车上安装了 GPS、雷达、摄像头、惯性测量单元（IMU）等各种传感器。它们不停地输出关于车辆位置、速度、加速度的数据。

看起来数据很充足对吧？但问题的关键是：这些观测都是 **带噪声的** 。GPS 信号会漂移、雷达会误反射、IMU 也会随着时间累积误差，每个时刻的观测都是不完美的。也就是说：我们真正关心的车辆的真实状态是 **被噪声隐藏起来的** 。

![滤波算法图像](src\content\posts\bayesian-filter\滤波算法1.jpg)

于是问题来了：

> 当观测数据不可靠时，我们该如何尽可能准确地估计出系统的真实状态？

这正是滤波算法要解决的问题。

“滤波” 这个名字其实很形象：就像在嘈杂的信号中筛出干净的部分一样，滤波算法的目标就是在充满噪声的不确定观测中，提取出最可能的真实状态。从概率论的角度来看，滤波本质上就是一种 **去噪估计** （Noise Reduction Estimation）。在随机过程理论中，这种 “利用有噪观测去恢复隐藏状态” 的过程，被定义为 ———— **滤波**（Filtering）。

## 滤波的数学定义

至此我们已经直观地理解了滤波所要解决的事情，而要从理论上严谨地描述这一过程，我们就需要借助 **统计估计理论** （Statistical Estimation Theory）这个工具。

在统计意义上，所谓估计就是根据观测数据去推测未知量的真实值。如果这种未知量是一个固定的常数，我们则称之为 **参数估计问题** ；但如果未知量会随时间动态变化，那么这类问题就属于 **动态估计问题** （Dynamic Estimation Problem）。滤波问题正是其中的一个经典应用场景。

假设一个系统在任意时刻 $t$ 的内部状态（例如位置、速度、温度等）可以用一个向量表示，记作 $x_t$ ，它描述了系统在该时刻的 “真实但不可直接观测” 的状态。

而我们能够直接获取的，是由传感器或测量设备提供的观测值，记作 $z_t$ ，这些观测值与真实状态相关，但通常包含噪声。

于是，一个典型的动态系统可以由两类方程来描述：

$$
\begin{cases}
x_t = f(x_{t-1}, v_{t-1}) & \text{（状态转移方程）} \\
z_t = h(x_t, w_t) & \text{（观测方程）}
\end{cases}
$$

其中：
- $f(\cdot)$：描述系统状态如何随时间演化（系统的 **动态规律** ）
- $h(\cdot)$：描述系统状态如何被观测到（系统的 **观测规律** ）
- $v_t$、$w_t$：分别代表系统噪声与观测噪声，通常假设它们相互独立

换句话说，系统在每个时刻都会经历两个过程：

> 先变化（预测） $\longrightarrow$  再被观测（更新）

给定一段时间内的观测序列：

$$
z_{1:t} = \{ z_1, z_2, \ldots, z_t \}
$$

我们的目标是估计在时刻 $t$ 的系统状态分布：

$$
P(x_t|z_{1:t})
$$

这就是滤波问题的数学定义：根据截至当前的所有观测信息，求系统当前状态的后验概率分布。

需要注意的是：如果我们仅使用当前观测 $z_t$ 来估计状态，那只是 **瞬时估计** （Instantaneous Estimation）。而滤波更强调的是 **递推性** （Recursiveness）———— 随着时间的推移，不断地预测与更新，持续修正我们对系统状态的 “信念” 。

## 贝叶斯估计



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