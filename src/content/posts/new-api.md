---
title: 【开源项目部署教程】NewAPI 项目教程
published: 2025-10-22
description: 基于 Docker Compose 的 NewAPI 独立部署教程，实现数据与宿主机环境的完全隔离
tags: [API, Docker, Github, Tutorial]
category: Github
draft: false 
---

# NewAPI 项目部署

NewAPI 是一个基于 One API 二次开发的强大的 API 管理与分发系统，支持多种大模型渠道。本文将介绍如何使用 Docker Compose 快速部署一个环境隔离的 NewAPI 实例。

## 获取项目代码

项目开源地址如下：

::github{repo="QuantumNous/new-api"}

首先，使用 Git 将项目克隆到本地：

```bash showLineNumbers
git clone https://github.com/QuantumNous/new-api.git
cd new-api
```

## 配置 Docker Compose

为了实现数据与宿主机的解耦，我们将使用 Docker 命名卷（Named Volumes）来替代传统的文件路径映射。

请编辑项目根目录下的 `docker-compose.yml` 文件，将其内容替换为以下配置：

```yaml showLineNumbers
# New-API Docker Compose Configuration (独立部署版)
#
# Quick Start:
#   1. docker compose up -d
#   2. Access at http://localhost:3000
#
# Notes:
#   - 不会在宿主机创建任何文件夹（完全独立运行）
#   - 数据与日志都存储在 Docker 的内部卷中
#   - 若需查看日志: docker logs new-api
#   - 若需备份数据或日志: docker cp new-api:/app/logs ./logs_backup

version: '3.4'

services:
  new-api:
    image: calciumion/new-api:latest
    container_name: new-api
    restart: always
    command: --log-dir /app/logs
    ports:
      - "3000:3000"
    environment:
      - SQL_DSN=postgresql://root:123456@postgres:5432/new-api
#      - SQL_DSN=root:123456@tcp(mysql:3306)/new-api  # Uncomment if using MySQL
      - REDIS_CONN_STRING=redis://redis
      - TZ=Asia/Shanghai
      - ERROR_LOG_ENABLED=true
      - BATCH_UPDATE_ENABLED=true
#      - STREAMING_TIMEOUT=300
#      - SESSION_SECRET=random_string
#      - SYNC_FREQUENCY=60
#      - GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
#      - UMAMI_WEBSITE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
#      - UMAMI_SCRIPT_URL=https://analytics.umami.is/script.js
    depends_on:
      - redis
      - postgres
#      - mysql
    healthcheck:
      test: ["CMD-SHELL", "wget -q -O - http://localhost:3000/api/status | grep -o '\"success\":\\s*true' || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - app_data:/data
      - app_logs:/app/logs

  redis:
    image: redis:latest
    container_name: redis
    restart: always

  postgres:
    image: postgres:15
    container_name: postgres
    restart: always
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 123456
      POSTGRES_DB: new-api
    volumes:
      - pg_data:/var/lib/postgresql/data
#    ports:
#      - "5432:5432"

#  mysql:
#    image: mysql:8.2
#    container_name: mysql
#    restart: always
#    environment:
#      MYSQL_ROOT_PASSWORD: 123456
#      MYSQL_DATABASE: new-api
#    volumes:
#      - mysql_data:/var/lib/mysql
#    ports:
#      - "3306:3306"

volumes:
  pg_data:
  app_data:
  app_logs:
#  mysql_data:
```

:::tip
**配置说明**：
上述配置使用了 `volumes` 模块定义了 `pg_data`、`app_data` 等命名卷。这意味着数据库文件和日志将托管在 Docker 内部，**不会污染你的本地项目目录**。即使删除了当前文件夹，只要不手动删除 Docker Volume，数据依然保留。
:::

## 启动服务

确保你的服务器已安装 Docker 和 Docker Compose。如果尚未安装，可以参考 [官方文档](https://docs.docker.com/compose/install/) 或 [New API 官方指南](https://www.newapi.ai/installation/docker-compose-installation/) 进行安装。

在 `docker-compose.yml` 所在目录下，执行以下命令启动服务：

```bash showLineNumbers
docker compose up -d
```

启动成功后，你可以通过浏览器访问：

*   **地址**: `http://localhost:3000`
*   **默认账号**: `root`
*   **默认密码**: `123456`

## 常用维护指令

由于我们采用了全容器化部署，以下是一些常用的维护指令：

*   **查看运行日志**:
    ```bash
    docker logs -f new-api
    ```
*   **备份日志文件到本地**:
    ```bash
    docker cp new-api:/app/logs ./logs_backup
    ```
*   **停止服务**:
    ```bash
    docker compose down
    ```

现在，你已经拥有了一个完全独立的 API 管理中心，无需再为繁杂的 API Key 管理而发愁了。