---
title: 【ACM 算法比赛】2026牛客暑期多校训练营02
published: 2026-08-01
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

# 比赛题目讲解

[比赛链接](https://ac.nowcoder.com/acm/contest/133877)

## Problem N

[题目链接](https://ac.nowcoder.com/acm/contest/133877/N)

### Problem Statement

给定一个长度为 $n$ 的数组 $a$ 。

一次操作中，你可以选择数组中的任意 $k$ 个元素，并将这 $k$ 个元素全部替换为它们的中位数。

你必须恰好执行一次操作，请求出操作后数组所有元素之和的最大值。

中位数定义如下：

设选中的 $k$ 个元素按照非递减顺序排列为：

$$
b_1 \leq b_2 \leq \cdots \leq b_k
$$

- 当 $k$ 为奇数时，中位数为唯一的中间元素：

$$
b_{\frac{k+1}{2}}
$$

- 当 $k$ 为偶数时，中位数为两个中间元素的平均值：

$$
\frac{b_{\frac{k}{2}}+b_{\frac{k}{2}+1}}{2}
$$

### Constraints

- $1 \leq T \leq 10^4$
- $1 \leq k \leq n \leq 2 \times 10^5$
- $1 \leq a_i \leq 10^9$
- 所有测试数据中 $n$ 的总和不超过 $2 \times 10^5$

### Input

输入包含多组测试数据：

- 第一行包含一个整数 $T$ ，表示测试数据组数。
- 接下来每组测试数据包含两行：
  - 第一行包含两个整数 $n,k$ ，表示数组长度和选择元素的数量。
  - 第二行包含 $n$ 个整数，表示数组中的元素。

> $T$
>
> $n \quad k$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

对于每组测试数据，输出一个整数，表示执行一次操作后数组元素和的最大值。

### Sample Input

```txt showLineNumbers=false
2
6 3
1 1 4 5 1 4
4 2
1 3 6 10
````

### Sample Output

```txt showLineNumbers=false
19
20
```

## Solution