---
title: 【机器学习笔记】回归分析（Google ML）
published: 2025-10-23
description: Google ML 回归分析学习笔记
tags: [Machine Learning, Course, Note]
category: ML Note
draft: false 
---

# 线性回归

## 损失类型

| MAE：平均绝对误差 | MSE：均方误差 | RMSE：均方根误差 |
|:-----------------:|:-------------:|:----------------:|

## 选择损失

在选择损失函数时，应重点考虑模型对离群值的处理方式。例如，**MSE** 会促使模型更加贴合离群点，而 **MAE** 对离群值的影响相对较小。这是因为：与 **L1** 损失相比，**L2** 损失会对较大的误差施加更高的惩罚。

:::important
**选择 MSE**：

- 当您希望对较大的预测误差施加更强的惩罚时，**MSE** 是更合适的选择。  
- 当离群值在任务中具有实际意义，并能反映数据的真实分布特征时，采用 **MSE** 可能更为合理。  

**注意**：由于 **MSE** 的二次形式具备良好的数学性质，优化过程通常更加平滑且易于收敛。此外，均方根误差（**RMSE**）常用于将误差恢复为与目标变量相同的量纲，从而便于结果解释和比较。

**选择 MAE**：

- 当数据集中存在不希望对模型造成过大影响的离群值时，**MAE** 通常更稳健。  
- 当您希望损失函数能够更直观地反映模型预测的平均偏差时，**MAE** 是更具可解释性的选择。    

在实际应用中，损失函数或评估指标的选择应结合具体的业务目标、数据特性及模型的鲁棒性要求进行综合考虑。
:::

## 梯度下降

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114052319679117&bvid=BV1CVAUeuECE&cid=28536998241&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 损失曲线

线性模型的损失函数始终呈现为 **凸函数** 。基于这一特性，当线性回归模型完成收敛时，我们可以确定模型已找到能够最小化损失的最优权重与偏置。  

也就是说，线性模型的损失函数 **仅存在一个全局最小值** ，而不会出现局部极小点。

## 超参数

**超参数** 是由人为设定、在模型训练过程中不会通过反向传播自动更新的参数。它们通常决定了模型的结构、学习速度以及正则化强度，对模型性能有重要影响。

### 学习率（Learning Rate）
控制参数更新的步长。  
学习率过大可能导致训练震荡甚至发散，过小则会导致收敛速度过慢。  
常见做法包括使用动态学习率衰减或自适应优化算法（如 Adam、RMSProp）。

### 批大小（Batch Size）
每次用于更新模型参数的样本数量。  
较大的 **batch** 有助于平滑梯度估计，降低离群值的影响，使训练过程更稳定；  
但过大的 **batch** 可能降低模型的泛化能力，并增加显存开销。

### 迭代轮次（Epochs）
指模型遍历整个训练集的次数。  
迭代次数过少可能导致欠拟合，而过多则容易造成过拟合。  
通常结合验证集性能来判断是否提前停止训练（Early Stopping）。

### 正则化系数（Regularization Strength）
用于约束模型复杂度的参数，如 **L1/L2 正则化** 中的惩罚项权重。  
较大的正则化系数可以减少过拟合，但可能导致欠拟合。

### 隐藏层与神经元数量（Hidden Layers & Units）
决定神经网络的结构复杂度。  
更多的层数与神经元通常能增强模型的表达能力，但也会增加训练难度和过拟合风险。

### 激活函数（Activation Function）
决定神经网络中非线性映射的方式。  
常见选择包括 **ReLU**、**Leaky ReLU**、**Sigmoid**、**Tanh** 等。  
不同激活函数会影响梯度传播与收敛性能。

### Dropout 比例（Dropout Rate）
在训练过程中随机丢弃部分神经元以防止过拟合。  
常见取值范围为 0.2～0.5。

### 优化器（Optimizer）
用于更新模型参数的算法，如 **SGD**、**Adam**、**RMSProp** 等。  
不同优化器在收敛速度与稳定性方面存在差异。

这些超参数往往需要通过 **经验调节** 或 **超参数搜索** （如 Grid Search、Random Search、Bayesian Optimization）来确定，以获得最佳模型性能。

---

# 逻辑回归

## S 型函数

**标准逻辑函数（Standard Logistic Function）** 通常被称为 **S 型函数**，其名称来源于其曲线呈现的 “S” 形。  
该函数定义为：

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

它将输入值映射到 (0, 1) 区间，常用于二分类模型（如逻辑回归）中的概率表示。

**对数几率函数（Logit Function）** 是 S 型函数的 **反函数** ，定义为：

$$
\text{logit}(p) = \ln\left(\frac{p}{1 - p}\right)
$$

也可以化简为：

$$
\text{logit}(\sigma(x)) = x, \quad \sigma(\text{logit}(p)) = p
$$

也就是说，**Sigmoid 函数**与其反函数 **Logit 函数** 互为逆映射：前者将实数映射到概率空间，后者将概率值映射回实数空间。

## 损失与正则化

:::important
**逻辑回归（Logistic Regression）** 的训练过程在形式上与 **线性回归（Linear Regression）** 相似，但存在以下两个关键区别：

- 逻辑回归模型采用 **对数损失函数（Log Loss）** 作为优化目标，而线性回归使用的是 **平方损失函数（Squared Loss）**。对数损失函数能够更好地度量预测概率与真实分类之间的差异，并保证输出结果位于 (0, 1) 区间内。

- 在逻辑回归中，应用 **正则化（Regularization）** 对防止模型发生 **过拟合（Overfitting）** 至关重要。常见的正则化形式包括 **L1（Lasso）** 和 **L2（Ridge）**，它们分别有助于特征选择与模型稳定性。

因此，逻辑回归在本质上是通过线性模型学习一个概率分布函数，并结合对数损失与正则化项实现稳健的分类效果。
:::

---

# 相关视频

## 回归分析系列

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113794554528405&bvid=BV1shriYXEEv&cid=27769966273&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113794571308923&bvid=BV1s8riYWEVK&cid=27770028835&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113794588084047&bvid=BV1periYDE65&cid=27770029664&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113913471435418&bvid=BV18KF3eBEwD&cid=28145156241&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114604038425646&bvid=BV1MK7MzAEGN&cid=30255746027&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114649773114756&bvid=BV1CJTdzaEMa&cid=30395729484&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114688394268381&bvid=BV1XFM8zVECm&cid=30517757868&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 回归分析项目

**线性回归**：[机器学习之线性回归算法Linear Regression](https://blog.csdn.net/qq_41750911/article/details/124883520)

**逻辑回归**：[Logistic回归（逻辑回归）及python代码实现](https://blog.csdn.net/weixin_50744311/article/details/131523136)

**分类算法**：[构建自己的图像分类数据集【两天搞定AI毕设】](https://www.bilibili.com/video/BV1Jd4y1T7rw/)