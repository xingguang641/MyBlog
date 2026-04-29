---
title: 【ACM 算法随笔】优先队列的应用
published: 2026-02-13
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 最优状态维护问题

许多算法题目的目标是要求 **输出前 K 个最优结果** ，这类问题的核心挑战在于，候选状态的总数可能呈指数级增长，但真正具备参考价值的仅为指定的 $K$ 个结果。因此，与其在生成全部结果后再进行全局排序，不如通过 **优先队列** 实时更新并维护当前最优的候选。这种策略有效地将计算聚集在最有潜力的状态上，从根本上避免了无效的枚举，从而显著降低了算法的时间复杂度。

在实际应用中，最优状态维护问题通常与 **状态扩展** 和 **搜索剪枝** 深度结合。在这种寻优模式下，堆顶始终维持着当前全局最优的状态；当该状态被取出后，算法通过精心设计的变换逻辑生成其后续候选状态并重新入堆。通过合理的算法设计，我们能够确保从最优状态扩展出的新状态依然具有较强的竞争力，从而在 **优中选优** 的过程中自然实现剪枝。通过这种方式，算法能够逐步提取前 $K$ 个结果。

## 数组第 K 大和

[题目链接](https://leetcode.cn/problems/find-the-k-sum-of-an-array/description)

### Problem Statement

给你一个下标从 $0$ 开始、长度为 $n$ 的整数数组 `nums` ，和两个整数 `k` 。你需要从数组中找出一个子序列，使得该子序列内元素的 **和** 为所有子序列和中 **第 k 大** 的一个。

返回该数组的 **第 k 大子序列和** 。

注意：子序列是指从数组中删除一些元素（也可以不删除）后剩余元素组成的数组。空子序列的和定义为 $0$ 。

### Constraints

- $n == nums.length$
- $1 \leq n \leq 10^5$
- $-10^9 \leq nums[i] \leq 10^9$
- $1 \leq k \leq \min(2000, 2^n)$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad k$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示第 $k$ 大的子序列和。

### Sample Input 1

```txt showLineNumbers=false
3 2
2 4 -2
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
3 5
1 -2 3
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析

我们首先考虑该问题的 **简化版本**：给定 $n$ 个非递减的非负整数序列 $a_0, a_1, \ldots, a_{n-1}$ ，找出其中第 $k$ 个最小的子序列和。在这个条件下，最小的和显然是空序列产生的 $0$（即 $k=1$ 时的答案）。对于 $k > 1$ 的情况，核心在于如何有序地产出后续所有的和。我们引入状态 $(t, i)$ 表示一个以 $a_i$ 为最后一个元素且总和为 $t$ 的子序列，并利用 **最小堆** 来动态维护这些状态。初始化时，堆中仅包含序列中最小的元素 $(a_0, 0)$ 。

为了确保探索过程有序且完备，每当我们从堆顶取出当前的最小状态 $(t, i)$ 时，需要执行两项关键的转移操作。第一是将 $a_{i+1}$ **拼接** 到当前子序列之后，生成新状态 $(t + a_{i+1}, i + 1)$ ，代表子序列长度的增加。第二是将当前子序列中的末尾元素 $a_i$ **替换** 为更大的 $a_{i+1}$，生成状态 $(t - a_i + a_{i+1}, i + 1)$ 。这种包含与替换的策略保证了每一次从堆顶弹出的元素都是当前全局尚未被发现的最小值。

$$
State_{push1} = (t + a_{i+1}, i + 1)
$$

$$
State_{push2} = (t - a_i + a_{i+1}, i + 1)
$$

通过这种方式，当我们第 $k-1$ 次从堆中取出元素时，所得到的 $t$ 就是序列中第 $k$ 个最小的子序列和。这种构造逻辑实际上是在一颗隐形的状态树上进行层序遍历，它利用了数组原本的有序性，避免了对 $2^n$ 空间的盲目搜索。

回到原问题中包含负数的情况，我们可以发现一个重要的性质：原序列中所有正数之和 $maxSum$ 构成了该数组能够达到的全局最大子序列和。任何其他子序列相对于这个最大值的降低，实质上都是由于两种行为导致的：要么是放弃了某个原本选中的正数 $x$ ，损失了 $|x|$ ；要么是加入了一个原本未选的负数 $y$ ，损失了 $|y|$ 。

$$
maxSum = \sum_{nums[i] > 0} nums[i]
$$

基于这一观察，无论原数正负，它们对总和造成的破坏程度都整齐划一地由其 **绝对值** 来衡量。我们只需要将原序列的所有元素统一取绝对值并从小到大排序，就将其完美转化为了上述的简化模型。此时，原问题的第 $k$ 大子序列和就等价于用全局最大和 $maxSum$ 减去绝对值序列中的第 $k-1$ 小子序列和。这种巧妙的对称性转化，避开了对正负数排列组合的复杂讨论，利用最小堆在 $O(k \log k)$ 的复杂度内精准锁定了目标结果。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int n, k; ll sum = 0;

int main() {
    cin >> n >> k;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
        if (nums[i] > 0) sum += nums[i];
        else nums[i] = -nums[i];
    }

    sort(nums.begin(), nums.end());
    if (k == 1) {
        cout << sum << endl;
        return 0;
    }

    priority_queue<
        pair<ll, int>,
        vector<pair<ll, int>>,
        greater<pair<ll, int>>
    > pq;
    pq.push({(ll)nums[0], 0});
    ll min_loss = 0;
    for (int i = 0; i < k - 1; i++) {
        auto [loss, idx] = pq.top(); pq.pop();
        if (idx + 1 < n) {
            pq.push({loss + nums[idx + 1], idx + 1});
            pq.push({loss + nums[idx + 1] - nums[idx], idx + 1});
        }
        min_loss = loss;
    }

    cout << sum - min_loss << endl;
}
```

## 序列合并问题

[题目连接](https://www.luogu.com.cn/problem/P1631)

### Problem Statement

有两个长度都是 $N$ 的正整数序列 $A$ 和 $B$ ，在 $A$ 和 $B$ 中各取一个数相加可以得到 $N^2$ 个和，求这 $N^2$ 个和中 **最小的 N 个** 值。

请注意：本题要求按 **从小到大** 的顺序输出前 $N$ 个最小的和。

### Constraints

- $n == A.length == B.length$
- $1 \leq n \leq 10^5$
- $1 \leq A[i], B[i] \leq 10^9$
- $1 \leq k \leq n$
- 序列 $A$ 和 $B$ 均已按 **升序** 排列

### Input

输入包含三行：

- 第一行包含一个整数 $N$ 。
- 第二行包含 $N$ 个整数，表示序列 $A$ 。
- 第三行包含 $N$ 个整数，表示序列 $B$ 。

> $N$
>
> $A_1 \quad A_2 \quad \ldots \quad A_N$
>
> $B_1 \quad B_2 \quad \ldots \quad B_N$

### Output

输出包含一行，包含 $N$ 个整数，两两之间用空格隔开，表示最小的 $N$ 个和。

### Sample Input 1

```txt showLineNumbers=false
3
1 2 3
1 2 3
```

### Sample Output 1

```txt showLineNumbers=false
2 3 3
```

## 题目要点解析

这道题目的核心在于如何从 $N^2$ 个可能的结果中，高效地筛选出最小的 $N$ 个值。由于给定的两个序列 $A$ 和 $B$ 均已按 **升序排列** ，我们可以将这个庞大的组合空间看作是 $N$ 条相互独立的 **有序链表** 。具体来说，我们可以固定序列 $A$ 中的每一个元素 $a_i$ ，将其与序列 $B$ 中的所有元素相加，得到序列 $\{a_i + b_0, a_i + b_1, \ldots, a_i + b_{N-1}\}$ 。由于 $B$ 是有序的，这 $N$ 条链表每一条内部也必然是单调递增的。

为了在不遍历整个 $N^2$ 空间的前提下获得全局最优解，我们可以利用 **最小堆** 来维护这 $N$ 条链表当前的边界。初始时，我们将每一条链表的第一个元素（即 $a_i + b_0$ ）连同其在 $A$ 和 $B$ 中的索引信息全部推入堆中。此时，堆顶元素即为全场最小的初始和。随后，我们进行 $N$ 次提取操作：每当从堆顶弹出当前的最小值时，立即通过索引信息找到该元素所属链表的 **下一个候选者** 并将其补充进堆。

这种策略的精妙之处在于，它通过 **局部有序性** 成功锁定了搜索的边界，使得堆的大小始终维持在 $O(N)$ 。在每一次弹出最小值后，我们只需要关注那条刚刚被消耗掉一个元素的链表，而不需要去查找其他链表深处的元素。

```cpp frame="code" title="main.cpp"
# include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAX = 1e5 + 100;
int a[MAX], b[MAX];

int main(){
    int N; cin >> N;
    for (int i = 0; i < N; i++) cin >> a[i];
    for (int i = 0; i < N; i++) cin >> b[i];

    priority_queue<
        pair<int, pair<int, int>>, 
        vector<pair<int, pair<int, int>>>, 
        greater<pair<int, pair<int, int>>>
    > pq;
    for (int i = 0; i < N; i++){
        pq.push({a[i] + b[0], {i, 0}});
    }
    for (int i = 0; i < N; i++){
        auto [cur, idx] = pq.top(); pq.pop();
        cout << cur << " ";
        if (idx.second + 1 < N)
            pq.push({a[idx.first] + b[idx.second + 1],
            {idx.first, idx.second + 1}});
    } cout << endl;
}
```

## 机器人奶牛群

[题目链接](https://www.luogu.com.cn/problem/P2541)

### Problem Statement

Bessie 需要建造 $K$ 头不同的机器人奶牛。每头机器人奶牛有 $N$ 个位置需要安装微控制器。对于每个位置 $i$ ，都有 $M_i$ 个备选的微控制器模型，每个模型都有对应的成本。

你需要从每个位置的备选模型中各选出一个，组成一头完整的机器人。由于每头机器人的微控制器组合必须是唯一的，你的目标是选出总成本最小的 $K$ 种不同组合，并计算这 **K 套方案的总成本之和** 。

### Constraints

- $1 \leq N \leq 10^5$
- $1 \leq K \leq 10^5$
- $1 \leq M_i \leq 10$
- $1 \leq P_{i,j} \leq 10^8$
- 保证方案总数不少于 $K$

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $K$ 。
- 接下来的 $N$ 行，第一个整数为该位置的模型数量 $M_i$ ，随后 $M_i$ 个整数表示该位置各个模型的成本。

> $N \quad K$
>
> $M_1 \quad P_{1,1} \quad P_{1,2} \quad \ldots \quad P_{1,M_1}$
>
> $M_2 \quad P_{2,1} \quad P_{2,2} \quad \ldots \quad P_{2,M_2}$
>
> $\ldots$
>
> $M_N \quad P_{N,1} \quad P_{N,2} \quad \ldots \quad P_{N,M_N}$

### Output

输出一个整数，表示建造 $K$ 头不同机器人奶牛的最小总成本之和。

### Sample Input 1

```txt showLineNumbers=false
2 3
2 1 10
2 5 3
```

### Sample Output 1

```txt showLineNumbers=false
15
```

## 题目要点解析

状态转移设计，如何设计有限的状态转移得到所有状态是这类问题的难点。

---

# 数据流中位数问题

数据流中位数问题的核心挑战在于数据以连续流的形式输入，并且要求系统在 **每次插入操作后定位序列的中心位置** 。如果采用全局排序的方式，计算成本会随着数据量的累积而迅速上升，难以满足实时处理的需求。中位数的数学性质在于它将有序序列划分为较小和较大的两个等分区间，其数值由左侧区间的最大值或右侧区间的最小值导出。因此，问题的关键不在于维护全局的有序性，而在于如何高效地动态维护这两个半区的边界。

实现这一目标的标准方案是构建双堆结构：利用一个 **最大堆** 管理较小的一半数据，确保堆顶始终锁定左半部分的边界最大值；同时利用一个 **最小堆** 管理较大的一半数据，使堆顶始终锁定右半部分的边界最小值。每当新数据进入系统，程序会根据数值大小将其分流至对应的堆中，并实时通过跨堆移动来平衡两者的规模，确保其元素数量之差不超过 1。在这种架构下，中位数始终处于两个堆顶的覆盖范围内，从而将查询效率优化至 $O(1)$ ，维护效率保持在 $O(\log n)$ 。

这种方法的本质是利用优先队列的局部有序性，对数据进行 **分组维护并暴露关键的边界元素** 。在双堆架构中，系统不再消耗资源去处理每一个元素的绝对排名，而是将算力集中在能够决定中位数的关键节点上。这种动态维护序列关键位置的策略，彻底规避了频繁排序带来的性能瓶颈，使得处理大规模实时数据流变得轻量且高效。

## 滑动窗口中位数

[题目链接](https://leetcode.cn/problems/sliding-window-median/description/)

### Problem Statement

中位数是有序序列中间的数。如果序列的长度是偶数，中位数则是中间两个数的平均值。

给定一个长度为 $N$ 的数组 $nums$ 和一个窗口大小 $k$ ，有一个大小为 $k$ 的窗口从数组的最左侧移动到最右侧。窗口每次向右移动一位。你的目标是找出每次窗口移动后，窗口内 $k$ 个数字的中位数。

### Constraints

- $1 \leq k \leq N \leq 10^5$
- $-2^{31} \leq nums[i] \leq 2^{31} - 1$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组 $nums$ 。

> $N \quad k$
> 
> $num_1 \quad num_2 \quad \ldots \quad num_N$

### Output

输出一行浮点数（保留五位小数），每个数之间用空格隔开，表示每个窗口的中位数。

### Sample Input 1

```txt showLineNumbers=false
8 3
1 3 -1 -3 5 3 6 7
```

### Sample Output 1

```txt showLineNumbers=false
1.00000 -1.00000 -1.00000 3.00000 5.00000 6.00000
```

## 题目要点解析

滑动窗口中位数问题的核心挑战在于，如何在窗口沿着序列移动的过程中，实时且高效地求解中位数。若每次移动窗口都对内部的 $k$ 个元素进行排序，时间复杂度将达到 $O(N \cdot k \log k)$ ，在 $10^5$ 的数据规模下会导致计算成本过高。因此，解题的关键在于构建一种能够动态维护有序性的机制，支持在增删元素时以极低成本定位中间值，从而避免对整个窗口的重复操作。

为了实现这一目标，可以使用对顶堆的设计：利用 **最大堆** 维护较小的一半数据，利用 **最小堆** 维护较大的一半数据，确保中位数始终处于两个堆顶的交界处。当窗口沿着序列移动时，只需将新滑入的元素归入对应的堆，同时将滑出的元素从相应的堆中移除，并维持两个堆的规模平衡。通过这种双堆对顶策略，窗口中位数可在 $O(1)$ 时间内由堆顶元素直接计算得出，从而将单次滑动后的更新效率优化至 $O(\log k)$ ，确保算法在处理大规模动态数据流时依然高效且稳定。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
multiset<int> leftset, rightset;

void leftToRight() {
    if (leftset.empty()) return;
    rightset.insert(*leftset.rbegin());
    leftset.erase(prev(leftset.end()));
}

void rightToleft() {
    if (rightset.empty()) return;
    leftset.insert(*rightset.begin());
    rightset.erase(rightset.begin());
}

void balance() {
    if (leftset.size() > rightset.size() + 1)
        leftToRight();
    if (rightset.size() > leftset.size())
        rightToleft();
}

int main() {
    int N, k; cin >> N >> k;
    vector<int> nums(N);
    for (int i = 0; i < N; i++) {
        cin >> nums[i];
    }

    for (int i = 0; i < N; i++) {
        if (leftset.empty() || nums[i] <= *leftset.rbegin())
            leftset.insert(nums[i]);
        else 
            rightset.insert(nums[i]);
        
        if (i >= k) {
            int out_val = nums[i - k];
            auto it = leftset.find(out_val);
            if (it != leftset.end()) 
                leftset.erase(it);
            else 
                rightset.erase(rightset.find(out_val));
        }

        balance();

        if (i >= k - 1) {
            double res;
            if (k % 2 == 1) {
                res = (double)*leftset.rbegin();
            } else {
                res = ((double)*leftset.rbegin() + *rightset.begin()) / 2.0;
            }
            cout << fixed << setprecision(1) << res << (i == N - 1 ? "" : " ");
        }
    }
    cout << endl;
}
```

---

# 反悔贪心策略问题

在传统的算法逻辑中，**贪心策略** 往往被视为一种一次性决策，即每一步都盲目追求当前状态下的局部最优。然而，许多复杂问题的全局最优解并不由局部最优简单累加而成，这就导致常规贪心容易陷入误区。**反悔贪心** 的引入，本质上是为这种僵化的决策机制注入了 **动态修正** 的能力。它不再强求每一步都绝对正确，而是允许算法先执行一次 **假贪心** ，在后续过程中根据全局利益的变化，灵活地收回并替换之前的决策。

反悔贪心的巧妙之处在于它构建了一个允许推倒重来的 **反馈回路** 。通过引入优先队列等数据结构，算法能够量化当前决策的 **反悔成本** 与后续候选方案的 **边际收益** 。当新出现的全局选择优于历史操作时，算法利用这种差值度量实现决策的 **动态回溯与替换** 。本质上，反悔贪心将局部最优转化为一种可调控的 **状态空间搜索** ，通过对决策增量的持续维护，使得算法在执行过程中能够不断自我纠错，从而在低时间复杂度下逼近 **全局最优** 。

## 工作调度问题

[题目链接](https://www.luogu.com.cn/problem/P2949)

### Problem Statement

有 $N$ 项任务，每项任务需要花费 $1$ 个单位时间来完成。对于第 $i$ 项任务，它有一个截止时间 $d_i$ 和一个完成该任务后可以获得的价值 $p_i$ 。每一时刻只能完成一项任务。

你的目标是合理安排任务的执行顺序，使得在所有截止时间之前完成的任务总价值最大。

### Constraints

- $1 \leq N \leq 10^5$
- $1 \leq d_i \leq 10^9$
- $1 \leq p_i \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ ，表示任务的总数。
- 接下来的 $N$ 行，每行包含两个整数 $d_i$ 和 $p_i$ ，分别表示第 $i$ 项任务的截止时间和价值。

> $N$
> 
> $d_1 \quad p_1$
> 
> $d_2 \quad p_2$
> 
> $\ldots$
> 
> $d_N \quad p_N$

### Output

输出一个整数，表示能够获得的最大总价值。

### Sample Input 1

```txt showLineNumbers=false
3
2 10
1 5
1 7
```

### Sample Output 1

```txt showLineNumbers=false
17
```

## 题目要点解析



## 股票收益最大化

[题目链接](https://www.luogu.com.cn/problem/CF865D)

### Problem Statement

你预测了未来 $N$ 天某只股票的价格。在第 $i$ 天，股票的价格为 $c_i$ 。

每天你可以执行以下三种操作之一：

1. **买入**：花费 $c_i$ 的代价买入一股股票。
2. **卖出**：将手中已持有的一股股票卖出，获得 $c_i$ 的收益。
3. **观望**：不进行任何买入或卖出。

假设你初始资金无限，且不限制持有股票的数量。你的目标是通过合理的操作，使得 $N$ 天后的总利润最大化。

### Constraints

- $1 \leq N \leq 3 \times 10^5$
- $1 \leq c_i \leq 10^6$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示天数。
- 第二行包含 $N$ 个整数 $c_1, c_2, \ldots, c_N$ ，分别表示第 $i$ 天的股票价格。

> $N$
> 
> $c_1 \quad c_2 \quad \ldots \quad c_N$

### Output

输出一个整数，表示能够获得的最大总利润。

### Sample Input 1

```txt showLineNumbers=false
9
10 5 4 7 9 12 6 2 10
```

### Sample Output 1

```txt showLineNumbers=false
20
```

### Sample Input 2

```txt showLineNumbers=false
20
3 1 4 1 5 9 2 6 5 3 5 8 9 7 9 3 2 3 8 4
```

### Sample Output 2

```txt showLineNumbers=false
41
```

## 题目要点解析

这是一道维护候选项的题，我们可以引入反悔状态。

---

# 参考文献列表

1. [【Luogu 博客】浅谈前 k 优方案相关问题](https://www.luogu.com.cn/article/rcmx938z)

2. [【wshcl】反悔贪心相关题目收集](https://www.cnblogs.com/wshcl/p/18712932)

3. [【Luogu 博客】反悔贪心的再理解](https://www.luogu.com.cn/article/hwrxooq5)