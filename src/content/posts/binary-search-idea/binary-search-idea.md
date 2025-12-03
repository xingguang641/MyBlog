---
title: 【ACM 算法随笔】二分查找与二分技巧
published: 2025-11-26
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 二分查找基本原理



---

# 最大值最小化相关问题收集

最大值最小化问题是二分答案法最经典、也最直观的应用之一。它的核心思想是：当答案具有明确的 “可行/不可行” 边界时，我们就可以把搜索从具体方案转移到答案空间本身。通过二分一个候选值，并检验在这个约束下能否完成任务，我们便能逐步逼近那个使得最大代价尽可能小的最优解。

这一类问题的共同特征在于，只要给定一个上限，我们往往可以用贪心或模拟的方法判断是否可行；而这个判断函数的单调性，又恰好使得二分答案成为最自然、最高效的解法。因此，无论是分割数组、安排工作日程，还是把物体尽量均匀划分到若干容器中，“最大值最小化” 都可以作为统一的分析视角，将各种题目串联到同一个框架下。

## 分割数组的最大值（画匠问题）

[题目链接](https://leetcode.cn/problems/split-array-largest-sum/description/)

### Problem Statement

给定一个非负整数数组 $nums$ 和一个整数 $k$ ，你需要将这个数组分成 $k$ 个非空的连续子数组，使得这 $k$ 个子数组各自和的最大值 **最小** 。

### Constraints

- $1 \leq nums.length \leq 1000$
- $0 \leq nums[i] \leq 10^6$
- $1 \leq k \leq min{50, nums.length}$

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
7 2 5 10 8
```

### Sample Output 1

```txt showLineNumbers=false
18
```

### Sample Input 2

```txt showLineNumbers=false
5 3
1 2 3 4 5
```

### Sample Output 2

```txt showLineNumbers=false
9
```

## 题目解析

画匠问题（Painter's Partition Problem）是最大值最小化问题中最具代表性的经典案例之一，而这类问题的标志性高效解法正是 **二分查找（Binary Search）**。之所以能够应用二分法，是基于以下转化逻辑：最大值最小化问题本质上是一个 **优化问题** ，但它巧妙地通过引入一个 **决策函数（Decision Function）**，将其转化为了一个具有 **单调性** 的 **判定问题** ，从而使二分搜索成为可能。

1. **定义判定问题**

    我们定义一个判定函数 $P(X)$，来回答以下问题：

    > **“我们能否在最大值不超过 $X$ 的限制下完成所有任务/满足所有条件？”**

2. **关键的单调性**

    如果 $P(X)$ 成立，那么对于任何 $X' > X$ 的值，$P(X')$ 也一定成立。

    *   **直观理解**：如果能在最长耗时 10 分钟的限制下完成工作，那么也能在最长耗时 11 分钟的限制下完成。

    如果 $P(X)$ 不成立，那么对于任何 $X'' < X$ 的值，$P(X'')$ 也一定不成立。

    *   **直观理解**：如果不能在最长耗时 10 分钟的限制下完成工作，那肯定不能在最长耗时 9 分钟的限制下完成。

3. **形成 "False-True" 序列**

    这就形成了一个关于 $X$ 的单调序列：

    $$\underbrace{\text{False}, \dots, \text{False}}_{\text{无法满足}}, \underbrace{\text{True}}_{\text{最优解 } X_{\text{opt}}}, \underbrace{\text{True}, \dots, \text{True}}_{\text{可以满足}}$$

由于这个判定函数的返回值是 **单调的**（从 $\text{False}$ 变为 $\text{True}$ ），因此我们就可以对答案的范围进行二分查找。

*   **搜索空间**： 二分查找不是作用在输入数据上，而是作用在**最终答案 $X$ 的可能取值范围 $[L, R]$** 上。
*   **搜索目标**： 我们的目标是找到使 $P(X)$ **首次变为 $\text{True}$** 的那个最小值 $X_{\text{opt}}$ 。

下面给出这道题的完整代码：

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

---

# 静态中位数相关问题收集

二分答案法在求中位数或第 $k$ 小值的问题中同样大放异彩。对于这些静态、离线处理的场景，我们不直接寻找答案本身，而是对答案的取值空间进行二分。每当我们二分到一个候选数 $x$ 时，只需要统计数组中有多少元素小于或等于 $x$ ，就能判断 $x$ 是否已经达到第 $k$ 小的要求。通过这样的判断，我们不断缩小搜索区间，最终锁定真实的中位数或第 $k$ 小值。

而在需要动态维护中位数的场景中，我们通常会采用 “双优先队列” 的结构来处理：用一个最大堆维护较小的一半元素，再用一个最小堆维护较大的一半元素，通过保持两边规模平衡，就能在每次插入后迅速得到当前的中位数。

## 找出第 K 小的数对距离

[题目链接](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/description/)

### Problem Statement

数对 $(a,b)$ 由整数 a 和 b 组成，其数对距离定义为 a 和 b 的绝对差值。

给你一个整数数组 $nums$ 和一个整数 $k$ ，数对由 $nums[i]$ 和 $nums[j]$ 组成且满足 $0 <= i < j < nums.length$ 。返回 **所有数对距离中** 第 $k$ 小的数对距离。

### Constraints

- $2 \leq nums.length \leq 10^4$
- $0 \leq nums[i] \leq 10^6$
- $1 \leq k \leq n * (n - 1) / 2$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ 。其中，$N$ 表示数组的长度，$k$ 的含义已在题目描述中给出
- 第二行包含 $n$ 个整数，表示数组中的元素

> $n \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3 1
1 2 1
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

## 题目解析

既然二分可以解决静态中位数问题，自然可以解决静态 k-th 问题。我们只需要将 “查找第 $k$ 小的值” 这一优化问题转化为判断原始数据集中小于等于某个值 $X$ 的元素个数是否大于或等于 $k$ 的判定问题，并对答案的值域进行二分查找即可。

根据上面的思路，我们代码可以这样写：

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

---

# 逆向求解相关问题收集

## 刀砍毒杀怪兽问题

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class051/Code07_CutOrPoison.java)

## 可以安排的最多任务数目

[题目链接](https://leetcode.cn/problems/maximum-number-of-tasks-you-can-assign/description/)

---

# 参考文献

1. [【OI WiKi】二分查找相关知识](https://oi-wiki.org/basic/binary/)

2. [【二分查找】详细图解](https://blog.csdn.net/qq_45978890/article/details/116094046)

3. [【数据结构】二分查找 (四种写法)](https://www.cnblogs.com/MarisaMagic/p/17093253.html)

4. [【C++】二分查找超详细图解（小白一看就懂！！！）](https://blog.csdn.net/weixin_45031801/article/details/137439994)

5. [【代码随想录】二分查找](https://programmercarl.com/0704.二分查找.html)

6. [二分法总结 | 万字长文带你看透二分查找](https://zhuanlan.zhihu.com/p/533408649)

7. [【算法详解】二分查找](https://blog.csdn.net/Z1tai/article/details/137512467)