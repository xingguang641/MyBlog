---
title: 【博客指南】如何创建一个独立页面
published: 2025-11-24
description: 基于 Fuwari 模板创建自定义独立页面（如成就、友链等）的完整教程
tags: [Fuwari, Static Pages, Tutorial]
category: Guides
draft: false 
---

> 写在前面：本文将介绍如何在 Fuwari 模板中添加一个自定义的独立页面（例如 “成就” 、“友链” 等）。

## 编写页面内容

首先，我们需要准备该独立页面所要展示的主体内容。

请在 `src/content/spec` 目录下创建一个 Markdown 文件（例如 `achievements.md` ）。这个文件不需要包含复杂的 Frontmatter，直接编写你想要展示的 Markdown 内容即可。

## 创建页面组件

接下来，我们需要创建一个 Astro 页面文件来渲染上述内容。

在 `src/pages` 目录下新建一个 `.astro` 文件（推荐与你的 Markdown 文件名一致，例如 `achievements.astro`）。

你可以直接复制 `about.astro` 的样例代码并稍作修改，或者使用下面的自定义模板代码。该代码会自动获取 `src/content/spec` 中的内容并渲染到主布局中。

```astro frame="code" title="src/pages/achievements.astro"
---
import { getEntry, render } from "astro:content";
import Markdown from "@components/misc/Markdown.astro";
import MainGridLayout from "../layouts/MainGridLayout.astro";

// 获取步骤 1 中创建的 'achievements' 内容
// 如果你的文件名是 other.md，请将下方的 "achievements" 改为 "other"
const achievementsPost = await getEntry("spec", "achievements");

if (!achievementsPost) {
	throw new Error("Achievements page content not found");
}

const { Content } = await render(achievementsPost);
---
<!-- title 和 description 将显示在浏览器标签页和 SEO 信息中 -->
<MainGridLayout title="成就" description="我的个人成就清单">
    <div class="flex w-full rounded-[var(--radius-large)] overflow-hidden relative min-h-32">
        <div class="card-base z-10 px-9 py-6 relative w-full ">
            <Markdown class="mt-2">
                <Content />
            </Markdown>
        </div>
    </div>
</MainGridLayout>
```

## 配置导航栏入口

页面文件准备好后，最后一步是将其添加至博客顶部导航栏，使访客能够正常访问。

打开 `src/config.ts` 文件，找到常量 `navBarConfig` ，并在 `links` 数组中添加一项新的导航链接：

```ts frame="code" title="src/config.ts"
export const navBarConfig: NavBarConfig = {
    links: [
        LinkPreset.Home,
        LinkPreset.Archive,
        LinkPreset.About,
        // 添加新的页面入口
        // name: 导航栏显示的文字
        // url: 对应的路由地址（即 src/pages/ 下的文件名）
        { name: "成就", url: "/achievements/" },
    ],
};
```

保存所有文件后，你就能在博客的顶部导航栏看到新添加的独立页面了。