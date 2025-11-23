---
title: 【博客指南】如何创建一个独立页面
published: 2024-04-10
updated: 2025-11-24
description: 教你如何使用 Fuwari 模板创建独立页面
tags: [Fuwari, Static Pages]
category: Guides
draft: false 
---

## 创建独立页面

创建独立页面只需要修改三个地方就可以了。

首先我们需要在 `src/content/spec` 中创建一个 mardown 文件，这个文件不需要任何的初始格式，直接输入你想要的内容即可。

然后我们需要在 `src/pages` 中创建一个 astro 文件，最好跟上面的 mardown 文件的名字相同，然后仿造 `about.astro` 文件的格式写入内容就可以了，下面给出我创建的 “成就” 页面文件做示范。

```astro frame="code" title="achievements.astro"
---

import { getEntry, render } from "astro:content";
import Markdown from "@components/misc/Markdown.astro";
import MainGridLayout from "../layouts/MainGridLayout.astro";

const achievementsPost = await getEntry("spec", "achievements");

if (!achievementsPost) {
	throw new Error("Achievements page content not found");
}

const { Content } = await render(achievementsPost);
---
<MainGridLayout title="成就" description="成就">
    <div class="flex w-full rounded-[var(--radius-large)] overflow-hidden relative min-h-32">
        <div class="card-base z-10 px-9 py-6 relative w-full ">
            <Markdown class="mt-2">
                <Content />
            </Markdown>
        </div>
    </div>
</MainGridLayout>
```

最后我们只需要在 `src/config.ts` 文件的常量 `navBarConfig` 中填入相应的键值对即可，下面依旧给出 “成就” 的示例。

```ts frame="code" title="config.ts"
export const navBarConfig: NavBarConfig = {
	links: [
		LinkPreset.Home,
		LinkPreset.Archive,
		LinkPreset.About,
		{ name: "成就", url: "/achievements/" },
        // 在这里填入相应的键值对
	],
};
```

这样我们就能在博客上方的页面栏添加一个新的独立页面了。