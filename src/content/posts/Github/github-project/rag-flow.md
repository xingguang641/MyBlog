---
title: 【开源项目部署教程】RAGFlow项目教程
published: 2025-12-10
description: 基于 Docker Compose 的 RAGFlow 独立部署教程
tags: [RAG, Docker, Github, Agent]
category: Github Project
draft: false 
---

> 写在前面：本篇博客教程来自于该视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=113950951736220&bvid=BV1WiP2ezE5a&cid=28278981043&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# Ollama模型配置

在配置 **RAGFlow** 之前，第一步是准备好本地的 **大语言模型（LLM）**，而 **Ollama** 是一个非常方便的工具，可以用来在本地运行和管理这些模型。首先，需要在本机上下载并安装 Ollama 平台。安装完成后，接下来就是对环境进行一些必要的配置，以保证虚拟机中的 RAGFlow 可以顺利访问到本地模型。

在配置过程中，有两个环境变量需要特别注意。第一个是 `OLLAMA_HOST` ，通常设置为 `0.0.0.0:11434` 。这个设置的作用是让虚拟机可以通过网络访问本机上的 Ollama 服务。如果配置完成后虚拟机无法访问，很可能是本机防火墙拦截了 11434 端口。此时，如果不想直接开放这个端口，也可以通过 **SSH 端口转发** 来实现访问。完成环境变量配置后，记得重启系统或者终端，使设置生效。

另一个需要配置的环境变量是 `OLLAMA_MODELS` ，它用于指定模型存储位置。Ollama 默认会将下载的模型放在 C 盘，如果你希望将模型保存到其他盘符或自定义目录，需要通过该环境变量进行调整。

在环境配置完成之后，就可以通过 Ollama 下载所需的模型了。以 DeepSeek 大模型为例，命令非常简单，只需执行 `ollama run deepseek-r1:1.5b` ，Ollama 就会自动下载并启动该模型，准备好供 RAGFlow 使用。通过这一系列步骤，你就完成了本地 LLM 的准备工作，为后续的 RAGFlow 配置打下了基础。

# RAGF项目部署

**RAGFlow** 是一个集成本地大语言模型与知识检索的问答系统，能够将本地大模型与外部知识库结合，实现智能问答、内容生成和信息检索的统一管理。它可以直接在本地 Python 环境中运行，但为了保证环境隔离、依赖一致性以及后续维护的便利，通常推荐使用 **Docker 容器化部署**。

通过 Docker 部署 RAGFlow，可以在独立的容器中运行所有服务，避免因系统环境或依赖冲突导致的问题。同时，容器化也方便对不同版本的模型和服务进行管理和更新，实现快速启动、易于备份和迁移。对于个人用户来说，这种方式能够快速搭建一个可用的本地问答环境；对于团队或服务器环境，则能够保证服务的稳定性和可扩展性。

在容器化环境中，RAGFlow 可以直接连接本地已配置好的 Ollama 服务和 DeepSeek 模型，实现对模型的调用和管理。借助 Docker Compose 或类似工具，还可以一次性启动数据库、RAGFlow 服务以及其他依赖组件，形成一个完整的、独立可运行的问答系统。这种部署方式不仅提高了系统稳定性，还方便在不同机器或环境间迁移，极大地降低了运维成本。

## 获取项目代码

项目开源地址如下：

::github{repo="infiniflow/ragflow"}

首先使用 Git 将项目克隆到本地：

```bash showLineNumbers
git clone https://github.com/infiniflow/ragflow.git
```

## 配置Docker

进入 **docker** 文件夹，利用官方提前构建好的 Docker 镜像即可启动 RAGFlow 服务器。

:::warning
⚠️ **注意**：当前官方提供的 Docker 镜像均基于 **x86 架构** 构建，不提供 ARM64 架构的镜像。如果你的操作系统是 ARM64 架构，请参考[官方文档](https://ragflow.io/docs/dev/build_docker_image)自行构建 Docker 镜像。
:::

运行以下命令会自动下载并启动 **RAGFlow Docker 镜像 `v0.22.1`** 。如果需要使用其他版本的镜像，请在运行 `docker compose` 之前，先更新 **docker/.env** 文件中的 `RAGFLOW_IMAGE` 变量。

```bash showLineNumbers
$ cd ragflow/docker

# 可选：切换到稳定版本标签（查看发布记录：https://github.com/infiniflow/ragflow/releases）
# git checkout v0.22.1
# 这一步确保代码中的 entrypoint.sh 文件与 Docker 镜像版本保持一致

# 使用 CPU 执行 DeepDoc 任务
$ docker compose -f docker-compose.yml up -d

# 使用 GPU 加速 DeepDoc 任务（需在 .env 文件首行添加 DEVICE=gpu）
# sed -i '1i DEVICE=gpu' .env
# docker compose -f docker-compose.yml up -d
```

:::tip
**镜像版本说明**：`v0.22.0` 之前的版本，官方提供了两种镜像：包含 embedding 模型的完整镜像和不含 embedding 模型的 slim 镜像。
:::

| RAGFlow image tag | 镜像大小 (GB) | 是否包含 embedding 模型 | 稳定性  |
| ----------------- | --------- | ----------------- | ---- |
| v0.21.1           | ≈9        | ✔️                | 稳定版本 |
| v0.21.1-slim      | ≈2        | ❌                 | 稳定版本 |

通过以上步骤，即可在 Docker 环境中快速启动 RAGFlow 服务，并可根据实际需求灵活选择 CPU 或 GPU 运行模式。同时该方式能够确保服务配置与镜像版本保持一致，便于后续的升级、使用与维护。需要注意的是，在访问服务时请关闭代理，否则可能导致服务无法正常访问。

## 访问RAGFlow

完成容器化部署后，你可以通过浏览器或 API 直接访问 RAGFlow 服务。Docker Compose 会将 RAGFlow 的 Web 服务端口映射到本地环境中，常用端口如下：

- **HTTP**：`${SVR_WEB_HTTP_PORT}`（默认 80）
- **HTTPS**：`${SVR_WEB_HTTPS_PORT}`（默认 443）
- **Admin Server**：`${ADMIN_SVR_HTTP_PORT}`（默认 9381）

例如，在浏览器中访问 `http://localhost:${SVR_WEB_HTTP_PORT}` 就可以打开 RAGFlow 主界面；若启用了 HTTPS，则可使用 `https://localhost:${SVR_WEB_HTTPS_PORT}` 进行访问。