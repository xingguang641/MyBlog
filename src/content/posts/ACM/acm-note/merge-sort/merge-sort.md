---
title: 【ACM 算法随笔】归并分治算法的应用
published: 2025-11-20
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: false
---

# 归并分治基本原理

对于多维偏序问题，常见的处理方式是先对其中一个维度进行排序，以此固定该维度上的相对顺序，从而实现降维并简化问题。然而这种排序手段 **只能使用一次** ，在二维偏序问题中能较为从容地解决。当维度扩展到三维及更高维度时，单次排序已不足以处理多个维度之间的偏序关系。**归并分治** 正是在这一背景下引入的一种方法，它借助归并排序的算法思想，在算法流程中自然地引入顺序约束，从而隐式地维护多维偏序关系。

归并分治的关键在于 **它能够在不影响统计完整性的前提下，间接实现对两个维度的排序** 。在分治过程中元素被划分为左右两个部分，而划分本身建立在第一维偏序关系之上，因此在合并阶段左半部分中的所有元素在第一维偏序上必然不大于右半部分中的元素，第一维偏序关系 **在结构层面已经被保证** 。

基于这一事实，在合并阶段可以将左右两部分视为在第一维偏序关系上有序的两个整体。只要不改变元素所属的分治区间，左右两部分内部的元素就可以任意重排而不破坏第一维偏序约束，因此可以在合并阶段进一步按照第二维偏序进行排序处理，这正是归并分治 **能够同时处理两维偏序关系** 的原因。

在统计贡献时，归并分治依赖方向性的约束。如果在合并阶段仅计算左侧元素对右侧元素的贡献，则对于任意一个元素而言，其最终累计的结果正是所有位于其左侧的元素对自身产生的影响。由于任意一对元素必然会在某一层分治中 **恰好被统计一次** ，因此不会遗漏或重复统计贡献。

## CDQ分治简介

CDQ 分治本质上是 **归并分治思想在处理多维偏序问题中的深度应用** ，它并未在归并分治的基础框架上引入新的逻辑，而是充分利用了归并排序在合并阶段天然具备的顺序约束。这种约束使得我们能够在不依赖对所有维度进行排序的前提下，建立起维度之间的逻辑依赖，从而完成多维偏序关系的精准统计。

在实际的算法竞赛中，CDQ 分治常用于解决 **三维及以上的高维偏序问题** 。这类问题的核心挑战在于多个维度之间相互交织的约束关系，会让传统的单维排序做法顾此失彼。而 CDQ 分治通过 **一维排序、二维归并、三维统计** 的经典套路，将复杂的多维偏序问题逐层降维：

1.  **一维排序**：通过对第一维偏序进行全局预处理排序，确保在后续的分治过程中，左区间的任何元素在第一维偏序上满足不大于右区间元素的条件，从而消除了第一维偏序的限制。
2.  **二维归并**：在合并过程中，程序通过归并排序的方式对第二维偏序进行重排，这使得我们在处理右区间的每个元素时，可以利用双指针将左区间中满足第二维偏序限制的元素逐一加入统计范围。
3.  **三维统计**：由于前两维的约束已经在分治与双指针的过程中被成功维护，此时只需用 **树状数组或线段树** 等高效的数据结构维护第三维偏序，即可在 $O(\log n)$ 的时间内完成实时统计。

在实际应用中，这种分治架构为处理 **大规模数据下的多维依赖** 提供了极其便捷的底层框加。它将原本需要嵌套多层高级数据结构才能解决的复杂统计问题，转化为一系列在线性扫描过程中完成的单向更新。这种降维策略显著降低了算法的实现难度，使其成为处理各类偏序统计问题的通用范式。

> 具体的题目类型可以看下面这些视频

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114607746195424&bvid=BV1sa7zz1EVx&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
  <iframe width="100%" height="200" src="//player.bilibili.com/player.html?isOutside=true&aid=114653598322831&bvid=BV1RsTiz4EAw&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
</div>

此外，CDQ 分治在 **动态问题静态化** 方面也展现出极强的普适性。通过引入时间轴作为第一维坐标，我们可以将复杂的动态修改与实时查询操作，统一建模为静态的三维偏序问题。在这种视角下，每一次修改被视为一个带有时间戳的贡献点，而每一次查询则是在特定时间窗口与空间范围内的贡献统计。

---

# 偏序数对相关问题

在多维偏序类型题中，绝大部分题目的求解核心均围绕 **偏序数对的计数问题** 展开。该类问题通常要求我们在给定点集中，检索并计数所有满足特定多维偏序约束的元素对。针对这种非线性的偏序限制，我们通常需要引入高维数据结构或分治技巧，通过排序降维将高维约束逐层剥离，从而将计算复杂度强行压缩至更高效的对数级别。

从建模视角分析，**二维数点问题** 是几何空间中最经典的偏序数对计数问题。通过容斥原理将矩形区域查询拆解为前缀矩形查询后，核心问题就被转化为统计满足 $x_i \leq X$ 且 $y_i \leq Y$ 的元素集合。在笛卡尔坐标系中，这本质上是检索与给定参考点 $(X, Y)$ 构成二维偏序关系的受限点集。这种从几何区域到代数偏序的转化，不仅统一了问题模型，也为后续利用归并分治和 CDQ 分治等技巧进行降维维护提供了核心切入点。

## 计算数组的小和

[题目链接](https://www.nowcoder.com/practice/edfe05a1d45c4ea89101d936cac32469)

### Problem Statement

数组小和的定义：$\displaystyle \sum_{i = 1}^{n} f_i$ ，其中 $f_i$ 的定义是第 $i$ 个数左侧小于等于 $s_i$ 的元素和。

例如，数组 $s = [1, 3, 5, 2, 4, 6]$

- 在 $s[0]$ 的左边小于或等于 $s[0]$ 的数的和为 $0$

- 在 $s[1]$ 的左边小于或等于 $s[1]$ 的数的和为 $1$

- 在 $s[2]$ 的左边小于或等于 $s[2]$ 的数的和为 $1 + 3 = 4$

- 在 $s[3]$ 的左边小于或等于 $s[3]$ 的数的和为 $1$

- 在 $s[4]$ 的左边小于或等于 $s[4]$ 的数的和为 $1 + 3 + 2 = 6$

- 在 $s[5]$ 的左边小于或等于 $s[5]$ 的数的和为 $1 + 3 + 5 + 2 + 4 = 15$

所以 $s$ 的小和为 $0 + 1 + 4 + 1 + 6 + 15 = 27$

给定一个数组 $s$  ，实现函数返回 $s$ 的小和。

### Constraints

- $0 < n \leq 10^5$
- $-100 \leq s[i] \leq 100$
- 所有输入均为整数

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的各个元素。

> $N$
> 
> $s_1 \quad s_2 \quad \ldots \quad s_N$

### Output

输出一个整数表示数组的小和。

### Sample Input 1

```txt showLineNumbers=false
6
1 3 5 2 4 6
```

### Sample Output 1

```txt showLineNumbers=false
27
```

### Sample Input 2

```txt showLineNumbers=false
1
1
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析

解决该问题的关键在于需要运用[对象交换贡献法](https://xingguang641.com/posts/acm/acm-note/enumeration/#对象交换贡献法)来转换统计方式，将原本统计每个数左侧有多少个比它小的数，转变为统计每个数 $s_i$ 会作为较小值被其右侧比它大的数累加多少次。这一逻辑与经典的 **逆序对问题** 高度相似，只不过逆序对问题统计的是左侧比自己大的个数，而本题则是在归并排序的合并阶段，利用左右子区间的有序性，一次性计算出左区间元素对右区间更大元素的贡献值。

这种基于归并分治的策略，可以在 $O(n \log n)$ 的排序过程中完成跨区间的答案统计。在区间合并时，每个元素的贡献都得以被精准计算且不重不漏，从而保证了最终结果的正确性。该方法在时间复杂度上远优于 $O(n^2)$ 的暴力扫描，其实现逻辑也比树状数组或线段树等结构更加直观。利用归并分治算法，原本复杂的全局统计被巧妙拆解为局部有序区间之间的线性累加，实现了在排序的同时同步完成偏序计数。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 1e5 + 100;
int n; ll ans = 0;
int a[MAXN];

void merge(int l, int r, int mid, int *a){
    int b[r - l + 1];
    int i = l, j = mid + 1, k = 0;

    while (i <= mid && j <= r){
        if (a[i] <= a[j]){
            // a[i] 对右侧 [j, r] 的所有元素产生贡献
            ans += 1LL * a[i] * (r - j + 1);
            b[k++] = a[i++];
        } else {
            b[k++] = a[j++];
        }
    }

    while (i <= mid) b[k++] = a[i++];
    while (j <= r) b[k++] = a[j++];

    for (int t = 0; t < k; t++){
        a[l + t] = b[t];
    }
}

void merge_sort(int l, int r, int *a){
    if (l == r) return;

    int mid = (l + r) / 2;
    merge_sort(l, mid, a);
    merge_sort(mid + 1, r, a);
    merge(l, r, mid, a);
}

int main(){
    cin >> n;
    for (int i = 0; i < n; i++){
        cin >> a[i];
    }

    if (n > 1){
        merge_sort(0, n - 1, a);
    }

    cout << ans << "\n";
}
```

## 统计重要翻转对

[题目链接](https://leetcode.cn/problems/reverse-pairs/description/)

### Problem Statement

给定一个数组 $nums$ ，如果 $i < j$ 且 $nums[i] > 2 * nums[j]$ 我们就将 $(i, j)$ 称作一个 **重要翻转对** 。

你需要返回给定数组中的重要翻转对的数量。

### Constraints

- 给定数组的长度不会超过 $50000$
- 输入数组中的所有数字都在 $32$ 位整数的表示范围内

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组的长度。
- 第二行包含 $N$ 个整数，表示数组中的各个元素。

> $N$
> 
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示数组翻转对的数量。

### Sample Input 1

```txt showLineNumbers=false
5
1 3 2 3 1
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
5
2 4 3 5 1
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析

解决该问题的关键在于利用归并排序中左右子区间的 **天然位置顺序** 。在分治的合并阶段，左区间的所有元素下标 $i$ 必然小于右区间的所有元素下标 $j$ 。由于左右子区间在统计前已各自有序，我们可以利用双指针同步扫描右区间的每一个 $nums[j]$ ，并在左区间找到第一个满足 $nums[i] > 2 \cdot nums[j]$ 的位置。此时利用左区间的有序性，我们可以借助下标计算出左区间所有满足条件的元素个数，从而在 $O(n \log n)$ 的总复杂度内高效完成计数。

需要注意的是，本题与普通的逆序对问题略有不同。在传统的逆序对计算中，由于统计条件与合并条件完全相同，我们可以在归并排序的合并过程中顺便完成计数。然而本题的统计条件 $nums[i] > 2 \cdot nums[j]$ 与合并时的排序条件 $nums[i] > nums[j]$ 并不一致，这导致双指针在计算贡献与移动元素时无法同步推进。因此我们必须在常规的合并操作之前，用一个独立的双指针逻辑先完成当前层级的翻转对统计。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int MAXN = 5e4 + 100;
int n; ll ans = 0;
ll a[MAXN];

void merge(int l, int r, int mid, ll *a){
    // 统计重要翻转对
    int j = mid + 1;
    for (int i = l; i <= mid; i++){
        while (j <= r && a[i] > 2LL * a[j]){
            j++;
        }
        ans += (j - (mid + 1));
    }

    // 正常归并排序
    ll b[r - l + 1];
    int i = l; j = mid + 1; int k = 0;

    while (i <= mid && j <= r){
        if (a[i] <= a[j]) b[k++] = a[i++];
        else b[k++] = a[j++];
    }

    while (i <= mid) b[k++] = a[i++];
    while (j <= r) b[k++] = a[j++];

    for (int t = 0; t < k; t++){
        a[l + t] = b[t];
    }
}

void merge_sort(int l, int r, ll *a){
    if (l >= r) return;

    int mid = (l + r) / 2;
    merge_sort(l, mid, a);
    merge_sort(mid + 1, r, a);
    merge(l, r, mid, a);
}

int main(){
    cin >> n;
    for (int i = 0; i < n; i++){
        cin >> a[i];
    }

    if (n > 1){
        merge_sort(0, n - 1, a);
    }

    cout << ans << "\n";
    return 0;
}
```

---

# 参考文献引用列表

1. [【OI WiKi】CDQ 分治相关知识](https://oi-wiki.org/misc/cdq-divide/)

2. [【Luogu 博客】CDQ 分治和整体二分](https://www.luogu.com.cn/article/nl6r7elc)