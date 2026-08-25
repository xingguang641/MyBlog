---
title: 【ACM 算法比赛】2026牛客暑期多校训练营01
published: 2026-07-31
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://ac.nowcoder.com/acm/contest/133876)

## Problem F

### Problem Statement

对于一个由 $0$ 到 $n-1$ 组成的排列 $P$ ，定义其价值为：

$$
f(P)=\sum_{0 \leq i < j < n}(P_j-P_i)
$$

给定一个由 $0$ 到 $n-1$ 组成的排列 $P$ ，以及两个整数 $k$ 和 $x$ 。

请构造一个排列 $P'$ ，满足：

- $P'_k = x$ ，即下标为 $k$ 的位置上的元素为 $x$（下标从 $0$ 开始）
- $f(P') \equiv f(P) \pmod n$

如果存在满足条件的排列 $P'$ ，输出任意一个合法排列。如果不存在，输出 $-1$ 。

### Constraints

- $1 \leq n \leq 2 \times 10^5$
- $0 \leq k,x < n$

### Input

输入包含两行：

- 第一行包含三个整数 $n$ 、$k$ 和 $x$ 。
- 第二行包含 $n$ 个整数 $P_0, P_1, \ldots, P_{n-1}$ ，表示给定的排列。

> $n \quad k \quad x$
>
> $P_0 \quad P_1 \quad \ldots \quad P_{n-1}$

### Output

如果不存在满足条件的排列，输出一个整数 `-1` ；否则输出一行包含 $n$ 个整数，表示构造出的排列 $P'$ 。

### Sample Input

```txt showLineNumbers=false
4 1 3
2 0 1 3
```

### Sample Output

```txt showLineNumbers=false
0 3 1 2
```

## Solution

由于公式中的 $P_j - P_i$ 实际上记录的是两个元素之间的 **相对信息** ，因此对所有元素同时增加一个相同的数并不会改变这种相对信息。对所有元素同时增加常数 $c$ ，两个元素之间的差值保持不变：

$$
(P_j + c) - (P_i + c) = P_j - P_i
$$

因此直接对所有元素同时增加一个常数，就可以调整元素值的同时保持 $f(P)$ 不变。但这样变换后并不能保证所有元素仍在 $0$ 到 $n-1$ 的范围内，因此 **无法得到** 一个合法排列。

注意到题目要求构造出的排列需要满足：

$$
f(P') \equiv f(P) \pmod n
$$

由于模 $n$ 运算不会影响这种相对信息在模 $n$ 意义下的结果，因此可以令：

$$
P'_i = (P_i + c) \bmod n
$$

这样得到的 $P'$ 仍然是一个排列，并且对于任意 $i < j$ 都有：

$$
P'_j - P'_i \equiv P_j - P_i \pmod n
$$

接下来需要选择合适的常数 $c$ 使第 $k$ 个位置上的元素变为 $x$ ：

$$
P'_k = (P_k + c) \bmod n = x
$$

为了使上式成立，需要令：

$$
c = (x - P_k + n) \bmod n
$$

将这个常数应用到所有元素上，即可按照相同的规则构造出新的排列，并同时满足题目中的两个条件。整个构造过程只需要遍历一次排列，因此时间复杂度为 $O(n)$ ，空间复杂度为 $O(n)$ 。

如果将公式中的减法改成加法，例如定义：

$$
g(P) = \sum_{0 \leq i < j < n}(P_j + P_i)
$$

此时对所有元素同时增加 $c$ ，每一对元素的贡献都会增加 $2c$ 。由于一共有 $C_n^2$ 对元素，因此总增量为：

$$
2c \times C_n^2 = 2c \times \frac{n(n-1)}{2} = cn(n-1)
$$

这个增量是 $n$ 的倍数，因此有：

$$
g(P') \equiv g(P) \pmod n
$$

也就是说，加法形式下整体增加常数虽然会改变函数值，但变化量是 $n$ 的倍数，因此模 $n$ 意义下仍保持不变。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 2e5 + 100;
int n, k, x; int arr[MAXN];

int main() {
    cin >> n >> k >> x;
    for (int i = 0; i < n; i++){
        cin >> arr[i];
    }
    
    int d = ((x - arr[k]) % n + n) % n;
    for (int i = 0; i < n; i++){
        cout << (arr[i] + d) % n << " ";
    }
}
```

## Problem C

### Problem Statement

给定一个 $n \times m$ 的网格，其中部分格子中存在鱼，其余格子为障碍物。网格中有一条鱼由你控制，可以反复将它移动到相邻格子，即上、下、左、右四个方向，但不能移出网格。如果目标格子是障碍物，则可以直接移动到该格子。如果目标格子中存在一条大小严格小于当前鱼的鱼，则可以吃掉该鱼，并使自身大小增加 $1$。

初始时所有格子均为障碍物，接下来按顺序进行 $q$ 次操作，每次操作为以下两种类型之一：

- 给定 $x, y, v$ ，移除位置 $(x, y)$ 处的障碍物，并在该位置放置一条大小为 $v$ 的鱼。求这条鱼在由你控制的情况下最多可以吃掉多少条鱼。保证 $(x,y)$ 当前为障碍物，并且 $v$ 不小于此前放置的所有鱼的大小。

- 给定 $x, y$ ，假设在进行上述过程之前，可以将位置 $(x, y)$ 处的鱼的初始大小增加一个非负整数。设通过任意增加后的大小，这条鱼最多可以吃掉 $k$ 条鱼，求使其能够吃掉 $k$ 条鱼所需增加的最小大小。

对于以上两种操作，吃鱼过程均为假设进行，不会改变网格中已经放置的鱼的实际状态。

### Constraints

- $1 \leq n, m \leq 2.5 \times 10^5$
- $1 \leq q \leq 5 \times 10^5$
- $1 \leq v \leq 10^9$
- 其中 $n \times m \leq 2.5 \times 10^5$

### Input

输入包含多行：

- 第一行包含三个整数 $n$ 、$m$ 和 $q$ ，分别表示网格的行数、列数以及操作次数。
- 接下来 $q$ 行，每行描述一次操作。对于每次操作，给定经过加密的坐标 $x'$ 和 $y'$ 。设上次操作的输出为 $l$ ，对于第一次操作有 $l = 0$ ，实际坐标通过以下方式计算：

    $$
    x = x'\oplus l \qquad y = y'\oplus l
    $$

    其中 $\oplus$ 表示按位异或运算，并保证 $1 \leq x \leq n$ 且 $1 \leq y \leq m$ 。

    操作分为以下两种类型：

    - `1 x' y' v`：计算实际坐标 $(x, y)$ 。移除位置 $(x, y)$ 的障碍物并在该处放置一条大小为 $v$ 的鱼，求这条鱼最多可以吃掉多少条鱼。保证 $(x, y)$ 当前为障碍物，并且 $v$ 不小于此前放置的所有鱼的大小。
    - `2 x' y'`：计算实际坐标 $(x, y)$ 。假设在进行吃鱼过程前，可以将位置 $(x, y)$ 的鱼的初始大小增加一个非负整数。设其最多可以吃掉的鱼数量为 $k$ ，求使其能够吃掉 $k$ 条鱼所需增加的最小大小。

    其中类型为 $1$ 的操作中的 $v$ 不需要进行加密。

> $n \quad m \quad q$
>
> $1 \quad x' \quad y' \quad v$
>
> $2 \quad x' \quad y'$

### Output

输出 $q$ 行，每行包含一个整数，表示对应操作的答案。

### Sample Input

```txt showLineNumbers=false

2 3 9
1 1 2 1
1 2 1 1
1 2 1 2
2 1 2
1 1 3 8
2 2 1
1 1 1 9
2 2 2
2 1 3
```

### Sample Output

```txt showLineNumbers=false

0
0
2
1
3
5
4
4
0
```

## Solution

Kruskal 重构树

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem L



## Solution

AC 自动机

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem H



## Solution

随机博弈 DP + MDP 优化

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```