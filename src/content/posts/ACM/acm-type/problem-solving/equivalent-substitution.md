---
title: 【ACM 算法题单】等价变换相关问题
published: 2026-05-08
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 等价变换题目合集



## 复杂的购票难题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class091/Code03_GroupBuyTickets1.java)

### Problem Statement

某单位共有 $n$ 个人，景区里一共有 $m$ 个项目。每个项目 $i$ 有两个正整数参数：折扣系数 $K_i$ 和票价 $B_i$ 。

购票规则如下：

- 如果有 $x$ 个人买票游玩项目 $i$ ，则单张门票的价格为 $\max \{ B_i - K_i \times x, 0 \}$ 。
- $x$ 个人游玩该项目的总花费为 $x \times \max \{ B_i - K_i \times x, 0 \}$ 。由于总花费不会为负数，实际计算公式为 $\max \{ x \times (B_i - K_i \times x), 0 \}$ 。

单位里的每个人最多可以选择 $1$ 个项目游玩，也可以不选任何项目。所有员工将在明晚提交他们的选择，然后由你统一购票。你需要准备足够多的钱，以应对所有可能的员工选择情况。请返回这个 “最保险” 的钱数（即在所有可能的分配方案中，单位总花费的最大值）。

### Constraints

- $1 \leq m, n, K_i, B_i \leq 10^5$

### Input

输入包含多行：

- 第一行包含两个整数 $m$ 和 $n$ 。
- 接下来的 $m$ 行，每行包含两个整数，分别表示第 $i$ 个项目的 $K_i$ 和 $B_i$ 。

> $m \quad n$
> 
> $K_1 \quad B_1$
> 
> $K_2 \quad B_2$
> 
> $\ldots$
> 
> $K_m \quad B_m$

### Output

输出一个整数，表示最保险的准备金额。

## 题目要点解析



## 灌溉花园所需的最少水龙头数目

[题目链接](https://leetcode.cn/problems/minimum-number-of-taps-to-open-to-water-a-garden/description/)

### Problem Statement

在 $x$ 轴上有一个长度为 $n$ 的花园，范围从 $0$ 到 $n$ 。

花园里安装了 $n + 1$ 个水龙头，分别位于 $[0, 1, \dots, n]$ 的位置。给你一个整数 $n$ 和一个长度为 $n + 1$ 的整数数组 `ranges` ，其中 `ranges[i]` 表示第 $i$ 个水龙头（位于 $i$ 处）的灌溉范围为 $[i - ranges[i], i + ranges[i]]$ 。

请你求出能够灌溉整个花园 $[0, n]$ 所需的最少水龙头数目。如果花园无法被水龙头全灌溉，请返回 $-1$ 。

### Constraints

- $1 \leq n \leq 10^4$
- $ranges.length == n + 1$
- $0 \leq ranges[i] \leq 100$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ 。
- 第二行包含 $n + 1$ 个整数，表示数组 $ranges$ 中的元素。

> $n$
> 
> $ranges_0 \quad ranges_1 \quad \ldots \quad ranges_n$

### Output

输出一个整数，表示能够灌溉整个花园的最少水龙头数目。

### Sample Input 1

```txt showLineNumbers=false
5
3 4 1 1 0 0
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
3
0 0 0 0
```

### Sample Output 2

```txt showLineNumbers=false
-1
```

## 题目要点解析


