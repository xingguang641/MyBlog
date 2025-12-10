---
title: 【常见问题解决方案】新浪微博图片无法显示
published: 2025-11-12
description: 解决老博客的新浪图片显示错误问题
tags: [Course, Blogging]
category: Fixes
draft: false 
---

## 问题来源

老博客中的新浪微博图床图片无法显示，通常是因为新浪微博开启了 **防盗链（Referer Hotlinking Protection）** 机制。简单来说，当浏览器加载图片时，新浪服务器会检测请求头中的 `Referer` 字段（即请求来源）。如果该字段显示请求来自你的个人博客域名，而非新浪自家的域名，服务器就会拦截请求并返回 403 错误。

![图片报错图像](src\content\posts\healing-layer\图片报错1.png)

解决方案非常简单：我们只需要通过浏览器插件修改请求头，将 `Referer` 伪装成新浪微博的域名即可欺骗服务器正常返回图片。

## 解决方案

### 1. 安装 Header Editor 插件

在 Chrome、Edge 或 Firefox 的扩展商店中搜索并安装 **Header Editor** 插件。

![插件商城图像](src\content\posts\healing-layer\Header-Editor1.jpg)

### 2. 添加修改规则

安装完成后，点击插件图标进入管理界面，点击右下角或右上角的 **“添加”** 按钮。

![插件商城图像](src\content\posts\healing-layer\Header-Editor2.jpg)

### 3. 配置规则详情

这是最关键的一步，请按照以下逻辑进行配置：

*   **规则类型**：选择 **修改请求头** 。
*   **匹配规则**：选择 **域名** 。
*   **头名称**：输入 `Referer` 。
*   **头内容**：输入 `https://weibo.com` 。

![插件商城图像](src\content\posts\healing-layer\Header-Editor3.jpg)

**关于匹配规则的说明**：在 “匹配规则” 一栏中，你需要填入 **图片链接的域名**（即图床服务器的域名）。你可以按 `F12` 打开开发者工具，选中无法显示的图片，查看其 URL。

如果图片地址是 `https://ws1.sinaimg.cn/large/...` ，那么你应该填入 `ws1.sinaimg.cn` 或 `sinaimg.cn` 。

![插件商城图像](src\content\posts\healing-layer\Header-Editor4.jpg)

### 4. 保存并测试

点击保存，确保插件处于 **“启用”** 状态。刷新你的博客页面，原本裂开的图片应该就能正常加载了。

> **进阶提示**：
>
> 如果你的博客引用了多个不同服务器的新浪图片（如 `ws1.sinaimg.cn` ，`wx3.sinaimg.cn` 等），建议将匹配规则改为 **正则表达式** ，并输入 `.*sinaimg.cn.*` ，这样可以一次性匹配所有新浪图床的子域名。