---
title: 【博客指南】从零开始发布一篇文章
published: 2025-10-22
description: 基于 Fuwari 主题的博客文章创建与部署全流程指南
tags: [Fuwari, Blogging, Tutorial]
category: Guides
draft: false 
---

> 写在前面：本文将介绍如何在 Fuwari 模板中创建新文章，并将其部署到 Nginx 服务器的完整流程。

## 创建文章

### 方式一：使用命令行

你可以使用项目内置的脚本快速生成文章模板：

```bash showLineNumbers
pnpm new-post "文章的文件名"
```

### 方式二：手动创建

你也可以直接在 `src/content/posts/` 目录下创建一个新的 `.md` 或 `.mdx` 文件。请确保文件头部包含正确的 Frontmatter 信息（即标题、日期等元数据）。

## 构建与部署

在发布之前，需要将 Markdown 文件编译为静态 HTML 页面。

### 构建项目

在本地终端执行以下命令生成静态文件：

```bash showLineNumbers
pnpm build
```

构建完成后，项目根目录下会生成一个 `dist` 文件夹。

### 上传至服务器

使用 `scp` 命令将 `dist` 文件夹中的内容上传至服务器的站点目录。

> ⚠️ **注意**：请根据实际情况替换命令中的 `<占位符>` 。

```bash showLineNumbers
# scp -r <本地构建目录>/* <用户名>@<服务器IP>:<服务器站点目录>
scp -r ./dist/* user@192.168.1.1:/var/www/html/blog
```

## 配置服务器权限

如果你的服务器使用 Nginx，上传新文件后可能会因为文件所有权问题导致访问出现 `403 Forbidden` 错误。我们需要修正文件权限。

首先，登录你的服务器：

```bash showLineNumbers
ssh user@192.168.1.1
```

然后，依次执行以下三条命令。这些命令将确保 Nginx 有权限读取你的博客文件：

```bash showLineNumbers
# 将目录所有权交给 Web 用户 (通常是 www-data)
sudo chown -R www-data:www-data /var/www/html/blog

# 将所有文件夹的权限设置为 755 (所有者读写执行，其他人读取执行)
sudo find /var/www/html/blog -type d -exec chmod 755 {} \;

# 将所有文件的权限设置为 644 (所有者读写，其他人只读)
sudo find /var/www/html/blog -type f -exec chmod 644 {} \;
```

:::tip
**小贴士**：
每次上传新的页面或资源文件后，如果遇到 `403` 或资源加载失败的问题，通常重新运行上述权限命令即可解决。
:::