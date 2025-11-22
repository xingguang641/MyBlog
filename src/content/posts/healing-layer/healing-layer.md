---
title: 【常见问题解决方案】新浪微博图片无法显示
published: 2025-11-12
description: 解决老博客的新浪图片显示错误问题
tags: [Course, Blogging]
category: Fixes
draft: false 
---

## 新浪图片无法显示的原因

之所以会出现图片无法正常显示的 BUG 是因为新浪微博在某次更新后会检测跳转链接的一级域名，如果该域名不是新浪微博的本地域名就会拦截此次访问，因此我们只需要正则匹配博客图片的一级域名后改成新浪微博的域名即可。

### 下载 Header-Editor 插件

打开任意浏览器插件商城搜索 Header-Editor 插件。

![插件商城图像](src\content\posts\healing-layer\Header-Editor1.jpg)

### 修改图片一级域名

进入插件主界面后点击右上角的添加。

![插件商城图像](src\content\posts\healing-layer\Header-Editor2.jpg)

然后规则类型选择 **修改请求头** ，匹配规则选择 **域名** 。

![插件商城图像](src\content\posts\healing-layer\Header-Editor3.jpg)

然后输入你需要修复的图片链接的一级域名（点击 `F12` 后选择目标图片查看跳转链接），最后在下方填入新浪微博的域名 `https://weibo.com` 。

![插件商城图像](src\content\posts\healing-layer\Header-Editor4.jpg)

保持插件运行，这样当前博客的图片 BUG 就会永久修复。但其他博客的图片链接的一级域名不一定与你此时输入的域名相同，因此可以尝试使用匹配规则的 **正则表达式** 功能。