---
title: 【机器学习基本模型】第四节：朴素贝叶斯分类器
published: 2025-10-25
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: true
---

# 朴素贝叶斯分类器基本原理

**朴素贝叶斯分类器（Naive Bayes Classifier）** 是一种基于 **贝叶斯定理（Bayes' Theorem）** 并假设各个特征之间 **相互独立** 的概率分类模型。它属于 **生成式模型** ，常用于文本分类、垃圾邮件检测、情感分析、医学诊断等任务。

朴素贝叶斯分类器是 **贝叶斯决策论** 在分类任务中的一个具体实现，它通过条件独立假设来 **近似实现** 贝叶斯最优决策规则。因此我们要想了解朴素贝叶斯分类器，首先就得知道什么是贝叶斯决策论。

![贝叶斯肖像](.\贝叶斯肖像.gif)

## 最优分类器

假设有 $N$ 种可能的类别标记，即 $Y = \{ c_1, c_2, \dots, c_N \}$ 是将一个真实标记为 ​$c_i$ 的样本误分类为 $c_j$ 所产生的损失，基于后验概率 $P(c_i|x)$ 可获得将样本 $x$ 分类为 $c_i$ 所产生的期望损失（Expected Loss）, 即在样本 $P(c_i | x)$ 上的 **条件风险（Conditional Risk）**。

$$
R(c_i|x) = \sum_{j=1}^N \lambda_{ij} P(c_j|x)
$$

我们的任务是寻找一个判定准则 $h : X \mapsto Y$ ，以最小化总体风险：

$$
R(h) = \mathbb{E}_{x} \Big[ R(h(x)|x) \Big]
$$

显然，对每个样本 $x$ 若 $h$ 能最小化条件风险 $R(h(x) | x)$ ，则总体风险 $R(h)$ 也将被最小化，这就产生了贝叶斯判定准则（Bayes Decision Rule）：为最小化总体风险，只需在每个样本上选择那个能使条件风险 $R(c | x)$ 最小的类别标记（要想均值最小化，只需要最小化每一个样本）。

$$
h^*(x) = \arg \min_{c \in \mathcal{Y}} R(c|x)
$$

此时 $h^*$ 称为 **贝叶斯最优分类器（Bayes Optimal Classifier）**，与之对应的总体风险 $R(h^*)$ 称为 **贝叶斯风险（Bayes Risk）**。而 $1 - R(h^*)$ 则反映了分类器所能达到的最佳性能，即通过机器学习所能产生的模型精度的理论上限。

具体来说，若目标是最小化分类错误率，则误判损失函数可写为：

$$
\lambda_{ij} = 
\begin{cases} 
0, & i = j \\ 
1, & i \neq j 
\end{cases}
$$

此时条件风险为 $R(c|x) = 1 - P(c|x)$ ，于是最小化分类错误率的贝叶斯最优分类器可以写作：

$$
h^*(x) = \arg \max_{c \in \mathcal{Y}} P(c|x)
$$

即对每个样本应选择能使后验概率 $P(c|x)$ 最大的类别标记。

## 朴素贝叶斯

不难看出，欲使用贝叶斯判定准则来最小化决策风险，首先要获得后验概率 $P(c|x)$ 。然而，在现实任务中这通常难以直接获得。从这个角度来看，机器学习所要实现的是 **基于有限的训练样本集** 尽可能准确地 **估计** 出后验概率 $P(c|x)$ 。

![朴素贝叶斯分类器图像](.\朴素贝叶斯分类器1.jpg)

大体来说，主要有两种策略：

- 通过直接建模 $P(c|x)$ 来预测 $c$ ，这样得到的是 **判别式模型（Discriminative Models）**，代表是决策树、BP 神经网络、支持向量机等
- 先对联合概率分布 $P(x, c)$ 建模，然后再由此获得 $P(c|x)$ ，这样得到的是 **生成式模型（Generative Models）**，代表是贝叶斯分类器等

> 判别式模型是给定特征的情况下预测这个样本的标签
> 
> 生成式模型是假设样本的分布特征后构建分类模型

对于生成式模型，必然考虑：

$$
P(c|x) = \frac{P(x, c)}{P(x)} = \frac{P(c)P(x|c)}{P(x)}
$$

- $P(c)$ 是类 **先验** （Prior）概率，表达了样本空间中各类样本所占的比例，可通过各类样本出现的频率来进行估计（大数定律）
- $P(c|x)$ 是样本 $x$ 相对于类标记 $c$ 的类 **条件概率（Class-Conditional Probability）**，或称为 **似然（Likelihood）**
- $P(x)$ 是用于归一化的 **证据（Evidence）** 因子，与类别无关，可以不考虑

不难发现，基于贝叶斯公式来估计后验概率 $P(c|x)$ 的主要困难在于：类条件概率 $P(x|c)$ 是所有属性上的联合概率，难以从有限的训练样本直接估计而得。为避开这个障碍，朴素贝叶斯分类器采用了 **属性条件独立性假设（Attribute Conditional Independence Assumption）**：对已知类别，假设所有属性相互独立。

基于属性条件独立性假设，贝叶斯公式可重写为：

$$
P(c|x) = \frac{P(c)P(x|c)}{P(x)} = \frac{P(c)}{P(x)} \prod_{i=1}^d P(x_i|c)
$$

由于对所有类别来说 $P(x)$ 相同，因此基于贝叶斯判定准则有：

$$
h_{nb}(x) = \arg\max_{c \in \mathcal{Y}} P(c) \prod_{i=1}^{d} P(x_i|c)
$$

这就是朴素贝叶斯分类器的表达式。

---

# 朴素贝叶斯分类器代码实现

在给出代码之前，我们先介绍一个重要的操作 ———— **拉普拉斯平滑（Laplace Smoothing）**。在朴素贝叶斯模型中，如果某个特征 **在训练数据中从未出现过** ，那么模型会将其对应的概率估计为 0 。这样一来，当我们计算类别的联合概率（多个特征概率的乘积）时，只要出现一个 0 ，整个结果就会变成 0 ，导致分类器彻底失效。为了解决这个问题，我们需要对类条件概率 $P(c_i|x)$ 进行适当修正，即在统计频数的基础上加入一个平滑项，从而避免出现零概率的情况。

除了 “朴素” 假设外，朴素贝叶斯分类器还要假定样本的分布，因此根据假设分布的不同，朴素贝叶斯分类器还分为不同的种类。下面我们就介绍最常见的三种朴素贝叶斯分类器，并且因为朴素贝叶斯分类器实现繁杂（原理很简单），我们就用 ScikitLearn 机器学习库来实现。 

对于任何一个朴素贝叶斯分类器来说，我们只需要求解出 $P(c)$ 与 $P(x|c)$ 即可（并且朴素贝叶斯分类器也是一个 “闭式解” 模型，因此无需梯度迭代）。$P(c)$ 的求解方式是用频率估计概率，也就是直接用样本计数的方式求解；$P(x|c)$ 则是我们的假设分布，对于不同的朴素贝叶斯分类器，我们有不同的假设分布。

## 1. 高斯贝叶斯

对于高斯贝叶斯分类器，假设分布如下：

$$
P(x_i | c) = \frac{1}{\sqrt{2\pi\sigma_{c,i}^2}} 
\exp\left(-\frac{(x_i - \mu_{c,i})^2}{2\sigma_{c,i}^2}\right)
$$

由于求解高斯分布只需要用到样本的均值和方差，因此无需做拉普拉斯平滑操作。

```py frame="code" title="GaussianNB.py"
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.naive_bayes import GaussianNB
X, y = make_classification(
    n_samples=500, n_features=2, n_redundant=0, n_informative=2,
    n_clusters_per_class=1, random_state=42
)


# 执行代码
if __name__ == "__main__":
    # 模型训练
    model = GaussianNB()
    model.fit(X, y)

    # 绘制决策边界
    xx, yy = np.meshgrid(
        np.linspace(X[:,0].min()-1, X[:,0].max()+1, 200),
        np.linspace(X[:,1].min()-1, X[:,1].max()+1, 200)
    )
    Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1].reshape(xx.shape)

    plt.figure(figsize=(7,6))
    plt.contourf(xx, yy, Z, cmap='RdBu', alpha=0.6)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='RdBu', edgecolor='k')
    plt.title("Decision Boundary of Gaussian Naive Bayes", fontsize=14)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.colorbar(label="P(y=1|x)")
    plt.show()
```

## 2. 多项式贝叶斯

对于多项式贝叶斯分类器，假设分布如下：

$$
P(x_i | c) = \frac{(\sum_i x_i)!}{\prod_i x_i!} 
\prod_i \theta_{c,i}^{x_i} 
\quad \text{where } 
\theta_{c,i} = \frac{N_{c,i} + \alpha}{\sum_j (N_{c,j} + \alpha)}
$$

上述公式中已使用拉普拉斯平滑操作。

```py frame="code" title="MultinomialNB.py"
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
# 文本数据
texts = ["I love machine learning", 
        "Naive Bayes is simple",
        "I love learning",
        "Bayes theorem is powerful"
]
y = [1, 0, 1, 0]
# 转换为词频向量
vec = CountVectorizer()
X = vec.fit_transform(texts)

# 执行代码
if __name__ == "__main__":
    # 模型训练
    model = MultinomialNB(alpha=1.0)  # alpha=1 表示拉普拉斯修正
    model.fit(X, y)

    # 预测
    test = ["I love Bayes"]
    X_test = vec.transform(test)
    print("Predicted label:", model.predict(X_test))
    print("Posterior probabilities:", model.predict_proba(X_test))
```

## 3. 伯努利贝叶斯

对于伯努利贝叶斯分类器，假设分布如下：

$$
P(x_i | c) = \prod_i p_{c,i}^{x_i} (1 - p_{c,i})^{1 - x_i} 
\quad \text{where } 
p_{c,i} = \frac{N_{c,i} + \alpha}{N_y + 2\alpha}
$$

无论是伯努利贝叶斯还是多项式贝叶斯，其假设分布都需要用古典概型的方式进行拟合，有可能会产生 0 从而导致分类器失效，因此需要对它们使用拉普拉斯平滑操作。

```py frame="code" title="BernoulliNB.py"
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
texts = ["I love AI", "AI is fun", "I hate bugs", "bugs are annoying"]
y = [1, 1, 0, 0]
# 转换为 0/1 特征矩阵
vec = CountVectorizer(binary=True)
X = vec.fit_transform(texts)

# 执行代码
if __name__ == "__main__":
    # 模型训练
    model = BernoulliNB(alpha=1.0)
    model.fit(X, y)

    # 预测
    test = ["I love bugs"]
    X_test = vec.transform(test)
    print("Predicted label:", model.predict(X_test))
    print("Posterior probabilities:", model.predict_proba(X_test))
```

## 4. 内容拓展

尽管它们的假设看起来过于简化，但朴素贝叶斯分类器在许多实际情况下表现良好，著名的例子包括文档分类和垃圾邮件过滤。它们只需要少量训练数据就能估计必要的参数。

> 关于为什么朴素贝叶斯效果好以及在哪些类型的数据上效果好的理论原因，请参见下面的参考文献

[The optimality of Naive Bayes.](https://www.cs.unb.ca/~hzhang/publications/FLAIRS04ZhangH.pdf)

与更复杂的方法相比，朴素贝叶斯分类器的速度非常快。类条件特征分布的解耦意味着每个分布都可以独立地作为一维分布进行估计。这反过来有助于减轻由维数灾难引起的问题。

另一方面，虽然朴素贝叶斯被认为是一个不错的分类器，但它也是一个糟糕的估计器，因此 `predict_proba` 的概率输出不应过于重视。

---

# 深层问题探究

1. 什么是半朴素贝叶斯分类器？其与朴素贝叶斯分类器的区别是什么？（朴素贝叶斯分类器的局限是什么？）

    在现实生活中，属性条件独立性假设往往很难成立，于是人们尝试对属性条件独立性假设进行一定程度的放松，由此产生了一类称为 **半朴素贝叶斯分类器（Semi-Naive Bayes Classifiers）** 的学习方法。

    ![半朴素贝叶斯分类器图像](.\半朴素贝叶斯分类器1.png)

    **独依赖估计**（One-Dependent Estimator, 简称 ODE）是半朴素贝叶斯分类器最常用的一种策略。顾名思议，所谓 “独依赖” 就是假设每个属性在类别之外最多仅依赖于一个其他属性，即：

    $$
    P(c | x) \propto P(c) \prod_{i=1}^d P(x_i | c, pa(i))
    $$

    其中 $pa(i)$ 为属性 $x_i$ 所依赖的属性，称为 $x_i$ 的父属性。此时，对每个属性 $x_i$ 若其父属性 $pa(i)$ 已知，则可采用频率估计概率的办法来估计概率值 $P(x_i | c, pa(i))$ 。于是，问题的关键就转化为如何确定每个属性的父属性，不同的做法产生不同的独依赖分类器。

    - SPODE（Super-Parent ODE）方法假设所有属性都依赖于同一个属性，然后通过交叉验证等模型选择方法来确定超父属性
    - TAN（Tree Augmented naive Bayes）则是通过计算任意两个属性之间的条件互信息，构建最大带权生成树，从而将属性间依赖关系约简为树形结构，仅保留强相关属性之间的依赖性，条件互信息的公式为：

    $$
    I(x_i, x_j | y) = 
    \sum_{x_i, x_j; c \in \mathcal{Y}} 
    P(x_i, x_j | c) 
    \log \frac{P(x_i, x_j | c)}{P(x_i | c) P(x_j | c)}
    $$

    - AOED（Averaged One-Dependent Estimator）是一种集成学习机制的独依赖分类器，尝试将每个属性作为超父来构建 SPODE，然后将那些具有足够训练数据支撑的 SPODE 集成起来作为最终结果，即：

    $$
    P(c | x) \propto 
    \sum_{\substack{i=1 \\ |D_{x_i}| \ge m'}}^{d} 
    P(c, x_i) 
    \prod_{j=1}^{d} P(x_j | c, x_i)
    $$

    不难看出，与朴素贝叶斯分类器类似，AOED 无需模型选择，既能通过预计算节省预测时间，也能采取懒惰学习方式在预测时再进行计数，并且易于实现增量学习。

    > 更多半朴素贝叶斯分类器的内容可以看下面两个博客

    [机器学习（六）贝叶斯分类器](https://baidinghub.github.io/2020/04/03/机器学习（六）贝叶斯分类器/)

    [【机器学习基础】第二十四课：半朴素贝叶斯分类器](https://blog.csdn.net/qq_34222839/article/details/147490529)

2. 如何直观理解对条件概率建模表示判别模型，对联合概率建模表示生成模型？（究竟什么是判别模型？什么是生成模型？为什么朴素贝叶斯对后验概率建模却是生成模型？）

    若想解决上述问题，我们只需要弄清楚两种模型的目的分别是什么即可。

    判别模型的思路是：我不关心 $x$ 是怎么来的，我只关心不同类别之间的分界。

    - 因此给定一个 $x$ ，我们只需要判断它属于哪个 $y$ 即可，因此我们可以直接对条件概率 $P(y|x)$ 建模。判别模型要做的就是 **在某个空间中** ，用 **一个超平面** 将数据进行区分。

    生成模型的思路是：我先去理解每个类别的数据究竟是如何产生的（由此可以构建生成器），再根据贝叶斯公式去构建判别器（更准确地说是在做预测）。

    - 因此生成模型本质是在建模 $P(x|y)$ 。但根据公式 $P(x, y) = P(x|y)P(y)$ 我们可以知道，建模后验概率就是在建模联合概率。因此我们 **通常说建模联合概率表示生成模型，但本质是在建模后验概率** 。

---

# 参考文献列表

1. [朴素贝叶斯分类器(Naive Bayes Classifier)教程](https://blog.csdn.net/FFMXjy/article/details/145255053)

2. [Naive Bayes（朴素贝叶斯分类器）](https://blog.csdn.net/m0_52049033/article/details/143114512)

3. [【维基百科】朴素贝叶斯分类器](https://en.wikipedia.org/wiki/Naive_Bayes_classifier#Probabilistic_model)

4. [伯努利朴素贝叶斯详解：初学者的可视化指南与代码示例](https://blog.csdn.net/wjjc1017/article/details/141768420)

5. [[NLP复习笔记] 朴素贝叶斯分类器](https://www.cnblogs.com/MarisaMagic/p/17948124)

6. [【ScikitLearn】朴素贝叶斯](https://scikit-learn.cn/1.6/modules/naive_bayes.html)

7. [Zhroyn 的学习笔记之贝叶斯分类器](https://zhroyn.github.io/MyNotes/课程/机器学习/贝叶斯分类器.html)