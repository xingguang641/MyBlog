---
title: 【ACM 算法随笔】动态规划思想
published: 2026-02-26
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: true
---

> 写在前面：本篇博客写作灵感来源于 N 神的动态规划概述

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114531325973175&bvid=BV1m9EUzLEB4&cid=30031939563&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 动态规划递归转化

从算法建模的角度看，**绝大多数动态规划问题在本质上都可以通过递归形式进行刻画** 。递归的核心价值在于清晰地定义了问题的 **最优子结构**：即一个规模为 $n$ 的复杂问题，其最优解能够被分解为若干规模更小的子问题解的组合。因此优先以 **递归视角** 明确状态的定义及其相互依赖关系，是揭示问题底层逻辑最直观的途径。

虽然朴素递归能完整描述求解逻辑，但其最大的弊端在于产生大量的 **重复子问题** 。在递归树的展开过程中，不同分支往往会多次触达完全相同的状态。当状态空间有限且计算结果具有确定性时，我们可以引入缓存机制，即 **记忆化搜索（Memoization）**。通过记录已求解状态的结果，计算效率可以实现从指数级到多项式级的质变。在这个意义上，记忆化搜索正是 **自顶向下** 实现动态规划的核心手段。

## 一年的火车旅行

[题目链接](https://leetcode.cn/problems/minimum-cost-for-tickets/description/)

### Problem Statement

在一个火车旅行很受欢迎的国度，你提前一年计划了一些火车旅行。在接下来的一年里，日历第 `days[i]` 天是你将会进行旅行的日子。这些天数按 **升序** 给出。

火车票有 **三种不同的销售方式** ：

1.  **1 天通行证** ：售价为 `costs[0]` 美元，允许你在 1 天内不限次数地乘坐火车。
2.  **7 天通行证** ：售价为 `costs[1]` 美元，允许你在 7 天内（包含开始的那天）不限次数地乘坐火车。
3.  **30 天通行证** ：售价为 `costs[2]` 美元，允许你在 30 天内（包含开始的那天）不限次数地乘坐火车。

返回你想要完成所有计划日期内旅行所需的 **最低消费** 。

### Constraints

- $1 \leq days.length \leq 365$
- $1 \leq days[i] \leq 365$
- $days$ 按 **升序** 排列
- $costs.length == 3$
- $1 \leq costs[i] \leq 1000$

### Input

输入包含两行：

- 第一行包含若干个整数，表示计划旅行的日子。
- 第二行包含三个整数，表示三种通行证的价格。

> $days_1 \quad days_2 \quad \ldots \quad days_n$
> 
> $costs_0 \quad costs_1 \quad costs_2$

### Output

输出包含一个整数，表示最低花费。

### Sample Input 1

```txt showLineNumbers=false
1 4 6 7 8 20
2 7 15
```

### Sample Output 1

```txt showLineNumbers=false
11
```

### Sample Input 2

```txt showLineNumbers=false
1 2 3 4 5 6 7 8 9 10 30 31
2 7 15
```

### Sample Output 2

```txt showLineNumbers=false
17
```

## 题目要点解析



## 简单的解码方法

[题目链接](https://leetcode.cn/problems/decode-ways/)

### Problem Statement

一条包含字母 `A-Z` 的消息通过以下映射进行了 **编码**：

- `'A' -> "1"`
- `'B' -> "2"`
- ...
- `'Z' -> "26"`

要 **解码** 已编码的消息，所有数字必须分组，然后按上述映射逆向映射回字母。例如 `"11106"` 可以映射为：

- `"AAJF"` ，将消息分组为 `(1, 1, 10, 6)`
- `"KJF"` ，将消息分组为 `(11, 10, 6)`

注意，消息不能分组为 `(1, 11, 06)` ，因为 `"06"` 不能映射为 `"F"` ，由于 `"6"` 和 `"06"` 在映射中是不同的。

给你一个只含数字的 **非空** 字符串 $s$ ，请计算并返回 **解码** 方法的 **总数** 。

题目数据保证答案肯定是一个 **32 位** 的整数。

### Constraints

- $1 \leq s.length \leq 100$
- $s$ 只包含数字，并且可能包含前导零

### Input

输入仅包含一行：

> $s$

### Output

输出包含一个整数，表示解码方法的总数。

### Sample Input 1

```txt showLineNumbers=false
12
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
226
```

### Sample Output 2

```txt showLineNumbers=false
3
```

### Sample Input 3

```txt showLineNumbers=false
06
```

### Sample Output 3

```txt showLineNumbers=false
0
```

## 题目要点解析



## 困难的解码方式

[题目链接](https://leetcode.cn/problems/decode-ways-ii/)

### Problem Statement

一条包含字母 `A-Z` 的消息通过以下映射进行了 **编码**：

- `'A' -> "1"`
- `'B' -> "2"`
- ...
- `'Z' -> "26"`

除了数字之外，已编码的消息还可以包含 `'*'` 字符，该字符可以表示从 `'1'` 到 `'9'` 的任意数字。例如，`"1*"` 可以表示从 `"11"` 到 `"19"` 的任何编码消息。

要 **解码** 一条消息，所有数字必须分组，然后按上述映射逆向映射回字母。

给你一个字符串 $s$ ，由数字和 `'*'` 字符组成，返回 **解码** 该消息的 **总数** 。

由于答案可能会非常大，所以必须对 $10^9 + 7$ 取模。

### Constraints

- $1 \leq s.length \leq 10^5$
- $s[i]$ 是数字或 `'*'`

### Input

输入仅包含一行：

> $s$

### Output

输出包含一个整数，表示解码方法的总数对 $10^9 + 7$ 取模后的结果。

### Sample Input 1

```txt showLineNumbers=false
*
```

### Sample Output 1

```txt showLineNumbers=false
9
```

### Sample Input 2

```txt showLineNumbers=false
1*
```

### Sample Output 2

```txt showLineNumbers=false
18
```

### Sample Input 3

```txt showLineNumbers=false
2*
```

### Sample Output 3

```txt showLineNumbers=false
15
```

## 题目要点解析



## 骑士的存活概率

[题目链接](https://leetcode.cn/problems/knight-probability-in-chessboard/)

### Problem Statement

在一个 $n \times n$ 的国际象棋棋盘上，一个骑士从单元格 $(row, column)$ 开始，并尝试进行 $k$ 次移动。行和列从 **0** 开始计数，所以左上角的单元格为 $(0, 0)$，右下角的单元格为 $(n-1, n-1)$。

象棋骑士有 $8$ 种可能的移动方式。每次移动在 $L$ 形方向上前进：选择一个方向（上下左右）走 2 格，然后垂直于该方向走 $1$ 格。每当骑士需要移动时，它会从 $8$ 种可能的移动中 **等概率** 地选择一种（即使棋子移动后会离开棋盘），然后移动到那里。

骑士继续移动，直到它完成了 $k$ 次移动或跳出了棋盘。返回骑士在完成 $k$ 次移动后仍留在棋盘上的 **概率** 。

### Constraints

- $1 \leq n \leq 25$
- $0 \leq k \leq 100$
- $0 \leq row, column \leq n - 1$

### Input

输入包含三行：

- 第一行包含一个整数 $n$ ，表示棋盘的边长。
- 第二行包含一个整数 $k$ ，表示骑士的移动次数。
- 第三行包含两个整数 $row$ 和 $column$ ，表示骑士的起始位置。

> $n$
> 
> $k$
> 
> $row \quad column$

### Output

输出一个浮点数，表示骑士最终仍停留在棋盘上的概率。

### Sample Input 1

```txt showLineNumbers=false
3
2
0 0
```

### Sample Output 1

```txt showLineNumbers=false
0.06250
```

### Sample Input 2

```txt showLineNumbers=false
1
0
0 0
```

### Sample Output 2

```txt showLineNumbers=false
1.00000
```

## 题目要点解析



---

# 动态规划建模技巧

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

# 动态规划经典重构

动态规划的精髓在于通过 **状态划分** 与 **递推关系** 刻画子问题的依赖结构。在入门实践中，将问题归类为背包、区间或树形等 **经典模型** 是构建建模思维的基础。然而在竞赛算法的学习中，我们经常会遇到一类题目：它们虽然在表象上与经典模型高度相似，但数据规模却大幅超出了经典范式的承载极限。面对这种显著的数据规模差异，经典算法直接失效，这就要求我们必须跨越模板的思维定式，深入剖析题目本质。

处理此类难题的关键在于寻找经典模型之外的 **特殊限制** ，并将这些特殊限制作为突破口。当数据规模超出常规算法的承载范围时，题目中通常包含额外的条件约束，例如 **极小的值域范围** ，或者将输入数组 **限定为排列** 。深入挖掘这些特性可以 **改变状态转移结构** ，进而对算法做出 **针对性的优化或重构** 。通过这些手段，原本难以承受的计算代价能够被降低到合理范围，确保算法在处理大规模数据时依然能够 **高效运行** 。

## 最长递增子排列

[题目链接](https://www.luogu.com.cn/problem/P1439)

### Problem Statement

给出两个长度为 $n$ 的排列 $P_1$ 和 $P_2$ ，计算它们的最长公共子序列的长度。

**排列** 是指 $1$ 到 $n$ 这 $n$ 个整数每个数恰好出现一次的序列。

### Constraints

- $1 \leq n \leq 10^5$
- $P_1, P_2$ 均为 $1$ 到 $n$ 的排列

### Input

输入包含三行：

- 第一行包含一个整数 $n$ ，表示排列的长度。
- 第二行包含 $n$ 个整数，表示排列 $P_1$ 。
- 第三行包含 $n$ 个整数，表示排列 $P_2$ 。

> $n$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $b_1 \quad b_2 \quad \ldots \quad b_n$

### Output

输出一个整数，表示最长公共子序列的长度。

### Sample Input

```txt showLineNumbers=false
5
3 2 1 4 5
1 2 3 4 5
```

### Sample Output

```txt showLineNumbers=false
3
```

## 题目要点解析

假最长公共子序列问题

## 使集合总和相近

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class087/Code02_PickNumbersClosedSum.java)

### Problem Statement

给定正整数 $n$ 和 $k$ ，你需要从 $1$ 到 $n$ 的整数中选择 $k$ 个数字组成集合 $A$ ，剩下的 $n-k$ 个数字组成集合 $B$ 。目标是使得集合 $A$ 中所有元素的累加和与集合 $B$ 中所有元素的累加和之差的绝对值不超过 $1$ 。

如果存在满足条件的方案，返回集合 $A$ 中所选的所有数字；如果无法做到，返回一个长度为 $0$ 的数组。

### Constraints

- $2 \leq n \leq 10^6$
- $1 \leq k \leq n$

### Input

输入仅包含一行：

> $n \quad k$

### Output

输出一行整数，表示集合 $A$ 中所选的所有数字。

## 题目要点解析

假01背包问题

## 最优的部署方案

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class128/Code02_BestDeploy1.java)

### Problem Statement

有 $n$ 台机器排成一排，编号为 $1$ 到 $n$。你需要依次部署这些机器，且可以自由决定部署的顺序，最终所有机器都需要被部署。

给定三个数组 `no[]`、`one[]` 和 `both[]`，对于每一台机器 $i$：

- `no[i]`：当第 $i$ 号机器部署时，如果其相邻的机器均未部署，此时获得的收益。
- `one[i]`：当第 $i$ 号机器部署时，如果其相邻的机器中恰有一台已部署，此时获得的收益。
- `both[i]`：当第 $i$ 号机器部署时，如果其相邻的机器中已有两台已部署，此时获得的收益。

注意：第 $1$ 号机器和第 $n$ 号机器在部署时，相邻的已部署机器最多只有一台。请计算并返回部署所有机器能获得的最大收益。

### Constraints

- $1 \leq n \leq 10^5$
- $0 \leq no[i], one[i], both[i] \leq 10^4$

### Input

输入包含四行：

- 第一行包含一个整数 $n$ 。
- 第二行包含 $n$ 个整数，表示 $no$ 数组。
- 第三行包含 $n$ 个整数，表示 $one$ 数组。
- 第四行包含 $n$ 个整数，表示 $both$ 数组。

> $n$
>
> $\text{no}_1 \quad \text{no}_2 \quad \ldots \quad \text{no}_n$
>
> $\text{one}_1 \quad \text{one}_2 \quad \ldots \quad \text{one}_n$
>
> $\text{both}_1 \quad \text{both}_2 \quad \ldots \quad \text{both}_n$

### Output

输出一个整数，表示部署所有机器能获得的最大收益。

## 题目要点解析

假区间dp问题

## 增加限制的最长公共子序列问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class128/Code03_AddLimitLcs.java)

### Problem Statement

给定两个只由小写字母组成的字符串 $s_1$ 和 $s_2$ ，其中 $s_1$ 的长度为 $n$ ，$s_2$ 的长度为 $m$ 。请计算并返回这两个字符串的 **最长公共子序列** 的长度。

### Constraints

- $1 \leq n \leq 10^6$
- $1 \leq m \leq 10^3$

### Input

输入包含两行：

- 第一行包含一个字符串 $s_1$ 。
- 第二行包含一个字符串 $s_2$ 。

> $s_1$
>
> $s_2$

### Output

输出一个整数，表示两个字符串的最长公共子序列长度。

## 题目要点解析

假最长公共子序列问题

## 树上最大异或和

[题目链接](https://www.luogu.com.cn/problem/P4551)

### Problem Statement

给定一棵 $n$ 个点的带权树，结点下标从 $1$ 开始到 $n$ 。求树中所有异或路径的最大值。

异或路径指树上两个结点之间唯一路径上的所有边权的异或值。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq u_i, v_i \leq n$
- $0 \leq w < 2^{31}$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示结点数。
- 接下来 $n - 1$ 行，每行包含三个整数 $u$ 、$v$ 和 $w$ 。

> $n$
>
> $u_1 \quad v_1 \quad w_1$
>
> $u_2 \quad v_2 \quad w_2$
>
> $\ldots$
>
> $u_{n-1} \quad v_{n-1} \quad w_{n-1}$

### Output

输出一个整数表示答案。

### Sample Input

```txt showLineNumbers=false
4
1 2 3
2 3 4
2 4 6
```

### Sample Output

```txt showLineNumbers=false
7
```

## 题目要点解析

假树型dp问题

---

# 参考文献列表

## 经典的DP分类

1. [【ACM 算法题单】背包动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/knapsack-dp/)

2. [【ACM 算法题单】区间动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/interval-dp/)

3. [【ACM 算法题单】树型动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)

4. [【ACM 算法题单】状压动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/state-dp/)

5. [【ACM 算法题单】数位动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/digit-dp/)

## 经典的DP问题

1. [【ACM 算法题单】子数组最大累加和问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/maximum-subarray-sum/)

2. [【ACM 算法题单】最长公共子序列问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/longest-common-subsequence/)

3. [【ACM 算法题单】最长递增子序列问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/longest-increasing-subsequence/)

4. [【ACM 算法题单】双蛋搜索问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/egg-dropping-puzzle/)

## 经典的DP优化

1. [【ACM 算法题单】单调数据结构优化问题](https://xingguang641.com/posts/acm/acm-type/dp-optimization/monotonic-structure/)

2. [【ACM 算法题单】区间数据结构优化问题](https://xingguang641.com/posts/acm/acm-type/dp-optimization/interval-structure/)