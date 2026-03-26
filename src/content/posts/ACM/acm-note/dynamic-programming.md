---
title: 【ACM 算法随笔】动态规划思想
published: 2026-02-26
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

> 本篇博客写作灵感来源于 N 神的动态规划概述

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=114531325973175&bvid=BV1m9EUzLEB4&cid=30031939563&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 动态规划状态设计

动态规划建模的核心难点往往不在于推导转移公式，而在于对 **状态的精准刻画** 。状态设计的本质是信息的一场取舍游戏：它决定了哪些关键变量必须被显式记录以维持逻辑完备，哪些冗余信息可以被忽略以降低搜索开销。一个精妙的状态定义能让转移路径清晰可见，而一个臃肿的定义则会使问题陷入复杂度爆炸的泥潭。

从实际建模的路径来看，状态设计绝非一蹴而就的固定模板，而是一个动态的 **组织与压缩过程** 。为了确保决策的 **无后效性** ，我们有时必须通过升维来捕捉必要的历史轨迹；而为了突破时空复杂度的瓶颈，则需通过分析问题的内在性质进行降维。这种调整本质上是在 **可行解空间的完整性** 与 **计算资源的有限性** 之间寻找最优平衡点，使转移过程在封闭且单调的逻辑轨道上运行。

从高层逻辑审视，状态可以被视为对高维可行解空间的一种 **低维投影** 。每一个维度都对应着问题中的一个核心约束或量化指标，而设计的过程就是决定哪些维度应作为显式枚举的坐标，哪些维度可以通过极值（ $\max / \min$ ）或单调性被压缩为状态值。合理的设计不仅能构建起自洽的逻辑闭环，更能从根本上消除冗余计算，将原本混沌的搜索空间转化为层次分明的递推结构。

## 维度转置与压缩

在许多优化型动态规划问题中，往往存在两个核心量，例如资源与收益。最常见的建模方式是固定资源维度，并将收益作为被优化对象，例如：

$$
dp[i][j] = k
$$

表示在前 $i$ 个决策下，资源为 $j$ 时能够达到的最优收益为 $k$ 。这种表达形式符合 “在给定限制下求最优” 的直观思路，但在具体实现时，若收益范围过大或转移缺乏良好的结构性质，状态可能难以维护。若将两个变量的角色进行交换，改为：

$$
dp[i][k] = j
$$

表示达到收益 $k$ 所需的最小资源为 $j$ ，则问题结构有时会更加规整。此时，原本作为答案输出的量成为状态维度，而原本作为状态维度的量则成为被优化对象，转移方向发生改变。

从信息完整性的角度，可以将问题抽象为三维 **可行性状态**：

$$
dp[i][j][k] =
\begin{cases}
1 & \text{if reachable} \\
0 & \text{if unreachable}
\end{cases}
$$

上述两种二维状态，本质上都是在三维可行域中对某一维进行 **极值压缩**：

$$
dp[i][j] = \max \Big( k \mid dp[i][j][k] = 1 \Big), \quad dp[i][k] = \min \Big( j \mid dp[i][j][k] = 1 \Big)
$$

因此，所谓维度转置，并非改变问题本身，而是改变对 **可行域** 进行投影的方向。

在实际算法设计中，维度选择往往受数值范围的直接影响。若两个量的取值规模存在明显差异，通常应当将取值范围较小的量作为 **状态维度** ，而将取值范围较大的量压缩为 **状态值** 进行极值维护。原因在于，状态维度直接决定 **时间与空间复杂度** ；而被压缩为状态值的量，只在转移时参与比较或更新，不会形成额外的枚举开销。

在更一般的情形下，也可以将问题的约束全部显式地纳入状态维度，然后再通过分析单调性或极值结构，将其中一维压缩为状态值。通过这种方式，可以在保持信息完整性的前提下，逐步降低维度规模，实现复杂度优化。综上所述，维度转置与压缩的核心并不在于形式变化，而在于对 **变量角色与规模结构** 的重新评估。合理的维度安排，往往能够从根本上改变状态空间的形态，使原本难以处理的问题转化为结构清晰、复杂度可控的动态规划模型。

## 贿赂怪兽问题

[题目链接](https://www.nowcoder.com/practice/736e12861f9746ab8ae064d4aae2d5a9)

### Problem Statement

你正在面对 $n$ 只怪兽，必须按 **从左到右** 的顺序依次通过。每只怪兽有两个属性：能力值 $a_i$ 和贿赂它所需的钱数 $b_i$ 。开始时你的能力为 $0$ 。

对于每一只怪兽，你的通过规则如下：

* **必须贿赂**：如果你当前的能力 **小于** $i$ 号怪兽的能力，则你必须付出 $b_i$ 的钱贿赂这只怪兽。
* **可以选择贿赂**：如果你当前的能力 **大于等于** $i$ 号怪兽的能力，你可以选择直接通过（不花钱，能力不增加），也可以选择依然付出 $b_i$ 的钱贿赂这只怪兽。
* **贿赂的效果**：如果你贿赂了怪兽，怪兽会加入你的队伍，其能力 $a_i$ 会直接累加到你的当前能力上。

你的目标是按顺序通过所有 $n$ 只怪兽。请计算通关所需的 **最小钱数** 。

### Constraints

- $1 \leq n \leq 1000$
- $1 \leq a_i \leq 10^4$
- $1 \leq b_i \leq 10$

### Input

输入格式如下：

* 第一行包含一个整数 $n$ ，表示怪兽的数量。
* 接下来 $n$ 行，每行包含两个整数 $a_i, b_i$ ，描述一只怪兽。

> $n$
> 
> $a_1 \quad b_1$
> 
> $a_2 \quad b_2$
> 
> $\dots$
> 
> $a_n \quad b_n$

### Output

输出一个整数，表示通关所需的最小钱数。

### Sample Input 1

```txt showLineNumbers=false
2
8 10
6 5
```

### Sample Output 1

```txt showLineNumbers=false
10
```

## 题目要点解析

动态规划的核心挑战在于如何设计一个既能涵盖所有必要决策信息，又能在时空复杂度限制内运行的状态表示。对于本题，如果按照常规思维，将 “当前积累的能力值” 作为 DP 的一个维度（例如定义 $dp[i][j]$ 为面对前 $i$ 只怪兽、当前能力为 $j$ 时的最小花费），会直接面临复杂度失效的问题。由于单只怪兽的能力值 $a_i$ 最高可达 $10^4$ ，总能力上限在 $10^7$ 数量级，这种设计会导致内存溢出（MLE）且转移效率极低。

为了优化模型，我们可以通过交换状态与数值的角色，转而定义 **$dp[j]$ 为花费恰好 j 元钱时所能积累的最大能力值** 。由于题目中总花费的上限仅为 $1000 \times 10 = 10000$，这个维度的空间开销非常理想。在此框架下，判定能否通过某只怪兽的标准从 “求最小钱数” 转变为 “验证在给定花费下所能达到的最大能力是否足以覆盖怪兽防御力” 。

在具体的转移实现中，每只怪兽的处理逻辑可以看作是 **0/1 背包问题** 的变体。针对每一个可能的总钱数 $j$ ，存在两条逻辑分支：首先是 **贿赂决策** ，只要之前的状态 $j - b_i$ 合法（即该花费是可以达到的），就可以通过支付 $b_i$ 元，在原有能力基础上累加 $a_i$ 。其次是 **武力通过决策** ，其前提是当前花费 $j$ 元所能达到的最大能力已经不小于该怪兽的防御力 $a_i$ 。在这种情况下，无需额外支出，能力值保持不变。

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

## 自由度压缩技巧

在设计动态规划模型时，初学者往往倾向于将问题中所有变化的变量（如多个对象的位置、时间、步数等）直接映射为状态维度。然而，这种直观的设计极易导致 **维度爆炸** ，使状态空间达到 $O(n^3)$ 甚至更高，超出了计算资源的承载能力。事实上，许多复杂问题中看似独立的变量之间，往往存在着某种 **隐含的约束关系** 。通过挖掘并利用这些关系，我们可以剔除冗余维度，这种优化手段被称为 **自由度压缩** 。

自由度压缩的核心逻辑在于寻找状态变量之间的 **函数依赖或守恒关系** 。在物理学中，自由度代表描述系统状态所需的最小独立变量个数；同理，在 DP 建模中，如果 $k$ 个变量之间存在一个确定的等式关系，那么我们只需要记录其中的 $k-1$ 个变量，剩下的一个便可被唯一确定。通过这种方式，原本高维的状态空间被投影到了更低维的流形上，从而在不丢失任何有效信息的前提下，显著降低算法的时空复杂度。

这种技巧在 **多路径同步移动** 、**网格路径相遇** 以及 **多对象追踪** 等问题中尤为常见。例如，在两个棋子同时从网格左上角出发移动到右下角的问题中，如果它们每步都只能向右或向下走，那么在任何时刻，这两个棋子的坐标 $(x_1, y_1)$ 和 $(x_2, y_2)$ 必须满足步数守恒：$x_1 + y_1 = x_2 + y_2 = step$ 。此时，我们只需记录当前的步数 $step$ 以及两个棋子的横坐标 $x_1$ 和 $x_2$ ，纵坐标则可以通过 $y = step - x$ 直接推导而出。

综上所述，自由度压缩不仅是一种节省空间的技巧，更是一种对问题 **结构特征** 的深度洞察。它要求我们跳出 “直观记录” 的思维定式，转而寻找变量背后的 **内在一致性** 。通过减少状态的自由度，我们可以将原本看似不可做的复杂问题，转化为结构精炼、运行高效的低维动态规划模型。

## 往返摘樱桃难题

[题目链接](https://leetcode.cn/problems/cherry-pickup/description/)

### Problem Statement

一个 $n \times n$ 的网格 `grid` 代表棋盘，每个单元格内容可以是以下三种之一：

* `0`：表示该单元格是空的，可以穿过。
* `1`：表示该单元格包含一个樱桃，可以在经过时摘取。
* `-1`：表示该单元格包含一个障碍物，无法穿过。

你需要执行以下操作：

1. 从起点 $(0, 0)$ 出发，只能向 **右** 或向 **下** 移动，直到到达终点 $(n-1, n-1)$ 。
2. 在经过包含樱桃的单元格时，摘取樱桃，该单元格随后变为 `0`（空）。
3. 到达 $(n-1, n-1)$ 后，从该点出发，只能向 **左** 或向 **上** 移动，直到回到起点 $(0, 0)$ 。
4. 同样，在回程经过包含樱桃的单元格时，摘取樱桃（如果第一次经过时已经摘取，则此处为 `0` ）。

如果不存在一条可以从起点到终点、再从终点回到起点的路径（即路径被障碍物堵死），则返回 $0$ 。

请计算你最多能摘取的樱桃总数。

### Constraints

- $n == grid.length$
- $n == grid[i].length$
- $1 \leq n \leq 50$
- $grid[i][j]$ 为 $-1, 0, 1$
- $grid[0][0] \ne -1$
- $grid[n-1][n-1] \ne -1$

### Input

输入格式如下：

* 第一行包含一个整数 $n$ ，表示网格的大小。
* 接下来 $n$ 行，每行 $n$ 个整数，表示网格数组 $grid_{i,j}$ 。

> $n$
> 
> $grid_{1,1} \quad grid_{1,2} \quad \dots \quad grid_{1,n}$
> 
> $\dots$
> 
> $grid_{n,1} \quad grid_{n,2} \quad \dots \quad grid_{n,n}$

### Output

输出一个整数，表示最多能摘取的樱桃总数。

### Sample Input 1

```txt showLineNumbers=false
3
0 1 -1
1 0 -1
1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
5
```

## 题目要点解析



## 扰乱字符串问题

[题目链接](https://leetcode.cn/problems/scramble-string/description/)

### Problem Statement

使用下面描述的算法可以扰乱字符串 $s$ 得到字符串 $t$ ：

1. 如果字符串的长度为 $1$ ，算法停止。

2. 如果字符串的长度 $> 1$ ，执行下述步骤：

    * 在一个随机下标处将字符串分割成两个非空的子字符串。即，如果已知字符串 $s$ ，则可以将其分成 $x$ 和 $y$ ，且满足 $s = x + y$ 。
    * **随机** 决定是否交换这两个子字符串。若交换，则 $s$ 变成 $y + x$ ；若不交换，则 $s$ 变成 $x + y$ 。
    * 应用该算法继续递归地对两个子字符串进行扰乱。

给你两个 **长度相等** 的字符串 $s1$ 和 $s2$ ，判断 $s2$ 是否是 $s1$ 的扰乱字符串。如果是，返回 `true` ；否则，返回 `false` 。

### Constraints

- $s1.length == s2.length$
- $1 \leq s1.length \leq 30$
- $s1$ 和 $s2$ 仅由小写英文字母组成

### Input

输入格式如下：

* 第一行包含一个字符串 $s1$ ，表示原始字符串。
* 第二行包含一个字符串 $s2$ ，表示待检查的字符串。

> $s1$
> 
> $s2$

### Output

* 如果 $s2$ 是 $s1$ 的扰乱字符串，输出 `true` ；否则输出 `false` 。

### Sample Input 1

```txt showLineNumbers=false
great
rgeat
```

### Sample Output 1

```txt showLineNumbers=false
true
```

### Sample Input 2

```txt showLineNumbers=false
abcde
caebd
```

### Sample Output 2

```txt showLineNumbers=false
false
```

## 题目要点解析



---

# 动态规划建模技巧

动态规划的核心价值并不在于对既有模型的机械套用，而在于 **对复杂问题进行形式化抽象与结构化表达的能力** 。许多问题在表层呈现出明显的递推特征，但若仅凭直观感性去构造状态，往往会导致状态空间规模爆炸、依赖关系错综复杂或转移机制难以精确刻画。因此，动态规划的进阶关键并非背诵固定范式，而是在深挖问题内在逻辑的基础上，构建一套能够准确反映子问题演化规律的状态表示体系。

所谓建模技巧，实质上是 **对问题表达框架的重构过程** 。在确保原问题语义与目标函数不变的前提下，通过视角切换或变量重新定义，使问题结构更契合递推分析的需求。例如，将单点往返路径重构为双点同步推进模型，可以将原本具有时间先后依赖的折返过程转化为同阶段的并行演化，从而消除跨阶段的逻辑耦合；又如在网格类问题中，通过对坐标系进行旋转或平移，可以将分散在两个维度的约束条件统一为线性表达，使状态间的转移条件更为直观清晰。这些方法并非改变了问题本身，而是通过重构形式化表达，使潜在的结构规律显性化。

由此可见，动态规划建模绝非模板匹配的简单劳动，而是一种基于结构分析的形式重建活动。有效的建模技巧往往源于对问题 **对称性、单调性、依赖方向以及约束特征** 的系统考察。通过对这些转化方式进行归纳与提炼，我们可以在面对形式多变的问题时，更敏锐地识别其深层的递推逻辑，从而构造出逻辑严密、表达简洁且复杂度可控的动态规划模型。

## 最少的跳跃能力

[题目链接](https://www.luogu.com.cn/problem/P8775)

### Problem Statement

小青蛙库睿奇要过河去参加派对。河的宽度为 $n$ ，河上分布着 $n-1$ 块石头，第 $i$ 块石头距离河左岸的距离为 $i$ ，其高度为 $h_i$ 。

由于高度限制，每块石头最多只能被踩 $h_i$ 次。库睿奇准备从左岸跳到右岸，再从右岸跳回左岸，如此往返共 $2x$ 次（即 $x$ 次从左往右，$x$ 次从右往左）。

在跳跃过程中，库睿奇的能力值为 $y$ ，这意味着它每次跳跃的距离 **不能超过** $y$ 。

请计算库睿奇能够完成 $2x$ 次跳跃所需的 **最小能力值 y** 。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq x \leq 10^9$
- $1 \leq h_i \leq 10^9$

### Input

输入格式如下：

* 第一行包含两个整数 $n$ 和 $x$ ，分别表示河的宽度和往返的总次数。
* 第二行包含 $n-1$ 个整数 $h_1, h_2, \dots, h_{n-1}$ ，表示每块石头的高度。

> $n \quad x$
> 
> $h_1 \quad h_2 \quad \dots \quad h_{n-1}$

### Output

输出一个整数，表示要求的最小能力值 $y$ 。

### Sample Input 1

```txt showLineNumbers=false
5 1
1 0 1 0
```

### Sample Output 1

```txt showLineNumbers=false
4
```

## 题目要点解析



## 过河所需石子数

[题目链接](https://www.luogu.com.cn/problem/P1052)

### Problem Statement

在河上有一座独木桥，长度为 $L$ 。桥上分布着 $M$ 颗石子，每颗石子所在的坐标都是 $1$ 到 $L-1$ 之间的整数。

青蛙库里奇准备从桥的起点（坐标 $0$ ）跳到桥的终点（坐标 $L$ 或更远的地方）。库里奇每次跳跃的距离范围是 $[S, T]$ 之间的任意整数。

在跳跃过程中，如果库里奇落下的位置刚好有一颗石子，它就会踩到这颗石子。库里奇希望在顺利过河的前提下，**踩到的石子数量最少** 。

请计算出库里奇过河所需踩到的最少石子数。

### Constraints

- $1 \leq L \leq 10^9$
- $1 \leq S \leq T \leq 10$
- $1 \leq M \leq 100$
- 石子坐标在 $(0, L)$ 范围内

### Input

输入格式如下：

* 第一行包含一个整数 $L$ ，表示桥的长度。
* 第二行包含三个整数 $S, T, M$ ，分别表示跳跃的最短距离、最长距离和石子总数。
* 第三行包含 $M$ 个整数，表示桥上每颗石子的坐标 $x_1, x_2, \dots, x_M$ 。

> $L$
> 
> $S \quad T \quad M$
> 
> $x_1 \quad x_2 \quad \dots \quad x_M$

### Output

输出一个整数，表示最少踩到的石子数。

### Sample Input 1

```txt showLineNumbers=false
10
2 3 5
2 3 5 6 7
```

### Sample Output 1

```txt showLineNumbers=false
2
```

## 题目要点解析



---

# 动态规划递归转化

从算法建模的角度看，**绝大多数动态规划问题在本质上都可以通过递归形式进行刻画** 。递归的核心价值在于清晰地定义了问题的 **最优子结构**：即一个规模为 $n$ 的复杂问题，其最优解能够被分解为若干规模更小的子问题解的组合。因此，在构建任何动态规划模型时，优先以 **递归视角** 明确状态的定义及其相互依赖关系，是揭示问题底层逻辑最直观的途径。

虽然朴素递归能完整描述求解逻辑，但其最大的弊端在于产生大量的 **重复子问题** 。在递归树的展开过程中，不同分支往往会多次触达完全相同的状态。当状态空间有限且计算结果具有确定性时，我们可以引入缓存机制，即 **记忆化搜索（Memoization）**。通过记录已求解状态的结果，计算效率可以实现从指数级到多项式级的质变。在这个意义上，记忆化搜索正是 **自顶向下** 实现动态规划的核心手段。

## 最低票价问题

[题目链接](https://leetcode.cn/problems/minimum-cost-for-tickets/description/)

### Problem Statement

在一个火车旅行很受欢迎的国度，你提前一年计划了一些火车旅行。在接下来的一年里，日历第 `days[i]` 天是你将会进行旅行的日子。这些天数按 **升序** 给出。

火车票有 **三种不同的销售方式** ：

1.  **1 天通行证** ：售价为 `costs[0]` 美元，允许你在 1 天内不限次数地乘坐火车。
2.  **7 天通行证** ：售价为 `costs[1]` 美元，允许你在 7 天内（包含开始的那天）不限次数地乘坐火车。
3.  **30 天通行证** ：售价为 `costs[2]` 美元，允许你在 30 天内（包含开始的那天）不限次数地乘坐火车。

通行证允许表示，如果你在第 `d` 天买了一张 **7 天通行证** ，那么你可以在第 $d, d + 1, d + 2, d + 3, d + 4, d + 5, d + 6$ 天内无限制乘车。

返回你想要完成所有计划日期内旅行所需的 **最低消费** 。

### Constraints

- $1 \leq days.length \leq 365$
- $1 \leq days[i] \leq 365$
- $days$ 按 **升序** 排列
- $costs.length == 3$
- $1 \leq costs[i] \leq 1000$

### Input

输入包含两行：

- 第一行包含若干个整数，表示计划旅行的日子 `days` 。
- 第二行包含三个整数，表示三种通行证的价格 `costs` 。

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

要 **解码** 已编码的消息，所有数字必须分组，然后按上述映射逆向映射回字母（可能有多种分组方式）。例如 `"11106"` 可以映射为：

- `"AAJF"` ，将消息分组为 `(1, 1, 10, 6)`
- `"KJF"` ，将消息分组为 `(11, 10, 6)`

注意，消息不能分组为 `(1, 11, 06)` ，因为 `"06"` 不能映射为 `"F"` ，由于 `"6"` 和 `"06"` 在映射中是不同的。

给你一个只含数字的 **非空** 字符串 $s$ ，请计算并返回 **解码** 方法的 **总数** 。

题目数据保证答案肯定是一个 **32 位** 的整数。

### Constraints

- $1 \leq s.length \leq 100$
- $s$ 只包含数字，并且可能包含前导零。

### Input

输入包含一行，为一个只包含数字的字符串 $s$ 。

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

除了数字之外，已编码的消息还可以包含 `'*'` 字符，该字符可以表示从 `'1'` 到 `'9'` 的任意数字（不包括 `'0'` ）。例如，`"1*"` 可以表示从 `"11"` 到 `"19"` 的任何编码消息。

要 **解码** 一条消息，所有数字必须分组，然后按上述映射逆向映射回字母（可能有多种分组方式）。

给你一个字符串 $s$ ，由数字和 `'*'` 字符组成，返回 **解码** 该消息的 **总数** 。

由于答案可能会非常大，所以必须对 $10^9 + 7$ 取模。

### Constraints

- $1 \le s.length \le 10^5$
- $s[i]$ 是数字或 `'*'`

### Input

输入包含一行，为一个包含数字和 `'*'` 的字符串 $s$ 。

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

输入包含三行，分别为棋盘大小 $n$、移动次数 $k$、起始行 $row$ 和起始列 $column$ 。

> $n$
> 
> $k$
> 
> $row \quad column$

### Output

输出包含一个浮点数，表示最终留在棋盘上的概率。

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

# 动态规划经典重构

动态规划作为求解最优化与计数问题的核心范式，其精髓在于通过 **状态划分** 与 **递推关系** 刻画子问题的依赖结构。在学习与竞赛实践中，将问题归类为背包、区间或树形等 **经典模型** ，是构建建模思维的第一步。这种基于范式的训练有助于快速建立系统化的框架。然而，面对复杂或大规模数据时，机械套用模板往往会导致状态空间或转移次数呈阶乘级或高阶多项式增长，使算法在理论或实践层面失去可行性。

事实上，许多高阶问题虽然表象上契合经典 DP 模型，但其深层结构中往往隐含着 **单调性、可分性、凸性或特殊的代数约束** 。若未能识别这些隐藏特质，仅仅沿用传统的维度设计，便会得到一个 “形式正确但复杂度失控” 的算法。因此，动态规划的进阶关键不在于背诵模板，而在于对问题本质结构的深度剖析。通过重新定义状态、旋转维度视角或重构转移逻辑，才能实现对复杂度的降维打击。

这一部分的讨论将聚焦于 **动态规划的经典重构** 这一核心议题，重点剖析那些看似符合经典范式、实则陷阱重重的题目类型。我们将通过对题目内在结构的严谨拆解，展示如何敏锐地捕捉题目中 **不同于常规 DP 的特殊性质** ，例如极小的值域范围、隐含的单调性或特殊的变量约束。利用这些差异点对状态与转移进行 “手术级” 重构，不仅能在逻辑上保持正确，更能从根本上扭转时空复杂度，使原本在经典 DP 框架下不可能处理的大规模数据范围变得 **完全可能且高效可控** 。

## 最长递增子排列

[题目链接](https://www.luogu.com.cn/problem/P1439)

### Problem Statement

给出两个长度为 $n$ 的排列 $P_1$ 和 $P_2$ ，计算它们的最长公共子序列的长度。

**排列** 是指 $1$ 到 $n$ 这 $n$ 个整数每个数恰好出现一次的序列。

### Constraints

- $1 \leq n \leq 10^5$
- $P_1, P_2$ 均为 $1$ 到 $n$ 的排列

### Input

输入格式如下：

* 第一行包含一个整数 $n$ ，表示排列的长度。
* 第二行包含 $n$ 个整数，表示排列 $P_1$ 。
* 第三行包含 $n$ 个整数，表示排列 $P_2$ 。

> $n$
> 
> $a_1 \quad a_2 \quad \dots \quad a_n$
> 
> $b_1 \quad b_2 \quad \dots \quad b_n$

### Output

输出一个整数，表示最长公共子序列的长度。

### Sample Input 1

```txt showLineNumbers=false
5
3 2 1 4 5
1 2 3 4 5
```

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点解析

假最长公共子序列问题

## 使集合总和相近

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class087/Code02_PickNumbersClosedSum.java)



## 题目要点解析

假01背包问题

## 最优的部署方案

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class128/Code02_BestDeploy1.java)



## 题目要点解析

假区间dp问题

## 增加限制的最长公共子序列问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class128/Code03_AddLimitLcs.java)



## 题目要点解析

假最长公共子序列问题

---

# 参考文献列表

## 经典 DP 问题

1. [【ACM 算法题单】子数组最大累加和问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/maximum-subarray-sum/)

2. [【ACM 算法题单】最长公共子序列问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/longest-common-subsequence/)

3. [【ACM 算法题单】最长递增子序列问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/longest-increasing-subsequence/)

4. [【ACM 算法题单】整数拆分问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/integer-partition/integer-partition/)

5. [【ACM 算法题单】有效括号问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/regular-bracket/)

## 经典 DP 分类

1. [【ACM 算法题单】背包动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/knapsack-dp/)

2. [【ACM 算法题单】区间动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/interval-dp/)

3. [【ACM 算法题单】树型动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/)

4. [【ACM 算法题单】状压动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/state-dp/)

5. [【ACM 算法题单】数位动态规划相关问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/digit-dp/)