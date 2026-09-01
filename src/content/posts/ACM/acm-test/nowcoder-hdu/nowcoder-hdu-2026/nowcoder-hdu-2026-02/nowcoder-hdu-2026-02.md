---
title: 【ACM 算法比赛】2026 牛客暑期多校训练营 02
published: 2026-08-01
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://ac.nowcoder.com/acm/contest/133877)

## Problem N

### Problem Statement

给定一个长度为 $n$ 的数组 $a$ 。一次操作中，你可以选择数组中的任意 $k$ 个元素，并将这 $k$ 个元素全部替换为它们的中位数。你必须恰好执行一次操作，请求出操作后数组所有元素之和的最大值。

### Constraints

- $1 \leq T \leq 10^4$
- $1 \leq k \leq n \leq 2 \times 10^5$
- $1 \leq a_i \leq 10^9$
- 所有测试用例中 $n$ 的总和不超过 $2 \times 10^5$

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

  - 第一行包含两个整数 $n$ 和 $k$ ，分别表示数组长度和选择元素的数量。
  - 第二行包含 $n$ 个整数，表示数组中的元素。

> $n \quad k$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

对于每个测试用例，输出一行一个整数，表示执行一次操作后数组元素和的最大值。

### Sample Input

```txt showLineNumbers=false
2
6 3
1 1 4 5 1 4
4 2
1 3 6 10
```

### Sample Output

```txt showLineNumbers=false
19
20
```

## Solution

枚举中位数，前半部分尽量小，变大之后收益就大，后半部分尽量小，变小之后亏损就小

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 2e5 + 100;
ll a[MAXN], s[MAXN];

int main(){
    int T; cin >> T;
    while(T--){
        int n, k; cin >> n >> k;
        for(int i = 1; i <= n; i++) cin >> a[i];
        sort(a + 1 , a + n + 1);
        for(int i = 1; i <= n; i++) s[i] = s[i - 1] + a[i];

        ll ans = 0;
        if (k % 2 == 1){
            int half = (k + 1) / 2;
            for (int i = half; i + k - half <= n; i++){
                ll leftSum = s[half - 1];
                ll rightSum = s[i + k - half] - s[i - 1];
                ll cur = s[n] + k * a[i] - leftSum - rightSum;
                ans = max(ans, cur);
            }
        }else{
            int half = k / 2;
            for (int i = half; i + half <= n; i++){
                ll leftSum = s[half - 1];
                ll rightSum = s[i + half] - s[i - 1];
                ll cur = s[n] + k * (a[i] + a[i + 1]) / 2 - leftSum - rightSum;
                ans = max(ans, cur);
            }
        }

        cout << ans << endl;
    }
}
```

## Problem B

### Problem Statement

给定一个非负整数数组 $a$ 。你需要将数组中的所有元素分配到两个空的多重集合 $A$ 和 $B$ 中。

最终得分为两个多重集合异或值之和：

$$
xor(A) + xor(B)
$$

请你求出可能得到的最大得分。

### Constraints

- $1 \leq T \leq 10^4$
- $1 \leq n \leq 5 \times 10^5$
- $0 \leq a_i < 2^{30}$
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

  - 第一行包含一个整数 $n$ ，表示数组长度。
  - 第二行包含 $n$ 个整数，表示数组中的元素。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

对于每个测试用例，输出一行一个整数，表示可以得到的最大得分。

### Sample Input

```txt showLineNumbers=false
4
1
1
3
1 2 3
4
1 1 3 3
4
1 2 2 3
```

### Sample Output

```txt showLineNumbers=false
1
6
6
4
```

## Solution

异或线性基

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem G

### Problem Statement

给定一个包含无限个顶点的有向图，顶点用正整数 $1, 2, \ldots$ 编号。

对于任意满足 $1 \leq i < j$ 的整数对 $(i, j)$ ，存在一条从 $i$ 指向 $j$ 的有向边，其边权为 $w_{i, j} = \gcd(i, j)$ ，即从 $i$ 到达 $j$ 需要支付 $w_{i, j}$ 的代价。图中不存在其他边。

对于任意满足 $1 \leq u < v$ 的整数对 $(u, v)$ ，定义 $cost(u, v)$ 为经过一条或多条边从 $u$ 到达 $v$ 的最小代价。

给定参数 $l, r, n$ ，请计算以下表达式的值：

$$
\sum_{i = l}^{r} cost(i, n)
$$

### Constraints

- $1 \leq T \leq 100$
- $1 \leq l \leq r < n \leq 10^7$

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

    - 第一行包含三个整数 $l$ 、$r$ 和 $n$ 。

> $l \quad r \quad n$

### Output

对于每个测试用例，输出一行一个整数，表示 $\sum cost(i, n)$ 的值。

### Sample Input

```txt showLineNumbers=false
3
1 5 6
2 33 36
1 99 100
```

### Sample Output

```txt showLineNumbers=false
8
54
158
```

## Solution

神秘题目，有取巧做法和反演做法

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem L

### Problem Statement

Sean 被要求对长度为 $n$ 的排列进行洗牌。一个排列是长度为 $n$ 且包含 $1$ 到 $n$ 中每个数字恰好一次的整数序列。

他的主管通过比较洗牌前后排列的逆序对数量来检查他的工作，即定义一个排列 $A$ 的逆序对数量为：

$$
f(A) = \sum_{1 \leq i < j \leq n} \mathbb{1}_{A_i > A_j}
$$

假设洗牌前后的排列分别为 $A$ 和 $A'$ ，主管通过计算以下值来检查 Sean 的工作：

$$
g(A, A') = |f(A) - f(A')|
$$

主管希望这个值尽可能大。

但是 Sean 很懒，他并不想真正去洗牌。因此他决定使用一个固定长度为 $n$ 的排列 $p = [p_1, p_2, \ldots, p_n]$ ，当遇到一个排列 $A = [A_1, A_2, \ldots, A_n]$ 时，他直接提交 $f_p(A) = [A_{p_1}, A_{p_2}, \ldots, A_{p_n}]$ 作为洗牌结果。

若 Sean 使用上述洗牌方法，当且仅当排列 $A$ 使得 $g(A, f_p(A))$ 达到最大值时称排列 $A$ 为一个 **幸运排列** 。也就是说，对于任意长度为 $n$ 的排列 $A_0$ ，均满足 $g(A, f_p(A)) \geq g(A_0, f_p(A_0))$ 。

请求出有多少个幸运排列？由于答案可能很大，输出其对 $998 244 353$ 取模后的结果。

### Constraints

- $1 \leq n \leq 22$
- $1 \leq p_i \leq n$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示排列的长度。
- 第二行包含 $n$ 个整数 $p_1, \, p_2, \, \ldots, \, p_n$ ，表示 Sean 用来洗牌的排列 $p$ 。

> $n$
>
> $p_1 \quad p_2 \quad \ldots \quad p_n$

### Output

输出一个整数，表示幸运排列的数量对 $998 244 353$ 取模后的结果。

### Sample Input 1

```txt showLineNumbers=false
3
3 1 2
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
3
3 2 1
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## Solution

逆序对 DP，从小数字考虑到大数字即可

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem H

### Problem Statement

一个 $n$ 维变换超立方体是一个包含 $2^n$ 个顶点的无向图，每个顶点对应一个唯一的长度为 $n$ 的二进制字符串。当且仅当两个顶点的二进制字符串恰好有两位不同时，它们之间存在一条边。每个顶点用其二进制字符串对应的整数值进行标记，因此顶点的编号为 $0, 1, \ldots, 2^n - 1$ 。

现在有恰好两个节点 $a$ 和 $b$ 损坏。请判断能否将剩余的 $2^n - 2$ 个节点划分成若干对，使得每个节点恰好出现在一对中，且每对中的两个节点在图中相邻。如果可以，请输出一种合法方案。

### Constraints

- $1 \leq T \leq 10^4$
- $2 \leq n \leq 22$
- $0 \leq a, b \leq 2^n - 1$
- 所有测试用例中 $2^n$ 的总和不超过 $2^{22}$

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

    - 第一行包含三个整数 $n$ 、$a$ 和 $b$ 。

> $n \quad a \quad b$

### Output

对于每个测试用例，如果存在满足条件的划分方案，第一行输出 `Yes` ，接下来的 $2^{n - 1} - 1$ 行中，每行输出两个整数 $u$ 和 $v$ ；如果不存在满足条件的划分方案，输出一行 `No` 。

### Sample Input

```txt showLineNumbers=false
3
2 0 3
2 0 1
3 2 7
```

### Sample Output

```txt showLineNumbers=false
Yes
1 2
No
Yes
0 5
1 4
3 6
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem A

### Problem Statement

考虑一个大小为 $2N \times 2M$ 的网格图，节点用 $(i, j)$ 标记，其中 $1 \leq i \leq 2N$ 且 $1 \leq j \leq 2M$ 。若目标节点存在，每个节点 $(i, j)$ 均可通过一条长度为 $1$ 的道路连接至 $(i - 1, j)$ 和 $(i, j - 1)$ 。

你的移动速度为单位时间 $1$ ，即通过每条道路需要消耗 $1$ 单位时间。

对于每对满足 $1 \leq r \leq N$ 和 $1 \leq c \leq M$ 的整数，四个节点 $(2r - 1, 2c - 1)$ 、$(2r - 1, 2c)$ 、$(2r, 2c - 1)$ 和 $(2r, 2c)$ 构成一个 **十字路口** 。初始时，每个十字路口均显示红灯，禁止所有通过该路口的移动。

包含 $(2r - 1, 2c - 1)$ 、$(2r - 1, 2c)$ 、$(2r, 2c - 1)$ 的十字路口只能通过到达其 **控制节点** $(2r, 2c)$ 来激活。到达控制节点后，你可以按下按钮：十字路口有 $p \mathbin{/} q$ 的概率进入 **状态 A** ，有 $1 - p \mathbin{/} q$ 的概率进入 **状态 B** 。

- **状态 A**：按下按钮后的第 $1$ 单位时间内，行方向移动（即改变 $i$）显示绿灯，列方向移动（即改变 $j$）显示红灯。之后两个方向每单位时间交替显示绿灯与红灯。
- **状态 B**：按下按钮后的第 $1$ 单位时间内，列方向移动（即改变 $j$）显示绿灯，行方向移动（即改变 $i$）显示红灯。之后两个方向每单位时间交替显示绿灯与红灯。

只有当你在通过十字路口时该方向当前显示绿灯，你才可以通行。不同十字路口的信号状态彼此 **独立** 。

你从 $(2N, 2M)$ 出发，希望以 **最优策略** 移动以最小化到达 $(1, 1)$ 的期望总用时。

你需要输出一个整数 $x$（ $0 \leq x < 998 244 353$ ），使得 $q \times x \equiv p \pmod{998 244 353}$ 。

### Constraints

- $1 \leq T \leq 100$
- $1 \leq N, M \leq 10^6$
- $1 \leq p < q < 998 244 353$

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

    - 第一行包含四个整数 $N$ 、$M$ 、$p$ 和 $q$ 。

> $N \quad M \quad p \quad q$

### Output

对于每个测试用例，输出一行一个整数，表示最优策略下期望用时对 $998 244 353$ 取模后的结果。

### Sample Input

```txt showLineNumbers=false
2
2 2 1 2
3 5 1 3
```

### Sample Output

```txt showLineNumbers=false
6
271128110
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

给定一棵包含 $n$ 个节点且以 $1$ 为根的树，树上的每条边均被赋予了一个非负整数数边权。对于节点 $u$ 和 $v$ 之间的边，其边权记为 $w_{u, v}$ 。你需要为树上的每个节点 $u$ 分配一个非负整数 $a_u$ ，如果对于树上每一条边 $(u, v)$ ，均满足 $w_{u, v} = |a_u - a_v|$ ，则称这棵树是 **绝妙的** 。

对于一棵绝妙的树，定义其 **复杂度** 为树中所有节点点权的最大值与最小值之差。

现在节点点权缺失，对于每个 $i$（ $1 \leq i \leq n$ ），假设只考虑以 $i$ 为根的子树，你需要为该子树中的节点分配非负整点权，使其成为一棵绝妙的树，求此时该子树复杂度的最小值。

### Constraints

- $1 \leq T \leq 10^4$
- $3 \leq n \leq 10^5$
- $1 \leq u_i, v_i \leq n$
- $0 \leq w_{u_i, v_i} \leq 5000$
- 所有测试用例中 $n$ 的总和不超过 $\displaystyle \min \left(\frac{3 \times 10^7}{\max(1, W)}, 10^5 \right)$

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

    - 第一行包含一个整数 $n$ ，表示树的节点数量。
    - 接下来 $n - 1$ 行，第 $i$ 行包含三个整数 $u_i$ 、$v_i$ 和 $w_{u_i, v_i}$ 。

> $n$
>
> $u_1 \quad v_1 \quad w_{u_1, v_1}$
>
> $u_2 \quad v_2 \quad w_{u_2, v_2}$
>
> $\ldots$
>
> $u_{n - 1} \quad v_{n - 1} \quad w_{u_{n - 1}, v_{n - 1}}$

### Output

对于每个测试用例，输出一行包含 $n$ 个整数，表示以节点 $1, 2, \ldots, n$ 为根的子树在成为绝妙的树时的答案。

### Sample Input

```txt showLineNumbers=false
3
3
1 2 1
2 3 1
4
1 2 2
2 3 1
3 4 2
5
1 2 4
1 3 1
2 4 2
2 5 1
```

### Sample Output

```txt showLineNumbers=false
1 1 0
3 2 2 0
4 2 0 0 0
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```