---
title: 【ACM 算法题单】子数组最大累加和问题
published: 2026-02-07
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: true
---

# 单区间累加和问题

在动态规划的视角下，处理连续子数组问题需要 **严格的逻辑安排** 。由于题目要求元素在空间上必须紧密相连，动态规划的重点不在于全局搜索，而在于如何让递推过程始终受限于这种连续性。与处理子序列问题时那种相对自由的状态转移不同，连续子数组问题要求每一个状态都必须明确地归属于以当前元素为结尾的区间。这种对 **终点位置的严格限定** ，有效地将复杂的整体问题转化为对每个元素位置的单点抉择，从而消除了逻辑上的歧义，确保了整个推导过程的可靠性与准确性。

针对此类问题，动态规划具体的状态设计是将 $dp[i]$ 定义为以第 $i$ 个位置为区间终点的最优解。在算法执行到每一个节点时，核心的逻辑在于 **决策是否延续前序区间的最优积累** ，即通过分析当前节点独立构成新区间的可能性，或者将其并入现有区间所带来的数值变化，来确定当前状态的最优值。这种 **逐点推进的策略** 清晰地展现了局部最优解如何通过严格的路径约束，在不断迭代中构建出全局的最优结果。

## 子数组最大总和

[题目链接](https://leetcode.cn/problems/maximum-subarray)

### Problem Statement

给你一个整数数组 `nums` ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

子数组是数组中的一个连续部分。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $-10^4 \leq nums[i] \leq 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示数组中的各个元素。

> $n$
> 
> $nums_1, nums_2, \ldots, nums_n$

### Output

输出一个整数表示答案。

### Sample Input

```txt showLineNumbers=false
9
-2 1 -3 4 -1 2 1 -5 4
```

### Sample Output

```txt showLineNumbers=false
6
```

## 题目要点解析

处理连续子数组问题的核心在于引入 “以当前位置结尾” 这一约束，将原本发散的区间搜索转化为有序的动态规划递推。通过定义 $dp[i]$ 为以第 $i$ 个元素为终点的最大子数组和，我们将复杂的全局最优解问题简化为局部的逻辑决策，即判断是承接前序序列以累加收益，还是舍弃前序以当前元素为起点重新构建。

其核心递推关系简洁地表达为：

$$
dp[i] = \max(nums[i], dp[i-1] + nums[i])
$$

这种建模技巧的本质是用局部结尾的确定性来换取状态转移的极简性。通过一次线性扫描，我们在每一个递推步中捕获局部最优，并在遍历过程中维护全局最大值，从而在 $O(n)$ 的时间复杂度内完成对连续性约束问题的求解。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 1e5 + 100;
int a[MAXN]; ll dp[MAXN];

int main() {
    int n; cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    dp[0] = a[0]; ll ans = a[0];
    for (int i = 1; i < n; i++) {
        dp[i] = max((ll)a[i], dp[i - 1] + a[i]);
        ans = max(ans, dp[i]);
    }

    cout << ans << endl;
}
```

## 环数组最大总和

[题目链接](https://leetcode.cn/problems/maximum-sum-circular-subarray/)

### Problem Statement

给定一个长度为 `n` 的 **环形整数数组** `nums` ，请你找出该数组中具有最大和的 **非空子数组** ，并返回其最大和。

**环形数组** 意味着数组的末端将会与开头相连呈环状。形式上，`nums[i]` 的下一个元素是 `nums[(i + 1) % n]` ，而 `nums[i]` 的前一个元素是 `nums[(i - 1 + n) % n]` 。

### Constraints

- $n == nums.length$
- $1 \leq n \leq 3 \times 10^4$
- $-3 \times 10^4 \leq nums[i] \leq 3 \times 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示环形数组中的各个元素。

> $n$
> 
> $nums_1, nums_2, \ldots, nums_n$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3
1 -2 3
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
3
5 -3 5
```

### Sample Output 2

```txt showLineNumbers=false
10
```

## 题目要点解析

针对环形数组，常见的处理策略通常分为两类：一种是 **倍增数组法** ，通过构造长度为 $2n$ 的数组将环形结构展平为线性序列，并使用长度为 $n$ 的定长滑动窗口规定数组范围，从而避免决策中对同一元素的重复选择。虽然该方法直观易于实现，但其代价在于需要进行 $n$ 次完整滑动窗口的循环操作，导致总时间复杂度增加，在面对大规模数据时效率极低。另一种更为高效的策略是 **分类讨论法** ，其核心在于根据子数组是否跨越数组边界，将问题拆解为两个对偶的线性子问题。

对于 **不跨越边界** 的情况，子数组完全包含在原数组内部，其求解等价于标准的线性子数组最大累加和。通过状态转移方程 $dp_{max}[i] = \max(a[i], dp_{max}[i-1] + a[i])$ ，可以计算以每个位置结尾的最大增益。对于 **跨越边界** 的情况，最大子数组由原数组的前缀与后缀拼接而成，其逻辑等价于从总和 $TotalSum$ 中减去中间的一段连续最小子数组。因此，求解跨越边界的最大和，转化为求解线性数组的最小累加和这一对偶问题，通过 $dp_{min}[i] = \min(a[i], dp_{min}[i-1] + a[i])$ 即可同步维护。

最终的全局最优解在 $\max(dp_{max})$ 与 $TotalSum - \min(dp_{min})$ 之间产生。这种处理方式规避了显式的环形遍历，通过同步维护最大与最小状态，在 $O(n)$ 时间复杂度内实现了对全解空间的覆盖。需要注意的是，当数组元素全部为负值时，$TotalSum$ 与最小累加和相等，此时对应的补集为空集，应直接取 $\max(dp_{max})$ 作为结果。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 1e5 + 100;
int a[MAXN];
ll dp_max[MAXN], dp_min[MAXN];

int main() {
    int n; cin >> n;
    ll total_sum = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        total_sum += a[i];
    }

    dp_max[0] = dp_min[0] = a[0];
    ll max_ans = a[0];
    ll min_ans = a[0];
    for (int i = 1; i < n; i++) {
        dp_max[i] = max((ll)a[i], dp_max[i - 1] + a[i]);
        max_ans = max(max_ans, dp_max[i]);

        dp_min[i] = min((ll)a[i], dp_min[i - 1] + a[i]);
        min_ans = min(min_ans, dp_min[i]);
    }

    if (max_ans < 0) {
        cout << max_ans << endl;
    } else {
        cout << max(max_ans, total_sum - min_ans) << endl;
    }
}
```

## 子数组最大乘积

[题目链接](https://leetcode.cn/problems/maximum-product-subarray/)

### Problem Statement

给你一个整数数组 `nums` ，请你找出数组中乘积最大的非空连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。

测试用例的答案是一个 **32 位** 整数。

### Constraints

- $1 \leq nums.length \leq 2 \times 10^4$
- $-10 \leq nums[i] \leq 10$
- `nums` 的任意前缀或后缀的乘积都在 **32 位** 整数范围内

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示数组中的各个元素。

> $n$
> 
> $nums_1, nums_2, \ldots, nums_n$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
4
2 3 -2 4
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
3
-2 0 -1
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析

这道题与最大子数组累加和的思路如出一辙，核心逻辑并没有发生本质改变。我们依然是在维护一个以当前位置结尾的最优状态，只不过运算规则从加法变成了乘积。但在处理乘法时，负数带来的影响是绝对不能忽视的。在加法运算中，负数顶多是让和变小，但在乘法运算中，两个负数相乘反而会得到正数，这种特殊情况不容忽视。

在处理乘积最大子数组问题时，由于负数的存在会导致乘积的正负性质发生翻转，因此状态转移需同步维护两个递推状态：以当前位置结尾的最大乘积 $dp_{max}[i]$ 与最小乘积 $dp_{min}[i]$ 。对于当前元素 $nums[i]$ ，最大乘积的更新取决于三个候选值的极值：前一位置最大乘积与当前值的积 $dp_{max}[i-1] \times nums[i]$ 、前一位置最小乘积与当前负值的积 $dp_{min}[i-1] \times nums[i]$ ，以及当前元素自身 $nums[i]$ 。

其核心的递推逻辑可以直观地表达为：

$$
dp_{max}[i] = \max(nums[i], \, dp_{max}[i-1] \cdot nums[i], dp_{min}[i-1] \cdot nums[i])
$$

$$
dp_{min}[i] = \min(nums[i], \, dp_{max}[i-1] \cdot nums[i], dp_{min}[i-1] \cdot nums[i])
$$

通过同步维护最大与最小状态，算法在一次 $O(n)$ 的线性扫描中，实现了对正数增长、负数翻转以及零点截断三种情况的全覆盖。这种建模方式简化了复杂的分类讨论，高效地从局部决策推导出了全局最优。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 2e4 + 100;
int a[MAXN];
ll dp_max[MAXN], dp_min[MAXN];

int main() {
    int n; cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    dp_max[0] = dp_min[0] = a[0];
    ll ans = a[0];
    for (int i = 1; i < n; i++) {
        ll cur = a[i];
        ll nxt_max = max({(ll)cur, dp_max[i - 1] * cur, dp_min[i - 1] * cur});
        ll nxt_min = min({(ll)cur, dp_max[i - 1] * cur, dp_min[i - 1] * cur});
        
        dp_max[i] = nxt_max;
        dp_min[i] = nxt_min;

        ans = max(ans, dp_max[i]);
    }

    cout << ans << endl;
}
```

---

# 子序列累加和问题

在动态规划的框架下，连续子数组问题的 **逻辑深度** 源于其对于 **空间关联性** 的严格限定。由于元素必须在序列中保持物理上的连续，算法决策被局限在特定的范围内，这使得我们能够通过以当前位置为终点的状态定义，将全局的最优性通过逐点推进的递推关系进行精准刻画。这种对位置连续性的依赖，消除了决策过程中的歧义，为动态规划在处理区间问题时提供了稳固的逻辑支撑。

与之不同，子序列累加和问题彻底解构了这种空间限制，赋予了元素极高的选取自由度。解决没有任何额外限制的子序列问题 **无需设计复杂的动态规划** ，因为仅凭简单的贪心逻辑选取所有正数即为最优解，这直接导致了该类问题失去了动态规划的讨论价值。因此子序列累加和这类题目，**必然建立在特定的约束条件之上** 。只有引入这些额外的限制，子序列累加和问题才具备了动态规划的讨论价值，从而使状态转移能够有效地刻画复杂的决策过程。

**打家劫舍问题** 就是子序列问题的经典范例。该类题目通过增加 **相邻元素不可同时选取** 的规则，彻底打破了贪心算法的全局最优性。在此类约束下，每一个位置的决策不再独立，而是必须通过状态转移权衡是否选取当前元素的收益。这种对决策状态的精准划分，将原本简单的累加问题转化为了 **带条件的路径选择** ，迫使算法在递推过程中必须动态评估前序决策所带来的约束限制。

### 打家劫舍对偶问题

打家劫舍的对偶问题是指在选择子序列时，约束条件从 “相邻位置不能同时选择” 变为 “相邻位置必选其一” 。这意味着在序列中，任何两个相邻元素都不允许被同时跳过。从对偶的角度来看，这一问题可以直接套用打家劫舍的思路：要求选中的元素满足相邻必选其一，等同于未选中的元素满足相邻不能同时选取。因此，如果目标是最小化选中元素的总和，本质上就是用数组总和减去该序列中满足打家劫舍约束的最大独立集之和。

如果我们考虑从正面直接求解，则需要利用状态定义来排除连续漏选的可能性。设 $dp[i][0]$ 为不选择当前元素时的最小累加和，$dp[i][1]$ 为选择当前元素时的最小累加和。状态之间的转移方式如下：

- 若当前位置 $i$ 不选，则前一个位置 $i-1$ 必须被选中

    $$
    dp[i][0] = dp[i-1][1]
    $$

- 若当前位置 $i$ 被选中，则前一个位置 $i-1$ 选或不选均可

    $$
    dp[i][1] = \min(dp[i-1][0], \, dp[i-1][1]) + nums[i]
    $$

这种建模方式直接在状态转移逻辑中整合了约束条件，通过前后位置的相互依赖，确保了选择结果的合法性。得益于这种状态设计的严密性，我们能够充分发挥动态规划的递推优势，仅通过一次线性扫描，即可高效解析出满足全部结构约束的最优方案。

## 打家劫舍基础题

[题目链接](https://leetcode.cn/problems/house-robber)

### Problem Statement

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警** 。

给定一个代表每个房屋存放金额的非负整数数组 `nums` ，计算你 **在不惊动警报装置的情况下** ，一夜之内能够偷窃到的最高金额。

### Constraints

- $1 \leq nums.length \leq 100$
- $0 \leq nums[i] \leq 400$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示房屋的数量。
- 第二行包含 $N$ 个整数，表示每个房屋中存放的金额。

> $N$
> 
> $nums_0 \quad nums_1 \quad \ldots \quad nums_{N-1}$

### Output

输出一个整数，表示你能够偷窃到的最高金额。

### Sample Input 1

```txt showLineNumbers=false
4
1 2 3 1
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
5
2 7 9 3 1
```

### Sample Output 2

```txt showLineNumbers=false
12
```

## 题目要点解析



## 环数组打家劫舍

[题目链接](https://leetcode.cn/problems/house-robber-ii/)

### Problem Statement

你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都 **围成一圈** ，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警** 。

给定一个代表每个房屋存放金额的非负整数数组 `nums` ，计算你 **在不惊动警报装置的情况下** ，今晚能够偷窃到的最高金额。

### Constraints

- $1 \leq nums.length \leq 100$
- $0 \leq nums[i] \leq 1000$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示房屋的数量。
- 第二行包含 $N$ 个整数，表示每个房屋中存放的金额。

> $N$
> 
> $nums_0 \quad nums_1 \quad \ldots \quad nums_{N-1}$

### Output

输出一个整数，表示你能够偷窃到的最高金额。

### Sample Input 1

```txt showLineNumbers=false
3
2 3 2
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
4
1 2 3 1
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析



## 序列最大中位数

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class128/Code05_MaximizeMedian1.java)

### Problem Statement

给定一个长度为 $n$ 的数组 `arr` 。请在所有合法的子序列中，找到最大的中位数。

一个合法的子序列定义为：在原数组中，任意相邻的两个数至少要有一个被挑选所组成的子序列。

**注意**：中位数的定义为 **上中位数** 。

- $[1, 2, 3, 4]$ 的上中位数是 $2$ 。
- $[1, 2, 3, 4, 5]$ 的上中位数是 $3$ 。

### Constraints

- $2 \leq n \leq 10^5$
- $1 \leq arr[i] \leq 10^9$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组的长度。
- 第二行包含 $n$ 个整数，表示数组 $arr$ 中的元素。

> $n$
> 
> $arr_0 \quad arr_1 \quad \ldots \quad arr_{n-1}$

### Output

输出一个整数，表示所有合法子序列中可能的最大中位数。

## 题目要点解析

打家劫舍对偶问题

## 最大交替子序列

[题目链接](https://leetcode.cn/problems/maximum-sum-of-alternating-subsequence-with-distance-at-least-k/description/)



## 题目要点解析



---

# 多区间累加和问题

多区间累加和问题通常根据 **区间长度是否固定** 分为两类。当长度固定时，区间结构规整，仅由起点决定；而长度可变时，左右端点均可自由浮动，导致 **状态设计与转移逻辑** 更为复杂。从建模上看，此类问题结合了子数组与子序列的特性：区间内部要求元素绝对连续，继承了子数组的连续性；区间之间则允许互不相邻，体现了子序列的灵活性。这种复合结构要求我们在状态转移时，既要维护好内部的连续性，也要协调好各区间间的跳跃逻辑。

除了区间长度，**区间个数** 同样是此类问题的核心约束。对于区间长度固定的情形，如果不限制区间个数，那么我们可以用最简单的线性动态规划解决，只需要预处理以每个位置开头的定长区间累加和即可。而对于长度可变的情形，如果不限制区间个数，那么问题则会直接退化为 **最普通的子序列累加和问题** ，我们只需贪心选取所有正数即可求解，从而失去了动态规划探讨的深度。接下来，我们将针对这两种情形，详细探讨在引入区间个数限制后，如何完成 **状态定义与转移逻辑** 的构建。

### 固定长度区间选取

在区间长度固定的场景下，假设每个区间的长度均为 $L$ ，且总共需要选取 $K$ 个区间。由于长度固定，任何合法的区间均可由其右端点 $i$ 唯一确定为 $[i-L+1, i]$ ，这使得问题的自由度归结为 **对一系列预设区间起点的选择** 。为了优化计算，我们可以先利用前缀和预处理出所有长度为 $L$ 的区间和，将原问题简化为在这些预设区间中，寻找 $K$ 个互不重叠且总和最大的组合。

预处理阶段，通过前缀和数组 $pre$ 快速计算以 $i$ 为结尾的区间和 $w[i]$：

$$
w[i] = pre[i] - pre[i-L]
$$

在构建动态规划模型时，我们设 $dp[i][j]$ 表示在前 $i$ 个位置中选取 $j$ 个长度为 $L$ 的区间所能达到的最大累加和。此时，在每一个位置 $i$ 处，决策逻辑简化为对当前结尾区间的选择与否：

$$
dp[i][j] = \max\Big( dp[i-1][j], \, dp[i-L][j-1] + w[i] \Big)
$$

方程的第一项 $dp[i-1][j]$ 代表不选择以 $i$ 为结尾的区间，直接继承前一位置的最优结果；第二项则代表强制选择区间 $[i-L+1, i]$ ，由于区间长度为 $L$ ，为了保证不重叠，上一个区间的结束位置必须在 $i-L$ 之前。这种建模方式利用了区间长度固定的特性，使冲突范围变得极其确定，整体时间复杂度稳定在 $O(nK)$ 。

### 自由长度区间选取

相比之下，当区间长度不再固定时，每个区间的左右端点 $[l, r]$ 均可自由选取，这显著提升了问题的灵活性与复杂度。我们设 $dp[i][j]$ 表示在前 $i$ 个位置中选取 $j$ 个互不重叠区间的最大总和。此时，核心决策逻辑在于：要么不以当前位置 $i$ 作为任何区间的结尾，直接继承 $dp[i-1][j]$ ；要么令第 $j$ 个区间在 $i$ 处结束，此时该区间的左端点 $t$ 成为决定性的变量。

若通过前缀和 $pre$ 进行初步建模，并枚举最后一个区间的起点 $t$ ，其转移方程可以表示为：

$$
dp[i][j] = \max\Big( dp[i-1][j], \, \max_{0 \leq t < i} \big( dp[t][j-1] + pre[i] - pre[t] \big) \Big)
$$

直接枚举起点 $t$ 会导致 $O(n^2K)$ 的计算复杂度，在处理大规模数据时效率较低。为了优化性能，我们可以将第二项的结构重新整理为以下形式：

$$
(dp[t][j-1] - pre[t]) + pre[i]
$$

观察可以发现，对于固定的区间个数 $j$ ，当 $i$ 向后扫描时，$pre[i]$ 是一个确定的偏移量，而我们需要寻找的是历史跨度中 $dp[t][j-1] - pre[t]$ 的最大值。因此，我们只需在扫描过程中实时维护一个变量 $best$：

$$
best = \max_{0 \le t < i} \big( dp[t][j-1] - pre[t] \big)
$$

此时，状态转移方程简化为：

$$
dp[i][j] = \max\big( dp[i-1][j], \, pre[i] + best \big)
$$

在每一步更新完 $dp[i][j]$ 后，随即利用当前的 $dp[i][j-1] - pre[i]$ 去更新 $best$ ，从而为后续位置的计算提供支持。通过这种方式，我们消除了对起点 $t$ 的显式枚举，使单次状态转移的时间复杂度降至 $O(1)$ ，整体复杂度也成功从 $O(n^2K)$ 优化至 $O(nK)$ 。这一优化的核心逻辑在于 **将区间枚举转化为历史最优值的增量维护** ，从而完成了从搜索型转移到常数级维护的结构升级。

## 神奇的魔法卷轴

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class071/Code03_MagicScrollProbelm.java)

### Problem Statement

给定一个数组 `nums` ，其中可能包含正数、负数和 $0$ 。

现在你有 **2 个** 魔法卷轴。每个魔法卷轴可以将数组 `nums` 中 **连续** 的一段区间内的所有数字全部变成 $0$ 。

你可以选择不使用卷轴，或者使用 $1$ 个或 $2$ 个卷轴。请返回在经过操作后，数组整体累加和可能的最大值。

### Constraints

- $1 \leq n \leq 10^6$
- $-10^9 \leq nums[i] \leq 10^9$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组的长度。
- 第二行包含 $n$ 个整数，表示数组 `nums` 中的元素。

> $n$
> 
> $nums_0 \quad nums_1 \quad \ldots \quad nums_{n-1}$

### Output

输出一个整数，表示在至多使用 $2$ 个魔法卷轴后，数组可能达到的最大累加和。

## 题目要点解析



## 无重叠子数组和

[题目链接](https://leetcode.cn/problems/maximum-sum-of-3-non-overlapping-subarrays)

### Problem Statement

给你一个整数数组 `nums` 和一个整数 `k` ，找出三个长度为 `k` 、互不重叠的子数组，它们的全部元素和最大。

我们需要返回这三个子数组起始下标的列表。如果存在多个结果，返回字典序最小的一个。

### Constraints

- $1 \leq nums.length \leq 2 \times 10^4$
- $1 \leq nums[i] < 2^{16}$
- $1 \leq k \leq \lfloor nums.length / 3 \rfloor$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ ，其中 $n$ 为数组长度。
- 第二行包含 $n$ 个整数，表示数组 `nums` 中的元素。

> $n \quad k$
> 
> $nums_0 \quad nums_1 \quad \ldots \quad nums_{n-1}$

### Output

输出三个整数，表示这三个互不重叠子数组的起始下标。

### Sample Input 1

```txt showLineNumbers=false
8 2
1 2 1 2 6 7 5 1
```

### Sample Output 1

```txt showLineNumbers=false
0 3 5
```

### Sample Input 2

```txt showLineNumbers=false
7 2
1 2 1 2 1 2 1
```

### Sample Output 2

```txt showLineNumbers=false
0 2 4
```

## 题目要点解析



## 环形最大子段和

[题目链接](https://www.luogu.com.cn/problem/P1121)

### Problem Statement

给出由 $n$ 个整数（可能为负数）组成的环状序列 $a_1, a_2, \ldots, a_n$ 。

你需要从该环状序列中选出两段 **互不重叠** 的非空连续子段，使得这两段子段中所有整数的和最大。

### Constraints

- $2 \leq n \leq 2 \times 10^5$
- $-10^4 \leq a_i \leq 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示环状序列的长度。
- 第二行包含 $n$ 个整数，表示环状序列中的各个元素。

> $n$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

输出一个整数，表示环状最大两段子段和的最大值。

### Sample Input 1

```txt showLineNumbers=false
7
2 -4 3 -1 2 -4 3
```

### Sample Output 1

```txt showLineNumbers=false
9
```

## 题目要点解析

也是对偶问题

## 反转数组最大和

[题目链接](https://github.com/algorithmzuo/algorithm-journey/blob/main/src/class071/Code05_ReverseArraySubarrayMaxSum.java)

### Problem Statement

给定一个数组 `nums` 。现在允许你随意选择数组中 **连续** 的一段区间进行 **翻转** 操作（即子数组逆序调整）。

- 例如：对于数组 `[1, 2, 3, 4, 5, 6]` ，翻转下标范围 `[2, 4]` 的子数组后，得到 `[1, 2, 5, 4, 3, 6]`

请返回在 **必须进行一次** 翻转操作后，所得数组的 **最大子数组累加和** 是多少。

### Constraints

- $1 \leq n \leq 10^6$
- $-10^9 \leq nums[i] \leq 10^9$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组的长度。
- 第二行包含 $n$ 个整数，表示数组 `nums` 中的元素。

> $n$
> 
> $nums_0 \quad nums_1 \quad \ldots \quad nums_{n-1}$

### Output

输出一个整数，表示必须翻转一次后，数组可能达到的最大子数组累加和。

## 题目要点解析



---

# 划分动态规划问题

划分动态规划的核心逻辑在于将一个给定序列 **完整地** 切分为若干连续的子段。这种题目类型要求序列中的每个元素都必须归属于某一个子段，从而实现对原序列的完全覆盖。在这种结构下，全局最优解的构建依赖于当前位置 $i$ 的最优状态，它是由前序某个切分点 $t$ 的子问题解与最后一段 $[t+1, i]$ 的代价直接拼接而成，从而实现从局部最优到整体最优的递推。

与多区间累加和问题相比，划分 DP 的核心在于元素分配的 **强制性** 。在区间选取问题中，我们可以灵活选择每个区间，从而通过放弃部分元素来规避负收益。但在划分 DP 的场景下，每个元素都必须被归入某个具体的段落中。这种全覆盖的约束迫使状态设计必须围绕切分点展开，从而确立了递推过程中的邻接依赖关系。

### 最优型划分问题

最优划分型问题通常不限制划分的具体个数，其目标是寻找一种分割方案，使得最终的累积得分或总代价达到全局最优。在这类问题中，状态定义通常采用一维形式，$dp[i]$ 表示前 $i$ 个元素达成最优划分时的得分。由于段数 $k$ 是未知的，在处理位置 $i$ 时，需要枚举所有可能的最后一个切分点 $t$ ，从而从历史的最优状态完成状态转移：

$$
dp[i] = \text{opt}_{0 \leq t < i} \{ dp[t] \otimes cost(t+1, i) \}
$$

这种建模方式将整个序列视为一个递归的切分决策序列，通过遍历所有合法的切分点 $t$ ，不断将当前区间 $[t+1, i]$ 的代价与前缀最优状态进行组合。最终，算法通过对所有历史切分可能性的比对，直接在状态空间中锁定全局最优的路径。

### 约束型划分问题

划分约束型问题对 **划分次数 K** 进行了明确限制。对于至多划分为 $K$ 份的需求，在实际处理中可以直接将其转化为恰好划分为 $j$ 份（ $1 \leq j \leq K$ ）的逻辑进行求解。在具体实现中，仅需按照恰好划分的流程计算出所有可能的段数结果，最后在结果收集阶段，从 $dp[n][1]$ 到 $dp[n][K]$ 中遍历并提取全局最优值。

在恰好划分为 $K$ 份的场景下，状态定义通常采用二维形式，$dp[i][j]$ 表示前 $i$ 个元素被精确划分为 $j$ 段时的最优值。在进行状态转移时，通过枚举最后一个划分点 $t$ 的位置来推进：假设最后一段的范围是 $[t+1, i]$ ，那么前 $t$ 个元素必然已经构成了 $j-1$ 段。其状态转移方程如下：

$$
dp[i][j] = \text{opt}_{j-1 \leq t < i} \{ dp[t][j-1] \otimes cost(t+1, i) \}
$$

**恰好型划分问题** 与 **多区间累加和问题** 在状态转移方程上非常相似，但核心区别在于 **状态继承项** 的处理。在多区间累加和问题中，由于元素允许被舍弃，方程必定包含 $dp[i-1][j]$ 这一项，代表当前元素不属于任何区间。但在恰好型划分问题中，由于区间必须实现全覆盖，方程必定不含 $dp[i-1][j]$ 这一项。

当 $cost(t+1, i)$ 具备可拆分性（如区间累加和 $pre[i] - pre[t]$ ）时，该模型同样可以进行结构优化。通过将方程整理为关于 $t$ 的独立项与关于 $i$ 的偏移项，可以引入辅助变量 $best$ 来实时维护历史最优值：

$$
best = \max_{j-1 \leq t < i} \{ dp[t][j-1] - pre[t] \}
$$

此时，状态转移方程简化为 $dp[i][j] = pre[i] + best$ 。在扫描过程中，每一步更新完 $dp[i][j]$ 后，随即利用当前的 $dp[i][j-1] - pre[i]$ 去更新 $best$ ，从而为后续位置的计算提供支持。这种优化方式消除了对起点 $t$ 的显式枚举，使单次状态转移的时间复杂度降至 $O(1)$ ，整体复杂度也从 $O(n^2K)$ 降至 $O(nK)$ 。

## 字符串乘积最值

[题目链接](https://www.luogu.com.cn/problem/P1018)

### Problem Statement

今年是 $2000$ 年，若某个同学能够解答出这个问题，他将获得 “中学生数学竞赛” 的冠军。这个问题是：有一个正整数 $N$（由 $n$ 位数字组成），现在你需要在这 $n$ 位数字之间插入 $k$ 个乘号，使得最终的乘积最大。

需要注意以下两点：

- 乘号不能放在数字的首尾。
- 插入的 $k$ 个乘号将 $N$ 分成了 $k + 1$ 个部分，这 $k + 1$ 个部分的乘积即为最终结果。

### Constraints

- $6 \leq n \leq 40$
- $1 \leq k \leq 6$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ 。
- 第二行包含一个长度为 $n$ 的正整数 $N$ 。

> $n \quad k$
> 
> $N$

### Output

输出一个整数，表示能够得到的最大乘积。

### Sample Input 1

```txt showLineNumbers=false
4 2
1231
```

### Sample Output 1

```txt showLineNumbers=false
62
```

## 题目要点解析



## 统计单词的个数

[题目链接](https://www.luogu.com.cn/problem/P1026)

### Problem Statement

给出一个长度不超过 $200$ 的字符串 $S$ ，该字符串由 $p$ 个部分组成，每个部分长度均为 $20$ 。现在需要将字符串 $S$ 分成 $k$ 个部分，使得这 $k$ 个部分中包含的单词总数最多。

**单词统计规则**：

- 单词在一个部分中出现，指的是该单词是该部分的子串。
- 如果一个单词在某个位置已经作为开头被统计过，则在该位置不能再统计其他单词。
- 单词表中的单词可能存在包含关系，需按上述规则计算。

### Constraints

- $1 \leq p \leq 10$
- $2 \leq k \leq 40$
- $1 \leq s \leq 6$

### Input

输入包含多行：

- 第一行包含两个整数 $p$ 和 $k$ 。
- 接下来的 $p$ 行，每行包含一个长度为 $20$ 的字符串，共同拼接成总字符串 $S$ 。
- 下一行包含一个整数 $s$ ，表示单词表中的单词个数。
- 接下来的 $s$ 行，每行包含一个单词。

> $p \quad k$
> 
> $S_{part1}$
> 
> $\ldots$
> 
> $S_{partP}$
> 
> $s$
> 
> $word_1$
> 
> $\ldots$
> 
> $word_s$

### Output

输出一个整数，表示最多能统计到的单词个数。

### Sample Input 1

```txt showLineNumbers=false
1 3
thisisabookyouareaoh
4
is
a
ok
sab
```

### Sample Output 1

```txt showLineNumbers=false
7
```

## 题目要点解析



## 环形的数字游戏

[题目链接](https://www.luogu.com.cn/problem/P1043)

### Problem Statement

在一条圆圈上有 $n$ 个数字（可能为负数），现在要将这 $n$ 个数字划分为 $m$ 个连续的部分（每个部分至少包含一个数字）。每一部分所有数字之和对 $10$ 取模（取模运算的结果应当在 $0$ 到 $9$ 之间，例如 $-1 \bmod 10 = 9$ ）。

最后将这 $m$ 个部分得到的数值相乘，请问最终的乘积最大和最小分别是多少。

### Constraints

- $1 \leq n \leq 50$
- $1 \leq m \leq 9$
- $-10^4 \leq a_i \leq 10^4$

### Input

输入包含多行：

- 第一行包含两个整数 $n$ 和 $m$ 。
- 接下来的 $n$ 行，每行包含一个整数，按顺序表示圆圈上的数字。

> $n \quad m$
> 
> $a_1$
> 
> $a_2$
> 
> $\ldots$
> 
> $a_n$

### Output

输出包含两行：

- 第一行输出一个整数表示可能的最小乘积。
- 第二行输出一个整数表示可能的最大乘积。

### Sample Input 1

```txt showLineNumbers=false
4 2
4
3
-1
2
```

### Sample Output 1

```txt showLineNumbers=false
7
81
```

## 题目要点解析



---

# 参考文献列表

1. [【elainafan】动态规划之划分型DP](https://www.cnblogs.com/namelessstory/p/19013752)