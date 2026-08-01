---
title: 【ACM 算法随笔】两数之和思想的应用
published: 2025-11-23
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: false
---

> 写在前面：本篇博客写作灵感来源于灵神的两数之和理解

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=305008442&bvid=BV1bP411c7oJ&cid=888954096&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 两数之和题目讲解

两数之和是 LeetCode 上编号为 $1$ 的开山题目，常被称作算法题中的 `Hello World!` 。它看起来十分基础，但其核心价值却远不止于新手练习。之所以值得专门展开讨论这个问题，是因为两数之和背后所蕴含的思想 **具有极强的泛用性** ，它不仅贯穿于大量经典算法问题之中，更是诸多数值统计方式的底层思想。许多题目你也许早已独立做过，却未必意识到它们在算法本质上有着如此紧密的内在联系。

接下来我们将以两数之和这一经典模型为主线，逐步串联起一系列相关题型及其解题思路。希望通过这样的横向对比与总结归纳，能够帮助我们跳脱出单个题目的有限视角，对那些看似零散却本质相通的问题形成更加 **系统化的认知** ，从而建立起更稳固的解题框架，做到真正的举一反三。

## 两数之和母题

[题目链接](https://leetcode.cn/problems/two-sum/description/)

### Problem Statement

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 **和为目标值** target 的那 **两个** 整数，并返回它们的数组下标。你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

### Constraints

- $2 \leq nums.length \leq 10^4$
- $-10^9 \leq nums[i] \leq 10^9$
- $-10^9 \leq target \leq 10^9$
- 只存在一个有效答案

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $target$ ，分别表示数组长度和目标值。
- 第二行包含 $n$ 个整数，表示数组中的各个元素。

> $n \quad target$
> 
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出两个整数 $i$ 和 $j$ 表示答案，且要满足 $i < j$ 。

### Sample Input 1

```txt showLineNumbers=false
4 9
2 7 11 15
```

### Sample Output 1

```txt showLineNumbers=false
0 1
```

### Sample Input 2

```txt showLineNumbers=false
3 6
3 2 4
```

### Sample Output 2

```txt showLineNumbers=false
1 2
```

### Sample Input 3

```txt showLineNumbers=false
2 6
3 3
```

### Sample Output 3

```txt showLineNumbers=false
0 1
```

## 题目要点解析

由于这个题目本身难度较低，我们不妨在它的基础上稍作扩展。具体来说，我们需要将原题中 **只存在一个有效答案** 的限制移除，允许出现 **多个不同的数对** 和为 target，并要求我们统计所有满足条件的数对数量。

为了统计所有满足条件的数对数量，我们可以先从最直观的解法入手：遍历数组中的每一个元素，并查找其左侧是否存在与之匹配的目标值。虽然这种直接枚举所有配对关系的暴力解法非常直观，但其时间复杂度高达 $O(n^2)$ 。

事实上，在从左到右遍历数组的过程中，当访问到当前的某个元素时，其左侧的所有信息均已知。如果我们能够在遍历的过程中 **实时记录** 已经出现过的数字及其频次，那么对于当前元素而言，我们只需花费 $O(1)$ 的时间就能立刻确认其匹配目标出现的次数，从而轻松得到当前元素对答案的贡献。

为此我们需要明确题目中所要求的条件：

$$
nums[i] + nums[j] = target
$$

然后将关于 $j$ 的部分移动到等式另一侧，可以得到：

$$
nums[i] = target - nums[j]
$$

当我们遍历数组时，如果能够实时记录已经出现过的数字 $nums[j]$ 的出现次数，那么对于当前数字 $nums[i]$ ，只需要查询它所对应的配对值 $target - nums[i]$ 之前总共出现了多少次，就能直接得出以 $i$ 为右端点所贡献的有效数对数量。我们可以得到如下的算法流程：

- **查询（Query）**：在哈希表中查找是否存在键为 $target - nums[i]$ 的记录，若存在则累计答案
- **记录（Update）**：将当前数字 $nums[i]$ 更新到哈希表中（出现次数 + 1 ），作为后续数字的配对目标

同理，我们也可以选择通过查询 $nums[i]$ 并记录 $target - nums[i]$ 的方式来解决这个问题。

```cpp frame="code" title="main.cpp"
# include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e4 + 100;
int n, target;
int a[MAXN];

int main(){
    cin >> n >> target;
    for (int i = 0; i < n; i++){
        cin >> a[i];
    }

    int ans = 0;  
    unordered_map<int, int> counts;
    for (int i = 0; i < n; i++){
        if (counts.count(target - a[i])){
            ans += counts[target - a[i]];
        }
        counts[a[i]]++;
    }

    cout << ans << endl;
}
```

核心代码也可以改成下面这样，效果是类似的：

```cpp frame="code" title="main.cpp"
int ans = 0;  
unordered_map<int, int> counts;
for (int i = 0; i < n; i++){
    if (counts.count(a[i])){
        ans += counts[a[i]];
    }
    counts[target - a[i]]++;
}
```

---

# 多元组序列类型题

掌握两数之和的核心思想后，我们便触及到序列处理的底层逻辑。而在面对杂乱的线性序列时，如何高效统计满足特定约束的多元素子序列，构成了算法中一类经典的 **多元组序列问题** 。无论是统计三元组还是探寻更高维度的组合序列，其核心的算法本质，都是两数之和思想在高维空间中的自然延伸。

当我们将视角从二元组扩展至三元组（满足 $i < j < k$ 的 $A_i, A_j, A_k$ ）时，**降维思想** 便成为了简化问题的核心工具。只需固定最右侧端点 $k$ ，原问题便退化为在动态变化的区间 $[0, k-1]$ 中寻找满足特定条件的二元组。这意味着，复杂的三元组统计并非全新的课题，而是建立在两数之和基础之上的嵌套结构。

除了固定右端点，我们还可以切换至 **中心枚举** 的视角。为了高效实现这一思路，我们需要引入按元素大小排序的下标数组 $idx$ ，从而在不破坏元素原始位置信息的前提下，获得一套按数值排列的索引映射。

在此基础上，当我们依次枚举 $idx$ 中的元素作为中心点 $j$ 时，可以将之前遍历过的历史下标按照位置关系进行分拣，把原始下标小于 $j$ 的放入左侧集合作为 $i$ 的候选，把原始下标大于 $j$ 的放入右侧集合作为 $k$ 的候选。由于整个枚举过程是严格按照数值大小推进的，此时分拣到左右两个集合中的元素便天然具备数值上的有序性，从而将棘手的偏序匹配问题巧妙地转化为 **两个有序序列** 之间的线性扫描。

## 三数累加和问题

[题目链接](https://leetcode.cn/problems/3sum-with-multiplicity/description/)

### Problem Statement

给定一个整数数组 `arr` ，以及一个整数 `target` 作为目标值。

请返回满足 `i < j < k` 且 `arr[i] + arr[j] + arr[k] == target` 的元组 `i, j, k` 的数量。

由于结果会非常大，请返回 $10^9 + 7$ 的模。

### Constraints

- $3 \leq arr.length \leq 3000$
- $0 \leq arr[i] \leq 100$
- $0 \leq target \leq 300$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $target$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad target$
>
> $arr_1 \quad arr_2 \quad \ldots \quad arr_N$

### Output

输出满足条件的三元组的数量。

### Sample Input

```txt showLineNumbers=false
10 8
1 1 2 2 3 3 4 4 5 5
```

### Sample Output

```txt showLineNumbers=false
20
```

## 题目要点解析

三数之和的做法并不复杂，我们可以先固定第三个下标 $k$ ，把它作为当前三元组的右端点，后续则只需要将范围限定在前缀区间 $[0, k-1]$ 即可。在 $k$ 已经确定的情况下，原问题便退化为经典的两数之和问题，即在该前缀区间内寻找一对下标 $i < j$ ，使得它们对应的两个数与 $arr[k]$ 之和等于目标值。

原问题中关于数值的约束可以写为：

$$
arr[i] + arr[j] + arr[k] = target
$$

将与 $k$ 相关的项移到等式右侧就能得到：

$$
arr[i] + arr[j] = target - arr[k]
$$

此时，问题已经完全转化为标准的 **两数之和计数问题**：在前缀区间 $[0, k-1]$ 中，统计有多少对下标满足 $i < j$ 且对应的元素之和等于 $target - arr[k]$ 。因此，只要我们能够在遍历过程中维护左侧区间中各个数值的出现次数，就可以在常数时间内计算出当前 $k$ 下标所贡献的有效三元组数量。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MOD = 1e9 + 7;
const int MAXN = 3000 + 5;
int n, target;
int arr[MAXN];

int main() {
    cin >> n >> target;
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    ll ans = 0;
    for (int k = 0; k < n; k++) {
        unordered_map<int, int> counts;
        
        for (int j = 0; j < k; j++) {
            int need = target - arr[k] - arr[j];
            if (counts.count(need)) {
                ans = (ans + counts[need]) % MOD;
            }
            counts[arr[j]]++;
        }
    }

    cout << ans << endl;
}
```

## 有效三角形数量

[题目链接](https://leetcode.cn/problems/valid-triangle-number/description/)

### Problem Statement

给定一个包含非负整数的数组 `nums` ，返回其中可以组成三角形三条边的三元组个数。

### Constraints

- $1 \leq nums.length \leq 1000$
- $0 \leq nums[i] \leq 1000$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组长度。
- 第二行包含 $N$ 个整数，表示数组元素。

> $N$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数，表示可以组成三角形的个数。

### Sample Input 1

```txt showLineNumbers=false
4
2 2 3 4
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
4
4 2 3 4
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析

根据三角形的性质，若三边满足 $a \leq b \leq c$ ，则只需满足 $a + b > c$ 即可。因此，我们可以先对数组进行升序排序，随后固定最大边的下标 $k$ ，在区间 $[0, k-1]$ 内寻找满足条件的二元组 $(i, j)$ 。

此时原问题的约束可以转化为：

$$
arr[i] + arr[j] > arr[k]
$$

在 $k$ 确定的情况下，我们可以使用 **双指针法** 快速计数。将左指针 $i$ 置于 $0$ ，右指针 $j$ 置于 $k-1$ 。

若当前满足 $arr[i] + arr[j] > arr[k]$ ，说明在 $j$ 固定的前提下，下标在 $[i, j-1]$ 范围内的所有元素均可作为最小边与 $arr[j]$ 组成三角形，其贡献的组合数为：

$$
Ans = Ans + (j - i)
$$

若当前两数之和不满足条件，则向右移动 $i$ 以增大数值。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

## 统计好的三元组

[题目链接](https://leetcode.cn/problems/count-good-triplets/description/)

### Problem Statement

给你一个长度为 $N$ 的整数数组 `arr` ，以及三个整数 $a$、$b$、$c$。请你统计其中 **好三元组** 的数量。

如果三元组 `(arr[i], arr[j], arr[k])` 满足下列全部条件，则认为它是一个好三元组：

- $0 \leq i < j < k < N$
- $|arr[i] - arr[j]| \leq a$
- $|arr[j] - arr[k]| \leq b$
- $|arr[i] - arr[k]| \leq c$

其中 $|x|$ 表示 $x$ 的绝对值。

### Constraints

- $3 \leq N \leq 100$
- $0 \leq arr[i] \leq 1000$
- $0 \leq a, b, c \leq 1000$

### Input

输入包含两行：

- 第一行包含四个整数 $N$ 、$a$ 、$b$ 和 $c$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad a \quad b \quad c$
> 
> $arr_1 \quad arr_2 \quad \ldots \quad arr_N$

### Output

输出一个整数，表示满足条件的好三元组的数量。

### Sample Input 1

```txt showLineNumbers=false
6 7 2 3
3 0 1 1 9 7

```

### Sample Output 1

```txt showLineNumbers=false
4

```

### Sample Input 2

```txt showLineNumbers=false
5 0 0 1
1 1 2 2 3

```

### Sample Output 2

```txt showLineNumbers=false
0

```

## 题目要点解析

针对这道题，最直观的策略是通过 **三重循环枚举** 所有的下标组合，并在枚举过程中逐一验证其是否满足那三个绝对值约束。在 $N \leq 100$ 的数据规模下，这种 $O(N^3)$ 的暴力解法足以通过评测。然而，这道题真正的价值在于如何打破多维约束的限制，利用降维思想来优化暴力的三重循环枚举。

第一种优化思路借鉴了 **三数之和** 中固定右端点的策略。我们尝试固定右端点 $k$ ，并在中间点 $j$ 从 $0$ 向 $k-1$ 顺序移动的过程中实现高效统计。为了在循环中同时维护多条约束，我们需要引入一个 **动态维护的频率数组** 来记录历史状态。当 $j$ 满足约束 $|arr[j] - arr[k]| \leq b$ 时，首先根据当前的频率数组查询左侧所有合法的 $i$ ，然后判断 $arr[j]$ 是否满足约束 $|arr[j] - arr[k]| \leq c$ ，若满足则将其存入频率数组作为后续迭代的候选。

这种设计的巧妙之处在于，查询操作发生在当前元素更新数组之前，从而满足 $i < j < k$ 的下标序关系。为了实现 $O(1)$ 的区间检索，我们利用前缀和数组 `pre` 来维护当前状态下 $\leq \text{num}$ 的元素个数。此时，第一个不等式约束 $|arr[i] - arr[j]| \leq a$ 便可转化为值域区间 $[arr[j]-a, \, arr[j]+a]$ 的范围计数问题，通过前缀差分即可快速获取答案。这种方法将复杂度优化至 $O(N^2 + N \cdot \text{maxVal})$ ，在值域较小时表现卓越。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

尽管这种做法十分巧妙，但由于复杂度与数值大小相关，在值域较大的情况下效率会降低，因此需要转变思路。绝对值约束的核心难点在于数据通常是无序的，而本题要求统计满足特定顺序的三元组，因此我们无法直接对原数组进行排序。为了能让数据有序，我们需要构建一个下标数组 `idx` ，并按照原数组 `arr` 中的数值进行升序排列。

每当我们枚举数组 `idx` 中的元素作为三元组的中间点 $j$ 时，需要将已遍历的历史元素重新分组。在此过程中，我们需要结合历史元素的原始下标及其对应的数值约束，将其分别归入 **left** 或 **right** 两个集合：当历史元素的原始下标 $idx[p] < j$ 且数值满足 $arr[j] - arr[idx[p]] \leq a$ 时，将其归入 left 集合作为合法的 $i$ 候选；当历史元素的原始下标 $idx[p] > j$ 且数值满足 $arr[j] - arr[idx[p]] \leq b$ 时，将其归入 right 集合作为合法的 $k$ 候选。

由于我们是按照 `idx` 的升序逻辑进行遍历，每次提取出的历史元素本身就具备单调性，这使得生成的 **left** 和 **right** 集合 **天然具备有序性** 。为了满足最后一个约束 $|arr[i] - arr[k]| \leq c$ ，需要通过枚举 left 中的每个元素 $x$ ，将问题转化为在 right 中寻找落在区间 $[x-c, \, x+c]$ 内的合法对象。利用 **三指针技巧** 维护两个在 **right** 上单调滑动的边界，即可在摆脱值域依赖的前提下，以 $O(N^2)$ 的复杂度完成所有配对统计。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

---

# 数组子段和类型题

在处理数组子段和问题时，如果我们预先定义 $pre$ 数组为原数组的前缀和数组，那么原数组中任意一段连续子数组的和 $sum(left, right)$ 都可以通过两个前缀项的差值来精确表达：

$$
sum(left, right) = pre[right] - pre[left]
$$

也就是说，一个数组子段的和本质上等价于 **两个前缀和之间的差值** 。当我们从这个角度重新观察问题时，就会发现很多原本看起来复杂的子数组问题，其实都可以转化为 **寻找满足某种关系的两个前缀值** 。换句话说，我们并不需要直接枚举整个数组的所有子数组，而是只需要关注 **前缀之间的关系** 。

这样一来，数组子段和就转化为经典的 **两数之和问题** 。当我们枚举右端点 $right$ 时，本质上就是固定了当前的前缀值 $pre[right]$ ，此时的问题就转化为判断 **是否存在某个左端点 left，使得 $pre[left]$ 与当前的前缀值满足某个条件** 。根据题目的不同限制，我们可以用不同的方式来维护这些可能的前缀值。

因此从建模角度来看，很多所谓的 **数组子段和问题** ，本质上都可以理解为一种 **前缀和上的两数关系问题** 。当我们意识到这一点之后，许多看似不同的题目其实都可以用类似的思路来处理：枚举一侧端点，并在另一侧维护可能成为答案的候选集合。接下来我们就通过几个具体的例子，来进一步体会这种转化在实战中的应用方式。

## 累加和为定值的最长子数组长度

[题目链接](https://www.nowcoder.com/practice/36fb0fd3c656480c92b569258a1223d5)

### Problem Statement

给定一个无序数组 $arr$ ，其中元素是在一定范围内的任意整数。

给定一个整数 $k$ ，求 $arr$ 所有子数组中累加和为 $k$ 的最长子数组长度。

### Constraints

- $1 \leq N \leq 10^5$
- $-10^9 \leq k \leq 10^9$
- $-100 \leq arr_i \leq 100$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad k$
>
> $arr_1 \quad arr_2 \quad \ldots \quad arr_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
5 0
1 -2 1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点解析

借用两数之和的核心思想，我们可以将子数组和问题转化为前缀和之间的差值问题。设 $pre[i]$ 表示前 $i$ 个元素的前缀和，则任意区间满足子数组和为 $k$ 的条件可以写成：

$$
pre[right] - pre[left] = k \qquad (left \leq right)
$$

基于这个等式，我们可以根据不同的移项方式，推导出两种完全对称但实现细节不同的写法。

### 思路一：查历史存当前

从原式移项变形后可以得到：

$$
pre[right] - k = pre[left]
$$

当我们遍历到位置 right 时，我们需要在哈希表中 **查找过去是否出现** 值为 $pre[right]-k$ 的前缀和。然后再把当前的前缀和 $pre[right]$ 记录到哈希表中，作为后续位置的查询依据。

由于此时存的是 **真实的前缀和** ，在正式开始遍历前，前缀和为 $0$ ，因此必须初始化为：

```cpp showLineNumbers
pos[0] = -1
```

### 思路二：查当前存期望

将原式换另一种移项方式变形：

$$
pre[right] = pre[left] + k
$$

当我们遍历到位置 right 时，我们需要在哈希表中 **查询过去是否需要** 值为 $pre[right]$ 的前缀和。接着再把未来的期望值 $pre[right] + k$ 存入哈希表，表示该元素希望遇到这个数来凑成区间和 $k$ 。

由于此时存的是 **期望值** ，初始前缀和为 $0$ ，而它期待未来遇到值为 $k$ 的前缀和，因此初始化为：

```cpp showLineNumbers
pos[k] = -1
```

无论采用哪种写法，为了找到 **最长子数组** ，哈希表都只需要记录每个键 **第一次出现的位置** 。这样当匹配成功时，左端点越靠前，区间长度自然越大。基于以上两类思路，我们即可写出最终代码：

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e5 + 100;
int N, k;
int arr[MAXN];

int main() {
    cin >> N >> k;
    for (int i = 0; i < N; i++) {
        cin >> arr[i];
    }

    unordered_map<long long, int> pos;  
    pos[k] = -1; int pre = 0, ans = 0;
    for (int i = 0; i < N; i++) {
        pre += arr[i];

        if (pos.count(pre)) {
            ans = max(ans, i - pos[pre]);
        }

        if (!pos.count(pre + k)) {
            pos[pre + k] = i;
        }
    }

    cout << ans << endl;
}
```

## 和为K的子数组

[题目链接](https://leetcode.cn/problems/subarray-sum-equals-k/description/)

### Problem Statement

给你一个整数数组 $nums$ 和一个整数 $k$ ，请你统计并返回该数组中和为 $k$ 的子数组的个数。

子数组是数组中元素的连续非空序列。

### Constraints

- $1 \leq nums.length \leq 2 * 10^4$
- $-1000 \leq nums[i] \leq 1000$
- $-10^7 \leq k \leq 10^7$

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
3 2
1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
3 3
1 2 3
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析

本题的核心突破口在于需要将连续区间求和转化为两个前缀和的差值。借助前缀和序列 $pre$ ，我们可以将题目中子数组和为 $k$ 的条件，等价变形为 $pre[j] - pre[i-1] = k$ 。这一转化成功将原本需要双重循环的区间枚举操作，转化为寻找特定数值匹配的两数之和问题。

在实现过程中，我们需要利用哈希表动态维护已经扫描过的前缀和及其出现频率。由于题目变形后的核心目标是寻找满足 $pre[i-1] = pre[j] - k$ 的历史状态，我们只需要在遍历过程中实现边查询边更新即可。需要特别注意的是，哈希表的初始状态应包含 `counts[0] = 1` ，表示子数组从第一个元素开始且前缀和正好为 $k$ 的特殊情况。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 2e4 + 100;
int N, k;
int nums[MAXN];

int main() {
    cin >> N >> k;
    for (int i = 0; i < N; i++){
        cin >> nums[i];
    }

    unordered_map<int, int> counts;
    int ans = 0, pre = 0; counts[k] = 1;
    for (int i = 0; i < N; i++){
        pre += nums[i];
        if (counts.count(pre)){
            ans += counts[pre];
        }
        counts[pre + k]++;
    }

    cout << ans << endl;
}
```

## 正负相同子数组

[题目链接](https://www.nowcoder.com/practice/545544c060804eceaed0bb84fcd992fb)

### Problem Statement

给定一个无序数组 $arr$ ，求 $arr$ 所有子数组中正数与负数个数相等的最长子数组的长度。

### Constraints

- $1 \leq arr.length \leq 10^5$
- $-100 \leq arr_i \leq 100$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ ，表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input

```txt showLineNumbers=false
5
1 -2 1 1 1
```

### Sample Output

```txt showLineNumbers=false
2
```

## 题目要点解析

题目中提到的 **正数与负数个数相等** 的要求是解题的突破口。对于这类需要保证两种特征值数量相等的问题，最经典的技巧就是对数据进行 **二值化** 处理，以此将数量相等的要求转化为累加和为 $0$ 的问题。

需要特别注意的是，原数组中的 $0$ 既不是正数也不是负数，在转换时应当保持为 $0$ ，编写 `if-else` 分支时切勿将其错误地归类到正数或负数当中。经过这样的处理后，原问题就等价为 **寻找累加和为 0 的最长子数组** ，至此我们便可以直接套用[累加和为定值的最长子数组长度](#累加和为定值的最长子数组长度)的代码框架来高效解决这个问题。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e5 + 100;
int N; int arr[MAXN];

int main() {
    cin >> N;
    for (int i = 0; i < N; i++) {
        int num; cin >> num;
        if (num < 0) arr[i] = -1;
        if (num > 0) arr[i] = 1;
    }

    unordered_map<long long, int> pos;
    pos[0] = -1; int pre = 0, ans = 0;
    for (int i = 0; i < N; i++) {
        pre += arr[i];

        if (pos.count(pre)) {
            ans = max(ans, i - pos[pre]);
        }

        if (!pos.count(pre)) {
            pos[pre] = i;
        }
    }

    cout << ans << endl;
}
```

## 题目相关拓展

这道题也可以从 **分类统计前缀和** 的视角来重新理解，我们定义两个新的辅助数组 $arr\_pos$ 和 $arr\_neg$ ：

- 若当前数字是正数，则 $arr\_pos[i] = 1$ ，若当前数字不是正数，则 $arr\_pos[i] = 0$
- 若当前数字是负数，则 $arr\_neg[i] = 1$ ，若当前数字不是负数，则 $arr\_neg[i] = 0$

然后对这两个数组分别求前缀和，得到 $pre\_pos$ 和 $pre\_neg$ ，那么 **正负数相同** 的子数组就可以表示为：

$$
pre\_pos[r] - pre\_pos[l] = pre\_neg[r] - pre\_neg[l]
$$

我们将这个等式进行变形，把属于同一个位置的属性归到等号同一侧，可以得到：

$$
pre\_pos[r] - pre\_neg[r] = pre\_pos[l] - pre\_neg[l]
$$

根据这个形式，我们可以定义一个新数组 $pre[i] = pre\_pos[i] - pre\_neg[i]$ ，上面的条件就等价为：

$$
pre[r] = pre[l]
$$

这个思路的推导结果 **本质上与二值化完全等价** ，因为 $pre[r] = pre[l]$ 同样表示子数组累加和为 $0$ 的含义。但分类统计前缀和的思路可以延伸到二值化无法处理的复杂问题上，也就是要求子数组包含三种或更多种元素的情况。比如题目如果需要寻找正数、负数和零个数都相等的最长子数组，二值化将会彻底失效。

利用这个思路，我们在处理正数、负数和零这三种元素时，核心目标就是寻找一个三种元素的出现次数完全相等的区间。为了同时约束这三个变量，我们需要列出连等式：

$$
pre\_pos[r] - pre\_pos[l] = pre\_neg[r] - pre\_neg[l] = pre\_zero[r] - pre\_zero[l]
$$

根据之前的变形技巧，我们将同一个位置的属性归类到等号同一侧。这个连等式可以 **拆解为两个独立的等式**：

$$
pre\_pos[r] - pre\_neg[r] = pre\_pos[l] - pre\_neg[l]
$$

$$
pre\_neg[r] - pre\_zero[r] = pre\_neg[l] - pre\_zero[l]
$$

根据这两个等式，我们可以定义两个新数组 $pre_1[i] = pre\_pos[i] - pre\_neg[i]$ 和 $pre_2[i] = pre\_neg[i] - pre\_zero[i]$ 。因此上面的条件就可以完美等价为：

$$
pre_1[r] = pre_1[l] \quad pre_2[r] = pre_2[l]
$$

为了同时满足这两个差值条件，我们需要将这两个新数组在相同位置的值绑定为二元组来代表该位置的状态：

$$
\big(pre_1[i], \, pre_2[i]\big)
$$

只要位置 $r$ 计算出的二元组与先前某个位置 $l$ 记录的二元组完全相同，就表明该区间内三种元素的 **出现次数完全相等** 。在遍历数组时，我们只需要利用哈希表记录每个二元组状态首次出现的位置，便可在 $O(1)$ 的时间内完成状态匹配，从而使整个算法在线性时间复杂度内高效完成。

## 良好最长时间段

[题目链接](https://leetcode.cn/problems/longest-well-performing-interval/)

### Problem Statement

给你一份工作时间表 $hours$ ，上面记录着某一位员工每天的工作小时数。

我们认为当员工一天中的工作小时数大于 8 小时的时候，那么这一天就是「劳累的一天」。

所谓「表现良好的时间段」，意味在这段时间内，「劳累的天数」是严格 大于「不劳累的天数」。

请你返回「表现良好时间段」的最大长度。

### Constraints

- $1 \leq hours.length \leq 10^4$
- $0 \leq hours[i] \leq 16$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ ，表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $hours_1 \quad hours_2 \quad \ldots \quad hours_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
7
9 9 6 0 6 6 9
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
3
6 6 6
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析

这道题可以使用类似于[正负相同子数组](#正负相同子数组)的二值化方法，只需将大于 $8$ 的数值映射为 $1$ ，小于等于 $8$ 的数值映射为 $-1$ 即可。此时，问题转化为寻找 **元素累加和大于 0 的最长子数组** 。引入前缀和数组 $pre$ 后，子数组累加和大于 $0$ 这一条件等价于 $pre[left] < pre[right]$ 。

从形式化定义来看，该问题等价于在前缀和数组中寻找一对特殊的索引 $(left, right)$ ，在满足 $left < right$ 且 $pre[left] < pre[right]$ 的前提下，使得区间长度 $right - left$ 最大。这本质上可以抽象为一个经典的 **单调栈问题**：我们需要为每一个右端点 $right$ ，在其左侧找到一个 **数值更小** 且 **距离最远** 的下标 $left$ ，进而通过维护全局最大差值来锁定最终答案。

值得注意的是，由于转化后的数组仅由 $\pm 1$ 构成，前缀和数组中相邻元素之间的绝对差值恒为 $1$ ，在数值变化上呈现出不可跳跃变化的 **单调连续性** 。利用这一性质，我们可以进一步优化算法。

当我们遍历到位置 $i$ 时，若 $pre[i] > 0$ ，则说明从数组的起始位置到当前位置的子数组累加和已满足约束，可以直接判定当前的最长长度为 $i + 1$ ；若 $pre[i] \leq 0$ ，则需要在其左侧寻找一个位置 $left$ ，在满足 $pre[left] < pre[i]$ 的前提下使区间长度 $i - left$ 达到最大，此时的关键便在于如何高效确定这个 $left$ 。

根据单调连续性，前缀和从 $0$ 下降到 $x$ 的过程中，必然会在 **更早的位置** 先变化为 $x + 1$ 。也就是说，$pre[i] - 1$ 首次出现的位置一定早于 $pre[i] - 2$ 、$pre[i] - 3$ 等其他更小数值首次出现的位置。因此为了最大化区间长度，我们只需关注 $pre[i] - 1$ 首次出现的位置，完全不用理会那些更小的前缀和数值。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e4 + 100;
int N; int hours[MAXN];

int main(){
    cin >> N;
    for (int i = 0; i < N; i++){
        cin >> hours[i];
    }

    unordered_map<int, int> first;
    first[0] = -1; int pre = 0; int ans = 0;
    for (int i = 0; i < N; i++){
        if (hours[i] > 8) pre += 1;
        else pre -= 1;

        if (pre > 0){
            ans = max(ans, i + 1);
        }

        else if (first.count(pre - 1)){
            ans = max(ans, i - first[pre - 1]);
        }

        if (!first.count(pre)){
            first[pre] = i;
        }
    }

    cout << ans << endl;
}
```

## 题目相关拓展

如果将题目中 **寻找最长子数组** 的条件改为 **统计目标子数组个数** ，我们又该如何处理呢？从形式化定义来看，该问题等价于在前缀和数组中统计有多少对 $(left, right)$ 满足 $left < right$ 且 $pre[left] < pre[right]$ 。由于每一个符合条件的数对都对应一个满足约束的子数组，因此统计数对个数即可得到目标子数组的总数。该问题在本质上属于 **顺序对问题** ，可以直接使用 **归并分治** 或 **树状数组** 来解决。

现在我们需要考虑如何利用 **单调连续性** 进行优化：由于前缀和的变化每次仅为 $\pm 1$ ，当遍历到某个位置时，我们只需要知道 **严格小于** 当前 $pre[i]$ 的前缀个数，就能直接获取当前满足要求的顺序对数量。基于这个特点，我们可以使用 **增量法** 来动态维护前缀的统计信息。

在遍历的过程中，若当前的前缀和 $pre[i]$ 比 $pre[i-1]$ 增加 $1$ ，那么严格小于 $pre[i]$ 的前缀个数，就是在严格小于 $pre[i-1]$ 的前缀个数的基础上累加 $pre[i-1]$ 的频次；若当前前缀和 $pre[i]$ 比 $pre[i-1]$ 减少 $1$ ，那么严格小于 $pre[i]$ 的前缀个数，就是在严格小于 $pre[i-1]$ 的前缀个数的基础上减去 $pre[i]$ 的频次。

由于前缀和变化的步长恒为 $1$ ，因此动态维护严格小于当前 $pre[i]$ 的前缀个数非常高效，只需用一个哈希表或数组统计每种前缀值出现的次数，便可在常数时间内轻松完成状态的更新。

## 构造P整除数组

[题目链接](https://leetcode.cn/problems/make-sum-divisible-by-p/description/)

### Problem Statement

给你一个正整数数组 $nums$ ，请你移除 **最短** 子数组（可以为 **空** ），使得剩余元素的 **和** 能被 $p$ 整除。**不允许** 将整个数组都移除。请你返回你需要移除的最短子数组的长度，如果无法满足题目要求，返回 $-1$ 。

**子数组** 定义为原数组中连续的一组元素。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $0 \leq nums[i] \leq 10^9$
- $1 \leq p \leq 10^9$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $p$ 。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
4 6
3 1 4 2
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
4 9
6 3 5 2
```

### Sample Output 2

```txt showLineNumbers=false
2
```

### Sample Input 3

```txt showLineNumbers=false
3 3
1 2 3
```

### Sample Output 3

```txt showLineNumbers=false
0
```

## 题目要点解析

首先这道题有一个很明显的突破口：如果整个数组的总和模 $p$ 余 $0$ ，那我们不需要移除任何元素。如果整个数组的总和模 $p$ 余 $r$ ，那我们的目标就转变为找到累加和（取模后）同样为 $r$ 的最短子数组。

因此我们可以得到下面这个条件：

$$
pre[right] - pre[left] \equiv r \pmod{p}
$$

我们将 $left$ 移至右侧可以得到：

$$
pre[right] \equiv r + pre[left] \pmod{p}
$$

因此，我们要在查询 $pre[i] \% p$ 的同时，记录 $(r + pre[i]) \% p$ 出现的最早位置。从两数之和的角度来看，这道题的标准做法其实很自然，虽然涉及取模运算，表面上看似乎有些奇怪，但其背后的数学逻辑非常直观。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int N; ll p;

int main() {
    cin >> N >> p;
    vector<long long> nums(N);
    for (int i = 0; i < N; i++) {
        cin >> nums[i];
    }

    ll total = 0;
    for (ll x : nums) total += x;
    int r = total % p;
    if (r == 0) {
        cout << 0 << endl;
        return 0;
    }

    unordered_map<int, int> pos;
    pos[0] = -1; ll pre = 0; int ans = N;
    for (int i = 0; i < N; i++) {
        pre = (pre + nums[i]) % p;

        int need = (pre - r + p) % p;
        if (pos.count(need)) {
            ans = min(ans, i - pos[need]);
        }

        pos[pre] = i;
    }

    if (ans == N) cout << -1 << endl;
    else cout << ans << endl;
}
```

## 树上的路径总和

[题目链接](https://leetcode.cn/problems/path-sum-iii/description/)

### Problem Statement

给定二叉树的根节点 `root` 和整数 `targetSum` ，求该二叉树里节点值之和等于 `targetSum` 的 **路径** 数目。

**路径** 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。

![树上的路径问题图像](src\content\posts\ACM\acm-note\two-sum-idea\树上的路径问题.png)

### Constraints

- 二叉树的节点个数的范围是 $[0,1000]$
- $-10^9 \leq Node.val \leq 10^9$
- $-1000 \leq targetSum \leq 1000$

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $targetSum$ ，其中 $N$ 表示节点个数。
- 第二行包含 $N$ 个整数，表示这颗树 $1 \sim N$ 节点的权值，其中 $1$ 节点为根节点。
- 接下来的 $N - 1$ 行中，每一行都会给出两个整数，表示这两个节点之间有边相连。

> $N \quad targetSum$
>
> $Node_1 \quad Node_2 \quad \ldots \quad Node_N$
> 
> $Node_{u_1} \quad Node_{v_1}$
>
> $\ldots$
>
> $Node_{u_{N-1}} \quad Node_{v_{N-1}}$

### Output

输出一个整数表示答案。

### Sample Input

```txt showLineNumbers=false
9 8
10 5 -3 3 2 11 3 -2 1
1 2
1 3
2 4
2 5
3 6
4 7
4 8
5 9
```

### Sample Output

```txt showLineNumbers=false
3
```

## 题目要点解析

这是一道典型的 **树上向下路径** 统计问题。由于路径只能从父节点走向子节点，因此在 DFS 过程中，从根节点到当前节点所构成的递归路径，本质上就是一条一维序列。于是问题进而可以转化为：在这条动态路径中，寻找满足条件的节点对，使得两者对应的前缀路径和的差等于 `targetSum` 。

设当前遍历到节点 $u$ 时，从根到 $u$ 的路径和为 `curSum` 。若存在某个祖先节点，其对应的路径和为 `x` ，满足：

$$
curSum - x = targetSum
$$

那么从该祖先之后到当前节点这一段路径就是一个合法解。因此我们可以在 DFS 过程中维护一个哈希表，用来记录当前路径上每个前缀和的出现次数。访问当前节点时，先计算新的 `curSum` ，然后查询 `curSum - targetSum` 在哈希表中出现的频次，并将其累加到答案中。随后将当前 `curSum` 计入哈希表，继续递归访问子树。而在递归返回时，需将当前 `curSum` 的出现次数减一，以确保哈希表中始终只保存当前递归路径上的有效信息。

整棵树只需进行一次 DFS，每个节点也只涉及常数次的查询与更新，因此时间复杂度为 $O(N)$ 。从结构上看，这类问题的关键在于路径与递归状态的完美重叠。这使得整棵树在递归的过程中，任意时刻从根到当前节点的路径都能被视作一维序列，从而将复杂的树上问题转化为该路径上的两数在线匹配问题。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 1005;
int N; ll targetSum;
ll val[MAXN];
vector<int> G[MAXN];

void dfs(int u, int parent, ll pre) {
    pre += val[u];
    if (counts.count(pre)) {
        ans += counts[pre];
    }

    counts[pre + targetSum]++;
    for (int v : G[u]) {
        if (v == parent) continue;
        dfs(v, u, pre);
    }
    counts[pre + targetSum]--;
}

int main() {
    cin >> N >> targetSum;
    for (int i = 1; i <= N; i++) {
        cin >> val[i];
    }

    for (int i = 1; i < N; i++) {
        int u, v;
        cin >> u >> v;
        G[u].push_back(v);
        G[v].push_back(u);
    }

    unordered_map<ll, int> counts;
    counts[targetSum] = 1; ll ans = 0;

    if (N > 0) {
        dfs(1, 0, 0);
    }

    cout << ans << endl;
}
```

## 相乘结果为正为负的子数组数量

[题目链接](https://codeforces.com/problemset/problem/1215/B)

### Problem Statement

给定一个长度为 $N$ 的整数序列 $a$ ，其中所有元素都 **不等于 0** 。

你需要计算以下两个值：

1. 满足 $l \leq r$ 的下标对 $(l, r)$ 的数量，使得 $a_l \cdot a_{l+1} \cdots a_r$ 的乘积为 **负数** 。
2. 满足 $l \leq r$ 的下标对 $(l,r)$ 的数量，使得 $a_l \cdot a_{l+1} \cdots a_r$ 的乘积为 **正数** 。

换句话说，你需要统计：

- 所有 **子数组乘积为负数** 的数量
- 所有 **子数组乘积为正数** 的数量

### Constraints

- $1 \leq N \leq 2 \times 10^5$
- $-10^9 \leq a_i \leq 10^9$
- $a_i \neq 0$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组长度。
- 第二行包含 $N$ 个整数，表示数组元素。

> $N$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_N$

### Output

输出两个整数，分别表示乘积为负数的子数组和乘积为正数的子数组的数量。

### Sample Input 1

```txt showLineNumbers=false
5
5 -3 3 -1 1
```

### Sample Output 1

```txt showLineNumbers=false
8 7
```

### Sample Input 2

```txt showLineNumbers=false
10
4 2 -4 3 1 2 -4 3 2 3
```

### Sample Output 2

```txt showLineNumbers=false
28 27
```

## 题目要点解析

这道题要求统计所有子数组中 **乘积为正数** 和 **乘积为负数** 的数量。由于数组中不存在 $0$ ，子子数组乘积的最终符号完全取决于该区间内 **负数的个数的奇偶性**：如果负数个数为偶数，则乘积为正；如果负数个数为奇数，则乘积为负。因此本题的核心并不在于真正计算乘积，而是判断区间内负数个数的奇偶性。

为了简化问题，我们可以直接对原数组进行状态映射：将所有负数记为 $1$ ，所有正数记为 $0$ 。此时，问题便直接转化为在一个仅由 $0$ 和 $1$ 构成的序列中，统计所有子数组中 $1$ 的个数为奇数或偶数的区间数量。

在这种表示方法下，我们可以非常自然地引入 **前缀异或和** 。设 $pre_i$ 表示前 $i$ 个元素中 $1$ 的个数的奇偶性（即这些元素的前缀异或结果）。根据异或的性质，任意区间 $[l,r]$ 中 $1$ 的个数的奇偶性可以表示为：

$$
pre_r \oplus pre_{l-1}
$$

若结果为 $0$ ，说明该区间负数个数为偶数，对应子数组乘积为正；若结果为 $1$ ，说明该区间负数个数为奇数，对应子数组乘积为负。这样一来，我们便可直接沿用[和为K的子数组](#和为k的子数组)的解题框架进行求解。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 翻转以聚类问题

[题目链接](https://atcoder.jp/contests/abc408/tasks/abc408_d)

### Problem Statement

给定一个长度为 $N$ 的字符串 $S$ ，字符串仅由字符 `'0'` 和 `'1'` 组成。

你可以进行任意次（包括 $0$ 次）如下操作：

- 选择一个位置 $i$（ $1 \leq i \leq N$ ），将 $S_i$ 翻转（即 `'0'` 变为 `'1'`，或 `'1'` 变为 `'0'`）

你的目标是使字符串中 **所有的 `'1'` 至多形成一个连续区间** 。

换句话说，最终字符串需要满足以下条件之一：

- 字符串中没有 `'1'`（全为 `'0'` ），或
- 存在一段区间 $[l, r)$ ，使得：

  - 当且仅当 $l \leq i < r$ 时，$S_i = '1'$
  - 其它位置均为 `'0'`

请你求出，为了满足上述条件，**最少需要进行多少次翻转操作** 。

### Constraints

- $1 \leq T \leq 2 \times 10^5$
- $1 \leq N \leq 2 \times 10^5$
- $S$ 是一个仅由 `'0'` 和 `'1'` 组成的字符串
- 所有测试用例中 $N$ 的总和不超过 $2 \times 10^5$

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

  - 第一行包含一个整数 $N$ ，表示字符串长度。
  - 第二行包含一个长度为 $N$ 的字符串 $S$ 。

> $N$
> 
> $S$

### Output

对于每个测试用例，输出一行一个整数，表示最少需要的翻转次数。

### Sample Input

```txt showLineNumbers=false
3
5
10011
10
1111111111
7
0000000
```

### Sample Output

```txt showLineNumbers=false
1
0
0
```

## 题目要点解析

这道题可以简单地理解为一个区间选择问题。由于最终状态要求所有的 `'1'` 至多形成一个连续区间，因此我们可以假设答案对应于某个区间 $[l, r]$：该区间内的字符全部为 `'1'` ，区间外的字符全部为 `'0'` 。在这种视角下，我们不再关心翻转的顺序，而是将目光聚焦于为了达成目标状态所需修改的字符总数。

在区间 $[l, r]$ 内，所有原本为 `'0'` 的字符都必须被翻转成 `'1'` ；而在区间外，所有原本为 `'1'` 的字符都必须被翻转成 `'0'` 。因此，翻转次数可以自然地拆分为这两部分之和。为了高效计算任意区间的代价，我们引入前缀和数组，其中 `pre0[i]` 表示前 $i$ 个字符中 `'0'` 的数量，`pre1[i]` 表示前 $i$ 个字符中 `'1'` 的数量。

当区间选为 $[l, r]$ 时，总的翻转次数可以表示为：

$$
pre0[r] - pre0[l - 1] + pre1[l - 1] + pre1[n] - pre1[r]
$$

对该式进行整理，可以将其拆解为一项只与右端点 $r$ 有关的部分，以及一项只与左端点 $l$ 有关的部分：

$$
\big(pre0[r] + pre1[n] - pre1[r]\big) + \big(pre1[l - 1] - pre0[l - 1] \big)
$$

这个拆分操作非常关键，它使得问题可以利用两数之和思想来处理。当右端点 $r$ 固定时，前半部分相当于一个常数，此时要做的就是在所有满足 $l \leq r$ 的左端点中，找到 $pre1[l - 1] - pre0[l - 1]$ 最大的位置。因此在单次扫描过程中，只需实时维护该表达式的历史最大值，即可在 $O(1)$ 时间内锁定当前 $r$ 对应的最小代价。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
int n; string s;

int main(){
    int T; cin >> T;
    while (T--){
        cin >> n >> s;
        vector<int> pre0(n + 1, 0), pre1(n + 1, 0);
        for (int i = 1; i <= n; i++){
            pre0[i] = pre0[i - 1];
            pre1[i] = pre1[i - 1];
            if (s[i - 1] == '0') pre0[i]++;
            else pre1[i]++;
        }

        int ans = INT_MAX, best = 0;
        for (int r = 1; r <= n; r++){
            int cur = pre0[r] + pre1[n] - pre1[r];
            ans = min(ans, cur + best);
            best = max(best, pre1[r] - pre0[r]);
        }

        cout << ans << '\n';
    }
}
```

---

# 树上点配对类型题

**树上点配对问题** 的核心在于统计满足特定约束的点对，其难点通常体现在如何高效处理 **跨子树的点对关系** 。为了解决此类问题，我们可以借用两数之和的思路：在遍历树的过程中，动态维护一个记录已遍历节点信息的结构。当枚举到新子树的节点时，我们只需利用该结构检索待匹配点的信息，即可完成跨子树的点对统计。

在实际的代码实现中，通常需要给每个节点或者子树都分配一个 **独立的数据结构** ，这意味着在子树信息向上传递的过程中，必然伴随着 **数据结构的合并** 。然而这种合并的开销与子树规模相关，在面对特殊的树形结构时极易导致时间复杂度的退化。为了打破这种由特殊树形结构带来的效率瓶颈，我们需要引入特定的优化策略。

其中一种优化策略是[树上点分治算法](https://xingguang641.com/posts/acm/acm-type/graph-problems/tree-algorithms/tree-algorithms/#树上点分治问题)，它直接打破了依赖父子回溯的递归框架，通过不断拆解树的重心，将递归分治树的高度严格限制在 $\log n$ 级别，从而保证了整体时间复杂度绝不会因为特殊的树形结构导致退化。另一种优化策略是[树上启发式合并](https://xingguang641.com/posts/acm/acm-type/graph-problems/tree-algorithms/tree-algorithms/#树上启发式合并)，它在合并子树时不再盲目地将所有子节点的数据结构合并至父节点，而是将规模最大的重儿子结构直接传递给父节点，尽可能保留先前合并的结果，从而降低合并带来的性能损耗。

### 树上路径问题的解题技巧

**树上路径问题** 也可以类比为树上点配对问题：由于树中的两点一旦确定，连接这两点的路径也唯一确定，统计路径 **本质就是统计点对** 。在递归过程中，可以通过数据结构维护已遍历节点的信息，来获取符合要求的路径信息。

对于 **统计长度恰好为 K 的路径个数** 问题，我们则需要借助最低公共祖先来辅助信息的维护。在树上，连接两点的路径必然在其最低公共祖先发生转折，其对应的路径长度必然满足：

$$
dep[u] + dep[v] - 2 \cdot dep[lca] = k
$$

对该式进行整理，将 $u$ 相关的部分单独留在一边，可以得到：

$$
dep[u] = k + 2 \cdot dep[lca] - dep[v]
$$

借助这个等式，我们只需要通过查询 $k + 2 \cdot dep[lca] - dep[i]$ 并记录 $dep[i]$ 的方式，即可在递归过程中统计出所有跨越不同子树的合法点对。需要注意的是，这里的查询与记录对象不能交换。由于 $dep[lca]$ 是一个变量，如果将包含它的表达式存入数据结构，后续就无法再进行修改，因此我们只能选择存储静态的 $dep[i]$ 。

对于 **统计长度不超过 K 的路径个数** 问题，其核心约束如下：

$$
dep[u] + dep[v] - 2 \cdot dep[lca] \leq k
$$

对该式进行整理，将 $u$ 相关的部分单独留在一边，可以得到：

$$
dep[u] \leq k + 2 \cdot dep[lca] - dep[v]
$$

从这个不等式可以看出，原本的精准匹配问题转化为了值域的前缀查询问题。在递归过程中，我们需要借助树状数组或线段树等支持前缀查询的数据结构来维护节点信息。在枚举新子树节点 $v$ 时，只需在数据结构中查询已遍历节点中满足深度不超过 $k + 2 \cdot dep[lca] - dep[v]$ 的节点个数，即可统计出所有跨越不同子树的合法点对。

## 北斗玄阵交感力

[题目链接](https://www.matiji.net/exam/brushquestion/77/4693/305EE97B0D5E361DE6A28CD18C929AF0)

### Problem Statement

给定一棵包含 $n$ 个节点的树，节点编号为 $1 \sim n$ ，其中编号为 $1$ 的节点是根节点，每个节点都有一个数值 $a_i$ 。

定义 $lca(x, y)$ 为节点 $x$ 和 $y$ 的最近公共祖先，$pop(x)$ 为整数 $x$ 在二进制表示下 $1$ 的数量。

请计算以下表达式的值（结果对 $10^9 + 7$ 取模）：

$$
\left( \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} (a_i + a_j)^{pop(a_{lca})} \right) \pmod{10^9 + 7}
$$

### Constraints

- $1 \leq n \leq 3 \times 10^5$
- $1 \leq a_i \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示这棵树的节点个数。
- 第二行包含 $n$ 个整数，表示这颗树上每个节点拥有的数值 $a_i$ 。
- 接下来 $n-1$ 行，每行包含两个整数 $x$ 和 $y$ ，表示 $x$ 和 $y$ 节点有一条边。

> $n$
> 
> $a_1 \quad a_2 \quad \ldots \quad a_n$
> 
> $x_1 \quad y_1$
> 
> $\ldots$
> 
> $x_{n-1} \quad y_{n-1}$

### Output

输出一个整数表示计算结果。

### Sample Input

```txt showLineNumbers=false
7
2 33 4 7 1 66 7
1 2
1 3
1 4
3 5
3 6
4 7
```

### Sample Output

```txt showLineNumbers=false
3450
```

## 题目要点解析

这道题最直观的做法是枚举每个节点作为最低公共祖先来统计其贡献，但整个问题的难点在于如何高效处理公式中的高次幂。若直接对子树内的点对进行双重循环枚举，时间复杂度将达到 $O(N^2)$ ，在题目给定的数据范围内无法通过。因此我们需要利用和式变换的思想，将互相耦合的 $i$ 和 $j$ 在逻辑上实现解耦。

为了打破指数带来的组合限制，最经典的数学优化手段就是引入 **二项式展开** 。如果我们令 $P_x = pop(a_x)$ ，那么对于以 $x$ 为最近公共祖先的任意两个节点 $i$ 和 $j$ ，其权值的高次幂项可以展开为：

$$
(a_i + a_j)^{P_x} = \sum_{k=0}^{P_x} \binom{P_x}{k} \cdot a_i^k \cdot a_j^{P_x-k}
$$

将展开式代入原本的双重求和公式，并通过 **交换求和次序** ，可以得到：

$$
\sum_{i \in T_x} \sum_{j \in Sub_v} \sum_{k=0}^{P_x} \binom{P_x}{k} a_i^k a_j^{P_x-k} = \sum_{k=0}^{P_x} \binom{P_x}{k} \left( \sum_{i \in T_x} \sum_{j \in Sub_v} a_i^k a_j^{P_x-k} \right)
$$

此时利用 **乘法分配律** ，我们可以将复杂的点对枚举转化为两个独立集的乘积：

$$
\sum_{k=0}^{P_x} \binom{P_x}{k} \left( \sum_{i \in T_x} a_i^k \right) \left( \sum_{j \in Sub_v} a_j^{P_x-k} \right)
$$

在具体实现时，我们可以借用两数之和思想：对于每个节点 $x$ ，维护其子树内所有权值的 $k$ 次幂之和 $f(x, k)$ 。利用当前已合并集合 $T_x$ 的累积信息，可以在 $O(P_x)$ 的时间内完成新子树 $Sub_v$ 的贡献统计：

$$
\Delta Ans = \sum_{k=0}^{P_x} \binom{P_x}{k} \cdot f(T_x, k) \cdot f(Sub_v, P_x-k)
$$

在 $Sub_v$ 的贡献统计完成后，我们再将其信息合并到 $T_x$ 中。通过这种子树合并的方式，我们成功将原本复杂的跨越不同子树的合法点对计数问题，转化为各子树的信息合并问题。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```