---
title: 【机器学习基本模型】第十一节：高斯过程分类
published: 2025-11-12
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 高斯分类基本原理

在传统的机器学习中， **逻辑回归** 是最基础、最常用的分类模型之一。它利用线性决策边界，并结合 sigmoid 函数，将输入映射为类别概率，从而解决二分类任务。然而在许多真实场景中，数据往往呈现出 **高度非线性、噪声强、决策边界复杂多样** 的特征。简单的线性决策面显然难以刻画这种复杂结构，也无法准确反映模型对自身预测的信心。

正因如此，我们需要引入 **概率建模** 的思想：不仅要输出分类结果，还要评估预测背后的 **不确定性** 。在上一篇文章中，我们通过高斯过程回归（GPR）已经见识过这种 “既预测函数，又衡量不确定性” 的能力。而在分类任务中，我们同样希望拥有类似的建模方式。

在这样的需求驱动下， **高斯过程分类**（Gaussian Process Classification，简称 GPC）应运而生。它和 GPR 一样属于 **非参数贝叶斯方法** ，无需人为设定决策边界的具体形式，而是通过为一个 “潜在函数” 建立高斯过程先验，让模型自动学习灵活、非线性的分类规则。同时可以为每一次预测提供严谨的概率解释与不确定性度量。

不过要真正理解高斯过程分类背后的思想，我们需要从它的 “简化形式” 开始构建直觉 ———— 这便是 **贝叶斯逻辑回归（Bayesian Logistic Regression）**。可以将 GPC 看作是 “将贝叶斯逻辑回归扩展到无限维函数空间” 的自然结果：当我们把线性模型替换为高斯过程先验，逻辑回归便以一种更强大、更优雅的方式被泛化到非线性情形之中。

![高斯过程回归分类](src\content\posts\gaussian-process-classification\高斯过程分类1.jpg)

## 贝叶斯逻辑回归

传统逻辑回归通常采用最大似然（MLE）学习参数 $w$ ，但这种做法存在两显著个局限：

- **无法表达参数不确定性** ：模型给出的结果是单一的、确定的权重向量 $w$ ，无法告诉我们 “模型是否确定” 这一判断。
- **容易过拟合** ：在小数据集或高维场景下，MLE 容易产生极端权重，使得模型泛化能力变差。

为了解决这些问题，我们可以像贝叶斯线性回归中一样，引入贝叶斯思想：将权重 $w$ 视为随机变量，并通过概率分布来表达我们对其的不确定性。

### 学习过程

在贝叶斯逻辑回归中，我们不再寻找某个 “最佳” 参数 $w$ ，而是对 **所有可能的参数** 进行建模，并根据数据来更新对这些参数的 “信念” 。我们首先对参数设置一个高斯先验：

$$
P(w) = \mathcal{N}(w | 0, \Sigma_0)
$$

这相当于表达这样一种偏好：

> 权重应当较小，并且围绕 0 分布，即模型不应过度依赖任何单一特征。

这在概率论意义上等价于逻辑回归中的 L2 正则项（具体原因可以看上一篇的深层问题思考）。

对于每个训练样本 $(x_i, y_i)$ ，我们有伯努利似然：

$$
P(y_i | x_i, w) = \sigma(w^{\rm T} x_i)^{y_i} \left(1 - \sigma(w^{\rm T} x_i)\right)^{1 - y_i}
$$

假设数据独立，则整体似然为：

$$
P(y | X, w) = \prod_{i=1}^{N} P(y_i | x_i, w)
$$

这表达了：

> 在参数为 $w$ 的情况下，观测到所有训练数据 $(X, y)$ 的概率。

根据贝叶斯法则，参数的后验分布为：

$$
P(w | X, y) \propto P(w) \, P(y | X, w)
$$

这一步将 “先验信念” 与 “数据证据” 结合在一起，得到对参数 $w$ 更加合理的概率描述。

不过，与贝叶斯线性回归不同，由于 logistic 似然含有 sigmoid 函数，它并不是高斯形式，因此：

> 后验分布不再具有解析形式，无法写成一个显式的高斯分布。

这也是贝叶斯逻辑回归以及后续高斯过程分类中需要求解的核心难点，需要借助 **拉普拉斯近似（Laplace Approximation）** 或 **变分推断（VI）** 等近似推断方法来求解。

### 预测过程

虽然贝叶斯逻辑回归的后验分布无法像线性回归那样得到解析解，但这并不妨碍我们继续理解模型如何用于预测。在深入讨论各种近似推断方法之前，我们可以先从整体流程出发，看看贝叶斯逻辑回归在已经获得参数后验分布 $ P(w∣X,y)$ 的情况下，模型究竟是如何对一个新样本 $x_*$ 做出预测。

对于一个新样本 $x_*$ ，我们真正关心的是它属于正类的预测概率：

$$
P(y_* = 1 | x_*, X, y)
$$

根据贝叶斯思想，这个概率应该同时考虑所有可能的参数取值，并按它们的后验概率加权。也就是说，我们不能再像普通逻辑回归那样只代入某个单一的 $w$ ，而是需要对所有 $w$ 的可能性做积分：

$$
P(y_* = 1 | x_*, X, y) = \int \sigma(w^{\rm T} x_*) P(w | X, y) \, dw
$$

从形式上看，这就是对所有可能的决策边界的加权平均，因此贝叶斯逻辑回归的预测通常比传统逻辑回归更加 “保守” ，也能体现模型的不确定性。

然而这个积分同样无法解析求解，原因与后验无法解析相同：Sigmoid 函数破坏了高斯结构，使得整个积分既非线性也非高斯（哪怕后验分布已经用过高斯近似）。

## 拉普拉斯近似

如上所述，贝叶斯逻辑回归的核心难点在于：后验分布 $P(w | X, y)$ 和预测分布 $P(y_* = 1 | x_*, X, y)$ 均无法解析求解。对此我们必须对后验分布做出某种近似。

在众多近似推断方法中， **拉普拉斯近似** 无疑是最直观、也最容易入门的一类。它通过对后验分布在最大后验点附近进行二阶近似，从而将一个复杂的非高斯后验替换为 “看起来像高斯” 的简单分布，既贴近直觉，又便于计算。

因此在正式进入更加系统、更加通用的近似推断方法（例如后续章节中要讲到的 **变分推断 VI** ）之前，我们先从拉普拉斯近似开始，理解它的核心思想与推导方式。这不仅能帮助你看懂贝叶斯逻辑回归的数学结构，也为下面理解高斯过程分类（GPC）打下概念基础。

### 后验分布近似

拉普拉斯近似的核心思想非常简单：在后验分布的最高点（即 MAP 点）附近，绝大多数概率质量都集中在一个局部区域。因此我们可以在这个点附近 **用一个二阶泰勒展开来近似对数后验分布** ，使得后验近似成为一个高斯分布。

具体来说，拉普拉斯近似包含三个关键步骤：

- 找到后验的最大值（MAP 点）

    也就是求解下面这个式子：

    $$
    w_{\text{MAP}} = \arg\max_w \log P(w | X, y)
    $$

    由于后验与先验、似然成正比，这一步相当于求解一个带 L2 正则的逻辑回归优化问题。

- 在该点附近对 log 后验进行二阶泰勒展开

    对该点使用泰勒展开可得：

    $$
    \log P(w | X, y) \approx \log P(w_{\text{MAP}} | X, y) - \frac{1}{2} (w - w_{\text{MAP}})^{\rm T} H(w - w_{\text{MAP}})
    $$

    其中 H 是负对数后验的 Hessian 矩阵：

    $$
    H = -\nabla^2 \log P(w | X, y) \Big|_{w=w_{\text{MAP}}}
    $$

- 得到高斯形式的近似后验

    根据二阶展开，后验分布被近似为高斯：

    $$
    P(w | X, y) \approx \mathcal{N}(w | w_{\text{MAP}}, H^{-1})
    $$

至此我们就用一个明确的高斯分布替代了复杂的非高斯后验，使得之前难以求解的积分与预测也变得可操作。

### 预测分布近似

在得到了拉普拉斯近似后的高斯后验之后，我们就可以对新样本 $x_*$ 进行预测。用拉普拉斯近似后的高斯后验代替真实后验：

$$
P(y_* = 1 | x_*, X, y) \approx \int \sigma(w^{\rm T} x_*) \mathcal{N}(w | w_{\text{MAP}}, H^{-1}) \, dw
$$

令 $a = w^{\rm T} x_*$ ，则 $a$ 近似服从一维高斯分布 $a \sim \mathcal{N}(m_a, s_a^2)$ ，其参数解析式如下：

$$
m_a = w_{\text{MAP}}^{\rm T} x_* \quad s_a^2 = x_*^{\rm T} H^{-1} x_*
$$

由此后验也可以写成如下形式：

$$
P(y_* = 1 | x_*, X, y) \approx \int \sigma(a) \, \mathcal{N}(a | m_a, s_a^2) \, da
$$

这个一维积分往往没有解析解，因此我们可以通过数值方法计算，或者使用 **常用的解析近似**（MacKay 公式）求解：

$$
P(y_* = 1 | x_*, X, y) \approx \sigma\left(\frac{m_a}{\sqrt{1 + \pi s_a^2 / 8}}\right)
$$

> 这是一个经验公式，具体推导过程可以看下面这篇论文

[A practical Bayesian framework for backpropagation networks](https://authors.library.caltech.edu/records/8n76z-g9k64)

## 理论基础

在分类问题中，我们不直接观测到连续的 $f(x)$ 值，而是观测到二元输出 $y_i \in \{0, 1\}$ ，表示每个数据点的类别。与回归问题不同，分类问题的目标是对这些二元输出进行建模。

为了把高斯过程应用到分类问题，我们需要使用逻辑回归中的类似方式：通过某个函数（如 sigmoid 函数）将潜在函数 $f(x)$ 映射到概率空间，从而得到每个样本属于类别 1 的概率。

我们假设每个样本的标签 $y_i$ 是由对应的潜在函数 $f(x_i)$ 通过一个逻辑回归的机制生成的。具体来说，给定输入 $x_i$ ，我们用 sigmoid 函数（也称为逻辑函数）来连接潜在函数值 $f_i = f(x_i)$ 和输出 $y_i$ ：

$$
P(y_i = 1 | f_i) = \sigma(f_i) = \frac{1}{1 + e^{-f_i}}
$$

其中 $\sigma(z)$ 是 sigmoid 函数，它将任意实数映射到 $[0, 1]$ 的概率值。

因此给定潜在函数值 $f_i$ 的条件下， $y_i$ 的条件概率由以下伯努利分布描述：

$$
P(y_i | f_i) = \sigma(f_i)^{y_i} \left(1 - \sigma(f_i)\right)^{1 - y_i}
$$

$$
P(y | f) = \prod_{i=1}^{n} \sigma(f_i)^{y_i} \left(1 - \sigma(f_i)\right)^{1 - y_i}
$$

这就为我们提供了一个关于潜在函数 $f$ 和输出 $y$ 的模型。也就是说，每个 $f_i$ 通过 sigmoid 函数生成了 $y_i$ ，因此模型的输出是基于潜在函数 $f$ 的概率。

---

# 高斯分类代码实现

高斯过程分类的流程与高斯过程回归的流程大体相似，为了便于理解，我们将对照代码进行讲解。

```py frame="code" title="main.py"
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import cho_factor, cho_solve
np.random.seed(42)
X_train = np.linspace(-5, 5, 20).reshape(-1, 1)
y_train = (X_train[:, 0] > 0).astype(int)


# 定义 RBF 核函数
def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1)
    X2 = np.atleast_2d(X2)
    sqdist = (
        np.sum(X1**2, 1).reshape(-1, 1)
        + np.sum(X2**2, 1)
        - 2 * X1 @ X2.T
    )
    return variance * np.exp(-0.5 / length_scale**2 * sqdist)

class GaussianProcessClassifier:
    def __init__(self, kernel, max_iter=20, tol=1e-6):
        self.kernel = kernel
        self.max_iter = max_iter
        self.tol = tol
        self.is_fit = False

    @staticmethod
    def sigmoid(a):
        return 1.0 / (1.0 + np.exp(-a))

    def fit(self, X_train, y_train):
        self.X_train = np.atleast_2d(X_train)
        self.y_train = y_train.reshape(-1, 1)
        n = len(y_train)

        def K_solve(v):
            return cho_solve(K_chol, v)

        self.K = self.kernel(self.X_train, self.X_train)
        f = np.zeros((n, 1))
        K_chol = cho_factor(self.K + 1e-6 * np.eye(n))
        for _ in range(self.max_iter):
            pi = self.sigmoid(f)
            W = (pi * (1 - pi)).flatten()

            grad = self.y_train - pi - K_solve(f)
            H = np.diag(W) + cho_solve(K_chol, np.eye(n))

            try:
                H_chol = cho_factor(H)
                delta = cho_solve(H_chol, grad)
            except:
                delta = np.linalg.solve(H, grad)

            f_new = f + delta
            if np.max(np.abs(delta)) < self.tol:
                f = f_new
                break
            f = f_new

        self.f_map = f
        self.W = (pi * (1 - pi)).flatten()

        H = np.diag(self.W) + cho_solve(K_chol, np.eye(n))
        H_chol = cho_factor(H)
        self.Sigma = cho_solve(H_chol, np.eye(n))

        self.K_chol = K_chol
        self.is_fit = True

    def predict(self, X_test):
        if not self.is_fit:
            raise RuntimeError("请先调用 fit() 训练模型。")

        X_test = np.atleast_2d(X_test)
        K_s = self.kernel(self.X_train, X_test)
        m_star = K_s.T @ cho_solve(self.K_chol, self.f_map)

        # predictive variance approx
        W_inv = np.diag(1.0 / (self.W + 1e-12))
        A = self.K + W_inv
        A_chol = cho_factor(A)

        v = cho_solve(A_chol, K_s)
        k_ss = self.kernel(X_test, X_test).diagonal()
        s2 = k_ss - np.sum(K_s * v, axis=0)

        # logistic integral approximation
        denom = np.sqrt(1 + np.pi * s2 / 8)
        prob = self.sigmoid(m_star.flatten() / denom)
        return prob

    def log_marginal_likelihood(self):
        f = self.f_map
        y = self.y_train
        W = self.W
        pi = self.sigmoid(f)
        log_lik = np.sum(
            y * np.log(pi + 1e-12) + (1 - y) * np.log(1 - pi + 1e-12)
        )
        K_chol = self.K_chol
        Kinv_f = cho_solve(K_chol, f)
        log_prior = -0.5 * f.T @ Kinv_f
        H = np.diag(W) + cho_solve(K_chol, np.eye(len(W)))
        H_chol = cho_factor(H)
        log_det_H = 2 * np.sum(np.log(np.diag(H_chol[0])))
        log_Z = log_lik + log_prior - 0.5 * log_det_H
        return log_Z.flatten()[0]

def optimize_rbf_hyperparameters(X_train, y_train):
    def objective(params):
        length_scale = np.exp(params[0])
        variance = np.exp(params[1])
        kernel = lambda X1, X2: rbf_kernel(
            X1, X2, length_scale=length_scale, variance=variance
        )
        gpc = GaussianProcessClassifier(kernel)
        gpc.fit(X_train, y_train)
        return -gpc.log_marginal_likelihood()

    res = minimize(
        objective,
        x0=np.log([1.0, 1.0]),
        bounds=[(-5, 5), (-5, 5)]
    )
    best_l, best_v = np.exp(res.x)
    return best_l, best_v


# 执行代码
if __name__ == "__main__":
    best_l, best_v = optimize_rbf_hyperparameters(X_train, y_train)
    print(f"最佳 length_scale = {best_l:.4f}, variance = {best_v:.4f}")
    kernel = lambda X1, X2: rbf_kernel(X1, X2, length_scale=best_l, variance=best_v)
    gpc = GaussianProcessClassifier(kernel)
    gpc.fit(X_train, y_train)

    X_test = np.linspace(-6, 6, 200).reshape(-1, 1)
    prob = gpc.predict(X_test)
    print("前 5 个预测概率：", prob[:5])
    print("Log Marginal Likelihood（Laplace）：", gpc.log_marginal_likelihood())
```

## 1. 准备过程

与高斯过程回归类似，高斯过程分类中的核函数超参数（如 RBF 核的长度尺度、幅度等）也需要通过最大化边际似然进行学习。

在回归任务中，由于观测噪声服从高斯分布，模型始终保持高斯结构，因此可以直接写出对数边际似然的解析形式：

$$
\log P(y | X, \theta) = -\frac{1}{2} y^{\rm T} (K + \sigma_n^2 \mathbf{I})^{-1} y - \frac{1}{2} \log |K + \sigma_n^2 \mathbf{I}| - \frac{N}{2} \log 2\pi
$$

这使得高斯过程回归的训练过程在数学上非常简洁，无需额外的近似方法。

然而在分类问题中情况完全不同。由于输出 $y_i \in {0,1}$ ，似然由伯努利分布决定，并通过 sigmoid 链接函数与潜在函数 $f$ 关联，因此整个模型不再保持高斯形式。结果是后验分布无法写成高斯，边际似然自然也无法解析地求解。

为了继续进行参数学习，我们必须对后验分布进行近似，而最常用、最直接的方法便是拉普拉斯近似。它与我们在贝叶斯逻辑回归中使用的方法完全一致（具体求解过程可以参考[上面](#拉普拉斯近似)的拉普拉斯近似讲解，下面的学习过程也给出具体流程，这里假设该分布已经求出）：

$$
P(f | X, y, \theta) \approx \mathcal{N}(f_{\text{MAP}}, H^{-1})
$$

接下来利用贝叶斯恒等式：

$$
P(f | X, y, \theta) = \frac{P(y | f, X) P(f | X, \theta)}{P(y | X, \theta)}
$$

在 $f = f_\text{MAP}$ 处取其对数可得：

$$
\log P(y | X, \theta) = \log P(y | f_{\text{MAP}}, X) + \log P(f_{\text{MAP}} | X, \theta) - \log P(f_{\text{MAP}} | X, y, \theta)
$$

其中第一项是似然项，直接套用对数伯努利似然公式即可：

$$
\log P(y | f_{\text{MAP}}, X) = \sum_i \Big[ y_i \log \sigma(f_{\text{MAP},i}) + (1 - y_i) \log \big(1 - \sigma(f_{\text{MAP},i})\big) \Big]
$$

第二项是先验项，我们依旧假设先验服从高斯分布 $f \sim \mathcal{N}(0, K_{\theta})$（本质就是一个高斯过程），取对数后可得：

$$
\log P(f_{\text{MAP}} \mid X, \theta) = -\frac{1}{2} f_{\text{MAP}}^{\rm T} K_\theta^{-1} f_{\text{MAP}} - \frac{1}{2} \log |K_\theta| - \frac{n}{2} \log 2\pi
$$

第三项是后验项，由前面的拉普拉斯近似求出：

$$
-\log P(f_{\text{MAP}} | X, y, \theta) \approx \frac{1}{2} \log |H| + \frac{n}{2} \log 2\pi
$$

将上述三项整理，可以得到高斯过程分类中常用的对数边际似然近似：

$$
\log P(y | X, \theta) \approx \ell(f_{\text{MAP}}) - \frac{1}{2} f_{\text{MAP}}^{\rm T} K_\theta^{-1} f_{\text{MAP}} - \frac{1}{2} \log |H| + \frac{n}{2} \log 2\pi
$$

```py showLineNumbers
# 定义 RBF 核函数
def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1)
    X2 = np.atleast_2d(X2)
    sqdist = (
        np.sum(X1**2, 1).reshape(-1, 1)
        + np.sum(X2**2, 1)
        - 2 * X1 @ X2.T
    )
    return variance * np.exp(-0.5 / length_scale**2 * sqdist)

# 对数边际似然函数
def log_marginal_likelihood(self):
    f = self.f_map
    y = self.y_train
    W = self.W
    pi = self.sigmoid(f)
    log_lik = np.sum(
        y * np.log(pi + 1e-12) + (1 - y) * np.log(1 - pi + 1e-12)
    )
    K_chol = self.K_chol
    Kinv_f = cho_solve(K_chol, f)
    log_prior = -0.5 * f.T @ Kinv_f
    H = np.diag(W) + cho_solve(K_chol, np.eye(len(W)))
    H_chol = cho_factor(H)
    log_det_H = 2 * np.sum(np.log(np.diag(H_chol[0])))
    log_Z = log_lik + log_prior - 0.5 * log_det_H
    return log_Z.flatten()[0]

# 超参数优化函数
def optimize_rbf_hyperparameters(X_train, y_train):
    def objective(params):
        length_scale = np.exp(params[0])
        variance = np.exp(params[1])
        kernel = lambda X1, X2: rbf_kernel(
            X1, X2, length_scale=length_scale, variance=variance
        )
        gpc = GaussianProcessClassifier(kernel)
        gpc.fit(X_train, y_train)
        return -gpc.log_marginal_likelihood()

    res = minimize(
        objective,
        x0=np.log([1.0, 1.0]),
        bounds=[(-5, 5), (-5, 5)]
    )
    best_l, best_v = np.exp(res.x)
    return best_l, best_v
```

## 2. 学习过程

在高斯过程分类中，训练目标是学习潜在函数 $f$ 的分布，使得它能够解释训练标签 $y$ 的观测情况。由于伯努利似然与高斯先验不兼容，后验 $P(f|X, y, \theta)$ 不再是高斯，无法直接解析求解。因此学习过程的核心是对后验进行近似，我们依旧使用拉普拉斯近似：

$$
P(f | X, y, \theta) \approx \mathcal{N}(f_{\text{MAP}}, H^{-1})
$$

我们来求解这个高斯分布的参数，首先构造对数后验：

$$
\log P(f | X, y, \theta) = \log P(y | f) + \log P(f | X, \theta)
$$

然后对 $f$ 求导并令其为零可得：

$$
\nabla_f \log P(f | X, y, \theta) = 0
$$

这通常通过 **牛顿法** 求解，因为 $\log P(y|f)$ 的形式是非线性的。

只要得到了 $f_\text{MAP}$ 就可以使用公式直接求解出 Hessian 矩阵：

$$
H = -\nabla_f^2 \log P(f | X, y, \theta) \Big|_{f = f_{\text{MAP}}}
$$

```py showLineNumbers
def fit(self, X_train, y_train):
    self.X_train = np.atleast_2d(X_train)
    self.y_train = y_train.reshape(-1, 1)
    n = len(y_train)

    def K_solve(v):
        return cho_solve(K_chol, v)

    self.K = self.kernel(self.X_train, self.X_train)
    f = np.zeros((n, 1))
    K_chol = cho_factor(self.K + 1e-6 * np.eye(n))
    for _ in range(self.max_iter):
        pi = self.sigmoid(f)
        W = (pi * (1 - pi)).flatten()

        grad = self.y_train - pi - K_solve(f)
        H = np.diag(W) + cho_solve(K_chol, np.eye(n))

        try:
            H_chol = cho_factor(H)
            delta = cho_solve(H_chol, grad)
        except:
            delta = np.linalg.solve(H, grad)

        f_new = f + delta
        if np.max(np.abs(delta)) < self.tol:
            f = f_new
            break
        f = f_new

    self.f_map = f
    self.W = (pi * (1 - pi)).flatten()

    H = np.diag(self.W) + cho_solve(K_chol, np.eye(n))
    H_chol = cho_factor(H)
    self.Sigma = cho_solve(H_chol, np.eye(n))

    self.K_chol = K_chol
    self.is_fit = True
```

## 3. 预测过程

假设我们在学习阶段得到了后验的拉普拉斯近似，现在要对新的输入点 $X_*$ 预测潜在函数值 $f_*$ 以及标签 $y_*$ ：

- 潜在函数预测

    潜在函数 $f_*$ 的条件分布为：

    $$
    f_* | X_*, X, f_{\text{MAP}}, \theta \sim \mathcal{N}(\mu_*, \sigma_*^2)
    $$

    其中的参数解析式为（直接套用高维高斯分布的参数公式）：

    $$
    \mu_* = K(X_*, X) K^{-1} f_{\text{MAP}}
    $$

    $$
    \sigma_*^2 = K(X_*, X_*) - K(X_*, X) (K + W^{-1})^{-1} K(X, X_*)
    $$

    其中 $W$ 是 $H$ 的一部分，满足公式 $H = K^{-1} + W$ 。

- 标签预测

    由于输出是二分类，我们需要将潜在函数 $f_*$ 经过 Sigmoid 映射得到类别概率：

    $$
    P(y_* = 1 | X_*, X, y) = \int \sigma(f_*) P(f_* | X_*, X, y) \, df_*
    $$

    这个积分依旧是没有解析解，因此常用近似方法，这里不再给出。

因为分类标签无法直接求解并且只与潜在函数有关，因此我们要先求解潜在函数。

```py showLineNumbers
def predict(self, X_test):
    if not self.is_fit:
        raise RuntimeError("请先调用 fit() 训练模型。")

    X_test = np.atleast_2d(X_test)
    K_s = self.kernel(self.X_train, X_test)
    m_star = K_s.T @ cho_solve(self.K_chol, self.f_map)

    # predictive variance approx
    W_inv = np.diag(1.0 / (self.W + 1e-12))
    A = self.K + W_inv
    A_chol = cho_factor(A)

    v = cho_solve(A_chol, K_s)
    k_ss = self.kernel(X_test, X_test).diagonal()
    s2 = k_ss - np.sum(K_s * v, axis=0)

    # logistic integral approximation
    denom = np.sqrt(1 + np.pi * s2 / 8)
    prob = self.sigmoid(m_star.flatten() / denom)
    return prob
```

---

# 参考文献列表

## 贝叶斯逻辑回归

1. [A Short Intro to Bayesian Logistic Regression](https://medium.com/@wtc2189/day-6-a-short-intro-to-bayesian-logistic-regression-6141c1d1d6c9)

2. [Variational Inference using Implicit Models](https://www.inference.vc/variational-inference-with-implicit-probabilistic-models-part-1-2/)

3. [Bayesian inference for a logistic regression model](https://darrenjw.wordpress.com/2022/08/07/bayesian-inference-for-a-logistic-regression-model-part-1/)

## 高斯过程分类

1. [高斯过程分类方法](https://apxml.com/zh/courses/bayesian-machine-learning/chapter-4-gaussian-processes/gp-classification-techniques)

2. [GaussianProcessClassifier（高斯过程分类器）](https://scikit-learn.cn/1.6/modules/generated/sklearn.gaussian_process.GaussianProcessClassifier.html)

3. [基于高斯过程分类的小样本图像识别](https://pdf.hanspub.org/AIRR20220400000_64886947.pdf)

4. [结合半监督核的高斯过程分类](https://nlpr.ia.ac.cn/2009papers/gnkw/nk9.pdf)