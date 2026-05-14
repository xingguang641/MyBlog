---
title: 【ACM 算法题单】字符串哈希相关问题
published: 2026-05-10
description: 记录一些 ACM 常见题型
tags: [Algorithm, Problem Type]
category: ACM Type
draft: false
---

# 字符串哈希相关题

可以替代KMP的子串比对，代替马拉车记录回文半径，但是要更慢

本质是将子串比对这个操作优化到 O(1)，这个是优势区间

## 数字频率相同的子字符串的数量

[题目链接](https://leetcode.doocs.org/lc/2168/)



## 题目要点解析

字符串去重（相当于暴力做法）

## 重复叠加字符串

[题目链接](https://leetcode.cn/problems/repeated-string-match/description/)



## 题目要点解析

需要找规律，建议记住

## 串联所有的单词

[题目链接](https://leetcode.cn/problems/substring-with-concatenation-of-all-words/description/)



## 题目要点解析

简单的字符串哈希+滑动窗口

## 失配字符串问题

[题目链接](https://leetcode.cn/problems/substring-with-concatenation-of-all-words/description/)



## 题目要点解析

字符串哈希+二分找不同点

---

# 参考文献列表

1. [【OI WiKi】字符串哈希相关知识](https://oi-wiki.org/string/hash/)