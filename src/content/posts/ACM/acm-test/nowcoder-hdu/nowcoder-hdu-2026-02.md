---
title: 【ACM 算法比赛】2026牛客暑期多校训练营02
published: 2026-08-01
description: 记录一些 ACM 常见竞赛
tags: [Algorithm, Nowcoder, Contest]
category: ACM Test
draft: false
---

# 比赛题目讲解

[比赛链接](https://ac.nowcoder.com/acm/contest/133877)

## Problem N

[题目链接](https://ac.nowcoder.com/acm/contest/133877/N)

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

  - 第一行包含两个整数 $n$ 和 $k$ ，表示数组长度和选择元素的数量。
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
# include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 2e5 + 100;
ll a[MAXN] , s[MAXN];

int main(){
    int T; cin >> T;
    while(T--){
        int n, k; cin >> n >> k;
        for(int i = 1; i <= n; i++) cin >> a[i];
        sort(a + 1 , a + n + 1);
        for(int i = 1; i <= n; i++) s[i] = s[i - 1] + a[i];

        ll ans = 0;
        if (k % 2 == 1){
            for (int i = (k + 1) / 2; i + k - (k + 1) / 2 <= n; i++){
                ans = max(ans , s[n] + k * a[i] - s[(k + 1) / 2 - 1] - (s[i + k - (k + 1) / 2] - s[i - 1]));
            }
        }else{
            for(int i = k / 2; i + k / 2 <= n; i++){
                ans = max(ans , s[n] + k * (a[i] + a[i + 1]) / 2 - s[k / 2 - 1] - (s[i + k / 2] - s[i - 1]));
            }
        }
        cout << ans << '\n';
    }
}
```

## Problem B

[题目链接](https://ac.nowcoder.com/acm/contest/133877/B)

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

### Sample Input 1

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

### Sample Output 1

```txt showLineNumbers=false
1
6
6
4
```

## Solution

异或线性基

## Problem L

[题目链接](https://ac.nowcoder.com/acm/contest/133877/L)



## Solution

