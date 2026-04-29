---
title: 【ACM 算法随笔】两数之和思想
published: 2025-11-23
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

> 写在前面：本篇博客写作灵感来源于灵神的两数之和理解

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=305008442&bvid=BV1bP411c7oJ&cid=888954096&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 两数之和题目讲解

两数之和是 LeetCode 上编号为 $1$ 的开山题目，常被称作算法题中的 `Hello World!` 。它表面看起来十分基础，却并不只停留在新手练习的层面。之所以值得专门展开讨论，是因为 **“两数之和” 背后所蕴含的思想具有极强的泛用性** ，并且贯穿于大量经典算法问题之中，衍生出多种重要的技巧与模型。许多题目你也许早已独立做过，却未必意识到它们之间存在着紧密而统一的内在逻辑。

接下来，我们将以 “两数之和” 这一核心问题为主线，逐步串联起一系列相关题型与解题思路。希望通过这样的梳理，能够帮助我们跳脱出单个题目的视角，对那些看似零散却本质相通的问题形成更加 **系统化、结构化的认识** ，从而建立更稳固的解题框架。

## 两数之和母题

[题目链接](https://leetcode.cn/problems/two-sum/description/)

### Problem Statement

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 **和为目标值** target 的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

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

由于这个题目本身难度较低，我们不妨在它的基础上稍作扩展。具体来说，我们将原题中 “只存在一个有效答案” 的限制移除，允许出现 **多个不同的数对** 和为 target，并要求我们统计所有满足条件的数对数量。为了统计所有满足条件的数对数量，我们可以先思考一个直观的解法：对于数组中每个元素，都去查找它左侧部分中是否存在与之配对的目标值。这样可以枚举所有可能的配对关系，但时间复杂度会达到 $O(n^2)$ 。

不过我们可以换一个视角：从左到右遍历数组，那么在访问当前元素之前，它左侧的所有信息都已知。如果我们能够在遍历过程中 **实时记录已经出现过的数字及其出现次数** ，那么对于当前元素，我们只需花费 $O(1)$ 的时间查询其 “配对目标” 是否已经出现过，并累加数量即可。这样一来，总体的时间复杂度便能从 $O(n^2)$ 优化到 **线性复杂度 $O(n)$** ，实现更高效的求解。

首先，我们明确题目所要求的条件：

$$
nums[i] + nums[j] = target
$$

然后我们将关于 $j$ 的部分移动到等式另一侧，可以得到：

$$
nums[i] = target - nums[j]
$$

当我们遍历数组时，如果能够实时记录已经出现过的数字 $nums[j]$ 的出现次数，那么对于当前数字 $nums[i]$ ，只需要查询它所对应的配对值 $target - nums[i]$ 之前出现了多少次，就能直接得出以 $i$ 为右端点所贡献的有效数对数量。我们可以得到如下的算法流程：

- **查询（Query）**：在哈希表中查找是否存在键为 $target - nums[i]$ 的记录，若存在则累计答案。
- **记录（Update）**：将当前数字 $nums[i]$ 更新到哈希表中（出现次数 + 1 ），作为后续数字的配对目标。

同理，我们也可以查询 $nums[i]$ ，记录 $target - nums[i]$ 。

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

核心代码还可以改成下面这样，效果是差不多的：

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

# 多元组序列问题

在掌握 “两数之和” 的解法后，我们实际上已经触及了序列处理的核心逻辑：如何在看似杂乱的线性序列中，高效统计满足特定约束的多元素子序列。这类问题统称为 **多元组序列问题** 。无论是统计三元组还是探寻更高维的组合，它们在算法底层并非孤立存在，而是 “两数之和” 思想向高维空间的自然延伸。

当我们将视野从两元扩展至三元组（满足 $i < j < k$ 的 $A_i, A_j, A_k$ ）时，**降维思想** 展现出了极强的普适性。如果我们固定最右侧端点 $k$ ，原问题便瞬间退化为：在动态变化的区间 $[0, k-1]$ 中寻找满足特定条件的二元组。这意味着，复杂的三元组统计并非全新的课题，而是建立在 “两数之和” 基础之上的嵌套结构。随着外层枚举的单向推进，内层始终维持着一个标准的、可随步进实时维护的低维系统。

除了固定右端点，我们还可以切换至 **中心枚举** 的视角重新审视，并引入 **idx 数组** 来辅组枚举。这里的 $idx$ 数组存储的是元素下标，并按照对应元素的大小进行排序。它让我们在不破坏元素原始位置信息的前提下，获得了一套按数值排列的索引映射。然后我们依次枚举 $idx$ 中的元素作为中心点 $j$ ，并将之前处理过的 $idx$ 进行分拣：早于 $j$ 的放入左侧候选集，晚于 $j$ 的放入右侧候选集。由于这个过程是按数值大小推进的，左右两个集合提取出的元素天然有序，从而将棘手的偏序匹配转化为两个有序序列间的线性扫描。

## 三数之和问题

[题目链接](https://leetcode.cn/problems/3sum-with-multiplicity/description/)

### Problem Statement

给定一个整数数组 `arr` ，以及一个整数 `target` 作为目标值，返回满足 `i < j < k` 且 `arr[i] + arr[j] + arr[k] == target` 的元组 `i, j, k` 的数量。

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

### Sample Input 1

```txt showLineNumbers=false
10 8
1 1 2 2 3 3 4 4 5 5
```

### Sample Output 1

```txt showLineNumbers=false
20
```

## 题目要点解析

三数之和的做法并不复杂，我们可以先固定第三个下标 $k$ ，把它当作当前三元组的右端点，然后只考虑区间 $[0, k-1]$ 中的元素。在 $k$ 已经确定的情况下，问题就变成了：在前缀区间中寻找一对下标 $i < j$ ，使得它们对应的两个数与 $arr[k]$ 之和等于目标值。也就是说，每固定一个 $k$ ，就在它左侧跑一次两数之和。

原问题中关于数值的约束可以写为：

$$
arr[i] + arr[j] + arr[k] = target
$$

将与 $k$ 相关的项移到等式右侧，就得到：

$$
arr[i] + arr[j] = target - arr[k]
$$

此时，问题就完全转化为一个标准的 **两数之和计数问题**：在前缀区间 $[0, k-1]$ 中，统计有多少对下标满足 $i < j$ 且对应的元素之和等于 $target - arr[k]$ 。因此，只要我们能够在遍历过程中维护左侧区间中各个数值的出现次数，就可以在常数时间内计算出当前 $k$ 所贡献的有效三元组数量。

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

## 统计好三元组

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

针对这道题，最直观的策略是直接根据题目定义的三个绝对值约束进行 **三重循环枚举** 。在 $N \leq 100$ 的数据规模下，$O(N^3)$ 的复杂度足以通过评测。然而，这个问题的核心价值在于其优化思路的启发性：如何通过固定特定端点，将三维相互耦合的约束转化为一维或二维的动态维护问题，是打破计算瓶颈的关键。

第一种优化思路借鉴了 **三数之和** 中固定右端点的策略。我们尝试固定右端点 $k$ ，并在中间点 $j$ 从 $0$ 向 $k-1$ 顺序移动的过程中实现高效统计。为了自动地满足多重约束，我们引入一个 **动态维护的频率数组** 来记录历史状态。其逻辑遵循严密的先后顺序：当 $j$ 满足约束 $|arr[j] - arr[k]| \leq b$ 时，立即发起一次针对左侧合法 $i$ 的查询；查询完成后，若 $arr[j]$ 满足约束 $|arr[j] - arr[k]| \leq c$ ，则将其存入频率数组中。

这种设计的巧妙之处在于，查询动作发生在当前元素入库之前，从而天然满足了下标 $i < j < k$ 的序关系。为了实现 $O(1)$ 的区间检索，我们利用前缀和数组 `pre` 维护当前桶中 $\leq \text{num}$ 的元素个数。此时，第一个不等式约束 $|arr[i] - arr[j]| \leq a$ 转化为值域区间 $[arr[j]-a, arr[j]+a]$ 的计数问题，通过 `pre[r] - pre[l-1]` 即可快速获取答案。这种方法将复杂度优化至 $O(N^2 + N \cdot \text{maxVal})$ ，在值域较小的场景下表现卓越。

```cpp frame="code" title="solution_1.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

尽管前面的做法非常巧妙，但没办法处理值域较大的情况，因此我们要换一个思路。绝对值问题的核心难点在于数据的无序性，但由于本题下标顺序与数值大小相互制约，我们无法直接对原数组排序。为此，我们构建一个下标数组 `idx` 并按照其在原数组 `arr` 中的数值进行升序排列。当我们依次枚举 `idx` 中的每一个元素作为三元组的中间点 $j$ 时，可以将数值比当前 $arr[j]$ 更小的历史元素（即在排序数组中排在 $j$ 之前的元素）进行 **动态分组** 。

在这一步中，我们只需将这些已经遍历过的、数值较小的元素，根据它们在原数组中的原始位置分配到 **left** 或 **right** 两个集合中。具体而言，只有原始下标 $idx[p] < j$ 且满足 $arr[j] - arr[idx[p]] \leq a$ 的元素才会被放入 left 集合，以此作为合法的 $i$ 候选；同理，只有原始下标 $idx[p] > j$ 且满足 $arr[j] - arr[idx[p]] \leq b$ 的元素才会被放入 right 集合，作为合法的 $k$ 候选。

由于我们是按照 `idx` 的升序逻辑进行遍历的，每次提取出的历史元素本身就遵循从小到大的排列，因此生成的 **left** 和 **right** 集合 **天然满足有序性** 。此时，三元组的构建就转化为了一个典型的有序数组跨集合匹配问题，即处理 $i$ 与 $k$ 之间的最后一道约束 $|arr[i] - arr[k]| \leq c$ 。我们只需枚举 **left** 中的每个元素 $x$ ，并在 **right** 中寻找落在区间 $[x-c, x+c]$ 内的元素。利用 **三指针技巧** 维护两个在 **right** 上单调滑动的边界，即可在摆脱值域依赖的前提下，以 $O(N^2)$ 的复杂度完成所有配对统计。

```cpp frame="code" title="solution_2.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

## 有效三角形数

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



---

# 数组子段和问题

在处理数组子段和问题时，一个最核心且具有普适性的观察在于，如果我们预先定义数组的前缀和序列为 pre，那么原数组中任意一段连续子数组的和 $[left,right]$ 都可以通过两个前缀项的差值来精确表达：

$$
pre[right] - pre[left] = sum[left: right]
$$

也就是说，一个子段的和本质上等价于 **两个前缀和之间的差值** 。当我们从这个角度重新观察问题时，就会发现很多原本看起来复杂的子数组问题，其实都可以转化为 **寻找满足某种关系的两个前缀值** 。换句话说，我们并不需要直接枚举整个子数组，而是只需要关注 **前缀之间的关系** 。

这样一来，数组子段和就转化为经典的 **两数之和问题** 。当我们枚举右端点 $right$ 时，实际上就是固定了一个前缀值 $pre[right]$ ，此时问题往往转化为：**是否存在某个左端点 left，使得 $pre[left]$ 与当前前缀值满足某种条件** 。根据题目的不同限制，我们可以用多种方式来维护这些可能的前缀值，例如使用 **哈希表统计出现次数、双指针维护区间、或借助有序结构进行查询** 等。

因此，从建模角度来看，很多所谓的 **数组子段和问题** ，本质上都可以理解为一种 **前缀和上的两数关系问题** 。当我们意识到这一点之后，许多看似不同的题目其实都可以用类似的思路来处理：枚举一侧端点，并在另一侧维护可能的前缀值集合。接下来我们就通过几个具体例子，来进一步体会这种转化在实际题目中的应用方式。

## 累加和为定值的最长子数组长度

[题目链接](https://www.nowcoder.com/practice/36fb0fd3c656480c92b569258a1223d5)

### Problem Statement

给定一个无序数组 $arr$ ，其中元素是在一定范围内的任意整数。给定一个整数 $k$ ，求 $arr$ 所有子数组中累加和为 $k$ 的最长子数组长度。

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

借鉴 “两数之和” 的核心思路，我们依然把子数组和的问题转化为前缀和差值。设 $pre[i]$ 表示前 $i$ 个元素的前缀和，则任意区间满足子数组和为 $k$ 的条件可以写成：

$$
pre[right] - pre[left] = k \qquad (left \leq right)
$$

与 “两数之和” 不同的一点在于，这里的运算是减法，它不具备 **交换律** 。因此我们不能像那道题一样随意决定 “存什么” 和 “查什么” ，必须严格按照移项后的形式来设计具体的存储和查找逻辑。基于这个形式，有两种完全对称、但实现细节不同的写法。

### 思路一：查历史存当前

从原式移项得到：

$$
pre[right] - k = pre[left]
$$

当我们遍历到位置 right 时，我们需要在哈希表中 **查找过去是否出现** 值为 $pre[right]-k$ 的前缀和；然后再把当前前缀和 $pre[right]$ 记录到哈希表中，作为后续位置的查询依据。

由于我们存的是 **真实前缀和** ，在正式开始遍历前，前缀和为 $0$ ，因此必须初始化：

```cpp showLineNumbers
pos[0] = -1
```

### 思路二：查当前存期望

把式子换另一种移项方式：

$$
pre[right] = pre[left] + k
$$

当我们遍历到位置 right 时，我们需要在哈希表中 **查询过去是否需要** 值为 $pre[right]$ 的前缀和；接着再把未来的期望值 $pre[right] + k$ 存入哈希表，表示该元素希望遇到这个数来凑成区间和 $k$ 。

由于此时存的是 **期望值** ，初始前缀和为 $0$ ，它期待未来遇到值为 $k$ 的前缀和，因此初始化为：

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

## 和为 K 的子数组

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

针对这道子数组求和问题，核心在于利用 **前缀和** 将连续区间的求和转化为两个端点值的差值。通过引入前缀和序列 $pre$ ，题目要求的子数组和 $k$ 便等价替换为 $pre[j] - pre[i-1] = k$ 。这种转化成功地将一个需要枚举区间的 $O(N^2)$ 问题，降维成了一个寻找特定数值匹配的二元组问题，在底层逻辑上与 “两数之和” 达成了高度统一。

在实现过程中，我们利用哈希表动态维护已经扫描过的前缀和及其出现频率。由于目标是寻找满足 $pre[i-1] = pre[j] - k$ 的历史状态，我们只需在遍历时随走随查、随查随储。需要特别注意的是，哈希表的初始状态应包含 `counts[0] = 1` ，这代表了前缀和恰好等于 $k$ 、即从数组起始位置开始的合法子数组。通过这种空间换时间的策略，我们能以 $O(N)$ 的复杂度优雅地统计出所有答案。

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

### Sample Input 1

```txt showLineNumbers=false
5
1 -2 1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
2
```

## 题目要点解析

首先观察题目，会发现题目中出现了 **“一样多”** 这个关键字。对于这种类型的问题，我们常用的技巧是将数据 **二值化** ，并通过累加和为 $0$ 来表示数量相等。这个技巧非常实用，在后续的题目中会经常用到。

具体做法是：将正整数看作 $1$ ，将负数看作 $-1$ ，然后寻找 **累加和为 0 的最长子数组** 。需要注意的是，原数组中可能存在 $0$ ，但我们可以直接忽略，不要在转换时把等于号也加入判断（尤其注意 `if else` 语句），否则会导致错误。这样处理后，我们就可以直接套用之前讲的 **“累加和为定值的最长子数组长度”** 的代码框架来解决问题。

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

同样地，我们将大于 $8$ 的数值映射为 $1$ ，小于等于 $8$ 的数值映射为 $-1$ 。此时，问题转化为寻找 **元素和大于 0 的最长子数组** 。引入前缀和数组 $pre$ ，子数组和大于 $0$ 等价于 $pre[left] < pre[right]$ 。

> **形式化描述**
>
> 在前缀和数组中，寻找一对索引 $(left, right)$ ，在满足 $left < right$ 且 $pre[left] < pre[right]$ 的前提下，使 $right - left$ 最大。这实际上是一个经典的 **单调栈问题** ，我们需要为每一个 $right$ 找到其左侧 **距离最远** 且 **数值更小** 的下标 $left$ ，然后计算差值，再在这些差值中寻找最大值。

这道题还有一个可以利用的特殊性质：数组中的数字只有 ±1 ，因此前缀和变化为 $1$ ，满足 **单调连续性** 。利用这一性质，我们可以进一步简化算法。对于当前位置 $i$ ，若 $pre[i] > 0$ ，说明从数组起始位置到当前位置的整体和为正，此时可以直接得到最长长度为 $i + 1$ 。若 $pre[i] \leq 0$ ，则需要在其左侧寻找一个位置 $left$ ，使得 $pre[left] < pre[i]$ ，从而最大化区间长度 $i - left$ 。关键在于如何高效地确定这个 $left$ 。

根据前缀和的单调连续性，前缀和从 $0$ 下降到 $pre[i]$（例如 $-5$ ）的过程中，**必然会在更早的位置** 先变化为 $pre[i] + 1$（例如 $-4$ ）。也就是说，$pre[i] - 1$ 首次出现的位置一定早于 $pre[i] - 2$ 、$pre[i] - 3$ 等更小数值首次出现的位置。因此，为了使区间长度最大，我们只需关注 $pre[i] - 1$ 首次出现的位置，无需枚举所有小于 $pre[i]$ 的前缀和值。

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

如果将 **“寻找最长子数组”** 的条件改为 **“统计目标子数组个数”** ，我们又该如何处理呢？同样地，我们先不考虑这道题的特殊性，直接给出这道题的一般形式。

> **形式化描述**
>
> 在前缀和数组中，统计有多少对 $(left, right)$ 满足 $left < right$ 且 $pre[left] < pre[right]$（每个数对都是一个子数组，因此统计数对个数即可得到子数组个数）。这实际上就是 **顺序对问题** ，因此可以直接使用 **归并分治** 来解决这个问题。

现在我们考虑如何利用 **单调连续性**：由于前缀和的变化每次仅 ±1 ，当遍历到某个下标时，我们只需要知道 **小于当前 $pre[i]$ 的前缀个数** 即可统计顺序对数量。基于这个特点，可以使用 **增量法** 动态维护前缀信息。

当 $pre$ 增加 $1$ 时，由于之前已统计了所有小于 $pre$ 的前缀个数，只需加上等于 $pre$ 的前缀数量即可；当 $pre$ 减少 $1$ 时，由于之前已统计了所有小于 $pre$ 的前缀个数，只需舍弃等于 $pre - 1$ 的前缀数量即可。由于前缀和变化的步长恒为 1，因此动态维护 **小于当前 $pre[i]$ 的前缀个数** 非常高效，只需统计每种前缀值出现的次数，即可在 $O(1)$ 时间完成更新。

## 构造 P 整除数组

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

首先这道题有一个很明显的点：如果整个数组的和模 $p$ 余 $0$ ，那我们不需要移除任何数。如果整个数组的和模 $p$ 余 $r$ ，那我们就要找到累加和（取模后）为 $r$ 的最短子数组。

因此我们可以得到下面这个条件：

$$
pre[right] - pre[left] \equiv r \pmod{p}
$$

根据两数之和的思想，我们将 $left$ 移至右侧可得：

$$
pre[right] \equiv r + pre[left] \pmod{p}
$$

因此我们要查询 $pre[i] \% p$ 的同时，统计 $(r + pre[i]) \% p$ 出现的最早位置。从 “两数之和” 的角度来看，这道题的标准写法其实很自然，虽然涉及取模运算，看似有些奇怪，但背后的数学思想非常直观。

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

给定一个二叉树的根节点 `root` ，和一个整数 `targetSum` ，求该二叉树里节点值之和等于 `targetSum` 的 **路径** 的数目。

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

### Sample Input 1

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

### Sample Output 1

```txt showLineNumbers=false
3
```

## 题目要点解析

这是一道典型的 “树上向下路径统计” 问题。由于路径只能从父节点走向子节点，因此在 DFS 过程中，当前递归栈上从根到当前节点形成的一条链，本质上就是一条一维序列。问题可以理解为：在这条动态路径中，寻找若干对位置，使得两者对应的路径和之差等于 `targetSum` 。

设当前遍历到节点 $u$ 时，从根到 $u$ 的路径和为 `curSum` 。若存在某个祖先节点，其对应的路径和为 `x` ，满足：

$$
curSum - x = targetSum
$$

那么从该祖先之后到当前节点这一段路径就是一个合法解。因此，在 DFS 过程中维护一个哈希表，记录当前路径上每个路径和出现的次数。访问当前节点时，先计算新的 `curSum` ，然后查询 `curSum - targetSum` 在哈希表中出现了多少次，并将其累加到答案中。随后将当前 `curSum` 计入哈希表，继续递归访问子树。递归返回父节点时，将当前 `curSum` 的出现次数减一，以完成回溯，确保哈希表中始终只保存当前递归路径上的信息。

整棵树只需一次 DFS，每个节点进行常数次哈希查询与更新，时间复杂度为 $O(N)$ ，空间复杂度为 $O(N)$ 。从结构上看，这类问题的关键在于路径方向单调，使得整棵树在遍历过程中始终可以被压缩成一条动态路径，从而把问题转化为路径上的 “两数之和” 在线匹配问题。这种转化方式在树上路径计数类问题中具有很强的普适性。

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

- 第一行是一个整数 $T$ ，表示测试用例的数量。
- 对于每个测试用例：

  - 第一行是一个整数 $N$ ，表示字符串长度。
  - 第二行是一个长度为 $N$ 的字符串 $S$ 。

> $T$
> 
> $N_1$
> 
> $S_1$
> 
> $N_2$
> 
> $S_2$
> 
> $\ldots$
> 
> $N_T$
> 
> $S_T$

### Output

对于每个测试用例，输出一行一个整数，表示最少需要的翻转次数。

### Sample Input 1

```txt showLineNumbers=false
3
5
10011
10
1111111111
7
0000000
```

### Sample Output 1

```txt showLineNumbers=false
1
0
0
```

## 题目要点解析

这道题可以等价地理解为一个区间选择问题。由于最终状态要求所有的 `'1'` 至多形成一个连续区间，因此我们可以假设答案对应于某个区间 $[l, r]$：该区间内的字符全部为 `'1'` ，区间外的字符全部为 `'0'` 。在这种视角下，我们不再关心翻转的顺序，而只关心为了达到这一目标状态，总共需要翻转多少个字符。

在区间 $[l, r]$ 内，所有原本为 `'0'` 的字符都必须被翻转成 `'1'` ；而在区间外，所有原本为 `'1'` 的字符都必须被翻转成 `'0'` 。因此，翻转次数可以自然地拆分为这两部分之和。为了高效计算任意区间的代价，我们引入前缀和数组，其中 `pre0[i]` 表示前 $i$ 个字符中 `'0'` 的数量，`pre1[i]` 表示前 $i$ 个字符中 `'1'` 的数量。

当区间选为 $[l, r]$ 时，总的翻转次数可以表示为：

$$
pre0[r] - pre0[l - 1] + pre1[l - 1] + pre1[n] - pre1[r]
$$

对该式进行整理，可以将其拆解为一项只与右端点 $r$ 有关的部分，以及一项只与左端点 $l$ 有关的部分：

$$
pre0[r] + pre1[n] - pre1[r] + \big(pre1[l - 1] - pre0[l - 1] \big)
$$

这一拆分形式非常关键，它使得问题可以用 “两数之和” 的方式来处理。当我们将右端点 $r$ 固定时，前半部分相当于一个常数，此时要做的就是在所有满足 $l \leq r$ 的左端点中，找出使 $pre1[l - 1] - pre0[l - 1]$ 最大的位置。因此在从左到右扫描字符串的过程中，只需要维护截至当前位置之前该表达式的最大值，就可以在 $O(1)$ 时间内计算出以当前 $r$ 作为右端点时的最小翻转代价，只需扫描一次即可完成所有区间的枚举与答案更新。

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

这道题要求统计所有子数组中 **乘积为正数** 和 **乘积为负数** 的数量。由于数组中不存在 $0$ ，子数组乘积的符号完全取决于其中 **负数的个数的奇偶性**：如果负数个数为偶数，则乘积为正；如果负数个数为奇数，则乘积为负。因此，本题的核心并不在于真正计算乘积，而是判断区间内负数个数的奇偶性。

为了简化问题，可以先对原数组进行一次符号映射：将所有正数看作 $1$ ，所有负数看作 $-1$ 。这样数组的每个元素只表示符号信息，而不再关心具体数值。接下来再进一步利用奇偶性的特点，将 $1$ 视为 $0$ ，$-1$ 视为 $1$ 。此时问题就转化为了：对于一个由 $0$ 和 $1$ 构成的序列，统计所有子数组中 **1 的个数为奇数或偶数** 的区间数量。

在这种表示方式下，可以引入 **前缀异或和** 。设 $pre_i$ 表示前 $i$ 个元素中 $1$ 的个数的奇偶性（即这些值的异或结果）。那么任意区间 $[l,r]$ 中 $1$ 的个数奇偶性可以表示为：

$$
pre_r \oplus pre_{l-1}
$$

如果结果为 $0$ ，说明区间中负数个数为偶数，乘积为正；如果结果为 $1$ ，说明区间中负数个数为奇数，乘积为负。这样一来，问题就与 **利用前缀和统计子数组性质** 的经典做法完全一致，只不过这里把加法换成了异或运算。

具体实现时，可以在遍历数组的过程中维护当前前缀异或值，同时记录此前出现过多少次 $0$ 和 $1$ 。如果当前前缀值为 $x$ ，那么与之前 **相同前缀值** 配对的区间，其异或结果为 $0$ ，对应乘积为正；而与之前 **不同前缀值** 配对的区间，其异或结果为 $1$ ，对应乘积为负。于是可以在扫描数组的同时不断累加这两类区间的数量。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 树上点配对问题

**树上点配对问题** 指的是在树上统计某些特殊的点对，其核心在于如何处理 **跨子树的交互关系** 。为了解决此类问题，我们可以借用 “两数之和” 的思路：在遍历每棵子树时，我们将已经遍历过的子树信息统计起来，当我们枚举到当前子树的节点时，通过维护信息的数据结构来查询需要的点，从而快速完成统计。这种在遍历过程中同步进行信息检索与样本入库的动态模式，通过利用 **DFS 的序关系** 巧妙地将 $O(n^2)$ 的两两匹配转化为高效的在线查找，使得原本杂乱的跨子树交互变得有序。

并且 **树上路径问题** 也可以类比为树上点配对问题，因为树上路径的端点固定，树上路径就唯一确定，因此 **统计路径本质就是在统计点对** 。在基础的路径统计中，我们经常通过两点的信息与 **LCA** 的信息共同刻画路径属性。例如，若要统计长度为 $k$ 的路径，本质上是在寻找满足 $dep[u] + dep[v] - 2 \cdot dep[LCA] = k$ 的点对。通过在递归回溯时维护哈希表计数器，我们可以高效地捕捉这些由端点定义的路径信息。

但不是所有的树上路径问题都可以这么类比。当统计条件涉及复杂的 **全局约束** 时，局部配对往往难以维持效率。一个典型的例子是统计 **长度不超过 $k$ 的路径总数** ，由于路径端点的分布极其分散且路径长度计算依赖于不同的 LCA，简单的子树合并容易导致复杂度退化。为了更高效地处理这类需要统揽全局的路径关系，我们通常需要引入[点分治算法](https://xingguang641.com/posts/acm/acm-type/dp-classification/tree-dp/#树上重心分治问题)，通过不断拆解树的重心，将全局路径拆分为经过特定重心的子问题，从而在 $O(\log n)$ 的层级内完成对全树点对的精准覆盖。

## 北斗玄阵交感力

[题目链接](https://www.matiji.net/exam/brushquestion/77/4693/305EE97B0D5E361DE6A28CD18C929AF0)

### Problem Statement

给定一棵包含 $n$ 个节点的树，节点编号为 $1 \sim n$ ，每个节点 $i$ 铭刻着一个数值 $a_i$ 。定义 $lca(x, y)$ 为节点 $x$ 和 $y$ 的最近公共祖先，$popcount(x)$ 为整数 $x$ 在二进制表示下 $1$ 的数量。请计算以下表达式的值（结果对 $10^9 + 7$ 取模）：

$$
\left( \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} (a_i + a_j)^{popcount(a_{lca(i,j)})} \right) \pmod{10^9 + 7}
$$

### Constraints

- $1 \leq n \leq 3 \times 10^5$
- $1 \leq a_i \leq 10^9$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示数组元素。
- 接下来 $n-1$ 行，每行包含两个整数 $x, y$ ，表示编号为 $x$ 和 $y$ 的星台之间有一条边。

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

输出一行一个整数，表示计算结果。

### Sample Input 1

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

### Sample Output 1

```txt showLineNumbers=false
3450
```

## 题目要点解析



---

# 参考文献列表

1. [【Luogu 博客】树上启发式合并详细介绍](https://www.luogu.com/article/7pqyu4i1)