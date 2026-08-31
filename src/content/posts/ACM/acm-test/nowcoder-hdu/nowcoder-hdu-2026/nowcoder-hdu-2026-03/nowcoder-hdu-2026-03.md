---
title: 【ACM 算法比赛】2026 牛客暑期多校训练营 03
published: 2026-08-05
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://ac.nowcoder.com/acm/contest/133878)

## Problem A

### Problem Statement

对于非负整数 $x$ ，定义 $f(x)$ 为 $x$ 在无前导零的二进制表示中极大幅度连续 $1$ 段的数量。例如 $f(23) = 2$ ，因为 $23 = (10111)_2$ ，其二进制表示中包含 $2$ 个连续的 $1$ 段。

给定 $n$ 个整数 $a_1, a_2, \ldots, a_n$ ，你需要处理 $m$ 次操作。每次操作由两个整数 $type$ 和 $x$ 描述：

- 若 $type = 1$ ，将每个 $a_i$ 替换为 $a_i \mathbin{\&} x$ 。
- 若 $type = 2$ ，将每个 $a_i$ 替换为 $a_i \mid x$ 。
- 若 $type = 3$ ，将每个 $a_i$ 替换为 $a_i \oplus x$ 。

这里 $\mathbin{\&}$ 表示按位与运算，$\mid$ 表示按位或运算，$\oplus$ 表示按位异或运算。

每次操作后，输出当前 $\displaystyle \sum_{i = 1}^{n} f(a_i)$ 的值。

### Constraints

- $1 \leq n \leq 3 \times 10^5$
- $0 \leq a_i < 2^{30}$
- $1 \leq m \leq 3 \times 10^5$
- $1 \leq type \leq 3$
- $0 \leq x < 2^{30}$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示数组的长度。
- 第二行包含 $n$ 个整数 $a_1, a_2, \ldots, a_n$ 。
- 第三行包含一个整数 $m$ ，表示操作的次数。
- 接下来 $m$ 行，每行包含两个整数 $type$ 和 $x$ 。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$
>
> $m$
>
> $type_1 \quad x_1$
>
> $type_2 \quad x_2$
>
> $\ldots$
>
> $type_m \quad x_m$

### Output

输出 $m$ 行，每行包含一个整数，表示第 $j$ 次操作后 $\sum f(a_i)$ 的值。

### Sample Input

```txt showLineNumbers=false
4
3 5 6 10
4
1 7
2 8
3 15
2 3
```

### Sample Output

```txt showLineNumbers=false
5
7
5
4
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem B

### Problem Statement

一瓶饮料的价格为 $1$ 美元。小明每喝完一瓶饮料，有 $a \mathbin{/} b$ 的概率中奖。如果中奖，他将获得 $c$ 美元，否则什么也得不到。获得的奖金可以用来购买更多的饮料，每瓶饮料的中奖事件彼此独立。

初始时小明有 $n$ 美元，求他在恰好喝完 $m$ 瓶饮料后花光所有钱并停止的概率。

你需要输出一个整数 $x$（ $0 \leq x < 998 244 353$ ），使得 $q \times x \equiv p \pmod{998 244 353}$ 。

### Constraints

- $1 \leq T \leq 200 000$
- $1 \leq n, m, c \leq 2 000 000$
- $0 \leq a < b < 998 244 353$

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

    - 第一行包含五个整数 $n$ 、$m$ 、$c$ 、$a$ 和 $b$ 。

> $n \quad m \quad c \quad a \quad b$

### Output

对于每个测试用例，输出一行一个整数，表示答案对 $998 244 353$ 取模后的结果。

### Sample Input

```txt showLineNumbers=false
4
1 1 2 1 2
1 3 2 1 2
2 2 3 1 3
1 2 2 1 2
```

### Sample Output

```txt showLineNumbers=false
499122177
873463809
776412275
0
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem G

### Problem Statement

给定一个 $n \times m$ 的网格，每个单元格中包含一个正整数。

如果存在两个单元格 $(r_1, c_1)$ 和 $(r_2, c_2)$ 满足 $r_1 < r_2$ 且 $c_1 < c_2$ ，并且这两个单元格中的数字相等，则满足 $r_1 \leq r \leq r_2$ 且 $c_1 \leq c \leq c_2$ 的每个单元格 $(r, c)$ 都会被标记。

输出整个网格最终的标记情况。

### Constraints

- $1 \leq n, m$
- $n \times m \leq 1 000 000$
- $1 \leq a_{i, j} \leq n \times m$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $m$ 。
- 接下来 $n$ 行，每行包含 $m$ 个整数，第 $i$ 行包含 $a_{i, 1}, a_{i, 2}, \ldots, a_{i, m}$ 。

> $n \quad m$
>
> $a_{1, 1} \quad a_{1, 2} \quad \ldots \quad a_{1, m}$
>
> $a_{2, 1} \quad a_{2, 2} \quad \ldots \quad a_{2, m}$
>
> $\ldots$
>
> $a_{n, 1} \quad a_{n, 2} \quad \ldots \quad a_{n, m}$

### Output

输出 $n$ 行，每行包含一个长度为 $m$ 且仅由字符 `'0'` 和 `'1'` 组成的字符串。

### Sample Input

```txt showLineNumbers=false
2 6
1 2 3 4 5 6
7 8 9 3 4 10
```

### Sample Output

```txt showLineNumbers=false
001110
001110
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

给定一个 $n \times m$ 的网格。你需要向每个单元格中填入一个来自 $\{0, 1, 2\}$ 的整数。

如果任意两个相邻（共享一条边）的单元格中填入的整数都不相同，则称该填法是合法的。

输出合法填法的总数对 $998 244 353$ 取模后的结果。

### Constraints

- $1 \leq n < 10$
- $1 \leq m < 998 244 353$

### Input

输入仅包含一行：

> $n \quad m$

### Output

输出一个整数，表示答案对 $998 244 353$ 取模后的结果。

### Sample Input

```txt showLineNumbers=false
2 2
```

### Sample Output

```txt showLineNumbers=false
18
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem J

### Problem Statement

给定一棵以节点 $1$ 为根的树，顶点编号为 $1$ 到 $n$ 。

你需要构建一棵新树，新树同样以节点 $1$ 为根且包含相同的 $n$ 个节点，并满足以下条件：对于每个节点 $x \neq 1$ ，它在新树中的父节点必须是它在原树中的祖先。

此外还给定了 $q$ 个限制条件，每个限制条件的形式为 $(u, v)$ ，表示在新树中 $u$ 必须是 $v$ 的后代。

设 $dep_i$ 表示节点 $i$ 在新树中的深度，其中根节点 $1$ 的深度为 $0$ 。请最小化 $\displaystyle \sum_{i = 1}^{n} dep_i$ ，并输出该最小值。

### Constraints

- $2 \leq n \leq 500 000$
- $0 \leq q \leq 500 000$
- $1 \leq p_i < i$
- $1 < u \leq n$
- $1 \leq v \leq n$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $q$ 。
- 接下来 $n - 1$ 行，第 $i - 1$ 行包含一个整数 $p_i$ ，表示在原树中节点 $i$ 的父节点为 $p_i$ 。
- 接下来 $q$ 行，每行包含两个整数 $u$ 和 $v$ ，表示一个限制条件。

> $n \quad q$
>
> $p_2$
>
> $p_3$
>
> $\ldots$
>
> $p_n$
>
> $u_1 \quad v_1$
>
> $u_2 \quad v_2$
>
> $\ldots$
>
> $u_q \quad v_q$

### Output

输出一个整数，表示 $\sum dep_i$ 可能的最小值。

### Sample Input

```txt showLineNumbers=false
7 4
1
2
3
3
2
6
4 2
4 3
5 2
7 2
```

### Sample Output

```txt showLineNumbers=false
11
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem I

### Problem Statement

对于一个数组 $a_1, a_2, \ldots, a_n$ ，定义其值为 $\displaystyle \sum_{i = 1}^{n - 1} |a_i - a_{i + 1}|$ 。

你可以选择两个不同的位置并交换这两处的元素，最多执行此操作一次。

求交换后数组可能达到的最大值。

### Constraints

- $1 \leq T \leq 100$
- $2 \leq n \leq 5 \times 10^5$
- $0 \leq a_i \leq 10^9$
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

    - 第一行包含一个整数 $n$ ，表示数组的长度。
    - 第二行包含 $n$ 个整数 $a_1, a_2, \ldots, a_n$ 。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

对于每个测试用例，输出一行一个整数，表示在最多执行一次交换后数组可能达到的最大值。

### Sample Input

```txt showLineNumbers=false
3
5
1 3 2 7 4
4
5 5 5 5
6
10 1 10 1 10 1
```

### Sample Output

```txt showLineNumbers=false
14
0
45
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem M

### Problem Statement

给定一棵包含 $n$ 个顶点的树。一名流浪者从顶点 $s$ 出发，希望到达顶点 $t$ 。流浪者希望尽量避免走回头路，但他的记忆力较差，只能记住自己上一步所在的位置。

若 $s = t$ ，旅程立即结束，移动步数为 $0$ 。否则，流浪者将按照以下规则移动：

- 在第一步中，他从与 $s$ 相邻的顶点中等概率随机选择一个并移动过去。
- 在后续的每一步中，假设他当前处于顶点 $x$ ，且上一步处于顶点 $y$ 。若 $x$ 的度数大于 $1$ ，他会在与 $x$ 相邻且不为 $y$ 的顶点中等概率随机选择一个并移动过去；若 $x$ 的度数等于 $1$ ，他只能返回顶点 $y$ 。
- 一旦流浪者到达顶点 $t$ ，旅程立即结束。

求旅程期望步数对 $998 244 353$ 取模后的结果。

### Constraints

- $1 \leq T \leq 100$
- $2 \leq n \leq 5 \times 10^5$
- $1 \leq s, t \leq n$
- $1 \leq p_i < i$
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

    - 第一行包含三个整数 $n$ 、$s$ 和 $t$ 。
    - 第二行包含 $n - 1$ 个整数 $p_2, p_3, \ldots, p_n$ ，表示在顶点 $i$ 与 $p_i$ 之间存在一条边。

> $n \quad s \quad t$
>
> $p_2 \quad p_3 \quad \ldots \quad p_n$

### Output

对于每个测试用例，输出一行一个整数，表示期望步数对 $998 244 353$ 取模后的结果。

### Sample Input

```txt showLineNumbers=false
4
4 2 4
1 2 3
3 2 1
1 2
3 3 1
1 2
4 1 2
1 1 1
```

### Sample Output

```txt showLineNumbers=false
3
2
2
665496239
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 参考文献列表

1. [【Luogu 博客】随机游走](https://www.luogu.com.cn/article/pl73yj93)