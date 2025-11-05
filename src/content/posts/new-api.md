---
title: NewAPI 项目教程
published: 2025-10-22
description: NewAPI 项目的详细部署教程（顺带部署至Docker）
tags: [API, Course, Github]
category: Github
draft: false 
---

# NewAPI 项目

## 下载项目

下面这个是项目的链接

::github{repo="QuantumNous/new-api"}

直接输入下面的指令克隆仓库

```cmd showLineNumbers
git clone https://github.com/QuantumNous/new-api.git
```

## 修改配置文件

将 `docker-compose.yml` 中的内容修改成下面这个

```yml showLineNumbers
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

这样可以让项目完全独立于本地，迁移至 Docker 之后直接删掉本地项目也不会有影响

## 部署至 Docker

首先就要下载 Docker 跟 Docker Compose，然后跟着下面的 Blog 一步步走就行了

[Docker Compose 部署 New API 指南](https://www.newapi.ai/installation/docker-compose-installation/)

这样你就有一个 API 管理中心了，不用再为如何保存数量繁多的 API 而发愁