---
title: 【ACM 算法题单】最长公共子序列问题
published: 2026-02-04
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 经典动态规划思想

最长公共子序列（LCS）与最长公共子串（LCSubstr）是动态规划中极具代表性的两个经典问题。它们本身并不复杂，但其建模方式却贯穿了大量序列类题目。许多看似形式各异的挑战，本质上都可以追溯到这两类问题的思想变形，只是在状态定义或转移条件上进行了不同程度的包装。

从建模逻辑来看，**子序列类问题的本质是寻找非连续的元素子集** 。在定义状态时，$dp[i][j]$ 往往表示考虑到第一个序列前 $i$ 个元素与第二个序列前 $j$ 个元素时的全局最优解，而不需要强求当前元素必须被选中。这种定义天然允许跳过某些元素，其转移过程通常围绕选或不选的决策展开。两序列当前字符相等时，意味着我们找到了交集的一个新成员，状态由 $dp[i-1][j-1]$ 累加递增；两序列当前字符不相等时，则通过继承 $dp[i-1][j]$ 或 $dp[i][j-1]$ 的已有结果来保持交集的最大化。

与之相对，**子串类问题则要求目标序列必须在物理空间上绝对连续** 。这使得状态定义必须显式刻画以某个位置结尾的信息，例如定义 $dp[i][j]$ 为以两个序列当前字符结尾的最长公共后缀长度。在这种约束下，一旦序列中断了连续性，即当前元素无法与前序构成紧密关联，其状态价值必须被强制重置。因此这类问题的转移更加局部，高度依赖当前位置之间的直接匹配关系，而无法像子序列样跨越节点。

### 最短公共父序列

最短公共超序列（SCS）同样是动态规划的一个经典问题，其核心目标是构造一个最短的序列，使得两个原始序列都能作为其子序列完整出现。如果将 LCS 理解为提取序列间的 **最大交集** ，那么 SCS 则是寻找它们的 **最小并集** 。为了实现这一目标，我们通常有两种截然不同但逻辑互补的建模视角。

第一种视角是将 SCS 看作 LCS 的 **对偶问题** 。为了使构造长度降至最低，问题的本质在于 **最大化复用** 两个序列中的相同字符。这种复用逻辑深刻体现了 **容斥原理**：并集的规模等于两个集合规模之和减去交集规模。在这种逻辑下，我们无需重新设计算法，可以直接通过下式计算超序列的长度：

$$
Length(SCS) = Length(S_1) + Length(S_2) - Length(LCS)
$$

在具体构造字符串时，这种做法相当于以 **LCS 为骨架** 。我们先确定公共字符的位置，然后在这些骨架字符的空隙中，按原有的相对顺序依次填入两个序列各自特有的差异字符。

另一种视角则是直接针对 **必选约束下的最优覆盖** 进行建模。我们设 $dp[i][j]$ 为使 $S_1$ 前 $i$ 个字符和 $S_2$ 前 $j$ 个字符成为其子序列的最短超序列长度。当字符相等时（ $S_1[i] == S_2[j]$ ），我们获得了一个珍贵的复用机会，该字符在结果中只占一个位宽，状态由下式转移：

$$
dp[i][j] = dp[i-1][j-1] + 1
$$

当字符不等时（ $S_1[i] \neq S_2[j]$ ），我们不再像处理 LCS 那样简单地抛弃不匹配的部分，而是必须在结果中 **接纳当前字符** 以保证覆盖的完整性。此时，我们需要在 “接纳 $S_1$ 的当前字符” 与 “接纳 $S_2$ 的当前字符” 这两个分支中，选择 **代价更小** 的路径继续推进：

$$
dp[i][j] = \min(dp[i-1][j], \, dp[i][j-1]) + 1
$$

这种直接建模方式不仅解决了长度计算问题，更为我们提供了一套精准的 **回溯流程** 。通过观察 $dp$ 表的决策路径，我们能够按图索骥地构造出这个包含所有原始信息的最小字符序列。

## 最长公共子序列

[题目链接](https://leetcode.cn/problems/longest-common-subsequence/)

### Problem Statement

给定两个字符串 `text1` 和 `text2` ，返回这两个字符串的最长 **公共子序列** 的长度。如果不存在 **公共子序列** ，返回 $0$ 。一个字符串的 **子序列** 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

- 例如，`"ace"` 是 `"abcde"` 的子序列，但 `"aec"` 不是 `"abcde"` 的子序列。

两个字符串的 **公共子序列** 是这两个字符串所共同拥有的子序列。

### Constraints

- $1 \leq text1.length, text2.length \leq 1000$
- `text1` 和 `text2` 仅由小写英文字符组成

### Input

输入包含两行：

- 第一行包含一个字符串，表示 $text1$ 。
- 第二行包含一个字符串，表示 $text2$ 。

> $text1$
> 
> $text2$

### Output

输出一个整数，表示这两个字符串的最长公共子序列的长度。

### Sample Input 1

```txt showLineNumbers=false
abcde
ace
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
abc
abc
```

### Sample Output 2

```txt showLineNumbers=false
3
```

### Sample Input 3

```txt showLineNumbers=false
abc
def
```

### Sample Output 3

```txt showLineNumbers=false
0
```

## 题目要点解析

可以从前往后匹配也可以从后往前匹配

## 不同子序列个数

[题目链接](https://leetcode.cn/problems/distinct-subsequences/description/)

### Problem Statement

给你两个字符串 `s` 和 `t` ，统计并返回在 `s` 的 **子序列** 中 `t` 出现的个数，结果需要对 $10^9 + 7$ 取模。

题目测试用例保证压力在可控范围内，结果不会超过 $2^{63} - 1$ 。

### Constraints

- $1 \leq s.length, t.length \leq 1000$
- `s` 和 `t` 由英文字母组成

### Input

输入包含两行：

- 第一行包含一个字符串，表示 $s$ 。
- 第二行包含一个字符串，表示 $t$ 。

> $s$
> 
> $t$

### Output

输出一个整数，表示在 $s$ 的子序列中 $t$ 出现的个数。

### Sample Input 1

```txt showLineNumbers=false
rabbbit
rabbit
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
babgbag
bag
```

### Sample Output 2

```txt showLineNumbers=false
5
```

## 题目要点解析



## 最短公共父序列

[题目链接](https://leetcode.cn/problems/shortest-common-supersequence/description/)

### Problem Statement

给出两个字符串 `str1` 和 `str2` ，返回同时以 `str1` 和 `str2` 作为 **子序列** 的最短字符串。如果答案不止一个，则可以返回满足条件的 **任意一个** 答案。

如果从字符串 $T$ 中删除一些字符（也可能不删除），可以形成字符串 $S$ ，那么 $S$ 就是 $T$ 的子序列。

### Constraints

- $1 \leq str1.length, str2.length \leq 1000$
- `str1` 和 `str2` 仅由小写英文字母组成

### Input

输入包含两行：

- 第一行包含一个字符串，表示 $str1$ 。
- 第二行包含一个字符串，表示 $str2$ 。

> $str1$
> 
> $str2$

### Output

输出一个字符串，表示满足条件的最短公共超序列。

### Sample Input 1

```txt showLineNumbers=false
abac
cab
```

### Sample Output 1

```txt showLineNumbers=false
cabac
```

### Sample Input 2

```txt showLineNumbers=false
aaaaaaaa
aaaaaaaa
```

### Sample Output 2

```txt showLineNumbers=false
aaaaaaaa
```

## 题目要点解析



## 最低的编辑距离

[题目链接](https://leetcode.cn/problems/edit-distance/description/)

### Problem Statement

给你两个单词 `word1` 和 `word2` ， 请返回将 `word1` 转换成 `word2` 所使用的最少操作数。

你可以对一个单词进行如下三种操作：

- 插入一个字符
- 删除一个字符
- 替换一个字符

### Constraints

- $0 \leq word1.length, word2.length \leq 500$
- `word1` 和 `word2` 仅由小写英文字母组成

### Input

输入包含两行：

- 第一行包含一个字符串，表示 $word1$ 。
- 第二行包含一个字符串，表示 $word2$ 。

> $word1$
> 
> $word2$

### Output

输出一个整数，表示将 $word1$ 转换成 $word2$ 所需的最少操作数。

### Sample Input 1

```txt showLineNumbers=false
horse
ros
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
intention
execution
```

### Sample Output 2

```txt showLineNumbers=false
5
```

## 题目要点解析



## 交错字符串问题

[题目链接](https://leetcode.cn/problems/interleaving-string/description/)

### Problem Statement

给定三个字符串 `s1` 、`s2` 、`s3`，请你帮忙验证 `s3` 是否是由 `s1` 和 `s2` **交错** 组成的。

两个字符串 `s` 和 `t` 交错的定义与过程如下，其中每个字符串都会被分割成若干 **非空** 子字符串：

- $s = s_1 + s_2 + \ldots + s_n$
- $t = t_1 + t_2 + \ldots + t_m$
- 如果 $|n - m| \leq 1$ ，且满足下述任意一种拼接顺序，则认为其是交错的：
    - $s_1 + t_1 + s_2 + t_2 + s_3 + t_3 + \ldots$
    - $t_1 + s_1 + t_2 + s_2 + t_3 + s_3 + \ldots$

**注意**：$a + b$ 表示字符串 $a$ 和 $b$ 连接。

### Constraints

- $0 \leq s1.length, s2.length \leq 100$
- $0 \leq s3.length \leq 200$
- `s1` 、`s2` 、`s3` 均由小写英文字母组成

### Input

输入包含三行：

- 第一行包含一个字符串，表示 $s1$ 。
- 第二行包含一个字符串，表示 $s2$ 。
- 第三行包含一个字符串，表示 $s3$ 。

> $s1$
> 
> $s2$
> 
> $s3$

### Output

如果 `s3` 是由 `s1` 和 `s2` 交错组成的，输出 `true` ；否则，输出 `false` 。

### Sample Input 1

```txt showLineNumbers=false
aabcc
dbbca
aadbbcbcac
```

### Sample Output 1

```txt showLineNumbers=false
true
```

### Sample Input 2

```txt showLineNumbers=false
aabcc
dbbca
aadbbbaccc
```

### Sample Output 2

```txt showLineNumbers=false
false
```

### Sample Input 3

```txt showLineNumbers=false
""
""
""
```

### Sample Output 3

```txt showLineNumbers=false
true
```

## 题目要点解析



## 正则表达式匹配

[题目链接](https://leetcode.cn/problems/regular-expression-matching)

### Problem Statement

给你一个字符串 `s` 和一个字符规律 `p` ，请你来实现一个支持 `'.'` 和 `'*'` 的正则表达式匹配。

- `'.'` 匹配任意单个字符
- `'*'` 匹配零个或多个前面的那一个元素

所谓匹配，是要涵盖 **整个** 字符串 `s` 的，而不是部分字符串。

### Constraints

- $1 \leq s.length \leq 20$
- $1 \leq p.length \leq 20$
- `s` 只包含从 `a-z` 的小写字母
- `p` 只包含从 `a-z` 的小写字母，以及字符 `.` 和 `*`
- 保证每次出现字符 `*` 时，前面都匹配到有效的字符

### Input

输入包含两行：

- 第一行包含一个字符串，表示 $s$ 。
- 第二行包含一个字符串，表示 $p$ 。

> $s$
> 
> $p$

### Output

如果输入字符串 $s$ 与字符规律 $p$ 匹配，输出 `true` ；否则，输出 `false` 。

### Sample Input 1

```txt showLineNumbers=false
aa
a
```

### Sample Output 1

```txt showLineNumbers=false
false
```

### Sample Input 2

```txt showLineNumbers=false
aa
a*
```

### Sample Output 2

```txt showLineNumbers=false
true
```

### Sample Input 3

```txt showLineNumbers=false
ab
.*
```

### Sample Output 3

```txt showLineNumbers=false
true
```

## 题目要点解析

最长公共子序列+完全背包思想

---

# 参考文献列表

1. [【Luogu 博客】最长公共子序列问题](https://www.luogu.com/article/ml584xxs)