---
title: 【XCPC 赛题复盘】2021 年 CCPC 新疆省赛 
published: 2026-01-17
description: 2021 CCPC 新疆省赛全题目解法复盘与易错点总结。
tags: [Algorithm, XCPC, ACM]
category: ACM XCPC
draft: false
---

> 比赛链接：[2021 CCPC 大学生程序设计竞赛新疆省赛](https://ac.nowcoder.com/acm/contest/35232)

# 赛后总结复盘

我们赛事做出了ABD这三道题，其实C和E是有机会做出来的，但是没多想就结束比赛了。AB就是最简单的签到题没什么好说的，D是优先队列的常见用法，需要掌握。C则是基本上都想到了，但是没学过强连通分量做不出俩。E题就是观察题目随机应变的题目，一开始没有想清楚导致后面没人去写，一开始以为是是卷积问题了，其实根本不是。H题是看过答案之后也能写出来的题目，就是位运算基本的思考路线，按位拆分。

## D MaxSum

[题目链接](https://ac.nowcoder.com/acm/contest/22754/D)

### Problem Statement

给你 $n$ 个数 $a_i$ ，定义 $S_{(l,r)} = \sum_{i=l}^{r} a_i$（ $1 \leq l \leq r \leq n $ ），显然有 $\frac{n \times (n + 1)}{2}$ 个 $S$ ，出题人希望你能求出这些区间和中 **最大的前 $w$ 个 $S$** 。

### Input

* 第一行是两个整数 $n, w$ 。
* 第二行包含 $n$ 个数，第 $i$ 个数是 $a_i$ 。
* $0 \leq a_i \leq 10^9, 0 \leq w \leq \min\left(\frac{n \times (n + 1)}{2}, 10^5\right), 0 \leq n \leq 10^5$

### Output

输出 $w$ 个数，这些数代表答案，用空格分隔。

### Sample Input 1

```txt showLineNumbers=false
6 8
1 1 4 5 1 4
```

### Sample Output 1

```txt showLineNumbers=false
16 15 14 12 11 11 10 10
```

### Sample Input 2

```txt showLineNumbers=false
7 8
1 9 1 9 8 1 0
```

### Sample Output 2

```txt showLineNumbers=false
29 29 28 28 28 27 20 19
```

## 题目要点分析



## E Array

[题目链接](https://ac.nowcoder.com/acm/contest/22754/E)

### Problem Statement

给定两个整数数组 $a$ 和 $b$ ，Bob 想要计算数组 $c$ 。

数组 $c$ 的计算公式如下：

$$
c_i = max_{0 \leq j < n} \{ a_j + b_{(i-j+n) mod n} \}
$$

### Input

* 第一行是一个正整数 $n$ 。
* 第二行包含 $n$ 个整数 $a_0, a_1, \ldot, a_{n-1}$ 。
* 第三行包含 $n$ 个整数 $b_0, b_1, \ldot, b_{n-1}$ 。
* $0 \leq a_i, b_i \leq 5000, \sum a_i \leq 5000, \sum b_i \leq 5000, n \leq 2 \times 10^5$

### Output

输出一行，包含 $n$ 个整数 $c_0, c_1, \ldot, c_{n-1}$ 。

### Sample Input 1

```txt showLineNumbers=false
5
3 2 4 7 5
8 9 6 1 0
```

### Sample Output 1

```txt showLineNumbers=false
14 12 12 15 16
```

## 题目要点分析



## C Bomb

[题目链接](https://ac.nowcoder.com/acm/contest/22754/C)

### Problem Statement

小祥有一个包含 $n$ 个点和 $m$ 条边的 **有向图** 。起初，图上每个点都是白色的。现在小祥想把每个点都染成黑色。她可以进行几轮染色，规则如下：

* **染色数量**：在每一轮染色中，可以染 **任意数量** 的点。
* **染色限制**：在同一轮中，被染色的点集里不能出现一对 **不同** 的点 $i, j$ ，使得点 $i$ 能够到达点 $j$ 。

你需要计算：想要将所有点染成黑色，**至少** 需要进行多少轮染色。

### Input

* 第一行包含两个正整数 $n, m$ ，代表点数和边数。点的编号为 $1 ~ n$ 。
* 接下来 $m$ 行，每行两个正整数 $x, y$ ，表示存在一条从 $x$ 指向 $y$ 的有向边。
* 范围：$2 \leq n \leq 10^6, 1 \leq m \leq 10^6$ 。

### Output

仅包含一行一个正整数，表示最少染色轮数。

### Sample Input 1

```txt showLineNumbers=false
5 4
1 2
2 3
3 1
4 5
```

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点分析



## H XOR

[题目链接](https://ac.nowcoder.com/acm/contest/22754/H)

### Problem Statement

给定 $n$ 个正整数 $a_1, a_2, \ldots, a_n$ ，请求计算：$\sum_{i=1}^{n} \sum_{j=1}^{n} (a_i \oplus a_j)^2$

其中 “$\oplus$” 表示按位异或（XOR）操作。


### Input

* 第一行包含一个正整数 $n$ 。
* 第二行包含 $n$ 个正整数 $a_1, a_2, \ldots, a_n$ 。
* $1 \leq n \leq 50000, 0 < a_i \leq 10^9$

### Output

输出一个整数，即答案，对 $10^9 + 7$ 取模。

### Sample Input 1

```txt showLineNumbers=false
3
2 5 4
```

### Sample Output 1

```txt showLineNumbers=false
172
```

## 题目要点分析

