---
title: 【XCPC 赛题复盘】2021 年 ICPC 陕西站
published: 2026-01-18
description: 2021 ICPC 陕西站全题目解法复盘与易错点总结。
tags: [Algorithm, XCPC, ACM]
category: ACM XCPC
draft: false
---

> 比赛链接：[2021年ICPC陕西省第九届大学生程序设计竞赛](https://ac.nowcoder.com/acm/contest/35232)

# 赛后总结复盘

赛时我们通过的是CEIJ这四道题。这一场的签到题目是I和J，E稍微动一下脑子也能解出来，但犯错特别多，需要重点注意。其中C题也算是比较难的题目，但是我们已经做出来了。其中E题很有可能做出来，本场比赛5题就能获得金牌，因此E题我们必须要争取。除此之外的题目都非常难，不需要考虑。

## E Swapping Game

[题目链接](https://ac.nowcoder.com/acm/contest/35232/E)

### Problem Statement

FF 有 n 只狗狗，编号为 $1, 2, 3, \ldot, n$ 。起初，狗狗们按编号升序排列。它们正在玩一个交换游戏，规则如下：

1. 狗狗们 **每秒** 都会进行一次交换。

2. **如果当前秒数是奇数**：交换下标为 $2 i - 1$ 和 $2i$ 的狗狗（其中 $1 \leq i \leq $ ）。
* *例如 $n = 5$ ，第 1 秒时：$(1, 2)$ 交换，$(3, 4)$ 交换，序列变为 $2, 1, 4, 3, 5$* 。

3. **如果当前秒数是偶数**：交换下标为 $2 i$ 和 $2 i + 1$ 的狗狗（其中 $1 \leq i \leq $ ）。
* *例如 $n = 5$ ，第 2 秒时：在之前的基础上，$(2, 3)$ 交换，$(4, 5)$ 交换，序列变为 $2, 4, 1, 5, 3$* 。

FF 想知道，在 **$k$ 秒之后** ，编号为 $q$ 的狗狗所在的 **下标（位置）** 是多少？

### Input

* 输入包含多组测试用例。第一行包含一个整数 $t(1 \leq t \leq 10^5)$ ，表示测试用例的数量。
* 每组测试用例包含三个整数 $n, k, q(1 \leq n, k, q \leq 10^9)$ 。

### Output

对每个测试用例，输出一行包含一个整数，代表最终位置。

### Sample Input 1

```txt showLineNumbers=false
3
5 1 3
5 2 3
6 1 4
```

### Sample Output 1

```txt showLineNumbers=false
4
5
3
```

## 题目要点分析



## C GCD

[题目链接](https://ac.nowcoder.com/acm/contest/35232/C)

### Problem Statement

Bob 对最大公约数（GCD）非常感兴趣。对于一组正整数 $(a_1, \ldot, a_k)$ ，$gcd(a_1, \ldot, a_k)$ 定义为最大的正整数 $d$ ，使得 $d$ 能整除每一个 $a_i$ 。

Bob 选定了一个闭区间 $[l, r]$ 。他准备从该区间内选择 **$k$ 个互不相同** 的整数，并计算它们的最大公约数。最终的计算结果（即 GCD 值）会有很多种可能性。Bob 想知道，一共有多少个不同的正整数可以作为这 $k$ 个不同整数的 GCD 值？

### Input

* 唯一的一行输入包含三个整数 $l, r, k$ 。
* 范围限制：$1 \leq l \leq r \leq 10^12, 2 \leq k \leq r - l + 1$ 。

### Output

输出一个整数，代表可能的 GCD 值的总数。

### Sample Input 1

```txt showLineNumbers=false
5 9 2
```

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点分析



## D Disease

[题目链接](https://ac.nowcoder.com/acm/contest/35232/D)

### Problem Statement

Gates 是一位超级富豪。由于 COVID-19 的影响，他必须采取充分的保护措施。为了远离病毒，他制定了严格的防护方案。

Gates 共有 $n - 1$ 个仆人，编号为 $2$ 到 $n$（Gates 本人的编号为 $1$ ）。他们之间存在 $n - 1$ 条接触边 $(u, v, a, b)$ ，满足以下规则：如果 $u$ 和 $v$ 两人中的一人感染了病毒，则另一人有 $a / b$ 的概率被传染。

我们保证这  条边构成一棵 **树** ，且 **Gates（编号 $1$ ）是这棵树的根** 。

* **等级定义**：一个人的 “等级” 被定义为其在树中的深度（Gates 的等级始终为 $1$ ）。
* **初始感染概率**：已知第  个人有  的概率从外部世界（初始时）感染病毒。
* **灾难值定义**：灾难值定义为 **所有感染者中等级最低（数值最小）的人的等级** 。如果没有人感染，则灾难值为 $0$ 。

请帮 Gates 计算 **灾难值的期望值** 。

### Input

* 第一行包含一个整数 $n(1 \leq n \leq 10^5)$ ，代表总人数。
* 接下来的 $n$ 行，每行包含两个整数 $p_i, q_i(0 \leq p_i \leq q_i \leq 10^6, q_i ≠ 0)$ ，描述第 $i$ 个人初始感染的概率。
* 接下来的 $n$ 行，每行包含四个整数 $u, v, a, b(1 \leq u, v \leq n, 0 \leq a \leq b \leq 10^6, b ≠ 0)$ ，描述树上的边及传染概率。

### Output

如果答案是最简分数 $\frac{A}{B}$ ，请输出 $\frac{A}{B}(mod 10^9 + 7)$。

### Sample Input 1

```txt showLineNumbers=false
3
0 1
0 1
1 1
1 2 1 2
2 3 1 2
```

### Sample Output 1

```txt showLineNumbers=false
250000004
```

## 题目要点分析



# 赛后总结提升

