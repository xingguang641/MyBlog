---
title: 【开源项目部署教程】JupyTrans项目教程
published: 2025-10-21
description: 基于 LLM 和阿里云机器翻译的 Jupyter Notebook 翻译工具部署指南
tags: [Translate, Python, Github]
category: Github Project
draft: false 
---

# JupyTrans项目部署

Jupyter Translate 是一个能够将 `.ipynb` 文件进行自动翻译的工具，支持多种翻译引擎，能够在保留代码与输出不变的情况下，批量处理 Markdown 文本与注释的语言转换。通过简单的配置，你就可以让它在笔记本中实现一键翻译，适用于整理学习资料、生成双语 Notebook 或快速阅读外文教程。下面将介绍如何安装、配置并实际使用这个工具。

## 获取项目代码

首先访问项目的 GitHub 仓库：

::github{repo="jexonn/jupyter-translate"}

使用 Git 命令克隆项目到本地：

```bash showLineNumbers
git clone https://github.com/jexonn/jupyter-translate.git
cd jupyter-translate
```

### 安装依赖

项目依赖列表在 `requirements.txt` 中。

:::tip
**网络提示**：
如果在安装过程中遇到网络超时问题，建议使用国内镜像源（如清华源）进行安装。
:::

```bash showLineNumbers
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

如果仍然安装失败，你可以打开 `requirements.txt` 查看具体内容，依次手动安装缺失的库。

## 配置翻译服务

该项目支持多种翻译后端。为了获得最佳的翻译质量和速度，我们通常结合使用 **大语言模型（LLM）** 和 **阿里云机器翻译**。你需要手动修改项目中的配置文件（通常在 `main.py` 或独立的 `config.py` 中）。

### 配置 LLM（以 DeepSeek 为例）

你可以使用任意兼容 OpenAI 接口的大模型。这里以性价比极高的 DeepSeek 为例：

```python showLineNumbers
# 填入你的 LLM API 信息
api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
base_url = "https://api.deepseek.com/v1/"
model_name = "deepseek-chat"
```

### 配置阿里云机器翻译（Aliyun MT）

为了处理某些特定的翻译任务，你需要配置阿里云的 AccessKey。

1.  **注册账号**：前往 [阿里云官网](https://www.aliyun.com/) 注册并登录。
2.  **开通服务**：访问 [机器翻译控制台](https://mt.console.aliyun.com/) 开通服务（通常有免费额度）。
3.  **获取密钥**：访问 [RAM 访问控制](https://ram.console.aliyun.com/manage/ak) 创建 AccessKey。

获取上述信息后，将其填入配置：

```python showLineNumbers
# 填入阿里云 AccessKey
access_key_id = "LTAIxxxxxxxxxxxxxxxx"
access_key_secret = "xxxxxxxxxxxxxxxxxxxxxxxx"
```

## 执行翻译任务

配置完成后，即可使用命令行工具进行翻译。

### 基础用法

使用 `-e ai` 参数指定使用 AI 引擎进行翻译：

```bash showLineNumbers
# python main.py -e [引擎类型] [目标文件路径]
python main.py -e ai "jupyter file/rag_from_scratch_1_to_4.ipynb"
```

### 翻译结果

程序运行完成后，会在原文件同级目录下生成一个新的文件，文件名通常以 `_zh` 结尾：

-   **原文件**：`rag_from_scratch_1_to_4.ipynb`
-   **翻译后**：`rag_from_scratch_1_to_4_zh.ipynb`

你可以直接使用 Jupyter Lab 或 VS Code 打开该文件查看双语或翻译后的内容。