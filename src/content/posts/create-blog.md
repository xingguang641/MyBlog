---
title: 如何创建一个自己的文章
published: 2025-10-22
description: 如何创建一个 Fuwari 模板的博客
tags: [Fuwari, Blogging]
category: Guides
draft: false 
---

## 创建文章模板

可以输入下面这个指令直接生成一个模板文件

```cmd showLineNumbers
pnpm new-post "filename"
```

也可以直接在 `src/content/posts/` 目录中创建新的文件

## 上传文章至服务器

首先 build 出新文章的 html 文件，输入以下命令

```cmd showLineNumbers
pnpm build
```

然后 push 本地的 dist 文件夹至服务器上

```cmd showLineNumbers
scp -r ./dist/* 用户名@服务器公网IP:目标目录
```

## 配置 Nginx 权限

登录你的服务器

```cmd showLineNumbers
ssh 用户名@服务器公网IP
```

并输入下面三个命令，不然 Nginx 没有权限访问新的文章导致 `403` 错误

```cmd showLineNumbers
sudo chown -R www-data:www-data 目标目录
sudo find 目标目录 -type d -exec chmod 755 {} \;
sudo find 目标目录 -type f -exec chmod 644 {} \;
```

只要博客有新的页面出现都要配置这个（出现 `403` 错误输入这三行代码基本都能搞定）