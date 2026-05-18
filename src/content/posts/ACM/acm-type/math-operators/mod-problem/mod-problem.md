---
title: 【ACM 算法题单】MOD相关问题
published: 2026-03-24
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# MOD两数之和问题

在处理涉及模运算的加法问题时，一个核心的观察在于对操作数取值范围的精确控制。当我们预先对 $a$ 和 $b$ 分别执行 $a \pmod M$ 与 $b \pmod M$ 的标准化操作后，这两个操作数均被约束在半开区间 $[0, M)$ 之内。此时，它们的算术和 $a + b$ 的取值范围必然处于 $[0, 2M - 2]$ 之间。这一性质直接简化了取模运算的逻辑分支：

由于 $a + b$ 最大也不会达到 $2M$ ，因此 $(a + b) \pmod M$ 的结果只存在两种线性可能。若 $a + b$ 小于 $M$ ，则其模运算结果即为原和本身；若 $a + b$ 落在 $[M, 2M - 2]$ 之间，则等价于从和中减去一个周期的偏移量。这种分类讨论通常被表述为：

$$
(a + b) \pmod M =
\begin{cases}
a + b, & a + b < M \\
a + b - M, & a + b \geq M
\end{cases}
$$

这一结论在算法优化中具有极高的实用价值。它不仅规避了计算机底层的除法/取模指令（这些指令通常比加减法慢数倍），还为诸如 **双指针** 或 **二分查找** 解决 “两数之和模 $M$ 的最大值” 等问题奠定了理论基础。通过将复杂的余数分布简化为简单的线性平移，我们能够更直观地在同余系下维护数值的单调性，从而将原本 $O(N^2)$ 的暴力搜索通过排序与双指针技巧优化至 $O(N \log N)$ 。

## 取模累加和问题

[题目链接](https://atcoder.jp/contests/abc416/tasks/abc416_d)



## 题目要点解析



## 二小姐取数问题

[题目链接](https://ac.nowcoder.com/acm/contest/119225/E)



## 题目要点解析



## 整除子序列问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class071/Code02_MaxSumDividedBy7.java)



## 题目要点解析



---

# 参考文献列表

1. [【ACM 算法题单】同余原理相关问题](https://xingguang641.com/posts/acm/acm-type/math-operators/mod-problem/congruence/)