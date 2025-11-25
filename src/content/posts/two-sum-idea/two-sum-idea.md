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

不过，如果我们换一个视角：从左到右遍历数组，那么在访问当前元素之前，它左侧的所有信息都已知。如果我们能够在遍历过程中 **实时记录已经出现过的数字及其出现次数** ，那么对于当前元素，我们只需用 $O(1)$ 的时间查询其 “配对目标” 是否已经出现过，并累加数量即可。

这样一来，总体时间复杂度便能从 $O(n^2)$ 优化到 **线性复杂度 $O(n)$** ，实现更高效的求解。

首先，我们明确题目所要求的条件：

$$
nums[i] + nums[j] = target
$$

然后我们将关于 $j$ 的部分移动到等式另一侧，可以得到：

$$
nums[i] = target - nums[j]
$$

这意味着：当我们遍历数组时，如果能够实时记录已经出现过的数字 $target - nums[j]$ 的出现次数，那么对于当前数字 $nums[i]$ ，只需要查询它所对应的配对值 $nums[i]$ 之前出现了多少次，就能直接得出以 $i$ 为右端点所贡献的有效数对数量。

换句话说：对于每个数，我们可以查找 $nums[i]$ ，统计 $target - nums[i]$ 。同理，我们可以查找 $target - nums[i]$ ，统计 $nums[i]$ 。

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
        int num; cin >> num;
        a[i] = num;
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

或许大家都知道，如果我们定义数组的前缀和为 $pre$，那么任意子数组的和都可以表示为：

$$
pre[right] - pre[left] = sum[left: right]
$$

我们惊奇地发现，这不就是两数之和吗？！也就是说，对于所有的数组子段和问题，我们都可以借助 “两数之和” 的思路来高效解决。接下来就让我们通过几个例子来深入理解这一技巧吧。

> 下面部分题目来源于这个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=447731638&bvid=BV1Sj411q7fi&cid=1245726571&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 累加和为定值的最长子数组

[题目链接](https://www.nowcoder.com/practice/36fb0fd3c656480c92b569258a1223d5)

### Problem Statement

给定一个无序数组 $arr$ , 其中元素是在一定范围内的任意整数。给定一个整数 $k$ ，求 $arr$ 所有子数组中累加和为 $k$ 的最长子数组长度。

### Constraints

- $1 \leq N \leq 10^5$
- $-10^9 \leq k \leq 10^9$
- $-100 \leq arr_i \leq 100$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。其中， $N$ 表示数组的长度， $k$ 的含义已在题目描述中给出
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

由于减法不具备加法的 **交换律** （Symmetry），我们不能像 “两数之和” 那样随意交换 “存储对象” 和 “查询对象” ，必须根据移项后的公式严格确定逻辑。这里存在两种等价的变形思路：

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

这意味着：当我们遍历到 $right$ 时，应该在哈希表中查询是否存在 $pre[right]$ （看过去是否有人 “期望” 凑成这个和），并存储未来的 “期望值” $pre[right] + k$ 。

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
    return 0;
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