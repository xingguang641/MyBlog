---
title: 【机器学习基本模型】第一节：线性回归
published: 2025-10-23
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 线性回归基本原理

**线性回归（Linear Regression）** 是机器学习中最基础、最经典的算法之一。尽管其结构简单，但它揭示了从数据中学习规律的核心思想，是学习更复杂算法（如神经网络）的基石。

其核心思想非常直观：**通过拟合一个线性函数，来刻画输入变量与输出变量之间的定量关系** 。通俗地说，线性回归试图在数据点中找到一条 “最佳拟合直线（或超平面）” ，使得所有样本点到这条直线的 “综合距离” 最小，从而能够根据新的输入预测出合理的输出。

## 从简单到多元

在最简单的情况下，我们只有一个输入特征 $x$ 。例如仅根据 “房屋面积” 来预测 “房价” ，模型的形式就是最熟悉的直线方程：

$$
y = wx + b
$$

当输入变量扩展到多个维度时（例如根据 “面积” 、“房龄” 、“距离地铁距离” 共同预测 “房价” ），这种思想就自然地推广为 **多元线性回归（Multiple Linear Regression）**。此时模型的目标是找到一个函数，让它能够描述输入向量 $x = [x_1, x_2, \ldots, x_n]^{\rm T}$ 与输出变量 $y$ 之间的关系：

$$
y = w^{\rm T} x + b
$$

其中 $w = [w_1, w_2, \ldots, w_n]^{\rm T}$ 是权重向量（Weight），表示每个特征的重要性。$b$ 是偏置项（Bias），表示截距。从几何角度看，这个模型对应于 $n$ 维空间中的一个 **超平面（Hyperplane）**。训练模型的过程，本质上就是不断调整 $w$ 和 $b$ ，使这个超平面尽可能贴近所有训练数据点，从而最小化预测误差。

![线性回归图像](src\content\posts\regression-model\线性回归分析1.jpg)

---

# 线性回归代码讲解

为了便于理解和可视化，下面的代码展示了 **简单线性回归（单特征）** 的基本实现过程（建议先通读一遍代码以建立整体印象，若有细节暂时不理解，可在阅读后文的 “原理讲解” 部分时再回头对照理解）。

```py frame="code" title="linear_regression.py"
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

## 1. 损失函数

如何衡量模型预测的准确性？我们需要一个评估指标。在线性回归中，最常用的指标是 **均方误差**（Mean Squared Error，简称 MSE）。下面给出对应的代码实现：

```py showLineNumbers
def loss_func(w, b, data):
    total_cost = 0
    for i in range(len(data)):
        x, y = data[i]
        total_cost += (w * x + b - y) ** 2
    return total_cost / len(data)
```

函数 `loss_func` 对应的数学公式为：

$$
L(w, b) = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

其中：

* $y_i$ ：第 $i$ 个样本的真实标签。
* $\hat{y}_i = w x_i + b$ ：模型对第 $i$ 个样本的预测值。
* $(y_i - \hat{y}_i)^2$ ：预测误差的平方。

## 2. 梯度下降

在有了损失函数之后，我们的目标就是找到使损失最小的最优参数 $w$ 和 $b$ 。当解析解不可行或特征维度较高时，最常用的方法便是 **梯度下降（Gradient Descent）**———— 根据损失函数的梯度不断更新参数，就像沿着山坡的最陡方向一步步 “下山” 。

参数更新公式为：

$$
w \leftarrow w - \alpha \frac{\partial L}{\partial w} \quad\quad b \leftarrow b - \alpha \frac{\partial L}{\partial b}
$$

其中 $\alpha$ 是 **学习率（Learning Rate）**，用于控制每一步更新的幅度。

```py showLineNumbers
def grad_desc(cur_w, cur_b, alpha, data):
    sum_w = 0
    sum_b = 0
    # 对每个样本点，累加梯度
    for i in range(len(data)):
        x, y = data[i]
        sum_w += (cur_w * x + cur_b - y) * x
        sum_b += cur_w * x + cur_b - y
    # 计算当前梯度
    grad_w = 2 / len(data) * sum_w
    grad_b = 2 / len(data) * sum_b
    # 更新参数
    updated_w = cur_w - alpha * grad_w
    updated_b = cur_b - alpha * grad_b
    return updated_w, updated_b
```

### 梯度推导

令误差项 $e_i = (w x_i + b) - y_i$ ，损失函数可以写为：

$$
L = \frac{1}{n}\sum e_i^2
$$

根据链式法则，可以得到：

1. **对 $w$ 求偏导**

$$
\frac{\partial L}{\partial w} = \frac{1}{n} \sum_{i=1}^{n} 2 e_i \cdot \frac{\partial e_i}{\partial w} = \frac{2}{n} \sum_{i=1}^{n} \underbrace{((w x_i + b) - y_i)}_{\text{误差}} \cdot x_i
$$

2. **对 $b$ 求偏导**

$$
\frac{\partial L}{\partial b} = \frac{1}{n} \sum_{i=1}^{n} 2 e_i \cdot \frac{\partial e_i}{\partial b} = \frac{2}{n} \sum_{i=1}^{n} ((w x_i + b) - y_i)
$$

代码中的更新规则正是对上述推导的直接实现。

## 3. 内容拓展

虽然在本示例中使用梯度下降进行训练，但对于线性回归这种凸优化问题，其实可以通过 **最小二乘法（Least Squares）** 直接求得参数的闭式解，也就是所谓的 **解析解（Analytical Solution）**。

### 统计视角下的推导

假设真实数据生成过程为：

$$
y_i = \beta_0 + \beta_1 x_i + \varepsilon_i
$$

其中 $\varepsilon_i$ 是随机噪声。

为了让模型拟合效果最佳，我们希望最小化残差平方和（SSE）：

$$
J(\beta_0, \beta_1) = \sum_{i=1}^{n} \big(y_i - (\beta_0 + \beta_1 x_i)\big)^2
$$

这是一个求极值的问题。通过对 $\beta_0$ 和 $\beta_1$ 分别求偏导并令其为 0，可以得到最优参数的闭式解：

$$
\hat{\beta}*1 = \frac{\sum*{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2}
$$

$$
\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}
$$

（注：这里的 $\beta_1$ 对应前文的 $w$ ，$\beta_0$ 对应前文的 $b$ ）

### 为什么仍需要梯度下降？

1. **计算复杂度**：解析解需要计算矩阵的逆（尤其在多元回归中），当特征维度很高时，计算量会非常大。而梯度下降通过迭代逼近最优解，在海量数据场景下更加高效。
2. **通用性**：大多数复杂的机器学习模型（如深度神经网络）没有解析解，必须依赖梯度下降或其变种进行优化。因此在线性回归中学习梯度下降，不仅能理解优化机制，也为后续复杂模型的学习打下基础。

---

# 参考文献列表

1. [机器学习之线性回归算法 Linear Regression](https://blog.csdn.net/qq_41750911/article/details/124883520)

2. [【方法与实践】最小二乘估计讲解](https://otexts.com/fppcn/least-squares.html)