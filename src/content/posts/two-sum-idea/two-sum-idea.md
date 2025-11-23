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

两数之和是 LeetCode 上编号为 1 的开山题目，堪称算法题中的 `Hello World!` 。看似简单，却绝非只能停留在新手练习层面。

之所以值得专门写一篇文章来讲解，是因为 “两数之和” 背后的思想具有极强的泛用性，它贯穿于大量经典算法题之中，衍生出多种技巧与思路。你也许已经独立完成过这些题目，却未曾意识到它们之间存在着紧密的联系。

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

换句话说：对于每个数，我们可以查找 $nums[i]$ ，统计 $target - nums[i]$ ；同理，我们可以查找 $target - nums[i]$ ，统计 $nums[i]$ 。

下面给出完整代码：

```cpp frame="code" title="main.cpp"
# include <bits/stdc++.h>
using namespace std;
const int MAXN = 1e5;
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



### Constraints



### Input



### Output



### Sample Input 1

```txt showLineNumbers=false

```

### Sample Output 1

```txt showLineNumbers=false

```

