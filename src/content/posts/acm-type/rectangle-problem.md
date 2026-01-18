---
title: 【ACM 算法题单】矩形相关问题
published: 2025-12-13
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type, Grid Graph]
category: ACM Type
draft: false
---

# 矩形累加和问题

矩形累加和是矩形类问题中最基础、也最常见的一类题型。对于一个二维矩阵，最直接的思路是枚举矩形的左上角和右下角位置，从而确定出一个子矩形并计算其元素之和。然而在这种朴素做法中，左上角的选择需要 $O(n^2)$ 的时间，右下角同样需要 $O(n^2)$ 的时间，整体枚举复杂度高达 $O(n^4)$ ，在实际题目中往往是 **无法接受的** 。

为了降低复杂度，我们需要重新审视 “枚举矩形” 这一过程。一个常见且行之有效的优化思路是：**不再同时枚举四条边，而是固定其中的两条边** 。具体来说，我们只枚举矩形的上边界和下边界，将这两条边之间的所有行压缩到一维数组中。这样一来，原本的二维矩形问题就被转化为了一个一维区间问题。

在完成压缩之后，问题的本质便转变为：**在一个一维数组中，寻找满足题目条件的子区间** 。此时，我们可以直接套用各种成熟的一维算法，例如前缀和、哈希表、双指针或最大子段和等经典方法，从而高效地枚举左右边界。通过这种典型的 **“二维转一维”** 技巧，我们将整体时间复杂度成功优化到了 $O(n^3)$ ，这一复杂度在大多数矩形累加和相关问题中都足够高效，也构成了此类题目的 **核心解题框架** 。

## 均衡矩形计数

[题目链接](https://atcoder.jp/contests/abc410/tasks/abc410_f)

### Problem Statement

给定一个 $H \times W$ 的网格，每个单元格包含 `#` 或 `.` 。

每个单元格中的符号信息由 $H$ 个长度为 $W$ 的字符串 $S_1, S_2, \ldots, S_H$ 给出，其中第 $i$ 行第 $j$ 列的单元格包含与 $S_i$ 的第 $j$ 个字符相同的符号。

找出满足以下所有条件的矩形区域的数量：

- 矩形区域内包含 `#` 的单元格数量和包含 `.` 的单元格数量相等。

正式地，找出满足以下所有条件的整数四元组 $(u, d, l, r)$ 的数量：

- $1 \leq u \leq d \leq H$
- $1 \leq l \leq r \leq W$

当从第 $u$ 行到第 $d$ 行以及从第 $l$ 列到第 $r$ 列提取网格的一部分时，提取部分中包含 `#` 的单元格数量和包含 `.` 的单元格数量相等。

你有 $T$ 个测试用例。对每个测试用例找出答案。

### Constraints

- $1 \leq T \leq 25000$
- $1 \leq H, W$
- 所有测试用例在一个输入中的 $H \times W$ 之和不超过 $3 \times 10^5$
- $S_i$ 是长度为 $W$ 的由 `#` 和 `.` 组成的字符串

### Input

输入从标准输入中以以下格式给出：

> $T$
>
> $case_1$
>
> $case_2$
>
> $\ldots$
>
> $case_T$

$case_i$ 表示第 $i$ 个测试用例。每个测试用例的格式如下：

> $H \quad W$
>
> $S_1$
>
> $S_2$
>
> $\ldots$
>
> $S_H$

### Output

输出 $T$ 行。第 $i$ 行应该包含第 $i$ 个测试用例的答案。

## 题目要点解析



---

# 完全子矩形问题

完全子矩形是矩形类问题中的第二类典型题型。与前一种矩形累加和问题类似，如果直接通过枚举子矩形的左上角和右下角来确定一个矩形，其时间复杂度同样会非常高，在数据规模稍大的情况下往往难以通过。尤其是在需要对每一个候选矩形进行额外判定或计算时，这种朴素枚举方法在实际题目中显然是不可接受的，因此必须寻找更加高效的枚举方式。

不同于矩形累加和问题需要枚举上下两条边，完全子矩形问题通常不再显式枚举矩形的上下边界，而是选择 **枚举矩形的底边** 作为切入点。以当前行为底边向上延伸，我们可以统计每一列中连续满足条件的高度，从而将原本的二维矩形问题转化为一个一维的柱状图问题。此时，问题等价于求解 **「柱状图中最大的矩形」** 这一经典题目。

由于「柱状图中最大的矩形」这一经典问题可以借助单调栈在 $O(n)$ 的时间内高效解决，因此，当我们将矩阵中的每一行依次视为矩形的底边并进行处理时，整体时间复杂度便可以稳定地控制在 $O(n^2)$ 。在这一过程中，二维矩形问题被系统性地转化为一系列一维柱状图问题，从而充分利用了成熟的一维算法工具。这种处理方式有效避免了对矩形四条边进行高维度的暴力枚举，大幅降低了计算复杂度，是解决完全子矩形问题时最为常见、也最为标准的解题思路。

## 寻找最大矩形

[题目链接](https://leetcode.cn/problems/largest-rectangle-in-histogram/description/)

### Problem Statement

给定 $n$ 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 $1$ 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。

### Constraints

- $1 \leq heights.length \leq 10^5$
- $0 \leq heights[i] \leq 10^4$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示数组中的各个元素。

> $n$
> 
> $heights_1 \quad heights_2 \quad \ldots \quad heights_n$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
6
2 1 5 6 2 3
```

### Sample Output 1

```txt showLineNumbers=false
10
```

### Sample Input 2

```txt showLineNumbers=false
2
2 4
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析



## 统计全 1 矩形

[题目链接](https://leetcode.cn/problems/count-submatrices-with-all-ones/description/)

### Problem Statement

给你一个 `m x n` 的二进制矩阵 `mat` ，请你返回有多少个 **子矩形** 的元素全部都是 $1$ 。

### Constraints

- $1 \leq m, n \leq 150$
- $mat[i][j]$ 仅包含 $0$ 或 $1$

### Input

输入包含多行：

- 第一行包含两个整数 $m$ 和 $n$ ，表示矩阵大小。
- 接下来 $m$ 行包含 $n$ 个整数，表示矩阵的一行。

> $m \quad n$
> 
> $mat_{1, 1} \quad mat_{1, 2} \quad \ldots \quad mat_{1, n}$
> 
> $\ldots$
> 
> $mat_{h, 1} \quad mat_{h, 2} \quad \ldots \quad mat_{m, n}$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3 3
1 0 1
1 1 0
1 1 0
```

### Sample Output 1

```txt showLineNumbers=false
13
```

### Sample Input 2

```txt showLineNumbers=false
3 4
0 1 1 0
0 1 1 1
1 1 1 0
```

### Sample Output 2

```txt showLineNumbers=false
24
```

## 题目要点解析



## 最大子矩形

[题目链接](https://leetcode.cn/problems/PLYXKQ/description/)

### Problem Statement

给定一个由 $0$ 和 $1$ 组成的矩阵 `matrix` ，找出只包含 $1$ 的最大矩形，并返回其面积。

注意：此题 `matrix` 输入格式为一维 $01$ 字符串数组。

### Constraints

- $rows == matrix.length$
- $cols == matrix[0].length$
- $0 <= row, cols <= 200$
- $matrix[i][j]$ 仅包含 $0$ 或 $1$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示矩阵的行数。
- 接下来 $n$ 行包含一个字符串，表示矩阵的一行。

> $n$
> 
> $S_1$
> 
> $\ldots$
> 
> $S_2$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
4
10100
10111
11111
10010
```

### Sample Output 1

```txt showLineNumbers=false
6
```

## 题目要点解析



### Problem Statement

给定一个由 $0$ 和 $1$ 组成的矩阵 `matrix` ，找出只包含 $1$ 的最大矩形，并返回其面积。

注意：此题 `matrix` 输入格式为一维 $01$ 字符串数组。

### Constraints

- $rows == matrix.length$
- $cols == matrix[0].length$
- $0 <= row, cols <= 200$
- $matrix[i][j]$ 仅包含 $0$ 或 $1$

### Input

输入包含多行：

- 第一行包含一个整数 $n$ ，表示矩阵的行数。
- 接下来 $n$ 行包含一个字符串，表示矩阵的一行。

> $n$
> 
> $S_1$
> 
> $\ldots$
> 
> $S_2$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
4
10100
10111
11111
10010
```

### Sample Output 1

```txt showLineNumbers=false
6
```

## 寻找高光片段

[题目链接](https://atcoder.jp/contests/abc420/tasks/abc420_f)

### Problem Statement

给定一个 $N \times M$ 的网格。每个单元格包含 `.` 或 `#` 。

每个单元格中的符号信息由 $N$ 个字符串 $S_1, S_2, \ldots, S_N$ 给出，其中第 $i$ 行第 $j$ 列的单元格包含与 $S_i$ 的第 $j$ 个字符相同的符号。

有多少个最多包含 $K$ 个单元格的矩形区域，使得所有单元格都包含 `.` ？

正式地，计算满足以下条件的整数四元组 $(l_x, r_x, l_y, r_y)$ 的数量：

- $1 \leq l_x \leq r_x \leq N$
- $1 \leq l_y \leq r_y \leq M$
- $(r_x - l_x + 1) \times (r_y - l_y + 1) \leq K$

对于所有满足 $l_x \leq i \leq r_x$ 且 $l_y \leq j \leq r_y$ 的整数对 $(i, j)$ ，第 $i$ 行第 $j$ 列的单元格包含 `.` 。

### Constraints

- $N, M, K$ 是整数。
- $1 \leq N, M \leq 5 \times 10^5$
- $1 \leq N \times M \leq 5 \times 10^6$
- $1 \leq K \leq N \times M$
- $S_i$ 是长度为 $M$ 的由 `.` 和 `#` 组成的字符串

### Input

输入从标准输入中以以下格式给出：

> $N \quad M \quad K$
> 
> $S_1$
> 
> $S_2$
> 
> $\ldots$
> 
> $S_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
3 3 4
#..
...
..#
```

### Sample Output 1

```txt showLineNumbers=false
19
```

### Sample Input 2

```txt showLineNumbers=false
7 5 35
.....
.....
.....
.....
.....
.....
.....
```

### Sample Output 2

```txt showLineNumbers=false
420
```

### Sample Input 3

```txt showLineNumbers=false
10 9 25
#.....#..
....#....
.......#.
.........
.......#.
.#.......
.........
#........
........#
.#.....#.
```

### Sample Output 3

```txt showLineNumbers=false
984
```

## 题目要点解析

