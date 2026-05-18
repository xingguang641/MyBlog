---
title: 【ACM 算法随笔】String算法汇总
published: 2026-05-09
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note, ACM]
category: ACM Note
draft: false
---

# 字符匹配算法原理



## 单模式匹配算法

BM 算法    Sunday 算法    KMP 算法（需要强调KMP真正的优点：按位独立性）

先讲解LSP数组的性质

[Border理论](https://www.luogu.com/article/qgl51obr)

[Border理论小记](https://www.luogu.com.cn/article/ds5cz0sg)

拓展KMP（Z函数）

## 另一棵树的子树

[题目链接](https://leetcode.cn/problems/subtree-of-another-tree/description/)



## 题目要点解析

需要结合DFN序

## 不断删除字符串

[题目链接](https://www.luogu.com.cn/problem/P4824)



## 题目要点解析

类似消消乐的这种题目统一用栈解决

## 二叉树中的链表

[题目链接](https://leetcode.cn/problems/linked-list-in-binary-tree/description/)



## 题目要点解析

依旧自上而下DFS降维

## 找到好的字符串

[题目链接](https://leetcode.cn/problems/find-all-good-strings/description/)



## 题目要点解析

数位DP+KMP算法，需要了解KMP的特殊性

## 将单词恢复初始状态所需的时间

[题目链接](https://leetcode.cn/problems/minimum-time-to-revert-word-to-initial-state-ii/description/)



## 题目要点解析

Z数组的简单运用

## 多模式匹配算法

AC 自动机

## 好字符串的构造

[题目链接](https://www.luogu.com.cn/problem/P3311)



## 题目要点解析

和上面那道数位DP+KMP的题目一模一样，只是改成AC自动机读取多个模式串

---

# 回文判断算法原理

Manacher 算法    回文自动机

## 最长的回文子串

[题目链接](https://leetcode.cn/problems/longest-palindromic-substring/)



## 题目要点解析

水题

## 回文子串的数量

[题目链接](https://leetcode.cn/problems/palindromic-substrings/description/)



## 题目要点解析

水题

## 不重叠回文子串

[题目链接](https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/)



## 题目要点解析

贪心题

## 拉拉队排练问题

[题目链接](https://www.luogu.com.cn/problem/P1659)



## 题目要点解析

中心点对应一个回文串

## 最长双回文子串

[题目链接](https://www.luogu.com.cn/problem/P4555)



## 题目要点解析

前后缀分解

---

# 参考文献列表

1. [【ACM 算法题单】字符串哈希相关问题](https://xingguang641.com/posts/acm/acm-type/string-problems/string-hash/)

2. [【ACM 算法题单】字符串索引相关问题](https://xingguang641.com/posts/acm/acm-type/string-problems/string-index/)

3. [【ACM 算法题单】字符串嵌套相关问题](https://xingguang641.com/posts/acm/acm-type/string-problems/string-nest/)