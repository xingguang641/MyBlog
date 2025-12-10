---
title: 【ACM 算法随笔】单调数据结构
published: 2025-11-27
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 单调数据结构介绍

在设计算法与解决问题时，我们常常通过识别并利用题目隐含的结构性特征来简化分析与实现，从而在处理大规模数据或频繁更新时仍能保持良好的时间与空间性能。许多的算法题都具备一定的 **单调性** ，而单调性往往都需要数据结构来维护，我们就来仔细介绍一下有哪些常见的单调数据结构。

## 滑动窗口

在各种数组与序列相关的题目中，滑动窗口几乎是最常见、也最实用的技巧之一。它的核心做法很简单：通过两个指针在序列上同步向前移动，始终维护一个当前的区间，并在移动的过程中不断检查区间是否满足题目的要求。

不过，滑动窗口并不是可以随意使用的。它之所以能够高效，是因为许多问题本身具备一种 “关于窗口长度的单调性” 。典型的情形是：**窗口越长越不满足条件，或者窗口越长越容易满足条件** 。只要这种单调性存在，我们在扩张右端点的时候，就能确定左端点应该怎么移动，从而保证整个过程不会出现回退与重复扫描。

![滑动窗口图像](src\content\posts\monotonic-structure\滑动窗口1.png)

一个典型的例子是「子数组和不超过 $k$ 」。如果数组中的元素全部是非负数，那么随着窗口长度增加，窗口的累加和只会上升，不会下降。这样一来，窗口 “越短越满足条件” ，我们就可以放心地在和超过上限时收缩左端点，通过滑动窗口在线性时间内完成整个搜索。但如果数组里出现了负数，累加和就不再单调，此时窗口扩张后可能反而更容易满足条件，单调性被破坏，滑动窗口自然也就失效了，需要换用其他算法。

本质上，只要题目中的判断条件在窗口扩张或收缩过程中呈现出单调变化，我们就可以让窗口在序列上单向滑动，并在这个过程中实时维护答案。对于满足这种性质的问题，滑动窗口往往能将原本需要嵌套循环的枚举过程压缩到 $O(n)$ 的时间，非常适合在大数据规模下使用。

## 单调栈/单调队列

在许多序列相关的问题中，我们不仅需要维护数据的出现顺序，还需要在扫描的过程中持续保持某种局部最优或约束关系。为了让这些结构性的关系在遍历过程中高效地被记录与更新，单调栈与单调队列便成为非常常用的工具。它们的核心思想都是在容器内部维持一种单调性的组织方式，只保留那些未来仍可能发挥作用的元素，而把无关或失效的候选者主动剔除，从而把整个序列的处理成本压缩到线性级别。

从结构上看，栈与队列都属于线性容器，只是在操作端口上存在差异：栈仅允许在一端进行插入与删除，而队列则可以在一端插入、另一端删除。单调栈与单调队列正是基于这两个操作模型发展而来的——它们采用的单调维护原则完全相同，只是接口能力的不同，使得它们在不同类型的问题中展现出不同的侧重点。

**单调栈** 常用于解决 “下一个更大元素” “下一个更小元素” 等结构性问题。借助其单端更新的特性，我们可以在扫描序列时保持栈内的元素递增或递减，从而确保一旦违反单调性，就可以直接剔除失效的数据，让整个结构始终维持最精简的候选集合。

![单调栈图像](src\content\posts\monotonic-structure\单调栈1.png)

**单调队列** 则更贴近滑动窗口的应用场景，用于在窗口移动过程中实时维护区间的最大值或最小值。随着窗口向前推进，队列一端删除已经离开窗口的旧元素，另一端删除在当前窗口中已不可能再成为极值的冗余元素。最终，队列中剩下的便是一段按单调顺序维护的 “候选区” ，能够在任何时刻 $O(1)$ 得到窗口的当前极值。

![单调队列图像](src\content\posts\monotonic-structure\单调队列1.png)

归根到底，无论使用单调栈还是单调队列，其目的都是一致的：**用单调性主动压缩掉无效候选，从而在一次遍历中完成本应需要多重循环才能实现的关系维护。**
它们为许多涉及局部最值、区间判定、结构扫描的问题提供了高效而简洁的解决方式。

---

# 寻找最近上邻与下邻

## 和至少为 K 的最短子数组

[题目链接](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/)

---

# 寻找最远上邻与下邻



---

# 滑动窗口极值与极差

## 极差不超过 K 的最长子数组

[题目链接](https://leetcode.cn/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)

## 接取雨水的最小花盆

[题目链接](https://www.luogu.com.cn/problem/P2698)

## 满足不等式的最大值

[题目链接](https://leetcode.cn/problems/max-value-of-equation/description/)

---

# 构造式单调题目收集

## 至少有 K 个重复字符的最长子串

[题目链接](https://leetcode.cn/problems/longest-substring-with-at-least-k-repeating-characters/description/)

---

# 潜在式单调题目收集

## 去除重复字母

[题目链接](https://leetcode.cn/problems/remove-duplicate-letters/description/)

## 大鱼吃小鱼

[题目链接](https://www.nowcoder.com/practice/77199defc4b74b24b8ebf6244e1793de)

## 使数组按非递减顺序排列

[题目链接](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/description/)

---

# 参考文献

## 滑动窗口

1. [算法与数据结构（一）：滑动窗口法总结](https://blog.csdn.net/Dby_freedom/article/details/89066140)

2. [滑动窗口算法核心代码模板](https://labuladong.online/algo/essential-technique/sliding-window-framework/)

3. [【算法】滑动窗口算法详解](https://blog.csdn.net/2401_87820834/article/details/145998759)

4. [【Gaowalyrrn】滑动窗口法](https://www.cnblogs.com/Gaowaly/p/18344802)

## 单调栈

1. [【OI WiKi】单调栈相关知识](https://oi-wiki.org/ds/monotonous-stack/)

2. [关于单调栈的详细讲解及应用案例](https://blog.csdn.net/zy_dreamer/article/details/131036101)

3. [【算法通关手册】单调栈](https://algo.itcharge.cn/03_stack_queue_hash_table/03_02_monotone_stack/)

4. [数据结构之单调栈：从原理到实战，玩转高效解题](https://blog.csdn.net/2301_79248256/article/details/155377188)

5. [如何优雅地使用单调栈（一）：基础篇](https://www.cnblogs.com/molinchn/p/14772025.html)

## 单调队列

1. [【OI WiKi】单调队列相关知识](https://oi-wiki.org/ds/monotonous-queue/)

2. [数据结构之单调队列](https://blog.csdn.net/2301_79248256/article/details/155452653)

3. [单调队列：实用而好写的数据结构](https://www.cnblogs.com/jerrycyx/p/18683014)

4. [算法学习笔记：单调栈/单调队列](https://www.cnblogs.com/P2441M/p/18637702)