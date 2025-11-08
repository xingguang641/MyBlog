---
title: 【机器学习基本模型】第一节：线性回归
published: 2025-10-23
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 线性回归基本原理

**线性回归** （Linear Regression）是一种结构简单、应用广泛、且易于理解的经典机器学习算法，非常适合作为算法学习的入门模型。

它的核心思想是：通过拟合一条线性函数，刻画输入变量与输出变量之间的关系。换句话说，线性回归试图找到一条最能代表数据趋势的直线，使得所有样本点到这条直线的距离总体上最小。

## 多元线性回归介绍

在简单线性回归中，我们通常用一条直线去刻画输入变量与输出变量之间的线性关系。当输入变量扩展到多个维度时，这种思想自然推广至 **多元线性回归** （Multiple Linear Regression）。

多元线性回归的目标是找到一个能够描述输入向量 $x = [x_1, x_2, \ldots, x_n]^{\rm T}$ 与输出变量 $y$ 之间线性关系的函数：

$$
y = w^{\rm T} x + b
$$

其中 $w = [w_1, w_2, \ldots, w_n]^{\rm T}$ 表示各特征对应的权重，$b$ 为偏置项（bias）。

从几何角度来看，这个模型对应于一个 $n$ 维空间中的超平面（hyperplane）。数据样本点通常分布在超平面的两侧，而训练的过程，就是要调整 $w$ 和 $b$，使这个超平面尽可能地贴近所有数据点，从而最小化整体预测误差。

![线性回归图像](src/content/posts/linear-regression/线性回归分析1.jpg)

# 代码讲解

建议先看代码部分，若有不理解的地方，可结合后续的讲解对照理解。

```py frame="code" title="main.py"
import numpy as np
data = np.array([
    [32, 31], [53, 68], [61, 62], [47, 71], [59, 87],
    [55, 78], [52, 79], [39, 59], [48, 75], [52, 71],
    [45, 55], [54, 82], [44, 62], [58, 75], [56, 81],
    [48, 60], [44, 82], [60, 97], [45, 48], [38, 56],
    [66, 83], [65, 118], [47, 57], [41, 51], [51, 75],
    [59, 74], [57, 95], [63, 95], [46, 79], [50, 83]
])


# 损失函数
def loss_func(w, b, data):
    total_cost = 0
    for i in range(len(data)):
        x, y = data[i]
        total_cost += (w * x + b - y) ** 2
    return total_cost / len(data)
# 梯度下降
def grad_desc(cur_w, cur_b, alpha, data):
    sum_w = 0
    sum_b = 0
    # 对每个点，代入公式求和
    for i in range(len(data)):
        x, y = data[i]
        sum_w += (cur_w * x + cur_b - y) * x
        sum_b += cur_w * x + cur_b - y
    # 用公式求当前梯度
    grad_w = 2 / len(data) * sum_w
    grad_b = 2 / len(data) * sum_b
    # 梯度下降，更新当前的w和b
    updated_w = cur_w - alpha * grad_w
    updated_b = cur_b - alpha * grad_b
    return updated_w, updated_b
# 主函数
def main(data, initial_w, initial_b, alpha, num_iter):
    w = initial_w
    b = initial_b
    # 定义一个list保存所有的损失函数值，用来显示下降的过程
    cost_list = []
    for i in range(num_iter):
        cost_list.append(loss_func(w, b, data))
        w, b = grad_desc(w, b, alpha, data)
    return [w, b, cost_list]


# 设置超参数
alpha = 0.0001
initial_w = 0
initial_b = 0
num_iter = 10
# 执行代码
if __name__ == "__main__":
    w, b, cost_list = main(data, initial_w, initial_b, alpha, num_iter)
    print("\n训练结束")
    print("w =", w)
    print("b =", b)
    cost = loss_func(w, b, data)
    print("cost =", cost)
```

## 损失函数

线性回归使用的损失函数是最常见的 **均方误损失** （Mean Squared Error）。

```py showLineNumbers
def loss_func(w, b, data):
    total_cost = 0
    for i in range(len(data)):
        x, y = data[i]
        total_cost += (w * x + b - y) ** 2
    return total_cost / len(data)
```

均方损失函数的数学表达式如下：

$$
L(w, b) = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

其中：

- $L$：表示均方损失
- $n$：样本数量
- $y_i$：第 $i$ 个样本的真实值（真实标签）
- $\hat{y}_i$：第 $i$ 个样本的预测值

根据线性回归公式 $$\hat{y}_i = \hat{w} x_i + \hat{b}$$ ，替换掉公式中的 $\hat{y}_i$ 即可得到代码中的公式。

## 梯度下降

由于这是我们第一次接触 **梯度下降** （Gradient Descent），这里先给出它的基本形式。梯度下降是一种常用的参数优化方法，其核心思想是：沿着目标函数梯度的反方向不断调整参数，使损失函数逐步减小，直到收敛到最优值。

其参数更新的基本公式如下：

$$
w \leftarrow w - \alpha \frac{\partial L}{\partial w}
$$

$$
b \leftarrow b - \alpha \frac{\partial L}{\partial b}
$$

```py showLineNumbers
def grad_desc(cur_w, cur_b, alpha, data):
    sum_w = 0
    sum_b = 0
    # 对每个点，代入公式求和
    for i in range(len(data)):
        x, y = data[i]
        sum_w += (cur_w * x + cur_b - y) * x
        sum_b += cur_w * x + cur_b - y
    # 用公式求当前梯度
    grad_w = 2 / len(data) * sum_w
    grad_b = 2 / len(data) * sum_b
    # 梯度下降，更新当前的w和b
    updated_w = cur_w - alpha * grad_w
    updated_b = cur_b - alpha * grad_b
    return updated_w, updated_b
```

梯度下降的关键就是求出偏导数，因此我们推导一下线性回归损失函数的两个偏导数：

$$
L(w,b) = \frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2
= \frac{1}{n}\sum_{i=1}^n \bigl(y_i - (w x_i + b)\bigr)^2
$$

我们先对 $w$ 求偏导，令误差 $e_i = y_i - (w x_i + b)$ ，那么：

$$
L(w, b) = \frac{1}{n}\sum_{i=1}^n e_i^2
$$

对 $w$ 求导（分步）：

- 使用链式法则 $\dfrac{\partial}{\partial w} e_i^2 = 2 e_i \dfrac{\partial e_i}{\partial w}$

- 然后有 $\dfrac{\partial e_i}{\partial w} = \dfrac{\partial}{\partial w}\bigl(y_i - (w x_i + b)\bigr) = -x_i$

把这些代回：

$$
\begin{aligned}
\frac{\partial L(w, b)}{\partial w}
&= \frac{1}{n}\sum_{i=1}^n 2 e_i \left(-x_i\right) = -\frac{2}{n}\sum_{i=1}^n e_i x_i \\
&= -\frac{2}{n}\sum_{i=1}^n \bigl(y_i - (w x_i + b)\bigr) x_i
\end{aligned}
$$

同理，对 $b$ 求导 $\dfrac{\partial e_i}{\partial b} = -1$ ，因此：

$$
\begin{aligned}
\frac{\partial L(w, b)}{\partial b}
&= \frac{1}{n}\sum_{i=1}^n 2 e_i \left(-1\right) = -\frac{2}{n}\sum_{i=1}^n e_i \\
&= -\frac{2}{n}\sum_{i=1}^n \bigl(y_i - (w x_i + b)\bigr)
\end{aligned}
$$

# 参考文献

1. [机器学习之线性回归算法Linear Regression](https://blog.csdn.net/qq_41750911/article/details/124883520)