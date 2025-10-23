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

本单元着重介绍 **数值数据**、 表示整数或浮点值 其行为方式与数字类似的函数。也就是说，它们是可累加的、可数的、有序的， 依此类推。

下一部分将重点介绍**分类数据**，其中可能包含行为类似于类别的数字。第三单元重点介绍如何 准备数据，确保在训练和评估时获得高质量结果模型。

:::important
数值数据的示例包括：

- 温度
- 重量
- 自然保护区的鹿数量

相比之下，美国邮政编码虽然是 5 位数或 9 位数的数字，但其行为方式与数字不同，也不代表数学关系。邮政编码 40004（肯塔基州尼尔森县）不是邮政编码 20002（华盛顿特区）的两倍。这些数字代表类别（具体而言是地理区域），被视为分类数据。
:::

## 特征向量

使用数据集中的 *实际* 值进行训练，而不是使用 *经过更改* 的值，模型的预测结果会更好吗？令人惊讶的是，答案是否定的。

您必须确定将原始数据集值表示为特征向量中可训练值的最佳方法。此过程称为**特征工程**，是机器学习的重要组成部分。最常见的特征工程技术包括：

- **归一化**：将数值转换为标准范围。
- **分箱**（也称为**分桶**）：将数值转换为范围分桶。

本单元将介绍归一化和分箱。下一部分“处理分类数据”将介绍其他形式的**预处理**，例如将非数值数据（例如字符串）转换为浮点值。

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