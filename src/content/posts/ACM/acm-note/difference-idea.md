---
title: 【ACM 算法随笔】差分数组与差分思想
published: 2025-11-25
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 差分数组基本原理

差分是一种 **常用且高效** 的数组处理技巧，它的核心思想是将 **原本作用在整个区间上的更新** ，巧妙地转化成 **只在区间端点进行的局部操作** 。对一个数组构造差分数组时，我们记录的是 **相邻元素之间的变化量**：

$$
d[i] = a[i] - a[i-1]
$$

原数组可以通过对差分数组 **求前缀和** 恢复出来。差分的关键优势在于，它允许我们在 **只修改两个位置** 的前提下完成对 **整个区间** 的更新。例如，如果我们想让区间 $[l, r]$ 的所有元素都增加 $x$ ，在差分数组中仅需执行 `d[l] += x` 和 `d[r+1] -= x` 。之后在最终阶段对差分数组求前缀和，就能得到修改后的完整数组。

差分非常适用于处理 **大量区间加减操作** 的情形，因为它将每次区间更新的时间复杂度从线性的 $O(n)$ **直接降到常数级 $O(1)$** 。在算法设计中，差分常用于 **批量区间修改、构造前缀和结构、处理扫描线类问题** 等，是一种 **简洁而高效** 的基础技巧。

## 差分的狭义视角

差分可以被看作是 **离散意义下的导数** 。在连续数学中，导数刻画的是函数在某一点附近的变化率；而在离散情形下，由于无法取极限，我们便用相邻位置的差值来描述变化：

$$
d[i] = a[i] - a[i-1]
$$

它正对应了连续情形中的近似关系：

$$
f'(x) \approx f(x) - f(x-1)
$$

从这个角度看，**原数组描述的是 “状态”** ，而 **差分数组描述的是 “变化”** 。对差分数组求前缀和的过程，则相当于对离散导数进行一次“积分”，从而恢复出原函数。

也正因为这种对应关系，许多在连续数学中依赖导数与积分解决的问题，在算法中往往都能找到相应的 **差分 + 前缀和** 形式。无论是区间修改、单调性分析，还是计数函数的变化统计，其本质都可以归结为：**先对变化进行建模，再通过累积恢复结果** 。因此，几乎所有适用于前缀和的计算思路，也都可以自然地迁移到差分框架之中。

这一视角虽然简洁，却几乎涵盖了差分技巧在算法设计中的全部思想基础。

> 具体思路可以看 N 神的视频讲解

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113927966954406&bvid=BV1dCFfemEHX&cid=28173994960&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 差分的广义视角

不过，我们今天要讨论的并不仅限于常见的 **“差分数组” 这一标准技巧** 。传统差分的使用场景非常明确：**通过将区间修改转化为端点操作，再借助前缀和还原结果** 。而在竞赛题目中，我们有时也会将一些看似相关的做法统称为 **“差分思路”** 。需要注意的是，这里的 “差分” 并不是一个严格定义的算法或数据结构，而更像是一类 **经验性的建模方式** 。

在这种更广义的语境下，差分并不一定发生在数组上，而是体现在 **对条件或统计对象的处理方式** 上。竞赛中的这类 “差分技巧” 通常 **不会真的去构造差分数组** ，而是通过 **放宽原有的严格条件，再用差值恢复精确信息** 来降低问题难度。一个典型的形式是，将难以直接处理的等式条件，转化为两个更容易处理的不等式，再通过相减得到目标结果。

在这里，原本对 “恰好等于” 的精确统计，被拆解为两个 **前缀型、不等式形式的统计问题** 。这类不等式往往更容易建模或计算：它们具有单调性，适合使用前缀和、二分、扫描线、DP 或最短路等工具来处理。通过对相邻两个不等条件的结果取差，就可以恢复出原本严格的等式信息。

从本质上看，这种做法与差分数组的思想是高度一致的：**不直接处理目标本身，而是关注“变化发生的地方”** 。只不过这里的变化不再是数组元素的增减，而是 **计数、可行性或约束边界的变化** 。正是这种对 “变化” 的捕捉，使得许多原本看似难以直接下手的问题，能够被拆解为若干结构更清晰、处理成本更低的子问题。

---

# 差分构造题目收集

在算法竞赛中，我们经常会遇到这样一类问题：给定一个初始数组，允许对其中若干子区间同时进行加减操作，询问是否能够通过这些操作将原数组转换为指定的目标数组，或要求构造出满足条件的操作方案。表面上看，这类题目似乎只是围绕数组数值本身展开；但如果直接在原数组层面进行分析，往往会陷入区间叠加关系复杂、操作顺序难以理清的问题之中。

事实上，这类问题的本质并不在于数组的 “数值” ，而在于 **相邻位置之间变化是如何产生的** 。一旦引入差分数组的视角，问题就会被显著简化：对子区间 $[l,r]$ 的加减操作，在差分数组中只会体现在端点处的两个修改。因此原本看似复杂的多次区间操作，可以被统一转化为对差分数组的局部构造或约束问题。

从这个角度出发，所谓的 “数组能否被构造出来” ，实际上等价于：**是否存在一种合法的差分数组，使其在满足操作规则的前提下，通过前缀和还原后恰好得到目标数组** 。也正因如此，许多此类题目最终都会转化为对差分数组取值范围、符号分布或总和关系的分析与构造。

这一类题目往往不要求显式模拟所有操作，而是更强调对差分结构的理解与整体约束的把握。只要抓住 “区间操作对应差分端点变化” 这一核心思想，许多看似棘手的构造问题，都会变得条理清晰、逻辑可控。

## 形成目标数组

[题目链接](https://leetcode.cn/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/description/)

### Problem Statement

给你一个整数数组 `target` 和一个数组 `initial` ，`initial` 数组与 `target` 数组有同样的大小，且一开始全部为 $0$ 。

一次操作中，你可以从 `initial` 数组中选择 任何 子数组，并将每个值加 $1$ 。

返回从 `initial` 数组构造 `target` 数组的最少操作次数。

答案保证在 $32$ 位整数以内。

### Constraints

- $1 \leq target.length \leq 10^5$
- $1 \leq target[i] \leq 10^5$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ 。其中 $N$ 表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $target_1 \quad target_2 \quad \ldots \quad target_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
5
1 2 3 2 1
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
4
3 1 1 2
```

### Sample Output 2

```txt showLineNumbers=false
7
```

## 题目要点解析



---

# 多重差分题目收集

在最基础的差分模型中，我们通常处理的是：对一个区间内的所有元素 **同时累加同一个常数** 。这类操作对应到差分数组中，只需要在区间端点进行两次修改，因而结构非常清晰。然而，在实际竞赛题目中，区间内被累加的数值并不总是一个常数，而是 **按照某种规则变化的数列** 。

当区间内的增量具有固定规律（例如等差、等比，或由某个低阶函数决定）时，依然可以借助差分思想进行处理。这类技巧通常被称为 **多重差分**：通过对数组进行不止一次差分，将原本复杂的区间变化，转化为更高层次上的 “常数区间修改” 。

其核心思想在于：**每做一次差分，就会降低一次区间更新函数的复杂度** 。例如，区间内加一个等差数列，在一次差分后会转化为分段常数；再进行一次差分，往往就只剩下对个别位置的常数修改。最终，我们仍然可以通过多次前缀和，将结果还原回原数组。

多重差分本质上是把 “变化的变化” 继续拆解，直到问题退化为最基础、最容易处理的形式。这种方法在处理区间加多项式、斜率变化、分段函数等问题时尤为有效。虽然形式上更抽象，但一旦理解了其结构，就能用非常统一的方式解决一大类看似复杂的区间构造与统计问题。



---

# 等式条件变为不等条件相关题目收集

在许多问题中，**等式条件往往过于严格** ，直接求解会比较复杂；相比之下，**不等式的限制更宽松** ，通常更容易处理。因此我们常通过差分式思路，将原本的等式条件转化为两个不等式的差，从而简化计算过程：

$$
\text{count}(ans = k) = \text{count}(ans \le k) - \text{count}(ans \le k-1)
$$

这种技巧的核心在于：先解决更容易统计的不等式问题，再通过两者的差值恢复精确的等式计数。这样的转化在竞赛题中非常常见，且效率很高。

> 下面部分题目来源于这个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=405456839&bvid=BV1DG411d7fh&cid=29083175448&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## K 种整数子数组

[题目链接](https://leetcode.cn/problems/subarrays-with-k-different-integers/description/)

### Problem Statement

给定一个正整数数组 $nums$ 和一个整数 $k$ ，返回 $nums$ 中 **「好子数组」** 的数目。

如果 $nums$ 的某个子数组中不同整数的个数恰好为 $k$ ，则称 $nums$ 的这个连续、不一定不同的子数组为「好子数组」。

- 例如，$[1, 2, 3, 1, 2]$ 中有 $3$ 个不同的整数：$1$ ，$2$ ，以及 $3$ 。

**子数组** 是数组的 **连续** 部分。

### Constraints

- $1 \leq nums.length \leq 2 * 10^4$
- $1 \leq nums[i], k \leq nums.length$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。其中 $N$ 表示数组的长度，$k$ 的含义已在题目描述中给出。
- 第二行包含 $N$ 个整数，表示数组中的元素。

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

## 题目要点解析

处理子数组问题时，一个自然的想法是尝试使用 **滑动窗口** 。但滑动窗口并不是万能的，它要求问题本身具有 **单调性** ，否则窗口无法顺利扩张或收缩。判断单调性的标准，是看条件是否随窗口长度的变化而 **“越长越满足”** 或 **“越短越满足”** ，对应的两类条件分别是 **“至少 $k$ 种”** 和 **“至多 $k$ 种”** 。

在本题中，原目标是统计 **“恰好有 $k$ 个不同整数”** 的子数组。但 “恰好” 这一等式条件本身不具备滑动窗口所需的单调性：扩张或收缩窗口都无法保证窗口状态持续合法，因此无法像处理 “至多 $k$ 个不同整数” 那样稳定维护。也正因为缺乏这种可维护性，这道题不能直接使用滑动窗口解决。

为了处理这一问题，我们可以借助前面提到的 **差分思想** ，将等式转化为两个更容易处理的不等式：

* **至多 $k$ 个不同整数**
* **至多 $k-1$ 个不同整数**

于是，原问题可以写成：

$$
\text{count}(\text{distinct} = k) = \text{count}(\text{distinct} \le k) - \text{count}(\text{distinct} \le k-1)
$$

这两个不等式条件都具备单调性，可以稳定地使用滑动窗口求解，从而间接得到 **“恰好 $k$”** 的结果。这是一种在竞赛中极其常见且高效的转化方法。

基于上述思路，下面给出本题的完整代码实现：

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

# 区间求和变为前缀求和相关题目收集

在很多算法问题中，**直接处理区间求和往往不够直观** ，不仅实现复杂，还容易引入重复计算；而将其转化为 **前缀求和形式** 后，问题结构会变得更加清晰，计算也更加高效。因此，我们常通过引入前缀和数组，把区间约束统一转写为端点之间的差值关系，从而简化整体推导过程：

$$
\sum_{i = l}^{r} a_i = pre[r] - pre[l-1]
$$

这种技巧的核心在于：**用全局累积信息代替局部区间计算** ，将原本分散的区间操作压缩为常数次查询。这样的转化在竞赛题中极为常见，不仅能显著降低时间复杂度，也为后续的建模、优化与约束处理提供了统一而稳定的表达方式。

## 数组递增划分

[题目链接](https://leetcode.cn/problems/ways-to-split-array-into-three-subarrays/description/)

### Problem Statement

我们称一个分割整数数组的方案是 **好的** ，当它满足：

- 数组被分成三个 **非空** 连续子数组，从左至右分别命名为 `left` ，`mid` ，`right` 。
- `left` 中元素和小于等于 `mid` 中元素和，`mid` 中元素和小于等于 `right` 中元素和。

给你一个 **非负** 整数数组 `nums` ，请你返回 **好的** 分割 `nums` 方案数目。由于答案可能会很大，请你将结果对 $10^9 + 7$ 取余后返回。

### Constraints

- $3 \leq nums.length \leq 10^5$
- $0 \leq nums[i] \leq 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ 。其中 $N$ 表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3
1 1 1
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
6
1 2 2 2 5 0
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析



## 指定区间求和

[题目链接](https://atcoder.jp/contests/abc404/tasks/abc404_g)

### Problem Statement

给定一个整数 $N$ 和长度为 $M$ 的整数序列：

$$
L = (L_1, L_2, \ldots, L_M) \\
R = (R_1, R_2, \ldots, R_M) \\
S = (S_1, S_2, \ldots, S_M)
$$

确定是否存在一个长度为 $N$ 的正整数序列 $A$ 满足以下条件。如果存在这样的序列，找到 $A$ 的最小可能和。

$$
\sum_{j=L_i}^{R_i} A_j = S_i (1 \leq i \leq M)
$$

### Constraints

- 所有输入值都是整数
- $1 \leq N, M \leq 4000$
- $1 \leq L_i \leq R_i \leq N$
- $1 \leq S_i \leq 10^9$

### Input

输入从标准输入中以以下格式给出：

> $N \quad M$
>
> $L_1 \quad R_1 \quad S_1$
> 
> $L_2 \quad R_2 \quad S_2$
> 
> $\ldots$
>
> $L_M \quad R_M \quad S_M$

### Output

如果不存在满足条件且长度为 $N$ 的正整数序列 $A$ ，则打印 `-1` 。

否则，打印 $A$ 的最小可能总和。

### Sample Input 1

```txt showLineNumbers=false
5 3
1 2 4
2 3 5
5 5 5
```

### Sample Output 1

```txt showLineNumbers=false
12
```

### Sample Input 2

```txt showLineNumbers=false
1 2
1 1 1
1 1 2
```

### Sample Output 2

```txt showLineNumbers=false
-1
```

### Sample Input 3

```txt showLineNumbers=false
9 6
8 9 8
3 6 18
2 4 19
5 6 8
3 5 14
1 3 26
```

### Sample Output 3

```txt showLineNumbers=false
44
```

## 题目要点解析



---

# 双边条件变为单边条件相关题目收集

在许多算法竞赛问题中，我们经常需要统计满足某种 **双边约束** 的组合数量，例如：

$$
\text{lower} \le \text{nums}[i] + \text{nums}[j] \le \text{upper}
$$

这个条件本质上描述的是一个 **区间限制** 。如果直接在双重循环中逐一检查，时间复杂度通常会达到 $O(n^2)$ ，在数据规模稍大时难以接受。解决这类问题的关键，在于将原本的 **双边不等式约束** 转化为更容易处理的 **单边不等式** 。为此我们可以引入中间变量：

* 令 $T = \text{nums}[i] + \text{nums}[j]$

原本的条件是：$\text{lower} \le T \le \text{upper}$ ，可以等价地写成两个单边条件的组合：

$$
T \le \text{upper} \quad \text{且} \quad T \ge \text{lower}
$$

在此基础上，进一步引入一个计数函数 $f(X)$ ，表示满足 $T \le X$ 的组合数量，那么原问题就可以转化为：

$$
\text{count}(\text{lower} \le T \le \text{upper}) = f(\text{upper}) - f(\text{lower} - 1)
$$

这种转化思路核心在于：**先解决一个更宽松、易于统计的单边条件问题，再通过差分的方式恢复精确的双边计数结果** 。该技巧在区间统计、二分答案、双指针以及前缀结构等场景中都具有极强的通用性，是算法竞赛中非常值得熟练掌握的一类思想。

值得一提的是，在[数位 DP](https://xingguang641.com/posts/acm/acm-type/dp-classification/digit-dp/)相关的题目中，这类上下界问题有着天然的契合。例如统计某个区间内满足特定条件的数字数量时，原本的双边界限制可以直接转化为单边界的计数函数 $f(X)$ 。然而数位 DP 的上下界往往非常大，如果直接计算 $f(\text{lower}-1)$ 可能涉及高精度减法，为了避免这种情况，可以对 **lower 的情况单独特判** 。

我们可以先计算 $f(\text{upper}) - f(\text{lower})$ ，再单独判断 $lower$ 本身是否满足要求。这样就可以避免写高精度减法，同时依然保持算法的正确性和效率。这个技巧在处理大整数的数位 DP 时非常实用，也是算法竞赛中处理上下界问题的一种常见套路。

## 统计公平数对

[题目链接](https://leetcode.cn/problems/count-the-number-of-fair-pairs/description/)

### Problem Statement

给你一个下标从 $0$ 开始、长度为 $n$ 的整数数组 `nums` ，和两个整数 `lower` 和 `upper` ，返回 **公平数对的数目** 。

如果 $(i, j)$ 数对满足以下情况，则认为它是一个 **公平数对**：

- $0 <= i < j < n$
- $lower <= nums[i] + nums[j] <= upper$

### Constraints

- $1 \leq nums.length \leq 10^5$
- $nums.length == n$
- $-10^9 \leq nums[i] \leq 10^9$
- $-10^9 \leq lower \leq upper \leq 10^9$

### Input

输入包含两行：

- 第一行包含三个整数 $N$ 、$lower$ 和 $upper$ 。其中 $N$ 表示数组的长度，$lower$ 和 $upper$ 的含义已在题目中给出。
- 第二行包含 $N$ 个整数，表示数组中的元素。

> $N \quad lower \quad upper$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
6 3 6
0 1 7 4 4 5
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
5 11 11
1 7 9 2 5
```

### Sample Output 2

```txt showLineNumbers=false
1
```

## 题目要点解析



---

# 参考文献列表

1. [【OI WiKi】前缀和 & 差分](https://oi-wiki.org/basic/prefix-sum/)

2. [【算法学习】算法技巧之差分](https://blog.csdn.net/myRealization/article/details/104594255)