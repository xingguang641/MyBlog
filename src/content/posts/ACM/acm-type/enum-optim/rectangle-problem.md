---
title: 【ACM 算法题单】矩形相关问题
published: 2025-12-13
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 矩形累加和问题

矩形累加和是矩形类问题中最基础、也最常见的一类题型。如果我们要在二维矩阵中寻找累加和最大的子矩形，最直接的思路是枚举矩形的左上角和右下角，从而确定出一个子矩形并计算其元素之和。然而在这种朴素做法中，整体枚举复杂度高达 $O(n^4)$ ，在实际题目中往往是 **无法接受的** 。为了降低复杂度，我们不再同时枚举四条边，而是只枚举矩形的上下边界，然后将这两条边之间的所有行压缩到一维数组中。这样一来，原本的二维矩形问题就被转化为一维区间问题。

在完成压缩之后，问题的本质便转变为 **在一个一维数组中寻找满足题目条件的子区间** 。此时，我们可以直接套用各种成熟的一维算法，例如前缀和、哈希表、双指针或最大子段和等经典方法，从而高效地求解矩形的左右边界。通过这种典型的 **二维转一维** 技巧，我们成功地将整体时间复杂度优化到了 $O(n^3)$ ，这一复杂度在大多数矩形累加和相关问题中都足够高效，也构成了此类题目的 **核心解题框架** 。

## 子矩阵的最大和

[题目链接](https://leetcode.cn/problems/max-submatrix-lcci)

### Problem Statement

给定一个正整数、负整数和 $0$ 组成的 $N × M$ 矩阵，编写代码找出元素总和最大的子矩阵。

返回一个数组 `[r1, c1, r2, c2]` ，其中 `r1, c1` 分别代表子矩阵左上角的行号和列号，`r2, c2` 分别代表右下角的行号和列号。若有多个满足条件的子矩阵，返回任意一个均可。

### Constraints

- $1 \leq matrix.length \leq 200$
- $1 \leq matrix[0].length \leq 200$

### Input

输入包含多行：

- 第一行包含两个整数 $N$ 和 $M$ ，表示矩阵大小。
- 接下来 $M$ 行包含 $N$ 个整数，表示矩阵的一行。

### Output

输出一个四元组表示答案矩阵的坐标。

### Sample Input

```txt showLineNumbers=false
2 2
-1 0
0 -1
```

### Sample Output

```txt showLineNumbers=false
0 1 0 1
```

## 题目要点解析



## 均衡的矩形计数

[题目链接](https://atcoder.jp/contests/abc410/tasks/abc410_f)

### Problem Statement

给定一个 $H \times W$ 的网格，每个单元格包含 `#` 或 `.` 。每个单元格中的符号信息由 $H$ 个长度为 $W$ 的字符串 $S_1, S_2, \ldots, S_H$ 给出，其中第 $i$ 行第 $j$ 列的单元格包含与 $S_i$ 的第 $j$ 个字符相同的符号。

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
- 所有测试用例中 $H \times W$ 的总和不超过 $3 \times 10^5$
- $S_i$ 是长度为 $W$ 的由 `#` 和 `.` 组成的字符串

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

对于每个测试用例：

- 第一行包含两个整数 $H$ 和 $W$ ，表示网格的大小。
- 接下来的 $H$ 行，每行包含一个长度为 $W$ 的字符串。

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

输出 $T$ 行，第 $i$ 行应该包含第 $i$ 个测试用例的答案。

### Sample Input

```txt showLineNumbers=false
3
3 2
##
#.
..
6 6
..#...
..#..#
#.#.#.
.###..
######
.###..
15 50
.......................#...........###.###.###.###
....................#..#..#..........#.#.#...#.#..
.................#...#####...#.....###.#.#.###.###
..................#..##.##..#......#...#.#.#.....#
...................#########.......###.###.###.###
....................#.....#.......................
.###........##......#.....#..#...#.####.####.##..#
#..#.........#......#.....#..#...#.#....#....##..#
#..#.........#......#.....#..#...#.#....#....##..#
#.....##...###..##..#.....#..#...#.#....#....#.#.#
#....#..#.#..#.#..#.#..##.#..#...#.####.####.#.#.#
#....#..#.#..#.####.#....##..#...#.#....#....#.#.#
#....#..#.#..#.#....#.....#..#...#.#....#....#..##
#..#.#..#.#..#.#..#.#....#.#.#...#.#....#....#..##
.##...##...####.##...####..#..###..####.####.#..##
```

### Sample Output

```txt showLineNumbers=false
4
79
4032
```

## 题目要点解析



---

# 完全子矩形问题

完全子矩形（元素全为 $1$ 的矩形）是矩形类问题中第二类典型题型。与前一种矩形累加和问题相同，如果直接通过枚举子矩形的左上角和右下角来确定一个矩形，其时间复杂度会非常高，在数据规模稍大的情况下难以通过，因此我们需要找到新的枚举思路。不同于矩形累加和问题，完全子矩形问题不需要枚举矩形的上下边界，只需要单独 **枚举矩形的底边** 即可。以当前行为底边向上延伸，我们可以统计出每一列中连续为 $1$ 的高度，从而将原本的二维矩形问题转化为一维柱状图问题。此时，问题等价于 **「柱状图中最大的矩形」** 这一经典题目。

由于「柱状图中最大的矩形」这一经典问题可以借助单调栈在 $O(n)$ 的时间内高效解决，当我们将矩阵中的每一行依次视为矩形的底边并进行处理时，整体时间复杂度便可以稳定地控制在 $O(n^2)$ 。在这一过程中，二维矩形问题被系统性地转化为一维柱状图问题，从而利用「柱状图中最大的矩形」这一成熟的算法工具。这种处理方式有效避免了对矩形四条边进行高维度暴力枚举，是解决完全子矩形问题时最为常见、也最为标准的思路。

## 柱状图最大矩形

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



## 最大的全一矩形

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



## 全一矩形的个数

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



## 寻找高光的片段

[题目链接](https://atcoder.jp/contests/abc420/tasks/abc420_f)

### Problem Statement

给定一个 $N \times M$ 的网格。每个单元格包含 `.` 或 `#` 。每个单元格中的符号信息由 $N$ 个字符串 $S_1, S_2, \ldots, S_N$ 给出，其中第 $i$ 行第 $j$ 列的单元格包含与 $S_i$ 的第 $j$ 个字符相同的符号。有多少个最多包含 $K$ 个单元格的矩形区域，使得所有单元格都包含 `.` ？

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
- $S_i$ 是长度为 $M$ 且由 `.` 和 `#` 组成的字符串

### Input

输入包含多行：

- 第一行包含三个整数 $N$ 、$M$ 和 $K$ 。
- 接下来的 $N$ 行，每行包含一个长度为 $M$ 的字符串。

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

