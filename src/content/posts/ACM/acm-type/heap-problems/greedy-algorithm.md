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

## 国王的奖赏游戏

[题目链接](https://www.luogu.com.cn/problem/P1080)



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

### Sample Input

```txt showLineNumbers=false
3
2 2
3 1
1 3
```

### Sample Output

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



## 最大异或和问题

[题目链接](https://codeforces.com/gym/675909/problem/K)



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

### Sample Input

```txt showLineNumbers=false
12
```

### Sample Output

```txt showLineNumbers=false
81
```

## 题目要点解析



## 拆分的最大乘积

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class090/Code02_MaximumProduct.java)

### Problem Statement

给定一个正整数 $n$ ，将其拆分为 **恰好 k 个** 正整数，使得这 $k$ 个整数的乘积最大。

由于结果可能非常大，请将最终结果对 $10^9 + 7$ 取模。

### Constraints

- $1 \leq k \leq n \leq 10^{12}$

### Input

输入仅包含一行：

> $n \quad k$

### Output

输出一个整数，表示最大乘积对 $10^9 + 7$ 取模后的值。

## 题目要点解析



---

# 整数均摊贪心问题



## 平均值最小总和

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class091/Code04_SplitMinimumAverageSum.java)

### Problem Statement

给定一个长度为 $n$ 的数组 `arr` 和一个正整数 $k$ 。现需要将 `arr` 划分为 $k$ 个集合，使得数组中的每个数字恰好进入一个集合。

请计算并返回这 $k$ 个集合各自平均值的累加和的最小值。每个集合的平均值计算方式为：该集合内所有元素的总和除以元素个数，结果 **向下取整** 。

### Constraints

- $1 \leq n \leq 10^5$
- $0 \leq arr[i] \leq 10^5$
- $1 \leq k \leq n$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ ，分别表示数组长度和需要划分的集合数量。
- 第二行包含 $n$ 个整数，表示数组 $arr$ 中的元素。

> $n \quad k$
> 
> $arr_1 \quad arr_2 \quad \ldots \quad arr_n$

### Output

输出一个整数，表示所有集合平均值累加和的最小值。

## 题目要点解析



---

# 小船过河贪心问题



## 双人船渡河问题

[题目链接](https://www.luogu.com.cn/problem/P1809)

### Problem Statement

在月黑风高的夜晚，$n$ 个人来到河边，准备借助仅有的一盏灯过河。由于河水湍急，每次最多只能有两人同时过河，且过河时必须携带灯。

已知每个人单独过河所需的时间，若两人同时过河，其所需时间取决于较慢的那个人。由于灯只有一盏，每次两人过河后，必须有一人将灯送回对岸，以便其他人过河。

请计算出全员过河所需的最短总时间。

### Constraints

- $1 \leq n \leq 10^5$
- 每个人的过河时间为不超过 $10^6$ 的正整数

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示总人数。
- 接下来 $n$ 行，每行包含一个整数，表示第 $i$ 个人过河所需的时间。

> $n$
> 
> $t_1$
> 
> $t_2$
> 
> $\ldots$
> 
> $t_n$

### Output

输出一个整数表示答案。

### Sample Input

```txt showLineNumbers=false
4
1
2
5
10
```

### Sample Output

```txt showLineNumbers=false
17
```

## 题目要点解析



---

# 樵夫伐木贪心问题



## 梦幻城的黄金树

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class094/Code05_CuttingTree.java)

### Problem Statement

在梦幻城市中有 $n$ 棵黄金树，每棵树每天都会结出金子。已知第 $i$ 棵树初始时已有 $a_i$ 个金币，且每天会新长出 $b_i$ 个金币。

JAVAMAN 准备在梦幻城市停留 $m$ 天，每天他只能选择砍掉一棵树并获得该树上所有的金币。需要注意的是，如果某一天他不砍树，那么在那之后的日子里他也无法再砍树。

请计算他在 $m$ 天内最多可以获得的金币总数。

### Constraints

- $1 \leq T \leq 200$
- $1 \leq m \leq n \leq 250$
- $1 \leq a_i \leq 1000$
- $1 \leq b_i \leq 1000$

### Input

输入包含多个测试用例：

- 第一行包含一个整数 $T$ ，表示测试用例的数量。
- 对于每个测试用例：

  - 第一行包含两个整数 $n$ 和 $m$ 。
  - 第二行包含 $n$ 个整数，表示每棵树初始的金币数 $a_i$ 。
  - 第三行包含 $n$ 个整数，表示每棵树每天增长的金币数 $b_i$ 。

> $T$
> 
> $n \quad m$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $b_1 \quad b_2 \quad \ldots \quad b_n$

### Output

输出一个整数，表示最多可以获得的金币总数。

### Sample Input

```txt showLineNumbers=false
2
2 1
10 10
1 1
2 2
8 10
2 3
```

### Sample Output

```txt showLineNumbers=false
10
21
```

## 题目要点解析



## 最优的烹调方案

[题目链接](https://www.luogu.com.cn/problem/P1417)

### Problem Statement

由于美食节将至，店主希望在 $t$ 时间内做出一些美味佳肴。现有 $n$ 件食材，每件食材有三个属性：$a_i$、$b_i$ 和 $c_i$ 。

如果在第 $j$ 时刻完成第 $i$ 件食材的烹调，可以获得的美味度为：

$$
a_i - j \times b_i
$$

每件食材烹调所需的时间为 $c_i$ 。请问如何安排烹调顺序，才能使获得的美味度总和最大。

### Constraints

- $1 \leq n \leq 50$
- $1 \leq t \leq 10^5$
- $1 \leq a_i, b_i, c_i \leq 10^5$

### Input

输入包含四行：

- 第一行包含两个整数 $t$ 和 $n$ 。
- 第二行包含 $n$ 个整数，表示 $a_1, a_2, \ldots, a_n$ 。
- 第三行包含 $n$ 个整数，表示 $b_1, b_2, \ldots, b_n$ 。
- 第四行包含 $n$ 个整数，表示 $c_1, c_2, \ldots, c_n$ 。

> $t \quad n$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $b_1 \quad b_2 \quad \ldots \quad b_n$
> 
> $c_1 \quad c_2 \quad \ldots \quad c_n$

### Output

输出一个整数，表示最大美味度总和。

### Sample Input

```txt showLineNumbers=false
74 1
502
2
47
```

### Sample Output

```txt showLineNumbers=false
408
```

## 题目要点解析



## 我们一起来打CF

[题目链接](https://www.luogu.com.cn/article/aqjndtsb)



## 题目要点解析



---

# 田忌赛马贪心问题

解锁任务型贪心

## 复杂版田忌赛马

[题目链接](https://www.luogu.com.cn/problem/P1650)

### Problem Statement

中国古代的历史上，齐王和田忌赛马的故事家喻户晓。齐王和田忌各有 $N$ 匹马，每匹马都有一个固定的速度值。

比赛规则如下：

- 每一轮双方各出一匹马进行比赛，每匹马只能使用一次，直到 $N$ 匹马全部赛完。
- 在一轮比赛中，如果田忌的马速度大于齐王的马，田忌获胜，得 $200$ 银币。
- 如果田忌的马速度小于齐王的马，田忌失败，扣除 $200$ 银币。
- 如果两匹马速度相等，则是平局，不奖励也不扣除银币。

田忌已知齐王出马的顺序。请你通过合理安排田忌出马的顺序，使得田忌最终能获得的银币总数最大。

### Constraints

- $1 \leq N \leq 2000$
- 马的速度不超过 $1000$

### Input

输入包含三行：

- 第一行包含一个整数 $N$ ，表示马的数量。
- 第二行包含 $N$ 个整数，表示田忌的 $N$ 匹马的速度。
- 第三行包含 $N$ 个整数，表示齐王的 $N$ 匹马的速度。

> $N$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_N$
> 
> $b_1 \quad b_2 \quad \ldots \quad b_N$

### Output

输出一个整数，表示田忌能获得的最大银币数。

### Sample Input 1

```txt showLineNumbers=false
3
92 83 71
95 87 74
```

### Sample Output 1

```txt showLineNumbers=false
200
```

### Sample Input 2

```txt showLineNumbers=false
2
20 20
20 20
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析



## 最新版田忌赛马

[题目链接](https://ac.nowcoder.com/acm/contest/119605/D)

### Problem Statement

田忌与齐王再次进行赛马比赛。这次比赛规则有所不同，田忌需要通过合理安排马匹的对阵顺序，最大化自己的赏金收益。

田忌有 $n$ 匹马，第 $i$ 匹马的速度为 $a_i$ ；齐王有 $m$ 匹马，第 $i$ 匹马的速度为 $b_i$ 。由于田忌对自己和齐王的马匹了如指掌，他知道他和齐王的马都是按速度降序排列的。

每次比赛，田忌可以选择自己的一匹从未出战的马 $i$ 与齐王的一匹从未出战的马 $j$ 进行比赛：

- 如果田忌的马速度严格大于齐王的马，田忌将获得 $b_j$ 的赏金。
- 如果田忌的马速度小于或等于齐王的马，田忌不会获得赏金。

你需要计算田忌能够获得的 **最大** 赏金总额。

### Constraints

- $1 \leq n, m \leq 5 \times 10^5$
- $1 \leq a_i, b_i \leq 10^9$
- 数组 $a$ 和 $b$ 均已按 **升序** 排列

### Input

输入包含三行：

- 第一行包含两个整数 $n$ 和 $m$ ，分别表示田忌和齐王的马匹数量。
- 第二行包含 $n$ 个整数，表示田忌各匹马的速度。
- 第三行包含 $m$ 个整数，表示齐王各匹马的速度。

> $n \quad m$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $b_1 \quad b_2 \quad \ldots \quad b_m$

### Output

输出一个整数，表示田忌能够获得的最大赏金总额。

### Sample Input 1

```txt showLineNumbers=false
2 2
3 1
4 2
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
3 3
11 10 7
10 9 8
```

### Sample Output 2

```txt showLineNumbers=false
19
```

### Sample Input 3

```txt showLineNumbers=false
6 7
6 5 4 3 2 1
7 6 5 4 3 2 1
```

### Sample Output 3

```txt showLineNumbers=false
15
```

## 题目要点解析



## 加强版田忌赛马

[题目链接](https://ac.nowcoder.com/acm/contest/119605/E)

### Problem Statement

田忌与齐王再次进行赛马比赛。这次比赛规则有所不同，田忌需要通过合理安排马匹的对阵顺序，最大化自己的赏金收益。

田忌有 $n$ 匹马，第 $i$ 匹马的速度为 $a_i$ ；齐王有 $m$ 匹马，第 $i$ 匹马的速度为 $b_i$ 。由于田忌对自己和齐王的马匹了如指掌，他知道他和齐王的马都是按速度降序排列的。

每次比赛，田忌可以选择自己的一匹从未出战的马 $i$ 与齐王的一匹从未出战的马 $j$ 进行比赛：

- 如果田忌的马速度严格大于齐王的马，田忌将获得 $b_j$ 的赏金。
- 如果田忌的马速度小于或等于齐王的马，田忌不会获得赏金。

你需要计算田忌能够获得的 **最大** 赏金总额，以及有多少种 **本质不同** 的对阵方案可以获得该最大赏金总额。

两种对阵策略被称为本质不同的，当且仅当其中一个对阵策略中，存在某个田忌的马 $i$ 与齐王的马 $j$ 比赛，而另一个对阵策略中，田忌的马 $i$ 不与齐王的马 $j$ 比赛。

由于对阵策略种类数可能很多，对阵策略种类数只需要计算对 $998244353$ 取模后的答案，但是注意不要对最大赏金总额取模。

注意：你不需要最大化比赛数量，不进行任何比赛也是对阵策略的一种。

### Constraints

- $1 \leq n, m \leq 5 \times 10^5$
- $1 \leq a_i, b_i \leq 10^9$
- 数组 $a$ 和 $b$ 均已按 **降序** 排列

### Input

输入包含三行：

- 第一行包含两个整数 $n$ 和 $m$ ，分别表示田忌和齐王的马匹数量。
- 第二行包含 $n$ 个整数，表示田忌各匹马的速度。
- 第三行包含 $m$ 个整数，表示齐王各匹马的速度。

> $n \quad m$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $b_1 \quad b_2 \quad \ldots \quad b_m$

### Output

输出两个整数，第一个整数表示田忌能够获得的最大赏金总额，第二个整数表示有多少种本质不同的对阵策略可以获得该最大赏金总额，其中对阵策略种类数需要对 $998244353$ 取模。

### Sample Input

```txt showLineNumbers=false
2 2
3 1
4 2
```

### Sample Output

```txt showLineNumbers=false
2 2
```

## 题目要点解析



## 大规模募资问题

[题目链接](https://leetcode.cn/problems/ipo/description/)

### Problem Statement

假设 LeetCode 即将开始 IPO。为了以更高的价格将股票卖给风险投资公司，LeetCode 希望在 IPO 之前开展一些项目以增加其资本。由于资源有限，它只能在 IPO 之前完成最多 $k$ 个不同的项目。帮助 LeetCode 设计完成最多 $k$ 个指定的项目后，可获得的最大总资本。

给你 $n$ 个项目。对于每个项目 $i$ ，它都有一个纯利润 $profits[i]$ ，和启动该项目需要的最小资本 $capital[i]$ 。

最初，你的资本为 $w$ 。当你完成一个项目时，你将获得纯利润，且利润将被添加到你的总资本中。

总而言之，从给定项目中选择最多 $k$ 个不同项目的列表，以 **最大化最终资本** ，并输出最终可获得的最多资本。

### Constraints

- $1 \leq k \leq 10^5$
- $0 \leq w \leq 10^9$
- $n == profits.length$
- $n == capital.length$
- $1 \leq n \leq 10^5$
- $0 \leq profits[i] \leq 10^4$
- $0 \leq capital[i] \leq 10^9$

### Input

输入包含四行：

- 第一行包含两个整数 $n$ 和 $k$ ，分别表示项目的数量和最多可选择的项目数量。
- 第二行包含一个整数 $w$ ，表示初始资本。
- 第三行包含 $n$ 个整数，表示每个项目的纯利润 $profits$ 。
- 第四行包含 $n$ 个整数，表示每个项目启动所需的最小资本 $capital$ 。

> $n \quad k$
> 
> $w$
> 
> $profits_1 \quad profits_2 \quad \ldots \quad profits_n$
> 
> $capital_1 \quad capital_2 \quad \ldots \quad capital_n$

### Output

输出一个整数，表示最终可获得的最大总资本。

### Sample Input 1

```txt showLineNumbers=false
3 2
0
1 2 3
0 1 1
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
3 3
0
1 2 3
0 1 2
```

### Sample Output 2

```txt showLineNumbers=false
6
```

## 题目要点解析



## 最低的加油次数

[题目链接](https://leetcode.cn/problems/minimum-number-of-refueling-stops/description/)

### Problem Statement

汽车从起点出发驶向目的地，该目的地位于距起点 `target` 英里处。

沿途有若干个加油站，每个 `station[i]` 代表一个加油站，它位于距起点 $station[i][0]$ 英里处，并且有 $station[i][1]$ 升汽油。

假设汽车离起点距离无限远且油箱容量无限大，初始时燃料为 `startFuel` 升。它每行驶 $1$ 英里就会用掉 $1$ 升汽油。当汽车到达一个加油站时，它可能停下来加油，将加油站所有的汽油都装入油箱。

为了到达目的地，汽车最少需要加油多少次？如果无法到达目的地，则返回 $-1$ 。

注意：如果汽车到达目的地时剩余燃料为 $0$ ，它仍然被视为到达了目的地。如果它到达加油站时剩余燃料为 $0$ ，它仍然可以在该加油站加油。

### Constraints

- $1 \leq target, startFuel \leq 10^9$
- $0 \leq stations.length \leq 500$
- $0 < station[i][0] < station[i+1][0] < target$
- $1 \leq station[i][1] \leq 10^9$

### Input

输入包含多行：

- 第一行包含两个整数 $target$ 和 $startFuel$ ，分别表示目的地的距离和初始燃料量。
- 第二行包含一个整数 $N$ ，表示加油站的数量。
- 接下来 $N$ 行，每行包含两个整数 $dist_i$ 和 $fuel_i$ ，表示第 $i$ 个加油站距离起点的距离和拥有的燃料量。

> $target \quad startFuel$
> 
> $N$
> 
> $dist_1 \quad fuel_1$
> 
> $dist_2 \quad fuel_2$
> 
> $\ldots$
> 
> $dist_N \quad fuel_N$

### Output

输出一个整数，表示最少需要的加油次数。如果无法到达，输出 `-1` 。

### Sample Input 1

```txt showLineNumbers=false
100 1
1
10 100
```

### Sample Output 1

```txt showLineNumbers=false
-1
```

### Sample Input 2

```txt showLineNumbers=false
100 10
4
10 60
20 30
30 30
60 40
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析



---

# 数组同化贪心问题

中位数贪心相关

[中位数贪心及其证明](https://zhuanlan.zhihu.com/p/1922938031687595039)

## 使数组元素相等

[题目链接](https://leetcode.cn/problems/minimum-moves-to-equal-array-elements-ii/description/)



## 题目要点解析



## 构造模交替数组

[题目链接](https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-i/description/)



## 题目要点解析



---

# 建筑抢修贪心问题

经典反悔贪心之一

## 建筑抢修小游戏

[题目链接](https://www.luogu.com.cn/problem/P4053)

### Problem Statement

小修正在赶往一些建筑进行抢修。由于建筑物的受损程度不同，抢修每个建筑所需的时间以及该建筑能够支撑的最晚抢修时间也各不相同。

具体而言，第 $i$ 个建筑抢修需要花费的时间为 $T_1$ ，而它在 $T_2$ 时刻之后就会倒塌。如果小修决定抢修某个建筑，他必须在 **该建筑倒塌之前** 完成抢修。

小修从 $0$ 时刻出发，每次只能抢修一个建筑。请你帮助小修进行规划，使得他能够抢修的建筑数量最多。

### Constraints

- $1 \leq N \leq 1.5 \times 10^5$
- $1 \leq T_1 \leq T_2 < 2^{31}$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ ，表示建筑的数量。
- 接下来 $N$ 行，每行包含两个整数 $T_1$ 和 $T_2$ ，分别表示抢修该建筑需要的时间和该建筑的最晚倒塌时间。

> $N$
> 
> $T_{1,1} \quad T_{2,1}$
> 
> $T_{1,2} \quad T_{2,2}$
> 
> $\ldots$
> 
> $T_{1,N} \quad T_{2,N}$

### Output

输出一个整数，表示最多可以抢修的建筑数量。

### Sample Input 1

```txt showLineNumbers=false
4
100 200
200 1300
1000 1250
2000 3200
```

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点解析



---

# 城市绿化贪心问题



## 复杂的种树问题

[题目链接](https://www.luogu.com.cn/problem/P1792)

### Problem Statement

在一条环形街道旁共有 $N$ 棵树。为了美化环境，需要在其中选择 $M$ 棵树种上装饰物。

种树需要遵守以下规则：

- 任意两棵相邻的树不能同时被种上装饰物。
- 由于是环形街道，第 $1$ 棵树与第 $N$ 棵树被视为相邻。
- 每棵树都有一个美观度 $a_i$ ，你的目标是使得选出的 $M$ 棵树的总美观度最大。

如果无法按照规则种下 $M$ 棵树，则输出 `Error!` 。

### Constraints

- $1 \leq N \leq 2 \times 10^5$
- $1 \leq M \leq N$
- $-1000 \leq a_i \leq 1000$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $M$ ，分别表示树的总数和需要种装饰物的树的数量。
- 第二行包含 $N$ 个整数，表示每棵树的美观度。

> $N \quad M$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_N$

### Output

输出一个整数，表示最大总美观度。如果方案不存在，输出 `Error!` 。

### Sample Input 1

```txt showLineNumbers=false
7 3
1 2 3 4 5 6 7
```

### Sample Output 1

```txt showLineNumbers=false
15
```

### Sample Input 2

```txt showLineNumbers=false
7 4
1 2 3 4 5 6 7
```

### Sample Output 2

```txt showLineNumbers=false
Error!
```

## 题目要点解析



---

# 参考文献列表

1. [【CSDN 博客】贪心算法之区间问题](https://blog.csdn.net/2301_79248256/article/details/155039748)

2. [【Luogu 博客】反悔贪心的再理解](https://www.luogu.com.cn/article/hwrxooq5)

3. [【wshcl】反悔贪心相关题目收集](https://www.cnblogs.com/wshcl/p/18712932)