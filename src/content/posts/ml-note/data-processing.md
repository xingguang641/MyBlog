---
title: 【机器学习笔记】数据处理 (Google ML)
published: 2025-10-23
description: 基于 Google ML 课程的数据处理笔记
tags: [Machine Learning, Google ML, Data Processing, Feature Engineering, Note]
category: ML Note
draft: false 
---

# 数据类型辨析

在机器学习中，正确识别数据类型是选择处理方法的前提。

### 数值数据（Numerical Data）
*   **定义**：表示数量、大小或度量的连续或离散数值。
*   **特性**：具有 **可度量性**（Measurable）和 **有序性**（Ordered）。
*   **运算**：支持数学运算（如加减乘除），其数值大小具有实际的物理意义。
*   **示例**：温度、体重、商品价格、鹿群数量。

### 分类数据（Categorical Data）
*   **定义**：表示某种特征的离散类别或标签。
*   **特性**：通常 **无序**（Nominal）且 **不可累加** 。
*   **处理**：机器无法直接理解文本标签，通常需要转化为数值形式，常用方法包括：
    *   **整数编码（Label Encoding）**：用于有序类别（如：低/中/高 -> 0/1/2）。
    *   **独热编码（One-Hot Encoding）**：用于无序类别（如：红/绿/蓝）。
*   **示例**：性别、颜色、省份、犬种。

:::warning
**⚠️ 易错点：数字不一定都是数值数据**

**美国邮政编码（ZIP Code）** 虽然由数字组成（如 `20002`, `40004`），但它们属于 **分类数据** 。

*   **理由**：
    1.  **无数学意义**：邮编 `40004` 并不是邮编 `20002` 的两倍。
    2.  **仅作标识**：数字在这里仅代表地理区域的 “ID” ，而非数量的大小。
    
**处理建议**：在特征工程中，应将邮政编码视为离散的类别特征进行独热编码或其他嵌入处理，而不是直接作为连续数值输入模型。
:::

---

# 特征工程（Feature Engineering）

**核心问题**：直接使用原始数据（Raw Data）进行训练效果最好吗？**答案**：通常不是。

**特征工程** 是将原始数据转换为更能代表潜在问题预测模型的特征的过程。它是机器学习成功的关键要素。

我们必须将原始数据转换为 **特征向量（Feature Vector）**。常见的预处理技术包括：

*   **归一化（Normalization）**：
    *   将数值缩放到统一的范围（如 [0, 1] 或 [-1, 1]）。
    *   **目的**：防止某些大数值特征主导梯度下降的方向，加速收敛。
*   **分箱（Binning/Bucketing）**：
    *   将连续数值划分为若干个离散的区间（桶）。
    *   **目的**：引入非线性，降低离群值的影响。例如，将 “年龄” 划分为 “青年/中年/老年” 。

> **延伸阅读**
> *   [知乎：特征工程详解](https://zhuanlan.zhihu.com/p/166356924)
> *   [CSDN：特征工程 9 大方法](https://blog.csdn.net/qq_55948984/article/details/136402828)

---

# 📚 学习资源汇总

## 数据可视化（Data Visualization）

> 数据可视化是理解数据分布、发现异常值的首要步骤。

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=660383281&bvid=BV1dh4y127Pv&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=113991753998159&bvid=BV1doK7eJEfg&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=426551834&bvid=BV1t3411A7Z8&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=795023367&bvid=BV1YC4y147cE&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

## 数据预处理实战（Preprocessing）

> 涵盖特征工程、数据清洗及 PyTorch 工程规范。

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=976027811&bvid=BV1t44y1x7Hw&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=115254222656103&bvid=BV1DtJyz6EJv&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114478410699738&bvid=BV1VrVSz1Eme&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114561508187738&bvid=BV15kj4z4Eju&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

### Kaggle 经典项目实战系列
本系列博客完整记录了从数据理解到模型训练的全流程：

1.  **数据探索**：[数据理解与整体探索](https://blog.csdn.net/wsp_1138886114/article/details/81366353/)
2.  **数据清洗**：[数据清洗实战](https://blog.csdn.net/wsp_1138886114/article/details/81542011/)
3.  **特征变换**：[特征转换与衍生](https://blog.csdn.net/wsp_1138886114/article/details/81583734/)
4.  **特征筛选**：[特征筛选策略](https://blog.csdn.net/wsp_1138886114/article/details/81911511/)
5.  **模型训练**：[模型训练与调优](https://blog.csdn.net/wsp_1138886114/article/details/81913016/)
6.  **工程规范**：[PyTorch 工程规范指南](https://blog.csdn.net/wsp_1138886114/article/details/87911264/)

> **进阶阅读**：[AI 大模型中的数据清洗与预处理技术研究](https://blog.csdn.net/deepever/article/details/148565284)