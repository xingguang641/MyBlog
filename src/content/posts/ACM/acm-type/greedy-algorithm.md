---
title: 【ACM 算法题单】贪心算法相关问题
published: 2026-03-25
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 子串拼接贪心问题

记录各种贪心排序

## 最大数构造问题

[题目链接](https://leetcode.cn/problems/largest-number/description/)

### Problem Statement

给定一组非负整数 `nums` ，重新排列每个数的顺序（每个数不可拆分）使之组成一个最大的整数。

**注意**：输出结果可能非常大，所以你需要返回一个字符串而不是整数。

### Constraints

- $1 \leq nums.length \leq 100$
- $0 \leq nums[i] \leq 10^9$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组的长度。
- 第二行包含 $n$ 个非负整数，表示数组 $nums$ 中的元素。

> $n$
> 
> $nums_0 \quad nums_1 \quad \ldots \quad nums_{n-1}$

### Output

输出一个字符串，表示组成的最大的整数。

### Sample Input 1

```txt showLineNumbers=false
2
10 2
```

### Sample Output 1

```txt showLineNumbers=false
210
```

### Sample Input 2

```txt showLineNumbers=false
5
3 30 34 5 9
```

### Sample Output 2

```txt showLineNumbers=false
9534330
```

## 题目要点解析

交叉组合排序

## 所需的最少能量

[题目链接](https://leetcode.cn/problems/minimum-initial-energy-to-finish-tasks/description/)

### Problem Statement

给你一个任务数组 $tasks$ ，其中 $tasks[i] = [actual_i, minimum_i]$ ：

- $actual_i$ 是完成第 $i$ 个任务需要耗费的能量。
- $minimum_i$ 是开始第 $i$ 个任务前需要具备的最少能量。

比如，如果任务为 $[10, 12]$ ，而你当前的能量为 $11$ ，那么你不能开始该任务。如果你当前的能量为 $13$ ，你可以开始该任务，且完成任务后剩余能量为 $3$ 。

你可以按 **任意顺序** 完成任务。请你返回完成所有任务所需的 **最少** 初始能量。

### Constraints

- $1 \leq tasks.length \leq 10^5$
- $1 \leq actual_i \leq minimum_i \leq 10^4$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示任务的数量。
- 接下来的 $n$ 行，每行包含两个整数，分别表示 $actual_i$ 和 $minimum_i$ 。

> $n$
> 
> $actual_1 \quad minimum_1$
> 
> $actual_2 \quad minimum_2$
> 
> $\ldots$
> 
> $actual_n \quad minimum_n$

### Output

输出一个整数，表示完成所有任务所需的最少初始能量。

### Sample Input 1

```txt showLineNumbers=false
5
1 3
2 4
10 11
10 12
8 9
```

### Sample Output 1

```txt showLineNumbers=false
32
```

### Sample Input 2

```txt showLineNumbers=false
3
1 7
2 8
3 9
```

### Sample Output 2

```txt showLineNumbers=false
13
```

## 题目要点解析

差值贪心排序

## 知识竞赛的筹备

[题目链接](https://www.nowcoder.com/practice/2a9089ea7e5b474fa8f688eae76bc050)

### Problem Statement

部门要选两位员工参加知识竞赛。每个员工 $i$ 有两个能力值：推理能力 $A_i$ 和阅读能力 $B_i$ 。

如果选择第 $i$ 个人和第 $j$ 个人组队，他们在竞赛中表现出的能力如下：

- **阅读能力**：$X = \frac{B_i + B_j}{2}$
- **推理能力**：$Y = \frac{A_i + A_j}{2}$

现在需要最大化他们表现较差一方面的能力，即让 $\min(X, Y)$ 尽可能大。请问这个最大值是多少？

### Constraints

- $2 \leq n \leq 2 \times 10^5$
- $1 \leq A_i, B_i \leq 10^8$

### Input

输入包含多行：

- 第一行包含一个正整数 $n$ ，代表员工数。
- 接下来的 $n$ 行，每行包含两个正整数 $A_i$ 和 $B_i$ ，分别描述第 $i$ 个员工的推理能力和阅读能力。

> $n$
> 
> $A_1 \quad B_1$
> 
> $A_2 \quad B_2$
> 
> $\ldots$
> 
> $A_n \quad B_n$

### Output

仅输出一行，包含一个一位小数，表示 $\min(X, Y)$ 的最大值。

### Sample Input 1

```txt showLineNumbers=false
3
2 2
3 1
1 3
```

### Sample Output 1

```txt showLineNumbers=false
2.0
```

## 题目要点解析

最小值贪心排序/差值绝对值贪心排序（最小值贪心需要证明正确性，可以对拍）

## 消灭的怪物数量

[题目链接](https://leetcode.cn/problems/eliminate-maximum-number-of-monsters/description/)

### Problem Statement

你正在玩一款电子游戏，在游戏中你需要保护城市免受怪物的进攻。给你两个长度为 $n$ 的整数数组 $dist$ 和 $speed$ ，其中 $dist[i]$ 是第 $i$ 只怪物距离城市的初始距离，而 $speed[i]$ 是这只怪物每分钟向城市移动的速度。

你在游戏开始时（第 $0$ 分钟）有一把武器，并已经蓄力完毕。你可以使用这把武器 **瞬间** 消灭一只怪物。但是，武器每次使用后都需要 $1$ 分钟的时间进行再充电，在此期间你无法再次使用。

当怪物的距离 **小于或等于 0** 时，它就到达了城市，游戏结束。

请返回在输掉游戏前，你最多能消灭的怪物数量。如果你可以在所有怪物到达城市前将它们全部消灭，返回 $n$ 。

### Constraints

- $n == dist.length == speed.length$
- $1 \leq n \leq 10^5$
- $1 \leq dist[i], speed[i] \leq 10^5$

### Input

输入包含三行：

- 第一行包含一个整数 $n$ ，表示怪物的数量。
- 第二行包含 $n$ 个整数，表示数组 $dist$ 中的元素。
- 第三行包含 $n$ 个整数，表示数组 $speed$ 中的元素。

> $n$
> 
> $dist_0 \quad dist_1 \quad \ldots \quad dist_{n-1}$
> 
> $speed_0 \quad speed_1 \quad \ldots \quad speed_{n-1}$

### Output

输出一个整数，表示你最多能消灭的怪物数量。

### Sample Input 1

```txt showLineNumbers=false
3
1 3 4
1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
4
1 1 2 3
1 1 1 1
```

### Sample Output 2

```txt showLineNumbers=false
1
```

## 题目要点解析

性价比排序

## 最低的雇佣成本

[题目链接](https://leetcode.cn/problems/minimum-cost-to-hire-k-workers/description/)

### Problem Statement

有 $n$ 名工人。给定两个整数数组 $quality$ 和 $wage$ ，其中 $quality[i]$ 表示第 $i$ 名工人的工作质量，$wage[i]$ 表示第 $i$ 名工人的最低期望工资。

现在我们想雇佣恰好 $k$ 名工人组成一个小组。在雇佣一组工人时，我们必须按照下述规则付费：

- 对小组内的每一名工人，应当按其工作质量与小组内其他工人的工作质量的比例来付工资。
- 小组内每名工人的工资至少应当是其最低期望工资。

请返回支付这 $k$ 名工人的最低成本。与实际答案误差在 $10^{-5}$ 以内的结果将被视为正确。

### Constraints

- $n == quality.length == wage.length$
- $1 \leq k \leq n \leq 10^4$
- $1 \leq quality[i], wage[i] \leq 10^4$

### Input

输入包含三行：

- 第一行包含两个整数 $n$ 和 $k$ 。
- 第二行包含 $n$ 个整数，表示数组 $quality$ 中的元素。
- 第三行包含 $n$ 个整数，表示数组 $wage$ 中的元素。

> $n \quad k$
> 
> $quality_0 \quad quality_1 \quad \ldots \quad quality_{n-1}$
> 
> $wage_0 \quad wage_1 \quad \ldots \quad wage_{n-1}$

### Output

输出一个浮点数，表示最低总成本，保留五位小数。

### Sample Input 1

```txt showLineNumbers=false
3 2
10 20 5
70 50 30
```

### Sample Output 1

```txt showLineNumbers=false
105.00000
```

### Sample Input 2

```txt showLineNumbers=false
5 3
3 1 10 10 1
4 8 2 2 7
```

### Sample Output 2

```txt showLineNumbers=false
30.66667
```

## 题目要点解析

性价比排序

---

# 两地调度贪心问题

先全部选一个数组，然后再适当调整的贪心策略

## 两地的调度问题

[题目链接](https://leetcode.cn/problems/two-city-scheduling/description/)

### Problem Statement

公司计划面试 $2n$ 名调度人员。给你一个数组 $costs$ ，其中 $costs[i] = [aCost_i, bCost_i]$ ，表示第 $i$ 人飞往 $A$ 市的费用为 $aCost_i$ ，飞往 $B$ 市的费用为 $bCost_i$ 。

返回将每个人飞往其中一座城市的最低总费用，要求每个城市都有 $n$ 人抵达。

### Constraints

- $2n == costs.length$
- $2 \leq costs.length \leq 100$
- $costs.length$ 是偶数
- $1 \leq aCost_i, bCost_i \leq 1000$

### Input

输入包含多行：

- 第一行包含一个整数 $2n$ ，表示调度人员的总数。
- 接下来的 $2n$ 行，每行包含两个整数，分别表示 $aCost_i$ 和 $bCost_i$ 。

> $2n$
> 
> $aCost_1 \quad bCost_1$
> 
> $aCost_2 \quad bCost_2$
> 
> $\ldots$
> 
> $aCost_{2n} \quad bCost_{2n}$

### Output

输出一个整数，表示最低总费用。

### Sample Input 1

```txt showLineNumbers=false
4
10 20
30 200
400 50
30 20
```

### Sample Output 1

```txt showLineNumbers=false
110
```

### Sample Input 2

```txt showLineNumbers=false
6
259 770
448 54
926 667
184 139
840 118
577 469
```

### Sample Output 2

```txt showLineNumbers=false
1859
```

## 题目要点解析



---

# 果子合并贪心问题



## 果子的合并难题

[题目链接](https://www.luogu.com.cn/problem/P1090)

### Problem Statement

在一个果园里，多多已经打下了 $n$ 堆果子，每堆果子都有一定的质量。多多决定把这些果子合并成一堆。

每次合并时，多多可以把两堆果子合并到一起，消耗的体力等于两堆果子的质量之和。经过 $n-1$ 次合并后，所有的果子就合并成了一堆。

由于多多体力有限，他希望在将所有果子合并成一堆的过程中，消耗的总体力最小。请你计算并输出这个最小体力值。

### Constraints

- $1 \leq n \leq 10^4$
- 每堆果子的质量均小于 $2 \times 10^4$
- 保证最终耗费的总体力值小于 $2^{31}$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示果子的堆数。
- 第二行包含 $n$ 个整数，用空格隔开，表示第 $i$ 堆果子的质量 $a_i$ 。

> $n$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

输出一个整数，表示最小消耗的体力值。

### Sample Input 1

```txt showLineNumbers=false
3
1 2 9
```

### Sample Output 1

```txt showLineNumbers=false
15
```

## 题目要点解析



---

# 整数拆分贪心问题

整数拆分动态规划是计算拆分的不同方法数，整数拆分贪心是使得最终的累乘积最大

## 竹子的最大价值

[题目链接](https://leetcode.cn/problems/jian-sheng-zi-ii-lcof/description/)

### Problem Statement

现需要将一根长为正整数 `bamboo_len` 的竹子砍为若干段，每段长度均为 **正整数** 。请返回每段竹子长度的 **最大乘积** 是多少。

由于答案可能很大，请将结果对 $10^9 + 7$ 取模。

### Constraints

- $2 \leq n \leq 1000$

### Input

输入仅包含一行：

> $n$

### Output

输出一个整数，表示最大乘积对 $10^9 + 7$ 取模后的值。

### Sample Input 1

```txt showLineNumbers=false
12
```

### Sample Output 1

```txt showLineNumbers=false
81
```

## 题目要点解析



## 拆分的最大乘积

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class090/Code02_MaximumProduct.java)



## 题目要点解析



---

# 会议安排贪心问题

有排序做法也有不排序做法

区间调度问题，一般都需要用优先队列

## 会议的安排问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class090/Code03_MeetingMonopoly1.java)



## 题目要点解析



## 最大的会议数量

[题目链接](https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended/description/)



## 题目要点解析

这题就是经典的区间调度问题

---

# 整数均摊贪心问题



## 平均值最小总和

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class091/Code04_SplitMinimumAverageSum.java)



## 题目要点解析



---

# 小船过河贪心问题



## 过河问题

[题目链接](https://www.luogu.com.cn/problem/P1809)



## 题目要点解析



---

# 樵夫伐木贪心问题



## 砍树问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class094/Code05_CuttingTree.java)



## 题目要点解析



## 烹调方案

[题目链接](https://www.luogu.com.cn/problem/P1417)



## 题目要点解析



---

# 田忌赛马贪心问题

解锁任务型贪心

## 简单的田忌赛马

[题目链接](https://www.luogu.com.cn/problem/B3928)



## 题目要点解析



## 复杂的田忌赛马

[题目链接](https://www.luogu.com.cn/problem/P1650)



## 题目要点解析



## 最新版田忌赛马

[题目链接](https://ac.nowcoder.com/acm/contest/119605/D)



## 题目要点解析



## IPO问题

[题目链接](https://leetcode.cn/problems/ipo/description/)



## 题目要点解析



## 最低的加油次数

[题目链接](https://leetcode.cn/problems/minimum-number-of-refueling-stops/description/)



## 题目要点解析



---

# 建筑抢修贪心问题

经典反悔贪心之一

---

# 参考文献列表

1. [【CSDN 博客】贪心算法之区间问题](https://blog.csdn.net/2301_79248256/article/details/155039748)

2. [【Luoge 题单】贪心算法专项训练](https://www.luogu.com.cn/training/5199)

3. [【Luoge 题单】反悔贪心相关问题合集](https://www.luogu.com.cn/training/440831#problems)