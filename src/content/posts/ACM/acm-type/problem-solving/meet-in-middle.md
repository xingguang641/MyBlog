---
title: 【ACM 算法题单】折半搜索相关问题
published: 2026-05-08
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 折半搜索题目合集

折半搜索（也常被称为双向搜索）是我们处理算法问题时 **缓解状态爆炸** 的经典技巧。其核心思想在于将原本规模为 $n$ 的搜索问题拆分为两个规模约为 $n/2$ 的子问题，通过分别独立搜索再进行结果合并，将指数级增长的复杂度有效降低。这种转化并未从根本上消除问题的指数级特征，而是通过 **路径重构** ，将原本深层搜索带来的计算压力 **转移到了结果的整合阶段** 。这种通过拆分搜索任务来平衡计算开销的策略，使得原本因搜索树规模呈指数级扩张而导致时空开销过大的一类问题，在严苛的时限内得以解决。

搜索过程的简化必然伴随着合并逻辑的复杂化，因此掌握折半搜索的关键在于 **对中间结果的整合** 。在具体解题中，整合步骤通常需要调用 **排序、二分查找、哈希表或双指针** 等工具，这意味着我们不仅要能够编写基础的搜索函数，更需要根据问题的 **数值特征与单调性** ，选择最合适的整合策略。通过系统归纳典型题目的匹配方式，我们能够更直观地理解不同工具的适用场景，从而在面对复杂搜索空间时，构建出 **最高效的整合方案** 。

## 不相邻整数序列

[题目链接](https://atcoder.jp/contests/abc427/tasks/abc427_f)

### Problem Statement

给定一个长度为 $N$ 的整数序列 $A = (A_1, A_2, \ldots, A_N)$ ，序列 $A$ 的子序列一共有 $2^N$ 种。对于一个子序列 $(A_{i_1}, A_{i_2}, \ldots, A_{i_k})$ ，满足 $1 \leq i_1 < i_2 < \ldots < i_k \leq N$ 。请你统计满足以下两个条件的子序列个数：

1. 所有被选出的元素在原序列中 **不相邻** 。
2. 子序列的元素和是 $M$ 的倍数。

即使两个子序列的值相同，只要取自不同的位置，也视为不同的子序列。

### Constraints

- $1 \leq N \leq 60$
- $1 \leq M \leq 10^9$
- $0 \leq A_i < M$
- 所有输入均为整数

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $M$ 。
- 第二行包含 $N$ 个整数，表示序列 $A$ 。

> $N \quad M$
>
> $A_1 \quad A_2 \quad \ldots \quad A_N$

### Output

输出满足条件的子序列数量。

### Sample Input 1

```txt showLineNumbers=false
7 6
3 1 4 1 5 3 2
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
15 10
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
```

### Sample Output 2

```txt showLineNumbers=false
798
```

## 题目要点解析

从题目表面上看，这是一个非常典型的 **动态规划** 问题。在常规的计数场景下，我们可以定义 $dp[i][j][0/1]$ 表示前 $i$ 个数中选出的子序列和取模 $M$ 等于 $j$ ，且当前第 $i$ 位选或不选的方案数。然而，本题的约束条件中 $M$ 高达 $10^9$ ，这导致状态空间中取模维度直接爆炸，常规 DP 无法在有限的时空内维护如此庞大的状态转移表。

由于 $N$ 的范围在 $60$ 以内，与常见的折半搜索适用区间相吻合，因此我们可以考虑通过这种技巧来解决。我们将序列 $A$ 按下标划分为左右两部分：左半部分为 $A_1 \sim A_k$ ，右半部分为 $A_{k+1} \sim A_N$ ，其中 $k=\lfloor N/2 \rfloor$ 。对每一部分分别进行深度优先搜索，枚举所有满足不相邻约束的子序列状态。

在枚举左半部分时，对每一个合法子序列记录其元素和对 $M$ 取模后的值 $s$ ，以及一个关键的布尔标记 $t$ ，用来表示该子序列是否选取了左半部分的末尾元素 $A_k$ 。我们将枚举结果按照 $t$ 的取值分为 $L_0$（未选 $A_k$ ）和 $L_1$（已选 $A_k$ ）两组。同理，对右半部分进行枚举，记录模值 $s'$ 以及表示是否选取了右半部分首元素 $A_{k+1}$ 的标记 $u$ ，并将其分为 $R_0$ 和 $R_1$ 两组。

在最后的合并阶段，我们需要处理跨越分界线的相邻约束。根据不相邻的规则，如果左半部分选了 $A_k$（即来自 $L_1$ ），则右半部分绝对不能选 $A_{k+1}$（即只能匹配 $R_0$ ）；如果左半部分没选 $A_k$（即来自 $L_0$ ），则右半部分可选也可不选（即匹配 $R_0 \cup R_1$ ）。我们需要统计满足以下等式的组合数量：

$$
(s + s') \equiv 0 \pmod M
$$

具体实现时，由于单侧枚举出的状态数在 $2^{30}$ 以内（实际受不相邻约束限制，状态数远小于此），我们可以通过对右半部分的模值进行排序，然后利用 **二分查找** 快速定位补数 $(M-s) \bmod M$ 的出现次数。通过这种方式，原本无法处理的 $10^9$ 量级模值维度被转化为对两个 $10^6$ 级别序列的扫描与合并，从而在时限内求得最终答案。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 100;
int n, mid; ll modM;
ll arr[MAXN];

// cntLeft[t][mod]：左半部分，t = 是否选了arr[mid]
unordered_map<ll, ll> cntLeft[2];
void dfsLeft(int pos, bool lastTaken, bool takeLast, ll sumMod) {
    if (pos > mid) {
        cntLeft[takeLast][sumMod]++;
        return;
    }

    // 不选当前元素
    dfsLeft(pos + 1, false, takeLast, sumMod);
    // 选当前元素（需满足不相邻）
    if (!lastTaken) {
        bool newTakeLast = takeLast;
        if (pos == mid) newTakeLast = true;
        dfsLeft(pos + 1, true, newTakeLast,
               (sumMod + arr[pos]) % modM);
    }
}

// cntRight[u][mod]：右半部分，u = 是否选了arr[mid+1]
unordered_map<ll, ll> cntRight[2];
void dfsRight(int pos, bool lastTaken, bool takeFirst, ll sumMod) {
    if (pos > n) {
        cntRight[takeFirst][sumMod]++;
        return;
    }

    // 不选当前元素
    dfsRight(pos + 1, false, takeFirst, sumMod);
    // 选当前元素（需满足不相邻）
    if (!lastTaken) {
        bool newTakeFirst = takeFirst;
        if (pos == mid + 1) newTakeFirst = true;
        dfsRight(pos + 1, true, newTakeFirst,
                (sumMod + arr[pos]) % modM);
    }
}

int main() {
    cin >> n >> modM;
    for (int i = 1; i <= n; i++) {
        cin >> arr[i];
    }

    mid = n / 2;
    dfsLeft(1, false, false, 0);
    dfsRight(mid + 1, false, false, 0);

    ll answer = 0;
    for (int takeLast = 0; takeLast <= 1; takeLast++) {
        for (auto &[leftMod, leftCount] : cntLeft[takeLast]) {
            ll need = (modM - leftMod) % modM;
            if (takeLast) {
                // 左边选了 arr[mid]，右边不能选 arr[mid+1]
                if (cntRight[0].count(need)) {
                    answer += leftCount * cntRight[0][need];
                }
            } else {
                // 左边没选 arr[mid]，右边随意
                if (cntRight[0].count(need)) {
                    answer += leftCount * cntRight[0][need];
                }
                if (cntRight[1].count(need)) {
                    answer += leftCount * cntRight[1][need];
                }
            }
        }
    }

    cout << answer << "\n";
}
```

## 通往整数的路径

[题目链接](https://atcoder.jp/contests/abc402/tasks/abc402_f)

### Problem Statement

给定一个 $N \times N$ 的格子。格子中每个位置 $(i, j)$ 都写有一个数字 $A_{i,j}$（取值范围是 $1$ 到 $9$ ）。目前棋子最开始放在格子 $(1,1)$ 。你需要进行以下操作 **共 $2N-1$ 次**：

- 把当前棋子所在格子中的数字 **追加到字符串 $S$** 的末尾
- 然后把棋子朝 **下方或右方** 移动一格
    
    *注意：在第 $2N-1$ 次操作中不再移动棋子*

执行完这些操作后，棋子最终会到达格子 $(N, N)$ ，并且字符串 $S$ 的长度为 $2N-1$ 。把字符串 $S$ 视为一个十进制整数，然后对 $M$ 取模后的余数就是得分。你的任务是输出可以得到的 **最大得分** 。也就是说，你可以在每次移动时任意选择向右或者向下，但必须最后从 $(1,1)$ 到达 $(N,N)$ ，并要 **最大化 $S \bmod M$** 。

### Constraints

- $1 \leq N \leq 20$
- $2 \leq M \leq 10^9$
- $1 \leq A_{ij} \leq 9$
- 所有输入均为整数

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $M$ 。
- 接下来 $N$ 行，每行包含 $N$ 个整数。

> $N \quad M$
> 
> $A_{11} \quad A{12} \quad \ldots \quad A_{1N}$
> 
> $A_{21} \quad A{22} \quad \ldots \quad A_{2N}$
> 
> $\ldots$
> 
> $A_{N1} \quad A{N2} \quad \ldots \quad A_{NN}$


### Output

输出一个整数表示可以达到的最大得分 （即最大化字符串 $S$ 对 $M$ 取模的结果）。

### Sample Input 1

```txt showLineNumbers=false
2 7
1 2
3 1
```

### Sample Output 1

```txt showLineNumbers=false
5
```

### Sample Input 2

```txt showLineNumbers=false
3 100000
1 2 3
3 5 8
7 1 2
```

### Sample Output 2

```txt showLineNumbers=false
13712
```

### Sample Input 3

```txt showLineNumbers=false
5 402
8 1 3 8 9
8 2 4 1 8
4 1 8 5 9
6 2 1 6 7
6 6 7 7 6
```

### Sample Output 3

```txt showLineNumbers=false
384
```

## 题目要点解析

从 $(1,1)$ 走到 $(N,N)$ 的合法路径共有 $C_{2N-2}^{N-1}$ 条，当 $N = 20$ 时，路径总数约为 $3.5 \times 10^{10}$ 。在如此庞大的搜索空间下，直接枚举所有路径显然会超出时间限制。因此，我们可以采用 **折半搜索** 的策略，在中间层将路径一分为二。我们考虑所有满足 $i + j = N + 1$ 的格子作为分界点，这样任意一条完整路径都可以被拆分为 **从 $(1,1)$ 到某个中点格子的前半段路径** 和 **从该中点格子到 $(N,N)$ 的后半段路径** 两个部分。

对于前半段路径，我们枚举所有从 $(1,1)$ 走到每个中点 $(i,j)$ 的路径，并计算对应字符串表示的数值对 $M$ 取模的结果。由于拼接采用十进制，我们在转移时维护变量 $h$ ，并对每一个中点格子记录所有可能的前半段模值集合：

$$
h = (h_{prev} \times 10 + A_{i,j}) \bmod M
$$

对于后半段路径，我们反向枚举所有从 $(N,N)$ 走到每个中点 $(i, j)$ 的路径，并计算对应字符串表示的数值对 $M$ 取模的结果。由于中点值 $A_{i,j}$ 已经在前半段计入，要注意排除这个中点值。并且我们是逆向求解，因此要多维护一个变量 $k$ 表示当前格子距离终点的步数：

$$
t = (t_{prev} + A_{i,j} \times 10^k) \bmod M
$$

在合并阶段，对于每一个中点格子，我们已经拥有该处所有可能的前半段集合 $\{h\}$ 和后半段集合 $\{t\}$ 。如果直接枚举所有 $(h, t)$ 的组合，时间复杂度将达到平方量级，在大规模数据下无法通过，因此我们需要找到更高效的合并方法。首先我们把问题形式化，将前半段数值向左平移 $N-1$ 位，得到合并公式：

$$
S \bmod M = (h \times 10^{N-1} + t) \bmod M
$$

为了最大化这个结果，我们可以令 $x = (h \times 10^{N-1}) \bmod M$ ，那么这个问题就变成经典的[两数之和取模问题](https://xingguang641.com/posts/acm/acm-type/math-operators/mod-problem/mod-problem/#mod两数之和问题)。由于在合并前 $x$ 和 $t$ 均已对 $M$ 取模，它们的取值范围均在 $[0, M)$ 之内。这意味着两数之和对 $M$ 取模只有两种可能的结果：

$$
(x + t) \bmod M =
\begin{cases}
x + t, & x + t < M \\
x + t - M, & M \le x + t < 2M
\end{cases}
$$

基于这一观察，当我们要最大化结果时，优先目标是让 $x+t$ 尽量接近但不超过 $M$ ；如果无法做到，则退而求其次选择 $x+t$ 尽量大的情况。因此，在固定 $x$ 的前提下，我们只需在已排序的 $\{t\}$ 集合中，通过二分寻找满足 $t < M - x$ 的最大值，或者直接取 $\{t\}$ 中的最大值进行尝试，这两种情况必然覆盖了所有可能的最优解。通过这种方式，我们可以将合并阶段的复杂度从平方量级降低为 $O(n \log n)$ 。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 25;
int n; ll modM;
ll grid[MAXN][MAXN];
// pow10[i] = 10^i % modM
ll pow10[MAXN * 2];

// leftVals[i][j]：从 (1,1) 到 (i,j) 的所有前缀模值
vector<ll> leftVals[MAXN][MAXN];
void dfsLeft(int x, int y, ll curVal) {
    curVal = (curVal * 10 + grid[x][y]) % modM;
    if (x + y == n + 1) {
        leftVals[x][y].push_back(curVal);
        return;
    }

    if (x + 1 <= n) dfsLeft(x + 1, y, curVal);
    if (y + 1 <= n) dfsLeft(x, y + 1, curVal);
}

// rightVals[i][j]：从 (i,j) 到 (n,n) 的所有后缀模值（不包含 (i,j)）
vector<ll> rightVals[MAXN][MAXN];
void dfsRight(int x, int y, ll curVal, int len) {
    // 到中点就停，不再把 grid[x][y] 加进去
    if (x + y == n + 1) {
        rightVals[x][y].push_back(curVal);
        return;
    }
    curVal = (grid[x][y] * pow10[len] + curVal) % modM;

    if (x - 1 >= 1) dfsRight(x - 1, y, curVal, len + 1);
    if (y - 1 >= 1) dfsRight(x, y - 1, curVal, len + 1);
}

int main() {
    cin >> n >> modM;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> grid[i][j];
        }
    }
    // 预处理 10 的幂
    pow10[0] = 1 % modM;
    for (int i = 1; i <= 2 * n; i++) {
        pow10[i] = (pow10[i - 1] * 10) % modM;
    }

    dfsLeft(1, 1, 0);
    dfsRight(n, n, 0, 0);

    ll answer = 0;
    for (int i = 1; i <= n; i++) {
        int j = n + 1 - i;
        if (j < 1 || j > n) continue;

        int rightLen = (n - i) + (n - j);
        auto &L = leftVals[i][j];
        auto &R = rightVals[i][j];
        if (L.empty() || R.empty()) continue;

        sort(R.begin(), R.end());
        for (ll leftVal : L) {
            ll x = (leftVal * pow10[rightLen]) % modM;
            ll need = (modM - x) % modM;

            // 尝试 a + b < M 的最大情况
            auto it = lower_bound(R.begin(), R.end(), need);
            if (it != R.begin()) {
                --it;
                answer = max(answer, (x + *it) % modM);
            }

            // 尝试 a + b >= M 的情况
            answer = max(answer, (x + R.back()) % modM);
        }
    }

    cout << answer << "\n";
}
```

---

# 参考文献列表

1. [【CSDN 博客】C++ 折半搜索](https://blog.csdn.net/2501_90415399/article/details/159130103)

2. [【zhouyiran2011】折半搜索](https://www.cnblogs.com/zhouyiran2011/p/18874958)