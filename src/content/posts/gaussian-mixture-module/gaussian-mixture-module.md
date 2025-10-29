---
title: 【机器学习基本模型】第六节：高斯混合模型
published: 2025-10-27
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 高斯混合模型基本原理

前面我们讲到了诸多的 **分类算法** （Classification Algorithm），虽然它们的数学原理差别很大，但它们其实都属于 **有监督学习** （Supervised Learning）这一个类别当中。也就是说：它们在训练过程中需要数据拥有自己对应的标签。

而我们今天要讲的 **高斯混合模型** （Gaussian Mixture Model，简称 GMM），它是一个 **聚类算法** （Clustering Algorithm），而聚类算法不同于分类算法，它们属于 **无监督学习** （Unsupervised Learning）这一类别。也就是说：高斯混合模型不要求数据有自己的标签，高斯混合模型会自动地将数据分为不同的类别。

我们来思考一个简单的问题：如果给你一些数据，你想用什么模型去拟合这些数据的分布呢？可能很多人的第一想法就是用正态分布去拟合，毕竟正态分布是生活中最为常见的分布。其实这个想法是正确的，但仍有缺陷：虽然正态分布是最常见的分布，但现实世界太过于复杂，我们不能确保一个正态分布就能拟合出所有的数据集。对此，我们可以试着想一想：如果用多个正态分布去拟合，效果会不会更好？没错，这正是高斯混合模型的出发点。

## 高斯加权混合

为了解决高斯模型的单峰性的问题，我们引入多个高斯模型的加权平均来拟合多峰数据：

$$
P(x) = \sum_{k=1}^K \alpha_k \mathcal{N}(\mu_k, \Sigma_k)
$$

由于我们只能观察到每个样本 $x$ 的信息，而无法了解每个样本究竟属于哪个高斯分布，因此我们可以引入一个隐变量 $z$ （ $z = k$ 表示样本属于第 K 个高斯分布）来辅助我们的推导：

$$
P(z = i) = p_i \quad \sum_{i=1}^{k} P(z = i) = 1
$$

于是 $P(x)$ 可以写成：

$$
P(x) = \sum_z P(x,z) = \sum_{k=1}^K P(x,z=k) = \sum_{k=1}^K P(z=k) P(x|z=k)
$$

最后可以得到：

$$
P(x) = \sum_{k=1}^K p_k \mathcal{N}(x|\mu_k,\Sigma_k)
$$

值得注意的是：高斯混合模型并 **不在意** 每个数据点究竟属于哪个类别（只是推导过程关注于单个数据点）。它想要做的事情是让多个高斯模型去拟合整个数据集，从而去预测新数据属于哪哪个高斯分布。另外，高斯混合模型也 **不能确定** 究竟要用多少个高斯云（即高斯分布的图像）去拟合图像，因此要自己设置初始值 K。

![高斯混合模型图像](src\content\posts\gaussian-mixture-module\高斯混合模型1.jpg)

## 梯度下降的局限

写出高斯混合模型的对数似然函数：

$$
\begin{align*}
L(\theta) &= \sum_{i=1}^{N} \log P(x_i) = \sum_{i=1}^{N} \log \sum_{k=1}^{K} p_k \mathcal{N}(x_i | \mu_k, \Sigma_k)
\end{align*}
$$

其中 $\theta = \{p_1, p_2, \dots, p_K, \mu_1, \mu_2, \dots, \mu_K, \Sigma_1, \Sigma_2, \dots, \Sigma_K\}$

对这个表达式直接通过求导，由于连加号的存在，会无法得到解析解。因此我们无法直接根据极大似然估计的原理对这个式子使用常见的梯度下降算法。

# EM 算法

由于无法直接对含有隐变量的似然函数求导，所以梯度下降无法求解出 GMM 的极大似然估计。对此我们引入一个专门解决此类问题的算法：EM 算法。

![高斯混合模型图像](src\content\posts\gaussian-mixture-module\EM算法1.jpg)

## 证据下界

我们可以先假设 $Z$ 服从的分布为 $Z \sim q(Z | \theta)$ ，于是有：

$$
\begin{align*}
\log P(X | \theta) &= \log P(X, Z | \theta) - \log P(Z | X, \theta) \\
&= \log \frac{P(X, Z | \theta)}{q(Z | \theta)} - \log \frac{P(Z | X, \theta)}{q(Z | \theta)}
\end{align*}
$$

两边同时关于 $Z \sim q(Z | \theta)$ 同时计算期望：

$$
\begin{align*}
\log P(X | \theta) &= \sum_{Z} q(Z | \theta) \log \frac{P(X, Z | \theta)}{q(Z | \theta)} - \sum_{Z} q(Z | \theta) \log \frac{P(Z | X, \theta)}{q(Z | \theta)} \\
&= \mathbb{E}_{Z \sim P(Z|X,\theta^{(t)})} \Big[ \log P(X, Z | \theta) \Big] - \sum_{Z} q(Z | \theta) \log q(Z | \theta) + \operatorname{KL}(q(Z | \theta) \parallel P(Z | X, \theta)) \\
&= \mathbb{E}_{Z \sim P(Z|X,\theta^{(t)})} \Big[\log P(X, Z | \theta) \Big] + H(q(Z | \theta)) + \operatorname{KL}(q(Z | \theta) \parallel P(Z | X, \theta)) \\
&= ELBO(q, \theta | X) + \operatorname{KL}(q(Z | \theta) \parallel P(Z | X, \theta))
\end{align*}
$$

由于 KL 散度始终大于 0 ，因此 **ELBO** （Evidence Lower Bound Optimization，中文译名为 **证据下界** ）是 $L(\theta)$ 的一个下界（至于什么是 KL 散度可以参考下面这个视频）。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114558102410096&bvid=BV1r6jHzpE1J&cid=30166354742&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 流程介绍

EM 算法本质上是通过最大化 ELBO 来间接最大化对数似然函数。具体步骤分为 E-step 和 M-step。

- 寻找使得 KL 散度最小的 $q^{(t+1)}(Z) = P\left( Z | X, \theta^{(t)} \right)$ ，使得 ELBO 进一步逼近 $L(\theta)$
- 寻找 $ELBO(\theta | q^{(t+1)}, X)$ 的极大值点作为新参数 $\theta^{(t+1)}$

两者交替迭代，最终收敛到局部最优解。

### E-step

$$
L(\theta) - \text{ELBO}(q,\theta | X) = \text{KL}(q \parallel P(Z | X,\theta))
$$

要使 ELBO 逼近 $L(\theta)$ ，就要让 KL 散度最小，先通过当前参数 $\theta^{(t)}$ 估计 $q^{(t+1)}$ ，得 $q^{(t+1)}(Z) = P\left(Z | X, \theta^{(t)}\right)$ ，于是有：

$$
\begin{align*}
L(\theta) &= \log P(X | \theta) = \mathbb{E}_{Z \sim P(Z | X, \theta^{(t)})} \Big[ \log P(X | \theta) \Big] \\
&= Q(\theta | \theta^{(t)}) + \text{KL}(P(Z | X, \theta^{(t)}) \parallel P(Z | X, \theta))
\end{align*}
$$

这里我们将 $ELBO(\theta | q^{(t+1)}, X)$ 记为 $Q(\theta | \theta^{(t)})$ ：

$$
Q(\theta | \theta^{(t)}) = \mathbb{E}_{Z \sim P(Z | X,\theta^{(t)})} \Big[ \log P(X,Z | \theta) \Big] + H(P(Z | X,\theta^{(t)}))
$$

### M-step

由于信息熵为常数项，因此最大化 $Q(\theta | \theta^{(t)})$ 等价于将对数似然 $\log P(X, Z | \theta)$ 的期望最大化：

$$
\theta^{(t+1)} = \arg \max_{\theta} Q(\theta | \theta^{(t)}) = \arg \max_{\theta} \mathbb{E}_{Z \sim P(Z|X,\theta^{(t)})} \Big[ \log P(X, Z | \theta) \Big]
$$

## 理论推导

> 以下推导部分参考自该视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1400527903&bvid=BV1Q6421u7qb&cid=1448856301&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

我们先用 **琴声不等式** （Jensen's inequality）放缩的方式求解出 ELBO：

$$
\begin{align*}
L(\theta^{(t)}) &= \sum_{X} \log P(X | \theta^{(t)}) = \sum_{X} \log \left[ \sum_{Z} P(X,Z | \theta^{(t)}) \right] \\
&= \sum_{X} \log \left[ \sum_{Z} q^{(t+1)}(Z)\, \frac{P(X,Z | \theta^{(t)})}{q^{(t+1)}(Z)} \right] = \sum_{X} \log \mathbb{E}_{Z\sim q^{(t+1)}(Z)} \Big[ \frac{P(X,Z | \theta^{(t)})}{q^{(t+1)}(Z)} \Big] \\
&\ge \sum_{X} \mathbb{E}_{Z\sim q^{(t+1)}(Z)} \Big[ \log \frac{P(X,Z | \theta^{(t)})}{q^{(t+1)}(Z)} \Big] = \sum_{X}\sum_{Z} q^{(t+1)}(Z) \log \frac{P(X,Z | \theta^{(t)})}{q^{(t+1)}(Z)}
\end{align*}
$$

根据琴声不等式的取等条件我们可知：

$$
\frac{P(X, Z | \theta^{(t)})}{q^{(t+1)}(Z)} = C \quad \text{where } \sum_{Z} q^{(t+1)}(Z) = 1
$$

将 $q^{(t+1)}(Z)$ 乘到等式的右侧可得：

$$
P(X, Z | \theta^{(t)}) = C \cdot q^{(t+1)}(Z)
$$

因为 $q^{(t+1)}(Z)$ 对变量 $Z$ 的积分为 1，因此我们将两边同时对 $Z$ 进行积分：

$$
\sum_{Z} P(X, Z | \theta^{(t)}) = \sum_{Z} C \cdot q^{(t+1)}(Z) = C \sum_{Z} q^{(t+1)}(Z) = C
$$

将上式重新代入琴声不等式的取等条件中：

$$
q^{(t+1)}(Z) = \frac{P(X, Z | \theta^{(t)})}{\sum_{Z} P(X, Z | \theta^{(t)})} = \frac{P(X, Z | \theta^{(t)})}{P(X | \theta^{(t)})} = P(Z | X, \theta^{(t)})
$$

于是我们就轻松求解出 E-step 中的 $q^{(t+1)}(Z)$ 了。

由于不等式已经取等，因此有：

$$
\begin{align*}
L(\theta^{(t)}) &= \sum_{X} \sum_{Z} q^{(t+1)}(Z) \log \left[ \frac{P(X, Z | \theta^{(t)})}{q^{(t+1)}(Z)} \right] \\
&= \sum_{X, Z} q^{(t+1)}(Z) \log P(X, Z | \theta^{(t)}) - \sum_{X, Z} q^{(t+1)}(Z) \log q^{(t+1)}(Z) \\
&= \mathbb{E}_{Z\sim q^{(t+1)}(Z)} \Big[ L(X, Z | \theta^{(t)}) \Big] - \sum_{X, Z} P(Z | X, \theta^{(t)}) \log P(Z | X, \theta^{(t)})
\end{align*}
$$

由于后面的信息熵为常数，所以 $\theta$ 的极大似然估计为：

$$
\begin{align*}
\theta^{(t+1)} &= \arg \max_{\theta} \sum_{X} \sum_{Z} q^{(t+1)}(Z) \log \left[ \frac{P(X, Z | \theta)}{q^{(t+1)}(Z)} \right] \\
&= \arg \max_{\theta} \mathbb{E}_{Z\sim P(Z | X, \theta)} \Big[ \log P(X, Z | \theta^{(t)}) \Big]
\end{align*}
$$

## 收敛性证明

EM 算法的流程并不复杂，但是还有一个很重要的问题需要我们思考：EM 算法收敛吗？如果 EM 算法无法正常收敛，那么这个算法的过程无论多么精美都没用。就让我们再证明一下 EM 算法的收敛性吧。

根据单调有界原理，如果数列单调递增且有界，那么该数列收敛。

- 首先我们来看看有界性。

定义似然函数：

$$
L(\theta) = \sum_{X} \log P(X | \theta)
$$

由于概率值有界，而有界函数的有限次线性组合仍然有界，因此 $L(\theta)$ 有界。

- 然后我们来看看单调性。

不妨设函数 $F(q, \theta)$ ：

$$
F(q, \theta) = \sum_{X}\sum_{Z} q(Z) \log \frac{P(X,Z | \theta)}{q(Z)}
$$

其中 $q(Z)$ 可以是任意分布。

在 EM 算法执行之前，根据琴声不等式，对于任意的 $q$ ，有下列关系：

$$
L(\theta^{(t)}) \geq F(q, \theta^{(t)})
$$

经过 E-step 的迭代后，因为 E-step 的目的就是让琴声不等式取等，所以有：

$$
L(\theta^{(t)}) \geq F(q^{(t+1)}, \theta^{(t)})
$$

因为 M-step 的目标如下：

$$
\theta^{(t+1)} = \arg \max_{\theta} F(q^{(t+1)}, \theta)
$$

显然有下列关系：

$$
F(q^{(t+1)}, \theta^{(t+1)}) \geq F(q^{(t+1)}, \theta^{(t)})
$$

回到最上面的关系，令 $q = q^{(t+1)}$

$$
L(\theta^{(t+1)}) \geq F(q^{(t+1)}, \theta^{(t+1)})
$$

将上面所有步骤组成不等式链可得：

$$
L(\theta^{(t+1)}) \ge F(q^{(t+1)}, \theta^{(t+1)}) \ge F(q^{(t+1)}, \theta^{(t)}) = L(\theta^{(t)})
$$

因此函数 $L(\theta)$ 具有单调性。

# 代码实现

准备了这么多，终于可以来看一下 GMM 的代码了。

```py frame="code" title="main.py"
import numpy as np
np.random.seed(0)
X1 = np.random.multivariate_normal([0,0], [[1,0],[0,1]], 100)
X2 = np.random.multivariate_normal([5,5], [[1,0],[0,1]], 100)
X = np.vstack([X1, X2])


# 计算多维高斯概率密度函数
def gaussian_pdf(x, mean, cov):
    D = x.shape[0]
    cov_det = np.linalg.det(cov)
    cov_inv = np.linalg.inv(cov)
    norm_const = 1.0 / np.sqrt((2 * np.pi)**D * cov_det)
    diff = x - mean
    return norm_const * np.exp(-0.5 * diff.T @ cov_inv @ diff)

class GMM:
    def __init__(self, n_components, tol=1e-6, max_iter=100):
        self.K = n_components
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, X):
        # 初始化参数
        N, _ = X.shape
        self.p = np.ones(self.K) / self.K
        self.mu = X[np.random.choice(N, self.K, replace=False)]
        self.Sigma = np.array([np.cov(X, rowvar=False)] * self.K)

        log_likelihood_old = 0
        for _ in range(self.max_iter):
            # E-step
            gamma = np.zeros((N, self.K))
            for i in range(N):
                for k in range(self.K):
                    gamma[i, k] = self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
                gamma[i, :] /= np.sum(gamma[i, :])

            # M-step
            N_k = np.sum(gamma, axis=0)
            self.p = N_k / N
            self.mu = (gamma.T @ X) / N_k[:, np.newaxis]
            for k in range(self.K):
                diff = X - self.mu[k]
                self.Sigma[k] = (gamma[:, k][:, np.newaxis] * diff).T @ diff / N_k[k]

            # 计算对数似然函数判断是否收敛
            log_likelihood = 0
            for i in range(N):
                temp = 0
                for k in range(self.K):
                    temp += self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
                log_likelihood += np.log(temp)

            if np.abs(log_likelihood - log_likelihood_old) < self.tol:
                break
            log_likelihood_old = log_likelihood

        return self

    # 软预测函数
    def predict_proba(self, X):
        N = X.shape[0]
        gamma = np.zeros((N, self.K))
        for i in range(N):
            for k in range(self.K):
                gamma[i, k] = self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
            gamma[i, :] /= np.sum(gamma[i, :])
        return gamma

    # 硬预测函数
    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)


# 执行代码
if __name__ == "__main__":
    gmm = GMM(n_components=2)
    gmm.fit(X)

    labels = gmm.predict(X)
    print("混合系数 p:", gmm.p)
    print("均值 mu:", gmm.mu)
    print("协方差 Sigma:", gmm.Sigma)
```

## E-step

E-step 的目标是计算每个数据点属于每个分量的 **后验概率** ，因此有：

$$
\gamma_{ik} = P(z_{ik} = 1 \mid x_i, \theta^{(t)}) = \frac{p_k^{(t)} \, \mathcal{N}(x_i \mid \mu_k^{(t)}, \Sigma_k^{(t)})}{\sum_{j=1}^K p_j^{(t)} \, \mathcal{N}(x_i \mid \mu_j^{(t)}, \Sigma_j^{(t)})}
$$

这里 $\gamma_{ik}$ 通常称为 **responsibility** ，表示第 $K$ 个高斯对 $x_i$ 的责任。

```py showLineNumbers
gamma = np.zeros((N, self.K))
for i in range(N):
    for k in range(self.K):
        gamma[i, k] = self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
    gamma[i, :] /= np.sum(gamma[i, :])
```

## M-step

M-step 是最大化 期望的完整数据对数似然：

$$
Q(\theta | \theta^{(t)}) = \sum_{i=1}^N \sum_{k=1}^K \gamma_{ik} \, \log \big( p_k \, \mathcal{N}(x_i \mid \mu_k, \Sigma_k) \big)
$$

根据定义可以知道 **混合系数$p_k$** 、 **均值$\mu_k$** 和 **协方差$Sigma_k$** 的更新公式：

$$
p_k^{(t+1)} = \frac{1}{N} \sum_{i=1}^N \gamma_{ik}
$$

$$
\mu_k^{(t+1)} = \frac{\sum_{i=1}^N \gamma_{ik} x_i}{\sum_{i=1}^N \gamma_{ik}}
$$

$$
\Sigma_k^{(t+1)} = \frac{\sum_{i=1}^N \left[ \gamma_{ik} (x_i - \mu_k^{(t+1)}) \right]^{\rm T} (x_i - \mu_k^{(t+1)})}{\sum_{i=1}^N \gamma_{ik}}
$$

```py showLineNumbers
N_k = np.sum(gamma, axis=0)
self.p = N_k / N
self.mu = (gamma.T @ X) / N_k[:, np.newaxis]
for k in range(self.K):
    diff = X - self.mu[k]
    self.Sigma[k] = (gamma[:, k][:, np.newaxis] * diff).T @ diff / N_k[k]
```

# 参考文献

## 高斯混合模型

1. [高斯混合模型（GMM）](https://zhuanlan.zhihu.com/p/30483076)

2. [【维基百科】高斯混合模型](https://en.wikipedia.org/wiki/Mixture_model#Gaussian_mixture_model)

3. [高斯混合模型 GMM计算方法](https://www.cnblogs.com/conpi/p/18956198)

4. [机器学习-09-高斯混合模型GMM](https://www.cnblogs.com/Cnoized/p/18897547)

5. [GMM：高斯混合模型原理实现与应用](https://zhuanlan.zhihu.com/p/619191372)

6. [混合高斯模型](https://blog.csdn.net/u013172930/article/details/144853287)

7. [高斯混合模型的数学基础与理论分析](https://juejin.cn/post/7321778862785544202)

8. [高斯混合模型(Gaussian Mixture Model)与EM算法原理(一)](https://zhuanlan.zhihu.com/p/60649774)

9. [高斯混合模型(Gaussian Mixture Model)与EM算法原理(二)](https://zhuanlan.zhihu.com/p/61103099)

10. [GMM (Gaussian Mixture Model)](https://aandds.com/blog/gmm.html)

11. [【ScikitLearn】高斯混合模型](https://scikit-learn.cn/stable/modules/mixture.html)

## EM 算法

1. [EM算法的理解和详细推导](https://jaredddddd.github.io/2024/01/01/EM/)

2. [深入理解EM算法（ELBO+KL形式）](https://zhuanlan.zhihu.com/p/365641813)

3. [深入剖析EM算法：原理、推导与应用](https://blog.csdn.net/2501_90186640/article/details/147234092)

4. [EM算法详解](https://luyiyun.github.io/2020/12/08/methods/methods-em/)

5. [EM（最大期望）算法推导、GMM的应用与代码实现](https://www.cnblogs.com/qizhou/p/13100817.html)