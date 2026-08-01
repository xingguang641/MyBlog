---
title: 【ACM 算法比赛】2026牛客暑期多校训练营01
published: 2026-07-31
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

[比赛链接](https://ac.nowcoder.com/acm/contest/133876)

## Problem F Nowcoder

[题目链接](https://ac.nowcoder.com/acm/contest/133876/F)

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

## 题目要点解析

由于公式中的Pi - Pj双重求和记录的是所有元素的相对大小信息，因此同时对每个元素加上一个数不会改变这个函数值，但由于题目要求输出的是排列，因此光添加一个数不行，但是题目中要求的是函数值模n意义下相同，因此可以对每个数添加一个常数并模n，使得新排列的第k位等于x即可。

如果题目加上绝对值就能消解方向性，从而要求中的mod n就可以删除，如果题目改成加法，虽然所有元素增加一个数会导致f值改变，但是每个元素增加一个数的同时mod n不会改变f值，此时mod n也不需要。

（加法特别写一下思路）

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