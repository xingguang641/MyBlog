---
title: 【ACM 算法题单】树上算法相关问题
published: 2026-03-06
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type, Grid Graph]
category: ACM Type
draft: false
---

# DFN 序相关问题

在树结构的算法中，**DFN 序（Depth First Numbering）**指的是在进行一次深度优先搜索时，按照节点被第一次访问的顺序为每个节点分配的编号。具体来说，当 DFS 第一次访问到节点 $u$ 时，就给它分配一个递增的时间戳，这个编号称为该节点的 **dfn 值** 。因此，DFN 序本质上就是 **节点在 DFS 遍历过程中被访问的先后顺序** 。

在实现时，通常会维护一个全局计数器 `timer` 。当 DFS 第一次进入节点 $u$ 时执行：

$$
dfn[u] = ++timer
$$

表示节点 $u$ 是第 `timer` 个被访问到的节点。由于 DFS 会先访问当前节点，再递归访问其所有子节点，因此 **一个节点的整棵子树通常会被连续访问** 。如果记 $siz[u]$ 表示节点 $u$ 的子树大小，那么节点 $u$ 的子树在 DFN 序中往往对应一个连续区间：

$$
\big[dfn[u], dfn[u] + siz[u] - 1\big]
$$

这一性质使得我们可以把树结构中的 **子树问题** 转化为 **数组区间问题** 。

从结构上看，DFN 序的核心作用其实是一种 **树的线性化（linearization）**。原本的树是一个分支结构，而通过 DFS 编号之后，每个节点都会对应到一个一维数组的位置。这样一来，如果题目中需要对某个节点的 **整棵子树进行统计或计算** ，就可以直接转化为对数组中某一段区间进行操作，然后我们还能借助 **树状数组或线段树** 来维护区间信息，从而更高效地完成查询与更新。

从更高层次的角度来看，DFN 序的关键作用在于：**将树上的子树结构映射到一个连续的数组区间中** 。一旦完成这种映射，原本复杂的树结构问题就能够借助成熟的数组数据结构进行处理，从而大大简化算法设计。这也是 DFN 序在树上算法中被广泛使用的重要原因。

## 带修二叉树高度

[题目链接](https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/)



## 题目要点解析



## 删边的最小代价

[题目链接](https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/)



## 题目要点解析



## 另一颗树的子树

[题目链接](https://leetcode.cn/problems/subtree-of-another-tree/description/)



## 题目要点解析



## 比较树的权值

[题目链接](https://atcoder.jp/contests/abc406/tasks/abc406_f)



## 题目要点解析



## 树上逆序对计数

[题目链接](https://www.luogu.com.cn/problem/P3605)



## 题目要点解析



---

# 参考文献列表

1. [【Daltao's blog】树上算法](https://taodaling.github.io/blog/2019/09/10/树上算法/)