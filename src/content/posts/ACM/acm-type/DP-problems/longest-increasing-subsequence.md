---
title: 【ACM 算法题单】最长递增子序列问题
published: 2026-02-06
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 经典动态规划思想

最长递增子序列（LIS）是一个非常典型的 **偏序型动态规划问题** 。最自然的思路是从朴素的状态设计入手：定义 $dp[i]$ 表示 **以第 i 个元素结尾** 的最长递增子序列长度。那么在计算 $dp[i]$ 时，我们只需要枚举所有 $j < i$ ，如果 $a[j] < a[i]$ ，就可以尝试用 $dp[j] + 1$ 来更新 $dp[i]$ 。这种做法本质上是在所有可能的前驱中寻找最优决策，因此时间复杂度为 $O(n^2)$ 。

然而这种朴素做法虽然直观，但效率偏低。进一步观察可以发现：在位置 $i$ 之前的所有历史状态中，存在大量冗余的状态。如果某个位置 $j_1$ 的数值更小且对应的状态值更大，那么对于后续的任何决策而言，位置 $j_1$ 显然都比数值更大且状态值更小的位置 $j_2$ 更具竞争力。

### 单调二分优化

基于这一思想，我们不再显式维护每个位置的最优值，而是换一个角度：维护一个数组 $d[len]$ ，表示 **长度为 len 的递增子序列，其最小可能的结尾元素是多少** 。换句话说，我们对 “同一长度的所有递增子序列” 只保留结尾最小的那一个，因为结尾越小，未来可扩展的空间就越大，这显然是更优的代表状态。

这个数组具有一个重要性质：它一定是 **单调递增的** 。原因在于，长度为 $len+1$ 的递增子序列必然是在某个长度为 $len$ 的递增子序列后面添加一个更大的元素得到的，因此其结尾元素一定严格大于对应长度为 $len$ 的结尾元素。并且由于 $d[len]$ 中存储的是 **所有长度为 len 的递增子序列中结尾最小的那个值** ，它本身已经是该长度下的最优代表状态，所以无论长度为 $len+1$ 的序列是从哪个具体的长度为 $len$ 的序列转移过来的，其结尾元素都必然大于这个最小结尾。因此必然有：

$$
d[len] < d[len+1]
$$

这一单调性保证了我们可以对其进行二分查找。于是，当遍历到一个新元素 $a[i]$ 时，我们只需要在 $d$ 数组中找到 **第一个大于等于 $a[i]$** 的位置，用 $a[i]$ 去更新它；如果不存在这样的元素，则说明可以扩展最长长度。这样，每个元素只需一次二分查找，时间复杂度从 $O(n^2)$ 优化为 $O(n \log n)$ 。

### 树状数组优化

回到问题本身，我们也可以从最初的动态规划状态转移出发，对朴素的 $O(n^2)$ 枚举过程进行进一步优化。仍然定义 $dp[i]$ 表示 **以第 i 个元素结尾的最长递增子序列长度** 。根据递增子序列的性质，如果存在 $j<i$ 且满足 $a[j] < a[i]$ ，那么就可以从位置 $j$ 转移到位置 $i$ ，因此有转移关系：

$$
dp[i] = \max_{j<i,a[j]<a[i]} dp[j] + 1
$$

在朴素算法中，需要枚举所有满足条件的 $j$ ，从而导致 $O(n^2)$ 的时间复杂度。进一步观察可以发现，这个转移实际上只关心一件事情：在所有 **数值小于 $a[i]$** 的元素中，最大的 $dp$ 值是多少。也就是说，我们并不关心这些元素具体出现在序列的哪个位置，只需要知道当前所有满足 $a[j] < a[i]$ 的状态中的最优值即可。

为了能高效地完成这一查询，我们可以先对序列中的数值进行 **离散化** 。将所有出现过的数值进行排序并重新编号，使得每个元素 $a[i]$ 对应一个排名 $rank[i]$ 。这样一来，所有满足 $a[j] < a[i]$ 的元素，就等价于排名位于区间 $[1,rank[i]-1]$ 的元素。在此基础上，可以利用 **树状数组** 来维护这些信息。

树状数组的每个节点存储当前某个数值范围内的最大 $dp$ 值，并支持两种基本操作：一是查询区间 $[1,x]$ 的最大值，二是更新某个位置的最大值。当遍历到元素 $a[i]$ 时，首先在树状数组中查询区间 $[1,rank[i]-1]$ 的最大值，得到当前所有小于 $a[i]$ 的元素所对应的最大 $dp$ 值，记为 $best$ ，于是：

$$
dp[i] = best + 1
$$

随后再用 $dp[i]$ 去更新树状数组中位置 $rank[i]$ 的值即可。

由于树状数组的单次查询和更新操作复杂度均为 $O(\log n)$ ，整个算法的时间复杂度可以降低为 $O(n\log n)$ 。与前面的单调二分优化不同，树状数组优化的核心思想并不是通过维护最优代表状态来压缩状态空间，而是 **直接从动态规划转移关系出发，将原本需要枚举的转移过程转化为数据结构上的区间查询问题** 。

## 最长上升子序列

[题目链接](https://www.luogu.com.cn/problem/P1020)

### Problem Statement

某国为了防御敌国的导弹袭击，开发了一种导弹拦截系统。但这种系统存在一个缺陷：

- 第一发炮弹可以到达任意高度；
- 之后每一发炮弹的高度 **都不能高于前一发炮弹的高度** 。

由于系统仍在试用阶段，目前只有 **一套拦截系统** ，因此可能无法拦截所有导弹。

现在给出导弹依次飞来的高度序列，要求：

1. **一套拦截系统最多能够拦截多少枚导弹** ；
2. 如果希望拦截所有导弹，**最少需要多少套拦截系统** 。

### Constraints

- $n \leq 10^5$
- $0 \leq h_i \leq 5 \times 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组的长度。
- 第二行包含 $n$ 个整数，表示数组的元素。

> $n$
> 
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出包含两行：

- 一套系统最多能拦截的导弹数量
- 拦截所有导弹所需的最少系统数量

### Sample Input

```txt showLineNumbers=false
389 207 155 300 299 170 158 65
```

### Sample Output

```txt showLineNumbers=false
6
2
```

## 题目要点解析

首先考虑题目的第一个问题：**一套拦截系统最多能够拦截多少枚导弹** 。根据题目规则，拦截系统发射的炮弹高度必须满足后一发不高于前一发，也就是说拦截的导弹高度序列必须是一个 **不上升序列** 。因此问题可以直接转化为：在给定的导弹高度序列中，求一个 **最长不上升子序列** 。这一问题与经典的最长递增子序列问题是完全对称的，可以通过动态规划求解，利用二分优化将复杂度降低到 $O(n \log n)$ 。

接下来考虑第二个问题：**如果要拦截所有导弹，最少需要多少套拦截系统** 。每一套拦截系统所拦截的导弹序列都必须满足不上升的性质，因此本质上是在问：如何将整个序列划分成尽量少的若干个 **不上升子序列** 。从反向的角度来看，如果存在一个严格上升的子序列，那么其中的每一个元素都无法被同一套系统拦截，因为后一枚导弹高度高于前一枚导弹，违背了拦截规则。因此，这个上升序列中的每一个元素都必须由 **不同的拦截系统** 来处理。

由此可以得到一个重要结论：需要的最少拦截系统数量，恰好等于该序列的 **最长严格上升子序列** 的长度。换句话说，最长上升子序列中的每一个元素都至少需要一套独立的系统才能完成拦截。这个结论也可以从序列划分的角度理解：将一个序列划分为若干个不上升序列，其最少划分数量等于该序列的最长上升子序列长度。

综上这道题可以拆分为两个经典问题：第一个是求 **最长不上升子序列** ，第二个是求 **最长严格上升子序列** 。二者都可以利用最长递增子序列的标准算法进行求解，整体时间复杂度可以做到 $O(n \log n)$ 。

```cpp frame="code" title="main.cpp"
# include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 数组K递增问题

[题目链接](https://leetcode.cn/problems/minimum-operations-to-make-the-array-k-increasing)

### Problem Statement

给你一个下标从 $0$ 开始包含 $n$ 个正整数的数组 `arr` ，和一个正整数 `k` 。

如果对于每个满足 $k \leq i \leq n - 1$ 的下标 $i$ 都有 $arr[i-k] \leq arr[i]$ ，那么称数组 `arr` 是 **k 递增** 的。

- 比方说，`arr = [4, 1, 5, 2, 6, 2]` 对于 $k = 2$ 是 k 递增的，因为：
    - $arr[0] \leq arr[2] (4 \leq 5)$
    - $arr[1] \leq arr[3] (1 \leq 2)$
    - $arr[2] \leq arr[4] (5 \leq 6)$
    - $arr[3] \leq arr[5] (2 \leq 2)$
- 相反，`arr = [4, 1, 5, 2, 6, 2]` 对于 $k = 3$ 不是 k 递增的，因为 $arr[0] > arr[3]$ 。

在一步操作中，你可以选择一个下标 $i$ 并将 $arr[i]$ 改成 **任意** 正整数。

请你返回使数组 `arr` 变成 **k 递增** 的 **最少** 操作次数。

### Constraints

- $1 \leq arr.length \leq 10^5$
- $1 \leq arr[i], k \leq arr.length$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组 $arr$ 中的元素。

> $N \quad k$
> 
> $arr_0 \quad arr_1 \quad \ldots \quad arr_{N-1}$

### Output

输出一个整数，表示使数组变成 k 递增的最少操作次数。

### Sample Input 1

```txt showLineNumbers=false
6 1
5 4 3 2 1 1
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
6 2
4 1 5 2 6 2
```

### Sample Output 2

```txt showLineNumbers=false
0
```

### Sample Input 3

```txt showLineNumbers=false
6 3
4 1 5 2 6 2
```

### Sample Output 3

```txt showLineNumbers=false
2
```

## 题目要点解析

取模分组问题

## 嵌套的信封问题

[题目链接](https://leetcode.cn/problems/russian-doll-envelopes)

### Problem Statement

给你一个二维整数数组 `envelopes` ，其中 $envelopes[i] = [w_i, h_i]$ ，表示第 $i$ 个信封的宽度和高度。

当另一个信封的宽度和高度都比这个信封大的时候，这个信封就可以放进另一个信封里，如同俄罗斯套娃一样。

请计算 **最多** 能有多少个信封能形成一组 “俄罗斯套娃” 信封（即可以把一个信封放到另一个信封里面）。

**注意**：不允许旋转信封。

### Constraints

- $1 \leq envelopes.length \leq 10^5$
- $envelopes[i].length == 2$
- $1 \leq w_i, h_i \leq 10^5$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ ，表示信封的数量。
- 接下来 $N$ 行，每行包含两个整数 $w_i$ 和 $h_i$ ，表示每个信封的宽度和高度。

> $N$
> 
> $w_1 \quad h_1$
> 
> $w_2 \quad h_2$
> 
> $\ldots$
> 
> $w_N \quad h_N$

### Output

输出一个整数，表示最多能套娃的信封数目。

### Sample Input 1

```txt showLineNumbers=false
4
5 4
6 4
6 7
2 3
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
3
1 1
1 1
1 1
```

### Sample Output 2

```txt showLineNumbers=false
1
```

## 题目要点解析

二维偏序问题

## 最长数对链问题

[题目链接](https://leetcode.cn/problems/maximum-length-of-pair-chain)

### Problem Statement

给你一个包含 $n$ 个数对的数组 `pairs` ，其中 $pairs[i] = [left_i, right_i]$ 且 $left_i < right_i$ 。

现在，我们定义一种 **跟随** 关系，当且仅当 $b < c$ 时，数对 $p2 = [c, d]$ 才可以跟在 $p1 = [a, b]$ 后面。我们用这种形式来构造 **数对链** 。

请你返回能够形成的序列链的 **最长长度** 。

你不需要用到所有的数对，你可以以任何顺序选择其中的一些数对来构造。

### Constraints

- $n == pairs.length$
- $1 \leq n \leq 1000$
- $-1000 \leq left_i < right_i \leq 1000$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示数对的数量。
- 接下来 $n$ 行，每行包含两个整数 $left_i$ 和 $right_i$ 。

> $n$
> 
> $left_1 \quad right_1$
> 
> $left_2 \quad right_2$
> 
> $\ldots$
> 
> $left_n \quad right_n$

### Output

输出一个整数，表示最长数对链的长度。

### Sample Input 1

```txt showLineNumbers=false
3
1 2
2 3
3 4
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
3
1 2
7 8
4 5
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析



## 带修递增子序列

[题目链接](https://www.luogu.com.cn/problem/P8776)

### Problem Statement

给定一个长度为 $N$ 的整数序列：$A_1, A_2, \ldots, A_N$ 。你可以从中选择一个 **连续** 的区间，该区间的长度为 $K$ ，并将该区间内的所有数字全部修改成任意一个相同的整数。

请你返回在进行至多一次上述修改操作后，整个序列的 **最长不下降子序列** 的长度最大是多少。

最长不下降子序列的定义是：从原序列中按顺序取出若干个数字，使得这些数字满足非递减关系。

### Constraints

- $1 \leq K \leq N \leq 10^5$
- $1 \leq A_i \leq 10^6$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $K$ 。
- 第二行包含 $N$ 个整数，表示数组 $A$ 中的各个元素。

> $N \quad K$
> 
> $A_1 \quad A_2 \quad \ldots \quad A_N$

### Output

输出一个整数，表示在修改后能获得的最长不下降子序列的最大长度。

### Sample Input

```txt showLineNumbers=false
5 1
1 4 2 8 5
```

### Sample Output

```txt showLineNumbers=false
4
```

## 题目要点解析



## 使数组严格递增

[题目链接](https://leetcode.cn/problems/make-array-strictly-increasing/description/)

### Problem Statement

给你两个整数数组 `arr1` 和 `arr2` ，返回使 `arr1` 严格递增所需要的最小操作次数。

每一步操作中，你可以分别从 `arr1` 和 `arr2` 中各选出一个索引，分别为 $i$ 和 $j$ ，用 `arr2[j]` 替换 `arr1[i]` 。

如果无法让 `arr1` 严格递增，请返回 $-1$ 。

### Constraints

- $1 \leq arr1.length, arr2.length \leq 2000$
- $0 \leq arr1[i], arr2[i] \leq 10^9$

### Input

输入包含三行：

- 第一行包含两个整数 $N$ 和 $M$ ，分别表示 $arr1$ 和 $arr2$ 的长度。
- 第二行包含 $N$ 个整数，表示 $arr1$ 中的元素。
- 第三行包含 $M$ 个整数，表示 $arr2$ 中的元素。

> $N \quad M$
> 
> $arr1_0 \quad arr1_1 \quad \ldots \quad arr1_{N-1}$
> 
> $arr2_0 \quad arr2_1 \quad \ldots \quad arr2_{M-1}$

### Output

输出一个整数，表示使 $arr1$ 严格递增所需的最小操作次数。

### Sample Input 1

```txt showLineNumbers=false
4 3
1 5 3 6
1 3 2
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
4 3
1 5 3 6
4 3 1
```

### Sample Output 2

```txt showLineNumbers=false
2
```

### Sample Input 3

```txt showLineNumbers=false
4 3
1 5 3 6
1 6 3 3
```

### Sample Output 3

```txt showLineNumbers=false
-1
```

## 题目要点解析



## 最大不动点数目

[题目链接](https://leetcode.cn/problems/maximize-fixed-points-after-deletions/description/)



## 题目要点解析

二维偏序问题