---
title: 【ACM 算法比赛】华南理工 2024 程序设计竞赛
published: 2026-09-26
description: 记录一些 ACM 常规比赛
tags: [Algorithm, Contest, Nowcoder]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://ac.nowcoder.com/acm/contest/131454)

## Problem A

> `二分答案`

### Problem Statement

期末考试在即，紧张预习数据挖掘的 Capps 对如下问题十分感兴趣：

在一维空间中有点集 $S$ 包含 $n$ 个点，用什么算法能快速回答如下 $q$ 次查询：

- 第 $i$ 次查询给出点 $p_i$ 和整数 $k_i$ ，要求输出 $S$ 中与点 $p_i$ 距离第 $k_i$ 近的点和 $p_i$ 的 **距离** 。

**距离**：若点 $u_i$ 坐标为 $x_i$ ，$v_i$ 坐标为 $y_i$ ，则定义点 $u_i$ 与点 $v_i$ 的距离为 $|x_i - y_i|$ 。

### Constraints

- $1 \leq n, q \leq 2 \times 10^5$
- $-10^9 \leq a_i \leq 10^9$
- $-10^9 \leq x_i \leq 10^9$
- $1 \leq k_i \leq n$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $q$ ，表示点集 $S$ 的大小和查询次数。
- 第二行包含 $n$ 个整数，第 $i$ 个整数 $a_i$ 描述点集 $S$ 里第 $i$ 个点的坐标。
- 接下来 $q$ 行，第 $i$ 行包含两个整数 $x_i$ 和 $k_i$ ，表示 $p_i$ 的坐标和需要查询距离 $p_i$ 第 $k_i$ 近的结果。

> $n \quad q$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$
>
> $x_1 \quad k_1$
>
> $x_2 \quad k_2$
>
> $\ldots$
>
> $x_q \quad k_q$

### Output

输出 $q$ 行，第 $i$ 行包含一个整数，表示第 $i$ 次查询的答案。

### Sample Input

```txt showLineNumbers=false
5 3
10 -2 1 3 4
12 4
3 1
2 2
```

### Sample Output

```txt showLineNumbers=false
11
0
1
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem H

> `换根 DP`

### Problem Statement

Sppac 国有 $n$ 个基站和 $n - 1$ 条街道，第 $i$ 条街道连接两个基站 $u_i$ 和 $v_i$ ，保证任意两个基站都可以穿过若干条街道到达彼此。**初始每个基站上都有一个信号塔** ，一条街道上拥有网络覆盖需要满足以下 **至少一个条件**：

- 此街道直接连接的两个基站上共存在至少一个信号塔。
- Sppac 国国王 Capps 居住在此街道。

Sppac 国的居民都居住在街道上，国王 Capps 爱民如子，希望每条街道都有网络覆盖，同时国家的经费又十分紧张，所以 Capps 希望拆除尽量多的信号塔，使得每条街道还都有网络覆盖。

请对每个 $i$（ $1 \leq i \leq n - 1$ ），求出当国王 Capps 居住在第 $i$ 条街道时 Sppac 国最多可以拆除的信号塔个数。

### Constraints

- $1 \leq T \leq 10^5$
- $2 \leq n \leq 2 \times 10^5$
- $1 \leq u_i, v_i \leq n$
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

    - 第一行包含一个整数 $n$ ，表示 Sppac 国的基站数目。
    - 接下来 $n - 1$ 行，第 $i$ 行包含两个整数 $u_i$ 和 $v_i$ ，表示第 $i$ 条街道连接 $u_i$ 基站和 $v_i$ 基站。

> $n$
>
> $u_1 \quad v_1$
>
> $u_2 \quad v_2$
>
> $\ldots$
>
> $u_{n - 1} \quad v_{n - 1}$

### Output

对于每个测试用例，输出一行 $n - 1$ 个整数，第 $i$ 个数表示当国王 Capps 居住在第 $i$ 条街道时 Sppac 国最多可以拆除多少个信号塔使得每条街道还都有网络覆盖，其中相邻整数以一个空格隔开。

### Sample Input

```txt showLineNumbers=false
2
5
1 2
2 3
2 4
1 5
6
1 6
5 6
3 5
4 3
2 1
```

### Sample Output

```txt showLineNumbers=false
3 3 3 4
3 4 3 4 4
```

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main(){
    int T; cin >> T;
    while(T--){
        int n; cin >> n;
        vector<vector<int>> grap(n);
        vector<int> eu(n - 1), ev(n - 1);
        for (int i = 0; i < n - 1; i++){
            int u, v; cin >> u >> v; --u, --v;
            eu[i] = u; ev[i] = v;
            grap[u].push_back(v);
            grap[v].push_back(u);
        }

        vector<int> parent(n), order;
        vector<int> st; st.push_back(0);
        parent[0] = -2;
        while(!st.empty()){
            int cur = st.back();
            st.pop_back();
            order.push_back(cur);

            for (int nxt : grap[cur]){
                if (nxt == parent[cur]) continue;
                parent[nxt] = cur;
                st.push_back(nxt);
            }
        }

        vector<int> dp0(n, 0), dp1(n, 0);
        vector<int> sum1(n, 0), sumMin(n, 0);
        for (int idx = n - 1; idx >= 0; idx--){
            int cur = order[idx];

            int sum = 0, min_sum = 0;
            for (int nxt : grap[cur]){
                if (parent[nxt] == cur){
                    sum += dp1[nxt];
                    min_sum += min(dp0[nxt], dp1[nxt]);
                }
            }

            dp0[cur] = sum;
            dp1[cur] = 1 + min_sum;

            sum1[cur] = sum;
            sumMin[cur] = min_sum;
        }

        vector<int> up0(n, 0), up1(n, 0);
        for (int idx = 0; idx < n; idx++){
            int cur = order[idx];

            for (int nxt : grap[cur]){
                if (parent[nxt] == cur){
                    up1[nxt] = 1 + (cur == 0 ? 0 : min(up0[cur], up1[cur])) + sumMin[cur] - min(dp0[nxt], dp1[nxt]);
                    up0[nxt] = (cur == 0 ? 0 : up1[cur]) + sum1[cur] - dp1[nxt];
                }
            }
        }

        for (int i = 0; i < n - 1; i++){
            int u = eu[i], v = ev[i];
            int child = (parent[u] == v ? u : v);

            int ans1 = min(dp0[child], dp1[child]);
            int ans2 = min(up0[child], up1[child]);
            int res = n - ans1 - ans2;
            cout << res << " ";
        }
        cout << endl;
    }
}
```

## Problem K



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem M

https://codeforces.com/contest/2256/problem/B

## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem J



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem F



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem L



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem B



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem D



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem C



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```