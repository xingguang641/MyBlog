---
title: 【机器学习基本模型】第三节：高斯判别分析
published: 2025-10-24
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: true
---

# 高斯判别基本原理

虽然逻辑回归在机器学习任务中的效果非常好，但在样本呈现特殊分布的情况下，我们可以使用其他更好的算法。**高斯判别分析**（Gaussian Discriminant Analysis，简称 GDA）就是其中的一个。这篇博客的主要内容，就是介绍高斯判别分析算法的主要原理以及公式的推导。

![高斯判别分析图像](.\高斯判别模型1.jpg)

## 基本先验假设

与逻辑回归不同，高斯判别分析需要两个先验假设，分别为：

- 类别标签 $y$ 服从伯努利分布

    $$
    P(y) =
    \begin{cases}
    \phi^{y}(1 - \phi)^{1 - y} & y = 0, 1 \\\\
    0 & y \ne 0, 1
    \end{cases}
    $$

- 正负样本均符合正态分布

    $$
    P(x \mid y = 0)
    = \frac{1}{(2\pi)^{\frac{n}{2}} |\Sigma|^{\frac{1}{2}}}
    \exp\!\left(
        -\frac{1}{2} (x - \mu_0)^{\rm T} \Sigma^{-1} (x - \mu_0)
    \right)
    $$

    $$
    P(x \mid y = 1)
    = \frac{1}{(2\pi)^{\frac{n}{2}} |\Sigma|^{\frac{1}{2}}}
    \exp\!\left(
        -\frac{1}{2} (x - \mu_1)^{\rm T} \Sigma^{-1} (x - \mu_1)
    \right)
    $$

正因为在模型中我们需要预先假设样本服从正态分布，这也是 “高斯判别分析” 名字的由来。

有了以上的假设之后，我们就能进行下一步的推导。

## 对数似然函数

在前面的先验假设中，我们需要用到 $\phi$ 、$\Sigma$ 、$\mu_0$ 和 $\mu_1$ 等参数，所以我们先要给出这些参数的参数估计。

首先我们要求出对数似然函数。对于整个数据集，似然函数是：

$$
\prod_{i=1}^m P(x^{(i)}, y^{(i)} \mid \phi, \Sigma, \mu_0, \mu_1) = \prod_{i=1}^m P(x^{(i)} \mid y^{(i)}) P(y^{(i)})
$$

取对数后，得到的对数似然函数：

$$
L(\phi, \Sigma, \mu_0, \mu_1) = \sum_{i=1}^m \left[ \log P(x^{(i)} \mid y^{(i)}) + \log P(y^{(i)}) \right]
$$

### 分解条件概率

为了便于处理不同类别的数据，我们将条件概率项 $\log P(x^{(i)} \mid y^{(i)})$ 根据 $y^{(i)}$ 的值进行分解。由于 $y^{(i)}$ 是二值的，我们可以使用 $y^{(i)}$ 作为指示函数：

- 当 $y^{(i)} = 1$ 时，$\log P(x^{(i)} \mid y^{(i)}) = \log P(x^{(i)} \mid y^{(i)} = 1)$
- 当 $y^{(i)} = 0$ 时，$\log P(x^{(i)} \mid y^{(i)}) = \log P(x^{(i)} \mid y^{(i)} = 0)$

因此，求和项可以重写为：

$$
\sum_{i=1}^m \log P(x^{(i)} \mid y^{(i)}) = \sum_{i=1}^m \left[ y^{(i)} \log P(x^{(i)} \mid y=1) + (1-y^{(i)}) \log P(x^{(i)} \mid y=0) \right]
$$

带入对数似然函数可得：

$$
L(\phi, \Sigma, \mu_0, \mu_1) = \sum_{i=1}^m \left[ y^{(i)} \log P(x^{(i)} \mid y=1) + (1-y^{(i)}) \log P(x^{(i)} \mid y=0) \right] + \sum_{i=1}^m \log P(y^{(i)})
$$

---

# 高斯判别代码讲解

不同于前面两个模型，高斯判别模型是 **闭式解** 的分类器，无需梯度下降之类的梯度迭代。因此高斯判别分析的代码非常简单，下面是完整代码：

```py frame="code" title="main.py"
import numpy as np
from sklearn.datasets import make_classification
X, y = make_classification(
    n_samples=500,
    n_features=5,
    n_classes=2,
    n_informative=5,
    n_redundant=0,
    random_state=42
)


class GDA:
    def __init__(self):
        self.phi = None
        self.mu0 = None
        self.mu1 = None
        self.sigma = None

    # 求解出四个关键参数
    def fit(self, X, y):
        m, _ = X.shape

        # 1. 计算先验概率 phi
        self.phi = np.mean(y)

        # 2. 计算各类别均值 mu0, mu1
        self.mu0 = np.mean(X[y == 0], axis=0)
        self.mu1 = np.mean(X[y == 1], axis=0)

        # 3. 向量化计算协方差矩阵 Sigma
        diff0 = X[y == 0] - self.mu0
        diff1 = X[y == 1] - self.mu1
        self.sigma = (diff0.T @ diff0 + diff1.T @ diff1) / m

    # 求解出线性判别函数的两个参数
    def predict_proba(self, X):
        inv_sigma = np.linalg.inv(self.sigma)
        
        # 线性判别函数参数
        w = inv_sigma @ (self.mu1 - self.mu0)

        b = (
              np.log(self.phi / (1 - self.phi))
            + 0.5 * self.mu0.T @ inv_sigma @ self.mu0
            - 0.5 * self.mu1.T @ inv_sigma @ self.mu1
        )
        
        return 1 / (1 + np.exp(-(X @ w + b)))

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)


# 执行代码
if __name__ == "__main__":    
    model = GDA()
    model.fit(X, y)
    y_pred = model.predict(X)
    print("准确率：", np.mean(y_pred == y))
```

## 1. 先验参数求解

接[上面](#似然函数-likelihood-function)所说，我们要想满足先验，首先就要求解出四个关键参数。根据极大似然估计的原理，我们要想使得模型最优，就要让似然函数取到最大值，这等价于让对数似然函数取到最大值。因此我们可以对四个关键参数求偏导来得到四个参数的具体值：

```py showLineNumbers
def fit(self, X, y):
    m, _ = X.shape

    # 1. 计算先验概率 phi
    self.phi = np.mean(y)

    # 2. 计算各类别均值 mu0, mu1
    self.mu0 = np.mean(X[y == 0], axis=0)
    self.mu1 = np.mean(X[y == 1], axis=0)

    # 3. 向量化计算协方差矩阵 Sigma
    diff0 = X[y == 0] - self.mu0
    diff1 = X[y == 1] - self.mu1
    self.sigma = (diff0.T @ diff0 + diff1.T @ diff1) / m
```

根据最大似然估计（MLE）的原理，我们对每个参数求偏导，并令其等于零即可解出参数的估计值。

- 参数 $\phi$ 的估计

    参数 $\phi = P(y=1)$ 是类别标签 $y$ 的伯努利分布的参数。由于 $\phi$ 只存在于 $\displaystyle \sum_{i=1}^m \log P(y^{(i)})$ 一项中，我们可以单独对这一项求导：

    $$
    \begin{aligned}
    \frac{\partial L(\phi, \Sigma, \mu_0, \mu_1)}{\partial \phi} 
    &= \frac{\partial \sum_{i=1}^m \log P(y^{(i)})}{\partial \phi} \\
    &= \frac{\partial \sum_{i=1}^m \log \phi^{y^{(i)}}(1 - \phi)^{1 - y^{(i)}}}{\partial \phi} \\
    &= \frac{\partial \sum_{i=1}^m y^{(i)} \log \phi + (1 - y^{(i)}) \log (1 - \phi)}{\partial \phi} \\
    &= \sum_{i=1}^m y^{(i)} \frac{1}{\phi} - (1 - y^{(i)}) \frac{1}{1 - \phi}
    \end{aligned}
    $$

    令导数等于零，解得：

    $$
    \phi = \frac{1}{m} \sum_{i=1}^m \frac{y^{(i)}}{y^{(i)} + (1 - y^{(i)})} = \frac{1}{m} \sum_{i=1}^m y^{(i)}
    $$

    这正是 **正样本在总样本中的比例** ，符合我们对先验概率 $\phi$ 的直观理解。

- 均值向量 $\mu_k$ 的估计

    我们假设 $\mu_0$ 和 $\mu_1$ 分别是 $y=0$ 和 $y=1$ 时的条件均值向量。
    
    以 $\mu_1$ 为例，它只出现在条件概率 $P(x | y=1)$ 项中，因此有：

    $$
    \begin{aligned}
    \frac{\partial L(\phi, \Sigma, \mu_0, \mu_1)}{\partial \mu_1} 
    &= \frac{\partial \sum_{i=1}^m y^{(i)} \log P(x^{(i)} | y^{(i)} = 1)}{\partial \mu_1} \\
    &= \frac{\partial \sum_{i=1}^m y^{(i)} \log \frac{1}{(2\pi)^{\frac{n}{2}} |\Sigma|^{\frac{1}{2}}} \exp(-\frac{1}{2}(x - \mu_1)^{\rm T} \Sigma^{-1}(x - \mu_1))}{\partial \mu_1} \\
    &= \sum_{i=1}^m y^{(i)} \Sigma^{-1}(x^{(i)} - \mu_1)
    \end{aligned}
    $$

    令导数为零解得：

    $$
    \mu_1 = \frac{\sum_{i=1}^m y^{(i)} x^{(i)}}{\sum_{i=1}^m y^{(i)}}
    $$

    同理可得：

    $$
    \mu_0 = \frac{\sum_{i=1}^m (1 - y^{(i)}) x^{(i)}}{\sum_{i=1}^m (1 - y^{(i)})}
    $$

    这两个结果分别表示 **正样本和负样本的样本均值** 。

- 协方差矩阵 $\Sigma$ 的估计

    相对于上面三个参数，求解 $\Sigma$ 则更要复杂一些：

    $$
    \begin{aligned}
    \frac{\partial L(\phi, \Sigma, \mu_0, \mu_1)}{\partial \Sigma} 
    &= \frac{\partial \sum_{i=1}^m y^{(i)} \log P(x^{(i)} | y^{(i)} = 1) + \sum_{i=1}^m (1 - y^{(i)}) \log P(x^{(i)} | y^{(i)} = 0)}{\partial \Sigma} \\
    &= \frac{\partial \sum_{i=1}^m \log \frac{1}{(2\pi)^{\frac{n}{2}} |\Sigma|^{\frac{1}{2}}} - \frac{1}{2} \sum_{i=1}^m (x^{(i)} - \mu_{y^{(i)}})^{\rm T} \Sigma^{-1}(x^{(i)} - \mu_{y^{(i)}})}{\partial \Sigma} \\
    &= \frac{\partial - \frac{m}{2} (n \log 2\pi + \log |\Sigma|) - \frac{1}{2} \sum_{i=1}^m (x^{(i)} - \mu_{y^{(i)}})^{\rm T} \Sigma^{-1}(x^{(i)} - \mu_{y^{(i)}})}{\partial \Sigma} \\
    &= - \frac{m}{2} \Sigma^{-1} - \frac{1}{2} \sum_{i=1}^m (x^{(i)} - \mu_{y^{(i)}})(x^{(i)} - \mu_{y^{(i)}})^{\rm T} (\Sigma^{-1})^2
    \end{aligned}
    $$

    令等式为零并右乘 $\Sigma^2$ 解得：

    $$
    \Sigma = \frac{1}{m} \sum_{i=1}^m (x^{(i)} - \mu_{y^{(i)}})(x^{(i)} - \mu_{y^{(i)}})^{\rm T}
    $$

    其中 $\mu_{y^{(i)}}$ 表示 $x^{(i)}$ 所属类别的均值（即 $\mu_0$ 或 $\mu_1$ ）。
    
    这个结果正是 **基于类别均值的总体协方差矩阵的无偏估计** 。

由此我们就得到了所有参数的似然估计结果。

## 2. 模型参数求解

下面我们就来证明一下为什么 GDA 是 **线性** 判别模型，以及具体的模型参数该如何求解。

```py showLineNumbers
def predict_proba(self, X):
    inv_sigma = np.linalg.inv(self.sigma)
    
    # 线性判别函数参数
    w = inv_sigma @ (self.mu1 - self.mu0)

    b = (
            np.log(self.phi / (1 - self.phi))
        + 0.5 * self.mu0.T @ inv_sigma @ self.mu0
        - 0.5 * self.mu1.T @ inv_sigma @ self.mu1
    )
    
    return 1 / (1 + np.exp(-(X @ w + b)))
```

GDA 的核心是计算后验概率，它可以通过贝叶斯定理得到：

$$
P(y=1 | x) = \frac{P(x | y=1)P(y=1)}{P(x | y=0)P(y=0) + P(x | y=1)P(y=1)}
$$

为了方便分类，我们用对数几率作为判别函数来求解：

$$
\delta(x) = \log \frac{P(y = 1 | x)}{P(y = 0 | x)} = \log \frac{P(x | y = 1)P(y = 1)}{P(x | y = 0)P(y = 0)} = \log \frac{P(y=1)}{P(y=0)} + \log \frac{P(x | y=1)}{P(x | y=0)}
$$

### 线性模型推导

仔细观察[上面](#先验假设-prior-assumptions)的先验条件，我们假设了正例跟负例的协方差矩阵相同，因此条件概率密度公式可以写成：

$$
P(x | y = k) = \frac{1}{(2\pi)^{\frac{n}{2}}|\Sigma|^{\frac{1}{2}}} \exp\left(-\frac{1}{2}(x-\mu_k)^{\rm T}\Sigma^{-1}(x-\mu_k)\right)
$$

代入 $\delta(x)$ 的尾项后，展开平方化简可得：

$$
\log\frac{P(x | y=1)}{P(x | y=0)} = - \frac{1}{2}(x - \mu_1)^{\rm T}\Sigma^{-1}(x - \mu_1) + \frac{1}{2}(x - \mu_0)^{\rm T}\Sigma^{-1}(x - \mu_0)
$$

$$
\delta(x) = (\Sigma^{-1}(\mu_1 - \mu_0))^{\rm T}x + \left(\log \frac{\phi}{1 - \phi} - \frac{1}{2}(\mu_1^{\rm T}\Sigma^{-1}\mu_1 - \mu_0^{\rm T}\Sigma^{-1}\mu_0)\right)
$$

对比线性判别函数的形式自然可以得到：

$$
w = \Sigma^{-1}(\mu_1 - \mu_0)
$$

$$
b = \log \frac{\phi}{1 - \phi} - \frac{1}{2}(\mu_1^{\rm T}\Sigma^{-1}\mu_1 - \mu_0^{\rm T}\Sigma^{-1}\mu_0)
$$

根据这两个公式我们可以轻松求解高斯判别模型参数。

---

# 深层问题探究

1. 高斯判别分析要求正例和负例满足一定的条件，其中一个便是协方差要求相同，这是为什么？

    标准的 GDA（也是最常见的一种形式）假设：

    $$
    \Sigma_0 = \Sigma_1 = \Sigma
    $$

    这意味着：
    > 不同类别的样本具有 **相同** 的协方差矩阵，只是均值不同。

    这个假设非常重要，因为它会带来下面的结果：

    *   **线性判别分析（Linear Discriminant Analysis，简称 LDA）**：当我们假设 $\Sigma_0 = \Sigma_1 = \Sigma$ 时，对数几率 $\delta(x)$ 中的二次项（如 $x^{\rm T} \Sigma^{-1} x$ ）会被抵消，判别边界 $w^{\rm T} x + b = 0$ 是一条直线（或超平面）。此时 GDA 的决策边界与逻辑回归（Logistic Regression）类似，因此在决策边界层面 GDA 与 LDA 高度相关。

    *   **二次判别分析（Quadratic Discriminant Analysis，简称 QDA）**：如果我们 **不强制** 协方差相等，即假设 $\Sigma_0 \ne \Sigma_1$ ，那么对数几率 $\delta(x)$ 中涉及 $x$ 的二次项将 **不会被抵消** 。此时 $\delta(x)$ 会出现 $x^{\rm T} A x$ 形式的二次项，导致决策边界是一条 **二次曲线/曲面** 。这种模型被称为二次判别分析。

2. 高斯判别分析与逻辑回归的区别是什么？

    由上面证明 “为什么 GDA 是线性判别模型” 的结果我们可以知道，高斯判别模型的对数几率函数只不过是一个复杂的线性函数罢了，因此高斯判别模型本质上就是逻辑回归。**无需迭代但需要一定的先验** 便是高斯判别模型跟逻辑回归的区别，局限（需要先验）但高效（无需迭代）。

---

# 参考文献列表

1. [高斯判别分析GDA推导与代码实现](https://www.cnblogs.com/LuckyGlass-blog/p/17159433.html)

2. [[ML] GDA 高斯判别分析](https://cometeme.github.io/ml/2019/09/ML-GDA高斯判别分析.html)