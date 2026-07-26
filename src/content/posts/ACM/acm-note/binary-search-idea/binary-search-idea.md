---
title: 【ACM 算法随笔】二分查找与二分答案
published: 2025-11-26
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 二分查找基本原理

二分查找（Binary Search）是一种基于 **分治思想** 的经典检索算法，专门用于在 **有序序列** 中快速定位目标元素或寻找特定边界。算法通过不断选取当前搜索区间的中点进行可行性判断，根据判断结果直接舍弃不可能包含答案的一半区间，使搜索空间不断折半缩小。由于每轮搜索都会将搜索区间缩减一半，因此二分查找能够将查找问题的时间复杂度由 $O(n)$ 优化至 $O(\log n)$ ，是算法竞赛中最常用的基础算法之一。

在规模为 $n$ 的有序数组中，顺序查找在最坏情况下需要遍历整个序列，而二分查找仅需进行约 $\log_2 n$ 次比较即可完成查找。这意味着即便数据规模从百万级增长到十亿级，比较次数也仅从约 $20$ 次增加到约 $30$ 次。由此我们可以知道，随着数据规模不断增大，二分查找的优势也会愈发明显。

在实际应用中，二分查找通常有四种标准形式，分别对应四类边界查找：

- 最后一个 $< K$ 的位置，第一个 $\geq K$ 的位置
- 最后一个 $\leq K$ 的位置，第一个 $> K$ 的位置

尽管这四种形式的查找目标不同，但其代码框架高度一致，核心差异只体现在 **比较条件的选取** 与 **收缩策略的定义** 两个方面。从数轴的角度来看，它们本质上都是在有序序列中寻找某个特定性质的 **临界分割点** 。

![四种二分图像](src\content\posts\ACM\acm-note\binary-search-idea\四种二分1.png)

尽管这四种形式对应不同的边界，但其实现思路完全一致。理解的关键在于明确查找目标是满足条件的 **最小位置** 还是 **最大位置** ，再根据目标设计相应的比较条件和区间收缩方式，使搜索区间不断向目标边界收敛。下面将分别介绍这四种二分写法，并进一步总结出统一的二分模板。

## 二分的代码详解

下文给出的四段代码分别对应前文介绍的四种二分形式。为了统一代码风格，所有实现均采用 **闭区间 $[l, r]$** 的写法，并以 `l <= r` 作为循环条件。为了能够稳定地记录下答案，每种写法均使用 **辅助变量 ans** 保存当前满足条件的候选位置，从而保证循环结束后仍能正确返回最终答案。

虽然四种二分形式的查找目标不同，但它们都遵循相同的代码框架，核心差异仅体现在 **判定条件** 和 **区间收缩方向** 两个方面。掌握这两处变化，便能够快速写出四种标准二分模板，并灵活解决不同类型的边界查找问题。

### 最后一个 < K 的位置

```cpp title="main.cpp"
int lastLess(int a[], int n, int K) {
    int l = 0, r = n - 1, ans = -1;
    while (l <= r) {
        int m = (l + r) / 2;
        if (a[m] < K) {
            ans = m;
            l = m + 1;
        } else {
            r = m - 1;
        }
    }
    return ans;
}
```

该二分用于查找 **严格小于 K 的最大下标** 。

- 当 `a[m] < K` 时，将当前下标 `m` 记录到 `ans` 中，并更新左边界
- 当 `a[m] >= K` 时，不更新 `ans` ，并更新右边界

若最终不存在满足条件的元素，则 `ans` 保持为 `-1` ，函数返回 `-1` 。

### 第一个 ≥ K 的位置

```cpp title="main.cpp"
int firstGreaterEqual(int a[], int n, int K) {
    int l = 0, r = n - 1, ans = n;
    while (l <= r) {
        int m = (l + r) / 2;
        if (a[m] >= K) {
            ans = m;
            r = m - 1;
        } else {
            l = m + 1;
        }
    }
    return ans;
}
```

该二分用于查找 **大于等于 K 的最小下标** 。

- 当 `a[m] >= K` 时，将当前下标 `m` 记录到 `ans` 中，并更新右边界
- 当 `a[m] < K` 时，不更新 `ans` ，并更新左边界

若不存在满足条件的元素，则 `ans` 保持为 `n` ，函数返回 `n` 。

### 最后一个 ≤ K 的位置

```cpp title="main.cpp"
int lastLessEqual(int a[], int n, int K) {
    int l = 0, r = n - 1, ans = -1;
    while (l <= r) {
        int m = (l + r) / 2;
        if (a[m] <= K) {
            ans = m;
            l = m + 1;
        } else {
            r = m - 1;
        }
    }
    return ans;
}
```

该二分用于查找 **小于等于 K 的最大下标** 。

- 当 `a[m] <= K` 时，将当前下标 `m` 记录到 `ans` 中，并更新左边界
- 当 `a[m] > K` 时，不更新 `ans` ，并更新右边界

若最终不存在满足条件的元素，则 `ans` 保持为 `-1` ，函数返回 `-1` 。

### 第一个 > K 的位置

```cpp title="main.cpp"
int firstGreater(int a[], int n, int K) {
    int l = 0, r = n - 1;
    int ans = n;
    while (l <= r) {
        int m = (l + r) / 2;
        if (a[m] > K) {
            ans = m;
            r = m - 1;
        } else {
            l = m + 1;
        }
    }
    return ans;
}
```

该二分用于查找 **严格大于 K 的最小下标** 。

- 当 `a[m] > K` 时，将当前下标 `m` 记录到 `ans` 中，并更新右边界
- 当 `a[m] <= K` 时，不更新 `ans` ，并更新左边界

若不存在满足条件的元素，则 `ans` 保持为 `n` ，函数返回 `n` 。

## 二分的代码比较

前文已经介绍了四种二分的标准模板，虽然它们之间只存在少数几处差异，但这些差异正是决定最终查找边界的关键。接下来将围绕 **判定条件与答案更新的时机** 以及 **搜索区间的收缩方向** 两个方面进行分析。

首先来看判定条件和答案更新方式：

```cpp
if (a[m] < K) {
    ans = m;
}
```

既然我们的目标是查找满足 `< K` 的位置，那么判断条件就应当直接写成 `< K` 。同时 `ans` 的更新逻辑也必须放在这一判断条件内部，因为只有在 `a[m] < K` 成立时，当前位置 $m$ 才是一个真实满足条件的位置。

这一规律在其他三种二分形式中同样适用。判断语句中的比较关系直接对应当前二分的查找目标，因此只有在当前位置 $m$ 满足判定条件时，才会将其记录为候选答案，而 `ans` 始终保存最近一次满足条件的位置。 

接下来看搜索区间的收缩方向：

```cpp
if (a[m] < K) {
    ans = m;
    l = m + 1;
}
```

在当前位置满足判定条件并记录答案后，我们需要继续缩小搜索区间。若目标是寻找 **最后一个** 满足条件的位置，则需要继续搜索右半区间，确认是否还存在下标更大的合法位置，因此执行 `l = m + 1` 。若目标是寻找 **第一个** 满足条件的位置，则需要继续搜索左半区间，确认是否还存在下标更小的合法位置，因此执行 `r = m - 1` 。

由此可以发现，区间的收缩方向完全由查找目标决定。若寻找 **最后一个** 满足条件的位置就向右搜索，若寻找 **第一个** 满足条件的位置就向左搜索。掌握这一规律后，便能够快速写出四种标准二分。

---

# 二分查找相关问题

二分查找是一种建立在 **单调性** 上的高效算法，其核心思想是通过不断缩小搜索区间，在 **对数时间复杂度** 内定位目标位置。与顺序扫描不同，二分查找利用题目条件的单调性，根据当前判断结果缩小搜索区间，从而快速逼近最终结果。正因如此，掌握二分查找不仅需要熟悉代码模板，更重要的是能够识别并利用问题中的单调性。

二分查找通常有两类典型应用，第一类是在 **有序数据** 中查找目标元素或满足条件的边界。第二类则是利用题目条件的 **单调性** ，将问题转化为一个二值判定过程，通过寻找判定结果发生变化的 **临界点** 得到最终答案。许多题目并不会直接给出有序序列，而是需要分析题目的性质，构造出具有单调性的判定过程，再利用二分查找完成求解。

## 第K缺失正整数

[题目链接](https://leetcode.cn/problems/kth-missing-positive-number/description/)

### Problem Statement

给你一个 **严格递增** 的正整数数组 `arr` 和一个整数 `k` 。

请你找出这个数组中第 `k` 个缺失的正整数。

### Constraints

- $1 \leq arr.length \leq 1000$
- $1 \leq arr[i] \leq 1000$
- $1 \leq k \leq 1000$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ ，分别表示数组长度和缺失正整数的序号。
- 第二行包含 $n$ 个整数，表示数组 $arr$ 中的元素。

> $n \quad k$
>
> $arr_1 \quad arr_2 \quad \ldots \quad arr_n$

### Output

输出一个整数，表示第 $k$ 个缺失的正整数。

### Sample Input 1

```txt showLineNumbers=false
5 5
2 3 4 7 11
```

### Sample Output 1

```txt showLineNumbers=false
9
```

### Sample Input 2

```txt showLineNumbers=false
4 2
1 2 3 4
```

### Sample Output 2

```txt showLineNumbers=false
6
```

## 题目要点解析

二分查找第K个缺失的正整数大致位置在哪

## 剩余元素第K小

[题目链接](https://leetcode.cn/problems/k-th-smallest-remaining-even-integer-in-subarray-queries/description/)

### Problem Statement

给你一个整数数组 $nums$ ，其中 $nums$ 是 **严格递增** 的。

另给你一个二维整数数组 $queries$ ，其中 `queries[i] = [li, ri, ki]` 。

对于每个查询 `[li, ri, ki]`：

- 考虑 **子数组** `nums[li..ri]`
- 从 **无限** 的所有 **正偶数** 序列中：`2, 4, 6, 8, 10, 12, 14, ...`
- **移除** 所有出现在 **子数组** `nums[li..ri]` 中的元素
- 找到移除后序列中剩余的第 $k_i$ 个 **最小整数**

返回一个整数数组 `ans` ，其中 `ans[i]` 是第 $i$ 个查询的结果。

**子数组** 是数组中连续的 **非空** 元素序列。

如果数组中的每个元素都 **严格大于** 它的 **前一个** 元素（如果存在），则称该数组是 **严格递增** 的。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $1 \leq nums_i \leq 10^9$
- $1 \leq Q \leq 10^5$
- $0 \leq l \leq r < nums.length$
- $1 \leq k \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ ，表示数组 $nums$ 的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。
- 第三行包含一个整数 $Q$ ，表示查询的次数。
- 接下来 $Q$ 行，每行包含三个整数 $l_i, r_i, k_i$ ，表示一次查询。

> $N$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$
>
> $Q$
>
> $l_1 \quad r_1 \quad k_1$
>
> $\ldots$
>
> $l_Q \quad r_Q \quad k_Q$

### Output

输出包含 $Q$ 行，每行包含一个整数表示该次查询的答案。

### Sample Input

```txt showLineNumbers=false
3
1 4 7
3
0 2 1
1 1 2
0 0 3
```

### Sample Output

```txt showLineNumbers=false
2
6
6
```

## 题目要点解析



## 失配字符串问题

[题目链接](https://leetcode.cn/problems/substring-with-concatenation-of-all-words/description/)

### Problem Statement

给定一个字符串 `s` 和一个字符串数组 `words` 。`words` 中所有字符串的 **长度相同** 。

`s` 中的 **串联子串** 是指一个包含 `words` 中所有字符串以任意顺序排列连接起来的子串。

- 如果 `words = ["ab", "cd"]` ，那么 `"abcd"` 和 `"cdab"` 是串联子串。
- `"acdb"` 不是串联子串，因为他不是 `words` 排列的连接。

请你返回所有串联子串在 `s` 中的开始索引。你可以按 **任意顺序** 返回答案。

### Constraints

- $1 \leq s.length \leq 10^4$
- $1 \leq words.length \leq 5000$
- $1 \leq words[i].length \leq 30$
- `s` 和 `words[i]` 仅由小写英文字母组成

### Input

输入包含三行：

- 第一行包含一个字符串 $s$ 。
- 第二行包含一个整数 $M$ ，表示数组 $words$ 的长度。
- 第三行包含 $M$ 个由空格隔开的字符串，表示数组 $words$ 中的元素。

> $s$
>
> $M$
>
> $words_1 \quad words_2 \quad \ldots \quad words_M$

### Output

输出若干个整数，表示所有串联子串在 `s` 中的开始索引；如果没有满足条件的子串，则输出 `-1` 。

### Sample Input 1

```txt showLineNumbers=false
barfoothefoobarman
2
foo bar
```

### Sample Output 1

```txt showLineNumbers=false
0 9
```

### Sample Input 2

```txt showLineNumbers=false
wordgoodgoodgoodbestword
4
word good best word

```

### Sample Output 2

```txt showLineNumbers=false
-1
```

### Sample Input 3

```txt showLineNumbers=false
barfoofoobarthefoobarman
3
bar foo the
```

### Sample Output 3

```txt showLineNumbers=false
6 9 12
```

## 题目要点解析

二分查找不同点+字符串哈希

---

# 最大值最小化问题

最大值最小化问题是算法竞赛中常见的一类 **优化问题** 。其核心思想是在难以直接构造最优方案时，将目标从寻找具体方案转化为对 **答案范围** 的判断。通过枚举一个候选上限，并判断在该限制下是否存在可行方案，我们可以不断缩小答案范围，最终找到满足要求的 **最小值** 。

从理论上看，最大值最小化问题一定可以通过二分解决。我们将答案视为一个上界，并判断在该上界下是否存在 **可行方案** 。如果当前上界无法满足，那么更小的上界一定也无法满足。如果当前上界可以满足，那么更大的上界也一定可以满足。因此可行与不可行之间必然存在一个 **分界位置** ，二分正是通过定位这个位置得到 **最优答案** 。

## 分割数组最大值

[题目链接](https://leetcode.cn/problems/split-array-largest-sum/description/)

### Problem Statement

给定一个非负整数数组 $nums$ 和一个整数 $k$ ，你需要将这个数组分成 $k$ 个非空的连续子数组，使得这 $k$ 个子数组各自和的最大值 **最小** 。

### Constraints

- $1 \leq nums.length \leq 1000$
- $0 \leq nums[i] \leq 10^6$
- $1 \leq k \leq min\{50, nums.length\}$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
5 2
7 2 5 10 8
```

### Sample Output 1

```txt showLineNumbers=false
18
```

### Sample Input 2

```txt showLineNumbers=false
5 2
1 2 3 4 5
```

### Sample Output 2

```txt showLineNumbers=false
9
```

## 题目要点解析

该问题的背景是经典的 **画匠问题** ，也是 **最大值最小化问题** 的典型应用。题目的目标并不是直接构造一种最优划分方案，而是寻找所有方案中最小的最大值。因此我们可以转换思路，将原本的优化问题转化为对答案的判定问题。

具体来说，我们可以假设每个子数组的和不能超过某个上限 $X$ ，然后判断在这个限制下，是否能够将数组划分为 $K$ 个连续子数组。如果固定的上限 $X$ 越大，能够满足条件的划分方案只会越来越多，因此该判定过程具有明显的单调性。也正因为这种单调关系，我们可以利用二分不断调整答案范围，寻找满足条件的最小上限。

- **搜索空间**：二分查找的对象并不是数组元素，而是最终答案的可能范围 $[L, R]$
- **搜索目标**：寻找第一个满足判定条件的答案，也就是最小的可行上限 $X_{opt}$

通过这种方式，原本难以直接求解的最优化问题被转化为了简单的可行性判断。在判定过程中，我们只需要通过一次贪心扫描判断当前上限是否能够完成划分，从而将复杂的方案构造转化为高效的答案搜索。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

## 通往奥格瑞玛城

[题目链接](https://www.luogu.com.cn/problem/P1462)

### Problem Statement

在艾泽拉斯大陆上有一位名叫歪嘴哦的神奇术士，他是部落的中坚力量。有一天他醒来后发现自己居然到了联盟的主城暴风城。在被众多联盟的士兵攻击后，他决定逃回自己的家乡奥格瑞玛。

在艾泽拉斯，有 $n$ 个城市，编号为 $1, 2, 3, \ldots, n$ 。城市之间有 $m$ 条双向的公路。每经过一条公路，都会遭到攻击并损失一定的血量。此外，每当进入一个城市（包括起点和终点），都会被收取一定的费用。

当前掌握的信息如下：

- 城市 $1$ 为暴风城，城市 $n$ 为奥格瑞玛
- 术士的最大血量为 $b$ ，出发时血量是满的
- 若在途中血量降为负数，则无法到达终点

术士希望尽量少花钱。现在需要找到一条从 $1$ 到 $n$ 的路径，使得在血量不降为负的前提下，**路径上经过城市的单次收费最大值尽可能小** 。如果无法到达奥格瑞玛，则输出 `AFK` 。

### Constraints

- $1 \leq n \leq 10^4$
- $1 \leq m \leq 5 \times 10^4$
- $1 \leq b \leq 10^9$
- $1 \leq c_i \leq 10^9$
- $0 \leq f_i \leq 10^9$
- 可能存在重边

### Input

输入包含多行：

- 第一行三个整数 $n$ 、$m$ 和 $b$ ，分别表示城市与道路的数量，以及术士的最大血量。
- 接下来 $n$ 行，每行一个整数 $f_i$ ，表示经过城市 $i$ 需要支付的费用。
- 接下来 $m$ 行，每行三个整数 $a_i, b_i, c_i$ ，表示城市 $a_i$ 与 $b_i$ 之间有一条双向公路，通过会损失 $c_i$ 的血量。

> $n \quad m \quad b$
> 
> $f_1$
> 
> $f_2$
> 
> $\ldots$
> 
> $f_n$
> 
> $a_1 \quad b_1 \quad c_1$
> 
> $\ldots$
> 
> $a_m \quad b_m \quad c_m$

### Output

输出一个整数，表示路径上单次城市收费最大值的最小可能值。如果无法到达城市 $n$ ，输出 `AFK` 。

### Sample Input

```txt showLineNumbers=false
4 4 8
8
5
6
10
2 1 2
2 4 1
1 3 4
3 4 3
```

### Sample Output

```txt showLineNumbers=false
10
```

## 题目要点解析

这道题属于 **最大值最小化问题** 的另一个经典应用，其本质是寻找一条满足约束的路径，使路径上的最大城市费用尽可能小。对于这类问题，通常可以通过二分答案，将优化目标转化为可行性判断。由于答案范围具有明显的 **单调性** ，当允许的最大费用增加时，能够选择的路径只会增多不会减少，因此可以通过二分快速定位最优答案。

题目要求从城市 $1$ 走到城市 $n$ ，每经过一个城市需要支付费用 $f_i$ ，同时每条道路会消耗一定血量，而总血量损失不能超过 $b$ 。如果我们把路径中经过城市的费用最大值记为 $x$ ，那么问题就转化为：

> 在只允许经过 $f_i \leq x$ 的城市的情况下，是否还能从 $1$ 走到 $n$ ，并且总血量损失不超过 $b$ 。

对于这个判定过程，如果某个 $x$ 可以满足要求，那么更大的费用限制一定也可以满足，因为允许经过的城市只会增加。因此可行与不可行之间存在一个明确的分界点，我们可以通过二分寻找最小的可行值。

在具体实现中，我们可以二分得到最大城市费用 $mid$ ，并筛选出所有满足 $f_i \leq mid$ 的城市。随后在保留下来的图中执行最短路算法，其中边权表示经过道路损失的血量。若从城市 $1$ 到城市 $n$ 的最短距离不超过 $b$ ，说明当前的费用限制可行；否则说明当前的费用限制过小，需要扩大允许的费用范围。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

---

# 离线型中位数问题

二分答案法在 **求解中位数或第 k 小值** 的问题中同样非常有效。对于这些静态、离线处理的场景，我们无需直接寻找答案本身，而是对 **答案的取值空间** 进行二分。每当二分到一个候选数 $x$ 时，只需统计有多少元素小于或等于 $x$ ，就能判断 $x$ 是否满足第 $k$ 小值的要求。通过不断缩小搜索区间，最终便可以锁定真实的中位数或第 $k$ 小值。

这种思路其实用到了[广义差分](https://xingguang641.com/posts/acm/acm-note/difference-idea/#差分的广义视角)的逻辑。直接定位中位数是一个极其严苛的点约束，要求数值在全局排序中精确对位，而二分答案则将这一硬性条件拆解为更宽松的范围统计，即计算 “小于等于 $x$ 的元素个数” 。这种以面求点的方式，本质上是将复杂的全局序关系简化为数值在值域区间上的贡献分布。通过判断计数值是否超过所需总数，利用单调性不断逼近真相，将原本难以处理的单值查询转化为简单的计数查询。

在一些更复杂的题目中，仅仅统计 $\leq x$ 的数量还不够，往往还需要结合 **二值化（01 化）技巧** 。具体来说，可以将数组中的元素根据当前二分值 $x$ 进行转化，例如把满足条件的元素映射为 $1$ ，不满足的映射为 $-1$ 或 $0$ 。这样原本的 **中位数判定问题** 就可以转化为 **前缀和或子段和是否满足某种性质的问题** ，从而借助前缀和、树状数组或平衡树等数据结构高效完成统计。若想具体了解二值化技巧，可以看[这篇博客](https://www.cnblogs.com/dbywsc/p/19065445)。

而在需要[动态维护中位数](https://xingguang641.com/posts/acm/acm-note/priority-queue/#数据流中位数问题)的场景中，通常会采用 **堆顶对** 的结构：用一个最大堆维护较小的一半元素，用一个最小堆维护较大的一半元素。这样在每次插入新元素后，都能迅速得到当前的中位数。此外，当题目要求 **输出前 k 个最优答案** 时，也需要使用优先队列。这类问题通常会维护一个优先队列来持续扩充当前最优状态，每次取出当前最小（或最大）的候选解，并生成新的候选结果。通过这种方式，可以按顺序得到前 $k$ 个答案，而无需枚举所有可能情况，大大降低时间复杂度。

### 离线型平均数问题

与中位数类似，**平均数最大化或最小化** 的问题也可以通过 **二分答案法** 来解决。设数组为 $A_1,A_2,\ldots,A_n$ ，如果题目要求在某种约束条件下找到 **最大平均值** ，我们通常并不会直接计算平均数，而是对答案 $x$ 进行二分。对于每一个候选值 $x$ ，我们只需要判断是否存在一个合法的选择方案，使得该方案的平均值 **不小于 x** 。

平均值问题的关键在于一个常见的代数变形，若某个集合 $S$ 的平均值满足：

$$
\frac{\sum_{i \in S} A_i}{|S|} \geq x
$$

则原式等价于：

$$
\sum_{i \in S} (A_i - x) \geq 0
$$

这样一来，只需要将原数组进行一次 **线性变换 $B_i = A_i - x$** ，原问题就转化为 **是否存在一个合法集合 S，使得数组累加和大于 0** 。此时问题已经不再涉及平均值，而变成了一个 **最大子段和或最大权值选择问题** ，通常可以通过动态规划或使用数据结构来判断。这一技巧在算法竞赛中非常常见，通过将平均值转化为线性和的形式，可以有效避免直接处理分数带来的复杂性，从而使问题可以使用常见的数据结构和动态规划方法解决。

## 第K小数对距离

[题目链接](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/description/)

### Problem Statement

数对 `(a, b)` 由整数 `a` 和 `b` 组成，其数对距离定义为 `a` 和 `b` 的绝对差值。

给你一个整数数组 `nums` 和一个整数 $k$ ，数对由 `nums[i]` 和 `nums[j]` 组成且满足 $0 <= i < j < n$ ，$n$ 表示数组长度。返回 **所有数对距离中** 第 `k` 小的数对距离。

### Constraints

- $2 \leq n \leq 10^4$
- $0 \leq nums[i] \leq 10^6$
- $1 \leq k \leq n * (n - 1) / 2$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ 。
- 第二行包含 $n$ 个整数，表示数组中的元素。

> $n \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3 1
1 3 1
```

### Sample Output 1

```txt showLineNumbers=false
0
```

### Sample Input 2

```txt showLineNumbers=false
3 2
1 1 1
```

### Sample Output 2

```txt showLineNumbers=false
0
```

### Sample Input 3

```txt showLineNumbers=false
3 3
1 6 1
```

### Sample Output 3

```txt showLineNumbers=false
5
```

## 题目要点解析

这道题的目标是找到所有数对距离中的 **第 k 小值** 。由于数对的总数达到了 $O(n^2)$ 级别，直接枚举并排序在 $n=10^4$ 的数据规模下会超时。因此，我们需要转换思路，将问题看作是对 **距离值域** 的二分查找。我们并不直接去数对中寻找目标，而是通过二分一个候选距离 $X$ ，来判定真实答案与 $X$ 的位置关系。

这种转化的核心逻辑在于统计 **距离小于或等于 X 的数对数量** 。如果这个数量大于或等于 $k$ ，说明我们设定的距离 $X$ 已经覆盖了足够多的数对，第 $k$ 小的距离一定就在 $X$ 或者比 $X$ 更小的范围内，此时我们记录答案并尝试向左缩小距离上限。反之，如果数量小于 $k$ ，则说明 $X$ 定得太小，目标距离一定在 $X$ 的右侧。

为了快速完成统计，我们可以先对数组进行排序。在有序序列中，利用 **双指针** 技巧可以在 $O(n)$ 的时间内扫描出所有满足条件的数对，而无需嵌套循环。通过在 $0$ 到数组最大差值之间进行二分，配合这个高效的计数函数，我们就能在对数时间内精准锁定第 $k$ 小的数对距离。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

## 唯一数组中位数

[题目链接](https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/description/)

### Problem Statement

给你一个整数数组 `nums` 。数组 `nums` 的 **唯一性数组** 是一个按元素从小到大排序的数组，包含了 `nums` 的所有非空子数组中不同元素的个数。

换句话说，这是由所有 $0 \leq i \leq j < nums.length$ 的 `distinct(nums[i..j])` 组成的递增数组。

其中，`distinct(nums[i..j])` 表示从下标 $i$ 到下标 $j$ 的子数组中不同元素的数量。

返回 `nums` 唯一性数组的中位数。

注意，数组的中位数定义为有序数组的中间元素。如果有两个中间元素，则取值较小的那个。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $1 \leq nums[i] \leq 10^5$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示数组元素。

> $n$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出一个整数，表示唯一性数组的中位数。

### Sample Input 1

```txt showLineNumbers=false
3
1 2 3
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
5
3 4 3 4 5
```

### Sample Output 2

```txt showLineNumbers=false
2
```

### Sample Input 3

```txt showLineNumbers=false
4
4 3 5 4
```

### Sample Output 3

```txt showLineNumbers=false
2
```

## 题目要点解析



## 平均数与中位数

[题目链接](https://atcoder.jp/contests/abc236/tasks/abc236_e)

### Problem Statement

有 $N$ 张卡片，第 $i$ 张卡片上写着一个整数 $A_i$ 。高桥可以从这些卡片中选择任意多张，但必须满足一个条件：对于每个 $i$ ，第 $i$ 张卡片和第 $i+1$ 张卡片 **至少要选择一张** 。也就是说，**不允许存在两个相邻的卡片都不被选择** 。 

在所有满足条件的选择方案中，请求出：

1. 所选卡片上数字的 **平均值的最大可能值**
2. 所选卡片上数字的 **中位数的最大可能值**

需要注意的是：中位数定义为上中位数，平均数只要与正确答案的 **误差不超过 $10^{-3}$** 即可视为正确。

### Constraints

- $2 \leq N \leq 10^5$
- $1 \leq A_i \leq 10^9$
- 所有输入均为整数

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示卡片数量。
- 第二行包含 $N$ 个整数，表示每张卡片上的数字。

> $N$
> 
> $A_1 \quad A_2 \quad \ldots \quad A_N$

### Output

输出包含两行：

- 第一行输出所选卡片数字的 **最大可能平均值**
- 第二行输出所选卡片数字的 **最大可能中位数**

### Sample Input 1

```txt showLineNumbers=false
6
2 1 2 1 1 10
```

### Sample Output 1

```txt showLineNumbers=false
4
2
```

### Sample Input 2

```txt showLineNumbers=false
7
3 1 4 1 5 9 2
```

### Sample Output 2

```txt showLineNumbers=false
5.250000000
4
```

## 题目要点解析

[打家劫舍对偶问题](https://xingguang641.com/posts/acm/acm-type/dp-problems/maximum-subarray-sum/#打家劫舍对偶问题)

---

# 逆向分析求解问题

在算法竞赛的解题过程中，如果沿着题意正向推导，往往会面临难以处理的动态约束，此时**逆向求解** 便成了一种极为方便的解题思路。其核心逻辑在于：我们不再纠结如何直接构造出最优解，而是先假设一个候选答案 $x$ ，随后尝试判断这个 $x$ 是否能够满足题目给出的所有约束条件。

这种先猜后验的思想能够演变为经典的 **二分答案法** ，主要依赖两个前置条件。首先，题目通常带有极强的 **最值信号** ，如 “最大/最小” 、“至多/至少” 等字眼。当问题的目标是逼近某个临界点，逆向验证的价值才会凸显。其次，解空间必须具备 **单调性** 。随着候选答案 $x$ 的增减，满足条件的可能性必须呈现单向变化。若设定上界为 $k$ 时方案可行，那么放宽至 $k+1$ 也必然可行。这种性质确保了我们可以通过不断调整限制，在对数时间内锁定判定函数从 $\text{False}$ 跃迁至 $\text{True}$ 的临界点。

通过这种逆向思考，我们将棘手的 **最优化问题** 降级为了简单的 **判定性问题** 。这种重心转移极大地简化了代码实现的难度：我们不需要在复杂的约束中寻找最优解法，而是从答案出发，通过不断的逻辑校验来缩小搜索空间。这种逆向求解的思路，是解决高难度约束优化问题的核心套路。

## 刀砍与毒杀怪兽

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class051/Code07_CutOrPoison.java)

### Problem Statement

怪兽的初始血量是一个整数 $hp$ ，给出每一回合刀砍和毒杀的数值 $cuts$ 和 $poisons$ 。第 $i$ 回合如果用刀砍，怪兽在这回合会直接损失 $cuts[i]$ 的血，不再有后续效果；第 $i$ 回合如果用毒杀，怪兽在这回合不会损失血量，但是之后每回合都损失 $poisons[i]$ 的血量，并且所有毒杀效果可以叠加。

两个数组 $cuts$ 、$poisons$ ，长度都是 $n$ ，代表你一共可以进行 $n$ 回合。每一回合你只能选择刀砍或者毒杀中的一个动作，如果你在 $n$ 个回合内没有直接杀死怪兽，意味着你已经无法有新的行动了。但是怪兽如果有中毒效果的话，那么怪兽依然会在血量耗尽的那回合死掉。

返回至少多少回合，怪兽会死掉。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq hp \leq 10^9$
- $1 \leq cuts[i], poisons[i] \leq 10^9$

### Input

输入包含三行：

- 第一行包含两个个整数 $n$ 和 $hp$ 。
- 第二行包含 $n$ 个整数，表示 $cuts$ 数组中的元素。
- 第三行包含 $n$ 个整数，表示 $poisons$ 数组中的元素。

> $n \quad hp$
>
> $cuts_1 \quad cuts_2 \quad \ldots \quad cuts_n$
>
> $poisons_1 \quad poisons_2 \quad \ldots \quad poisons_n$

### Output

输出一个整数表示答案。

## 题目要点解析

这道题的核心难点在于 **伤害收益的动态变化** 。刀砍产生的伤害是即时的固定值，而毒杀的收益则取决于后续还能持续多少个回合。在不确定总回合数的情况下，我们很难在每一回合做出最优选择。但如果我们转换思路，假设已知怪兽会在第 $T$ 个回合死掉，那么第 $i$ 回合选择毒杀所能提供的总伤害就固定为 $(T - i) \times poisons[i]$ 。

这种性质使得问题具备了明显的 **单调性**：如果怪兽能在 $T$ 个回合内被击败，那么在更长的回合数（如 $T+1$ ）里也一定能被击败。反之，如果 $T$ 个回合不够，那么更短的时间内也绝对无法达成目标。基于这种单调性，我们可以通过 **二分答案** 来搜索最小的达标回合数。

在具体的判定逻辑中，当我们假定总时长为 $T$ 时，每一回合的选择就变得非常简单：只需要对比当前回合 “刀砍的固定伤害” 与 “毒杀直到第 $T$ 回合能累积的总伤害” 并直接选择较大者即可。通过贪心地累加每一回合的最优伤害，再判断总和是否达到怪兽的血量 $hp$ ，我们就能在对数时间内锁定最少的回合数。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

## 打家劫舍问题IV

[题目链接](https://leetcode.cn/problems/house-robber-iv)

### Problem Statement

沿街有一排连续的房屋。每间房屋内都藏有一定的现金。现在有一位小偷计划从这些房屋中窃取现金。由于相邻的房屋装有相互连通的防盗系统，所以小偷 **不会窃取相邻的房屋** 。小偷的 **窃取能力** 定义为他在窃取过程中能从单间房屋中窃取的 **最大金额** 。

给你一个整数数组 `nums` 表示每间房屋存放的现金金额。形式上，从左起第 `i` 间房屋中放有 `nums[i]` 美元。另给你一个整数 `k` ，表示窃贼将会窃取的 **最少** 房屋数。小偷总能窃取至少 `k` 间房屋。

返回小偷的 **最小** 窃取能力。

### Constraints

- $1 \leq n.length \leq 10^5$
- $0 \leq nums[i] \leq 10^9$
- $0 \leq k \leq (nums.length + 1) / 2$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ 。
- 第二行包含 $n$ 个整数，表示数组的元素。

> $n \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
4 2
2 3 5 9
```

### Sample Output 1

```txt showLineNumbers=false
5
```

### Sample Input 2

```txt showLineNumbers=false
5 2
2 7 9 3 1
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析



## 饥饿的高桥先生

[题目链接](https://atcoder.jp/contests/abc415/tasks/abc415_e)

### Problem Statement

给定一个 $H \times W$ 的网格，每个单元格 $(i, j)$ 上都有 $A_{i, j}$ 枚硬币。高桥初始位于 $(1, 1)$ 且持有 $x$ 枚硬币。

高桥需要在 $H + W - 1$ 天内完成移动，规则如下：
1. **收集硬币**：高桥到达一个单元格时，收集该单元格上的所有 $A_{i, j}$ 枚硬币。
2. **购买食物**：在每一天（即到达一个新的单元格后），他必须消耗 $P_k$ 枚硬币购买食物。如果手中持有的硬币少于 $P_k$ ，他将因饥饿倒下。
3. **行动逻辑**：如果 $k < H + W - 1$ ，高桥可以选择向下移动或向右移动。如果 $k = H + W - 1$ ，他停留在当前位置。

请找出使高桥能够不因饥饿而完成所有 $H+W-1$ 天移动的最小非负整数 $x$。

### Constraints

- $1 \leq H, W \leq 100$
- $1 \leq A_{i, j} \leq 10^9$
- $1 \leq P_k \leq 10^9$

### Input

输入包含多行：

- 第一行包含两个整数 $H$ 和 $W$ 。
- 接下来 $H$ 行，每行包含 $W$ 个整数，表示网格各单元格的硬币数量 $A_{i, j}$ 。
- 最后一行包含 $H + W - 1$ 个整数，表示每天需消耗的硬币数量 $P_i$ 。

> $H \quad W$
>
> $A_{1, 1} \quad A_{1, 2} \quad \ldots \quad A_{1, W}$
>
> $\ldots$
>
> $A_{H, 1} \quad A_{H, 2} \quad \ldots \quad A_{H, W}$
>
> $P_1 \quad P_2 \quad \ldots \quad P_{H+W-1}$

### Output

输出一个整数，表示满足条件所需的最小初始硬币数量。

### Sample Input

```txt showLineNumbers=false
2 2
3 1
4 1
1 3 6
```

### Sample Output

```txt showLineNumbers=false
2
```

## 题目要点解析

反向DP 或 二分+正向DP

## 可安排的任务数

[题目链接](https://leetcode.cn/problems/maximum-number-of-tasks-you-can-assign/description/)

### Problem Statement

给你 $n$ 个任务和 $m$ 个工人。每个任务需要一定的力量值才能完成，需要的力量值保存在下标从 0 开始的整数数组 $tasks$ 中，第 $i$ 个任务需要 $tasks[i]$ 的力量才能完成。每个工人的力量值保存在下标从 $0$ 开始的整数数组 $workers$ 中，第 $j$ 个工人的力量值为 $workers[j]$ 。

每个工人只能完成 **一个** 任务，且力量值需要 **大于等于** 该任务的力量要求值（即 $workers[j] >= tasks[i]$ ）。除此以外，你还有 $pills$ 个神奇药丸，可以给 **一个工人的力量值** 增加 $strength$ 。你可以决定给哪些工人使用药丸，但每个工人 **最多** 只能使用 **一片** 药丸。

请你返回 **最多** 有多少个任务可以被完成。

### Constraints

- $n == tasks.length$
- $m == workers.length$
- $1 \leq n, m \leq 5 * 10^4$
- $0 \leq pills \leq m$
- $0 \leq tasks[i], workers[j], strength \leq 10^9$

### Input

输入包含三行：

- 第一行包含四个整数 $n$ 、$m$ 、$pills$ 和 $strength$ 。
- 第二行包含 $n$ 个整数，表示 $tasks$ 数组中的元素。
- 第三行包含 $m$ 个整数，表示 $workers$ 数组中的元素。

> $n \quad m \quad pills \quad strength$
>
> $tasks_1 \quad tasks_2 \quad \ldots \quad tasks_n$
>
> $workers_1 \quad workers_2 \quad \ldots \quad workers_m$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3 3 1 1
3 2 1
0 3 3
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
2 3 1 5
5 4
0 0 0
```

### Sample Output 2

```txt showLineNumbers=false
1
```

### Sample Input 3

```txt showLineNumbers=false
3 5 3 10
10 15 30
0 10 10 10 10
```

### Sample Output 3

```txt showLineNumbers=false
2
```

## 题目要点解析

首先思考一下这道题的简单版本：假设 $tasks$ 数组和 $works$ 数组都是有序的，并且不存在大力药丸。那我们就可以直接用 **双指针匹配** 的思路来解决：如果当前工人的力量能够完成当前任务，就让他做该任务，否则跳过这个工人。整个过程就是工人与任务 **按顺序逐一配对** 。

在重新加入大力药丸之后，我们很容易会想到继续沿用上面的双指针策略：如果一个工人可以做当前的的任务，我们就让这个工人做当前的任务；如果不可以，我们就尝试让该工人吃药，再尝试完成当前的任务。这一思路看似合理，但其实是 **错误的** ，原因在于：当工人吃药之后，他在全体工人中的相对排序也随之改变。既然实力变强，他理论上就应该去承担更高难度的任务，而不再适合停留在原本的任务位置。

为了解决这个问题，我们可以尝试一个更合理的贪心：当一个工人能够胜任多个任务时，让他去完成 **他能力范围内最困难的任务** 。这是因为困难的任务可供选择的工人本来就更少，因此应当优先分配。可以轻易证明这个策略比按顺序逐一配对的思路更优。这就是所谓的[解锁任务](https://xingguang641.com/posts/acm/acm-type/heap-problems/greedy-algorithm/#田忌赛马贪心问题)的思路：对于每个工人，我们把所有他能做的任务加入一个任务集合，并优先分配其中最难的任务。

据此我们又可以尝试如下策略：如果当前工人完全做不了任务，那就让他吃药，再尝试解锁任务；如果仍无法完成，则撤销药丸并继续尝试下一个工人。不过这条看似严谨的贪心策略依然是 **错误的**：如果工人的能力数组为 $[2,3,4]$ ，任务的难度数组为 $[3,8,9]$ ，药丸只有一个并且药效为 `+5` 点能力值。那么我们直接给第一个工人吃药就只能做一个任务，而给第三个工人吃药则可以做两个任务。也就是说，我们无法确定哪个工人一定得吃药。

但如果我们事先就知道要完成的任务数量 $ans$ ，情况就会立刻变得明确。根据自然智慧，我们应当直接选择难度最低的 $ans$ 个任务和能力最大的 $ans$ 个工人。由于我们一定要完成 $ans$ 个任务，也就是每个被选中的工人都必须完成一个任务。因此在某个工人不吃药就无任务可做的情况下，我们就必须让他吃药。这样一来，我们就解决了正向思路中 “究竟该不该给某个工人吃药” 这一难以判断的问题。

这种判定逻辑具有天然的 **单调性**：要求的任务数量越多，达成目标的难度就越高；反之，任务数量越少，达成目标的难度就越低。基于这一单调性，我们可以对完成任务的数量进行二分搜索。在每一轮判定中，我们只需要验证在给定的药丸限制下，力量最大的 $T$ 个工人能否处理难度最低的 $T$ 个任务。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

---

# 参考文献列表

1. [【OI WiKi】二分查找相关知识](https://oi-wiki.org/basic/binary/)

2. [【Luogu 博客】二分算法讲解](https://www.luogu.com.cn/article/gp2mquii)