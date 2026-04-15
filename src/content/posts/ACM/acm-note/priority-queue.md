---
title: 【ACM 算法随笔】优先队列的应用
published: 2026-02-13
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 最优状态维护问题

在许多算法问题中，我们往往需要在大量候选状态中 **不断选出最优的一部分** 。例如，在所有可能的结果中找到最大的若干个值，或者在搜索过程中始终保留当前最有希望的若干个状态。这类问题的共同特点是：候选状态数量可能非常多，但我们真正关心的只有 **前 K 个最优结果** 。因此，与其完整枚举所有结果再排序，不如在计算过程中 **动态维护前 K 个最优状态** ，这就是常见的 **Top-K 查询** 问题。

从算法角度看，Top-K 问题的核心在于如何在状态不断产生的过程中，始终快速获得当前最优的若干个候选。常见的实现方式包括使用 **优先队列** 来维护候选集合，或结合 **搜索与剪枝** 的思想，只扩展最有潜力的状态。这种方法可以避免对所有可能结果进行完整枚举，从而显著降低时间复杂度。

在实际题目中，Top-K 维护常常与 **排序、堆结构、搜索、以及状态扩展** 等技巧结合。例如，当每个状态可以生成新的候选状态时，我们可以始终从优先队列中取出当前最优的状态进行扩展，并把新产生的状态重新加入队列中，从而逐步得到前 $K$ 个结果。

### 有序状态空间搜索

在最优状态维护中，**多路归并** 是一种极其高效的搜索策略。当问题的状态空间可以划分为多个内部有序的集合时，我们无需对所有元素进行排序，而只需利用一个小根堆来动态管理各个集合的边界。以 “合并 $m$ 个已排序序列” 为例，初始时将各序列的首元素入堆，每次弹出堆顶的最小值并立即补充该序列的后续元素。这种机制将堆的大小严格控制在 $O(m)$ ，从而以 $O(K \log m)$ 的复杂度按序提取出全局前 $K$ 个最优解。

这种逻辑的核心在于将组合问题转化为 **有序状态的动态扩展** 。在处理 “两序列之和的第 $K$ 小值” 时，我们可以固定序列 $a$ 中的每个元素 $a_i$ ，将其与有序序列 $b$ 的结合视为 $n$ 条隐含的有序路径。通过优先队列在这些路径间进行跳转，算法能够根据当前的取值情况动态决定下一步的搜索方向，从而避免了无效的枚举。这种将 **局部有序性转化为搜索边界控制** 的技巧，是解决复杂堆结构问题及大规模有序数据检索的关键手段。

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

- 第一行包含两个整数 $N$ 和 $k$ 。其中 $N$ 表示数组的长度，$k$ 的含义已在题目中给出。
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

解决这道题的直觉点在于，子序列的组合数量是 $2^n$ 级别的，直接搜索必然导致复杂度爆炸。因此，问题的突破口在于将 “求前 $k$ 个最大和” 转化为 **求前 k - 1 个最小损失**。我们首先锁定全局最大和 $maxSum$ ，即数组中所有正数之和。此时，任何其他子序列都可以看作是从这个满选状态中通过 “反向操作” 得到的：要么是丢弃了一个原本选中的正数 $x$ ，要么是引入了一个原本没选的负数 $y$ 。这种对称性说明，无论原数正负，它们对总和造成的破坏程度完全取决于其 **绝对值的大小** 。

通过将原数组中所有元素取 **绝对值** 并进行 **升序排序** ，我们建立了一个单调的 “损失候选池” 。此时，原问题的 “第 $k$ 大子序列和” ，就等价于 $maxSum$ 减去绝对值数组中第 $k-1$ 小的子序列和。排序操作为我们提供了贪心的基础，使得我们可以利用 **最小堆** 在 $O(k \log k)$ 的时间内精准提取出前 $k-1$ 个最小损失值，而无需盲目遍历所有组合。

在堆的维护过程中，我们采用了一种 **包含与替换** 的双路径转移策略。每当从堆顶弹出当前的最小损失 `loss` 及其索引 `idx` 时，我们通过两种方式生成后续状态：一是保留当前组合并包含下一个更重的项，即 `loss + nums[idx + 1]` ；二是撤销当前的末尾选择并替换为下一个更重的项，即 `loss - nums[idx] + nums[idx + 1]` 。这种决策机制实质上是在按代值排序的状态树上进行 **广度优先搜索** 。由于我们总是优先探索增量最小的分支，最终，第 $k$ 大的和即为全局最大和减去堆中产出的第 $k-1$ 个最小损失。

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

有两个长度都是 $N$ 的正整数序列 $A$ 和 $B$ ，在 $A$ 和 $B$ 中各取一个数相加可以得到 $N^2$ 个和，求这 $N^2$ 个和中 **最小的 k 个** 值。

请注意：本题要求按 **从小到大** 的顺序输出前 $k$ 个最小的和。

### Constraints

- $n == A.length == B.length$
- $1 \leq n \leq 10^5$
- $1 \leq A[i], B[i] \leq 10^9$
- $1 \leq k \leq n$
- 序列 $A$ 和 $B$ 均已按 **升序** 排列。

### Input

输入包含三行：

- 第一行包含一个整数 $N$（本题中 $k$ 等于 $N$）。
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

这道题目的核心在于如何从 $N^2$ 个可能的加法组合中，高效地筛选出最小的 $N$ 个值。由于给定的两个序列 $A$ 和 $B$ 均已按 **升序排列** ，我们可以将这个庞大的组合空间看作是 $N$ 条相互独立的 **有序链表** 。具体来说，我们可以固定序列 $A$ 中的每一个元素 $a_i$ ，将其与序列 $B$ 中的所有元素相加，得到序列 $\{a_i + b_0, a_i + b_1, \dots, a_i + b_{N-1}\}$ 。由于 $B$ 是有序的，这 $N$ 条链表每一条内部也必然是单调递增的。

为了在不遍历整个 $N^2$ 空间的前提下获得全局最优解，我们利用 **最小堆** 来维护这 $N$ 条链表当前的边界。初始时，我们将每一条链表的第一个元素（即 $a_i + b_0$ ）连同其在 $A$ 和 $B$ 中的索引信息全部推入堆中。此时，堆顶元素即为全场最小的初始和。随后，我们进行 $N$ 次提取操作：每当从堆顶弹出当前的最小值时，立即通过索引信息找到该元素所属链表的 **下一个候选者** 并将其补充进堆。

这种策略的精妙之处在于，它通过 **局部有序性** 成功锁定了搜索的边界，使得堆的大小始终维持在 $O(N)$ 。在每一次弹出最小值后，我们只需要关注那条刚刚被消耗掉一个元素的链表，而不需要去窥探其他链表深处的元素。通过这种动态扩展状态的方式，算法将原本可能达到指数级或平方级的复杂度压缩到了 $O(N \log N)$ ，从而在面对 $10^5$ 量级的数据时依然能保持极高的运行效率。

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
- 接下来的 $N$ 行，每行描述一个位置：第一个整数为该位置的模型数量 $M_i$ ，随后是 $M_i$ 个整数，表示该位置各个模型的成本。

> $N \quad K$
>
> $M_1 \quad P_{1,1} \quad P_{1,2} \quad \dots \quad P_{1,M_1}$
>
> $M_2 \quad P_{2,1} \quad P_{2,2} \quad \dots \quad P_{2,M_2}$
>
> $\dots$
>
> $M_N \quad P_{N,1} \quad P_{N,2} \quad \dots \quad P_{N,M_N}$

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

# 区间顺序调度问题

在许多区间问题中，我们需要在若干个区间之间进行调度或选择，而这些区间之间的关系并不满足传统数据结构中的 **先进先出** 或 **先进后出** 的规律。区间的处理顺序往往由 **区间端点的大小关系** 决定，而不是由插入顺序决定。这类问题通常被称为 **区间顺序调度问题** ，而解决它们最常用的数据结构就是 **优先队列** 。

优先队列与普通队列的本质区别在于：队列中元素的出队顺序并不取决于进入的时间，而是取决于某个 **优先级** 。在区间问题中，这个优先级往往由 **区间的右端点或左端点** 决定。例如，当我们按区间的左端点从小到大遍历时，当前需要处理的往往是 **右端点最小的区间** ，因为它最早结束，对后续区间的影响最大。因此，我们可以使用一个以右端点为关键字的优先队列，动态维护当前活跃的区间。

从算法结构上看，这类问题通常具有一种 **扫描线式的过程** 。我们首先按照区间的左端点排序，然后依次扫描每一个区间。当扫描到新的区间时，将其右端点加入优先队列；与此同时，不断检查优先队列的队首元素，如果某些区间已经结束（例如其右端点小于当前扫描位置），就将它们从优先队列中移除。由于优先队列总是能够在 $O(\log n)$ 时间内得到当前 **最小或最大的端点** ，因此可以高效地维护区间之间的关系。

这种结构很好地体现了优先 “队列” 的特殊含义：元素虽然被不断加入和移除，但它们的出队顺序并不依赖于进入顺序，而是由 **区间端点所决定的优先级** 决定。某些后来加入的区间，如果右端点更小，反而可能更早被处理；而一些较早加入的区间，如果右端点较大，则会在优先队列中停留更长时间。这种 “动态排序” 的行为正是优先队列在区间问题中的核心作用。

## 最大重叠区间

[题目链接](https://www.nowcoder.com/practice/1ae8d0b6bb4e4bcdbf64ec491f63fc37)

### Problem Statement

给定 $N$ 个区间，每个区间用 $[start, end]$ 表示。我们需要在坐标轴上找到一个点，使得覆盖该点的区间数量最多。请问这个 **最大的覆盖数量** 是多少？

注意：每个区间的范围是左闭右闭的，即点如果在 $start$ 或 $end$ 上，也算作被该区间覆盖。但在某些版本中，题目可能定义为左闭右开 $[start, end)$ ，请以具体输入逻辑为准。

### Constraints

- $1 \leq N \leq 10^5$
- $-10^9 \leq start \leq end \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $N$ 。
- 接下来的 $N$ 行，每行包含两个整数 $start$ 和 $end$ ，表示一个区间的起始和终止坐标。

> $N$
>
> $start_1 \quad end_1$
>
> $start_2 \quad end_2$
>
> $\dots$
>
> $start_N \quad end_N$

### Output

输出一个整数，表示坐标轴上被区间覆盖最多的点所对应的最大覆盖次数。

### Sample Input 1

```txt showLineNumbers=false
3
1 4
2 5
3 6
```

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点解析

这道题的核心目标是在给定的一组区间中，寻找坐标轴上被覆盖次数最多的点。由于坐标范围可能非常大（达到 $10^9$ ），传统的布尔数组标记法会失效，因此我们采用基于 **贪心思想的扫描线算法** 配合 **优先队列** 来高效求解。

首先，我们将所有线段按照起始端点进行 **升序排序** 。这一步的目的是为了让我们能按顺序扫描坐标轴。当我们处理到一个新线段 $[s, e]$ 时，所有起始点晚于 $s$ 的线段目前都不需要考虑，我们只需要关注那些已经开始、但尚未结束的线段。

在遍历过程中，我们使用一个 **小根堆** 来维护当前所有 “活跃” 线段的右端点。对于每一个新线段，我们先检查堆顶元素（即当前最早结束的线段）。如果堆顶的结束位置小于或等于当前线段的起点 $s$ ，说明这两条线段互不重叠，我们便将其从堆中弹出。随后，将当前线段的右端点 $e$ 压入堆中。此时，**堆的大小** 恰好代表了覆盖当前起点 $s$ 的活跃线段数量。最后，我们只需在遍历过程中不断更新堆规模的最大值即可得到答案。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAX = 1e5 + 100; 
pair<int, int> a[MAX];

int main() {
    int N; cin >> N;
    for (int i = 0; i < N; i++) {
        cin >> a[i].first >> a[i].second;
    }

    sort(a, a + N);

    priority_queue<int, vector<int>, greater<int>> pq;
    int ans = 0;
    for (int i = 0; i < N; i++){
        int s = a[i].first;
        int e = a[i].second;
        
        while (!pq.empty() && pq.top() <= s) { 
            pq.pop();
        }
        
        pq.push(e);
        ans = max(ans, (int)pq.size());
    }
    
    cout << ans << endl;
}
```

除了前面提到的堆做法，**离散化配合差分数组** 是处理区间问题的另一种核心思路。既然坐标范围高达 $10^9$ 但线段数量 $N$ 只有 $10^5$ ，那么在坐标轴上绝大部分位置的覆盖次数其实是保持不变的。真正会让覆盖次数发生变化的，只有那 $2N$ 个端点。我们首先将所有起止坐标收集起来，进行排序并去重，这就完成了一次 “空间压缩” ，把稀疏的大坐标映射到了连续的小序号上。

在这些压缩后的序号上，我们应用 **差分思想**：对于每个原始区间 $[s, e]$ ，我们在它对应的起点序号上记一个 `+1` ，在终点序号的 **后一个位置**（即 $e+1$ 对应的序号）执行 `-1` 。因为这道题认为端点重合也算重叠，所以在坐标 $e$ 这个位置，减法还不能生效。最后，我们只需要从头到尾扫一遍这些序号，把这些 `+1` 和 `-1` 累加起来求前缀和，过程中出现的那个最大值，就是我们要找的最高重合次数。

这种做法的时间复杂度同样是 $O(N \log N)$ ，主要耗时在排序和去重上。它的优势在于逻辑非常固定，一旦完成了坐标映射，后续的加减操作和前缀和扫描都是线性的，非常适合处理静态的区间统计问题。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAX = 1e5 + 100;
pair<int, int> a[MAX];
int diff[MAX * 2];

int main() {
    int N; cin >> N;
    vector<int> points;
    for (int i = 0; i < N; i++) {
        cin >> a[i].first >> a[i].second;
        points.push_back(a[i].first);
        points.push_back(a[i].second + 1);
    }

    sort(points.begin(), points.end());
    points.erase(unique(points.begin(), points.end()), points.end());

    auto get_id = [&](int x) {
        return lower_bound(points.begin(), points.end(), x) - points.begin();
    };

    for (int i = 0; i < N; i++) {
        diff[get_id(a[i].first)]++;
        diff[get_id(a[i].second + 1)]--;
    }

    int ans = 0; int current_coverage = 0;
    for (int i = 0; i < points.size(); i++) {
        current_coverage += diff[i];
        ans = max(ans, current_coverage);
    }

    cout << ans << endl;
}
```

---

# 数据流中位数问题

在许多在线算法问题中，数据会不断加入，我们需要在 **每次插入后快速得到当前序列的中位数** 。如果每次都重新排序整个数组，时间复杂度会达到 $O(n \log n)$ ，在数据规模较大或需要实时处理的场景中显然不可行。因此，一个更高效的思路是 **在数据插入的过程中动态维护序列的结构** 。

中位数的一个重要性质是：当数组按大小排序后，可以把它划分为 **较小的一半** 和 **较大的一半** 。如果数据个数为奇数，中位数就是中间那个元素；如果为偶数，则通常取左右中位数之一或它们的平均值。换句话说，中位数实际上就是 **左半部分的最大值** 或 **右半部分的最小值** 。利用这一性质，我们可以将数据分成两个集合，并分别维护它们的边界元素。

具体实现时，可以使用两个优先队列来维护这两个集合：用 **最大堆** 保存较小的一半数据，使得堆顶元素始终是左半部分的最大值；用 **最小堆** 保存较大的一半数据，使得堆顶元素始终是右半部分的最小值。每当有新数据加入时，根据大小关系将其放入对应的堆中，并通过适当的调整保证两个堆的规模始终保持平衡（大小差不超过 $1$ ）。这样一来，中位数就始终暴露在堆顶位置，可以在 $O(1)$ 时间内获得，而插入操作的复杂度为 $O(\log n)$ 。

这种方法的本质，其实是利用优先队列对数据进行 **分组维护，并暴露关键的边界元素** 。通过最大堆与最小堆的配合，可以在数据不断加入的过程中始终保持序列被划分为两部分，从而避免频繁地重新排序全部数据。由于插入元素只需要进行一次堆操作，因此时间复杂度为 $O(\log n)$ ，而查询中位数只需读取堆顶元素即可，复杂度为 $O(1)$ 。这种通过堆结构 “动态维护序列关键位置” 的思想，在许多在线算法与数据流问题中都非常常见。

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
> $num_1 \quad num_2 \quad \dots \quad num_N$

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

在处理滑动窗口中位数问题时，最直观的挑战在于窗口的 **动态移动** 。每当窗口向右移动一位，都会涉及到一个旧元素的滑出和一个新元素的滑入。如果每次移动都重新对窗口内的所有元素进行全量排序，处理效率将无法应对大规模的数据输入。因此，我们需要一种能够 **实时维护有序性** 且能快速定位中间位置的机制，确保窗口在滑行过程中，中位数的更新始终处于受控状态。

为了高效追踪中位数，我们可以将窗口内的元素划分为两部分。使用一个 **大根堆维护前半部分** 数据，即较小的一半；使用一个 **小根堆维护后半部分** 数据，即较大的一半。这种对顶堆结构的设计精妙之处在于，它能够直接将 **中间的两个数字暴露出来** ，即左半部分的最大值与右半部分的最小值。无论窗口如何滑动，中位数永远只会在这两个集合的交界处产生，从而避免了对整个窗口进行无效的重复检索。

在算法执行过程中，核心在于一套 **动态平衡逻辑** 。每当新元素进入时，我们根据其数值决定插入方向；每当旧元素离开时，则从对应的集合中将其精准剔除。为了保证中位数指向准确，我们必须在每次操作后检查两个集合的大小关系，通过相互迁移元素来确保它们的数量差不超过一个。当窗口大小为奇数时，中位数即为左半部分的最大值，若为偶数，则由两个交界位置数值的平均值计算得出。这种双集对顶的思路，为处理动态序列统计值提供了一个通用的逻辑框架。

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

这种策略的核心逻辑在于构造一个能够容纳 **后悔药** 的反馈环。在执行过程中，我们依然维持着贪心的直觉，但每当做出一个选择，都会通过特定的数据结构监控 **撤回代价** 与新决策的潜在收益。当面临约束冲突或更优路径时，算法能够通过置换旧有决策来腾出资源或调整方向。这种 **先尝试、后调优** 的思路，使得算法能够在保持高效性的同时，通过不断的自我修正逐步逼近 **全局最优解** 。

从本质上看，反悔贪心是利用了 **贡献度的可维护性** 。只要题目满足操作增量可以被量化且撤回成本可控，我们就能将复杂的全局搜索简化为对 **增量值** 的动态监控。根据处理反悔方式的不同，这种策略在实现层面上通常演化为两种截然不同的模式：**直接置换模式** 与 **对冲构造模式** 。

### 直接置换模式

在 **直接置换模式** 下，算法的核心在于对已选结果集的动态维护。我们通常会预先按照某一维度对数据进行排序，从而确保决策过程具备单向的逻辑性。在遍历过程中，如果当前选项满足约束条件，算法会先行将其纳入结果集；而当约束达到上限时，算法并不会简单地拒绝后续更高质量的选项，而是通过 **优先队列** 实时捕捉已选集合中的 **最劣决策** 。

此时，堆中维护的是 **已选答案的本体** 。一旦发现当前候选项的价值高于已选集合中的最小值，算法便会执行置换逻辑：剔除掉贡献最低的旧决策，换入收益更高的新决策。这种模式在逻辑上是一种 **存量优化** ，它保证了在决策数量受限或时间窗口固定的情况下，结果集内部的质量始终处于动态上升的状态。通过这种不断的剔除与更新，算法最终能够筛选出整体贡献最大的组合。

### 对冲构造模式

与直接置换不同，**对冲构造模式** 更多用于约束关系更为复杂的场景，例如决策之间存在相邻互斥或相互抵消的逻辑。在这种模式下，我们无法通过简单地删除某一个已选元素来腾出空间，因为每一个动作都可能连锁反应式地改变周围的状态。因此，算法会向堆中注入一个经过数学构造成的 **反悔状态** 。

这个新压入堆的元素通常被称为 **虚点** ，其权值精确对应于 **撤回当前决策并开启新决策** 的净收益差额。此时，堆中维护的是所有 **潜在的增量** 。如果这个反向增量在后续被选中，其在数值上产生的效果等同于对历史决策的对冲与修正。这种模式的精妙之处在于，它将抽象的逻辑回溯转化为了简单的 **数值叠加** 。通过构造这种具有补偿性质的权值，算法在形式上依然维持着简单的贪心提取，但在底层逻辑上却实现了复杂的路径重构。

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

输入包含 $N+1$ 行：

- 第一行包含一个整数 $N$ ，表示任务的总数。
- 接下来的 $N$ 行，每行包含两个整数 $d_i$ 和 $p_i$ ，分别表示第 $i$ 项任务的截止时间和价值。

> $N$
> 
> $d_1 \quad p_1$
> 
> $d_2 \quad p_2$
> 
> $\dots$
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

在处理具有硬性时间限制的调度问题时，**截止时间** 划定了每个决策的生存边界。我们首要的操作是对任务进行 **升序排序** ，其逻辑在于：截止时间越早的任务，可被分配的时间窗位就越稀缺。一旦时间轴越过该任务的截止点，它在物理意义上便彻底失效。因此，排序的本质是建立一个全覆盖的评估序列，确保每个任务都能在凋零前，被算法纳入当前的资源分配视野。

这种基于时间的预处理，实际上是为后续的 **价值置换** 铺平了道路。在遍历过程中，排序确保了我们是按照约束由紧到松的顺序进行扩张。当当前占用的时间槽尚未达到截止上限时，算法遵循贪心策略优先填充；而当资源出现冲突，这种排序序列保证了新出现的任务拥有更宽裕的生存空间。此时，**小根堆** 维护的已选任务价值便充当了 “准入门槛” ，让高价值任务能够通过置换逻辑，挤掉那些贡献度较低的早期占位者。

从全局视野来看，排序将抽象的时间约束转化为了具体的席位竞争。通过从小到大遍历，我们实际上是在每一个关键的时间节点进行优胜劣汰。这种机制确保了算法不会因为盲目追求后期收益而浪费早期的获益可能，也不会因为死守早期的低价值任务而错失后期的重磅收益。通过这种基于时序的动态筛选，算法在确保时间合法性的前提下，通过不断的决策迭代，最终收敛于总价值最大化的全局解。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
struct Task {
    int deadline, profit;
    bool operator<(const Task& other) const {
        return deadline < other.deadline;
    }
};

int main() {
    int n; cin >> n;
    vector<Task> tasks(n);
    for (int i = 0; i < n; i++) {
        cin >> tasks[i].deadline >> tasks[i].profit;
    }

    sort(tasks.begin(), tasks.end());

    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i = 0; i < n; i++) {
        if (tasks[i].deadline > (int)pq.size()) {
            pq.push(tasks[i].profit);
        } 
        else if (!pq.empty() && tasks[i].profit > pq.top()) {
            pq.pop();
            pq.push(tasks[i].profit);
        }
    }

    long long total_profit = 0;
    while (!pq.empty()) {
        total_profit += pq.top();
        pq.pop();
    }

    cout << total_profit << endl;
}
```

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
- 第二行包含 $N$ 个整数 $c_1, c_2, \dots, c_N$ ，分别表示第 $i$ 天的股票价格。

> $N$
> 
> $c_1 \quad c_2 \quad \dots \quad c_N$

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

1. [《寻找第 k 优解的几种方法》阅读笔记](https://www.luogu.com/article/7mr8ihp7)

2. [浅谈与求前 k 优方案有关的问题](https://www.luogu.com.cn/article/rcmx938z)

3. [【wshcl】反悔贪心相关题目收集](https://www.cnblogs.com/wshcl/p/18712932)