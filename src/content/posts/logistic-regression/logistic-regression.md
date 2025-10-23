---
title: 【机器学习基本模型】第二节：逻辑回归
published: 2025-10-23
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

# 逻辑回归基本原理

在模式识别问题中，我们所关心的是分类，比如是否会患有某种疾病，这时就不能用简单的线性回归来完成这个问题了。为了解决此类问题，我们引入了非线性激活函数 $$g: \mathbb{R} \to (0,1)$$ 来预测类别标签的后验概率 $$p(y = 1 \mid x)$$ ，其中 $$y \in \{0, 1\}$$ ，函数 $g$ 的作用是把线性函数的值域从实数区间挤压到0和1之间

在Logistic回归中，激活函数的表达式为：

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

标签 $y = 1$ 的后验概率为:

$$
p(y = 1 \mid x) = \sigma(w^{\rm T} x) = \frac{1}{1 + e^{-w^{\rm T} x}}
$$

这里 $$\mathbf{x} = [x_1, \cdots, x_D, 1]^{\rm T}$$ 和 $$\mathbf{w} = [w_1, \cdots, w_D, b]^{\rm T}$$ 分别为 $D + 1$ 维的增广特征向量与增广权重向量，标签 $y = 0$ 的后验概率为：

$$
p(y=0 \mid \mathbf{x}) = 1 - p(y=1 \mid \mathbf{x}) 
= 1 - \sigma(\mathbf{w}^{\rm T} \mathbf{x}) 
= \frac{e^{- \mathbf{w}^{\rm T} \mathbf{x}}}{1 + e^{- \mathbf{w}^{\rm T} \mathbf{x}}}
$$

综上可得：

$$
\mathbf{w}^{\rm T} \mathbf{x} 
= \log \frac{p(y=1 \mid \mathbf{x})}{1 - p(y=1 \mid \mathbf{x})} 
= \log \frac{p(y=1 \mid \mathbf{x})}{p(y=0 \mid \mathbf{x})}
$$

上式左边为线性函数，右边为正反后验概率比值（几率）取对数，因此 Logistic 回归也称为**对数几率回归**

![逻辑回归图像](src\content\posts\logistic-regression\逻辑回归分析1.jpg)

## 代码讲解

这次的代码我们将使用大量的匿名函数来简化我们的代码（如果不懂匿名函数的也没关系，看一下就懂了）

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

与线性回归不同，逻辑回归的损失函数用的是交叉熵损失而不是均方损失，其中一个原因便是在逻辑回归中交叉熵损失函数的图像要比均方损失函数的图像要光滑很多，关于其他的一些原因可以看下面这个视频了解一下

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114675626875309&bvid=BV12VMzzxExF&cid=30475028383&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

简单看一下代码中的损失函数

```py showLineNumbers
loss_func = lambda X, y, w: -np.mean(
    y * np.log(sigmoid(X @ w)) + (1 - y) * np.log(1 - sigmoid(X @ w))
)
```

交叉熵损失函数的数学表达式如下：

$$
L = -\frac{1}{N} \sum_{i=1}^{N} [y_i \log(\hat{y}_i) + (1 - y_i)\log(1 - \hat{y}_i)]
$$

把 $$\hat{y} = \sigma(Xw)$$ 带入上面的式子便可以直接得到上面的代码了

## 梯度下降

逻辑回归跟线性回归的另一个区别便是逻辑回归模型比线性回归模型多套了一层激活函数，也就是多复合了一层函数，但是区别不大，无非就是链式法则多一步的问题

```py showLineNumbers
gradient = lambda X, y, w: X.T @ (sigmoid(X @ w) - y) / len(y)
def grad_desc(cur_w, alpha, X, y):
    grad = gradient(X, y, cur_w)
    updated_w = cur_w - alpha * grad
    return updated_w
```

逻辑回归的梯度下降算法的难点依旧是梯度，我们来简单推导一下交叉熵损失函数的导数

$$
\hat{y} = \sigma(Xw) = \frac{1}{1 + e^{-Xw}}
$$

$$
J(w) = -\frac{1}{N} \sum_{i=1}^{N} \Big[ y_i \log(\hat{y}_i) + (1 - y_i)\log(1 - \hat{y}_i) \Big]
$$

将 $$\hat{y}_i = \sigma(X_i w)$$ 代入，并对 $w$ 求导，得到：

$$
\nabla_w J(w) = \frac{\partial J(w)}{\partial w}
= \frac{1}{N} X^{\rm T} (\hat{y} - y)
$$

然后套用梯度下降算法的迭代公式就行了

## 内容拓展

Logistic 回归可以用于分类非线性可分的数据。尽管 Logistic 回归本身是一个线性分类器，但可以通过引入多项式特征、交互特征、组合特征等方法来扩展其能力，从而处理非线性的分类问题。

具体来说，可以通过特征工程的方式将原始特征进行变换，以引入非线性关系。例如：可以通过添加多项式特征，将原始特征的高阶项加入到模型中，以及原始特征的平方项、立方项等。还可以引入交互特征，将不同特征之间的乘积或分割点（例如，做差或做除）作为新的特征。

通过引入这些非线性特征，Logistic 回归可以更好地捕捉到数据中的非线性关系，从而能够更好地分类非线性可分的数据。需要注意的是，在引入非线性特征时，可能需要进行正则化或其他模型调优技巧，以避免过拟合问题。

# 参考文献

1. [Logistic回归（逻辑回归）](https://blog.csdn.net/weixin_50744311/article/details/131523136)