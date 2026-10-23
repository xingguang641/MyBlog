---
title: 【ACM 算法随笔】并查数据结构的应用
published: 2026-04-03
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: false
---

# 并查集等价性维护

并查集最基础的用法，是维护哪些元素属于同一类。这种关系有三条基本性质：任何元素与自己是同一类，同类元素之间不分先后，同类元素之间还可以相互传递。因此只要题目的条件能被解读成某两个元素必须归为一类，并且这种归类方式具有传递性，就可以交给并查集来解决。

但更多时候题目并不会直接表明两个元素同类，只会说明它们共享某种特征，例如落在同一行同一列，拥有公共的质因子，或者能经由某个中间元素到达。此时需要额外多做一步，把特征本身也视为一个点，于是共享特征就转化为共同连接同一个中介点，这种并查集就叫 **中介并查集** 。

## 程序自动化分析

[题目链接](https://www.luogu.com.cn/problem/P1955)

### Problem Statement

在实现程序自动分析的过程中，常常需要判定一些约束条件是否能被同时满足。

考虑一个简化版本：假设 $x_1, x_2, x_3, \cdots$ 代表程序中出现的变量，给定 $n$ 个形如 $x_i = x_j$ 或 $x_i \neq x_j$ 的变量相等/不等的约束条件，请判定是否可以分别为每一个变量赋予恰当的值，使得上述所有约束条件同时被满足。

现在给出一些约束满足问题，请分别对它们进行判定。

### Constraints

- $1 \leq t \leq 10$
- $1 \leq n \leq 10^5$
- $1 \leq i, j \leq 10^9$
- $e \in \{0, 1\}$

### Input

输入包含多个测试用例：

- 第一行包含一个整数 $t$ ，表示测试用例的数量。

> $t$
>
> $case_1$
>
> $case_2$
>
> $\ldots$
>
> $case_t$

- 对于每个测试用例：

    - 第一行包含一个正整数 $n$ ，表示该问题中需要被满足的约束条件个数。
    - 接下来 $n$ 行，每行包含三个整数 $i, j, e$ ，描述一个相等/不等的约束条件，相邻整数之间用单个空格隔开。若 $e = 1$ ，则该约束条件为 $x_i = x_j$ ；若 $e = 0$ ，则该约束条件为 $x_i \neq x_j$ 。

> $n$
>
> $i_1 \quad j_1 \quad e_1$
>
> $i_2 \quad j_2 \quad e_2$
>
> $\ldots$
>
> $i_n \quad j_n \quad e_n$

### Output

输出 $t$ 行，第 $k$ 行包含一个字符串 `YES` 或者 `NO` 。

### Sample Input 1

```txt showLineNumbers=false
2
2
1 2 1
1 2 0
2
1 2 1
2 1 1
```

### Sample Output 1

```txt showLineNumbers=false
NO
YES
```

### Sample Input 2

```txt showLineNumbers=false
2
3
1 2 1
2 3 1
3 1 1
4
1 2 1
2 3 1
3 4 1
1 4 0
```

### Sample Output 2

```txt showLineNumbers=false
YES
NO
```

## 题目要点解析



## 金字塔对齐问题

[题目链接](https://atcoder.jp/contests/abc428/tasks/abc428_f)

### Problem Statement

数轴上有 $N$ 个区间，区间 $i$ 的左端坐标为 $0$ ，右端坐标为 $W_i$ ，其中 $W_1 < W_2 < \cdots < W_N$ 。

给定 $Q$ 个询问，请按给出的顺序依次处理。每个询问是以下三种类型之一：

- `1 v`：设当前区间 $v$ 的 **左端点** 坐标为 $l$ ，平移所有编号不大于 $v$ 的区间，使它们的 **左端点** 坐标均为 $l$ 。
- `2 v`：设当前区间 $v$ 的 **右端点** 坐标为 $r$ ，平移所有编号不大于 $v$ 的区间，使它们的 **右端点** 坐标均为 $r$ 。
- `3 x`：输出当前包含坐标 $x + 1 / 2$ 的区间个数。

### Constraints

- $1 \leq N \leq 2 \times 10^5$
- $1 \leq Q \leq 2 \times 10^5$
- $1 \leq W_i \leq 10^9$
- $1 \leq v \leq N$
- $0 \leq x \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ ，表示区间的个数。
- 第二行包含 $N$ 个整数，表示每个区间右端点的初始坐标。
- 第三行包含一个整数 $Q$ ，表示询问的个数。
- 接下来 $Q$ 行，每行包含两个整数。

> $N$
>
> $W_1 \quad W_2 \quad \ldots \quad W_N$
>
> $Q$
>
> $type_1 \quad num_1$
>
> $type_2 \quad num_2$
>
> $\ldots$
>
> $type_Q \quad num_Q$

### Output

设类型 3 的询问共有 $q$ 个，输出 $q$ 行，第 $j$ 行包含第 $j$ 个类型 3 询问的答案。

### Sample Input

```txt showLineNumbers=false
4
2 4 6 10
5
2 3
1 2
3 2
2 4
3 1
```

### Sample Output

```txt showLineNumbers=false
4
1
```

## 题目要点解析



## 移除最多的石头

[题目链接](https://leetcode.cn/problems/most-stones-removed-with-same-row-or-column/description/)

### Problem Statement

$n$ 块石头放置在二维平面中的一些整数坐标点上，每个坐标点上最多只能有一块石头。

如果一块石头的 **同行或者同列** 上有其他石头存在，那么就可以移除这块石头。

请求出 **可以移除的石头** 的最大数量。

### Constraints

- $1 \leq n \leq 1000$
- $0 \leq x_i, y_i \leq 10^4$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示石头的数量。
- 接下来 $n$ 行，第 $i$ 行包含两个整数 $x_i$ 和 $y_i$ ，表示第 $i$ 块石头的坐标。

> $n$
>
> $x_1 \quad y_1$
>
> $x_2 \quad y_2$
>
> $\ldots$
>
> $x_n \quad y_n$

### Output

输出一个整数，表示最多可以移除的石头数量。

### Sample Input 1

```txt showLineNumbers=false
6
0 0
0 1
1 0
1 2
2 1
2 2
```

### Sample Output 1

```txt showLineNumbers=false
5
```

### Sample Input 2

```txt showLineNumbers=false
5
0 0
0 2
1 1
2 0
2 2
```

### Sample Output 2

```txt showLineNumbers=false
3
```

### Sample Input 3

```txt showLineNumbers=false
1
0 0
```

### Sample Output 3

```txt showLineNumbers=false
0
```

## 题目要点解析

（中介并查集）

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

:::tip
本题涉及上文提及的「中介并查集」技巧
:::

## 可激活最大点数

[题目链接](https://leetcode.cn/problems/maximum-points-activated-with-one-addition/description/)

### Problem Statement

给定二维平面上的 $n$ 个整数坐标点，任意两个点的坐标互不相同。

如果一个点被 **激活** ，那么所有与该点具有相同 $x$ 坐标或相同 $y$ 坐标的点也会被 **激活** 。

激活会一直持续，直到没有额外的点可以被激活为止。

你可以额外添加一个不在给定点集中的整数坐标点 $(x, y)$ ，并从这个新添加的点开始 **激活** 。

请求出可以被激活的 **最大** 点数，包括新添加的点。

### Constraints

- $1 \leq n \leq 10^5$
- $-10^9 \leq x_i, y_i \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示点的数量。
- 接下来 $n$ 行，第 $i$ 行包含两个整数 $x_i$ 和 $y_i$ ，表示第 $i$ 个点的坐标。

> $n$
>
> $x_1 \quad y_1$
>
> $x_2 \quad y_2$
>
> $\ldots$
>
> $x_n \quad y_n$

### Output

输出一个整数，表示可以被激活的最大点数。

### Sample Input 1

```txt showLineNumbers=false
3
1 1
1 2
2 2
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
3
2 2
1 1
3 3
```

### Sample Output 2

```txt showLineNumbers=false
3
```

### Sample Input 3

```txt showLineNumbers=false
4
2 3
2 2
1 1
4 5
```

### Sample Output 3

```txt showLineNumbers=false
4
```

## 题目要点解析

（中介并查集）

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

:::tip
本题涉及上文提及的「中介并查集」技巧
:::

## 又有一道好问题

[题目链接](https://ac.nowcoder.com/acm/contest/79505/K)

### Problem Statement

智能时代已扑面而来，为创新带来了前所未有的机遇和挑战。华为坚持基础研究不动摇，坚持开放创新不动摇，开放心胸，沿着客户的需求顺势而为，同时加强科学技术牵引客户需求，构建灵活的商业模式，使能百模千态，赋能千行万业，把数字世界带入每个人，每个家庭，每个组织，构建万物互联的智能世界。

从万物互联的智能世界里穿越回来的 Capps 为大家带来了又一道好题：

你有一个长度为 $n$ 的整数序列 $a = \{a_1, a_2, \ldots, a_n\}$ ，初始时 $a$ 序列的每个元素的值都为 $0$ 。现对序列 $a$ 执行操作共 $q$ 次，操作的输入和执行内容分为以下两种：

- `1 x`：将 $a$ 序列中 **下标** 为 $x$ 的元素 $+1$ 。
- `2 x`：将 $a$ 序列中 **数值** 为 $x$ 的元素都 $+1$ 。

最后请输出在顺序执行 $q$ 次操作之后的 $a$ 序列。

### Constraints

- $1 \leq T \leq 3 \times 10^5$
- $1 \leq n, q \leq 3 \times 10^5$
- $1 \leq op \leq 2$
- 所有测试用例中 $n$ 的总和不超过 $3 \times 10^5$
- 所有测试用例中 $q$ 的总和不超过 $3 \times 10^5$

### Input

输入包含多个测试用例：

- 第一行包含一个整数 $T$ ，表示测试用例的数量。

> $T$
>
> $case_1$
>
> $case_2$
>
> $\ldots$
>
> $case_T$

- 对于每个测试用例：

    - 第一行包含两个整数 $n$ 和 $q$ ，表示序列长度和操作次数。
    - 接下来 $q$ 行，第 $i$ 行包含两个整数 $op_i$ 和 $x_i$ ，表示第 $i$ 次操作，其中 $op_i$ 表示操作类型。

> $n \quad q$
>
> $op_1 \quad x_1$
>
> $op_2 \quad x_2$
>
> $\ldots$
>
> $op_q \quad x_q$

### Output

对于每个测试用例，输出一行 $n$ 个整数，表示经过 $q$ 次操作后的 $a$ 序列。

### Sample Input

```txt showLineNumbers=false
4
3 3
2 0
1 2
2 2
2 2
1 1
1 1
1 1
2 0
4 3
2 0
2 1
1 4
```

### Sample Output

```txt showLineNumbers=false
1 3 1
2 0
1
2 2 2 3
```

## 题目要点解析

虚点技巧（中介并查集）

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

:::tip
本题涉及上文提及的「中介并查集」技巧
:::

## 最大公约数遍历

[题目链接](https://leetcode.cn/problems/greatest-common-divisor-traversal/description/)

### Problem Statement

给定一个长度为 $n$ 的整数序列 $a_1, a_2, \ldots, a_n$ 。对于两个不同的下标 $i$ 和 $j$ ，当且仅当 $\gcd(a_i, a_j) > 1$ 时，可以在两个下标之间通行，其中 $\gcd$ 表示两个数的 **最大公约数** 。

你需要判断对于 **任意** 两个满足 $i < j$ 的下标 $i$ 和 $j$ ，是否存在若干次通行可以从 $i$ 到达 $j$ 。

如果任意满足条件的下标对都可以互相到达，请输出 `YES` ，否则输出 `NO` 。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq a_i \leq 10^5$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示序列的长度。
- 第二行包含 $n$ 个整数 $a_1, a_2, \ldots, a_n$ 。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

输出一行一个字符串，`YES` 表示任意两个下标之间都可以互相到达，`NO` 表示不可以。

### Sample Input 1

```txt showLineNumbers=false
3
2 3 6
```

### Sample Output 1

```txt showLineNumbers=false
YES
```

### Sample Input 2

```txt showLineNumbers=false
3
3 9 5
```

### Sample Output 2

```txt showLineNumbers=false
NO
```

### Sample Input 3

```txt showLineNumbers=false
4
4 3 12 8
```

### Sample Output 3

```txt showLineNumbers=false
YES
```

## 题目要点解析

GCD并查集（枚举因子）（中介并查集）

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

:::tip
本题涉及上文提及的「中介并查集」技巧
:::

## 最大公因数排序

[题目链接](https://leetcode.cn/problems/gcd-sort-of-an-array/description/)

### Problem Statement

给定一个长度为 $n$ 的整数序列 $a_1, a_2, \ldots, a_n$ ，你可以对序列执行如下操作 **任意次** ：

- 如果 $\gcd(a_i, a_j) > 1$ ，交换 $a_i$ 和 $a_j$ 的位置，其中 $\gcd(a_i, a_j)$ 表示 $a_i$ 与 $a_j$ 的最大公因数。

如果能使用上述交换方式将序列按 **非递减顺序** 排列，请输出 `YES` ，否则输出 `NO` 。

### Constraints

- $1 \leq n \leq 3 \times 10^4$
- $2 \leq a_i \leq 10^5$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示序列的长度。
- 第二行包含 $n$ 个整数 $a_1, a_2, \ldots, a_n$ 。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

输出一行一个字符串，`YES` 表示可以将序列排成非递减顺序，`NO` 表示不可以。

### Sample Input 1

```txt showLineNumbers=false
3
7 21 3
```

### Sample Output 1

```txt showLineNumbers=false
YES
```

### Sample Input 2

```txt showLineNumbers=false
4
5 2 6 2
```

### Sample Output 2

```txt showLineNumbers=false
NO
```

### Sample Input 3

```txt showLineNumbers=false
5
10 5 9 3 15
```

### Sample Output 3

```txt showLineNumbers=false
YES
```

## 题目要点解析

GCD并查集（枚举因子）（中介并查集）

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

:::tip
本题涉及上文提及的「中介并查集」技巧
:::

---

# 并查集连通性维护

并查集的另一类用法是维护无向图的连通块，两个顶点之间若存在一条路径，就称它们连通，这种关系同样满足自反、对称与传递，因此也能交给并查集处理。从划分的角度看，一个连通块就是一个类，全部顶点被分成若干互不相交的连通块。与等价性不同的是，这里的关系由图的结构给出，并查集要维护的是加边过程中连通块如何合并。

无向图中的连通块随加边而合并，随删边而分裂。因此只加边不删边的题目可以在线维护，而只删边不加边的题目只要把操作序列倒过来处理，删除就变成了添加，这种技巧也被称作 **时光倒流** 。

## 删除后的最大和

[题目链接](https://leetcode.cn/problems/maximum-segment-sum-after-removals/description/)

### Problem Statement

给定两个长度为 $n$ 的整数序列 $a_1, a_2, \ldots, a_n$ 和 $p_1, p_2, \ldots, p_n$ ，其中 $p$ 是 $1$ 到 $n$ 的一个排列。

对于第 $i$ 次操作，删除 $a$ 中位于下标 $p_i$ 处的元素，将 $a$ 分割成更小的子段。

一个 **子段** 是 $a$ 中连续 **正** 整数形成的序列，**子段和** 是子段中所有元素的和。

请求出每次删除操作以后的 **最大** 子段和。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq a_i \leq 10^9$
- $1 \leq p_i \leq n$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示序列的长度。
- 第二行包含 $n$ 个整数，表示删除操作开始前的序列 $a$ 。
- 第三行包含 $n$ 个整数，第 $i$ 个整数表示第 $i$ 次删除操作的下标 $p_i$ 。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$
>
> $p_1 \quad p_2 \quad \ldots \quad p_n$

### Output

输出一行 $n$ 个整数，第 $i$ 个数表示第 $i$ 次删除操作后的最大子段和。

### Sample Input 1

```txt showLineNumbers=false
5
1 2 5 6 1
1 4 3 5 2
```

### Sample Output 1

```txt showLineNumbers=false
14 7 2 2 0
```

### Sample Input 2

```txt showLineNumbers=false
4
3 2 11 1
4 3 2 1
```

### Sample Output 2

```txt showLineNumbers=false
16 5 3 0
```

## 题目要点解析

仅有删边的题目转成加边题（逆向思维）

## 情侣的牵手难题

[题目链接](https://leetcode.cn/problems/couples-holding-hands/description/)

### Problem Statement

$n$ 对情侣坐在连续排列的 $2n$ 个座位上，想要牵到对方的手。

人和座位由一个整数数组表示，其中第 $i$ 个座位上的人的编号为 $r_i$ 。情侣们按顺序编号，第一对是 $(0, 1)$ ，第二对是 $(2, 3)$ ，以此类推，最后一对是 $(2n - 2, 2n - 1)$ 。

请求出最少交换座位的次数，以便每对情侣可以并肩坐在一起。

### Constraints

- $2 \leq n \leq 30$
- $0 \leq r_i \leq 2n - 1$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示情侣的对数。
- 第二行包含 $2n$ 个整数，第 $i$ 个整数表示第 $i$ 个座位上的人的编号。

> $n$
>
> $r_1 \quad r_2 \quad \ldots \quad r_{2n}$

### Output

输出一个整数，表示最少交换座位的次数。

### Sample Input 1

```txt showLineNumbers=false
2
0 2 1 3
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
2
3 2 0 1
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析

贪心+并查集

## 新增道路查询后的最短距离问题

[题目链接](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/description/)

### Problem Statement

有 $n$ 个城市，编号从 $0$ 到 $n - 1$ 。初始时，每个城市 $i$ 都有一条 **单向** 道路通往城市 $i + 1$（ $0 \leq i < n - 1$ ）。

接下来有 $q$ 个查询，第 $i$ 个查询给出 $u_i$ 和 $v_i$ ，表示新建一条从城市 $u_i$ 到城市 $v_i$ 的 **单向** 道路。每次查询后，你需要找到从城市 $0$ 到城市 $n - 1$ 的 **最短路径长度** 。保证不存在两个查询 $i \neq j$ 满足 $u_i < u_j < v_i < v_j$ 。

请求出处理完前 $i + 1$ 个查询后，从城市 $0$ 到城市 $n - 1$ 的最短路径长度。

### Constraints

- $3 \leq n \leq 10^5$
- $1 \leq q \leq 10^5$
- $0 \leq u_i < v_i < n$
- $1 < v_i - u_i$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $q$ ，分别表示城市数量和查询数量。
- 接下来 $q$ 行，第 $i$ 行包含两个整数 $u_i$ 和 $v_i$ ，表示第 $i$ 个查询。

> $n \quad q$
>
> $u_1 \quad v_1$
>
> $u_2 \quad v_2$
>
> $\ldots$
>
> $u_q \quad v_q$

### Output

输出一行 $q$ 个整数，第 $i$ 个数表示处理完前 $i$ 个查询后从城市 $0$ 到城市 $n - 1$ 的最短路径长度。

### Sample Input 1

```txt showLineNumbers=false
5 3
2 4
0 2
0 4
```

### Sample Output 1

```txt showLineNumbers=false
3 2 1
```

### Sample Input 2

```txt showLineNumbers=false
4 2
0 3
0 2
```

### Sample Output 2

```txt showLineNumbers=false
1 1
```

## 题目要点解析

区间并查集

## 二维矩阵集水器

[题目链接](https://leetcode.cn/problems/kskhHQ/solutions/1876216/jiantu-by-endlesscheng-rkra/)

### Problem Statement

字符串数组描述了一个二维平面中的矩阵形式的集水器，第 $i$ 行第 $j$ 列的字符为：

- `'l'` 表示向左倾斜的隔板（即从左上到右下）。
- `'r'` 表示向右倾斜的隔板（即从左下到右上）。
- `'.'` 表示此位置没有隔板。

已知当隔板构成存储容器可以存水，每个方格代表的蓄水量为 $2$ 。集水器初始浸泡在水中，除内部密闭空间外，所有位置均被水填满。现将其从水中竖直向上取出，请求出集水器最终的蓄水量。

**注意**：隔板具有良好的透气性，因此空气可以穿过隔板，但水无法穿过。

### Constraints

- $1 \leq n \leq 50$
- $1 \leq m \leq 50$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $m$ ，分别表示集水器的行数和列数。
- 接下来 $n$ 行，第 $i$ 行包含一个长度为 $m$ 的字符串，表示集水器第 $i$ 行各位置的隔板情况。

> $n \quad m$
>
> $s_1$
>
> $s_2$
>
> $\ldots$
>
> $s_n$

### Output

输出一个整数，表示集水器最终的蓄水量。

### Sample Input 1

```txt showLineNumbers=false
4 6
....rl
l.lr.r
.l..r.
..lr..
```

### Sample Output 1

```txt showLineNumbers=false
18
```

### Sample Input 2

```txt showLineNumbers=false
4 9
.rlrlrlrl
ll..rl..r
.llrrllrr
..lr..lr.
```

### Sample Output 2

```txt showLineNumbers=false
18
```

### Sample Input 3

```txt showLineNumbers=false
3 4
rlrr
llrl
llr.
```

### Sample Output 3

```txt showLineNumbers=false
6
```

### Sample Input 4

```txt showLineNumbers=false
8 9
...rl...
..r..l..
.r.rl.l.
r.r..l.l
l.l..rl.
.l.lr.r.
..l..r..
...lr...
```

### Sample Output 4

```txt showLineNumbers=false
30
```

## 题目要点解析

连通性维护（困难版）

## 判断角落可达性

[题目链接](https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/description/)

### Problem Statement

给定两个正整数 $X$ 和 $Y$ ，以及 $n$ 个圆，第 $i$ 个圆的圆心为 $(x_i, y_i)$ 、半径为 $r_i$ 。

坐标平面内有一个左下角在原点、右上角在 $(X, Y)$ 的矩形，你需要判断是否存在一条从左下角到右上角的一般路径，满足路径 **完全** 在矩形内部，**不会** 触碰或者经过 **任何** 圆的内部和边界，同时 **只** 在起点和终点接触到矩形。

如果存在这样的路径，请输出 `YES` ，否则输出 `NO` 。

### Constraints

- $3 \leq X, Y \leq 10^9$
- $1 \leq n \leq 1000$
- $1 \leq x_i, y_i, r_i \leq 10^9$

### Input

输入包含多行：

- 第一行包含三个整数 $X$ 、$Y$ 和 $n$ ，分别表示矩形右上角的横纵坐标与圆的个数。
- 接下来 $n$ 行，第 $i$ 行包含三个整数 $x_i$ 、$y_i$ 和 $r_i$ ，表示第 $i$ 个圆的圆心坐标与半径。

> $X \quad Y \quad n$
>
> $x_1 \quad y_1 \quad r_1$
>
> $x_2 \quad y_2 \quad r_2$
>
> $\ldots$
>
> $x_n \quad y_n \quad r_n$

### Output

输出一行一个字符串，`YES` 表示存在满足条件的路径，`NO` 表示不存在。

### Sample Input 1

```txt showLineNumbers=false
3 4 1
2 1 1
```

### Sample Output 1

```txt showLineNumbers=false
YES
```

### Sample Input 2

```txt showLineNumbers=false
3 3 1
1 1 2
```

### Sample Output 2

```txt showLineNumbers=false
NO
```

### Sample Input 3

```txt showLineNumbers=false
3 3 2
2 1 1
1 2 1
```

### Sample Output 3

```txt showLineNumbers=false
NO
```

### Sample Input 4

```txt showLineNumbers=false
4 4 1
5 5 1
```

### Sample Output 4

```txt showLineNumbers=false
YES
```

## 题目要点解析

连通性维护（困难版）

## 好路径的总个数

[题目链接](https://leetcode.cn/problems/number-of-good-paths/description/)

### Problem Statement

给定一棵 $n$ 个节点的树，节点编号从 $0$ 到 $n - 1$ 。每个节点有一个值，第 $i$ 个节点的值为 $v_i$ 。

一条 **好路径** 需要满足以下条件：

1. 开始节点和结束节点的值 **相同** 。
2. 开始节点和结束节点中间的所有节点值都 **小于等于** 开始节点的值。

请求出不同好路径的数目。注意，一条路径和它反向的路径算作 **同一** 路径。

### Constraints

- $1 \leq n \leq 3 \times 10^4$
- $0 \leq v_i \leq 10^5$
- $0 \leq a_i, b_i < n$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示节点数。
- 第二行包含 $n$ 个整数，第 $i$ 个整数表示编号为 $i - 1$ 的节点的值。
- 接下来 $n - 1$ 行，第 $i$ 行包含两个整数 $a_i$ 和 $b_i$ ，表示节点 $a_i$ 和 $b_i$ 之间有一条无向边。

> $n$
>
> $v_0 \quad v_1 \quad \ldots \quad v_{n - 1}$
>
> $a_1 \quad b_1$
>
> $a_2 \quad b_2$
>
> $\ldots$
>
> $a_{n - 1} \quad b_{n - 1}$

### Output

输出一个整数，表示不同好路径的数目。

### Sample Input 1

```txt showLineNumbers=false
5
1 3 2 1 3
0 1
0 2
2 3
2 4
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
5
1 1 2 2 3
0 1
1 2
2 3
2 4
```

### Sample Output 2

```txt showLineNumbers=false
7
```

### Sample Input 3

```txt showLineNumbers=false
1
1
```

### Sample Output 3

```txt showLineNumbers=false
1
```

## 题目要点解析

增量法+并查集

## 可获得的总分数

[题目链接](https://leetcode.cn/problems/maximum-number-of-points-from-grid-queries/description/)

### Problem Statement

给定一个 $m$ 行 $n$ 列的整数矩阵，其中第 $i$ 行第 $j$ 列的元素为 $a_{i,j}$ 。有 $k$ 次查询，第 $i$ 次查询给出一个整数 $q_i$ 。

对于每次查询，你从矩阵 **左上角** 单元格开始，重复以下过程：

- 如果 $q_i$ **严格** 大于你当前所处位置单元格的值，且该单元格是第一次访问，则获得 $1$ 分，并且你可以移动到上、下、左、右任一 **相邻** 单元格。
- 否则，你不能获得任何分，并结束这一过程。

请求出每次查询可以获得的最大分数。注意，对于每个查询，你可以访问同一个单元格 **多次** 。

### Constraints

- $2 \leq m, n \leq 1000$
- $4 \leq m \cdot n \leq 10^5$
- $1 \leq k \leq 10^4$
- $1 \leq a_{i, j}, q_i \leq 10^6$

### Input

输入包含多行：

- 第一行包含两个整数 $m$ 和 $n$ ，表示矩阵的行数和列数。
- 接下来 $m$ 行，第 $i$ 行包含 $n$ 个整数，表示矩阵第 $i$ 行的元素。
- 接下来一行包含一个整数 $k$ ，表示查询次数。
- 接下来 $k$ 行，每行包含一个整数，第 $i$ 行表示第 $i$ 次查询的 $q_i$ 。

> $m \quad n$
>
> $a_{1, 1} \quad a_{1, 2} \quad \ldots \quad a_{1, n}$
>
> $a_{2, 1} \quad a_{2, 2} \quad \ldots \quad a_{2, n}$
>
> $\ldots$
>
> $a_{m, 1} \quad a_{m, 2} \quad \ldots \quad a_{m, n}$
>
> $k$
>
> $q_1$
>
> $q_2$
>
> $\ldots$
>
> $q_k$

### Output

输出一行 $k$ 个整数，第 $i$ 个数表示第 $i$ 次查询可以获得的最大分数。

### Sample Input 1

```txt showLineNumbers=false
3 3
1 2 3
2 5 7
3 5 1
3
5
6
2
```

### Sample Output 1

```txt showLineNumbers=false
5 8 1
```

### Sample Input 2

```txt showLineNumbers=false
2 3
5 2 1
1 1 2
1
3
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析

增量法+并查集

## 动态边收缩问题

[题目链接](https://atcoder.jp/contests/abc411/tasks/abc411_f)

### Problem Statement

给定一张 $N$ 个顶点 $M$ 条边的无向图 $G_0$ ，顶点和边分别编号为 $1, 2, \ldots, N$ 和 $1, 2, \ldots, M$ ，边 $i$ 连接顶点 $U_i$ 和顶点 $V_i$ 。高桥君有一张图 $G$ 和编号为 $1, 2, \ldots, N$ 的 $N$ 个棋子，初始 $G = G_0$ 且棋子 $i$ 在 $G$ 的顶点 $i$ 上。

接下来他将依次进行 $Q$ 次操作，第 $i$ 次操作给出一个 $1$ 到 $M$ 之间的整数 $X_i$ ，并进行如下操作：

若在 $G$ 中，棋子 $U_{X_i}$ 与棋子 $V_{X_i}$ 位于不同的顶点，且它们之间（在 $G$ 上）存在边 $e$ ，则创建将边 $e$ 缩约后得到的图 $G'$ 。此时，若产生自环则将其删去，若存在重边则将其替换为简单边。

然后，在 $G$ 中边 $e$ 所连接的两个顶点上放置的所有棋子，都放到 $G'$ 中由 $e$ 的缩约新生成的顶点上；$G$ 上其他顶点上的棋子，放到 $G'$ 中对应的顶点上。最后，将这样得到的 $G'$ 作为新的 $G$ 。

若棋子 $U_{X_i}$ 与棋子 $V_{X_i}$ 位于同一顶点，或者它们所在的顶点之间没有边相连，则什么都不做。

对于每次操作 $i = 1, 2, \ldots, Q$ ，输出第 $i$ 次操作后 $G$ 的边数。

**边的缩约**：连接顶点 $u$ 与顶点 $v$ 的边的缩约，是把顶点 $u, v$ 合并为一个顶点的操作。更准确地说，对 $G$ 进行边缩约得到的图，是指对 $G$ 执行以下操作得到的结果：

- 向 $G$ 中新增一个顶点 $w$ 。
- 对于 $G$ 中除 $u, v$ 以外的每个顶点 $x$ ，当且仅当存在连接 $u$ 与 $x$ 或 $v$ 与 $x$ 的边时，添加连接 $w$ 与 $x$ 的边。
- 删除顶点 $u, v$ 并删除连接 $u$ 与 $v$ 的边以及连接 $u$ 或 $v$ 与其他顶点的所有边。

### Constraints

- $2 \leq N \leq 3 \times 10^5$
- $1 \leq M \leq 3 \times 10^5$
- $1 \leq U_i < V_i \leq N$
- $1 \leq Q \leq 3 \times 10^5$
- $1 \leq X_i \leq M$

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $M$ ，分别表示顶点数和边数。
- 接下来 $M$ 行，第 $i$ 行包含两个整数，表示第 $i$ 条边连接的两个顶点。
- 接下来一行包含一个整数 $Q$ ，表示操作次数。
- 接下来一行包含 $Q$ 个整数，第 $i$ 个整数表示第 $i$ 次操作给出的 $X_i$ 。

> $N \quad M$
>
> $U_1 \quad V_1$
>
> $U_2 \quad V_2$
>
> $\ldots$
>
> $U_M \quad V_M$
>
> $Q$
>
> $X_1 \quad X_2 \quad \ldots \quad X_Q$

### Output

输出 $Q$ 行，第 $i$ 行包含第 $i$ 次操作后 $G$ 的边数。

### Sample Input 1

```txt showLineNumbers=false
7 7
1 2
1 3
2 3
1 4
1 5
2 5
6 7
5
1 2 3 1 5
```

### Sample Output 1

```txt showLineNumbers=false
4
3
3
3
2
```

## 题目要点解析

缩点+并查集

## 受限可达集问题

[题目链接](https://atcoder.jp/contests/abc401/tasks/abc401_e)

### Problem Statement

给定一张 $N$ 个顶点、$M$ 条边的无向图。顶点编号为 $1, 2, \ldots, N$ ，第 $i$ 条边（ $1 \leq i \leq M$ ）连接顶点 $u_i$ 与顶点 $v_i$ 。对于 $k = 1, 2, \ldots, N$ ，请解决以下问题：

考虑如下操作：

- 选择一个顶点，将该顶点以及与它相连的所有边从图中删除。

判断能否通过重复上述操作满足以下条件：

- 从顶点 $1$ 出发沿边可以到达的顶点集合，恰好由顶点 $1, 2, \ldots, k$ 这 $k$ 个顶点组成。

若可以做到，求出满足该条件至少需要执行多少次操作。

### Constraints

- $1 \leq N \leq 2 \times 10^5$
- $0 \leq M \leq 3 \times 10^5$
- $1 \leq u_i < v_i \leq N$

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $M$ ，分别表示顶点数和边数。
- 接下来 $M$ 行，第 $i$ 行包含两个整数，表示第 $i$ 条边连接的两个顶点。

> $N \quad M$
>
> $u_1 \quad v_1$
>
> $u_2 \quad v_2$
>
> $\ldots$
>
> $u_M \quad v_M$

### Output

输出 $N$ 行，第 $i$ 行表示 $k = i$ 时的答案，若无法满足条件时输出 `-1` ，否则输出满足条件所需的最少操作次数。

### Sample Input 1

```txt showLineNumbers=false
6 7
1 2
1 5
2 3
2 4
2 5
3 6
5 6
```

### Sample Output 1

```txt showLineNumbers=false
2
3
3
2
1
0
```

### Sample Input 2

```txt showLineNumbers=false
5 4
1 5
2 3
3 4
4 5
```

### Sample Output 2

```txt showLineNumbers=false
1
-1
-1
-1
0
```

### Sample Input 3

```txt showLineNumbers=false
2 0
```

### Sample Output 3

```txt showLineNumbers=false
0
-1
```

### Sample Input 4

```txt showLineNumbers=false
11 25
6 9
5 9
2 3
1 9
10 11
4 5
9 10
8 9
7 8
3 5
1 7
6 10
4 7
7 9
1 10
4 11
3 8
2 7
3 4
1 8
2 8
3 7
2 10
1 6
6 11
```

### Sample Output 4

```txt showLineNumbers=false
5
-1
-1
-1
-1
-1
4
3
2
1
0
```

## 题目要点解析

缩点+并查集

## 减少病毒的传播

[题目链接](https://leetcode.cn/problems/minimize-malware-spread-ii/description/)

### Problem Statement

给定一个由 $n$ 个节点组成的网络，用 $n \times n$ 的连通矩阵表示，节点编号为 $1$ 到 $n$ 。当且仅当 $a_{i, j} = 1$ 时，节点 $i$ 与节点 $j$ 直接相连。一些节点最初被恶意软件感染。

只要两个节点直接连接，且其中至少一个节点受到恶意软件的感染，那么两个节点都将被恶意软件感染。这种传播会一直持续，直到没有更多的节点可以通过这种方式被感染。

假设 $M$ 是恶意软件停止传播之后，整个网络中感染恶意软件的最终节点数。

我们可以从最初被感染的节点中 **删除一个节点** ，并完全移除从该节点出发到任何其他节点的所有连接。

请输出移除后能够使 $M$ 最小的节点编号。如果有多个节点满足条件，输出编号 **最小** 的节点。

### Constraints

- $2 \leq n \leq 300$
- $1 \leq k < n$
- $a_{i,j} \in \{0, 1\}$
- $1 \leq p_i \leq n$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示节点数。
- 接下来 $n$ 行，第 $i$ 行包含 $n$ 个整数，表示节点 $i$ 与其他节点之间的直接连接情况。
- 接下来一行包含一个整数 $k$ ，表示最初被感染的节点数。
- 接下来一行包含 $k$ 个整数，表示最初被感染的节点编号。

> $n$
>
> $a_{1,1} \quad a_{1,2} \quad \ldots \quad a_{1,n}$
>
> $a_{2,1} \quad a_{2,2} \quad \ldots \quad a_{2,n}$
>
> $\ldots$
>
> $a_{n,1} \quad a_{n,2} \quad \ldots \quad a_{n,n}$
>
> $k$
>
> $p_1 \quad p_2 \quad \ldots \quad p_k$

### Output

输出一个整数，表示移除后能使 $M$ 最小的节点编号。

### Sample Input 1

```txt showLineNumbers=false
3
1 1 0
1 1 0
0 0 1
2
1 2
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
3
1 1 0
1 1 1
0 1 1
2
1 2
```

### Sample Output 2

```txt showLineNumbers=false
2
```

### Sample Input 3

```txt showLineNumbers=false
4
1 1 0 0
1 1 1 0
0 1 1 1
0 0 1 1
2
1 2
```

### Sample Output 3

```txt showLineNumbers=false
2
```

## 题目要点解析

缩点+并查集

---

# 并查集传递性维护

维护集合元素的相对关系

种类并查集就是取模带权并查集

扩展域并查集可以被种类并查集替代

## 推导部分和问题

[题目链接](https://www.luogu.com.cn/problem/P8779)



## 题目要点解析

加法传递性并查集

## 除法的求值问题

[题目链接](https://leetcode.cn/problems/evaluate-division/description/)



## 题目要点解析

除法传递性并查集

## 异或带权并查集

[题目链接](https://www.luogu.com.cn/problem/CF776D)



## 题目要点解析

异或传递性并查集

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=116481593645927&bvid=BV1jJ96B3E8v&cid=37909759022&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 增量偶权环查询

[题目链接](https://leetcode.cn/problems/incremental-even-weighted-cycle-queries/description/)



## 题目要点解析



## 银河英雄的传说

[题目链接](https://www.luogu.com.cn/problem/P1196)



## 题目要点解析



## 甄别食物链问题

[题目链接](https://www.luogu.com.cn/problem/P2024)



## 题目要点解析

带权并查集（种类并查集）、扩展域并查集

## 最小的冲突分配

[题目链接](https://www.luogu.com.cn/problem/P1525)



## 题目要点解析

扩展域并查集

## 敌人敌人是朋友

[题目链接](https://www.luogu.com.cn/problem/P1892)



## 题目要点解析

扩展域并查集

## 区间的奇偶问题

[题目链接](https://www.luogu.com.cn/problem/P5937)



## 题目要点解析

真正的取模带权并查集，跟种类并查集和扩展域并查集有区别，但可以用扩展域并查集来做

---

# 参考文献引用列表

1. [【OI WiKi】并查集相关知识](https://oi-wiki.org/ds/dsu/)