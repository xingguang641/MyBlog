---
title: 【ACM 算法比赛】Codeforces Round 1117 div2
published: 2026-08-22
description: 记录一些 ACM 常规比赛
tags: [Algorithm, Contest, CodeForces]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://codeforces.com/contest/2257)

## Problem D

> `矩形覆盖` &nbsp;&nbsp; `前缀和技巧`

### Problem Statement

海狸正在横渡大洋，这一次它的目标是探索百慕大矩形。与百慕大三角不同，人们对百慕大矩形所知甚少。具体来说，海狸确信该矩形的面积为 $S$ ，其边长均为整数，且左下角位于点 $(0, 0)$ 。

海狸想知道，一个边长为 $x$ 和 $y$ 、左下角位于点 $(0, 0)$ 的矩形中，有多少个单元格可以位于百慕大矩形内部。若存在一个满足百慕大矩形给定约束的矩形包含该单元格，则认为该单元格位于百慕大矩形内部。

请帮助海狸快速回答询问，你需要回答 $q$ 次询问。

### Constraints

- $1 \leq t \leq 10^4$
- $1 \leq S \leq 10^{14}$
- $1 \leq q \leq 3 \times 10^5$
- $1 \leq x, y \leq S$
- 所有测试用例中 $q$ 的总和不超过 $3 \times 10^5$
- 所有测试用例中 $\sqrt{S}$ 的总和不超过 $10^7$

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

    - 第一行包含两个整数 $S$ 和 $q$ ，分别表示百慕大矩形的面积与询问次数。
    - 接下来 $q$ 行，每行包含两个整数 $x$ 和 $y$ ，表示一次询问。

> $S \quad q$
>
> $x_1 \quad y_1$
>
> $x_2 \quad y_2$
>
> $\ldots$
>
> $x_q \quad y_q$

### Output

对于每次询问，输出一行一个整数，表示该次询问的答案。

### Sample Input

```txt showLineNumbers=false
3
6 4
2 3
4 5
6 6
1 1
5 2
2 2
3 4
8 2
3 1
5 6
```

### Sample Output

```txt showLineNumbers=false
6
11
14
1
3
6
3
15
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem E

> `贪心算法`

### Problem Statement

海狸创立了一家名为「忙碌海狸」的建筑公司。如今，为了树立公司的声誉，它需要建造尽可能高的大楼。

公司拥有 $x$ 根胡萝卜的初始资本（对于海狸来说是一种非常珍贵的货币），以及 $n$ 个可供建造的项目。每个项目都分配了独立的场地，目前那里还什么都没有建成，一个建筑项目由一系列建造下一层楼的合同组成。

要建造第 $i$ 栋建筑的第 $j$ 层，需要花费 $a_{i, j}$ 根胡萝卜；建成后，公司会立即获得 $b_{i, j}$ 根胡萝卜，这些胡萝卜会被加入预算，公司可以将它们用于建造同一栋建筑的更高楼层，或者用于其他项目。由于公司还很年轻，并非所有合同都有利可图；换句话说，有可能出现 $a_{i, j} > b_{i, j}$ 的情况。

海狸雇佣你来规划公司的行动方案，你需要决定以什么顺序建造哪些楼层。注意，不必完成项目，甚至不必开始它们。此外，在建造同一栋建筑的不同楼层之间，允许完成任意数量与该建筑无关的合同。

主要目标是 —— 建造尽可能高的大楼。

### Constraints

- $1 \leq t \leq 3 \times 10^4$
- $1 \leq n \leq 2 \times 10^5$
- $0 \leq x \leq 10^{18}$
- $1 \leq m_i \leq 2 \times 10^5$
- $0 \leq a_{i, j}, b_{i, j} \leq 10^9$
- 所有测试用例中 $m_i$ 的总和不超过 $2 \times 10^5$

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

    - 第一行包含两个整数 $n$ 和 $x$ ，分别表示建筑项目的数量与初始资金。
    - 接下来 $n$ 行描述各个项目，对于第 $i$ 个项目：
        - 第一行包含一个整数 $m_i$ ，表示该建筑最多可建造的楼层数。
        - 第二行包含 $m_i$ 个整数，表示各楼层的建造花费。
        - 第三行包含 $m_i$ 个整数，表示各楼层完工后获得的收益。

> $n \quad x$
>
> $m_1$
>
> $a_{1, 1} \quad a_{1, 2} \quad \ldots \quad a_{1, m_1}$
>
> $b_{1, 1} \quad b_{1, 2} \quad \ldots \quad b_{1, m_1}$
>
> $m_2$
>
> $a_{2, 1} \quad a_{2, 2} \quad \ldots \quad a_{2, m_2}$
>
> $b_{2, 1} \quad b_{2, 2} \quad \ldots \quad b_{2, m_2}$
>
> $\ldots$
>
> $m_n$
>
> $a_{n, 1} \quad a_{n, 2} \quad \ldots \quad a_{n, m_n}$
>
> $b_{n, 1} \quad b_{n, 2} \quad \ldots \quad b_{n, m_n}$

### Output

对于每组输入数据，输出一行两个整数，表示该组数据的答案。

### Sample Input

```txt showLineNumbers=false
2
1 6
4
4 4 2 1
2 4 1 1
2 3
2
4 4
5 5
2
2 20
4 0
```

### Sample Output

```txt showLineNumbers=false
4 1
2 1
```

## Solution

打包处理

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```