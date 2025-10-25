---
title: 【机器学习基本模型】第五节：支持向量机
published: 2025-10-25
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

> 写在前面：我们的教程终于来到了机器学习的第一个大难点 ———— 支持向量机。在深度学习盛行的今天，支持向量机是为数不多还能继续使用的传统机器学习算法之一，就让我们来看看大名鼎鼎的支持向量机到底是什么吧！

# 支持向量机基本原理

我们首先来思考这么一个问题，如上图所示，如果要求你画一条直线，使其能够将图中的两类点分开，并且在加入新的点后也尽可能实现这个目的（具有预测能力），你会如何画这个条直线呢？直觉上来讲，这条直线靠近任何一类点都不太可行。因此我们认为，这条直线到任何一个点都足够远时，直线的分类效果最好。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机2.jpg)

为了实现我们上述的初步猜想，我们要先引入一个概念： **间隔** （Margin）。间隔的作用是将两类数据所处的空间分隔开来，并且间隔越大，两类数据的差异也就越大。因此，要想区分两类数据，我们就得找到两类数据的最大间隔，然后我们再以间隔的正中间作为决策边界，就可以实现我们的猜想。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机3.jpg)

我们将已经找到的超平面上下移动 C 个单位，使其恰好经过某些数据点，我们称这两条直线为间隔上下边界。由于间隔上下边界必然会经过几个数据点，而这几个数据点也是起到了限制间隔上下边界的作用，因此我们称这几个点为 **支持向量** （Support Vector）。这便是 **支持向量机** （Support Vector Machine，简称 SVM）名称的由来。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机4.jpg)

> 上述图像截取自该视频内容（包括下面部分图像）

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=936042727&bvid=BV16T4y1y7qj&cid=494397114&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 归一化

对于直线方程来说，如果我们对其两边同时除以一个数，我们就可以得到一个新的方程。因此空间上的 **一条直线** 拥有 **无数** 个直线方程，这对我们的计算会产生影响。因此我们规定：决策上下边界的右值必须为 $\pm 1$ 。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机5.jpg)

这样我们就得到了三个平面：正超平面（Positive Hyperplane）、负超平面（Negative Hyperplane）和决策超平面（Decision Hyperplane）。

## 软间隔

我们再进一步思考这样一个问题：如果两类数据的间隔中出现了一个异常点，那么我们计算所得的的间隔就会缩小，但我们是否要为了这个异常点而牺牲我们的间隔呢？

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机6.jpg)

答案是否定的。但我们要如何判断什么样的点是异常点呢？或者说，我们可以让算法自己判断是否要忽略某个数据点吗？对此，我们引入了 **损失因子** （Penalty Factor）这个概念。你可以将原本的间隔视为经营的 **收入** ，而将损失看作经营的 **成本** ，那么我们最初的问题则可以转化为最大化 **利润** 。此时的间隔我们称之为 **软间隔** （Soft Margin）。

# 参考文献

1. [支持向量机（SVM）详解](https://blog.csdn.net/fyc1314/article/details/153789016)

2. [【ScikitLearn】支持向量机](https://scikit-learn.cn/stable/modules/svm.html)

3. [什么是支持向量机](https://blog.csdn.net/v20000727/article/details/135137095)

4. [支持向量机（SVM）——原理篇](https://www.zhihu.com/tardis/zm/art/31886934)

5. [【维基百科】支持向量机](https://zh.wikipedia.org/wiki/支持向量机)

6. [看了这篇文章你还不懂SVM你就来打我](https://zhuanlan.zhihu.com/p/49331510)

7. [支持向量机的工作原理](https://ww2.mathworks.cn/discovery/support-vector-machine.html)

8. [【图解数学】支持向量机](https://note.wcoder.com/MachineLearning/图解数学/files/支持向量机.pdf)