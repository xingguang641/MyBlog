---
title: 数据处理（Google ML）
published: 2025-10-23
description: Google ML 数据处理学习笔记
tags: [Machine Learning, Course, Note]
category: Google ML
draft: false 
---

# 数据处理

## 数据类别

**数值数据**用整数或浮点值来表示，它们是可累加的、可数的、有序的。

**分类数据**用整数来表示，它们通常是不可累加的。

:::important
数值数据的示例包括：

- 温度
- 重量
- 自然保护区的鹿数量

相比之下，美国邮政编码虽然是由 5 位数或 9 位数的数字构成，但其表达的含义与数值数据不同。例如：邮政编码 40004（肯塔基州尼尔森县）不是邮政编码 20002（华盛顿特区）的两倍。这些数字代表类别（具体而言是地理区域），被视为分类数据。
:::

## 特征向量

使用数据集中的 *实际* 值进行训练，而不是使用 *经过更改* 的值，会使模型的预测结果更好吗？答案是否定的。

您必须将原始数据集的原始值转变为特征向量中可训练的特征值。此过程称为**特征工程**，是机器学习的重要组成部分。最常见的特征工程技术包括：

- **归一化**：将数值映射至标准范围内。
- **分箱**（也称为**分桶**）：将数值划分成不同的区域（这个区域称为一个桶）。

本单元将介绍归一化和分箱。下一部分“处理分类数据”将介绍其他形式的**预处理**，例如将非数值数据（例如字符串）转换为浮点值。

## 特征工程

[特征工程【斯坦福21秋季：实用机器学习中文版】](https://www.bilibili.com/video/BV1t44y1x7Hw/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=976027811&bvid=BV1t44y1x7Hw&cid=423753460&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[【机器学习】特征工程详解](https://zhuanlan.zhihu.com/p/166356924)

[特征工程9大方法](https://blog.csdn.net/qq_55948984/article/details/136402828)

# 相关视频

## 数据可视化

[数据可视化的前世今生](https://www.bilibili.com/video/BV1dh4y127Pv/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=660383281&bvid=BV1dh4y127Pv&cid=1253221070&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[使用Deepseek打造可视化内容](https://www.bilibili.com/video/BV1doK7eJEfg/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113991753998159&bvid=BV1doK7eJEfg&cid=28359198482&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[python交互式地图数据可视化神器folium](https://www.bilibili.com/video/BV1t3411A7Z8/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=426551834&bvid=BV1t3411A7Z8&cid=720938952&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[数据可视化教程 无需框架代码 flourish在线制作五分钟搞定](https://www.bilibili.com/video/BV1YC4y147cE/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=795023367&bvid=BV1YC4y147cE&cid=191525813&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 数据预处理

[大白话讲明白标准化和归一化](https://www.bilibili.com/video/BV1DtJyz6EJv/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=115254222656103&bvid=BV1DtJyz6EJv&cid=32583585323&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[【毕导】这个定律，预言了你的人生进度条](https://www.bilibili.com/video/BV1VrVSz1Eme/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114478410699738&bvid=BV1VrVSz1Eme&cid=29894248891&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[【漫士】世界是对数的……吗？为什么？](https://www.bilibili.com/video/BV15kj4z4Eju/)

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114561508187738&bvid=BV15kj4z4Eju&cid=30123821538&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

[pytorch之—工程规范](https://blog.csdn.net/wsp_1138886114/article/details/87911264/)

[基于Kaggle的经典AI项目：数据理解与整体探索](https://blog.csdn.net/wsp_1138886114/article/details/81366353/)

[基于Kaggle的经典AI项目：数据清洗](https://blog.csdn.net/wsp_1138886114/article/details/81542011/)

[基于Kaggle的经典AI项目：特征转换与衍生](https://blog.csdn.net/wsp_1138886114/article/details/81583734/)

[基于Kaggle的经典AI项目：特征筛选](https://blog.csdn.net/wsp_1138886114/article/details/81911511/)

[基于Kaggle的经典AI项目：模型训练](https://blog.csdn.net/wsp_1138886114/article/details/81913016/)

[AI 大模型中的数据清洗与预处理技术研究](https://blog.csdn.net/deepever/article/details/148565284)