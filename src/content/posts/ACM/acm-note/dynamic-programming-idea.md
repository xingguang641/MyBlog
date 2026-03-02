---
title: 【ACM 算法随笔】动态规划分类
published: 2026-02-06
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 递归动态规划问题

从方法论角度看，**绝大多数动态规划问题都可以通过递归形式加以刻画** 。递归的核心在于刻画问题的 **最优子结构**：即一个规模为 $n$ 的问题，其最优解可以由若干规模更小的子问题的最优解构成。因此，在构造动态规划模型之前，首先以 **递归方式** 明确状态定义与状态之间的依赖关系，往往能够更加清晰地揭示问题的结构本质。

朴素递归虽然能够完整描述问题的求解过程，但通常会产生大量 **重复子问题** 。这是因为在递归树中，不同路径可能访问到相同的状态。当状态空间有限且每个状态的结果具有 **确定性** 时，可以通过缓存机制避免重复计算，即引入 **记忆化搜索** 。此时，时间复杂度通常由指数级降低为多项式级。需要指出的是，记忆化搜索 **本质上也属于动态规划** ，其形式为自顶向下的实现方式。

在进一步分析状态依赖关系后，如果能够为所有状态建立一个满足依赖约束的遍历顺序，则递归过程可以转化为 **自底向上的迭代形式** 。递归调用所隐含的依赖结构被显式地转化为数组之间的 **状态转移关系** ，计算过程则按照拓扑序逐步推进。从抽象角度看，每一个状态可视为图中的一个节点，状态转移关系构成一张有向无环图。递归对应于在该图上进行深度优先遍历，而动态规划则对应于按照拓扑序进行系统性计算。因此二者 **在理论本质上是一致的，仅在实现形式上存在差异** 。

综上所述，**动态规划并非完全独立于递归之外的一种技巧** ，而是对递归求解过程的结构化与系统化优化。合理的建模路径通常是：首先通过递归形式明确状态与转移关系；其次通过记忆化消除重复子问题；最后根据状态依赖关系改写为自底向上的动态规划实现。**这一过程构成了一条从问题抽象到算法实现的完整方法论路径** 。这一方法既确保模型构造的严谨性与正确性，也提升算法实现的效率与可控性。

## 斐波那契数列

[题目链接](https://leetcode.cn/problems/fibonacci-number/)



## 题目要点解析



## 不同结构二叉树

[题目链接](https://www.nowcoder.com/practice/aaefe5896cce4204b276e213e725f3e/)



## 题目要点解析



## 最低票价问题

[题目链接](https://leetcode.cn/problems/minimum-cost-for-tickets/description/)



## 题目要点解析



## 简单的解码方法

[题目链接](https://leetcode.cn/problems/decode-ways/)



## 题目要点解析



## 困难的解码方式

[题目链接](https://leetcode.cn/problems/decode-ways-ii/)



## 题目要点解析



## 骑士的存活概率

[题目链接](https://leetcode.cn/problems/knight-probability-in-chessboard/)



## 题目要点解析



---

# 特殊动态规划问题



## 寻找下一个丑数

[题目链接](https://leetcode.cn/problems/ugly-number-ii/)



## 题目要点解析



## 有效涂色问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class068/Code04_FillCellsUseAllColorsWays.java)



## 题目要点解析



## 扰乱字符串问题

[题目链接](https://leetcode.cn/problems/scramble-string/description/)



## 题目要点解析



## 最长有效括号

[题目链接](https://leetcode.cn/problems/longest-valid-parentheses/)



## 题目要点解析



## 不同的子序列

[题目链接](https://leetcode.cn/problems/distinct-subsequences-ii/)



## 题目要点解析



## 整除子序列问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class071/Code02_MaxSumDividedBy7.java)



## 题目要点解析



## 数组逆序对构造

[题目链接](https://leetcode.cn/problems/k-inverse-pairs-array/)



## 题目要点解析



## 通向自由的道路

[题目链接](https://leetcode.cn/problems/freedom-trail/description/)



## 题目要点解析



---

# 参考文献列表

## 经典 DP 问题

1. [【ACM 算法题单】子数组最大累加和问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/maximum-subarray-sum/)

2. [【ACM 算法题单】最长公共子序列问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/longest-common-subsequence/)

3. [【ACM 算法题单】最长递增子序列问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/longest-increasing-subsequence/)

4. [【ACM 算法题单】整数拆分问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/integer-partition/integer-partition/)

## 经典 DP 分类

1. [【ACM 算法题单】背包动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/knapsack-dp/)

2. [【ACM 算法题单】区间动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/interval-dp/)

3. [【ACM 算法题单】树型动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)

4. [【ACM 算法题单】状压动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)

5. [【ACM 算法题单】数位动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)