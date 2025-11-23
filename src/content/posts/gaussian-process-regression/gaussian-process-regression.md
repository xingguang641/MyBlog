---
title: 【机器学习基本模型】第十节：高斯过程回归
published: 2025-11-10
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 高斯过程回归基本原理

在传统的机器学习中， **线性回归** 是最基础的监督学习模型之一。它通过一条直线（或超平面）去拟合数据的整体趋势，从而建立输入与输出之间的关系。然而在很多复杂任务中，现实世界的数据往往呈现出 **非线性、不确定性强** 的特征，此时单纯的线性假设已无法很好地刻画真实关系。

为了解决这个问题，人们引入了 **概率建模** 的思想 ———— 我们不仅希望得到一个预测值，还希望能够衡量模型预测的不确定性，即给出预测结果的 **置信度** 。在这一思路下， **高斯过程回归** （Gaussian Process Regression，简称 GPR） 便应运而生。它是一种以概率论为基础的非参数方法，能够在建模复杂函数的同时，对预测结果的不确定性进行定量刻画。

然而我们要真正理解高斯过程回归的思想，首先需要从它的简化形式出发，也就是 **贝叶斯线性回归** （Bayesian Linear Regression）。高斯过程回归正是基于贝叶斯回归思想的一种推广与扩展。

![高斯过程回归图像](src\content\posts\gaussian-process-regression\高斯过程回归1.jpg)

## 贝叶斯线性回归

在线性回归中，我们假设输入特征 $x$ 与输出 $y$ 之间满足线性关系：

$$
y = w^{\rm T} x + \epsilon
$$

其中 $\epsilon \sim \mathcal{N}(0, \beta^{-1})$ 表示高斯噪声。

传统的最小二乘回归（OLS）会通过最小化均方误差（MSE）来估计参数：

$$
\hat{w} = \arg \min_w \sum_i (y_i - w^{\rm T} x_i)^2
$$

这种方法得到的是参数 $w$ 的 **点估计** （point estimate），这是一个确定的结果。然而在现实中，训练数据往往 **有限、带噪声甚至存在异常点** ，因此我们在对参数估计时应该要参杂一点 “不确定性” 。

> 下面的教程舍去了不必要的证明过程，如果感兴趣的读者可以观看这篇博客

[浅述贝叶斯线性回归](https://zhuanlan.zhihu.com/p/305042203)

### 贝叶斯思想

在贝叶斯线性回归中，我们引入一个重要的思想：

> 我们不把参数 $w$ 看作确定值，而是把它当作一个 **随机变量** ，用概率分布来描述我们对它的信念。

也就是说，我们要建模的是 $P(w|\mathcal{D})$ ：即给定数据集 $\mathcal{D} = \{ (x_i, y_i) \}_{i=1}^N$ 的条件下，参数 $w$ 的 **后验分布** 。这个分布告诉我们：在观察到数据之后，哪些 $w$ 是更可能的，哪些是不太可能的。这样我们不仅能够得到预测结果，还能量化预测的 “置信度” 。

为了得到这个后验分布，我们需要先引入两个概念：

- **先验分布（Prior）**

    在未观察到任何数据之前，我们对参数 $w$ 的可能取值有一个先验假设。最常见的假设是各维度相互独立、均值为 0 的高斯分布：

    $$
    P(w) = \mathcal{N}(w | 0, \alpha^{-1} \mathbf{I})
    $$

    其中 $\alpha$ 表示先验分布的精度。

- **似然函数（Likelihood）**

    假设观测数据由参数 $w$ 生成，并受到高斯噪声的影响：

    $$
    P(y | x, w) = \mathcal{N}(y | w^{\rm T} x, \beta^{-1})
    $$

    对于整个数据集 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ ，若假设样本独立同分布，则整体似然为：

    $$
    P(y | X, w) = \prod_{i=1}^{N} \mathcal{N}(y_i | w^{\rm T} \mathbf{x}_i, \beta^{-1})
    $$

    其中 $X$ 是特征矩阵， $y$ 是观测输出， $\beta$ 表示观测噪声的精度。

### 学习过程

正如上面所说：在贝叶斯线性回归中，我们的目标不再是寻找一个最优参数 $\hat{w}$ ，而是希望通过数据推断出参数的后验分布：

$$
P(w | X, y) = \frac{P(y | X, w) P(w)}{P(y | X)}
$$

由于我们假设先验与似然均为高斯分布，它们的乘积仍为高斯分布，因此后验分布 $P(w | X, y)$ 也服从高斯形式：

$$
P(w | X, y) = \mathcal{N}(w | \mathbf{m}_N, \mathbf{S}_N)
$$

将先验分布和似然函数带入贝叶斯公式后，可以得到后验分布的参数解析式：

$$
\mathbf{m}_N = \beta \mathbf{S}_N X^{\rm T} y \quad \mathbf{S}_N = (\alpha \mathbf{I} + \beta X^{\rm T} X)^{-1}
$$

### 预测过程

在获得参数的后验分布 $P(w | X, y)$ 后，我们就可以对新样本 $x_*$ 进行预测。与传统线性回归直接使用单一参数 $\hat{w}$ 不同，贝叶斯线性回归会综合考虑所有可能的参数值，并按照其后验概率加权平均：

$$
P(y_* | x_*, X, y) = \int P(y_* | x_*, w) \, P(w | X, y) \, dw
$$

这一积分表达了核心的贝叶斯思想：

> 预测不仅依赖模型的结构，还依赖我们对参数不确定性的认知。

由于被积函数的两项（条件分布和后验分布）均为高斯形式，积分结果仍为高斯分布：

$$
P(y_* | x_*, X, y) = \mathcal{N}(y_* | \mu_*, \sigma_*^2)
$$

将后验分布（我们学习得到的模型）和似然函数带入积分后，可以得到预测分布的参数解析式：

$$
\mu_* = \mathbf{m}_N^{\rm T} x_* \quad \sigma_*^2 = \frac{1}{\beta} + x_*^{\rm T} \mathbf{S}_N x_*
$$

## 高斯过程

通过贝叶斯线性回归，我们学会了如何在参数层面引入不确定性：我们不再寻找单一的参数向量 $w$ ，而是对其建立一个概率分布 $P(w|X, y)$ 。这使得模型能够在预测时量化不确定性，从而变得更稳健、更可信。然而线性模型本身仍然受到 **特征空间的限制** 。

在贝叶斯线性回归中，即使我们对参数 $w$ 进行了概率建模，模型仍然只能表达输入 $x$ 的线性组合形式。

为了表达非线性关系，我们可以通过引入 **特征映射函数** $\phi(x)$ ，将输入投影到更高维的空间：

$$
f(x) = w^{\rm T} \phi(x)
$$

但这样一来，模型的复杂度和参数数量会急剧增加，计算和存储都变得困难。

于是我们换一种视角：

> 与其对参数 $w$ 进行建模，不如直接对函数 $f(x)$ 本身建模。

也就是说，我们不再假设存在某个确定的 $w$ ，而是假设所有可能的函数 $f(x)$ 构成了一个分布。而 **高斯过程** （Gaussian Process，简称 GP）就是这样一种 “对函数分布建模” 的方法。

形式化地，我们假设：

$$
f(x) \sim \mathcal{GP}(m(x), k(x, x'))
$$

- $\displaystyle m(x) = \mathbb{E}\Big[f(x)\Big]$ 为 **均值函数** ，描述函数在输入空间的平均趋势
- $\displaystyle k(x, x') = \mathbb{E}\Big[\big(f(x) - m(x)\big)\big(f(x') - m(x')\big)\Big]$ 为 **核函数** ，刻画任意两个输入点之间的相关性

为了理解高斯过程的由来，我们可以从贝叶斯线性回归出发。回忆贝叶斯线性回归中的预测函数：

$$
f(x) = w^{\rm T} \phi(x)
$$

假设参数具有高斯先验 $P(w) = \mathcal{N}(0, \alpha^{-1} \mathbf{I})$ 那么我们可以计算出函数值的期望与协方差：

$$
\mathbb{E}\Big[f(x)\Big] = 0 \quad \text{Cov}\Big(f(x), f(x')\Big) = \alpha^{-1} \phi(x)^{\rm T} \phi(x')
$$

说明在这种假设下 $f(x)$ 本身服从一个高斯过程，其协方差函数为：

$$
k(x, x') = \alpha^{-1} \phi(x)^{\rm T} \phi(x')
$$

也就是说，贝叶斯线性回归天然地隐含了一个高斯过程假设。如果我们令特征映射 $\phi(x)$ 的维度趋于无穷，并用核函数直接定义 $k(x, x')$ ，就得到了 **高斯过程回归** ———— 贝叶斯线性回归的无限维形式。

---

# 代码实现

在前面的讨论中我们已经知道：高斯过程是一种直接对函数建立分布的建模方式。它不再依赖具体的参数向量 $w$ ，而是通过核函数 $k(x, x')$ 来刻画不同输入点之间的相关性。基于这种思想，我们现在来正式推导高斯过程回归的完整过程。

为了便于理解，我们将对照代码进行讲解。

```py frame="code" title="main.py"
import numpy as np
from scipy.optimize import minimize
np.random.seed(42)
X_train = np.linspace(-5, 5, 12).reshape(-1, 1)
y_train = np.sin(X_train) + 0.3 * np.random.randn(*X_train.shape)


# 定义 RBF 核函数
def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1); X2 = np.atleast_2d(X2)
    sqdist = np.sum(X1**2, 1).reshape(-1, 1) + np.sum(X2**2, 1) - 2 * X1 @ X2.T
    return variance * np.exp(-0.5 / (length_scale**2) * sqdist)

class GaussianProcessRegressor:
    def __init__(self, kernel, noise=1e-6):
        self.kernel = kernel
        self.noise = noise
        self.is_fit = False

    def fit(self, X_train, y_train):
        self.X_train = np.atleast_2d(X_train)
        self.y_train = np.atleast_2d(y_train).reshape(-1, 1)
        K = self.kernel(self.X_train, self.X_train)
        K_y = K + self.noise * np.eye(len(self.X_train))
        self.L = np.linalg.cholesky(K_y)
        self.alpha = np.linalg.solve(self.L.T, np.linalg.solve(self.L, self.y_train))
        self.is_fit = True

    def predict(self, X_test, return_cov=False):
        if not self.is_fit:
            raise RuntimeError("模型尚未训练，请先调用 fit()。")
        X_test = np.atleast_2d(X_test)
        K_s = self.kernel(self.X_train, X_test)
        K_ss = self.kernel(X_test, X_test)
        mu = K_s.T @ self.alpha
        v = np.linalg.solve(self.L, K_s)
        cov = K_ss - v.T @ v
        if return_cov:
            return mu.ravel(), cov
        else:
            return mu.ravel()

    def log_marginal_likelihood(self):
        y = self.y_train
        L = self.L
        n = len(y)
        term1 = -0.5 * y.T @ self.alpha
        term2 = -np.sum(np.log(np.diag(L)))
        term3 = -0.5 * n * np.log(2 * np.pi)
        return (term1 + term2 + term3).ravel()[0]

# 超参数优化函数
def optimize_rbf_hyperparameters(X_train, y_train, noise=0.1**2):
    def objective(params):
        # 对数变换保证参数 >0
        length_scale = np.exp(params[0])
        variance = np.exp(params[1])
        kernel = lambda X1, X2: rbf_kernel(X1, X2, length_scale=length_scale, variance=variance)
        gp = GaussianProcessRegressor(kernel=kernel, noise=noise)
        gp.fit(X_train, y_train)
        return -gp.log_marginal_likelihood()

    res = minimize(objective, x0=np.log([1.0, 1.0]), bounds=[(-5, 5), (-5, 5)])
    best_length_scale, best_variance = np.exp(res.x)
    return best_length_scale, best_variance

# 执行代码
noise = 0.1**2
if __name__ == "__main__":
    # 优化所有核参数
    best_l, best_v = optimize_rbf_hyperparameters(X_train, y_train, noise=noise)
    print(f"优化得到的 length_scale: {best_l:.4f}, variance: {best_v:.4f}")
    # 使用优化后的核参数重新训练模型
    gp = GaussianProcessRegressor(
        kernel=lambda x, y: rbf_kernel(x, y, length_scale=best_l, variance=best_v),
        noise=noise
    )
    gp.fit(X_train, y_train)

    # 预测过程
    X_test = np.linspace(-6, 6, 200).reshape(-1, 1)
    mean, cov = gp.predict(X_test, return_cov=True)
    std = np.sqrt(np.diag(cov))
    print("Posterior mean (前5个):", mean[:5])
    print("Posterior std  (前5个):", std[:5])
    print("Log Marginal Likelihood:", gp.log_marginal_likelihood())
```

## 准备过程

高斯过程回归依赖 **核函数** 来刻画输入点之间的相关性。核函数的参数通常可以由人工设定，但也可以通过 **最大化边际似然** （Max Marginal Likelihood） 自动学习得到。

假设我们有一组训练数据 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ ，其中观测值 $y_i$ 由真实函数 $f(x_i)$ 加上噪声生成：

$$
y_i = f(x_i) + \epsilon_i \quad \epsilon_i \sim \mathcal{N}(0, \sigma_n^2)
$$

我们进一步假设函数 $f(x)$ 服从一个高斯过程（为简化推导，通常假设均值函数为零）：

$$
f(x) \sim \mathcal{GP}(0, k(x, x'))
$$

于是对任意有限个输入点 ${x_1, x_2, \dots, x_N}$ ，其函数值向量服从多元高斯分布（在高斯过程中我们一般用多维随机向量来表示函数）：

$$
\mathbf{f} = [f(x_1), f(x_2), \ldots, f(x_N)]^{\rm T} \sim \mathcal{N}(0, K)
$$

其中协方差矩阵 $K$ 的元素由核函数 $K_{ij} = k(x_i, x_j)$ 给出。

由于观测值 $y$ 受到噪声影响，其分布为：

$$
y \sim \mathcal{N}(0, K + \sigma_n^2 \mathbf{I})
$$

我们就可以直接写出边际似然 $P(y|X, \theta)$ （关于这个分布为什么叫边际似然可以看下面的[深层问题思考](#深层问题思考)）：

$$
P(y|X, \theta) = \mathcal{N}(0, K + \sigma_n^2 \mathbf{I})
$$

其对数形式为：

$$
\log P(y | X, \theta) = -\frac{1}{2} y^{\rm T} (K + \sigma_n^2 \mathbf{I})^{-1} y - \frac{1}{2} \log |K + \sigma_n^2 \mathbf{I}| - \frac{N}{2} \log 2\pi
$$

通过最大化这个对数边际似然，我们可以找到最优的核函数超参数 $\theta$ 。在实际计算中，常用的方法包括梯度下降或 L-BFGS 等数值优化算法。

```py showLineNumbers
# 定义 RBF 核函数
def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1); X2 = np.atleast_2d(X2)
    sqdist = np.sum(X1**2, 1).reshape(-1, 1) + np.sum(X2**2, 1) - 2 * X1 @ X2.T
    return variance * np.exp(-0.5 / (length_scale**2) * sqdist)

# 对数边际似然函数
def log_marginal_likelihood(self):
    y = self.y_train
    L = self.L
    n = len(y)
    term1 = -0.5 * y.T @ self.alpha
    term2 = -np.sum(np.log(np.diag(L)))
    term3 = -0.5 * n * np.log(2 * np.pi)
    return (term1 + term2 + term3).ravel()[0]

# 超参数优化函数
def optimize_rbf_hyperparameters(X_train, y_train, noise=0.1**2):
    def objective(params):
        # 对数变换保证参数 >0
        length_scale = np.exp(params[0])
        variance = np.exp(params[1])
        kernel = lambda X1, X2: rbf_kernel(X1, X2, length_scale=length_scale, variance=variance)
        gp = GaussianProcessRegressor(kernel=kernel, noise=noise)
        gp.fit(X_train, y_train)
        return -gp.log_marginal_likelihood()

    res = minimize(objective, x0=np.log([1.0, 1.0]), bounds=[(-5, 5), (-5, 5)])
    best_length_scale, best_variance = np.exp(res.x)
    return best_length_scale, best_variance
```

## 学习过程

在准备阶段中我们已经推导出观测向量满足：

$$
y \sim \mathcal{N}(0, K + \sigma_n^2 \mathbf{I})
$$

但在实际的代码实现中，我们并不直接显式使用该分布的均值和协方差，而是希望得到预测时需要用到的关键参数：

$$
\alpha = (K + \sigma_n^2 \mathbf{I})^{-1} y
$$

这样在预测新输入时，均值可以简化为（这样可以避免反复求逆带来的开销）：

$$
\mathbb{E}\Big[f_*\Big] = K(X_*, X_{\text{train}}) (K + \sigma_n^2 \mathbf{I})^{-1} y = K(X_*, X_{\text{train}}) \alpha
$$

由于对矩阵直接求逆不仅计算代价高、数值稳定性较差，因此通常采用 Cholesky 分解：

$$
K + \sigma_n^2 \mathbf{I} = LL^{\rm T}
$$

其中 $L$ 为下三角矩阵，可以通过两次三角求解得到 $\alpha$ ：

$$
Lz = y  \quad \Rightarrow \quad L^{\rm T} \alpha = z
$$

需要注意的是，这些用于预测的关键参数（包括 $\alpha$ 和 $L$ ）都依赖于核矩阵：

$$
K_\theta = K(X_{\text{train}}, X_{\text{train}}; \theta)
$$

该矩阵已在上述的准备过程中学习得到。

```py showLineNumbers
def fit(self, X_train, y_train):
    self.X_train = np.atleast_2d(X_train)
    self.y_train = np.atleast_2d(y_train).reshape(-1, 1)
    K = self.kernel(self.X_train, self.X_train)
    K_y = K + self.noise * np.eye(len(self.X_train))
    # Cholesky 分解提高数值稳定性
    self.L = np.linalg.cholesky(K_y)
    self.alpha = np.linalg.solve(self.L.T, np.linalg.solve(self.L, self.y_train))
    self.is_fit = True
```

## 预测过程

当模型完成训练后，我们希望对新的输入点 $X_*$ 给出预测。

在高斯过程回归中，预测结果本质上来自 **多元高斯分布的条件分布公式** ，因此具有严格的解析解：

$$
f_* | X_*, X_{\text{train}}, y \sim \mathcal{N}(\mu_*, \Sigma_*)
$$

其中的均值与协方差的解析式为（直接套用高维高斯分布的参数公式）：

$$
\mu_* = K(X_*, X_{\text{train}}) (K + \sigma_n^2 \mathbf{I})^{-1} y
$$

$$
\Sigma_* = K(X_*, X_*) - K(X_{\text{train}}, X_*)^{\rm T} (K + \sigma_n^2 I)^{-1} K(X_{\text{train}}, X_*)
$$

将预测参数 $\alpha = (K + \sigma_n^2 \mathbf{I})^{-1} y$ 代入公式可将均值化简为：

$$
\mu_* = K(X_*, X_{\text{train}}) \alpha
$$

将辅助矩阵 $v = L^{-1} K(X_{\text{train}}, X_*)$ 代入公式可将协方差化简为：

$$
\Sigma_* = K(X_*, X_*) - v^{\rm T} v
$$

```py showLineNumbers
def predict(self, X_test, return_cov=False):
    if not self.is_fit:
        raise RuntimeError("模型尚未训练，请先调用 fit()。")
    X_test = np.atleast_2d(X_test)
    K_s = self.kernel(self.X_train, X_test)
    K_ss = self.kernel(X_test, X_test)
    mu = K_s.T @ self.alpha
    v = np.linalg.solve(self.L, K_s)
    cov = K_ss - v.T @ v
    if return_cov:
        return mu.ravel(), cov
    else:
        return mu.ravel()
```

---

# 深层问题思考

1. 贝叶斯思想中的先验分布和似然函数为什么是那样子的？（为什么贝叶斯线性回归优于普通线性回归？）

    我们先来讲解一下为什么似然函数要设成：

    $$
    P(y | x, w) = \mathcal{N}(y | w^{\rm T} x, \beta^{-1})
    $$

    似然函数反映的是：

    > 在参数 $w$ 已知的情况下，观测到数据 $y$ 的 “可能性” 有多大。

    换句话说，它描述了数据的生成机制：

    $$
    y = w^{\rm T} x + \epsilon
    $$

    其中 $\epsilon$ 是噪声项，用来表示真实观测和理想模型之间的偏差。

    我们假设 $\epsilon \sim \mathcal{N}(0, \beta^{-1})$ ，于是可以得到：

    $$
    y | x, w \sim \mathcal{N}(w^{\rm T} x, \beta^{-1})
    $$

    那为什么先验分布要设成：

    $$
    P(w) = \mathcal{N}(w | 0, \alpha^{-1} \mathbf{I})
    $$

    这里有 **数学便利性** 和 **建模含义** 两个方面的原因：

    - 数学便利性

        在贝叶斯推断中，我们要计算后验分布：

        $$
        P(w | X, y) \propto P(y | X, w) P(w)
        $$

        我们已经通过分析得到似然函数 $P(y | X, w)$ 服从高斯分布，如果我们将先验分布 $P(w)$ 也选择为高斯分布，那么先验函数和似然函数就满足 **高斯共轭性** （Gaussian Conjugacy），使得后验分布也会是高斯分布。

        这不仅简化了推导过程，还能得到后验的闭式解，避免数值近似或采样操作。

    - 建模含义

        在没有观测数据之前，我们对参数 $w$ 的了解是模糊的。于是我们假设每个参数 $w_j$ 相互独立、均值为 0、方差有限：

        $$
        w_j \sim \mathcal{N}(0, \alpha^{-1})
        $$

        这表示我们对参数的 **先验信念** ：模型应尽可能简单，除非数据强烈表明某个特征确实重要。

        在最大后验估计（MAP）框架下：

        $$
        \arg\max_w P(w | X, y) = \arg\max_w P(y | X, w) P(w)
        $$

        取对数后可以得到：

        $$
        \arg\max_w \log P(y|X, w) - \frac{\alpha}{2} \|w\|^2
        $$

        > 这其实就对应了 **L2 正则化** 的思想

        因此从优化角度看，给参数 $w$ 加上高斯先验等价于在目标函数中加入 L2 正则化项。这意味着贝叶斯线性回归在建模阶段就自然地抑制了过大的参数，从而减少过拟合、提升泛化能力。

2. 为什么优化核函数超参数的时候用的是边际似然而不是普通的似然函数？（什么是边际似然函数？）

    在高斯过程回归（GPR）中，我们希望根据观测数据学习核函数的超参数 $\theta$。直觉上，我们似乎可以最大化观测数据的似然。如果函数 $f$ 已知，则观测数据的似然为：

    $$
    P(y|f) = \mathcal{N}(y|f, \beta^{-1}\mathbf{I})
    $$

    然而问题在于：

    > 我们并不知道真实的 $f$ ，它本身是一个随机变量（随机过程）。

    因此直接最大化这个 “条件似然” 是没意义的，因为 $f$ 是不确定的，我们根本没有一个确定的 $f$ 可以优化（极大似然估计假定背后的隐藏参数是固定的，这是 **频率派的思想** ，而高斯过程假定隐藏函数是一个分布，这是 **贝叶斯派思想** ）。

    既然我们无法确定出一个确定的 $f$ ，就要利用积分来将其边缘化：

    $$
    P(y|X, \theta) = \int P(y|f) P(f|X, \theta) \, df
    $$

    这个积分结果被称为 **边际似然** （Marginal Likelihood），也常称为 **模型证据** （Model Evidence）。它衡量了在给定核函数超参数 $\theta$ 的情况下，模型整体上对观测数据 $y$ 的解释能力。

    通过最大化边际似然，我们能够自动选择那些既能很好拟合数据、又不会过度复杂化模型的核参数，从而实现一种 **贝叶斯式的自动正则化** 。

---

# 参考文献

## 贝叶斯线性回归

1. [贝叶斯线性回归（Bayesian Linear Regression）](https://blog.csdn.net/daunxx/article/details/51725086)

2. [如何通俗地解释贝叶斯线性回归的基本原理？](https://www.zhihu.com/question/22007264/answers/updated)

3. [多元线性回归贝叶斯模型](https://andrewwang.rbind.io/courses/bayesian_statistics/notes/Ch7_h.pdf)

4. [贝叶斯数据分析(七)——贝叶斯线性回归](https://blog.vicayang.cc/Note-Bayesian-Linear-Regression/)

5. [贝叶斯线性回归与贝叶斯逻辑回归](https://weirping.github.io/blog/Bayesian-Probabilities-in-ML.html)

## 高斯过程

1. [高斯过程 Gaussian Processes 原理、可视化及代码实现](https://borgwang.github.io/ml/2019/07/28/gaussian-processes.html)

2. [高斯过程 Gaussian Process](https://www.superui.cc/machine-learning/gaussian-process/)

3. [24秋机器学习笔记-07-高斯过程](https://blog.imyangty.com/note-ml2024fall/gaussian-process/)

4. [【ScikitLearn】高斯过程用于机器学习](https://scikit-learn.cn/stable/auto_examples/gaussian_process/index.html)

## 高斯过程回归

1. [高斯过程回归(Gaussian Processes Regression, GPR)简介](https://blog.csdn.net/HelloWorldTM/article/details/126980872)

2. [【ScikitLearn】高斯过程回归与高斯过程分类](https://scikit-learn.cn/stable/modules/gaussian_process.html)

3. [高斯过程回归【详细数学推导】](https://blog.csdn.net/v20000727/article/details/138086802)

4. [贝叶斯建模-高斯过程回归](https://bookdown.org/xiangyun/masr/gaussian-processes-regression.html)

5. [高斯过程回归（GPR）原理与实现](https://zhuanlan.zhihu.com/p/697071644)

6. [深度学习基础（高斯过程）](https://sirlis.cn/posts/deep-learning-gaussian-process/)