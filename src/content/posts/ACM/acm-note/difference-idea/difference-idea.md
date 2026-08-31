---
title: 【ACM 算法随笔】差分数组与差分思想
published: 2025-11-25
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: false
---

# 差分数组基本原理

在数据结构相关问题中，我们经常需要对一个序列进行 **高频区间修改** 。如果直接在原数组上进行修改，单次操作的时间复杂度为 $O(n)$ ，当面临 $q$ 次连续修改时，总时间复杂度高达 $O(nq)$ 。

为了打破这一性能瓶颈，差分提供了一种巧妙的区间处理思路。其核心思想在于放弃记录原数组的绝对数值，转而记录原数组 **相邻元素之间的变化量** ，将原本繁重的区间范围修改转化为简单的区间端点操作。

我们引入差分数组 $Diff$ 来记录原数组 $Arr$ 的相邻关系，其具体定义如下：

$$
Diff[i] = 
\begin{cases} 
Arr[i], & i = 0 \\ 
Arr[i] - Arr[i - 1], & i > 0 
\end{cases}
$$

根据该定义，原数组 $Arr$ 中的任意元素，都可以通过对差分数组 $Diff$ 求前缀和进行复原。

通过记录相邻元素之间的相对变化量，差分巧妙地规避了在原数组上频繁进行区间修改所带来的高昂开销，从而将整体时间复杂度优化至 $O(q + n)$ 。值得注意的是，虽然差分具备高效的修改性能，但是其 **查询效率较低** 。因此只有在面临高频区间修改且查询次数较少的场景下，差分数组才能展现出其独有的算法优势。

## 差分的数学本质

从数学本质上看，差分可以被视为 **离散意义下的导数** 。连续数学利用导数刻画函数的变化速率，离散数学则利用差分刻画数据的变化趋势。对于一维序列，其差分数组的定义为：

$$
Diff[i] = Arr[i] - Arr[i-1]
$$

这一映射关系完美对应了连续函数导数的离散化近似：

$$
f'(x) \approx \frac{f(x) - f(x - \Delta x)}{\Delta x} \xrightarrow{\Delta x = 1} f(x) - f(x - 1)
$$

对原始数组做一次差分相当于 **对离散函数进行一次微分运算** ，对差分数组求一次前缀和相当于 **对离散导数进行一次积分运算** 。由于差分与前缀和互为逆运算，这种关系使其成为处理区间修改与静态查询问题最常用的方法。

> 具体性质可以看 N 神的视频讲解

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113927966954406&bvid=BV1dCFfemEHX&cid=28173994960&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 差分的通用公式

尽管一维差分的数学结构十分简单，但当应用场景拓展至高维时，其数学结构的复杂度将会显著上升。由于直接推导多维差分的通用公式难度较大，我们先以二维差分作为切入点进行分析。若将状态数组中的每个元素视为平面网格单元，则坐标 $(x, y)$ 处的差分值在几何上对应由顶点 $(x - 1, y - 1)$ 与 $(x, y)$ 所构成的矩形区域。

利用 **容斥原理** 对该区域进行几何解构，可以得到：

$$
Diff[x][y] = Arr[x][y] - Arr[x - 1][y] - Arr[x][y - 1] + Arr[x - 1][y - 1]
$$

对于 $n$ 维空间中的状态数组，其在坐标 $x = (x_1, x_2, \dots, x_n)$ 处的通用公式为：

$$
Diff[x_1][x_2]\dots[x_n] = \sum_{k = 0}^{n} (-1)^k \sum_{1 \leq i_1 < i_2 < \dots < i_k \leq n} Arr[x_1]\dots[x_{i_1} - 1]\dots[x_{i_k} - 1]\dots[x_n]
$$

上述基于容斥原理的推导过程依赖几何直观，尽管提供了清晰的空间映射，但并不具备严格的数学推导。若要实现更严密的代数证明，则需通过多维差分算子的 **叠加原理** 重新理解。我们先引入向后差分算子：

$$
\Delta_i \, Arr[x_1]\dots[x_i]\dots[x_n] = Arr[x_1]\dots[x_i]\dots[x_n] - Arr[x_1]\dots[x_i - 1]\dots[x_n]
$$

由于算子 $\Delta_i$ 仅作用于对应的第 $i$ 维坐标，各维度的算子在代数上互不干扰，这种维度独立性决定了各差分算子天然满足交换律。根据线性叠加原理，$n$ 维差分算子 $\Delta$ 可表示为一维差分算子的张量积形式：

$$
\Delta = \prod_{i = 1}^{n} \Delta_i = \Delta_1 \Delta_2 \dots \Delta_n
$$

接着引入恒等算子 $I$ 与向后位移算子 $E_i^{-1}$，从而将一维向后差分算子拆解为 $\Delta_i = I - E_i^{-1}$ 。将其代入 $n$ 维复合差分算子可以得到如下形式：

$$
\Delta = \prod_{i = 1}^{n} (I - E_i^{-1}) = (I - E_1^{-1}) (I - E_2^{-1}) \dots (I - E_n^{-1})
$$

根据多项式乘法法则，该连乘积的展开项由各因式的选取组合决定。如果任意指定 $k$ 个维度选择位移算子 $E_i^{-1}$ ，则会产生 $(-1)^k$ 的符号贡献。穷举所有维度的算子组合可后可以得到如下形式：

$$
\Delta = \sum_{k = 0}^{n} (-1)^k \sum_{1 \leq i_1 < i_2 < \dots < i_k \leq n} E_{i_1}^{-1} E_{i_2}^{-1} \dots E_{i_k}^{-1}
$$

将算子 $\Delta$ 作用于状态数组 $Arr$ ，即可直接导出前述基于容斥原理的高维差分通用公式。这种基于算子代数的推导方式摆脱了对空间几何直观的依赖，从而在代数层面揭示了多维差分的数学本质。

---

# 差分构造相关问题

在处理涉及区间加减操作的构造题时，**频繁的区间覆盖** 使得维护原数组的成本极高。由于构造问题的核心在于设计并记录一系列操作以达成目标状态，如果直接在原数组上同步更新每一个元素将会带来巨大的维护开销，因此我们需要引入 **差分数组** 来高效记录每一步操作的结果。

从算法特性的视角审视，差分数组的核心优势在于能更简单地维护区间加减操作。差分技巧天然适用于 **多修改单查询** 的场景，而构造类题目恰好完美契合这一特性。因为它往往只关注所有操作执行完毕后的最终状态或具体方案，这种 **维护简单查询困难** 的特性使得差分技巧成为了处理此类构造问题的首要选择。

## 构造所需的数组

[题目链接](https://leetcode.cn/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/description/)

### Problem Statement

给你一个整数数组 `target` 和一个数组 `initial` ，`initial` 数组与 `target` 数组有同样的大小，且一开始全部为 $0$ 。一次操作中，你可以从 `initial` 数组中选择 **任何** 子数组，并将每个值加 $1$ 。

返回从 `initial` 数组构造 `target` 数组的最少操作次数。答案保证在 $32$ 位整数以内。

### Constraints

- $1 \leq target.length \leq 10^5$
- $1 \leq target[i] \leq 10^5$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $target_1 \quad target_2 \quad \ldots \quad target_N$

### Output

输出一个整数，表示最少操作次数。

### Sample Input 1

```txt showLineNumbers=false
5
1 2 3 2 1
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
4
3 1 1 2
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析

这道题的核心操作是选择一个子区间 $[l, r]$ 并将其中所有元素同时加 $1$ 。如果直接从区间修改的角度思考会比较复杂，我们可以引入 **差分数组** 来辅助分析：

$$
Diff[i] = Target[i] - Target[i - 1]
$$

区间加 $1$ 操作在差分数组中可以转化为 **双端点操作** ，即在左端点 $l$ 产生一个 $+1$ 的正变化，并在右端点越界位置 $r + 1$ 产生一个 $-1$ 的负变化。在最终的目标状态中所有局部的操作会相互累加，如果正变化量更多则说明有一部分负变化点落在数组右侧越界的位置，反之则说明有一部分正变化点落在数组左侧越界的位置。

因此我们只需要统计差分数组中的正/负变化量之和：

$$
P = \sum_{i = 1}^{n} \max(0, Diff[i]) \quad N = \sum_{i = 1}^{n} \max(0, -Diff[i])
$$

由于这些变化点需要相互配对才能形成一次完整的区间操作，因此最少操作次数就是两者中的较大值。整个过程只需要遍历一次数组并计算差分即可完成统计，因此时间复杂度为 $O(n)$ ，空间复杂度为 $O(1)$ 。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 元素相同的数组

[题目链接](https://www.luogu.com.cn/problem/solution/P4552)

### Problem Statement

给定一个长度为 $N$ 的数列 $a$ 。

每次操作可以选择一个区间 $[l,r]$ ，将区间内所有元素同时加 $1$ 或同时减 $1$ 。

请你求出以下问题的结果：

- 至少需要多少次操作才能使数列中的所有元素都相等。
- 在保证操作次数最少的前提下最终得到的数列共有多少种。

### Constraints

- $1 \leq N \leq 10^5$
- $0 \leq a_i \leq 2^{31}$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ ，表示数列的长度。
- 接下来 $N$ 行，每行包含一个整数，表示数组中的元素。

> $N$
>
> $a_1$
>
> $a_2$
>
> $\ldots$
>
> $a_N$

### Output

输出包含两行：

- 第一行输出使数列所有元素都相等的最少操作次数。
- 第二行输出在最少操作次数下最终得到的数列种数。

### Sample Input

```txt showLineNumbers=false
4
1
1
2
2
```

### Sample Output

```txt showLineNumbers=false
1
2
```

## 题目要点解析

计算有多少种，就是计算出差分数组第一项/最后一项有多少种情况

## 使数列递增所需的最少操作次数

[题目链接](https://atcoder.jp/contests/abc421/tasks/abc421_g)

### Problem Statement

给定一个长度为 $n$ 的整数序列 $A = (A_1, A_2, \ldots, A_n)$ ，以及 $m$ 个整数区间 $(L_i, R_i)$ 。你可以对序列 $A$ 进行任意次数的以下操作：选择一个整数 $i$（ $1 \leq i \leq m$ ），将 $A_{L_i}, A_{L_i + 1}, \ldots, A_{R_i}$ 的每一个元素加 $1$ 。

请判断是否能将 $A$ 变为广义单调递增序列。若可以，求出最少需要的操作次数；若无法做到，请输出 $-1$ 。

### Constraints

- $1 \leq n \leq 300$
- $1 \leq m \leq 300$
- $1 \leq A_i \leq 300$
- $1 \leq L_i \leq R_i \leq n$
- 所有输入均为整数

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $m$ 。
- 第二行包含 $n$ 个整数，依次表示序列 $A_1, A_2, \dots, A_n$ 。
- 接下来 $m$ 行，每行包含两个整数 $L_i, R_i$ ，表示第 $i$ 个区间的左右边界。

> $n \quad m$
>
> $A_1 \quad A_2 \quad \ldots \quad A_n$
>
> $L_1 \quad R_1$
>
> $\ldots$
>
> $L_m \quad R_m$

### Output

输出一个整数，表示最少操作次数，若无法完成则输出 `-1` 。

### Sample Input 1

```txt showLineNumbers=false
4 3
4 2 3 2
2 2
2 3
4 4
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
3 2
3 1 2
2 1
2 2
```

### Sample Output 2

```txt showLineNumbers=false
-1
```

### Sample Input 3

```txt showLineNumbers=false
4 4
1 1 2 3
1 1
2 2
3 3
4 4
```

### Sample Output 3

```txt showLineNumbers=false
0
```

## 题目要点解析

在离散的角度下，差分数组相当于原数组的导数，因此要想让原数组单调递增，只需要让差分数组的所有元素都大于 $0$ 即可。在差分的视角下，区间加操作的本质就是将 $L_i$ 位置的数值 $+1$ ，将 $R_i + 1$ 位置的数值 $-1$ 。也就是说，每次操作相当于将 $R_i + 1$ 位置的物品分出一份给 $L_i$ 位置，并付出 $1$ 的操作代价。

于是这道题就可以转化为：在给定若干个调配通道下，能否通过最少次数的调度，将每个位置的差分值都调整到大于等于 $0$ 。这种带有运力限制与最优化代价的全局调配问题，可以转化为最小费用最大流解决。

我们建立一个包含超级源点 $S$ 、超级汇点 $T$ 以及各个差分位置结点的网络拓扑。对于差分初始状态，根据各位置物资的盈缺情况进行分类连边：

- 对于 $d_i > 0$ 的位置，说明该处物资富余，我们从源点 $S$ 向该位置引一条流量为 $d_i$ 且费用为 $0$ 的边

$$
\text{Capacity}(S \to i) = d_i \quad \text{Cost}(S \to i) = 0
$$

- 对于 $d_i < 0$ 的位置，说明该处物资紧缺，我们从该位置向汇点 $T$ 引一条流量为 $-d_i$ 且费用为 $0$ 的边

$$
\text{Capacity}(i \to T) = -d_i \quad \text{Cost}(i \to T) = 0
$$

由于原数组最后一个位置之后的差分值不需要强制大于等于 $0$ ，因此该位置相当于一个无限的物资蓄水池。我们从源点 $S$ 向该位置引一条流量为 $\infty$ 且费用为 $0$ 的边。

最后，题目中给出的 $m$ 个可选区间操作，本质上就是网络中可以利用的传送通道。对于每个区间，允许将物资从 $R_i$ 无限制地运送回 $L_i - 1$ ，且每运送单位物资需要消耗 $1$ 的代价。因此，在图中建立对应的操作边：

$$
\text{Capacity}(R_i \to L_i - 1) = \infty \quad \text{Cost}(R_i \to L_i - 1) = 1
$$

在具体求解时，我们首先需要统计所有紧缺位置的总需求量：

$$
K = \sum_{i} \max(-d_i, 0)
$$

由于通往汇点 $T$ 的每条管道都受限于该位置的实际缺口大小，网络的总体最大流上限为 $K$ 。当且仅当网络的最大流等于 $K$ 时，才意味着每个紧缺结点的管道全都达到了容量上限。此时网络流算法在达到最大流状态时所产生的总费用，即为所有缺口被补齐时所需的最小操作次数。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 广义差分相关问题

在最基础的差分模型中，核心操作仅局限于对指定区间内的所有元素 **同步累加一个常数** 。然而在竞赛题目中，区间操作往往不是固定累加一个常数，而是需要对区间累加一个 **特定规律的数列** 。当题目扩展至高维空间时，还需要维护更复杂的区域更新。面对这些更加复杂的区间操作，原本的差分技巧难以直接应对。

为了解决这些问题，我们需要对差分技巧进行扩展，深入挖掘这些区间操作背后的数学性质。根据区间修改操作的不同，我们可以将这种题目大致分为两种类型：第一种是 **存在通项公式的** 一维区间修改问题，第二种是 **具备特定规律的** 二维区间修改问题。接下来我们将结合具体的经典题型，深入拆解这两类问题的应对技巧。

## 复杂数列叠加

在一维数组的区间修改问题中，若区间内各位置所累加的数值不再是某个固定的常数，而是会随着位置规律变化的复杂数列，常规的差分方法便会 **彻底失效** 。这是因为常规的差分方式只能抵消恒定的增量，但面对 **会随前项动态变化** 的数列增量时，简单的邻项相减就无法完全消除。

由于数列的本质就是一系列满足某种特定递推关系的数字，而差分的本质就是消除邻项间的增量，因此我们可以从数列的 **递推公式** 出发，总结出一套应对此类复杂区间操作的通用解法。

### 等差数列区间加操作

等差数列区间加操作是最具代表性的区间修改操作，因此我们可以将等差数列作为切入点，逐步总结出复杂数列区间叠加问题的通用解法。假设我们需要对区间 $[L, R]$ 内的每个位置 $i$ 叠加一个首项为 $s$ 且公差为 $d$ 的等差数列：

$$
Arr[i] \leftarrow Arr[i] + s + (i - L) \times d
$$

若对原数组求一阶差分，由于等差数列相邻两项之差恒为公差 $d$ ，原本随位置线性变化的区间增量便转化为了固定的常数增量。因此只需进一步维护二阶差分，便能够将等差数列区间加操作转化为有限的单点修改。

假设我们需要对区间 $[L,R]$ 内的每个位置 $i$ 叠加一个 $k$ 次多项式数列：

$$
Arr[i] \leftarrow Arr[i] + \mathcal{P}_k​(i − L)
$$

由于连续作差会不断降低多项式的次数，并且任意一个 $k$ 次多项式经过 $k$ 次差分后都会退化为常数，因此只需维护 $k+1$ 阶差分便能将任意多项式数列的区间修改转化为有限的单点修改。

### 斐波那契区间加操作

然而并非所有数列都能够通过连续作差消除区间内部的增量，对于斐波那契数列这类非多项式数列，无论进行多少次差分都不会退化为常数。假设我们需要对区间 $[L, R]$ 内的每个位置 $i$ 叠加一个斐波那契数列：

$$
Arr[i] \leftarrow Arr[i] + F(i - L)
$$

其中 $F(0) = F(1) = 1$ ，并满足递推关系：

$$
F(i) = F(i - 1) + F(i - 2)
$$

与等差数列不同，斐波那契数列的变化规律由前面的若干项共同决定，无法通过有限次相邻作差消除区间内部的增量。因此我们需要根据其递推关系重新构造出适用于斐波那契数列的广义差分：

$$
Diff[i] = Arr[i] − Arr[i − 1] − Arr[i − 2]
$$

更一般地，对于满足 $k$ 阶线性齐次递推关系的数列：

$$
f(i) = \sum_{j = 1}^{k} c_j f(i - j)
$$

只需根据其递推关系重新定义广义差分：

$$
Diff[i] = Arr[i] - \sum_{j = 1}^{k} c_j Arr[i - j]
$$

便能够消除区间内部的增量，从而将复杂的区间修改转化为有限的单点修改。

### 杨辉三角区间加操作

除了线性递推数列外，还有一类数列由高维递推关系生成。杨辉三角就是典型的二维递推数列，其沿特定方向截取的一维序列同样具有良好的差分性质。假设我们需要对区间 $[L, R]$ 内的每个位置 $i$ 叠加一行杨辉三角：

$$
Arr[i] \leftarrow Arr[i] + \binom{k + i - L}{i - L}
$$

令 $x = i - L$ ，则该序列可以表示为：

$$
Arr[i] \leftarrow Arr[i] + \binom{k + x}{x}
$$

可以发现，该序列本质上是杨辉三角中一条特殊的斜线。若将杨辉三角第 $n$ 行第 $m$ 列的位置记为 $C_n^m$ ，则该序列中的第 $x$ 项有 $n = k + x$ 和 $m = x$ ，因此满足 $n - m = k$ 。

为了方便描述，后文将满足 $n - m = k$ 的斜线称为第 $k$ 条斜线。

根据杨辉三角的递推关系：

$$
\binom{n}{m} = \binom{n - 1}{m} + \binom{n - 1}{m - 1}
$$

移项变形后我们可以得到：

$$
\binom{k + x}{x} - \binom{k + x - 1}{x - 1} = \binom{k + x - 1}{x}
$$

对该序列进行一次差分：

$$
\binom{k + x}{x} \rightarrow \binom{k + x - 1}{x}
$$

根据上述计算结果可以发现，差分后的序列对应杨辉三角第 $k - 1$ 条斜线。也就是说，原本位于第 $k$ 条斜线上的序列会移动到第 $k - 1$ 条斜线。因此每进行一次差分，该序列都会沿着杨辉三角斜线方向移动一层。

继续进行差分可以得到：

$$
\binom{k + x}{x}
\rightarrow
\binom{k + x - 1}{x}
\rightarrow
\binom{k + x - 2}{x}
\rightarrow
\cdots
\rightarrow
\binom{x}{x} = 1
$$

经过 $k$ 次差分后，该序列最终退化为常数。因此杨辉三角组合数序列同样具有有限阶差分性质，只需维护对应阶数的差分数组，便能够将复杂的组合数区间叠加转化为有限次单点修改。

## 三步必杀的招数

[题目链接](https://www.luogu.com.cn/problem/P4231)

### Problem Statement

给定一个长度为 $N$ 的数组，初始时所有元素均为 $0$ 。

接下来进行 $M$ 次区间加操作，每次操作由四个整数 $l, r, s, e$ 表示：

- 第 $l$ 个位置增加 $s$
- 第 $r$ 个位置增加 $e$
- 区间内增加的值构成一个等差数列

保证每次操作对应等差数列的所有项均为整数。

所有操作完成后，请输出 **数组所有元素的异或和** 以及 **数组中的最大值** 。

### Constraints

- $1 \leq N \leq 10^7$
- $1 \leq M \leq 3 \times 10^5$
- $1 \leq l < r \leq N$

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $M$ ，分别表示数组长度和操作次数。
- 接下来 $M$ 行，每行包含四个整数 $l, r, s, e$ ，描述一次区间修改操作。

> $N \quad M$
>
> $l_1 \quad r_1 \quad s_1 \quad e_1$
>
> $\ldots$
>
> $l_M \quad r_M \quad s_M \quad e_M$

### Output

输出两个整数，分别表示最终数组所有元素的按位异或和以及数组中的最大值。

### Sample Input 1

```txt showLineNumbers=false
5 2
1 5 2 10
2 4 1 1
```

### Sample Output 1

```txt showLineNumbers=false
3 10
```

### Sample Input 2

```txt showLineNumbers=false
6 2
1 5 2 10
2 4 1 1
```

### Sample Output 2

```txt showLineNumbers=false
3 10
```

## 题目要点解析

等差数列区间加

## 有趣的组合数组

[题目链接](https://www.luogu.com.cn/problem/CF407C)

### Problem Statement

给定一个长度为 $n$ 的数组 $a$ 。你需要对该数组执行 $m$ 次区间修改操作。

每次操作由三个整数 $l_i, r_i, k_i$ 描述，表示对于所有满足 $l_i \leq j \leq r_i$ 的位置 $j$ ，将 $a_j$ 加上二项式系数：

$$
\binom{j - l_i + k_i}{k_i}
$$

请输出完成所有 $m$ 次操作后，整个数组每个元素对 $10^9 + 7$ 取模后的最终结果。

### Constraints

- $1 \leq n, m \leq 10^5$
- $1 \leq l_i \leq r_i \leq n$
- $0 \leq k_i \leq 100$
- $0 \leq a_i \leq 10^9$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $m$ ，分别表示数组长度和操作次数。
- 第二行包含 $n$ 个整数，表示初始数组的元素 $a_1, a_2, \ldots, a_n$ 。
- 接下来 $m$ 行，每行包含三个整数 $l_i, r_i, k_i$ ，描述一次区间修改操作。

> $n \quad m$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $l_1 \quad r_1 \quad k_1$
> 
> $\ldots$
> 
> $l_m \quad r_m \quad k_m$

### Output

输出 $n$ 个整数，表示所有操作完成后，数组中每个元素模 $10^9 + 7$ 后的最终结果。

### Sample Input 1

```txt showLineNumbers=false
5 1
0 0 0 0 0
1 5 0
```

### Sample Output 1

```txt showLineNumbers=false
1 1 1 1 1
```

### Sample Input 2

```txt showLineNumbers=false
10 2
1 2 3 4 5 0 0 0 0 0
1 6 1
6 10 2
```

### Sample Output 2

```txt showLineNumbers=false
2 4 6 8 10 7 3 6 10 15
```

## 题目要点解析

杨辉三角组合数学差分

## 复合区域更新

与一维差分类似，二维差分同样利用相邻位置之间的变化规律消除区域内部的影响。对于普通二维矩形加操作，只需维护二维差分数组，通过修改四个角点即可将整个区域更新转化为有限次单点修改。然而在竞赛中，区域修改的形式往往更加复杂，普通的二维差分无法处理所有情况，需要进一步结合修改的结构特点进行拆分维护。

这类特殊的区域修改一般不存在明确的高维递推关系，但通常具有明显的 **中心对称特征** 。由于这类修改具有中心对称性，在经过一次二维差分后，区域内部的增量会相互抵消，最终只保留少量方向上的残余信息。因此在处理此类修改时，需要先通过高维差分将整体转化为若干残余结构，再根据这些结构的特点分别进行维护。

## 真寻的高效清理

[题目链接](https://www.luogu.com.cn/problem/P10266)

### Problem Statement

真寻的房间由 $n$ 行 $m$ 列的方砖组成，第 $i$ 行第 $j$ 列的方砖上初始灰尘数量为 $a_{i, j}$ ，真寻将会使用 $k$ 次清理炸弹打扫房间。第 $i$ 次操作她会在第 $x_i$ 行第 $y_i$ 列的方砖上使用能量值为 $p_i$ 的清理炸弹，其清理效果如下：

- **中心点 $(x_i, y_i)$**：灰尘数量减少 $p_i^2$
- **外围第 1 圈**：灰尘数量减少 $(p_i - 1)^2$
- **外围第 2 圈**：灰尘数量减少 $(p_i - 2)^2$
- $\ldots$
- **外围第 $p_i - 1$ 圈**：灰尘数量减少 $1^2$

需要注意以下两点：

1. 如果某块方砖上的灰尘数量小于要减少的量，则该方砖灰尘数量变为 $0$ 。
2. 外围第 $d$ 圈是指所有满足 $\max(|x - x_i|, |y - y_i|) = d$ 的方砖。

请输出每个方砖最终的灰尘数量。

### Constraints

- $1 \leq n, m, p_i \leq 10^3$
- $1 \leq k \leq 10^6$
- $0 \leq a_{i, j} \leq 10^{12}$
- $1 \leq x_i \leq n$
- $1 \leq y_i \leq m$

### Input

输入包含多行：

- 第一行包含三个整数 $n$ 、$m$ 和 $k$ ，分别表示方砖行数、列数及操作次数。
- 接下来 $n$ 行，每行 $m$ 个整数，表示初始灰尘数组 $a_{i, j}$ 。
- 接下来 $k$ 行，每行包含三个整数 $x_i, y_i, p_i$ ，描述一次清理操作。

> $n \quad m \quad k$
> 
> $a_{1, 1} \quad a_{1, 2} \quad \ldots \quad a_{1, m}$
> 
> $\ldots$
> 
> $x_1 \quad y_1 \quad p_1$
> 
> $\ldots$

### Output

输出 $n$ 行，每行包含 $m$ 个整数，表示 $k$ 次操作后每块方砖上最终的灰尘数量。

### Sample Input 1

```txt showLineNumbers=false
4 5 2
7 5 4 6 5
2 4 7 9 5
6 4 5 3 5
1 2 3 0 7
2 4 2
3 3 2
```

### Sample Output 1

```txt showLineNumbers=false
7 5 3 5 4 
2 3 5 4 4 
6 3 0 1 4 
1 1 2 0 7 
```

### Sample Input 2

```txt showLineNumbers=false
6 7 3
6 4 7 8 4 6 1
4 5 4 6 7 5 9
1 4 3 0 7 1 3
4 6 0 7 9 0 0
1 2 3 4 4 5 8
4 7 6 8 7 4 9
5 5 3
2 3 4
3 6 2
```

### Sample Output 2

```txt showLineNumbers=false
2 0 0 0 0 5 1 
0 0 0 0 2 3 8 
0 0 0 0 1 0 1 
0 2 0 0 0 0 0 
0 1 1 0 0 0 7 
4 7 5 4 3 0 8 
```

## 题目要点解析

从题目描述来看，清理炸弹的 **清理效果** 具有极强的中心对称性。由于 **差分数组** 本质上是原数组的离散导数，这种具有固定代数规律的区域修改在经过 **高阶差分** 处理后，往往能被简化为有限次的单点修改。

如果对单次清理操作产生的增量矩阵进行一次 **二维差分**（或者分别执行一次横向和竖向的差分），可以发现差分的结果是 **呈 X 型对称分布** 的四个等差数列。这意味着差分的结果仍然具备一定规律，因此可以考虑再次进行差分。

然而这里的难点在于 **如何选择合适的差分方向** 。由于这些等差数列沿 **两条对角线方向** 分布，如果直接使用斜向差分，虽然能简化其中一条对角线，但另一条正交方向上的等差数列就没办法被简化。

为了解决这一问题，我们可以建立两个 **独立的差分辅助数组**：一个专门维护从 **左上到右下** 方向的差分结果，另一个则维护从 **左下到右上** 方向的差分结果。对于每一次操作，我们只需要在两个数组对应的位置上进行标记。通过这种拆分逻辑，可以将原本互相干扰的两个方向解耦，使它们在各自的差分维度下都能被简化。

在最终复原时，我们首先沿着各自对应的斜向方向进行 **第二次前缀和复原** ，将差分标记还原为等差数列。随后将这两个数组的结果进行 **叠加** ，再统一执行一次 **二维前缀和处理**（或者分别进行一次横向和竖向的前缀和），从而得到每个位置累计的总清理量 $Sum[i][j]$ 。最终方砖的灰尘残余量通过以下公式计算：

$$
\text{Result}[i][j] = \max(0, Arr[i][j] - Sum[i][j])
$$

通过对变化量进行差分处理，将原本复杂的二维区域修改转化为两个方向上的一维规律，并分别维护对应的差分信息。每次操作只需进行有限次标记，复杂度为 $O(k)$ ，最后通过一次 $O(n \cdot m)$ 的扫描完成复原。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 等式条件变为不等条件相关题目收集

在许多复杂的计数与组合问题中，**等式条件往往较为严格，并且缺少明显的单调性** 。如果直接针对精确条件进行统计，往往难以利用条件本身进行高效求解。相比之下，**不等式条件更加宽松，并且具有更强的单调性** 。

因此我们经常采用一种类似差分的转换思路，将原本难以统计的精确条件，拆解为两个容易统计的不等式条件：

$$
\text{count}(\text{ans} = k) = \text{count}(\text{ans} \leq k) - \text{count}(\text{ans} \leq k - 1)
$$

这种技巧的核心在于，我们不再直接统计 **恰好等于某个值** 的情况，而是统计 **不超过某个值** 的累计数量，通过放宽限制条件来获得更强的可处理性。由于不等式条件往往具有更好的单调性，我们可以结合相应的算法技巧进行高效统计，从而将原本难以处理的精确计数问题转化为更加容易维护的范围计数问题。

这种从精确统计转向范围统计的方法，本质是对计数过程进行 **前缀化处理** 。这一思想在组合数学中也有体现，**二项式反演** 便是其中的典型代表。它通过建立「至多/至少」与「恰好」之间的关系，利用广义容斥将精确计数转化为累积量的组合关系。虽然二项式反演涉及更复杂的数学原理，但其核心仍然是通过累计信息反推出精确结果。

### 数学期望的尾概率公式

在求解数学期望时，我们经常会遇到状态过于复杂而难以刻画概率分布的情况。为了降低计算的复杂程度，算法竞赛中通常会引入一种 **将点概率转化为范围概率** 的思维模型，通过 **重新构建期望的计算方式** 来简化解题过程。

中学阶段求解数学期望时，我们通常会使用以下公式：

$$
E[X] = \sum_{i = 1}^{\infty} i \cdot P(X = i) = 1 \cdot P(X = 1) + 2 \cdot P(X = 2) + 3 \cdot P(X = 3)
$$

而在算法竞赛中，我们经常使用期望的 **尾概率公式**：

$$
E[X] = \sum_{i = 1}^{\infty} P(X \geq i) = P(X \geq 1) + P(X \geq 2) + P(X \geq 3)
$$

原因在于传统公式中的 $P(X = i)$ 描述的是 **恰好发生某个状态** 的概率，而这类概率在很多情况都难以维护，因此一般使用尾概率公式进行求解。而这个公式的推导非常简单，本质上只利用了 **改变求和顺序** 的思想。

我们可以将公式排列为一个 **三角形矩阵**：

$$
\begin{aligned}
E[X] = \quad & P(X = 1) \\
+ \quad & P(X = 2) + P(X = 2) \\
+ \quad & P(X = 3) + P(X = 3) + P(X = 3)
\end{aligned}
$$

传统的求解方式是 **横向求和** ，即先算出每一行的结果再相加。现在我们 **改变视角** ，将这个矩阵 **纵向按列合并**：

- 第一列包含了所有可能发生的事件概率

$$
P(X = 1) + P(X = 2) + P(X = 3) = P(X \geq 1)
$$

- 第二列去掉了 $X = 1$ 的情况，包含了所有大于等于 $2$ 的事件概率

$$
P(X = 2) + P(X = 3) = P(X \geq 2)
$$

- 第三列去掉了 $X = 1, 2$ 的情况，包含了所有大于等于 $3$ 的事件概率

$$
P(X = 3) = P(X \geq 3)
$$

不难发现，将所有纵列的结果相加，仍然能够得到与原式相同的期望值。这种通过 **调整求和顺序** 的方法，本质上是将原本按照精确状态划分的概率分布，转化为了按照范围进行统计的尾概率形式。它将难以维护的点概率问题转化为具有单调性的范围统计，从而降低了复杂概率问题中的状态设计难度。

## K种整数子数组

[题目链接](https://leetcode.cn/problems/subarrays-with-k-different-integers/description/)

### Problem Statement

给定一个正整数数组 $nums$ 和一个整数 $k$ ，返回 $nums$ 中 **「好子数组」** 的数目。如果 $nums$ 的某个子数组中不同整数的个数恰好为 $k$ ，则称 $nums$ 的这个连续、不一定不同的子数组为「好子数组」。

**子数组** 是数组的 **连续** 部分。

### Constraints

- $1 \leq nums.length \leq 2 \times 10^4$
- $1 \leq nums[i], k \leq nums.length$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数，表示好子数组的数目。

### Sample Input 1

```txt showLineNumbers=false
5 2
1 2 1 2 3
```

### Sample Output 1

```txt showLineNumbers=false
7
```

### Sample Input 2

```txt showLineNumbers=false
5 3
1 2 1 3 4
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析

在处理子数组计数问题时，一个自然的想法是使用 **滑动窗口** 技巧。然而滑动窗口能够高效维护的关键在于问题本身具有 **单调性** ，只有当窗口状态随着边界移动呈现出稳定的变化趋势时，窗口的扩张与收缩才有据可依。通常情况下，这类具有单调性的条件表现为 **至少满足某个限制** 或 **至多满足某个限制** 。

由于本题要求统计 **恰好包含 k 个不同整数** 的子数组，而 **恰好** 这一等式条件本身不具备单调性，窗口长度的变化可能使状态在满足与不满足之间反复变化，因此无法直接利用滑动窗口进行统计。

为了破解这一困局，我们可以借助上面提到过的 **广义差分思路** ，将严苛的等式约束差分为具备单调性的不等式条件。通过将恰好型计数转化为两个 **逻辑一致仅参数不同** 的不等式计数：

$$
\text{count}(\text{distinct} = k) = \text{count}(\text{distinct} \leq k) - \text{count}(\text{distinct} \leq k - 1)
$$

由于 **至多 k 个不同整数** 具有天然的单调性，我们可以使用滑动窗口维护当前窗口内不同数字的数量，分别求出两个范围内的子数组数量，最后通过作差得到 **恰好 k 个不同整数** 的答案。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 2e4 + 100;
int N, k;
int nums[MAXN];

int count(int k, int* a){
    int left = -1, pre = 0, ans = 0;
    unordered_map<int, int> counts;
    for (int right = 0; right < N; right ++){
        counts[a[right]] += 1;
        while (left <= right && (int)counts.size() > k){
            counts[a[++left]]--;
            if (!counts[a[left]])
                counts.erase(a[left]);
        }
        ans += right - left;
    }

    return ans;
}

int main() {
    cin >> N >> k;
    for (int i = 0; i < N; i++){
        cin >> nums[i];
    }

    cout << count(k, nums) - count(k - 1, nums);
}
```

## 最值的数学期望

[题目链接](https://atcoder.jp/contests/abc411/tasks/abc411_e)

### Problem Statement

有 $n$ 个六面骰子，编号为 $1 \sim n$ 。骰子 $i$ 的六个面上分别写着数值 $A_{i, 1}, A_{i, 2}, \ldots, A_{i, 6}$ 。

现在将这 $n$ 个骰子同时掷出。请计算所有骰子朝上面数值的 **最大值** 的数学期望，结果对 $998244353$ 取模。

每个骰子的面是独立且等概率出现的。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq A_{i, j} \leq 10^9$
- 所有输入均为整数

### Input

输入包含多行：

- 第一行包含一个整数 $n$ 。
- 接下来 $n$ 行，每行包含 $6$ 个整数，依次表示第 $i$ 个骰子的面数值。

> $n$
>
> $A_{1, 1} \quad A_{1, 2} \quad \ldots \quad A_{1, 6}$
>
> $A_{2, 1} \quad A_{2, 2} \quad \ldots \quad A_{2, 6}$
>
> $\ldots$
>
> $A_{n, 1} \quad A_{n, 2} \quad \ldots \quad A_{n, 6}$

### Output

输出一个整数，表示最大值的数学期望。

### Sample Input 1

```txt showLineNumbers=false
2
1 1 4 4 4 4
1 1 1 3 3 3
```

### Sample Output 1

```txt showLineNumbers=false
332748121
```

### Sample Input 2

```txt showLineNumbers=false
2
1 1 1 1 1 1
2 2 2 2 2 2
```

### Sample Output 2

```txt showLineNumbers=false
2
```

### Sample Input 3

```txt showLineNumbers=false
8
55 76 80 21 34 28
82 84 2 32 56 17
11 57 37 28 39 18
47 2 97 25 75 29
72 45 22 75 26 81
6 79 16 68 68 40
31 80 68 57 18 55
49 10 63 91 93 40
```

### Sample Output 3

```txt showLineNumbers=false
213725517
```

## 题目要点解析

尾概率公式

---

# 区间求和变为前缀求和相关题目收集

在许多算法问题中，直接计算区间求和往往效率较低。由于不同区间之间存在大量重叠，如果每次查询都 **重新枚举整个区间** 进行累加，已经计算过的信息便无法得到有效利用，从而产生大量重复计算。

在引入前缀和之后，任意的区间和都可以表示为两个前缀值的差，进而将 **区间信息转化为端点信息**：

$$
\sum_{i = l}^{r} a_i = pre[r] - pre[l - 1]
$$

这种技巧的核心在于，用 **两个端点的差值** 代替对整个区间的枚举。通过预处理前缀和数组，我们可以在 $O(1)$ 时间内求出任意区间的和，将区间求和转化为一次简单的 **差值运算** ，为后续的分析与优化打下基础。

在完成上述的转化后，问题的重点便转移到这两个前缀值上。此时可以借助[两数之和思想](https://xingguang641.com/posts/acm/acm-note/two-sum-idea/two-sum-idea/)进行处理：**固定右端点对应的前缀值，动态维护可能作为左端点的前缀值** ，从而快速统计满足条件的区间。

## 数组的递增划分

[题目链接](https://leetcode.cn/problems/ways-to-split-array-into-three-subarrays/description/)

### Problem Statement

我们称一个分割整数数组的方案是 **好的** ，当它满足：

- 数组被分成三个 **非空** 连续子数组，从左至右分别命名为 `left` ，`mid` ，`right` 。
- `left` 中元素和小于等于 `mid` 中元素和，`mid` 中元素和小于等于 `right` 中元素和。

给你一个 **非负** 整数数组 `nums` ，请你返回 **好的** 分割 `nums` 方案数目。

由于答案可能会很大，请你将结果对 $10^9 + 7$ 取余后返回。

### Constraints

- $3 \leq nums.length \leq 10^5$
- $0 \leq nums[i] \leq 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数，表示答案对 $10^9 + 7$ 取模后的结果。

### Sample Input 1

```txt showLineNumbers=false
3
1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
6
1 2 2 2 5 0
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析

这道题要求把数组 `nums` 分割成三个 **非空连续子数组** `Left` 、`Mid` 和 `Right` ，并满足两个条件：`sum(Left) ≤ sum(Mid)` 且 `sum(Mid) ≤ sum(Right)` 。由于需要频繁比较区间和，如果每次重新计算会非常低效，因此可以先构建 **前缀和数组** 来简化计算。设 `pre[i]` 表示数组前 $i$ 个元素的和，那么整个数组的总和就是 `pre[n]` 。

当数组在位置 `left` 和 `mid` 处分割时，三个区间可以用前缀和表示为 `pre[left]` 、`pre[mid] - pre[left]` 和 `pre[n] - pre[mid]` 。这样一来，只需要把题目中的条件转化为前缀和处理即可。

首先考虑条件 `sum(Left) ≤ sum(Mid)` ，代入前缀和表达式可以得到：

$$
pre[left] \leq pre[mid] - pre[left]
$$

整理后得到：

$$
2 \times pre[left] \leq pre[mid]
$$

这说明当 `left` 固定时，`mid` 的前缀和至少需要达到 `2 * pre[left]` 。

接下来考虑第二个条件 `sum(Mid) ≤ sum(Right)` ，代入前缀和表达式可以得到：

$$
pre[mid] - pre[left] \leq pre[n] - pre[mid]
$$

整理后得到：

$$
2 \times pre[mid] \leq pre[left] + pre[n]
$$

进一步整理得到：

$$
pre[mid] \leq \frac{pre[left] + pre[n]}{2}
$$

因此在 `left` 固定时，`mid` 的前缀和必须满足如下范围：

$$
2 \times pre[left] \leq pre[mid] \leq \frac{pre[left] + pre[n]}{2}
$$

因为 `mid` 的最小值是 `2 * pre[left]` ，如果这个值大于 `mid` 的最大值 `(pre[left] + pre[n]) / 2` ，那么就不存在合法的 `mid` 。将不等式整理后可以得到一个非常重要的 **剪枝条件**：

$$
3 \times pre[left] \leq pre[n]
$$

也就是说，当 `pre[left]` 满足：

$$
pre[left] > \frac{pre[n]}{3}
$$

无论怎样选择 `mid` 都无法满足条件，因此可以直接停止枚举 `left` 。

在枚举 `left` 时，`mid` 的合法位置是前缀和数组的一段区间，下界是第一个满足 `pre[mid] ≥ 2 * pre[left]` 的位置，而上界是最后一个满足 `pre[mid] ≤ (pre[left] + pre[n]) / 2` 的位置。由于前缀和数组单调递增，因此可以使用 **二分查找算法** 来快速定位这两个边界。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 指定区间累加和

[题目链接](https://atcoder.jp/contests/abc404/tasks/abc404_g)

### Problem Statement

给定一个整数 $N$ 和长度为 $M$ 的整数序列：

$$
L = (L_1, L_2, \ldots, L_M) \quad
R = (R_1, R_2, \ldots, R_M) \quad
S = (S_1, S_2, \ldots, S_M)
$$

确定是否存在一个长度为 $N$ 的正整数序列 $A$ 满足以下条件：

$$
\sum_{j = L_i}^{R_i} A_j = S_i (1 \leq i \leq M)
$$

如果存在这样的序列，找到 $A$ 的最小可能和。

### Constraints

- $1 \leq N, M \leq 4000$
- $1 \leq L_i \leq R_i \leq N$
- $1 \leq S_i \leq 10^9$
- 所有输入均为整数

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $M$ 。
- 接下来的 $M$ 行，每行包含三个整数 $L$ 、$R$ 和 $S$ 。

> $N \quad M$
>
> $L_1 \quad R_1 \quad S_1$
> 
> $L_2 \quad R_2 \quad S_2$
> 
> $\ldots$
>
> $L_M \quad R_M \quad S_M$

### Output

如果不存在满足条件且长度为 $N$ 的正整数序列 $A$ 则输出 `-1` ，否则输出 $A$ 的最小可能总和。

### Sample Input 1

```txt showLineNumbers=false
5 3
1 2 4
2 3 5
5 5 5
```

### Sample Output 1

```txt showLineNumbers=false
12
```

### Sample Input 2

```txt showLineNumbers=false
1 2
1 1 1
1 1 2
```

### Sample Output 2

```txt showLineNumbers=false
-1
```

### Sample Input 3

```txt showLineNumbers=false
9 6
8 9 8
3 6 18
2 4 19
5 6 8
3 5 14
1 3 26
```

### Sample Output 3

```txt showLineNumbers=false
44
```

## 题目要点解析

差分约束

---

# 双边条件变为单边条件相关题目收集

在算法竞赛中，我们经常会遇到需要统计满足某种 **双边约束** 问题。这类问题的核心矛盾通常体现在条件的双向限制上，即要求某个统计量 $T$ 必须同时受限于给定的上下界：

$$
\text{lower} \leq T \leq \text{upper}
$$

由于单边约束通常具有良好的单调性，而双边约束难以直接利用这种性质，因此双边条件往往更难处理。

解决这类问题的一种经典思路，是将原本 **双边约束** 转化为更容易处理的 **单边约束** 。可以注意到 $\text{lower} \leq T \leq \text{upper}$ 可以等价为两个单边条件的交集，即 $T \leq \text{upper}$ 与 $T \geq \text{lower}$ 。在此基础上引入计数函数 $f(X)$ 来表示满足单边约束 $T \leq X$ 的样本总量，可以将原问题转化为差分形式：

$$
\text{count}(\text{lower} \leq T \leq \text{upper}) = f(\text{upper}) - f(\text{lower} - 1)
$$

这种转化的核心思想在于，将原本需要同时满足上下界限制的双边约束，转化为具有单调性的单边计数问题。由于单边约束通常更容易进行统计与维护，因此只需求出对应的计数函数，再通过一次差分即可恢复满足双边约束的答案。这种化繁为简的思想在许多算法问题中都有着广泛的应用。

值得一提的是，这类双边约束条件在[数位 DP 问题](https://xingguang641.com/posts/acm/acm-type/dp-classification/digit-dp/)中十分常见。然而数位 DP 问题中的双边约束条件的上下界通常超出了普通整数的表示范围，如果直接计算 $f(\text{lower} - 1)$ 则可能涉及到高精度计算。为了避免这种情况，我们可以先计算 $f(\text{upper}) - f(\text{lower})$ ，再单独判断 $lower$ 是否满足要求。

## 统计完全K次幂

[题目链接](https://leetcode.cn/problems/count-k-th-roots-in-a-range/description/)

### Problem Statement

给你两个正整数 `l` 和 `r` ，以及一个整数 `k` 。

如果一个整数 $x$ 满足 $x = y^k$ ，其中 $y$ 也是一个整数，那么我们称 $x$ 是一个 **完全 k 次幂** 。

请你统计并返回闭区间 $[l, r]$ 内 **完全 k 次幂** 的数量。

### Constraints

- $1 \leq l \leq r \leq 10^9$
- $1 \leq k \leq 30$

### Input

输入仅包含一行：

> $l \quad r \quad k$

### Output

输出一个整数，表示区间内完全 $k$ 次幂的数量。

### Sample Input 1

```txt showLineNumbers=false
1 9 3
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
8 30 2
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析

根据差分思想，区间计数问题可以转化为两个前缀计数之差。设 `count(n)` 表示闭区间 $[0, n]$ 内完全 $k$ 次幂的数量，那么题目要求的闭区间 $[l, r]$ 内的答案就可以表示为：

$$
count(r) - count(l - 1)
$$

对于给定的上限 $n$ ，我们需要寻找有多少个正整数 $y$ 满足 $y^k \leq n$ 。对两边同时开 $k$ 次方，问题就转化为求解满足 $y \leq \lfloor n^{1 / k} \rfloor$ 的正整数 $y$ 的个数。由于 $y \geq 1$ ，这个答案恰好就等于 $\lfloor n^{1 / k} \rfloor$ 的值。

当 $k \geq 2$ 时，最简单的方法是利用内置的浮点数函数 $pow(n, 1.0 / k)$ 进行计算，但这种方法会引入浮点数精度误差。在计算机内部，二进制浮点数表示会导致精度截断。例如，原本应该得到整数 $7$ ，但浮点数计算的实际结果可能是 $6.999999999$ ，直接向下取整就会错误地得到 $6$ 。

为了消除这种精度隐患，我们需要在浮点数粗略估值的基础上进行二次验证与边界微调。首先利用浮点数函数得到一个初始估值 $y$ ，由于浮点误差的绝对值极小，该估值与真实值的偏差只会是 $0$ 或 $1$ 。此时我们可以通过整数乘法或快速幂来计算其确切的 $k$ 次幂值，如果发现 $(y + 1)^k \leq n$ ，说明初始估值偏小，应将 $y$ 向上修正。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 统计公平的数对

[题目链接](https://leetcode.cn/problems/count-the-number-of-fair-pairs/description/)

### Problem Statement

给你一个下标从 $0$ 开始、长度为 $n$ 的整数数组 `nums` ，和两个整数 `lower` 和 `upper` ，返回 **公平数对的数目** 。

如果 $(i, j)$ 数对满足以下情况，则认为它是一个 **公平数对**：

- $0 <= i < j < n$
- $lower <= nums[i] + nums[j] <= upper$

### Constraints

- $1 \leq nums.length \leq 10^5$
- $nums.length == n$
- $-10^9 \leq nums[i] \leq 10^9$
- $-10^9 \leq lower \leq upper \leq 10^9$

### Input

输入包含两行：

- 第一行包含三个整数 $N$ 、$lower$ 和 $upper$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad lower \quad upper$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数，表示公平数对的数目。

### Sample Input 1

```txt showLineNumbers=false
6 3 6
0 1 7 4 4 5
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
5 11 11
1 7 9 2 5
```

### Sample Output 2

```txt showLineNumbers=false
1
```

## 题目要点解析

这道题要求统计满足 $i < j$ 且 `lower ≤ nums[i] + nums[j] ≤ upper` 的数对数量。直接枚举所有 $(i, j)$ 的时间复杂度是 $O(n^2)$ ，显然无法通过 $10^5$ 的数据规模，因此需要换一种思路。

一个常见的技巧是把区间计数问题转化为 **两个前缀计数之差** 。设 `count(x)` 表示满足 `nums[i] + nums[j] ≤ x` 的数对数量，那么题目要求的答案就可以表示为：

$$
count(upper) - count(lower - 1)
$$

因此问题就转化为了如何高效计算 `count(x)` 。

为了计算 `count(x)` ，首先应对数组进行排序。排序后数组满足单调递增的特性，如果固定左端点 $i$ ，随着右端点 $j$ 的增大，`nums[i] + nums[j]` 也会单调增加，因此可以使用 **双指针** 来统计合法的数对数量。

分别计算 `count(upper)` 和 `count(lower - 1)` 后，两者相减即可得到最终答案。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 参考文献引用列表

1. [【OI WiKi】前缀和与差分相关知识](https://oi-wiki.org/basic/prefix-sum/)

2. [【夜空之星】高阶差分求解多项式求和](https://www.cnblogs.com/nightsky05/p/16200886.html)