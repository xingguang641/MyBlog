---
title: 【博客指南】如何为博客添加HTTPS
published: 2026-05-26
description: 如何添加/修改静态博客的SSL证书
tags: [Fuwari, Blogging, Tutorial]
category: Blog Guides
draft: false 
---

## 证书配置具体步骤

### 1. 创建配置目录

在创建文件夹之前，我们需要先确认 Nginx 的核心配置目录位置。通常情况下，Linux 系统的 Nginx 根目录为 `/etc/nginx` 。

你可以通过在服务器终端执行以下命令来验证该目录是否存在：

```bash showLineNumbers
ls -d /etc/nginx
```

确认输出结果为 `/etc/nginx` 后，再执行以下命令，在 Nginx 配置目录下建立专门的证书文件夹：

```bash showLineNumbers
sudo mkdir -p /etc/nginx/cert
```

### 2. 提交证书文件

在电脑本地解压从云平台下载的 **Nginx 版本** 证书压缩包，你会得到一个证书文件（ `.crt` 或 `.pem` ）和一个私钥文件（ `.key` ）。

直接在 **电脑本地终端** 利用 `scp` 命令，在将文件发送到服务器：

```bash
# scp <本地证书路径> <用户名>@<服务器IP>:<服务器证书绝对路径>
scp ./*.crt user@192.168.1.1:/etc/nginx/cert/blog.crt
scp ./*.key user@192.168.1.1:/etc/nginx/cert/blog.key
```

### 3. 重构配置文件

我们需要通过修改 Nginx 站点配置，实现 **HTTP 流量全强制跳转** 与 **HTTPS 证书精准指引** 。

使用终端编辑器（如 `sudo nano /etc/nginx/sites-enabled/digvps.conf` ）打开你的博客站点配置文件，清空内容并将以下标准配置完整写入：

```nginx
# 1. 拦截 80 端口（HTTP）流量，301 永久重定向至 HTTPS
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name xingguang641.com www.xingguang641.com; # 替换为你的域名
    
    return 301 https://$host$request_uri;
}

# 2. 托管 443 端口（HTTPS）核心加密服务
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name xingguang641.com www.xingguang641.com; # 替换为你的域名

    # 静态博客网页根目录
    root /var/www/digvps/dist;
    index index.html;

    # 核心配置：指定刚刚上传的证书与私钥绝对路径
    ssl_certificate      /etc/nginx/cert/blog.crt; 
    ssl_certificate_key  /etc/nginx/cert/blog.key;

    # 安全协议与算法优化
    ssl_session_timeout 5m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

    # SPA 静态路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 4. 重新加载证书

修改完配置文件后，需要利用 Nginx 内置的检查机制确保配置无误再进行启动。

在服务器终端输入以下命令：

```bash showLineNumbers
sudo nginx -t
```

如果终端返回 `nginx: configuration file ... syntax is ok` 以及 `test is successful` 的信号，说明配置完美无误。此时即可执行热重载命令，让新证书无缝接管：

```bash showLineNumbers
sudo nginx -s reload
```

## 证书更新具体步骤

由于免费 SSL 证书通常仅有 90 天有效期，当收到云平台发来的证书即将到期提醒时，**完全不需要重新修改 Nginx 配置文件** 。我们只需要将新证书下载到本地，直接覆盖服务器上的旧证书并热重载即可，整个过程约 1 分钟。

### 1. 覆盖证书文件

在电脑本地解压全新申请的 **Nginx 版本** 证书压缩包。

无需在服务器上做任何操作，直接在 **电脑本地终端** 利用 `scp` 命令，将全新的证书与私钥上传，此时会直接覆盖原有的 `blog.crt` 和 `blog.key`：

```bash showLineNumbers
# scp <本地新证书路径> <用户名>@<服务器IP>:<原服务器证书绝对路径>
scp ./*.crt root@192.168.1.1:/etc/nginx/cert/blog.crt
scp ./*.key root@192.168.1.1:/etc/nginx/cert/blog.key
```

### 2. 重新加载证书

证书文件虽然在后台完成了替换，但 Nginx 此时在内存中运行的依然是旧证书。我们需要让 Nginx 重新加载。

在服务器终端输入以下命令：

```bash showLineNumbers
sudo nginx -t
```

如果终端返回 `nginx: configuration file ... syntax is ok` 以及 `test is successful` 的信号，说明配置完美无误。此时即可执行热重载命令，让新证书无缝接管：

```bash showLineNumbers
sudo nginx -s reload
```