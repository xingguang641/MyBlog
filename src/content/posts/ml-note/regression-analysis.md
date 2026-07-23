---
title: 【机器学习笔记】回归分析 (Google ML)
published: 2025-10-23
description: 基于 Google ML 课程的回归分析学习笔记
tags: [Machine Learning, Google ML, Regression, Note]
category: ML Note
draft: true 
---

# 线性回归

## 1. 损失度量指标

在回归任务中，我们通常使用以下几种指标来衡量模型的预测误差：

| 指标 | 全称 | 特点 |
| :--- | :--- | :--- |
| **MAE** | 平均绝对误差（Mean Absolute Error） | 对离群值不敏感，反映预测值的平均偏移量。 |
| **MSE** | 均方误差（Mean Squared Error） | 对离群值敏感（误差被平方放大），便于梯度计算。 |
| **RMSE** | 均方根误差（Root Mean Squared Error） | 量纲与原目标变量一致，便于直观解释。 |

## 2. 选择损失函数

损失函数的选择直接决定了模型如何处理 **离群值（Outliers）**。

*   **L2 损失 (MSE)**：由于误差被平方，大的误差会产生巨大的损失值，因此模型会更关注离群点。
*   **L1 损失 (MAE)**：误差呈线性增长，模型对离群点的容忍度更高，拟合结果更具鲁棒性。

:::important
**💡 决策指南**

*   **选择 MSE 的场景**：
    *   **主要考量**：你需要对大的预测误差施加严厉惩罚。
    *   **数据特征**：离群值代表了重要的数据分布信息（而非噪声），模型必须尽可能拟合它们。
    *   **数学优势**：MSE 是处处可导的凸函数，优化过程通常比 MAE 更平滑、收敛更稳健。

*   **选择 MAE 的场景**：
    *   **主要考量**：你希望模型具有鲁棒性，不受少量极端值的干扰。
    *   **数据特征**：数据集中包含噪声或异常值，且你不希望这些异常点主导模型的训练方向。
:::

## 3. 梯度下降

_可视化演示：梯度下降如何寻找最优解_

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114052319679117&bvid=BV1CVAUeuECE&cid=28536998241&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 4. 模型收敛问题

线性回归模型的损失函数（通常是 MSE）是一个 **凸函数（Convex Function）**。这意味着：

1.  损失曲线形状如碗状，函数图像 **仅存在一个全局最小值** ，不存在局部极小值陷阱。
2.  只要学习率设置合理，梯度下降法理论上一定能收敛到全局最优解（权重与偏置）。

## 5. 超参数

超参数是训练前人为设定的 “旋钮” ，它们不通过数据训练得到，但决定了模型的结构和训练过程。

### 训练动态类
*   **学习率（Learning Rate）**：梯度下降的步长。
    *   *过大*：可能导致震荡或发散。
    *   *过小*：收敛速度极慢。
*   **批大小（Batch Size）**：单次参数更新所使用的样本数量。
    *   *大 Batch*：梯度估计更准，训练更稳，但显存要求高。
    *   *小 Batch*：引入随机性，有助于跳出局部最优（在非凸优化中），但训练波动大。
*   **迭代轮次（Epochs）**：模型遍历完整训练集的次数。
*   **优化器（Optimizer）**：参数更新的策略算法（如 SGD, Adam, RMSProp）。

### 模型结构与正则化类
*   **正则化系数（Regularization Strength）**：控制正则项（L1/L2）的权重，用于平衡偏差与方差。
*   **隐藏层与神经元（Hidden Layers & Units）**：(针对神经网络) 决定模型的容量和非线性表达能力。
*   **激活函数 (Activation Function)**：（针对神经网络）引入非线性因素（如 ReLU, Sigmoid）。
*   **Dropout 率**：随机失活神经元的比例，用于防止过拟合。

---

# 逻辑回归

## 1. 对数几率回归

逻辑回归的核心是将线性输出映射到 $(0, 1)$ 区间，以表示概率。

**S 型函数（Sigmoid Function）**

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

它将任意实数 $z$ 压缩到 $(0, 1)$ 之间。

**对数几率（Logit Function）**

它是 Sigmoid 的反函数，定义为概率 $p$ 的对数几率：

$$
\text{logit}(p) = \ln\left(\frac{p}{1 - p}\right)
$$

两者互为逆运算：$\text{logit}(\sigma(x)) = x$。这解释了逻辑回归也被称为 “对数几率回归” 的原因。

## 2. 损失与正则化

:::tip
**逻辑回归 vs 线性回归**

虽然逻辑回归在形式上看似只是线性回归加了一个 Sigmoid 壳，但它们的训练核心有两点本质不同：

1.  **损失函数**：
    *   **线性回归** 使用 **平方损失（Squared Loss）**。
    *   **逻辑回归** 使用 **对数损失（Log Loss / Cross Entropy）**。
    *   *原因*：如果在逻辑回归中使用平方损失，损失函数将变为非凸函数，难以优化；而对数损失不仅是凸函数，还基于最大似然估计推导而来，物理意义明确。

2.  **正则化的必要性**：
    *   逻辑回归极易在处理高维特征或线性可分数据时发生 **过拟合**（权重趋向无穷大以使概率逼近 1 或 0）。
    *   因此引入 **L2（Ridge）** 或 **L1（Lasso）** 正则化在逻辑回归中几乎是标准的做法。
:::

---

# 📚 学习资源汇总

## 回归分析系列

> 以下视频涵盖了从线性回归基础到进阶实战的完整流程。

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">
  <!-- 建议：如果不希望页面太长，可以使用这种 Grid 布局，或者只保留 1-2 个核心视频，其他的放链接 -->
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=113794554528405&bvid=BV1shriYXEEv&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=113794571308923&bvid=BV1s8riYWEVK&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=113794588084047&bvid=BV1periYDE65&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=113913471435418&bvid=BV18KF3eBEwD&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114584929177246&bvid=BV1hsjqzUETa&&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114604038425646&bvid=BV1MK7MzAEGN&&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114649773114756&bvid=BV1CJTdzaEMa&&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114688394268381&bvid=BV1XFM8zVECm&&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

## 实战项目与代码

*   **线性回归实战**：[CSDN - 机器学习之线性回归算法 (Linear Regression)](https://blog.csdn.net/qq_41750911/article/details/124883520)
*   **逻辑回归实战**：[CSDN - Logistic回归及Python代码实现](https://blog.csdn.net/weixin_50744311/article/details/131523136)
*   **综合实战**：[Bilibili - 两天搞定AI毕设：构建自己的图像分类数据集](https://www.bilibili.com/video/BV1Jd4y1T7rw/)