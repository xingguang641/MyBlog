---
title: 【博客指南】Markdown 扩展功能
published: 2024-04-10
updated: 2024-11-29
description: 在 Fuwari 中了解更多关于 Markdown 功能的信息
tags: [Demo, Example, Markdown, Fuwari]
category: Blog Guides
draft: false 
---

## GitHub 仓库卡片
你可以添加链接到 GitHub 仓库的动态卡片；页面加载时会从 GitHub API 拉取该仓库的信息。

::github{repo="Fabrizz/MMM-OnSpotify"}

创建一个包含代码的 GitHub 仓库卡片： `::github{repo="<owner>/<repo>"}`

```markdown
::github{repo="saicaca/fuwari"}
```

## 提示框

支持以下类型的提示框（admonitions）： `note` `tip` `important` `warning` `caution`

:::note
强调用户即使在快速浏览时也应该注意的信息。
:::

:::tip
可选信息，用于帮助用户更好地完成任务。
:::

:::important
用户成功所必需的重要信息。
:::

:::warning
由于潜在风险，需要用户立即关注的关键信息。
:::

:::caution
某个操作可能带来的负面后果。
:::

### 基本语法

```markdown
:::note
强调用户即使在快速浏览时也应注意的信息。
:::

:::tip
可选信息，用于帮助用户更顺利地完成任务。
:::
```

### 自定义标题

提示框的标题可以自定义。

:::note[MY CUSTOM TITLE]
这是一个带有自定义标题的备注。
:::

```markdown
:::note[MY CUSTOM TITLE]
这是一个带有自定义标题的备注。
:::
```

### GitHub 语法

> [!TIP]
> 同样支持 [GitHub 语法](https://github.com/orgs/community/discussions/16925)

```
> [!NOTE]
> 同样支持 GitHub 的语法。

> [!TIP]
> 同样支持 GitHub 的语法。
```

### 隐藏内容

你可以在文本中隐藏内容。文本同样支持 **Markdown** 语法。

The content :spoiler[is hidden **ayyy**]!

```markdown
The content :spoiler[is hidden **ayyy**]!

```