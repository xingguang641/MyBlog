---
title: 【ACM 算法题单】增量算法相关问题
published: 2026-05-08
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 增量算法题目合集

增量法是一类基于 **单调性** 或 **局部可更新性** 的处理技巧。其核心思想在于：通过人为构造一种状态演进的顺序，使得在处理每一个新元素时，我们仅需对受影响的局部变化进行维护，而非推倒重来进行全局计算。正因为这种方法高度依赖于我们对处理顺序的 **主动设计** ，它更像是一种底层思考方式而非固定的算法模板。无论是通过排序建立单调性，还是通过扫描线动态演进，本质上都是在利用已知状态与新状态之间的强关联来降低计算成本。

由于不存在一套能机械套用的统一流程，增量法的难点并不在于编码细节，而在于我们能否从错综复杂的约束中，通过 **构造合适的处理路径** ，敏锐地识别出具备增量维护特征的递推条件。通过对题目结构特征的深入剖析，我们可以准确识别出哪些 **难以处理的复杂约束** 适合通过增量方式进行化解，并以此为突破口建立状态间的递推联系。这种思维习惯能够帮助我们敏锐地察觉到题目约束中的突破点，从而在面对复杂的动态问题时，能够通过主动构造处理路径，将原本棘手的全局性限制转化为可控的局部更新。

## 限距的下降跳跃

[题目链接](https://atcoder.jp/contests/abc408/tasks/abc408_f)

### Problem Statement

有 `N` 个脚手架排成一排，编号为 `1` 到 `N` 。第 `i` 个脚手架的高度为 `H_i` 。

高桥将进行如下游戏：

- 开始时，他可以任选一个脚手架 `i` 站上去。
- 如果当前站在脚手架 `i`，他可以移动到脚手架 `j`，当且仅当满足：

  - `1 ≤ |i - j| ≤ R`
  - `H_j ≤ H_i - D`

也就是说：

- 目标脚手架与当前位置的距离 **不超过 `R` 且不为 0** 。
- 目标脚手架的高度 **至少比当前脚手架低 `D`** 。

高桥会不断移动，直到 **无法再进行合法移动为止** 。求他最多可以移动多少次。

### Constraints

- $1 \leq N \leq 5 × 10^5$
- $1 \leq D, R \leq N$

### Input

输入包含两行：

- 第一行包含三个整数 $N$ 、$D$ 、$R$ 。
- 第二行包含 $N$ 个整数 $H_i$ ，表示数组元素。

> $N \quad D \quad R$
> 
> $H_1 \quad H_2 \quad \ldots \quad H_N$

### Output

输出一个整数，表示最多可以进行的移动次数。

### Sample Input 1

```txt showLineNumbers=false
5 2 1
5 3 1 4 2
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
13 3 2
13 7 10 1 9 5 4 11 12 2 8 6 3
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析



## 数组逆序对构造

[题目链接](https://leetcode.cn/problems/k-inverse-pairs-array/)

### Problem Statement

对于一个包含 $1$ 到 $n$ 的整数的数组，如果满足 $i < j$ 且 `nums[i] > nums[j]` ，则称 `(i, j)` 为一个 **逆序对** 。

给定两个整数 $n$ 和 $k$ ，请返回满足恰好包含 $k$ 个逆序对的、长度为 $n$ 的数组的个数。由于答案可能很大，请返回答案对 $10^9 + 7$ 取模的结果。

### Constraints

- $1 \leq n \leq 1000$
- $0 \leq k \leq 1000$

### Input

输入仅包含一行：

> $n \quad k$

### Output

输出一个整数，表示满足条件的数组个数对 $10^9 + 7$ 取模的结果。

### Sample Input 1

```txt showLineNumbers=false
3 0
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
3 1
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析

