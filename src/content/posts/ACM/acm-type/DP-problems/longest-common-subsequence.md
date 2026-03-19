---
title: 【ACM 算法题单】最长公共子序列问题
published: 2026-02-04
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 经典动态规划思想

最长公共子序列（LCS）与最长公共子串（LCSubstr）是动态规划中极具代表性的两个经典问题。它们本身并不复杂，但所体现的建模方式却贯穿了大量序列类动态规划题目。许多看似形式各异的题目，本质上都可以追溯到这两类问题的思想变形，只是在状态定义或转移条件上作了不同程度的包装。

从建模角度来看，**子序列类问题的核心特征在于 “不要求连续”** 。因此，在定义状态时，$dp[i][j]$ 往往表示 “考虑到前 $i$ 个元素、前 $j$ 个元素时的最优解” ，而不需要关心当前元素是否被选中为结尾。这种定义天然允许 “跳过” 元素，其转移过程也通常围绕 “选或不选当前元素” 展开。

与之相对，**子串类问题则对连续性有严格要求** 。这使得状态定义必须显式刻画 “以某个位置结尾” 的信息，例如 “以第 $i$ 个字符结尾的最长公共后缀长度” 。一旦连续性被打破，状态便需要被重置，因此这类问题的转移通常更加局部，也更依赖当前位置之间的直接关系。

尽管两者在形式上差异明显，但它们的转移逻辑却高度统一：无非是在当前元素（或字符）相等时进行延续，不相等时选择继承已有结果或重新开始。正是这种 “在约束条件下进行选择” 的结构，使得它们成为理解动态规划思想的理想切入点。因此，掌握最长公共子序列与最长公共子串，并不仅仅是记住两道模板题，而是要透彻理解 **连续性约束如何影响状态设计** 、以及 “选与不选” 如何自然地体现在转移方程中。这种理解一旦建立，面对复杂的序列动态规划问题时，往往能够迅速抓住其本质结构。

## 最长公共子序列

[题目链接](https://leetcode.cn/problems/longest-common-subsequence/)



## 题目要点解析

可以从前往后匹配也可以从后往前匹配

## 不同的子序列

[题目链接](https://leetcode.cn/problems/distinct-subsequences/description/)



## 题目要点解析



## 编辑距离问题

[题目链接](https://leetcode.cn/problems/edit-distance/description/)



## 题目要点解析



## 交错字符串问题

[题目链接](https://leetcode.cn/problems/interleaving-string/description/)



## 题目要点解析



## 最长公共序列串

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class068/Code05_MinimumDeleteBecomeSubstring.java)



## 题目要点解析



## 正则表达式匹配

[题目链接](https://leetcode.cn/problems/regular-expression-matching)



## 题目要点解析

最长公共子序列+完全背包思想

---

# 参考文献列表

1. [迅速理解 LCS 问题](https://zhuanlan.zhihu.com/p/1924191282152054906)

2. [最长公共子序列问题](https://www.luogu.com/article/ml584xxs)

3. [最长公共子串问题](https://www.cnblogs.com/larry1024/p/18007566)