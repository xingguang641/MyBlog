---
title: 【机器学习笔记】数据处理（Google ML）
published: 2025-10-23
description: Google ML 数据处理学习笔记
tags: [Machine Learning, Course, Note]
category: ML Note
draft: false 
---

# 数据处理

## 数据类别

**数值数据（Numerical Data）**  
以整数或浮点数形式表示，具有可加性和可度量性，通常可进行大小比较与数学运算。  
这类数据是 **可度量且有序的** ，常用于反映数量、长度、温度等连续或离散的数值特征。

**分类数据（Categorical Data）**  
以离散的类别或标签形式表示，通常使用整数编码或独热编码（One-Hot Encoding）进行数值化处理。  
这类数据 **不可累加、无固定顺序** （除非为有序分类），用于表示性别、颜色、地区等非数值属性。

:::important
**数值数据（Numerical Data）** 的典型示例包括：

- 温度  
- 重量  
- 自然保护区中的鹿数量  

这些变量以数量形式表达，具备可度量性与可加性。

相比之下，**美国邮政编码（ZIP Code）** 虽然由 5 位或 9 位数字组成，但其含义与数值数据不同。
例如，邮政编码 **40004**（肯塔基州尼尔森县）并不表示是邮政编码 **20002**（华盛顿特区）的两倍。

这些数字仅用于标识地理区域，因此应被视为 **分类数据（Categorical Data）** ，而非数值数据。
:::

## 特征工程

使用数据集中的 *实际* 值进行训练，而不是使用 *经过更改* 的值，会使模型的预测结果更好吗？答案是否定的。

您必须将原始数据集的原始值转变为特征向量中可训练的特征值。此过程称为 **特征工程** ，是机器学习的重要组成部分。最常见的特征工程技术包括：

- **归一化**：将数值映射至标准范围内。
- **分箱**（也称为 **分桶** ）：将数值划分成不同的区域（这个区域称为一个桶）。

本单元将介绍归一化和分箱。下一部分“处理分类数据”将介绍其他形式的 **预处理** ，例如将非数值数据（例如字符串）转换为浮点值。

> 相关博客

[【机器学习】特征工程详解](https://zhuanlan.zhihu.com/p/166356924)

[特征工程9大方法](https://blog.csdn.net/qq_55948984/article/details/136402828)

> 相关视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=976027811&bvid=BV1t44y1x7Hw&cid=423753460&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 相关视频

## 数据可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=660383281&bvid=BV1dh4y127Pv&cid=1253221070&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113991753998159&bvid=BV1doK7eJEfg&cid=28359198482&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=426551834&bvid=BV1t3411A7Z8&cid=720938952&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=795023367&bvid=BV1YC4y147cE&cid=191525813&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 数据预处理

> 相关博客

[pytorch之—工程规范](https://blog.csdn.net/wsp_1138886114/article/details/87911264/)

[基于Kaggle的经典AI项目：数据理解与整体探索](https://blog.csdn.net/wsp_1138886114/article/details/81366353/)

[基于Kaggle的经典AI项目：数据清洗](https://blog.csdn.net/wsp_1138886114/article/details/81542011/)

[基于Kaggle的经典AI项目：特征转换与衍生](https://blog.csdn.net/wsp_1138886114/article/details/81583734/)

[基于Kaggle的经典AI项目：特征筛选](https://blog.csdn.net/wsp_1138886114/article/details/81911511/)

[基于Kaggle的经典AI项目：模型训练](https://blog.csdn.net/wsp_1138886114/article/details/81913016/)

[AI 大模型中的数据清洗与预处理技术研究](https://blog.csdn.net/deepever/article/details/148565284)

> 相关视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=115254222656103&bvid=BV1DtJyz6EJv&cid=32583585323&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114478410699738&bvid=BV1VrVSz1Eme&cid=29894248891&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114561508187738&bvid=BV15kj4z4Eju&cid=30123821538&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>