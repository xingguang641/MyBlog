---
title: 【ACM 算法题单】滑动窗口相关问题
published: 2026-03-22
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 普通滑动窗口模型

滑动窗口是解决数组或字符串中 **子区间优化** 问题的一种高效技巧。它的核心在于通过维护两个指针（左边界 $l$ 和右边界 $r$ ），动态地调整一个窗口的范围，从而避免重复计算。相比于暴力枚举所有子区间的 $O(n^2)$ 复杂度，滑动窗口通常能将算法优化至线性时间 $O(n)$ 。

该模型通常适用于具有 **单调性** 的问题。当我们向右移动右指针 $r$ 以增加新元素时，窗口内的某些属性（如元素之和、字符频率等）会随之单向变化。一旦窗口内的状态触发了特定的边界条件（例如总和超过了目标值 $k$ ），我们便开始移动左指针 $l$ 进行 “收缩” ，直到窗口重新满足约束。这种 “一进一出” 的动态平衡，本质上是在数组空间内进行的一次高效扫描。

## 最长休息间隔

[题目链接](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-i/description/)

### Problem Statement

一个公司有 $n$ 个会议，第 $i$ 个会议的开始时间为 `startTime[i]` ，结束时间为 `endTime[i]` 。所有的会议都在一天内进行，该天的总时长为 `eventTime` 。

你可以通过移动会议来重新安排日程，但必须遵守以下规则：
1. 会议的 **持续时间**（ `endTime[i] - startTime[i]` ）保持不变。
2. 会议之间的 **相对顺序** 必须保持不变。
3. 你最多可以移动 **k** 个会议。
4. 移动后，任何两个会议之间不能有重叠，且所有会议必须在 $[0, \text{eventTime}]$ 范围内。

你的目标是寻找一种移动方案，使得日程中出现一段 **最长** 的连续空余时间。返回这段空余时间的最大长度。

### Constraints

- $1 \leq n \leq 10^5$
- $k \leq n$
- $1 \leq \text{eventTime} \leq 10^9$
- $0 \leq startTime[i] < endTime[i] \leq \text{eventTime}$
- 会议按 `startTime` 升序排列，且不重叠。

### Input

输入包含三行：

- 第一行包含两个整数 $n$ 和 $k$ 。
- 第二行包含一个整数 `eventTime` 。
- 第三行包含 $n$ 个整数，表示每个会议的开始时间 `startTime` 。
- 第四行包含 $n$ 个整数，表示每个会议的结束时间 `endTime` 。

> $n \quad k$
> 
> $eventTime$
> 
> $startTime_0 \quad startTime_1 \quad \dots \quad startTime_{n-1}$
> 
> $endTime_0 \quad endTime_1 \quad \dots \quad endTime_{n-1}$

### Output

输出一个整数，表示重新安排后能获得的最大连续空余时间长度。

### Sample Input 1

```txt showLineNumbers=false
3 1
5
0 1 3
1 2 5
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
5 2
10
0 2 3 5 7
1 3 4 6 8
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析

这道题的核心在于 **视角转换** 。与其纠结于会议具体的起始与结束时间，不如将注意力转向会议之间的 “空隙” 。在 $n$ 个会议的序列中，天然存在着 $n+1$ 个间隔（包括首尾与边界的距离）。当我们拥有 $k$ 次移动会议的机会时，逻辑上等同于我们可以 “撤走” 夹在某些间隔中间的 $k$ 个会议，从而将连续的 **k + 1 个间隔** 强行汇聚成一段完整的空余时间。

在具体实现上，这便转化为一个标准的 **固定长度滑动窗口** 问题。我们预先提取出所有 $n+1$ 个间隔的长度并存入数组，随后利用大小为 $k+1$ 的窗口在数组上滑动。这种“反向维护”间隙而非正向维护会议的思路，极大地简化了题目中 “不改变相对顺序” 和 “不改变持续时间” 的复杂约束。

这种解题思维在处理区间类问题时非常高频且实用。它提醒我们：当直接操作实体对象（如会议）显得繁琐时，观察实体之间的 **相对距离** 或 **补集空间** 往往能发现更简单的线性规律。只需一次 $O(n)$ 的线性扫描，即可在各种可能的合并方案中锁定那个最大的空余总和。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int n, k, eventTime;

int main() {
    cin >> n >> k;
    cin >> eventTime;

    vector<int> startTime(n), endTime(n);
    for (int i = 0; i < n; i++) cin >> startTime[i];
    for (int i = 0; i < n; i++) cin >> endTime[i];

    vector<int> nums;
    for (int i = 0; i < (int) startTime.size(); i++){
        if (i == 0) nums.push_back(startTime[0] - 0);
        else nums.push_back(startTime[i] - endTime[i - 1]);
    }
    nums.push_back(eventTime - endTime[(int) endTime.size() - 1]);

    ll ans = 0, curSum = 0;
    if (k > (int) nums.size()) {
        for (int i = 0; i < (int) nums.size(); i++){
            ans += nums[i];
        }
        cout << ans << endl;
    } else {
        for (int i = 0; i < k; i++){
            curSum += nums[i];
        }
        for (int i = k; i < (int) nums.size(); i++){
            curSum += nums[i];
            ans = max(ans, curSum);
            curSum -= nums[i - k];
        }
        cout << ans << endl;
    }
}
```

## 串联所有的单词

[题目链接](https://leetcode.cn/problems/substring-with-concatenation-of-all-words/)



## 题目要点解析



## 使二进制字符串交替的最少反转

[题目链接](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/)



## 题目要点解析



## 环池塘人数统计

[题目链接](https://atcoder.jp/contests/abc429/tasks/abc429_d)



## 题目要点解析



---

# 种类滑动窗口问题

种类滑动窗口是一种通过 **人为施加约束** 来构造单调性的精妙技巧。标准的滑动窗口通常要求窗口内的总长度或总和满足某种单调性，但在处理诸如 “计算包含恰好 $k$ 种字符的最长子串” 这类问题时，窗口内字符种类的数量本身并不直接随窗口右移而线性增长，这使得简单的双指针难以直接奏效。为了破解这一困局，我们通常采取 **枚举字符种类数** 的策略，即将问题拆解为 “当窗口内恰好包含 $i$ 种字符时（$i$ 取值从 $1$ 到字符集大小 $\Sigma$ ）的最佳答案” 。

这种方法的核心在于利用了字符集大小（ $\Sigma$ ）通常极小的特性。以处理仅包含小写字母的字符串为例，$\Sigma$ 仅为 $26$ 。我们通过一个外层循环固定当前的种类数限制 $target$，随后在内层启动标准双指针：右指针不断向右扩展并维护一个哈希表或频率数组，一旦当前窗口内的不同字符数超过了 $target$ ，左指针便开始收缩。这种 “强行制造单调性” 的做法将原本复杂的组合搜索转化为了 $\Sigma$ 次线性的窗口扫描。虽然从形式上看复杂度增加了 $\Sigma$ 倍，但在 $O(\Sigma \cdot N)$ 的量级下，相比于暴力枚举或复杂的动态规划，它在处理长字符串题目时展现出了极高的运行效率和代码简洁度。

## 最长的平衡子串

[题目链接](https://leetcode.cn/problems/longest-balanced-substring-i/description/)



## 题目要点解析

两种做法：种类滑窗和灵神的 On 解法

---

# 分组滑动窗口问题

分组滑动窗口是一种通过 “数据解耦” 来简化复杂约束的策略。在许多数组或字符串题目中，题目要求我们处理某种特定元素（如数字 $x$ 或字符 $c$ ）的连续段性质，且数组本身可能存在修改操作或极其复杂的多元素交替。此时，若直接在原数组上维护窗口，往往会受到其他无关元素的干扰，导致逻辑冗余。

该方法的核心思想是：**按值归类，化繁为简** 。我们预先通过哈希表或动态数组（如 `vector<int> pos[Σ]` ），将每种元素出现的所有 **下标** 分别提取出来。这样，原本杂乱无章的数组就被拆解成了若干个单调递增的下标序列。在这些独立序列上进行滑动窗口，本质上是在研究 “该元素第 $i$ 次出现与第 $j$ 次出现之间遮蔽了多少其他元素” ，从而能极速计算出该特定元素在满足某种 “跨度” 或 “间隙” 约束下的最长连续段。

这种模型在 **带修题目** 中表现尤为出色。由于每种元素的下标序列是相对独立的，当发生位置修改（如将 $nums[i]$ 从 $x$ 改为 $y$ ）时，我们只需要在 $pos[x]$ 和 $pos[y]$ 这两个特定的组内进行 $O(\log N)$ 的有序维护（如平衡树或 `std::set` ），而不需要重构整个全局窗口。这种 “局部化” 的思维方式，将全局的混沌状态转化为了局部有序的窗口移动，是处理高频变动下区间最值问题的利器。

## 最长等值子数组

[题目链接](https://leetcode.cn/problems/find-the-longest-equal-subarray/description/)



## 题目要点解析


