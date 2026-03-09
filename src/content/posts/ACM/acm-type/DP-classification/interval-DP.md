---
title: 【ACM 算法题单】区间动态规划相关问题
published: 2026-03-01
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type, Mex]
category: ACM Type
draft: false
---

# 区间动态规划问题

区间动态规划是一类以区间 $[l,r]$ 作为状态单位的动态规划模型，通常定义 $dp[l][r]$ 表示区间 $[l,r]$ 内某种性质的最优值或可行性结果。这类问题的核心特征在于：状态天然依赖左右端点，转移围绕区间边界关系或区间划分方式展开。与线性 DP 不同，它关注的不是 “当前位置如何由前一位置转移” ，而是 **一个区间如何由更小的区间构成** 。

从结构角度来看，区间 DP 的转移方式大致可以归纳为两类：**端点拓展型** 与 **区间分治型** 。以有效括号为例，合法结构既可以嵌套，如 “(())” ，即外层括号包裹内部合法结构；也可以并列，如 “()()” ，表示两个合法结构的拼接。这两种结构形态，恰好对应区间 DP 的两种典型转移方式。

端点拓展型强调左右端点之间的匹配关系。其典型形式是当区间两端满足某种条件时，可以由内部区间转移而来：

$$
dp[l][r] \longleftarrow dp[l+1][r-1]
$$

这种转移隐含的是一种 **嵌套结构**：外层包裹内层，小区间被包含在大区间之中。最经典的例子便是嵌套型有效括号。嵌套形式正对应端点拓展型转移，因为区间是否合法取决于两端是否匹配以及内部区间是否合法。类似地，回文子序列或回文子串问题也可以视为一种对称嵌套结构：当两端字符相同，整体性质由内部区间决定，因此自然采用端点拓展型的转移方式。

另一类是区间分治型转移，其核心思想是通过枚举划分点，将区间拆分为左右两个子区间后再合并答案：

$$
dp[l][r] = \min_{k \in [l,r)} \big( dp[l][k] + dp[k+1][r] \big)
$$

这种形式强调的是 **并列结构**：一个区间的最优解可以由两个相邻子区间的最优解组合得到。有效括号中的并列结构正体现了这一点，而我们枚举的 $k$ ，本质上就是在寻找 “()()” 中间的那条分界线，从而把整体拆解为两个相互独立的合法区间。

从另一个角度看，区间分治型还可以理解为一种 **二叉分治结构** 。我们枚举的划分点 $k$ ，可以看作当前区间在 “最后一步操作” 或 “第一次操作” 中选定的关键位置。若把 $k$ 视为一棵二叉树的根节点，那么区间 $[l,k]$ 与 $[k+1,r]$ 分别对应左右子树；随后对子区间继续递归分解，整个决策过程便对应一棵递归生成的二叉结构。许多区间类问题（如表达式加括号、区间合并、构造最优二叉结构等）都可以从这种 “选定一个结构中心，再递归处理左右子区间” 的视角来理解，其本质都属于区间分治型转移。

从更抽象的层面来看，几乎所有区间 DP 问题都可以在结构上归结为 **嵌套关系** 或 **并列关系**：要么是外层包裹内层的递归结构，要么是通过选择一个划分点构造分治结构。一旦识别出问题中隐藏的这一层结构关系，就能够自然确定应采用端点拓展还是区间分治的转移方式，从而建立起清晰而系统的区间动态规划模型。

## 最长回文子序列

[题目链接](https://leetcode.cn/problems/longest-palindromic-subsequence/)

### Problem Statement

给定一个字符串 `s` ，找到它的 **最长回文子序列** 的长度。子序列是从原字符串中删除部分字符后留下的序列，并 **不改变剩余字符的顺序** 。回文序列是正读和反读都相同的字符串。

例如，字符串 `"bbbab"` 的最长回文子序列是 `"bbbb"` ，长度为 `4` 。

### Constraints

- $1 \leq s.length \leq 1000$
- `s` 仅由小写英文字母组成

### Input

输入包含一行：

- 该行包含一个字符串 `s` 。

> $s$

### Output

输出一个整数，表示字符串 `s` 的最长回文子序列的长度。

### Sample Input 1

```txt showLineNumbers=false
bbbab
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
cbbd
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析

嵌套类型题

## 构造回文字符串

[题目链接](https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/description/)

### Problem Statement

给定一个字符串 `s` ，你可以在 **任意位置插入字符** 使得这个字符串变成 **回文串** 。请返回使字符串成为回文串所需要的 **最少插入次数** 。

注意，插入字符不会删除原有字符，你可以在字符串的头部、尾部或中间任意位置插入字符。

### Constraints

- $1 \leq s.length \leq 500$
- `s` 仅由小写英文字母组成

### Input

输入包含一行：

- 该行包含一个字符串 `s` 。

> $s$

### Output

输出一个整数，表示将字符串 `s` 变成回文串所需的最少插入次数。

### Sample Input 1

```txt showLineNumbers=false
zzazz
```

### Sample Output 1

```txt showLineNumbers=false
0
```

### Sample Input 2

```txt showLineNumbers=false
mbadm
```

### Sample Output 2

```txt showLineNumbers=false
2
```

### Sample Input 3

```txt showLineNumbers=false
leetcode
```

### Sample Output 3

```txt showLineNumbers=false
5
```

## 题目要点解析

嵌套类型题

## 基于数组的博弈

[题目链接](https://leetcode.cn/problems/predict-the-winner/description/)

### Problem Statement

给定一个长度为 $N$ 的整数数组 `nums` ，两位玩家轮流进行游戏，每一轮玩家从数组的 **最左端或最右端** 选择一个数字取走，取走后该数字从数组中移除。两位玩家都采用 **最优策略** 玩游戏。

玩家 $1$ 先手，玩家 $2$ 后手。游戏结束后，玩家 $1$ 和玩家 $2$ 分别拥有自己的数字总和。请你预测 **先手玩家是否能够获胜**（即先手玩家的总和大于或等于后手玩家的总和）。

如果先手玩家有获胜的策略，则返回 `true` ，否则返回 `false`。

### Constraints

* $1 \leq N \leq 20$
* $0 \leq nums[i] \leq 10^7$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示数组 `nums` 的长度。
- 第二行包含 $N$ 个整数，表示数组中的各个元素。

> $N$
> 
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个布尔值（ `true` 或 `false` ），表示在双方采用最优策略的情况下，先手玩家是否能够获胜。

### Sample Input 1

```txt showLineNumbers=false
5
1 5 2 4 6
```

### Sample Output 1

```txt showLineNumbers=false
true
```

### Sample Input 2

```txt showLineNumbers=false
4
1 5 233 7
```

### Sample Output 2

```txt showLineNumbers=false
true
```

## 题目要点解析

题目明示端点扩展

## 多边形三角剖分

[题目链接](https://leetcode.cn/problems/minimum-score-triangulation-of-polygon/)

### Problem Statement

给你一个 **凸多边形** 的顶点数 $n$ 和一个长度为 $n$ 的整数数组 `values` ，其中 `values[i]` 表示第 $i$ 个顶点的权值。

对于一个凸多边形的三角剖分，每次选取三个顶点组成一条三角形，并将该三角形一分为二直到整个多边形被划分成非重叠三角形。
定义三角剖分的 **得分** 为所有组成三角形的权值乘积之和，每个三角形的得分为三个顶点对应权值的乘积。

请返回这个凸多边形所有合法三角剖分中能够得到的 **最低得分** 。

### Constraints

* $3 \leq values.length \leq 50$
* $1 \leq values[i] \leq 100$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示顶点数（也是数组长度）。
- 第二行包含 $N$ 个整数，表示数组 `values` 中每个顶点的权值。

> $N$
> 
> $values_1 \quad values_2 \quad \ldots \quad values_N$

### Output

输出一个整数，表示所有合法三角剖分中能得到的最低得分。

### Sample Input 1

```txt showLineNumbers=false
3
1 2 3
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
4
3 7 4 5
```

### Sample Output 2

```txt showLineNumbers=false
144
```

## 题目要点解析



## 打气球最大得分

[题目链接](https://leetcode.cn/problems/burst-balloons/)

### Problem Statement

有若干个气球排成一排，第 $i$ 个气球的数字为 `nums[i]` 。当你戳破一个气球时，你将获得的金币数等于该气球左侧和右侧未被戳破气球的数字乘积再乘以该气球本身的数字。如果某一侧已经没有未戳破的气球，则视为其数字为 $1$ 。

换句话说，假设你依次戳破气球的顺序为 $i_1, i_2, \ldots, i_n$，戳破第 $k$ 个气球时获得的金币为：

$$
coins = nums[i_k] × left × right
$$

其中 `left` 是第 $i_k$ 个气球左边尚未被戳破的气球数字（若不存在则为 $1$），`right` 是第 $i_k$ 个气球右边尚未被戳破的气球数字（若不存在则为 $1$ ）。

请返回你能获得的 **最大金币数** 。

### Constraints

* $1 \leq nums.length \leq 300$
* $0 \leq nums[i] \leq 1000$

### Input

输入包含两行：

* 第一行包含一个整数 $N$ ，表示气球的数量。
* 第二行包含 $N$ 个整数，表示数组 `nums` 中每个气球的数字。

> $N$
> 
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数，表示能获得的最大金币数。

### Sample Input 1

```txt showLineNumbers=false
4
3 1 5 8
```

### Sample Output 1

```txt showLineNumbers=false
167
```

### Sample Input 2

```txt showLineNumbers=false
1
5
```

### Sample Output 2

```txt showLineNumbers=false
5
```

## 题目要点解析



## 布尔运算表达式

[题目链接](https://leetcode.cn/problems/boolean-evaluation-lcci/description/)

### Problem Statement

给定一个只包含字符 `'0'` 、`'1'` 和布尔运算符 `'&'` 、`'|'` 、`'^'` 的字符串 `s` 以及一个布尔值 `result` 。
你需要统计有多少种不同的方式，在运算表达式中加入括号，使得整个表达式的计算结果为 `result` 。

布尔运算规则如下：

* `'&'` 表示逻辑与，如果左右两边都为真（ `1` ）则结果为真，否则为假（ `0` ）。
* `'|'` 表示逻辑或，只要左右任意一侧为真（ `1` ）则结果为真。
* `'^'` 表示逻辑异或，当左右两侧不同时结果为真。

你需要返回使表达式结果为给定 `result` 的 **不同括号组合的数量** 。

### Constraints

- $1 \leq s.length \leq 19$
- `s` 由数字 `'0'` 、`'1'` 与运算符 `'&'` 、`'|'` 、`'^'` 交替组成（即操作数与运算符交替出现）
- `result` 为布尔值（ `true` 或 `false` ）

### Input

输入包含两行：

* 第一行包含一个字符串 `s` ，表示布尔运算表达式。
* 第二行包含一个整数 `result` ，若为 `1` 表示目标结果为 `true` ，若为 `0` 表示目标结果为 `false` 。

> $s$
> 
> $result$

### Output

输出一个整数，表示所有不同的括号插入方式中，能够让表达式计算结果等于 `result` 的方案数。

### Sample Input 1

```txt showLineNumbers=false
1^0|0|1
0
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
0&0&0&1^1|0
1
```

### Sample Output 2

```txt showLineNumbers=false
10
```

## 题目要点解析

嵌套类型题

## 有效括号字符串

[题目链接](https://www.nowcoder.com/practice/e391767d80d942d29e6095a935a5b96b)

### Problem Statement

给定一个由 `'['` 、`']'` 、`'('` 、`')'` 组成的字符串，请问最少插入多少个括号才能使这个字符串的所有括号 **左右配对** 。

例如，当前字符串是 `"([[])"` ，那么插入一个 `']'` 即可满足所有括号匹配的要求。

### Constraints

* 字符串长度满足一定范围（具体原题未明示，但可认为长度 $\leq 10^5 $ ）
* 字符串仅由上述 $4$ 种括号字符组成

### Input

输入包含一行：

- 该行包含一个只由 `'['` 、`']'` 、`'('` 、`')'` 组成的字符串 `s` 。

> $s$

### Output

输出一个整数，表示使字符串所有括号配对所需插入的最少括号数。

### Sample Input 1

```txt showLineNumbers=false
([[])
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
([])[]
```

### Sample Output 2

```txt showLineNumbers=false
0
```

## 题目要点解析



## 奇怪的打印机

[题目链接](https://leetcode.cn/problems/strange-printer/)

### Problem Statement

有台奇怪的打印机，它每次可以打印一串 **相同字符** 的序列，也就是说每次打印过程只能选择一个字符并将其连续地打印在一段区间上。

给你一个字符串 `s` ，奇怪的打印机最开始是空的，它可以在任意位置开始打印。每次打印它会选择一个区间并将同一个字符覆盖写入，在这个过程中会覆盖掉原来存在的字符。

请问这台打印机 **打印出字符串 `s` 最少需要多少次打印操作** 。

### Constraints

- $1 \leq s.length \leq 100$
- `s` 由小写英文字母组成

### Input

输入包含一行：

- 该行包含一个字符串 `s` 。

> $s$

### Output

输出一个整数，表示奇怪的打印机打印出字符串 `s` 最少需要的操作次数。

### Sample Input 1

```txt showLineNumbers=false
aba
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
aaabbb
```

### Sample Output 2

```txt showLineNumbers=false
2
```

## 题目要点解析

尝试找到题目中的嵌套、并列关系

## 合唱班站队问题

[题目链接](https://www.luogu.com.cn/problem/P3205)

### Problem Statement

为了在晚会上有更好的演出效果，小 A 需要按照身高将合唱队的人排成一个队形。合唱队共有 $n$ 个人，编号从 $1$ 到 $n$ ，第 $i$ 个人的身高为 $h_i$ ，且所有身高互不相同。

小 A 想知道有多少种 **初始队形排列** 能够最终生成他理想中的队形。生成过程如下：

* 首先，所有人按某种顺序站成一个初始队形；
* 然后从左到右依次将每个人插入新的队列中。

  * 第一个人直接进入空队列；
  * 对于后面的每个人，如果他比队列中最后一个人高，则将他插入队列的 **最右边** ；
  * 如果他比队列中最后一个人矮，则将他插入队列的 **最左边** 。

当所有人都插入结束后，就得到一个最终队形。如果最终队形恰好与给定的理想队形一致，则认为这个初始队形是合法的。

请你计算 **所有能生成理想队形的初始队形数量** ，并输出答案对 $19650827$ 取模后的结果。

### Constraints

* $1 \leq n \leq 1000$
* $1000 \leq h_i \leq 2000$
* 所有身高互不相同

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示队伍中人的数量。
- 第二行包含 $N$ 个整数，表示理想队形中每个人的身高。

> $N$
>
> $h_1 \quad h_2 \quad \ldots \quad h_N$

### Output

输出一个整数，表示满足条件的合法初始队形数量对 $19650827$ 取模后的结果。

### Sample Input 1

```txt showLineNumbers=false
3
1 2 3
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
4
2 1 4 3
```

### Sample Output 2

```txt showLineNumbers=false
8
```

## 题目要点解析

题目明示端点扩展

## 移除盒子难题

[题目链接](https://leetcode.cn/problems/remove-boxes/)

### Problem Statement

给你一个由数字表示的盒子序列 `boxes` ，每个盒子的颜色由一个正整数表示。你可以执行以下操作：

每一次操作，你可以选择 **连续的一组颜色相同的盒子**（长度至少为 $1$ ），将这一组盒子取出并获得积分。取出长度为 $k$ 的这一组盒子后，你将获得的积分为 $k^2$ 。

取出之后，剩余的盒子会重新拼接成一个新的连续序列。你可以重复执行上述操作，直到所有盒子都被取出。

请返回你能获得的 **最大积分数** 。

### Constraints

- $1 \leq boxes.length \leq 100$
- $1 \leq boxes[i] \leq 100$

### Input

输入包含两行：

- 第一行包含一个整数 $N$ ，表示盒子数量。
- 第二行包含 $N$ 个整数，表示数组 `boxes` 中每个盒子的颜色。

> $N$
> 
> $boxes_1 \quad boxes_2 \quad \ldots \quad boxes_N$

### Output

输出一个整数，表示能够获得的最大积分数。

### Sample Input 1

```txt showLineNumbers=false
9
1 3 2 2 2 3 4 3 1
```

### Sample Output 1

```txt showLineNumbers=false
23
```

### Sample Input 2

```txt showLineNumbers=false
5
1 1 1 1 1
```

### Sample Output 2

```txt showLineNumbers=false
25
```

## 题目要点解析

尝试找到题目中的嵌套、并列关系

## 不同的回文序列

[题目链接](https://leetcode.cn/problems/count-different-palindromic-subsequences/)

### Problem Statement

给定一个字符串 `s` ，请你统计其中 **不同的非空回文子序列** 的个数。

注意：

* 子序列定义为可以通过删除原字符串中任意位置的字符（可能不连续）得到的新字符串；
* 只统计 **不同的回文子序列** ，重复的回文序列只计数一次；
* 最终结果可能很大，请返回答案对 $10^9 + 7$ 取模的值。

### Constraints

- $1 \leq s.length \leq 1000$
- `s` 仅由小写英文字母组成

### Input

输入包含一行：

- 该行包含一个字符串 `s` 。

> $s$

### Output

输出一个整数，表示字符串 `s` 中不同的非空回文子序列的数量，对 $10^9 + 7$ 取模后的结果。

### Sample Input 1

```txt showLineNumbers=false
bccb
```

### Sample Output 1

```txt showLineNumbers=false
6
```

### Sample Input 2

```txt showLineNumbers=false
aaa
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析

嵌套类型题

## 最高加分二叉树

[题目链接](https://www.luogu.com.cn/problem/P1040)



## 题目要点解析



---

# 参考文献列表

1. [区间 DP 详解](https://blog.csdn.net/fgddfjhdhj/article/details/149242740)