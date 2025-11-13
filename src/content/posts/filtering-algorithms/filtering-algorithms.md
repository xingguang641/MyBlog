---
title: 【机器学习基础算法】第一节：滤波算法
published: 2025-11-08
description: 介绍机器学习常见的算法
tags: [Machine Learning, Course]
category: ML Algorithm
draft: false
---

# 贝叶斯滤波框架介绍

从这一节开始，我们正式进入 **滤波算法** （Filtering Algorithms） 的章节。提到滤波算法，就不得不先讲讲它的理论核心 ———— **贝叶斯滤波** （Bayesian Filtering）。严格来说，贝叶斯滤波其实并不是一种具体的算法/模型，而是一种 **通用的思想框架** 。它告诉我们：如果我们知道系统是如何变化的，以及观测数据与真实状态之间的关系，那么就能通过 “更新信念” 的方式，不断修正对当前状态的估计。

但在正式讲解贝叶斯滤波之前，我们首先要了解什么是 **滤波算法** （Filtering Algorithms）。

想象这样一个场景：

你正在研究一辆自动驾驶汽车。车上安装了 GPS、雷达、摄像头、惯性测量单元（IMU）等各种传感器。它们不停地输出关于车辆位置、速度、加速度的数据。

看起来数据很充足对吧？但问题的关键是：这些观测都是 **带噪声的** 。GPS 信号会漂移、雷达会误反射、IMU 也会随着时间累积误差，每个时刻的观测都是不完美的。也就是说：我们真正关心的车辆的真实状态是 **被噪声隐藏起来的** 。

![滤波算法图像](src\content\posts\filtering-algorithms\滤波算法1.jpg)

于是问题来了：

> 当观测数据不可靠时，我们该如何尽可能准确地估计出系统的真实状态？

这正是滤波算法要解决的问题。

“滤波” 这个名字其实很形象：就像在嘈杂的信号中筛出干净的部分一样，滤波算法的目标就是在充满噪声的不确定观测中，提取出最可能的真实状态。从概率论的角度来看，滤波本质上就是一种 **去噪估计** （Noise Reduction Estimation）。在随机过程理论中，这种 “利用有噪观测去恢复隐藏状态” 的过程被称为 ———— **滤波**（Filtering）。

## 滤波的数学定义

至此我们已经直观地理解了滤波所要解决的事情，而要从理论上严谨地描述这一过程，我们就需要借助 **统计估计理论** （Statistical Estimation Theory）这个工具。

在统计意义上，所谓估计就是根据观测数据去推测未知量的真实值。如果这种未知量是一个固定的常数，我们则称之为 **参数估计问题** ；但如果未知量会随时间动态变化，那么这类问题就属于 **动态估计问题** （Dynamic Estimation Problem）。滤波问题正是其中的一个经典应用场景。

假设一个系统在任意时刻 $t$ 的内部状态（例如位置、速度、温度等）可以用一个向量表示，记作 $x_t$ ，它描述了系统在该时刻的 “真实但不可直接观测” 的状态。

而我们能够直接获取的，是由传感器或测量设备提供的观测值，记作 $z_t$ ，这些观测值与真实状态相关，但通常包含噪声。

于是，一个典型的动态系统可以由两类方程来描述：

$$
\begin{cases}
x_t = f(x_{t-1}, v_{t-1}) & \text{（状态转移方程）} \\
\\
z_t = h(x_t, w_t) & \text{（观测方程）}
\end{cases}
$$

其中：
- $f(\cdot)$ ：描述系统状态如何随时间演化（系统的 **动态规律** ）
- $h(\cdot)$ ：描述系统状态如何被观测到（系统的 **观测规律** ）
- $v_t$ 、$w_t$ ：分别代表系统噪声与观测噪声，通常假设它们相互独立

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

通过前面的内容我们已经知道，滤波问题的目标，是希望利用带噪声的观测序列 $z_{1:t}$ 去估计系统的真实状态 $x_t$ 。而在概率论的语境下，这个 “估计” 的本质，其实就是计算一个条件概率分布 $P(x_t|z_{1:t})$ 。而要得到这个后验概率，最自然的工具就是 **贝叶斯公式** （Bayes’ Rule）。

贝叶斯估计的核心思想非常简单：

> 先根据已知的模型和历史观测得到一个先验信念（Prior），再根据新的观测信息对它进行修正（Likelihood），从而获得一个新的信念（Posterior）

用数学形式表示就是：

$$
P(x_t|z_{1:t}) = \frac{P(z_t|x_t)P(x_t|z_{1:t-1})}{P(z_t|z_{1:t-1})}
$$

这正是贝叶斯滤波更新步骤的数学基础。如果我们能递推地计算出上述分布，就能在每个时刻动态地更新对系统状态的估计。

## 递推贝叶斯状态估计

贝叶斯滤波，又称 **递推贝叶斯状态估计** （Recursive Bayesian State Estimation），其本质是贝叶斯估计 **在时间序列上的递推形式** 。下面将给出其完整的推导过程。

根据贝叶斯公式，可以把滤波过程拆解为两个核心步骤：

1. **预测（Prediction）**

从全概率公式（对上一时刻状态积分/求和）出发：

$$
\begin{align*}
P(x_t | z_{1:t-1}) &= \int P(x_t, x_{t-1} | z_{1:t-1}) \, dx_{t-1} \\
&= \int P(x_t | x_{t-1}, z_{1:t-1}) \, P(x_{t-1} | z_{1:t-1}) \, dx_{t-1}
\end{align*}
$$

再利用马尔可夫性假设 $P(x_t | x_{t-1}, z_{1:t-1}) = P(x_t | x_{t-1})$ ，可以得到：

$$
P(x_t | z_{1:t-1}) = \int P(x_t | x_{t-1}) \, P(x_{t-1} | z_{1:t-1}) \, dx_{t-1}
$$

这个步骤可以理解为：“根据系统的动态规律，推测现在可能在哪里”。

2. **更新（Update）**

首先直接用贝叶斯公式：

$$
P(x_t | z_{1:t}) = \frac{P(z_t | x_t, z_{1:t-1}) P(x_t | z_{1:t-1})}{P(z_t | z_{1:t-1})}
$$

利用观测条件独立性 $P(z_t | x_t, z_{1:t-1}) = P(z_t | x_t)$ 将分子化简为 $P(z_t | x_t) P(x_t | z_{1:t-1})$ 。其中的归一化常数（分母）由全概率给出：

$$
P(z_t | z_{1:t-1}) = \int P(z_t | x_t) P(x_t | z_{1:t-1}) \, dx_t
$$

因此得到标准更新公式：

$$
P(x_t | z_{1:t}) = \frac{P(z_t | x_t) P(x_t | z_{1:t-1})}{\int P(z_t | x_t) P(x_t | z_{1:t-1}) \, dx_t}
$$

这个步骤可以理解为：“根据当前的观测，修正我们的信念”。

贝叶斯滤波为 **状态估计问题** 提供了最通用的理论框架。然而在实际应用中，该公式中的积分往往难以解析计算，尤其在 **非线性、非高斯** 系统下几乎无法得到闭式解。因此尽管贝叶斯滤波在理论上极其完备，但在工程中通常使用近似的方法实现：

- **卡尔曼滤波（Kalman Filter）** ———— 线性高斯系统的最优解
- **扩展卡尔曼滤波（EKF）** ———— 非线性系统的近似解
- **粒子滤波（Particle Filter）** ———— 适用于任意非线性、非高斯系统的采样方法

接下来我们将详细介绍这三个具体的滤波算法。

# 卡尔曼滤基本原理

在现实世界中，任何测量都伴随着噪声和不确定性。无论是追踪卫星轨迹、预测经济指标，还是实现自动驾驶汽车的精准定位，我们都需要一种方法从杂乱的数据中提取出真实的信号。 **卡尔曼滤波** （Kalman Filter）正是为解决这一问题而诞生的强大工具。

在 1960 年，卡尔曼发表了他著名的用递归方法解决离散数据线性滤波问题的论文。从那以后，得益于数字计算技术的进步，卡尔曼滤波器已经衍生出来多种版本的滤波器。

卡尔曼滤波是一种高效率的递归滤波器（自回归滤波器），如果不以人名命名，则其名称是 **线性二次估计** （Linear Quadratic Estimation），它能够从一系列的不完全及包含噪声的测量中，估计动态系统的状态。

![卡尔曼滤波图像](src\content\posts\filtering-algorithms\卡尔曼滤波1.jpg)

## 先验假设

在上面的贝叶斯滤波框架介绍我们知道：卡尔曼滤波是贝叶斯滤波在特定假设下的简化版本。或者更准确地说，是贝叶斯滤波在 **线性高斯假设** （Linear Gaussian Assumption）下的解析解。

下面我们详细讲清楚这背后的前提假设：

- 系统是线性的（Linear System）

$$
x_t = Ax_{t-1} + Bu_t + w_t \quad z_t = Hx_t + v_t
$$

这种线性结构保证了状态的演化与观测之间可以通过矩阵运算直接描述，使得贝叶斯滤波中的积分步骤能够被解析地求解，从而得到闭式递推公式。

- 噪声服从高斯分布（Gaussian Noise）

$$
w_t \sim \mathcal{N}(0, Q) \quad v_t \sim \mathcal{N}(0, R)
$$

其中 $w_t$ 为 **过程噪声** （Process Noise）， $v_t$ 为 **观测噪声** （Measurement Noise）。

由于高斯分布在线性变换下仍保持高斯形式（闭合性），因此系统的先验与后验分布始终保持为高斯分布，可完全由均值和协方差刻画。

- 噪声独立性假设（Independence Assumption）

$$
P(w_t, v_t | x_{0:t-1}, z_{1:t-1}) = P(w_t)\,P(v_t)
$$

这种独立性避免了联合分布中出现复杂的耦合项，大幅简化了贝叶斯推导的计算，使得滤波公式可以逐步递推。

- 初始状态为高斯分布（Gaussian Prior）

$$
x_0 \sim \mathcal{N}(\hat{x}_0, P_0)
$$

假设初始状态是高斯分布，这样通过线性高斯系统的递推，整个状态序列的分布都会保持高斯形式，保证卡尔曼滤波在每个时刻都能用 “均值 + 协方差” 精确描述系统状态的不确定性。

## 理论基础

在讲解贝叶斯滤波框架的时候我们已经给出了贝叶斯滤波的递推形式：

$$
\left\{
\begin{aligned}
&P(x_t | z_{1:t-1}) = \int P(x_t | x_{t-1})\,P(x_{t-1} | z_{1:t-1})\,dx_{t-1} && \text{(预测步)} \\
\\[0.5em]
&P(x_t | z_{1:t}) \propto P(z_t | x_t)\,P(x_t | z_{1:t-1}) && \text{(更新步)}
\end{aligned}
\right.
$$

我们已经知道整个滤波过程共分为预测和更新两个阶段。卡尔曼滤波正是在上述两步的基础上，利用线性高斯假设，将概率形式的积分与乘法转化为对 **均值与协方差** 的递推计算。

### Prediction Step

假设我们已经在时刻 $t-1$ 时获得了状态后验分布：

$$
x_{t-1} | z_{t-1} \sim \mathcal{N}(\hat{x}_{t-1|t-1}, P_{t-1|t-1})
$$

因此直接可以得到：

$$
P(x_{t-1}|z_{1:t-1}) = \mathcal{N}(\hat{x}_{t-1|t-1}, P_{t-1|t-1})
$$

根据系统状态方程：

$$
x_t = Ax_{t-1} + Bu_t + w_t \quad w_t \sim \mathcal{N}(0, Q)
$$

由于上述公式中出现的所有变量都服从高斯分布，因此 $x_t$ 在给定 $x_{t-1}$ 的情况下仍然是高斯分布（这里的 $u_t$ 是已知的控制输入，而 $x_{t-1}$ 是给定的条件，因此真正的变量只有 $w_t$ ，所以最终得到的分布的方差为 $Q$ ）：

$$
x_t|x_{t-1} \sim \mathcal{N}(Ax_{t-1} + Bu_t, Q)
$$

也就是：

$$
P(x_t|x_{t-1}) = \mathcal{N}(Ax_{t-1} + Bu_t, Q)
$$

根据贝叶斯滤波预测公式：

$$
P(x_t | z_{1:t-1}) = \int P(x_t | x_{t-1})\,P(x_{t-1} | z_{1:t-1})\,dx_{t-1}
$$

因为高斯分布的线性卷积仍为高斯分布，所以 $P(x_t|z_{1:t-1})$ 也同样是高斯分布。因此我们可以直接推导 $P(x_t|z_{1:t-1})$ 的均值和协方差从而确定出分布 $P(x_t|z_{1:t-1})$ ：

$$
P(x_t|z_{1:t-1}) = \mathcal{N}(\hat{x}_{t|t-1}, P_{t|t-1})
$$

- 预测方差（Law of total expectation）

$$
\begin{align*}
\hat{x}_{t|t-1} &= \mathbb{E} \Big[ x_t | z_{1:t-1} \Big] = \mathbb{E} \Big[ \mathbb{E} \big[ x_t | x_{t-1} \big] | z_{1:t-1} \Big] \\
&= \mathbb{E} \Big[ Ax_{t-1} + Bu_t | z_{1:t-1} \Big] = A\mathbb{E} \Big[ x_{t-1} | z_{1:t-1} \Big] + Bu_t \\
&= A\hat{x}_{t-1|t-1} + Bu_t
\end{align*}
$$

- 预测协方差（Law of total covariance）

$$
\begin{align*}
P_{t|t-1} &= \text{Cov} \Big( x_t | z_{1:t-1} \Big) = \mathbb{E} \Big[ \text{Cov} \big( x_t | x_{t-1} \big) | z_{1:t-1} \Big] + \text{Cov} \Big( \mathbb{E} \big[ x_t | x_{t-1} \big] | z_{1:t-1} \Big) \\
&= \mathbb{E} \Big[ Q | z_{1:t-1} \Big] + \text{Cov} \Big( Ax_{t-1} + Bu_t | z_{1:t-1} \Big) = Q + A \, \text{Cov} \Big( x_{t-1} | z_{1:t-1} \Big) \, A^{\rm T} \\
&= Q + AP_{t-1|t-1}A^{\rm T}
\end{align*}
$$

### Update Step

通过 Prediction Step 我们可以得到先验分布为：

$$
p(x_t | z_{1:t-1}) =
\frac{1}{(2\pi)^{\frac{n}{2}} |P_{t|t-1}|^{\frac{1}{2}}}
\exp \Big( -\frac{1}{2} (x_t - \hat{x}_{t|t-1})^{\rm T} P_{t|t-1}^{-1} (x_t - \hat{x}_{t|t-1}) \Big)
$$

当新的观测值 $z_t$ 到达时，我们利用观测方程：

$$
z_t = Hx_t + v_t \quad v_t \sim \mathcal{N}(0, R)
$$

因此可以得到观测似然为：

$$
p(z_t | x_t) =
\frac{1}{(2\pi)^{\frac{m}{2}} |R|^{\frac{1}{2}}}
\exp \Big( -\frac{1}{2} (z_t - H x_t)^{\rm T} R^{-1} (z_t - H x_t) \Big)
$$

根据贝叶斯滤波更新公式可得：

$$
\begin{aligned}
P(x_t | z_{1:t}) 
&\propto 
\exp \Big( -\frac{1}{2} (x_t - \hat{x}_{t|t-1})^{\rm T} P_{t|t-1}^{-1} (x_t - \hat{x}_{t|t-1}) \Big)
\exp \Big( -\frac{1}{2} (z_t - H x_t)^{\rm T} R^{-1} (z_t - H x_t) \Big) \\
&= \exp \Bigg( -\frac{1}{2} \Big[ x_t^{\rm T} P_{t|t-1}^{-1} x_t - 2 x_t^{\rm T} P_{t|t-1}^{-1} \hat{x}_{t|t-1} + (z_t - H x_t)^{\rm T} R^{-1} (z_t - H x_t) \Big] \Bigg)
\end{aligned}
$$

现在想办法将上述公式化简成如下形式：

$$
P(x_t | z_{1:t}) \propto 
\exp \Big( -\frac{1}{2} (x_t - \hat{x}_{t|t})^{\rm T} P_{t|t}^{-1} (x_t - \hat{x}_{t|t}) \Big)
$$

将指数项最后一项展开：

$$
(z_t - H x_t)^{\rm T} R^{-1} (z_t - H x_t) = x_t^{\rm T} H^{\rm T} R^{-1} H x_t - 2 x_t^{\rm T} H^{\rm T} R^{-1} z_t + z_t^{\rm T} R^{-1} z_t
$$

代回指数项整理可得：

$$
x_t^{\rm T} (P_{t|t-1}^{-1} + H^{\rm T} R^{-1} H) x_t - 2 x_t^{\rm T} (P_{t|t-1}^{-1} \hat{x}_{t|t-1} + H^{\rm T} R^{-1} z_t) + z_t^{\rm T} R^{-1} z_t
$$

对比二次型形式 $x_t^{\rm T} a x_t - 2 x_t^{\rm T} b$ ，忽略常数项（不含 $x_t$ 的项）后不难得出：

$$
a = P_{t|t-1}^{-1} + H^{\rm T} R^{-1} H \quad b = P_{t|t-1}^{-1} \hat{x}_{t|t-1} + H^{\rm T} R^{-1} z_t
$$

综合上述信息不难得到：

$$
P_{t|t} = (P_{t|t-1}^{-1} + H^{\rm T} R^{-1} H)^{-1} \quad \hat{x}_{t|t} = P_{t|t} \big( P_{t|t-1}^{-1} \hat{x}_{t|t-1} + H^{\rm T} R^{-1} z_t \big)
$$

接下来重复 Prediction Step 直至循环结束即可。

# 卡尔曼滤波代码讲解

卡尔曼滤波算法的核心非常简洁，本质上就是在上述推导过程中得到的两个步骤 ———— 预测与更新 ———— 的递推公式。

```py frame="code" title="main.py"
import numpy as np

class KalmanFilter:
    def __init__(self, A, B, H, Q, R, x0, P0):
        self.A = A; self.B = B; self.Q = Q
        self.H = H; self.R = R

        self.x = x0 # 后验均值
        self.P = P0 # 后验协方差

    def predict(self, u=None):
        if u is None:
            u = np.zeros((self.B.shape[1],))
        # 预测状态均值
        self.x = self.A @ self.x + self.B @ u
        # 预测协方差
        self.P = self.A @ self.P @ self.A.T + self.Q
        return self.x, self.P

    def update(self, z):
        # 计算卡尔曼增益
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        # 更新状态均值
        y = z - self.H @ self.x # 观测残差
        self.x = self.x + K @ y
        # 更新协方差
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P
        return self.x, self.P, K
```

# 扩展卡尔曼滤基本原理

在前一节中，我们介绍了 **卡尔曼滤波** ，它是一种针对线性系统的递推状态估计方法，通过预测和更新两步迭代实现对系统状态的高效估计。然而，在实际工程中，绝大多数系统具有明显的非线性特性，例如飞行器的姿态控制、移动机器人路径规划以及非线性传感器测量系统。传统的线性卡尔曼滤波器在处理这些非线性系统时可能产生较大的误差，甚至无法收敛。

为了解决这一问题，Schmidt 等学者提出了 **扩展卡尔曼滤波器** （Extended Kalman Filter，简称 EKF）。扩展卡尔曼滤波器的核心思想是：在每个时间步，将非线性系统在当前估计点附近进行局部线性化处理，然后沿用线性卡尔曼滤波的预测和更新步骤来估计系统状态。通过这种方式，EKF 能够在保持递推效率的同时，处理非线性系统的状态估计问题。

相比于线性卡尔曼滤波器，扩展卡尔曼滤波器具有更广泛的适用范围和更高的状态估计精度，同时可以适应不同频率的观测更新。因此，EKF 在航空航天、机器人导航、自动驾驶以及金融建模等领域得到了广泛应用，成为解决非线性系统状态估计问题的重要工具。

![扩展卡尔曼滤波图像](src\content\posts\filtering-algorithms\扩展卡尔曼滤波1.jpg)

## 理论基础

扩展卡尔曼滤波旨在解决非线性系统的状态估计问题，其状态空间方程可以表示为：

$$
\begin{cases}
x_t = f(x_{t-1}, u_t) + w_t \quad & w_t \sim \mathcal{N}(0, Q) \\
\\
z_t = h(x_t) + v_t \quad & v_t \sim \mathcal{N}(0, R)
\end{cases}
$$

要将卡尔曼滤波应用于非线性系统，核心步骤是对非线性系统进行线性化处理。扩展卡尔曼滤波通过在当前状态估计点对系统方程进行 **一阶泰勒展开** 来实现局部线性化，从而在每个时间步近似为线性系统进行预测与更新。

扩展卡尔曼滤波是一个二元向量输入多输出系统。对于对于一个二元输入、多输出的非线性系统函数有如下两个公式需要了解：

- 单输出的二元函数 $f(x, y)$ 在点 $(x_0, y_0)$ 处的一阶泰勒展开公式

$$
f(x, y) \approx f(x_0, y_0) + \frac{\partial f}{\partial x}\Big|_{(x_0, y_0)} (x - x_0) + \frac{\partial f}{\partial y}\Big|_{(x_0, y_0)} (y - y_0)
$$

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113553197499694&bvid=BV1WvBQYsEkL&cid=27052212975&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

- 多输出函数对输入向量求导公式（雅可比矩阵）

$$
\mathbf{J}_{\mathbf{f}}(\mathbf{x}) =
\frac{\partial \mathbf{f}}{\partial \mathbf{x}} =
\begin{bmatrix}
\dfrac{\partial f_1}{\partial x_1} \quad & \dfrac{\partial f_1}{\partial x_2} \quad & \cdots \quad & \dfrac{\partial f_1}{\partial x_n} \\[6pt]
\dfrac{\partial f_2}{\partial x_1} \quad & \dfrac{\partial f_2}{\partial x_2} \quad & \cdots \quad & \dfrac{\partial f_2}{\partial x_n} \\[6pt]
\vdots & \vdots & \ddots & \vdots \\[6pt]
\dfrac{\partial f_m}{\partial x_1} \quad & \dfrac{\partial f_m}{\partial x_2} \quad & \cdots \quad & \dfrac{\partial f_m}{\partial x_n}
\end{bmatrix}
$$

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=966638278&bvid=BV1DW4y1F7gB&cid=28736554042&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

对非线性状态函数 $f(x_{t-1}, u_t)$ 在当前状态估计 $\hat{x}_{t-1|t-1}$ 附近进行一阶展开：

$$
f(x_{t-1}, u_t) \approx f(\hat{x}_{t-1|t-1}, u_t) + F_{t-1} (x_{t-1} - \hat{x}_{t-1|t-1})
$$

其中 $F_{t-1}$ 是状态方程的雅可比矩阵。

同理对观测函数 $h(x_t)$ 在先验估计 $\hat{x}_{t|t-1}$ 附近进行一阶展开：

$$
h(x_t) \approx h(\hat{x}_{t|t-1}) + H_t (x_t - \hat{x}_{t|t-1})
$$

其中 $H_{t}$ 是观测方程的雅可比矩阵。

通过上述线性化，原本的非线性系统就被局部近似线性系统：

$$
\begin{cases}
x_t \approx f(\hat{x}_{t-1|t-1}, u_t) + F_{t-1} (x_{t-1} - \hat{x}_{t-1|t-1}) + w_t \quad & w_t \sim \mathcal{N}(0, Q) \\
\\
z_t \approx h(\hat{x}_{t|t-1}) + H_t (x_t - \hat{x}_{t|t-1}) + v_t \quad & v_t \sim \mathcal{N}(0, R)
\end{cases}
$$

引入 **状态偏移量** 和 **观测偏移量**：

$$
\bar{x}_{t-1} = x_{t-1} - \hat{x}_{t-1|t-1} \quad \bar{x}_t = x_t - f(\hat{x}_{t-1|t-1}, u_t)
$$

$$
\bar{x}_t = x_t - \hat{x}_{t|t-1} \quad \bar{z}_t = z_t - h(\hat{x}_{t|t-1})
$$

其中 $\hat{x}_{t-1|t-1}$ 、 $f(\hat{x}_{t-1|t-1}, u_t)$ 和 $h(\hat{x}_{t|t-1})$ 都是已知的，并且还有 $\hat{x}_{t|t-1} = f(\hat{x}_{t-1|t-1}, u_t)$ 。

经过简单的变形可得：

$$
\begin{cases}
\bar{x}_t = F_{t-1} \bar{x}_{t-1} + w_t \quad & w_t \sim \mathcal{N}(0, Q) \\
\\
\bar{z}_t = H_t \bar{x}_t + v_t \quad & v_t \sim \mathcal{N}(0, R)
\end{cases}
$$

这样就可以 **直接套用线性卡尔曼滤波的预测和更新公式** ，只是需要用雅可比矩阵 $F_{t-1}$ 和 $H_t$ 替代原来的线性矩阵 $A$ 和 $H$ ，并在每个时间步重新计算。

# 扩展卡尔曼滤波代码讲解

EKF 是对非线性系统的状态估计方法，其核心思想与线性卡尔曼滤波类似：在每个时间步进行 **预测** 和 **更新** 两个递推步骤。不同的是 EKF 对非线性状态和观测函数进行了局部线性化处理，通过雅可比矩阵近似系统的线性行为。

下面的代码展示了一个 EKF 的完整实现：

```py frame="code" title="main.py"
import numpy as np

class ExtendedKalmanFilter:
    def __init__(self, f, F_jacobian, h, H_jacobian, Q, R, x0, P0):
        self.f = f; self.F_jacobian = F_jacobian; self.Q = Q
        self.h = h; self.H_jacobian = H_jacobian; self.R = R

        self.x = x0 # 后验均值
        self.P = P0 # 后验协方差

    def predict(self, u=None):
        if u is None:
            u = np.zeros((1,))
        # 状态预测
        self.x = self.f(self.x, u)
        # 协方差预测
        F = self.F_jacobian(self.x, u)
        self.P = F @ self.P @ F.T + self.Q
        return self.x, self.P

    def update(self, z):
        # 雅可比矩阵
        H = self.H_jacobian(self.x)
        # 卡尔曼增益
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        # 状态更新
        y = z - self.h(self.x)
        self.x = self.x + K @ y
        # 协方差更新
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ H) @ self.P
        return self.x, self.P, K
```

# 粒子滤波基本原理

在非线性系统中，贝叶斯滤波面临的主要困难是 **状态分布的表达和积分计算** 。对于一般的 **非线性、非高斯** 系统，解析求解几乎不可行。为此人们引入了基于数值近似的 **蒙特卡罗方法** ，其中最具代表性的就是 **粒子滤波** （Particle Filter，简称 PF）。

粒子滤波通过一组带权重的随机样本（称为 “粒子” ）来近似系统状态的后验分布，并在每个时刻根据观测信息更新粒子的分布和权重。由于不依赖线性化或高斯假设，它能够处理任意形式的非线性与非高斯系统，因此广泛应用于 **机器人定位、目标跟踪、计算机视觉** 等领域。

直观地说，粒子滤波就像在迷雾中寻找宝藏：每个粒子代表一个可能的位置，而其权重反映了该位置与观测结果的匹配程度。随着观测不断更新，粒子会逐渐集中到更可能的区域，从而逼近真实的状态分布。

![粒子滤波图像](src\content\posts\filtering-algorithms\粒子滤波1.jpg)

## 蒙特卡洛近似

当系统的状态转移或观测模型存在强非线性或非高斯噪声时，贝叶斯滤波往往无法解析求解。为此粒子滤波引入了蒙特卡罗方法来对后验分布进行数值近似。

设函数 $g(x)$ 关于分布 $P(x)$ 的期望为：

$$
\mathbb{E} \Big[ g(x) \Big] = \int g(x) P(x) \, dx
$$

若能够从分布 $P(x)$ 中独立采样得到 $N$ 个样本 $\{x^{(i)}\}_{i=1}^N$，则该期望可以用样本均值近似为：

$$
\mathbb{E} \Big[ g(x) \Big] \approx \frac{1}{N} \sum_{i=1}^{N} g(x^i)
$$

当 $N \to \infty$ 时，根据 **大数定律** ，该近似将收敛于真实的期望值。

## 序贯重要性采样

在实际问题中，我们通常无法直接从后验分布 $P(x_t | z_{1:t})$ 中采样。为此粒子滤波采用了 **重要性采样** （Importance Sampling） 的思想（具体介绍会在后续的章节中给出）：从一个更容易采样的 **提议分布** $Q(x_t | x_{t-1}, z_t)$ 中生成样本（粒子），再通过加权修正来逼近真实后验分布。

在序贯估计问题中，我们考虑完整的状态轨迹 $x_{0:t}$ ，目标是从后验分布 $P(x_{0:t} | z_{1:t})$ 中抽样。引入提议分布 $Q(x_{0:t} | z_{1:t})$ ，则其重要性权重定义为：

$$
\lambda_t = \frac{P(x_{0:t} | z_{1:t})}{Q(x_{0:t} | z_{1:t})}
$$

若状态满足马尔可夫性质、观测满足条件独立性，则有：

$$
P(x_{0:t} | z_{1:t}) \propto P(z_t | x_t) P(x_t | x_{t-1}) P(x_{0:t-1} | z_{1:t-1})
$$

将两式结合，可得权重的递推形式：

$$
\lambda_t = \frac{P(z_t | x_t) P(x_t | x_{t-1})}{Q(x_t | x_{0:t-1}, z_{1:t})} \lambda_{t-1}
$$

在常见的设置中，我们通常选用状态转移概率作为提议分布，即 $Q(x_t | x_{0:t-1}, z_{1:t}) = P(x_t | x_{t-1})$ ，此时权重更新公式可简化为：

$$
\lambda_t = P(z_t | x_t) \lambda_{t-1}
$$

最后对所有粒子的权重进行归一化：

$$
\bar{\lambda}_t^i = \frac{\lambda_t^i}{\sum_{j=1}^{N} \lambda_t^j}
$$

## FPK 方程

在连续时间的动态系统中，系统状态的演化通常可以用 **随机微分方程** （Stochastic Differential Equation, SDE） 来描述：

$$
dx_t = f(x_t, t) dt + G(x_t, t) dW_t
$$

其中 $f(x_t, t)$ 表示系统的漂移项（drift term）， $G(x_t, t)$ 为扩散系数矩阵（diffusion matrix）， $W_t$ 是 **维纳过程** （Wiener Process），用于描述系统中的随机扰动。

对应于上述随机过程，系统状态的概率密度函数 $P(x, t)$ 满足 Fokker–Planck–Kolmogorov（FPK）方程：

$$
\frac{\partial P(x,t)}{\partial t} = -\sum_{i=1}^{n} \frac{\partial}{\partial x_i} \Big[ f_i(x,t) P(x,t) \Big] + \frac{1}{2} \sum_{i=1}^{n} \sum_{j=1}^{n} \frac{\partial^2}{\partial x_i \partial x_j} \Big[ (GG^{\rm T})_{ij} P(x,t) \Big]
$$

第一项表示 **漂移项的影响** （由系统动力学 $f(x,t)$ 导致的概率流动），第二项则反映 **扩散项的影响** （由噪声传播引起的概率扩散）。

FPK 方程描述了系统状态概率密度在时间上的演化过程。然而在实际问题中直接求解该偏微分方程往往十分困难，尤其是当系统维度较高时。

粒子滤波的核心思想正是通过蒙特卡洛方法来近似求解这一方程：通过在状态空间中生成大量样本（粒子）并随时间演化，用样本的加权分布去逼近 $P(x,t)$ 的动态变化，从而实现对系统状态的估计（这里并不需要完全了解什么是随机微分方程，我们会在扩散模型章节详细讲解这部分的内容）。

## 理论基础

粒子滤波建立在贝叶斯滤波框架之上，因此同样包含贝叶斯滤波的两个核心步骤： **预测** （Prediction）与 **更新** （Update）。

然而，与传统的解析贝叶斯滤波不同，粒子滤波引入了蒙特卡洛方法与重要性采样技术来对复杂的非线性、非高斯分布进行数值近似。为了克服粒子退化问题并获得更稳定的估计结果，粒子滤波在此基础上又增加了 **重采样** （Resampling）与 **状态估计** （Estimation）步骤。

接下来，我们将对粒子滤波的完整推导过程进行详细说明。

### Initialization Step

粒子滤波的第一步是 **初始化** （Initialization），其目标是根据系统的先验分布 $P(x_0)$ 生成初始粒子集合，用以表示系统在初始时刻的状态不确定性。

我们从先验分布中采样得到 $N$ 个粒子（具体粒子个数由人工设定）：

$$
x_0^{(i)} \sim P(x_0) \quad i = 1, 2, \ldots, N
$$

每个粒子代表系统在状态空间中的一个可能位置。由于在初始时刻通常没有观测信息可用于修正先验分布，因此所有粒子的初始权重均相等：

$$
\lambda_0^{(i)} = \frac{1}{N}
$$

此时整组粒子 $\{x_0^{(i)}, \lambda_0^{(i)}\}_{i=1}^N$ 就构成了对初始状态分布 $P(x_0)$ 的离散近似：

$$
P(x_0) \approx \sum_{i=1}^{N} \lambda_0^{(i)} \delta(x_0 - x_0^{(i)})
$$

其中 $\delta(\cdot)$ 为狄拉克 delta 函数，表示概率质量集中在粒子所在的位置（可以参考下方视频了解其直观含义）。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114646350566949&bvid=BV1ZCTDz6E15&cid=30384260188&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

通过这种方式，连续的概率分布被一组带权样本所替代，为后续的预测与更新步骤提供了基础。

### Prediction Step

假设我们已经得到了上一个时刻的后验分布的离散近似：

$$
P(x_{t-1} | z_{1:t-1}) \approx \sum_{i=1}^{N} \lambda_{t-1}^{(i)} \delta(x_{t-1} - x_{t-1}^{(i)})
$$

将上述离散近似公式带入预测公式：

$$
\begin{align*}
P(x_t | z_{1:t-1}) &= \int P(x_t | x_{t-1}) \sum_{i=1}^{N} \lambda_{t-1}^{(i)} \delta(x_{t-1} - x_{t-1}^{(i)}) \, dx_{t-1} \\
&= \sum_{i=1}^{N} \lambda_{t-1}^{(i)} \int P(x_t | x_{t-1}) \delta(x_{t-1} - x_{t-1}^{(i)}) \, dx_{t-1} \\
&= \sum_{i=1}^{N} \lambda_{t-1}^{(i)} P(x_t | x_{t-1}^{(i)})
\end{align*}
$$

> 这个公式告诉我们：预测分布可以看成上一时刻每个粒子通过系统模型推进后的状态分布的加权和。

然而我们 **并不需要** 显式求解出 “上一时刻每个粒子通过系统模型推进后的状态分布” 后再对这个分布采样来得到 $x_t^{(i)}$ （下面的推导是预测步骤的核心关键点）。

因为上一时刻的粒子 $x_{t-1}^{(i)}$ 已经是已知的样本点，根据系统状态方程：

$$
x_t^{(i)} = f(x_{t-1}^{(i)}) + w_t^{(i)}
$$

我们可以当前状态 $x_t$ 的随机性完全来自过程噪声 $w_t^{(i)}$ ，因此我们只需要将原本的粒子 **做一次非线性变换后再随机加噪** 就可以得到新粒子 $x_t^{(i)}$ 。
这些新粒子等价于从条件分布 $P(x_t | x_{t-1}^{(i)})$ 中采样得到的样本。

换言之，每一个新粒子都代表一个条件分布 $P(x_t | x_{t-1}^{(i)})$ ，所有的新粒子及其对应的权重（当前阶段的权重沿用上一次迭代的结果）共同构成了预测分布 $P(x_t | z_{1:t-1})$ 的离散近似。

### Update Step

预测步骤给出了系统在时刻 $t$ 的先验分布的离散近似：

$$
P(x_t | z_{1:t-1}) \approx \sum_{i=1}^{N} \lambda_{t-1}^{(i)} \delta(x_t - x_t^{(i)})
$$

此时新的观测量 $z_t$ 到达，我们希望利用该观测信息对预测结果进行修正，从而得到更接近真实状态的后验分布。

根据贝叶斯滤波更新公式可得：

$$
P(x_t | z_{1:t}) \propto \sum_{i=1}^{N} \lambda_{t-1}^{(i)} P(z_t | x_t^{(i)}) \delta(x_t - x_t^{(i)})
$$

这意味着每个粒子根据其与观测的一致程度（即观测似然）获得新的权重，权重更新公式为：

$$
\lambda_t^{(i)} = \lambda_{t-1}^{(i)} P(z_t | x_t^{(i)})
$$

根据系统观测方程：

$$
z_t = h(x_t) + v_t
$$

在给定 $x_t$ 的情况下，当前观测 $z_t$ 的随机性完全来自观测噪声 $v_t$ ，因此可以直接写出观测似然 $P(z_t | x_t)$ ：

$$
p(z_t | x_t) =
\frac{1}{(2\pi)^{\frac{m}{2}} |R|^{\frac{1}{2}}}
\exp \Big( -\frac{1}{2} (z_t - h(x_t))^{\rm T} R^{-1} (z_t - h(x_t)) \Big)
$$

然后直接代入每个 Prediction Step 得到的粒子参数计算出新的权重，最后还需要进行归一化操作：

$$
\bar{\lambda}_t^{(i)} = \frac{\lambda_t^{(i)}}{\sum_{j=1}^{N} \lambda_t^{(j)}}
$$

### Resampling Step

经过预测和更新后，粒子权重可能出现 **退化现象** ：大部分粒子的权重非常小，只有少数粒子权重占据主导。

这会导致计算效率低下，甚至状态估计失真。为了解决这个问题，需要进行 **重采样** （Resampling），保留高权重粒子，舍弃低权重粒子，同时恢复粒子数量。

假设我们在更新步骤后得到了权重归一化的粒子集合为 $\{x_t^{(i)}, \bar{\lambda}_t^{(i)}\}_{i=1}^N$ 。

然后我们根据归一化权重 $\bar{\lambda}_t^{(i)}$ 构造离散概率分布，并从该分布中 **有放回** 地采样 $N$ 个粒子得到新的粒子集合，权重全部重新设置为 $\frac{1}{N}$ 。

接下来重复 Prediction Step 直至循环结束即可。

## 渐进性分析

粒子滤波使用 $N$ 个粒子对后验分布 $P(x_t|z_{1:t})$ 进行离散近似：

$$
P(x_t | z_{1:t}) \approx \sum_{i=1}^{N} w_t^i \delta(x_t - x_t^i)
$$

对任意可积函数 $\phi$ ，用 $\displaystyle \hat{\phi}_N = \sum_{i=1}^{N} w_t^i \phi(x_t^i)$ 作为 $\displaystyle \int \phi(x) \, P(x | z_{1:t}) \, dx$ 的蒙特卡洛估计。

定义蒙特卡洛误差：

$$
\varepsilon_N = \hat{\phi}_N - \int \phi(x) P(x | z_{1:t}) dx
$$

如果粒子通过最优提议分布采样，并且经过重采样去掉权重偏差，可以将 $\{\phi(x_t^i)\}$ 看作独立同分布样本。

根据中心极限定理：

$$
\sqrt{N} \varepsilon_N = \sqrt{N} \left( \hat{\phi}_N - \mathbb{E}[\phi(x_t)] \right) \rightarrow \mathcal{N}(0, \sigma_\phi^2)
$$

$$
\sigma_\phi^2 = \text{Var}[\phi(x_t)] = \int \left( \phi(x) - \int \phi(x') P(x' | z_{1:t}) dx' \right)^2 P(x | z_{1:t}) dx
$$

当粒子数量 $N \to \infty$ 时，粒子滤波的蒙特卡洛估计 $\hat{\phi}_N$ **渐近无偏** ，且服从正态分布误差衰减，说明粒子滤波能逼近真实贝叶斯后验。

# 粒子滤波代码讲解

粒子滤波是一种基于序贯重要性采样（SIS）的非参数贝叶斯滤波方法，用于对非线性、非高斯系统进行状态估计。它通过一组带权粒子来离散化表示状态分布，并在每个时间步执行 **预测、更新、重采样** 递推。

下面的 Python 代码展示了一个粒子滤波的完整实现：

```py frame="code" title="main.py"
import numpy as np

class ParticleFilter:
    def __init__(self, N, f, h, Q, R, x0_prior):
        self.N = N
        self.f = f; self.Q = Q
        self.h = h; self.R = R

        # 初始化粒子集合
        self.particles = x0_prior(N)
        self.weights = np.ones(N) / N

    def predict(self):
        for i in range(self.N):
            w = np.random.multivariate_normal(np.zeros(self.Q.shape[0]), self.Q)
            self.particles[i] = self.f(self.particles[i]) + w

    def update(self, z):
        for i in range(self.N):
            v = z - self.h(self.particles[i])
            # 高斯观测似然
            likelihood = np.exp(-0.5 * v.T @ np.linalg.inv(self.R) @ v)
            likelihood /= np.sqrt((2*np.pi)**len(z) * np.linalg.det(self.R))
            self.weights[i] *= likelihood
        # 归一化权重
        self.weights /= np.sum(self.weights)

    def resample(self):
        indices = np.random.choice(self.N, size=self.N, p=self.weights)
        self.particles = self.particles[indices]
        self.weights.fill(1.0 / self.N)

    def estimate(self):
        return np.average(self.particles, weights=self.weights, axis=0)
```

# 深层问题思考

1. 贝叶斯滤波预测步骤用全概率公式展开的目的是什么？

贝叶斯滤波在预测步骤使用全概率公式展开的目的是为了利用 **系统的状态转移模型** $P(x_t|x_{t-1})$ 。

换句话说，我们通过全概率公式引入 $x_{t-1}$ 才能把系统动力学方程（状态转移方程）的条件概率 $P(x_t|x_{t-1})$ 利用上。否则我们没办法从上一步的分布 $P(x_{t-1}|z_{1:t-1})$ 过渡到当前的 $P(x_t|z_{1:t-1})$ 。

2. 在粒子滤波的序贯重要性采样理论中，我们为什么通常会选择状态转移概率作为提议分布？

在序贯重要性采样中，随着时间的推移，粒子的权重方差会不断增大，导致大多数粒子的权重接近于零，这一现象称为粒子退化问题。选择合适的提议分布可以有效减缓粒子退化问题。理论上可以证明，在最优提议分布 $Q^*(x_t | x_{t-1}, z_t) = P(x_t | x_{t-1}, z_t)$ 下权重方差最小（具体内容可以看下面这个博客）。

[AMCL深入解析 2/4 - 粒子滤波理论](https://zhuanlan.zhihu.com/p/676901879)

在实际应用中，最优提议分布往往难以直接采样，因此通常采用状态转移概率 $P(x_t | x_{t-1})$ 作为近似。粒子滤波正是基于这一思想：在其预测步骤中，粒子通过状态转移模型采样。

$$
x_t^{(i)} \sim P(x_t | x_{t-1}^{(i)})
$$

这实际上等价于在序贯重要性采样框架下选用状态转移概率作为提议分布。

# 参考文献

## 贝叶斯滤波

1. [Bayes Filter 算法介绍](https://aandds.com/blog/bayes-filter.html)

2. [从概率到贝叶斯滤波](https://zhuanlan.zhihu.com/p/268624245)

3. [贝叶斯滤波器学习笔记](https://blog.csdn.net/jimmychao1982/article/details/149745121)

## 卡尔曼滤波

1. [卡尔曼滤波(Kalman Filter)概念介绍及详细公式推导](https://blog.csdn.net/qq_37214693/article/details/130927283)

2. [【万字长文】让你一文轻松掌握卡尔曼滤波](https://www.cnblogs.com/SkyXZ/p/18660856)

3. [Kalman滤波器的原理与实现](https://www.cnblogs.com/CrescentWind/p/18132934)

4. [卡尔曼滤波（DezemingFamily）](https://zhengyu.tech/upload/2023/08/Kalman%20Filter.pdf)

5. [从贝叶斯到卡尔曼滤波](https://www.cnblogs.com/ishen/p/14987878.html)

6. [从贝叶斯估计到卡尔曼滤波（详细推导）](https://zhuanlan.zhihu.com/p/521538539)

## 扩展卡尔曼滤波

1. [扩展卡尔曼滤波(Extended Kalman Filter)原理](https://zhuanlan.zhihu.com/p/711709657)

2. [扩展卡尔曼滤波器：含例子及代码](https://zhuanlan.zhihu.com/p/672506748)

3. [扩展卡尔曼滤波器实例与推导](https://zhuanlan.zhihu.com/p/550160197)

4. [扩展卡尔曼滤波原理与示例](https://zhuanlan.zhihu.com/p/1934805328899323033)

5. [扩展卡尔曼滤波理论推导与实践](https://blog.csdn.net/qq570437459/article/details/144704211)

## 粒子滤波

1. [【滤波】粒子滤波（PF）](https://blog.csdn.net/qq_38410730/article/details/131214213)

2. [【维基百科】Particle Filter](https://en.wikipedia.org/wiki/Particle_filter)

3. [粒子滤波器解读](https://blog.csdn.net/qq_44648285/article/details/148074482)

4. [粒子滤波理论、方法及其在多目标跟踪中的应用](https://www.researchgate.net/publication/292354427_Particle_filtering_Theory_approach_and_application_for_multitarget_tracking)