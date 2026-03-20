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

# 划分动态规划问题

**划分动态规划** 是一类重要的动态规划模型，其基本思想是：将一个序列或区间按照某种方式划分为若干连续的部分，通过组合各部分的最优解得到整体的最优解。这类问题通常具有明显的 “分段” 结构，例如在序列中插入若干个分隔符、将区间划分为若干段、或者逐步决定最后一个划分位置等。由于每一种划分方式都可以看作是由前一部分的最优解扩展而来，因此非常适合用动态规划进行求解。

在划分动态规划中，最常见的状态定义是：

$$
dp[i][j]
$$

表示 **前 i 个元素被划分为 j 段时的最优值** 。在进行状态转移时，通常枚举最后一个划分点的位置。若最后一段是区间 $(k+1,i)$ ，那么前 $k$ 个元素已经被划分为 $j-1$ 段，于是转移方程一般写为：

$$
dp[i][j]= \max \min_{j-1\le k<i} (dp[k][j-1]+cost(k+1,i))
$$

其中 $cost(l,r)$ 表示区间 $[l,r]$ 的贡献或代价。通过枚举不同的划分点 $k$ ，可以找到当前状态的最优解。这类算法的时间复杂度通常为 $O(n^2k)$ ，其中 $n$ 是序列长度，$k$ 是划分次数。

一种常见的划分 DP 类型是 **固定划分次数的分段问题** 。在这类问题中，需要将序列划分为固定数量的段，例如在一个数字串中插入若干个乘号，使得得到的表达式值最大。这类问题通常需要预处理区间值，例如预处理子串对应的整数或区间代价，然后在 DP 中枚举最后一个划分点。典型题目包括数字分割、乘积最大问题等。

在解决这类问题时，动态规划的主要计算开销通常来自于 **枚举最后一个划分点 k** 。如果直接枚举所有可能的位置，整体复杂度一般为 $O(n^2k)$ 。在数据规模较大的情况下，可以根据问题的性质对这一过程进行优化，从而减少枚举范围或降低计算成本。

首先是 **区间代价的预处理优化** 。在许多划分问题中，转移方程中会频繁计算区间函数 $cost(l,r)$ 。如果每次都重新计算区间值，可能会增加额外的时间复杂度。因此通常会通过前缀和、预处理表或其他辅助数组，将区间代价提前计算出来，使得每次查询区间代价时只需要 $O(1)$ 的时间。例如在涉及区间和、区间平方和或子串转整数的问题中，都可以通过预处理降低转移时的计算开销。

其次是 **决策单调性优化** 。在某些划分问题中，最优划分点的位置会随着状态变化而呈现单调性，即对于状态 $dp[i][j]$ 的最优划分点 $opt[i][j]$ ，满足：

$$
opt[i][j] \le opt[i+1][j]
$$

当这种性质成立时，在计算 $dp[i][j]$ 时就不需要在整个区间内枚举划分点，而只需要在一个较小的范围内搜索。利用分治思想可以进一步减少枚举范围，从而将原本的 $O(n^2k)$ 复杂度优化为 $O(nk \log n)$ 或 $O(nk)$ 。这种优化在某些区间代价具有凸性或满足四边形不等式的分段问题中较为常见。

## 字符串乘积最值

[题目链接](https://www.luogu.com.cn/problem/P1018)



## 题目要点解析



## 统计单词个数

[题目链接](https://www.luogu.com.cn/problem/P1026)



## 题目要点解析



## 环形数字游戏

[题目链接](https://www.luogu.com.cn/problem/P1043)



## 题目要点解析



---

# 特殊动态规划问题

动态规划是一类非常重要的算法思想，在许多问题中都能够通过 **状态设计与转移关系** 来逐步构造答案。对于一些经典模型，例如背包问题、区间 DP、树形 DP 等，往往已经有较为固定的套路和解题方法。但在实际做题过程中，仍然会遇到大量 **不完全符合经典模型的动态规划问题** ，这些问题通常被称为 “特殊动态规划” 。

与常规模型不同，这类动态规划往往 **没有明显的模板可套** 。题目的关键往往在于如何观察问题结构，从中抽象出合适的状态表示方式，并找到合理的状态转移关系。很多时候，状态的设计本身就决定了问题是否能够用动态规划解决，因此这类题目往往更加依赖对问题结构的理解以及一定的解题经验。

在解决特殊动态规划问题时，常见的思考方式包括：尝试从问题的 **最优子结构** 入手，思考当前状态是否可以由更小规模的问题推导得到；观察题目中的 **顺序关系或结构限制** ，例如时间顺序、区间关系或树结构；以及考虑是否可以通过 **重新定义状态或引入辅助信息** 来简化转移过程。很多看似复杂的问题，一旦找到合适的状态表达方式，转移关系往往会变得非常自然。

总体来说，特殊动态规划问题的特点在于 **灵活性与创造性**。相比套用固定模板，更重要的是理解问题本身的结构，并通过合理的状态设计将其转化为可递推的形式。随着做题经验的积累，这类问题中的常见思路也会逐渐变得清晰，从而更容易发现隐藏在题目中的动态规划结构。

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

5. [【ACM 算法题单】有效括号问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/regular-bracket/)

## 经典 DP 分类

1. [【ACM 算法题单】背包动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/knapsack-dp/)

2. [【ACM 算法题单】区间动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/interval-dp/)

3. [【ACM 算法题单】树型动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)

4. [【ACM 算法题单】状压动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)

5. [【ACM 算法题单】数位动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)