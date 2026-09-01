---
title: 【ACM 算法比赛】2026 牛客暑期多校训练营 04
published: 2026-08-11
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://ac.nowcoder.com/acm/contest/133879)

## Problem B

### Problem Statement

给定一个正整数 $p$ ，你的任务是找出三个正整数 $x_1$ 、$x_2$ 和 $q$ 使得：

1. $1 \leq x_1 < q$ 且 $1 \leq x_2 < p$ 。
2. $x_1^2 \equiv p \pmod q$ 。
3. $x_2^2 \equiv q \pmod p$ 。

这里 $a \equiv b \pmod c$ 表示 $a$ 除以 $c$ 的余数与 $b$ 除以 $c$ 的余数相同。

如果存在多个解，输出任意一组合法的整数解 $(x_1, x_2, q)$ 即可。如果不存在这样的整数，报告无解。

### Constraints

- $1 \leq T \leq 10^4$
- $2 \leq p \leq 10^9$
- $1 \leq q \leq 10^{12}$

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

    - 第一行包含一个整数 $p$ 。

> $p$

### Output

对于每个测试用例，输出一行三个整数 $x_1$ 、$x_2$ 和 $q$（ $1 \leq q \leq 10^{12}$ ，$1 \leq x_1 < q$ ，$1 \leq x_2 < p$ ），表示任意一组合法的整数解，若不存在解则输出字符串 `Impossible` 。

### Sample Input

```txt showLineNumbers=false
3
2
5
6
```

### Sample Output

```txt showLineNumbers=false
12 1 71
19 2 89
12 3 69
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem D

### Problem Statement

Alice 和 Bob 在玩一个游戏，Alice 先手。初始有一个空序列，给定一个整数 $n$ ，他们将共同构建一个长度为 $n$ 的排列 $p$ 。每次操作中，当前玩家从 $1$ 到 $n$ 中选择一个之前未被选择过的整数，并将其追加到序列的末尾。恰好经过 $n$ 次操作后，序列变成 $1, 2, \ldots, n$ 的一个排列 $p$ 。

排列 $p = (p_1, p_2, \ldots, p_n)$ 的循环移位是指通过选择一个索引 $i$ 并写作 $(p_i, p_{i + 1}, \ldots, p_n, p_1, p_2, \ldots, p_{i - 1})$ 所得到的序列。例如 $(2, 3, 1)$ 的循环移位为 $(2, 3, 1)$ 、$(3, 1, 2)$ 和 $(1, 2, 3)$ 。

对于一个排列 $p$ ，定义 $f(p)$ 为 $p$ 的所有循环移位中字典序最小的那一个。

Alice 希望使 $f(p)$ 的字典序尽可能小，而 Bob 希望使 $f(p)$ 的字典序尽可能大。

假设双方均采取最优策略，求最终得到的排列 $f(p)$ 。

### Constraints

- $1 \leq T \leq 10^5$
- $1 \leq n \leq 5 \times 10^5$
- 所有测试用例中 $n$ 的总和不超过 $5 \times 10^5$

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

    - 第一行包含一个整数 $n$ 。

> $n$

### Output

对于每个测试用例，输出 $n$ 个整数，表示双方采取最优策略时最终得到的排列 $f(p)$ 。

### Sample Input

```txt showLineNumbers=false
4
1
2
3
4
```

### Sample Output

```txt showLineNumbers=false
1
1 2
1 3 2
1 3 2 4
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem F

### Problem Statement

定义一个序列 $b = (b_1, b_2, \ldots, b_m)$ 是 **好的** ，当且仅当对于每个 $i = 2, 3, \ldots, m$ 满足：

$$
2 \cdot b_{i - 1} \leq b_i \leq 3 \cdot b_{i - 1}
$$

特别地，任何长度为 $1$ 的序列总是好的。

给定一个长度为 $n$ 的正整数序列 $a = (a_1, a_2, \ldots, a_n)$ ，你需要回答 $q$ 次询问，每次询问给定一个区间 $[l, r]$ 。

对于每次询问，求在保持原顺序的情况下，区间 $[l, r]$ 中最长 **好的** 子序列的长度。

### Constraints

- $1 \leq n, q \leq 2 \times 10^5$
- $1 \leq a_i \leq 10^{18}$
- $1 \leq l \leq r \leq n$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $q$ ，分别表示序列的长度和询问的数量。
- 第二行包含 $n$ 个整数 $a_1, \, a_2, \, \ldots, \, a_n$ 。
- 接下来 $q$ 行，每行包含两个整数 $l$ 和 $r$ ，表示一次询问的区间。

> $n \quad q$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$
>
> $l_1 \quad r_1$
>
> $l_2 \quad r_2$
>
> $\ldots$
>
> $l_q \quad r_q$

### Output

输出 $q$ 行，每行包含一个整数，表示每次询问的答案。

### Sample Input

```txt showLineNumbers=false
5 4
1 2 4 6 17
1 3
2 4
1 5
1 4
```

### Sample Output

```txt showLineNumbers=false
3
2
4
3
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem C

### Problem Statement

在一场大型比赛结束后，评测集群需要进行最后一次复核：在相同的 $m$ 个测试点上重新运行 $n$ 个程序。

所有程序使用相同的测试点队列，当评测机处理一个程序时，它会从队列头部开始按顺序运行测试点。一旦某个测试点返回拒绝（Rejected）结果，评测机在运行完该测试点后会立即停止。被所有测试点通过（Accepted）的程序则会正常运行完整个测试点队列才会结束。

在复核开始之前，历史日志中已经记录了每个程序在每个测试点上的表现。程序 $i$ 在测试点 $j$ 上运行需要耗费 $d_{i, j}$ 的时间，结果要么是通过，要么是被拒绝。无论测试点运行结果如何，耗时 $d_{i, j}$ 都会累加到集群的总时间中。

在复核之前，你可以任意重新排列这 $m$ 个测试点的顺序。请找出完成所有 $n$ 个程序评测所需的最短总时间。

### Constraints

- $1 \leq n \leq 2 \times 10^4$
- $1 \leq m \leq 20$
- $1 \leq d_{i, \, j} \leq 10^9$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $m$ ，分别表示程序数量和测试点数量。
- 接下来 $n$ 行，每行包含 $m$ 个整数和一个长度为 $m$ 的字符串 $s_i$ 。如果 $s_i$ 的第 $j$ 个字符是 `A` ，表示程序 $i$ 通过了测试点 $j$ ；如果是 `R` ，则表示程序 $i$ 在测试点 $j$ 上被拒绝。

> $n \quad m$
>
> $d_{1, 1} \quad d_{1, 2} \quad \ldots \quad d_{1, m} \quad s_1$
>
> $d_{2, 1} \quad d_{2, 2} \quad \ldots \quad d_{2, m} \quad s_2$
>
> $\ldots$
>
> $d_{n, 1} \quad d_{n, 2} \quad \ldots \quad d_{n, m} \quad s_n$

### Output

输出一个整数，表示可能的最短总时间。

### Sample Input

```txt showLineNumbers=false
3 3
3 10 2 ARA
5 1 4 RAA
2 2 7 AAR
```

### Sample Output

```txt showLineNumbers=false
27
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem E

### Problem Statement

给定一个包含 $n$ 个顶点和 $m$ 条有向边的强连通带权有向图。顶点从 $1$ 到 $n$ 编号，边从 $1$ 到 $m$ 编号。

第 $k$ 条边表示为 $(u_k, v_k, w_k)$ ，即存在一条从 $u_k$ 到 $v_k$ 、边权为 $w_k$ 的有向边。

设 $dis(i, j)$ 表示从顶点 $i$ 到顶点 $j$ 的最短路径长度。对于一个图，定义其 **权值** 为：

$$
\max_{\substack{1 \leq i, j \leq n \\ i \neq j}} \frac{dis(i, j)}{dis(j, i)}
$$

现有 $q$ 次询问。每次询问给定一个边索引 $k$ 和一个新的边权 $x$（满足 $1 \leq x < w_k$ ）。仅在此次询问中，第 $k$ 条边的边权被临时修改为 $x$ 。你需要输出修改后图的权值。

所有询问是独立的，即每次询问结束后，图都会恢复到原始状态。

### Constraints

- $1 \leq T \leq 1000$
- $2 \leq n \leq m \leq 2000$
- $1 \leq q \leq 2000$
- $\sum n, \sum m, \sum q \leq 2000$
- $1 \leq k \leq m$
- $1 \leq u_k, v_k \leq n$
- $1 \leq x < w_k \leq 10^9$
- 绝对或相对误差不超过 $10^{-6}$

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

    - 第一行包含三个整数 $n$ 、$m$ 和 $q$ 。
    - 接下来 $m$ 行，每行包含三个整数 $u_k$ 、$v_k$ 和 $w_k$ 。
    - 接下来 $q$ 行，每行包含两个整数 $k$ 和 $x$ 。

> $n \quad m \quad q$
>
> $u_1 \quad v_1 \quad w_1$
>
> $u_2 \quad v_2 \quad w_2$
>
> $\ldots$
>
> $u_m \quad v_m \quad w_m$
>
> $k_1 \quad x_1$
>
> $k_2 \quad x_2$
>
> $\ldots$
>
> $k_q \quad x_q$

### Output

对于每次询问，输出一行包含一个实数，表示所有满足 $i \neq j$ 的有序对 $(i, j)$ 中 $\displaystyle \frac{dis(i, j)}{dis(j, i)}$ 的最大值。

### Sample Input

```txt showLineNumbers=false
2
3 3 2
1 2 2
2 3 3
3 1 4
2 1
1 1
5 7 4
1 2 7
1 4 3
2 3 4
4 1 2
1 5 5
5 2 6
3 1 8
5 3
6 5
1 4
3 2
```

### Sample Output

```txt showLineNumbers=false
6.0000000000
7.0000000000
6.0000000000
3.7500000000
3.6000000000
7.5000000000
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem H

### Problem Statement

给定 $n$ 个字符串 $s_1, s_2, \ldots, s_n$ 。

你可以按任意顺序重新排列这 $n$ 个字符串，并将它们按该顺序拼接起来得到一个字符串 $S$ 。

对于从 $0$ 到 $L$ 的每个整数 $k$（其中 $\displaystyle L = \sum_{i = 1}^{n} |s_i|$ ），在每次独立询问中，你都可以按任意顺序重新排列这 $n$ 个字符串，将其拼接得到字符串 $S$ ，然后最多修改 $S$ 中的 $k$ 个字符。在一次修改中，你可以将 $S$ 中的一个字符替换为另一个小写英文字母。你的任务是对于从 $0$ 到 $L$ 的每个 $k$ ，求出可以获得的字典序最小的字符串。

### Constraints

- $1 \leq T \leq 500$
- $1 \leq n \leq 500$
- $\displaystyle L = \sum_{i = 1}^{n} |s_i|$
- $s_i$ 仅由小写英文字母组成
- 所有测试用例中 $n$ 的总和不超过 $500$
- 所有测试用例中 $L$ 的总和不超过 $500$

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

    - 第一行包含一个整数 $n$ ，表示字符串的数量。
    - 第二行包含 $n$ 个非空字符串 $s_1, \, s_2, \, \ldots, \, s_n$ 。

> $n$
>
> $s_1 \quad s_2 \quad \ldots \quad s_n$

### Output

对于每个测试用例，输出 $L + 1$ 行，第 $k$ 行输出通过最多修改 $k$ 个字符所能得到的字典序最小的字符串。

### Sample Input

```txt showLineNumbers=false
3
5
bca a zz ab c
4
ba b aa aba
3
az za m
```

### Sample Output

```txt showLineNumbers=false
aabbcaczz
aaabbcazz
aaaaabczz
aaaaaabbz
aaaaaaabc
aaaaaaaab
aaaaaaaaa
aaaaaaaaa
aaaaaaaaa
aaaaaaaaa
aaababab
aaaaabab
aaaaaaab
aaaaaaaa
aaaaaaaa
aaaaaaaa
aaaaaaaa
aaaaaaaa
aaaaaaaa
azmza
aaazm
aaaam
aaaaa
aaaaa
aaaaa
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```