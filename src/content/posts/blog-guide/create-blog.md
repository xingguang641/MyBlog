---
title: 【博客指南】从零开始发布一篇文章
published: 2025-10-22
description: 基于 Fuwari 主题的博客文章创建与部署全流程指南
tags: [Fuwari, Blogging, Tutorial]
category: Blog Guides
draft: false 
---

> 写在前面：本文将介绍如何在 Fuwari 模板中创建新文章，并将其部署到 Nginx 服务器的完整流程。

## 创建文章

### 方式一：使用命令行

你可以通过项目内置的脚本快速创建一篇文章的基础模板：

```bash showLineNumbers
pnpm new-post "文章的文件名"
```

### 方式二：手动创建

你也可以直接在 `src/content/posts/` 目录下新建 `.md` 或 `.mdx` 文件。请确保文件开头包含正确的 Frontmatter 信息（标题、日期、标签等元数据），以便系统正确识别文章。

## 构建与部署

在发布之前，需要将 Markdown 文件编译为静态 HTML 页面。

### 构建项目

在本地执行以下命令完成静态资源的构建：

```bash showLineNumbers
pnpm build
```

构建结束后，项目根目录会生成一个 `dist` 文件夹，其中包含可直接部署的站点内容。

### 上传至服务器

将 `dist` 目录内容上传到服务器指定的站点路径。以下是示例命令，请根据实际情况替换 `<占位符>` ：

```bash showLineNumbers
# scp -r <本地构建目录>/* <用户名>@<服务器IP>:<服务器站点目录>
scp -r ./dist/* user@192.168.1.1:/var/www/html/blog
```

## 配置服务器权限

如果你使用 Nginx，由于上传文件的所有者通常与 Nginx 用户不同，可能会导致访问出现 `403 Forbidden` 。因此，需要调整目录的权限。

首先登录服务器：

```bash showLineNumbers
ssh user@192.168.1.1
```

接着依次执行以下命令，使 Nginx 能够正常读取站点内容：

```bash showLineNumbers
# 将目录所有权交给 Web 用户 (通常是 www-data)
sudo chown -R www-data:www-data /var/www/html/blog

# 将所有文件夹的权限设置为 755 (所有者读写执行，其他人读取执行)
sudo find /var/www/html/blog -type d -exec chmod 755 {} \;

# 将所有文件的权限设置为 644 (所有者读写，其他人只读)
sudo find /var/www/html/blog -type f -exec chmod 644 {} \;
```

:::tip
**小贴士**：如果遇到 `403` 或资源加载失败的问题，通常重新运行上述权限命令即可解决。
:::