---
title: 【ACM 算法随笔】两数之和思想
published: 2025-11-23
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

> 写在前面：我对 “两数之和” 这一题目的理解主要来源于灵神的一段视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=305008442&bvid=BV1bP411c7oJ&cid=888954096&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 两数之和题目讲解

两数之和是 LeetCode 上编号为 1 的开山题目，堪称算法题中的 `Hello World!` 。看似简单，却绝非只能停留在新手练习层面。之所以值得专门写一篇文章来讲解，是因为 “两数之和” 背后的思想具有极强的泛用性，它贯穿于大量经典算法题之中，衍生出多种技巧与思路。你也许已经独立完成过这些题目，却未曾意识到它们之间存在着紧密的联系。

接下来，我将以 “两数之和” 为主线，带你串联起各类相关题型。相信这趟旅程会让你对熟悉的题目有全新的理解，也能收获更体系化的解题思维。

## 两数之和

[题目链接](https://leetcode.cn/problems/two-sum/description/)

### Problem Statement

给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 **和为目标值** target 的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

### Constraints

- $2 \leq nums.length \leq 10^4$
- $-10^9 \leq nums[i] \leq 10^9$
- $-10^9 \leq target \leq 10^9$
- 只会存在一个有效答案

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $target$ ，分别表示数组长度和目标值
- 第二行包含 $n$ 个整数，表示数组中的各个元素

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

## 题目解析

由于这个题目本身难度较低，我们不妨在它的基础上稍作扩展，将其作为理解 “两数之和” 思想的入门练习。具体来说，我们将原题中 “只存在一个有效答案” 的限制移除，允许出现 **多个不同的数对** 和为 target，并要求我们统计所有满足条件的数对数量。

为了统计所有满足条件的数对数量，我们可以先思考一个直观的解法：对于数组中每个元素，都去查找它左侧部分中是否存在与之配对的目标值。这样可以枚举所有可能的配对关系，但时间复杂度会达到 $O(n^2)$ ，显然效率不高。

不过我们可以换一个视角：从左到右遍历数组，那么在访问当前元素之前，它左侧的所有信息都已知。如果我们能够在遍历过程中 **实时记录已经出现过的数字及其出现次数** ，那么对于当前元素，我们只需用 $O(1)$ 的时间查询其 “配对目标” 是否已经出现过，并累加数量即可。

这样一来，总体时间复杂度便能从 $O(n^2)$ 优化到 **线性复杂度 $O(n)$** ，实现更高效的求解。

首先，我们明确题目所要求的条件：

$$
nums[i] + nums[j] = target
$$

然后我们将关于 $j$ 的部分移动到等式另一侧，可以得到：

$$
nums[i] = target - nums[j]
$$

因此当我们遍历数组时，如果能够实时记录已经出现过的数字 $target - nums[j]$ 的出现次数，那么对于当前数字 $nums[i]$ ，只需要查询它所对应的配对值 $nums[i]$ 之前出现了多少次，就能直接得出以 $i$ 为右端点所贡献的有效数对数量。

这意味着算法流程如下：

- **查询（Query）**：在哈希表中查找是否存在键为 $target - nums[i]$ 的记录。如果存在，则说明找到了互补的数对。
- **记录（Update）**：将当前数字 $nums[i]$ 更新到哈希表中（出现次数 + 1），作为后续数字的 “配对目标” 。

同理，我们也可以查询 $target - nums[i]$ ，记录 $nums[i]$ 。

下面给出完整代码：

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
        if (counts.count(a[i])){
            ans += counts[a[i]];
        }
        counts[target - a[i]]++;
    }

    cout << ans << endl;
}
```

核心代码还可以改成下面这样，效果是差不多的：

```cpp frame="code" title="main.cpp"
int ans = 0;  
unordered_map<int, int> counts;
for (int i = 0; i < n; i++){
    if (counts.count(target - a[i])){
        ans += counts[target - a[i]];
    }
    counts[a[i]]++;
}
```

---

# 数组子段和题目讲解

或许大家都知道，如果我们定义数组的前缀和为 $pre$ ，那么任意子数组的和都可以表示为：

$$
pre[right] - pre[left] = sum[left: right]
$$

我们惊奇地发现，这不就是两数之和吗？！也就是说，对于所有的数组子段和问题，我们都可以借助 “两数之和” 的思路来高效解决。接下来就让我们通过几个例子来深入理解这一技巧吧。

> 下面部分题目来源于这个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=447731638&bvid=BV1Sj411q7fi&cid=1245726571&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 累加和为定值的最长子数组

[题目链接](https://www.nowcoder.com/practice/36fb0fd3c656480c92b569258a1223d5)

### Problem Statement

给定一个无序数组 $arr$ ，其中元素是在一定范围内的任意整数。给定一个整数 $k$ ，求 $arr$ 所有子数组中累加和为 $k$ 的最长子数组长度。

### Constraints

- $1 \leq N \leq 10^5$
- $-10^9 \leq k \leq 10^9$
- $-100 \leq arr_i \leq 100$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。其中，$N$ 表示数组的长度，$k$ 的含义已在题目描述中给出
- 第二行包含 $N$ 个整数，表示数组中的元素

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

## 题目解析

借鉴 “两数之和” 的思路，我们将子数组和问题转化为前缀和的差值问题。设 $pre[i]$ 为前 $i$ 个元素的累加和，则子数组区间和为 $k$ 可以表示为：

$$
pre[right] - pre[left] = k \quad (left \leq right)
$$

由于减法不具备加法的 **交换律（Symmetry）**，我们不能像 “两数之和” 那样随意交换 “存储对象” 和 “查询对象” ，必须根据移项后的公式严格确定逻辑。这里存在两种等价的变形思路：

### 思路一：查 “历史值” ，存 “当前值”

将 $pre[right]$ 移项可得：

$$
pre[right] - k = pre[left]
$$

这意味着：当我们遍历到 $right$ 时，应该在哈希表中 **查询** 是否存在 $pre[right] − k$ ，并 **存储** 当前的真实前缀和 $pre[right]$ 。

- **初始化**：因为我们存储的是 **真实** 的前缀和，初始状态下前缀和为 0，因此需要初始化 `pos[0] = -1`

### 思路二：查 “当前值” ，存 “期望值”

将 $pre[left]$ 移项可得：

$$
pre[right] = pre[left] + k
$$

这意味着：当我们遍历到 $right$ 时，应该在哈希表中查询是否存在 $pre[right]$（看过去是否有人 “期望” 凑成这个和），并存储未来的 “期望值” $pre[right] + k$ 。

- **初始化**：因为我们存储的是期望值（即 $pre + k$ ），初始状态下前缀和为 0，它期望未来遇到 $k$ 来凑对，因此需要初始化 `pos[k] = -1`

此外，由于题目要求 **最长子数组** ，哈希表中应只记录某个键值 **第一次出现的位置** 。这样在计算 $right−left$ 时，减去的 $left$ 越小，得到的区间长度就越大。

基于上述思路，最终代码如下：

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

- 第一行包含两个整数 $N$ 和 $k$ 。其中， $N$ 表示数组的长度， $k$ 的含义已在题目描述中给出
- 第二行包含 $N$ 个整数，表示数组中的元素

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

## 题目解析

这个题就非常简单了，直接仿照两数之和原题写代码就可以了（仍然要注意初始化问题）。

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

## 正负一样多的最长子数组

[题目链接](https://www.nowcoder.com/practice/545544c060804eceaed0bb84fcd992fb)

### Problem Statement

给定一个无序数组 $arr$ ，求 $arr$ 所有子数组中正数与负数个数相等的最长子数组的长度。

### Constraints

- $1 \leq arr.length \leq 10^5$
- $-100 \leq arr_i \leq 100$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ ，表示数组的长度
- 第二行包含 $N$ 个整数，表示数组中的元素

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

## 题目解析

首先观察题目，出现了关键字 “一样多” ，对于这种类型题，我们往往会将数据 “二值化” ，然后让数组累加和为 0 来表示 “一样多” 。请注意这个技巧，我们在后续的题目会经常用到。

因此，我们只需要将整数看成 1，将负数看成 -1，然后寻找最长的累加和为 0 的子数组即可（注意原数组是有 0 的，我们直接不用管，但是千万不要将等于号加入转换代码中，否则会导致错误）。

我们直接套用上面 “累加和为定值的最长子数组” 的代码：

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

## 表现良好的最长时间段

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

- 第一行包含两个整数 $N$ ，表示数组的长度
- 第二行包含 $N$ 个整数，表示数组中的元素

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

## 题目解析

同样的，我们将大于 8 的数值映射为 1，小于等于 8 的数值映射为 -1。此时，问题转化为寻找 **元素和大于 0 的最长子数组** 。引入前缀和数组 $pre$ ，子数组和大于 0 等价于 $pre[right] - pre[left] > 0$ ，即满足 $pre[left] < pre[right]$ 。

**形式化描述**：

在前缀和数组中，寻找一对索引 $(left, right)$ ，在满足 $left < right$ 且 $pre[left] < pre[right]$ 的前提下，使得 $right - left$ 的值最大。

这实际上是一个经典的单调栈问题（即 “最大宽度坡” 问题）：我们要为每一个 $right$ 找到其左侧 **距离最远** 且 **数值更小** 的下标 $left$ 并计算差值，然后在这些差值中寻找最大值即可。

> 关于单调栈的知识可以看我这篇博客

[【ACM 算法随笔】单调栈技巧](https://xingguang641.com/posts/monotonic-stack-idea/monotonic-stack-idea/)

但这道题其实还有其他的信息可以使用：由于数组内的数字的绝对值都是 1，因此数组前缀和的变化都是 1，满足 “单调连续性” 。

利用这一性质我们可以进一步简化算法：

- 如果 $pre[i] > 0$ ：

    说明从数组起始位置到当前位置的整体和大于 0，此时最长长度即为 $i + 1$ 。

- 如果 $pre[i] \geq 0$ ：

    我们需要寻找左侧某个 $pre[left]$ 满足 $pre[left] < pre[i]$ 。

    根据前缀和的连续性，前缀和从 0 下降到 $pre[i]$（例如 -5），必然要在更早的位置先经过 $pre[i] + 1$（例如 -4）。也就是说，$pre[i] − 1$ 的首次出现位置，一定早于 $pre[i] − 2$ 、$pre[i] − 3$ 等更小数值的首次出现位置。

    因此，为了让 $right − left$ 最大，我们不需要寻找所有小于 $pre[i]$ 的数，只需要寻找 $pre[i] − 1$ 第一次出现的位置即可。

下面就给出这个题目的完整代码：

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```

## 题目拓展

如果我们将 “寻找最长子数组” 这个条件改成 “统计目标数组个数” 又该怎么做呢？同样的，我们先不考虑这道题的特殊性，我们可以将问题转化为：

在前缀和数组中，有多少对 $(left, right)$ 满足 $left < right$ 且 $pre[left] < pre[right]$（一个数对对应一个子数组，因此统计数对个数就是在统计子数组个数）。

这不就是 “逆序对” 的共轭题目 “顺序对” 吗？！因此我们可以直接使用归并分治解决这个问题。

> 关于归并分治的知识可以看我这篇博客

[【ACM 算法随笔】归并排序与归并分治](https://xingguang641.com/posts/merge-sort/merge-sort/)

现在我们将 “单调连续” 这个条件用上：对于这个问题，我们只需要在遍历到某个下标时能够马上知道小于 $pre[i]$ 的前缀个数即可，因此我们可以动态维护小于当前 $pre[i]$ 的前缀个数。又因为 $pre$ 的变化是连续的，因此我们可以使用 **增量法** 来解决：

- 当 $pre + 1$ 时，由于我们已经求解出所有小于 $pre - 1$ 的前缀个数，因此我们只需要算上前缀和等于 $pre$ 的前缀个数即可
- 当 $pre - 1$ 时，由于我们已经求解出所有小于 $pre - 1$ 的前缀个数，因此我们只需要舍弃前缀和等于 $pre - 1$ 的前缀个数即可

由于前缀的变化每次都只有 1 这个量级，因此我们动态维护 “小于当前 $pre[i]$ 的前缀个数” 会非常的轻松，只需要统计每种前缀值出现的次数就能够 $O(1)$ 更新它。

## 使数组和能被 P 整除

[题目链接](https://leetcode.cn/problems/make-sum-divisible-by-p/description/)

### Problem Statement

给你一个正整数数组 $nums$ ，请你移除 **最短** 子数组（可以为 **空** ），使得剩余元素的 **和** 能被 $p$ 整除。**不允许** 将整个数组都移除。

请你返回你需要移除的最短子数组的长度，如果无法满足题目要求，返回 -1。

**子数组** 定义为原数组中连续的一组元素。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $0 \leq nums[i] \leq 10^9$
- $1 \leq p \leq 10^9$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $p$ 。其中，$N$ 表示数组的长度，$p$ 的含义已在题目描述中给出
- 第二行包含 $N$ 个整数，表示数组中的元素

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

### Sample Output 

```txt showLineNumbers=false
0
```

## 题目解析

首先这道题有一个很明显的点：如果整个数组的和模 $p$ 余 0，那我们不需要移除任何数。如果整个数组的和模 $p$ 余 $r$ ，那我们就要找到累加和（取模后）为 $r$ 的最短子数组。

因此我们可以得到下面这个条件：

$$
pre[right] - pre[left] \equiv r \pmod{p}
$$

根据两数之和的思想，我们将 $left$ 移至右侧可得：

$$
pre[right] \equiv r + pre[left] \pmod{p}
$$

因此我们要查询 $pre[i] \% p$ 的同时，统计 $(r + pre[i]) \% p$ 出现的最早位置。

根据两数之和的思路，我们可以轻易地想到这个题的标准写法，看似稀奇古怪的取模操作其实背后的数学思想非常简单，下面就给出这道题的完整代码供大家学习：

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main() {

}
```