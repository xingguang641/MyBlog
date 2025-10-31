---
title: 【机器学习基本模型】第三节：高斯判别分析
published: 2025-10-24
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 高斯判别分析基本原理

虽然逻辑回归在机器学习任务中的效果非常好，但在样本呈现特殊分布的情况下，我们可以使用其他更好的算法。 **高斯判别分析** (Gaussian Discriminant Analysis) 就是其中的一个。这篇博客的主要内容，就是介绍高斯判别分析算法的主要原理以及公式的推导。

![高斯判别分析图像](src\content\posts\gaussian-discriminant-analysis\高斯判别模型1.jpg)

## 先验假设

与逻辑回归不同，高斯判别分析需要两个先验假设，分别为：

- 样本的分类 $y$ 服从伯努利分布：

$$
P(y) =
\begin{cases}
\phi^{y}(1 - \phi)^{1 - y} & y = 0, 1 \\\\
0 & y \ne 0, 1
\end{cases}
$$

- 正负样本均符合正态分布：

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

正因为在模型中，我们需要预先假设样本服从正态分布，所以这也是 “高斯判别分析” 名字的由来。

有了以上的假设之后，我们就能进行下一步的推导。

## 似然函数

在前面的先验假设中，我们需要用到 $\phi$ 、 $\Sigma$ 、 $\mu_0$ 和 $\mu_1$ 等参数，所以我们先要对这些参数给出参数估计。

首先我们要求出对数似然函数，对于整个数据集，似然函数是：

$$
\prod_{i=1}^m P(x^{(i)}, y^{(i)} \mid \phi, \Sigma, \mu_0, \mu_1) = \prod_{i=1}^m P(x^{(i)} \mid y^{(i)}) P(y^{(i)})
$$

取对数后，得到的对数似然函数为：

$$
L(\phi, \Sigma, \mu_0, \mu_1) = \sum_{i=1}^m \left[ \log P(x^{(i)} \mid y^{(i)}) + \log P(y^{(i)}) \right]
$$

为了便于处理不同类别的数据，我们将条件概率项 $\log P(x^{(i)} \mid y^{(i)})$ 根据 $y^{(i)}$ 的值进行分解。由于 $y^{(i)}$ 是二值的（0或1），我们可以使用 $y^{(i)}$ 作为指示函数：

- 当 $y^{(i)} = 1$ 时， $\log P(x^{(i)} \mid y^{(i)}) = \log P(x^{(i)} \mid y^{(i)} = 1)$
- 当 $y^{(i)} = 0$ 时， $\log P(x^{(i)} \mid y^{(i)}) = \log P(x^{(i)} \mid y^{(i)} = 0)$

因此，求和项可以重写为：

$$
\sum_{i=1}^m \log P(x^{(i)} \mid y^{(i)}) = \sum_{i=1}^m \left[ y^{(i)} \log P(x^{(i)} \mid y=1) + (1-y^{(i)}) \log P(x^{(i)} \mid y=0) \right]
$$

带入对数似然函数可得：

$$
L(\phi, \Sigma, \mu_0, \mu_1) = \sum_{i=1}^m \left[ y^{(i)} \log P(x^{(i)} \mid y=1) + (1-y^{(i)}) \log P(x^{(i)} \mid y=0) \right] + \sum_{i=1}^m \log P(y^{(i)})
$$

# 代码讲解

不同于前面两个模型，高斯判别模型是 **闭式解** 的分类器，无需梯度下降之类的梯度迭代。

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

## 先验参数求解

接[上面](#似然函数)所说，我们要想满足先验，首先就要求解出四个参数。根据极大似然估计的原理，我们要想模型最好，我们只需要让似然函数取到最大值即可，也就等价于对数似然函数取到最大值。因此我们可以对四个关键参数求偏导来得到对数似然估计取得最大值时四个参数的具体值。

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

首先对 $\phi$ 求偏导，其中前两项和对 $\phi$ 的偏导均为 0 ，所以只需计算第三项的结果：

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

求解 $\Sigma$ 则更要复杂一些：

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

其中， $\Sigma$ 的表达式中会使用到 $\mu_0$ , $\mu_1$ 的值，所以接下来需要求 $\mu_1$ 的似然估计：

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

由此我们就得到了所有参数的似然估计结果。

## 模型参数求解

下面我们就来证明一下为什么 GDA 是 **线性** 判别模型，以及模型参数该如何求解。

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

GDA 的核心是计算后验概率：

$$
P(y=1 \mid x) = \frac{P(x \mid y=1)P(y=1)}{P(x \mid y=0)P(y=0) + P(x \mid y=1)P(y=1)}
$$

为了方便分类，我们用对数几率来求解：

$$
\delta(x) = \log \frac{P(y = 1 \mid x)}{P(y = 0 \mid x)} = \log \frac{P(x \mid y = 1)P(y = 1)}{P(x \mid y = 0)P(y = 0)} = \log \frac{P(y=1)}{P(y=0)} + \log \frac{P(x \mid y=1)}{P(x \mid y=0)}
$$

仔细观察上面的[先验条件](#先验假设)，其实我们假设了正例跟负例的协方差矩阵相同，因此条件概率密度公式可以写成：

$$
P(x \mid y = k) = \frac{1}{(2\pi)^{\frac{n}{2}}|\Sigma|^{\frac{1}{2}}} \exp\left(-\frac{1}{2}(x-\mu_k)^{\rm T}\Sigma^{-1}(x-\mu_k)\right)
$$

代入 $\delta(x)$ 的尾项可得：

$$
\log\frac{P(x \mid y=1)}{P(x \mid y=0)} = - \frac{1}{2}(x - \mu_1)^{\rm T}\Sigma^{-1}(x - \mu_1) + \frac{1}{2}(x - \mu_0)^{\rm T}\Sigma^{-1}(x - \mu_0)
$$

最后展开平方项并化简可得：

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

# 深层问题思考

1. 高斯判别分析要求正例和负例满足一定的条件，其中一个便是协方差要求相同，这是为什么？

标准的 GDA（也是最常见的一种形式）假设：

$$
\Sigma_0 = \Sigma_1 = \Sigma
$$

> 不同类别的样本具有 **相同** 的协方差矩阵，只是均值不同。

这个假设非常重要，因为它会带来下面的结果:

当 $ \Sigma_0 = \Sigma_1 = \Sigma $ 时，经过贝叶斯判别后得到的判别边界是：$w^{\rm T} x + b = 0$ ，也就是说，GDA 的决策边界是线性的（此时 `GDA ≈ 逻辑回归`）。

如果不强制协方差相等， GDA 的 **对数几率** 会出现二次项 $x^{\rm T} A x$ ，此时的模型叫做 **二次判别分析** （Quadratic Discriminant Analysis，简称 QDA）。它的决策边界是二次曲线/曲面，而不是直线了。

2. 高斯判别分析与逻辑回归的区别是什么？（生成模型与判别模型的区别是什么？）

由上面证明 “为什么 GDA 是线性判别模型” 的结果我们可以知道，高斯判别模型的对数几率函数只不过是一个复杂的线性函数罢了，因此高斯判别模型本质上就是逻辑回归。 **无需迭代但需要一定的先验** 便是高斯判别模型跟逻辑回归的区别，局限（需要先验）但高效（无需迭代）。

生成式模型跟判别式模型的区别可以看下面这个 Blog ，并且这篇博客还罗列了常见的一些模型，后续我们都会讲到，敬请期待。

[生成式模型和判别式模型](https://blog.csdn.net/qq_43703185/article/details/107852027)

# 参考文献

1. [高斯判别分析GDA推导与代码实现](https://www.cnblogs.com/LuckyGlass-blog/p/17159433.html)

2. [[ML] GDA 高斯判别分析](https://cometeme.github.io/ml/2019/09/ML-GDA高斯判别分析.html)