---
title: 【机器学习基本模型】第二节：逻辑回归
published: 2025-10-23
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 逻辑回归基本原理

在上一节的线性回归中，我们解决的是回归问题（预测连续值）。而在模式识别与机器学习中，我们更常遇到的是 **分类任务** ，例如判断一封邮件是否为垃圾邮件，或者判断一个人是否患有某种疾病。

对于这类二分类问题，输出标签通常为 $y \in \{0, 1\}$ 。如果我们直接使用线性回归模型预测，输出值可能会远超 0 到 1 的范围，这在概率解释上是不合理的。为此，我们在线性模型的基础上引入了一个非线性激活函数 $g: \mathbb{R} \to (0,1)$ ，将线性预测值映射为类别标签的后验概率 $P(y = 1 | \mathbf{x})$ 。

## 对数几率回归 (Logistic Regression)

在 **逻辑回归（Logistic Regression）** 中，选用的激活函数为 **Sigmoid 函数** ，其表达式为：

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

模型的预测目标是样本属于正类（ $y=1$ ）的后验概率：

$$
P(y = 1 | \mathbf{x}) = \sigma(\mathbf{w}^{\rm T} \mathbf{x}) = \frac{1}{1 + e^{-\mathbf{w}^{\rm T} \mathbf{x}}}
$$

为了简化公式，我们通常采用 **增广向量** 的形式：
*   增广特征向量 $\mathbf{x} = [x_1, \cdots, x_D, 1]^{\rm T}$
*   增广权重向量 $\mathbf{w} = [w_1, \cdots, w_D, b]^{\rm T}$

此时，样本属于负类（ $y=0$ ）的后验概率为：

$$
P(y=0 | \mathbf{x}) = 1 - P(y=1 | \mathbf{x}) 
= 1 - \sigma(\mathbf{w}^{\rm T} \mathbf{x}) 
= \frac{e^{- \mathbf{w}^{\rm T} \mathbf{x}}}{1 + e^{- \mathbf{w}^{\rm T} \mathbf{x}}}
$$

通过推导，我们可以发现线性模型 $\mathbf{w}^{\rm T} \mathbf{x}$ 与概率之间的关系：

$$
\mathbf{w}^{\rm T} \mathbf{x} 
= \ln \frac{P(y=1 | \mathbf{x})}{1 - P(y=1 | \mathbf{x})} 
= \ln \frac{P(y=1 | \mathbf{x})}{P(y=0 | \mathbf{x})}
$$

上式左边为线性函数，右边为正反后验概率比值（几率，Odds）的对数。因此，Logistic 回归也被称为 **对数几率回归** 。

![逻辑回归图像](src\content\posts\logistic-regression\逻辑回归分析1.jpg)

---

# 代码讲解

下面通过 Python 的 NumPy 库手写实现一个逻辑回归模型。为了使代码更加简洁且贴近数学公式的定义，本示例使用了 **匿名函数（Lambda Function）** 。

> **注意**：为了与理论部分的 “增广向量” 保持一致，我们在代码中会对输入特征 $X$ 增加一列全为 1 的数据，从而将偏置 $b$ 合并到权重 $w$ 中进行统一更新，这样也修复了原代码中函数返回值解包不匹配的问题。

```py frame="code" title="main.py"
import numpy as np
np.random.seed(0)
X = np.random.randn(100, 2)
true_w = np.array([2, -1])
sigmoid = lambda x: 1 / (1 + np.exp(-x))
y = (sigmoid(X @ true_w) > 0.5).astype(int)


# 激活函数
sigmoid = lambda x: 1 / (1 + np.exp(-x))
# 损失函数
loss_func = lambda X, y, w: -np.mean(
    y * np.log(sigmoid(X @ w)) + (1 - y) * np.log(1 - sigmoid(X @ w))
)
# 梯度下降
gradient = lambda X, y, w: X.T @ (sigmoid(X @ w) - y) / len(y)
def grad_desc(cur_w, alpha, X, y):
    grad = gradient(X, y, cur_w)
    updated_w = cur_w - alpha * grad
    return updated_w
# 主函数
def main(X, y, initial_w, alpha, num_iter):
    w = initial_w
    # 定义一个list保存所有的损失函数值，用来显示下降的过程
    cost_list = []
    for i in range(num_iter):
        cost_list.append(loss_func(X, y, w))
        w, b = grad_desc(w, alpha, X, y)
    return [w, b, cost_list]


# 设置超参数
alpha = 0.1
initial_w = np.zeros(X.shape[1])
num_iter = 1000
# 执行代码
if __name__ == "__main__":
    w, cost_list = main(X, y, initial_w, alpha, num_iter)
    print("\n训练结束")
    print("w =", w)
    cost = loss_func(X, y, w)
    print("cost =", cost)
```

## 1. 损失函数

与线性回归使用均方误差（MSE）不同，逻辑回归采用 **交叉熵损失（Cross-Entropy Loss）** 。主要原因在于，如果将 Sigmoid 函数代入 MSE 损失中，得到的损失函数关于权重 $w$ 是非凸的（Non-Convex），存在多个局部极小值，不利于梯度下降寻找全局最优解。而交叉熵损失函数则是凸函数，具有良好的优化性质。

> 更多细节可以参考以下视频深入了解

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114675626875309&bvid=BV12VMzzxExF&cid=30475028383&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

简单看一下代码中的损失函数：

```py showLineNumbers
loss_func = lambda X, y, w: -np.mean(
    y * np.log(sigmoid(X @ w)) + (1 - y) * np.log(1 - sigmoid(X @ w))
)
```

交叉熵损失函数的数学表达式如下：

$$
J(\mathbf{w}) = -\frac{1}{N} \sum_{i=1}^{N} \Big[ y_i \ln(\hat{y}_i) + (1 - y_i)\ln(1 - \hat{y}_i) \Big]
$$

其中 $\hat{y}_i = \sigma(\mathbf{x}_i \mathbf{w})$ 。

## 2. 梯度下降

逻辑回归模型在形式上只是比线性回归多嵌套了一层激活函数。从微积分的角度看，这仅增加了链式法则的一个环节。代码中的梯度计算非常简洁：

```py showLineNumbers
gradient = lambda X, y, w: X.T @ (sigmoid(X @ w) - y) / len(y)
def grad_desc(cur_w, alpha, X, y):
    grad = gradient(X, y, cur_w)
    updated_w = cur_w - alpha * grad
    return updated_w
```

其数学推导过程如下：

- 预测值

$$
\hat{y} = \sigma(X\mathbf{w}) = \frac{1}{1 + e^{-X\mathbf{w}}}
$$

- 损失函数

$$
J(\mathbf{w}) = -\frac{1}{N} \sum_{i=1}^{N} \Big[ y_i \ln(\hat{y}_i) + (1 - y_i)\ln(1 - \hat{y}_i) \Big]
$$

- 对权重求导

$$
\nabla J(\mathbf{w}) = \frac{\partial J(\mathbf{w})}{\partial \mathbf{w}}
= \frac{1}{N} X^{\rm T} (\hat{y} - y)
$$

这个结果的形式与线性回归的梯度惊人地相似（仅仅是 $\hat{y}$ 的定义不同），这正是 **广义线性模型（GLM）** 的优美之处。

## 3. 内容拓展

Logistic 回归本质上是一个 **线性分类器** ，其决策边界是线性的（即 $\mathbf{w}^{\rm T} \mathbf{x} = 0$ 是一个超平面）。对于 **线性不可分** 的数据，我们可以通过 **特征工程** 来提升模型的表达能力。

常见的特征扩展（Feature Expansion）方法包括：

- **多项式特征**：引入 $x_1^2, x_2^2, x_1x_2$ 等高阶项，使决策边界变为椭圆、抛物线等曲线。
- **交互特征**：构造特征之间的乘积、比值等，刻画变量间的耦合关系。

本质上，这是通过将低维的原始特征映射到高维空间，使得数据在高维空间中变得线性可分。但需要警惕的是，特征维度过高容易导致 **过拟合（Overfitting）** ，通常需要配合正则化（L1/L2 Regularization）使用。

---

# 深层问题思考

1. 为什么逻辑回归在线性回归的基础上套一层激活函数就可以进行分类呢？

    这个问题可以从 **直观理解** 和 **数学本质** 两个层面来回答：

    **直观理解：数值区间的映射**
    线性回归的预测输出 $z = \mathbf{w}^{\rm T} \mathbf{x}$ 的范围是 $(-\infty, +\infty)$ ，而二分类任务要求的概率 $P(y=1|\mathbf{x})$ 必须处于 $[0, 1]$ 之间。Sigmoid 函数 $\sigma(z)$ 的作用就是将任意实数 **映射（压缩）** 到 $(0, 1)$ 区间，使其具有 “概率” 的物理意义。

    **数学本质：对数几率的线性假设**
    逻辑回归本质上是 **广义线性模型** 的一种。我们并非随意选择了一个激活函数，而是基于一个核心假设：**样本为正类的 “对数几率” 与输入特征之间存在线性关系** 。

    几率定义为正类概率与负类概率的比值：
    
    $$
    \frac{P(y=1|\mathbf{x})}{P(y=0|\mathbf{x})}
    $$
    
    对几率取对数，即得到 **Logit 变换**：

    $$
    \text{logit}(P) = \ln \frac{P(y=1 | \mathbf{x})}{P(y=0 | \mathbf{x})} = \mathbf{w}^{\rm T} \mathbf{x}
    $$

    如果我们对上述公式进行 **逆变换** ，求解 $P(y=1 | \mathbf{x})$ ，就会自然导出 Sigmoid 函数的形式：

    $$
    \frac{P}{1-P} = e^{\mathbf{w}^{\rm T} \mathbf{x}} \implies P(y=1 | \mathbf{x}) = \frac{1}{1 + e^{- \mathbf{w}^{\rm T} \mathbf{x}}} = \sigma(\mathbf{w}^{\rm T} \mathbf{x})
    $$

    **结论**：Sigmoid 函数并非仅仅是 “套” 在外部的一层壳，它是 **对数几率线性假设** 在概率空间上的 **逆映射** 。

---

# 参考文献

1. [Logistic回归（逻辑回归）原理详解](https://blog.csdn.net/weixin_50744311/article/details/131523136)

2. [Scikit-Learn 官方文档: LogisticRegression](https://scikit-learn.cn/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)