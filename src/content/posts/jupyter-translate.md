---
title: Jupyter Translate 项目教程
published: 2025-10-21
description: Jupyter Translate 项目的详细部署教程
tags: [Translate, Course, Github]
category: Github
draft: false 
---

# Jupyter Translate 项目

## 下载项目

首先进入这个项目的Github网址

::github{repo="jexonn/jupyter-translate"}

照着 readme 安装依赖（挂梯子可能会导致依赖无法正常安装）

但其实依赖并没有很多，可以依次手动安装 `requirements.txt` 中的内容

## 注册API

大模型随便找一个即可，我这里用的是 DeepSeek

```txt showLineNumbers
api_key = sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
base_url = https://api.deepseek.com/v1/
model_name = deepseek-chat
```

也可以用其他 OpenAI 接口兼容的模型

然后来注册一下 Aliyun Machine Translation Service 的密钥

首先进入阿里云进行注册：
https://www.aliyun.com/

然后开通“机器翻译”服务：
https://mt.console.aliyun.com/

最后创建 AccessKey：
https://ram.console.aliyun.com/manage/ak


```txt showLineNumbers
access_key_id = LTAIxxxxxxxxxxxxxxxx
access_key_secret = xxxxxxxxxxxxxxxxxxxxxxxx
```

## 翻译指令

翻译指令如下

```cmd showLineNumbers
python main.py -e ai "jupyter file/rag_from_scratch_1_to_4.ipynb"
```

然后会出现如下的文件 `rag_from_scratch_1_to_4_zh.ipynb`