---
title: 【机器学习基本模型】第二节：逻辑回归
published: 2025-10-23
description: 介绍机器学习常见的模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 逻辑回归基本原理

在模式识别问题中，我们通常关心的是 **分类任务** ，例如判断一个人是否患有某种疾病。这时就不能简单地使用线性回归模型来解决。为此我们在模型中引入了一个非线性激活函数 $g: \mathbb{R} \to (0,1)$ 来预测类别标签的后验概率 $P(y = 1 | x)$ ，其中 $y \in \{0, 1\}$ ，函数 $g$ 的作用是把线性函数的值域从实数区间挤压到 0 和 1 之间。

## 对数几率回归介绍

在 Logistic 回归中，激活函数的表达式为：

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

标签 $y = 1$ 的后验概率为:

$$
P(y = 1 | x) = \sigma(w^{\rm T} x) = \frac{1}{1 + e^{-w^{\rm T} x}}
$$

这里 $x = [x_1, \cdots, x_D, 1]^{\rm T}$ 和 $w = [w_1, \cdots, w_D, b]^{\rm T}$ 分别为 $D + 1$ 维的增广特征向量与增广权重向量，标签 $y = 0$ 的后验概率为：

$$
P(y=0 | x) = 1 - P(y=1 | x) 
= 1 - \sigma(w^{\rm T} x) 
= \frac{e^{- w^{\rm T} x}}{1 + e^{- w^{\rm T} x}}
$$

综上可得：

$$
w^{\rm T} x 
= \log \frac{P(y=1 | x)}{1 - P(y=1 | x)} 
= \log \frac{P(y=1 | x)}{P(y=0 | x)}
$$

上式左边为线性函数，右边为正反后验概率比值（几率）取对数，因此 Logistic 回归也称为 **对数几率回归** 。

![逻辑回归图像](src\content\posts\logistic-regression\逻辑回归分析1.jpg)

---

# 代码讲解

下面通过 Python 实现一个简单的逻辑回归模型。这次我们会用一些 **匿名函数** 来简化我们的代码（如果不懂匿名函数的也没关系，看一下就懂了）。

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

## 损失函数

与线性回归不同，逻辑回归采用的损失函数是 **交叉熵损失** （Cross-Entropy Loss）而不是均方误差，其中一个原因便是在逻辑回归中交叉熵损失函数的图像要比均方损失函数的图像要光滑很多（便于梯度下降），关于其他一些原因可以观看下面这个视频进一步了解。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114675626875309&bvid=BV12VMzzxExF&cid=30475028383&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

简单看一下代码中的损失函数。

```py showLineNumbers
loss_func = lambda X, y, w: -np.mean(
    y * np.log(sigmoid(X @ w)) + (1 - y) * np.log(1 - sigmoid(X @ w))
)
```

交叉熵损失函数的数学表达式如下：

$$
L(w) = -\frac{1}{N} \sum_{i=1}^{N} \Big[ y_i \log(\hat{y}_i) + (1 - y_i)\log(1 - \hat{y}_i) \Big]
$$

把 $$\hat{y}_i = \sigma(X_iw)$$ 带入上面的式子便可以直接得到上述代码中的公式了。

## 梯度下降

逻辑回归跟线性回归的另一个区别便是逻辑回归模型比线性回归模型多嵌套了一层激活函数。从数学上看，这只是多了一层函数复合关系，因此在通过链式法则求梯度时只需要多进行一步求导即可，本质上差别并不大。

```py showLineNumbers
gradient = lambda X, y, w: X.T @ (sigmoid(X @ w) - y) / len(y)
def grad_desc(cur_w, alpha, X, y):
    grad = gradient(X, y, cur_w)
    updated_w = cur_w - alpha * grad
    return updated_w
```

逻辑回归的梯度下降算法的难点依旧是梯度，我们来简单推导一下交叉熵损失函数的导数：

$$
\hat{y} = \sigma(Xw) = \frac{1}{1 + e^{-Xw}}
$$

$$
L(w) = -\frac{1}{N} \sum_{i=1}^{N} \Big[ y_i \log(\hat{y}_i) + (1 - y_i)\log(1 - \hat{y}_i) \Big]
$$

将 $$\hat{y}_i = \sigma(X_i w)$$ 代入，并对 $w$ 求导，得到：

$$
\nabla J(w) = \frac{\partial J(w)}{\partial w}
= \frac{1}{N} X^{\rm T} (\hat{y} - y)
$$

然后套用梯度下降算法的迭代公式就行了。

## 内容拓展

Logistic 回归不仅可以用于线性可分的数据，还能够通过一定方式处理 **非线性可分** 的分类问题。虽然 Logistic 回归本质上是一个线性分类模型，但我们可以通过 **特征扩展**（Feature Expansion） 的方式，使其具备拟合非线性关系的能力。

具体来说，可以在输入特征上进行多种形式的变换：

- **多项式特征** ：在模型中加入特征的平方项、立方项等高阶项，以捕捉更复杂的曲线关系
- **交互特征** ：将不同特征之间的乘积、差值或比值作为新的输入特征，从而刻画变量之间的相互影响

这些方法本质上是在原始特征空间上构造了一个新的、非线性的特征空间，从而能够更好地拟合复杂的数据分布。

需要注意的是，随着特征数量和复杂度的增加，模型容易出现 **过拟合** （Overfitting）现象。因此在引入非线性特征时，通常需要配合正则化或其他模型调优技巧一同使用，以保持模型的 **泛化能力** 。

---

# 深层问题思考

1. 为什么逻辑回归在线性回归的基础上套一层激活函数就可以进行分类呢？

    逻辑回归假设：
    
    $$
    P(y=1 | x) = \sigma(w^{\rm T} x + b)
    $$

    $$
    P(y=0 | x) = 1 - \sigma(w^{\rm T} x + b)
    $$

    > 我们认为样本属于正类的 **对数几率** （log odds）与输入的线性组合成正比。

    用公式表示就是：

    $$
    \log \frac{P(y=1 | x)}{P(y=0 | x)} = w^{\rm T} x + b
    $$

    这叫作 **logit 变换** ，而 Sigmoid 函数正好是这个对数几率函数的 **逆变换** 。

---

# 参考文献

1. [Logistic回归（逻辑回归）](https://blog.csdn.net/weixin_50744311/article/details/131523136)

2. [【ScikitLearn】LogisticRegression](https://scikit-learn.cn/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)