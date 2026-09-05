---
title: 【ACM 算法随笔】动态规划的入门导论
published: 2026-02-26
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: false
---

> 写在前面：本篇博客写作灵感来源于 N 神的动态规划概述

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114531325973175&bvid=BV1m9EUzLEB4&cid=30031939563&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 动态规划状态设计

动态规划中最困难的部分往往并不是状态转移本身，而是如何从题目中 **提炼出真正有价值的信息** ，并据此完成状态设计。很多动态规划题目虽然背景各不相同，但题目中的某些 **关键信息** 往往会直接决定状态应该如何定义，以及整个问题适合采用怎样的建模方式，而能否快速识别这些特征，通常也是解决问题的关键。

在实际做题过程中，很多动态规划并不是从零开始凭空设计状态，而是先从题目描述中 **提取关键条件** ，再将问题转化为对应的经典模型。不同的题面往往会对应不同的 **建模套路** ，有些问题需要重新定义阶段，有些问题需要改变状态表示方式，还有些问题则需要通过 **等价转换** 来简化状态之间的关系。因此掌握动态规划不仅需要理解状态转移，更重要的是积累常见模型与建模技巧，并学会根据题目特征快速完成状态设计。

## 最小贿赂金币数

[题目链接](https://www.nowcoder.com/practice/736e12861f9746ab8ae064d4aae2d5a9)

### Problem Statement

你正在面对 $n$ 只怪兽，必须按 **从左到右** 的顺序依次通过。每只怪兽有两个属性：能力值 $a_i$ 和贿赂它所需的钱数 $b_i$ 。开始时你的能力为 $0$ 。

对于每一只怪兽，你的通过规则如下：

- **必须贿赂**：如果你当前的能力 **小于** $i$ 号怪兽的能力，则你必须付出 $b_i$ 的钱贿赂这只怪兽。
- **可以选择贿赂**：如果你当前的能力 **大于等于** $i$ 号怪兽的能力，你可以选择直接通过（不花钱，能力不增加），也可以选择依然付出 $b_i$ 的钱贿赂这只怪兽。
- **贿赂的效果**：如果你贿赂了怪兽，怪兽会加入你的队伍，其能力 $a_i$ 会直接累加到你的当前能力上。

你的目标是按顺序通过所有 $n$ 只怪兽。请计算通关所需的 **最小钱数** 。

### Constraints

- $1 \leq n \leq 1000$
- $1 \leq a_i \leq 10^4$
- $1 \leq b_i \leq 10$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示怪兽的数量。
- 接下来 $n$ 行，每行包含两个整数 $a_i$ 和 $b_i$ 。

> $n$
> 
> $a_1 \quad b_1$
> 
> $a_2 \quad b_2$
> 
> $\ldots$
> 
> $a_n \quad b_n$

### Output

输出一个整数，表示通关所需的最小钱数。

### Sample Input

```txt showLineNumbers=false
2
8 10
6 5
```

### Sample Output

```txt showLineNumbers=false
10
```

## 题目要点解析

动态规划的核心挑战在于如何设计一个既能涵盖所有必要决策信息，又能在时空复杂度限制内运行的状态表示。针对本题，如果按照常规思维，将 **当前积累的能力值** 作为 DP 的一个维度（即定义 $dp[i][j]$ 为面对前 $i$ 只怪兽、当前能力为 $j$ 时的最小花费），会直接面临复杂度过高的问题。由于单只怪兽的能力值 $a_i$ 最高可达 $10^4$ ，总能力上限在 $10^7$ 数量级，这种设计会产生巨大的状态空间，从而造成严重的内存溢出。

为了优化模型，我们可以利用 **维度转置** 的思想，将状态维度与数值角色互换，转而定义 **$dp[j]$ 为花费恰好 j 元钱时所能积累的最大能力值** 。由于题目中总花费的上限可控，该维度的空间开销非常理想。在此框架下，判定能否通过某只怪兽的标准从原本求解最小钱数转变为验证在给定花费下所能达到的最大能力是否足以覆盖怪兽防御力，这种转换直接摒弃了对原始庞大能力空间的直接枚举，转而将求解重心转移至取值更小且可控的花费维度。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 1005;
const int MAXM = 10005;
const ll INF = 0xcfcfcfcfcfcfcfcfLL;
ll dp[MAXN][MAXM];

int main() {
    int n; cin >> n;

    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= 10 * n; j++) {
            dp[i][j] = INF;
        }
    }
    dp[0][0] = 0;

    for (int i = 1; i <= n; i++) {
        ll a; int b;
        cin >> a >> b;
        for (int j = 0; j <= 10 * n; j++) {
            if (j >= b && dp[i - 1][j - b] != INF) {
                dp[i][j] = max(dp[i][j], dp[i - 1][j - b] + a);
            }

            if (dp[i - 1][j] >= a) {
                dp[i][j] = max(dp[i][j], dp[i - 1][j]);
            }
        }
    }

    for (int j = 0; j <= 10 * n; j++) {
        if (dp[n][j] >= 0) {
            cout << j << endl;
            break;
        }
    }
}
```

## 最少的跳跃能力

[题目链接](https://www.luogu.com.cn/problem/P8775)

### Problem Statement

小青蛙库睿奇要过河去参加派对。河的宽度为 $n$ ，河上分布着 $n-1$ 块石头，第 $i$ 块石头距离河左岸的距离为 $i$ ，其高度为 $h_i$ 。由于高度限制，每块石头最多只能被踩 $h_i$ 次。

库睿奇准备从左岸跳到右岸，再从右岸跳回左岸，如此往返共 $2x$ 次（即 $x$ 次从左往右，$x$ 次从右往左）。

在跳跃过程中，库睿奇的能力值为 $y$ ，这意味着它每次跳跃的距离 **不能超过** $y$ 。请计算库睿奇能够完成 $2x$ 次跳跃所需的 **最小能力值 y** 。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq x \leq 10^9$
- $1 \leq h_i \leq 10^9$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $x$ ，分别表示河的宽度和往返的总次数。
- 第二行包含 $n-1$ 个整数 $h_1, h_2, \ldots, h_{n-1}$ ，表示每块石头的高度。

> $n \quad x$
> 
> $h_1 \quad h_2 \quad \ldots \quad h_{n-1}$

### Output

输出一个整数，表示要求的最小能力值 $y$ 。

### Sample Input

```txt showLineNumbers=false
5 1
1 0 1 0
```

### Sample Output

```txt showLineNumbers=false
4
```

## 题目要点解析

往返模型

## 往返摘樱桃难题

[题目链接](https://leetcode.cn/problems/cherry-pickup/description/)

### Problem Statement

一个 $n \times n$ 的网格 `grid` 代表棋盘，每个单元格内容可以是以下三种之一：

- `0`：表示该单元格是空的，可以穿过。
- `1`：表示该单元格包含一个樱桃，可以在经过时摘取。
- `-1`：表示该单元格包含一个障碍物，无法穿过。

你需要执行以下操作：

1. 从起点 $(0, 0)$ 出发，只能向 **右** 或向 **下** 移动，直到到达终点 $(n-1, n-1)$ 。
2. 在经过包含樱桃的单元格时，摘取樱桃，该单元格随后变为 `0` 。
3. 到达 $(n-1, n-1)$ 后，从该点出发，只能向 **左** 或向 **上** 移动，直到回到起点 $(0, 0)$ 。
4. 同样，在回程经过包含樱桃的单元格时，摘取樱桃（如果第一次经过时已经摘取，则此处为 `0` ）。

请计算你最多能摘取的樱桃数。如果不存在一条合法的路径，则返回 $0$ 。

### Constraints

- $n == grid.length$
- $n == grid[i].length$
- $1 \leq n \leq 50$
- $grid[i][j]$ 为 $-1, 0, 1$
- $grid[0][0] \neq -1$
- $grid[n-1][n-1] \neq -1$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示网格的大小。
- 接下来 $n$ 行，每行 $n$ 个整数，表示网格数组 $grid_{i,j}$ 。

> $n$
> 
> $grid_{1,1} \quad grid_{1,2} \quad \ldots \quad grid_{1,n}$
> 
> $\dots$
> 
> $grid_{n,1} \quad grid_{n,2} \quad \ldots \quad grid_{n,n}$

### Output

输出一个整数，表示最多能摘取的樱桃总数。

### Sample Input

```txt showLineNumbers=false
3
0 1 -1
1 0 -1
1 1 1
```

### Sample Output

```txt showLineNumbers=false
5
```

## 题目要点解析

往返+曼哈顿旋转

## 过河所需石子数

[题目链接](https://www.luogu.com.cn/problem/P1052)

### Problem Statement

在河上有一座独木桥，长度为 $L$ 。桥上分布着 $M$ 颗石子，每颗石子所在的坐标都是 $1$ 到 $L-1$ 之间的整数。青蛙库里奇准备从桥的起点（坐标 $0$ ）跳到桥的终点（坐标 $L$ 或更远的地方）。库里奇每次跳跃的距离是 $[S, T]$ 之间的任意整数。

在跳跃过程中，如果库里奇落下的位置刚好有一颗石子，它就会踩到这颗石子。库里奇希望在顺利过河的前提下，**踩到的石子数量最少** 。请计算出库里奇过河所需踩到的最少石子数。

### Constraints

- $1 \leq L \leq 10^9$
- $1 \leq S \leq T \leq 10$
- $1 \leq M \leq 100$
- 石子坐标在 $(0, L)$ 范围内

### Input

输入包含三行：

- 第一行包含一个整数 $L$ ，表示桥的长度。
- 第二行包含三个整数 $S$ 、$T$ 和 $M$ 。
- 第三行包含 $M$ 个整数，表示桥上每颗石子的坐标。

> $L$
> 
> $S \quad T \quad M$
> 
> $x_1 \quad x_2 \quad \ldots \quad x_M$

### Output

输出一个整数，表示最少踩到的石子数。

### Sample Input

```txt showLineNumbers=false
10
2 3 5
2 3 5 6 7
```

### Sample Output

```txt showLineNumbers=false
2
```

## 题目要点解析



---

# 参考文献列表

1. [【james1BadCreeper】动态规划的状态设计](https://james1badcreeper.github.io/bb10c5df/#Problemset)

2. [【Tuifei_oier】状态的设计与简化](https://www.cnblogs.com/tuifei-oiers-home/p/14226145.html)