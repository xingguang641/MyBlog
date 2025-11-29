---
title: 【ACM 算法随笔】差分思想
published: 2025-11-25
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 差分技巧与差分思想

差分是一种将区间操作转化为端点操作的技巧。对一个数组构造差分数组时，我们记录的是相邻元素之间的变化量：$d[i] = a[i] − a[i−1]$ 。原数组可以通过对差分数组求前缀和恢复出来。因此，差分的关键优势在于，它允许我们在只修改两个位置的前提下完成对整个区间的更新。例如，如果我们想让区间 $[l, r]$ 的所有元素都增加 $x$ ，在差分数组中仅需执行 `d[l] += x` 和 `d[r+1] -= x` 。之后在最终阶段对差分数组求一遍前缀和，就能得到修改后的完整数组。

差分非常适用于需要处理大量区间加减操作的情形，因为它将每次区间更新的时间复杂度从线性的 $O(n)$ 下降到常数级的 $O(1)$ 。在算法设计中，差分常常用于批量区间修改、构造前缀和结构、处理扫描线类问题等场景，是一种简洁而高效的基础技巧。

## 差分的广义视角

不过，我们今天并不是要讨论常见的 “差分数组” 这种标准技巧。经典差分侧重于把区间加法转成端点操作，再通过前缀和还原结果；它的结构固定、用途清晰。而在实际竞赛中，还有一类更灵活的 “差分思想” ———— 它并不拘泥于构造差分数组本身，而是借用 “记录变化、用局部信息推导整体行为” 这一核心理念，用在更复杂的场景里。

这种竞赛中的差分技巧往往不会显式地搭建一个差分数组，而是通过观察状态在相邻位置之间的变化，巧妙地构造出能敲开题目结构的突破口。它可能体现在计数方式的转移、前缀信息的对消、某些贡献的边界标记，甚至是用差分式的思维把看似难以处理的区间问题拆解成若干可控的点操作。与常规差分相比，它更加抽象，也更依赖对题目的结构理解，但在关键题型中常常能起到 “一剑封喉” 的效果。

# 等式变为不等式相关题目

在许多问题中，等式条件往往过于严格，直接求解会变得复杂又麻烦；相比之下，不等式的限制更宽松，通常更容易处理。因此，我们常通过一种差分式的思路，把原本的等式条件转化为两个不等式的差，从而简化计算过程。

$$
count(ans == k) = count(ans \leq k) - count(ans \leq k - 1)
$$

这种技巧的核心是：先解决更容易统计的不等式问题，再通过两者的差值恢复精确的等式计数。这样的转化在竞赛题中非常常见，也非常高效。

> 下面部分题目来源于这个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=405456839&bvid=BV1DG411d7fh&cid=29083175448&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

---

## K 个不同整数的子数组

[题目链接](https://leetcode.cn/problems/subarrays-with-k-different-integers/description/)

### Problem Statement

给定一个正整数数组 $nums$ 和一个整数 $k$ ，返回 $nums$ 中 **「好子数组」** 的数目。

如果 $nums$ 的某个子数组中不同整数的个数恰好为 $k$ ，则称 $nums$ 的这个连续、不一定不同的子数组为「好子数组」。

- 例如， $[1, 2, 3, 1, 2]$ 中有 3 个不同的整数：1，2，以及 3。

**子数组** 是数组的 **连续** 部分。

### Constraints

- $1 \leq nums.length \leq 2 * 10^4$
- $1 \leq nums[i], k \leq nums.length$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。其中，$N$ 表示数组的长度，$k$ 的含义已在题目描述中给出
- 第二行包含 $N$ 个整数，表示数组中的元素

> $N \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
5 2
1 2 1 2 3
```

### Sample Output 1

```txt showLineNumbers=false
7
```

### Sample Input 2

```txt showLineNumbers=false
5 3
1 2 1 3 4
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目解析

处理子数组问题时，一个自然的想法就是尝试使用滑动窗口。但滑动窗口并不是万能的，它要求问题本身具备某种单调性，否则窗口无法顺利扩张或收缩。判断是否具备单调性的标准，就是看条件是否随窗口长度的变化而 “越长越满足” 或 “越短越满足” ，其对应的两种条件分别是 “至少 $k$ 种” 和 “至多 $k$ 种” 。

在这道题中，原本的目标是统计 “恰好有 $k$ 个不同整数” 的子数组。但 “恰好” 这个等式条件本身是没有单调性的 ———— 窗口变大可能增加 distinct，也可能减少 distinct（因为移除左边不会影响右边）。这样的条件无法直接用滑动窗口解决。

因此我们需要借助前面提到的差分思想，把等式转化为两个更容易处理的不等式：

- 至多 $k$ 个不同整数
- 至多 $k - 1$ 个不同整数

这样，原问题就可以写成：

$$
count(distinct == k) = count(distinct \leq k) - count(distinct \leq k - 1)
$$

这两个不等式条件都能稳定地用滑动窗口求解，从而让我们间接得到 “恰好 $k$ ” 的结果。这是一个在竞赛中极其常见、非常高效的转化方法。

下面我们基于上述思路，给出本题的完整代码实现：

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 2e4 + 100;
int N, k;
int nums[MAXN];

int count(int k, int* a){
    int left = -1, pre = 0, ans = 0;
    unordered_map<int, int> counts;
    for (int right = 0; right < N; right ++){
        counts[a[right]] += 1;
        while (left <= right && (int)counts.size() > k){
            counts[a[++left]]--;
            if (!counts[a[left]])
                counts.erase(a[left]);
        }
        ans += right - left;
    }

    return ans;
}

int main() {
    cin >> N >> k;
    for (int i = 0; i < N; i++){
        cin >> nums[i];
    }

    cout << count(k, nums) - count(k - 1, nums);
}
```

---

# 参考文献

1. [【OI WiKi】前缀和 & 差分](https://oi-wiki.org/basic/prefix-sum/)

2. [【算法学习】算法技巧之差分](https://blog.csdn.net/myRealization/article/details/104594255)