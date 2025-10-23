---
title: 【机器学习基本模型】第一节：线性回归
published: 2025-10-23
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 线性回归基本原理

线性回归（Linear Regression）是一种非常简单、用处非常广泛、含义也非常容易理解的一类经典算法，非常合适作为机器学习的入门算法。

线性回归就是想办法拟合出一个线性组合关系的函数。要找一条直线，并且让这条直线尽可能地拟合所有数据点。即：试图找到一条直线，使所有样本到直线上的欧式距离之和最小。

## 多元线性回归介绍

我们的目标是拟合出一个线性组合关系的函数： $y = w x + b$

这个模型的几何含义是多维空间中的超平面，而数据点散落在超平面的两侧。

![线性回归图像](src/content/posts/linear-regression/线性回归分析1.jpg)

## 代码讲解

先看代码内容，有不懂的地方再看下面的讲解

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

### 损失函数

线性回归使用的损失函数是最常见的均方误差（Mean Squared Error）

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
L = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

其中：

- $L$：表示均方损失
- $n$：样本数量
- $y_i$：第 $i$ 个样本的真实值（真实标签）
- $\hat{y}_i$：第 $i$ 个样本的预测值

根据线性回归公式 $$\hat{y}_i = \hat{w} x_i + \hat{b}$$ ，替换掉公式中的 $\hat{y}_i$ 即可得到代码中的公式

### 梯度下降

由于这是第一次介绍梯度下降，就把梯度下降的公式放出来吧，梯度下降法更新参数为：

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

梯度下降的关键就是求出偏导数，因此我们推导一下线性回归损失函数的两个偏导数

$$
L(w,b) = \frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2
= \frac{1}{n}\sum_{i=1}^n \bigl(y_i - (w x_i + b)\bigr)^2
$$

我们先对 $w$ 求偏导，令误差 $e_i = y_i - (w x_i + b)$ ，那么：

$$
L = \frac{1}{n}\sum_{i=1}^n e_i^2
$$

对 $w$ 求导（分步）：

1. 使用链式法则 $\dfrac{\partial}{\partial w} e_i^2 = 2 e_i \dfrac{\partial e_i}{\partial w}$

2. 而 $\dfrac{\partial e_i}{\partial w} = \dfrac{\partial}{\partial w}\bigl(y_i - (w x_i + b)\bigr) = -x_i$

把这些代回：

$$
\begin{aligned}
\frac{\partial L}{\partial w}
&= \frac{1}{n}\sum_{i=1}^n 2 e_i \left(-x_i\right) = -\frac{2}{n}\sum_{i=1}^n e_i x_i \\
&= -\frac{2}{n}\sum_{i=1}^n \bigl(y_i - (w x_i + b)\bigr) x_i
\end{aligned}
$$

同理，对 $b$ 求导 $\dfrac{\partial e_i}{\partial b} = -1$ ，因此：

$$
\begin{aligned}
\frac{\partial L}{\partial b}
&= \frac{1}{n}\sum_{i=1}^n 2 e_i \left(-1\right) = -\frac{2}{n}\sum_{i=1}^n e_i \\
&= -\frac{2}{n}\sum_{i=1}^n \bigl(y_i - (w x_i + b)\bigr)
\end{aligned}
$$

# 参考文献

1. [机器学习之线性回归算法Linear Regression](https://blog.csdn.net/qq_41750911/article/details/124883520)