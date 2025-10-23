---
title: 回归分析（Google ML）
published: 2025-10-23
description: Google ML 回归分析学习笔记
tags: [Machine Learning, Course, Note]
category: Google ML
draft: false 
---

# 线性回归

## 损失类型

**MAE**：平均绝对误差

**MSE**：均方误差

**RMSE**：均方根误差

## 选择损失

选择最佳损失函数时，请考虑您希望模型如何处理离群值。例如，**MSE** 会使模型更接近离群点，而 **MAE** 则不会。因为与 **L1** 损失相比，**L2** 损失对离群值的罚分要高得多。

:::important
**选择 MSE**：

- 如果您想严厉惩罚大误差。
- 如果您认为离群值很重要，并且表明模型应考虑的真实数据方差。

**注意**：MSE 的数学属性通常会使优化更顺畅。均方根误差 (RMSE) 通常用于将误差恢复为与标签相同的单位。

**选择 MAE**：

- 如果您的数据集中存在您不希望对模型产生过大影响的显著离群值。MAE 更稳健。
- 如果您希望损失函数能更直接地解释为平均误差幅度。

在实践中，指标选择还可能取决于具体的业务问题以及哪种类型的错误成本更高。
:::

## 梯度下降

[如何计算神经网络的参数](https://www.bilibili.com/video/BV1CVAUeuECE/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114052319679117&bvid=BV1CVAUeuECE&cid=28536998241&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 损失曲线

线性模型的损失函数始终会生成**凸面**。根据这一属性，当线性回归模型收敛时，我们知道该模型已找到可产生最低损失的权重和偏差。

线性模型一定有极值点

## 超参数

人为调控的参数称为超参数

**bath**：较大的 bath 有助于减少数据中存在离群值带来的负面影响。

# 逻辑回归

## S 型函数

**标准逻辑函数**即为 S 型函数（*sigmoid* 的意思是“S 形”）

**对数几率函数**是 S 型函数的反函数。

## 损失与正则化

:::important
**逻辑回归**模型的训练过程与**线性回归**模型相同，但有以下两个主要区别：

- 逻辑回归模型使用**对数损失函数**作为损失函数，而不是**平方损失函数**。
- 应用**正则化**对于防止出现**过拟合**至关重要。
:::

# 相关视频

## 回归分析系列

[怎样一步步才能学好回归分析](https://www.bilibili.com/video/BV1shriYXEEv/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113794554528405&bvid=BV1shriYXEEv&cid=27769966273&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[15分钟用人话讲多元线性回归](https://www.bilibili.com/video/BV1s8riYWEVK/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113794571308923&bvid=BV1s8riYWEVK&cid=27770028835&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[用人话讲清楚多元线性回归的流程](https://www.bilibili.com/video/BV1periYDE65/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113794588084047&bvid=BV1periYDE65&cid=27770029664&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[用人话教会你逻辑回归是什么](https://www.bilibili.com/video/BV18KF3eBEwD/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113913471435418&bvid=BV18KF3eBEwD&cid=28145156241&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[彻底搞懂广义线性回归！](https://www.bilibili.com/video/BV1MK7MzAEGN/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114604038425646&bvid=BV1MK7MzAEGN&cid=30255746027&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[搞清三种正则化回归](https://www.bilibili.com/video/BV1CJTdzaEMa/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114649773114756&bvid=BV1CJTdzaEMa&cid=30395729484&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[人话版Cox回归](https://www.bilibili.com/video/BV1XFM8zVECm/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114688394268381&bvid=BV1XFM8zVECm&cid=30517757868&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 回归分析项目

**线性回归**：[机器学习之线性回归算法Linear Regression](https://blog.csdn.net/qq_41750911/article/details/124883520)

**逻辑回归**：[Logistic回归（逻辑回归）及python代码实现](https://blog.csdn.net/weixin_50744311/article/details/131523136)

**分类算法**：[构建自己的图像分类数据集【两天搞定AI毕设】](https://www.bilibili.com/video/BV1Jd4y1T7rw/)