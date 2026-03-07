---
title: 【ACM 算法题单】树上算法相关问题
published: 2026-03-06
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type, Grid Graph]
category: ACM Type
draft: false
---

# DFN 序相关问题

在图论算法中，**DFN 序（Depth First Numbering）**指的是在进行一次深度优先搜索（DFS）时，按照节点被第一次访问的顺序所得到的一种编号序列。具体来说，当 DFS 访问到一个节点时，就为它分配一个递增的时间戳，这个编号就称为该节点的 **dfn 值** 。因此，DFN 序本质上就是 **DFS 遍历过程中节点被访问的时间顺序** 。

在实现时，我们通常维护一个全局计数器 `timer` 。当 DFS 第一次进入某个节点 $u$ 时，就执行 `dfn[u] = ++timer` ，表示这是当前第 `timer` 个被访问的节点。由于 DFS 会沿着一条路径不断向下递归，因此 **dfn 序往往会连续地覆盖整棵子树** 。也就是说，如果在 DFS 树中节点 $u$ 的子树包含若干节点，那么这些节点的 dfn 编号通常会形成一个连续区间。这一性质在许多算法中非常重要。

从结构上理解，DFN 序实际上是在给 DFS 树做一种 **线性化（linearization）**。原本的树结构是一个分支结构，而通过 DFS 编号之后，我们可以把节点映射到一个一维序列上。这样，许多 “子树问题” 就可以转化为 “数组区间问题” 。例如，如果节点 $u$ 的子树对应的 dfn 区间是 $\big[dfn[u], dfn[u] + siz[u] - 1\big]$ ，那么对子树进行查询或修改时，就可以转化为对这个区间进行操作。这也是树状数组和线段树在树结构中常见的应用方式。

DFN 序在许多经典图论算法中都有重要作用。例如在 **Tarjan 求强连通分量** 时，dfn 表示节点被 DFS 访问的时间，而通过比较 `dfn` 与 `low` 值可以判断一个强连通分量的根节点；在 **Tarjan 求割点和桥** 的算法中，dfn 同样用于表示访问顺序，并通过回边更新 `low` 值来判断图的结构性质。此外，在一些树上算法中，例如 **树链剖分** 或 **欧拉序列处理子树问题**，也会使用 DFS 编号来把树结构映射为数组区间。

从更高层次的角度看，DFN 序的核心作用在于：**利用 DFS 的访问顺序，把原本复杂的图或树结构转化为一个具有顺序关系的编号体系** 。一旦节点被映射到线性序列中，许多原本复杂的结构性问题就可以转化为简单的区间问题，从而借助各种数据结构高效解决。这也是 DFN 序在图论与树算法中被广泛使用的根本原因。

## 带修二叉树高度

[题目链接](https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/)



## 题目要点解析



## 删边的最小代价

[题目链接](https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/)



## 题目要点解析



---

# 参考文献列表

1. [【Daltao's blog】树上算法](https://taodaling.github.io/blog/2019/09/10/树上算法/)