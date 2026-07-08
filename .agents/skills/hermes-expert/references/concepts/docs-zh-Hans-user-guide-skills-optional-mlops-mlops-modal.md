# Modal Serverless Gpu — 用于运行 ML 工作负载的无服务器 GPU 云平台 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-modal](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-modal)

本页总览

用于运行 ML 工作负载的无服务器 GPU 云平台。适用于需要按需 GPU 访问而无需管理基础设施、将 ML 模型部署为 API，或运行具有自动扩缩容的批处理作业的场景。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 通过 `hermes skills install official/mlops/modal` 安装 |
| 路径 | `optional-skills/mlops/modal` |
| 版本 | `1.0.0` |
| 作者 | Orchestra Research |
| 许可证 | MIT |
| 依赖 | `modal>=0.64.0` |
| 平台 | linux, macos, windows |
| 标签 | `Infrastructure`, `Serverless`, `GPU`, `Cloud`, `Deployment`, `Modal` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# Modal Serverless GPU

在 Modal 无服务器 GPU 云平台上运行 ML 工作负载的完整指南。

## 何时使用 Modal[​](#何时使用-modal "何时使用 Modal的直接链接")

**在以下情况下使用 Modal：**

* 运行 GPU 密集型 ML 工作负载而无需管理基础设施
* 将 ML 模型部署为自动扩缩容 API
* 运行批处理作业（训练、推理、数据处理）
* 需要按秒计费的 GPU 定价，无空闲成本
* 快速原型化 ML 应用
* 运行定时作业（类 cron 工作负载）

**主要特性：**

* **无服务器 GPU**：按需提供 T4、L4、A10G、L40S、A100、H100、H200、B200
* **Python 原生**：用 Python 代码定义基础设施，无需 YAML
* **自动扩缩容**：缩容至零，或瞬间扩容至 100+ 个 GPU
* **亚秒级冷启动**：基于 Rust 的基础设施，实现快速容器启动
* **容器缓存**：镜像层缓存，支持快速迭代
* **Web 端点**：将函数部署为 REST API，支持零停机更新

**以下情况请使用替代方案：**

* **RunPod**：适用于需要持久状态的长时间运行 pod
* **Lambda Labs**：适用于预留 GPU 实例
* **SkyPilot**：适用于多云编排和成本优化
* **Kubernetes**：适用于复杂的多服务架构

## 快速开始[​](#快速开始 "快速开始的直接链接")

### 安装[​](#安装 "安装的直接链接")

```
pip install modal  
modal setup  # Opens browser for authentication
```

### GPU Hello World[​](#gpu-hello-world "GPU Hello World的直接链接")

```
import modal  
  
app = modal.App("hello-gpu")  
  
@app.function(gpu="T4")  
def gpu_info():  
    import subprocess  
    return subprocess.run(["nvidia-smi"], capture_output=True, text=True).stdout  
  
@app.local_entrypoint()  
def main():  
    print(gpu_info.remote())
```

运行：`modal run hello_gpu.py`

### 基础推理端点[​](#基础推理端点 "基础推理端点的直接链接")

```
import modal  
  
app = modal.App("text-generation")  
image = modal.Image.debian_slim().pip_install("transformers", "torch", "accelerate")  
  
@app.cls(gpu="A10G", image=image)  
class TextGenerator:  
    @modal.enter()  
    def load_model(self):  
        from transformers import pipeline  
        self.pipe = pipeline("text-generation", model="gpt2", device=0)  
  
    @modal.method()  
    def generate(self, prompt: str) -> str:  
        return self.pipe(prompt, max_length=100)[0]["generated_text"]  
  
@app.local_entrypoint()  
def main():  
    print(TextGenerator().generate.remote("Hello, world"))
```

## 核心概念[​](#核心概念 "核心概念的直接链接")

### 关键组件[​](#关键组件 "关键组件的直接链接")

| 组件 | 用途 |
| --- | --- |
| `App` | 函数和资源的容器 |
| `Function` | 带计算规格的无服务器函数 |
| `Cls` | 带生命周期 hook 的基于类的函数 |
| `Image` | 容器镜像定义 |
| `Volume` | 用于模型/数据的持久存储 |
| `Secret` | 安全凭证存储 |

### 执行模式[​](#执行模式 "执行模式的直接链接")

| 命令 | 描述 |
| --- | --- |
| `modal run script.py` | 执行后退出 |
| `modal serve script.py` | 开发模式，支持热重载 |
| `modal deploy script.py` | 持久化云端部署 |

## GPU 配置[​](#gpu-配置 "GPU 配置的直接链接")

### 可用 GPU[​](#可用-gpu "可用 GPU的直接链接")

| GPU | 显存 | 最适用于 |
| --- | --- | --- |
| `T4` | 16GB | 经济型推理、小型模型 |
| `L4` | 24GB | 推理，Ada Lovelace 架构 |
| `A10G` | 24GB | 训练/推理，比 T4 快 3.3 倍 |
| `L40S` | 48GB | 推荐用于推理（最佳性价比） |
| `A100-40GB` | 40GB | 大型模型训练 |
| `A100-80GB` | 80GB | 超大型模型 |
| `H100` | 80GB | 最快，支持 FP8 + Transformer Engine |
| `H200` | 141GB | 从 H100 自动升级，4.8TB/s 带宽 |
| `B200` | 最新 | Blackwell 架构 |

### GPU 规格配置模式[​](#gpu-规格配置模式 "GPU 规格配置模式的直接链接")

```
# Single GPU  
@app.function(gpu="A100")  
  
# Specific memory variant  
@app.function(gpu="A100-80GB")  
  
# Multiple GPUs (up to 8)  
@app.function(gpu="H100:4")  
  
# GPU with fallbacks  
@app.function(gpu=["H100", "A100", "L40S"])  
  
# Any available GPU  
@app.function(gpu="any")
```

## 容器镜像[​](#容器镜像 "容器镜像的直接链接")

```
# Basic image with pip  
image = modal.Image.debian_slim(python_version="3.11").pip_install(  
    "torch==2.1.0", "transformers==4.36.0", "accelerate"  
)  
  
# From CUDA base  
image = modal.Image.from_registry(  
    "nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04",  
    add_python="3.11"  
).pip_install("torch", "transformers")  
  
# With system packages  
image = modal.Image.debian_slim().apt_install("git", "ffmpeg").pip_install("whisper")
```

## 持久存储[​](#持久存储 "持久存储的直接链接")

```
volume = modal.Volume.from_name("model-cache", create_if_missing=True)  
  
@app.function(gpu="A10G", volumes={"/models": volume})  
def load_model():  
    import os  
    model_path = "/models/llama-7b"  
    if not os.path.exists(model_path):  
        model = download_model()  
        model.save_pretrained(model_path)  
        volume.commit()  # Persist changes  
    return load_from_path(model_path)
```

## Web 端点[​](#web-端点 "Web 端点的直接链接")

### FastAPI 端点装饰器[​](#fastapi-端点装饰器 "FastAPI 端点装饰器的直接链接")

```
@app.function()  
@modal.fastapi_endpoint(method="POST")  
def predict(text: str) -> dict:  
    return {"result": model.predict(text)}
```

### 完整 ASGI 应用[​](#完整-asgi-应用 "完整 ASGI 应用的直接链接")

```
from fastapi import FastAPI  
web_app = FastAPI()  
  
@web_app.post("/predict")  
async def predict(text: str):  
    return {"result": await model.predict.remote.aio(text)}  
  
@app.function()  
@modal.asgi_app()  
def fastapi_app():  
    return web_app
```

### Web 端点类型[​](#web-端点类型 "Web 端点类型的直接链接")

| 装饰器 | 使用场景 |
| --- | --- |
| `@modal.fastapi_endpoint()` | 简单函数 → API |
| `@modal.asgi_app()` | 完整 FastAPI/Starlette 应用 |
| `@modal.wsgi_app()` | Django/Flask 应用 |
| `@modal.web_server(port)` | 任意 HTTP 服务器 |

## 动态批处理[​](#动态批处理 "动态批处理的直接链接")

```
@app.function()  
@modal.batched(max_batch_size=32, wait_ms=100)  
async def batch_predict(inputs: list[str]) -> list[dict]:  
    # Inputs automatically batched  
    return model.batch_predict(inputs)
```

## 密钥管理[​](#密钥管理 "密钥管理的直接链接")

```
# Create secret  
modal secret create huggingface HF_TOKEN=hf_xxx
```

```
@app.function(secrets=[modal.Secret.from_name("huggingface")])  
def download_model():  
    import os  
    token = os.environ["HF_TOKEN"]
```

## 定时任务[​](#定时任务 "定时任务的直接链接")

```
@app.function(schedule=modal.Cron("0 0 * * *"))  # Daily midnight  
def daily_job():  
    pass  
  
@app.function(schedule=modal.Period(hours=1))  
def hourly_job():  
    pass
```

## 性能优化[​](#性能优化 "性能优化的直接链接")

### 冷启动缓解[​](#冷启动缓解 "冷启动缓解的直接链接")

```
@app.function(  
    container_idle_timeout=300,  # Keep warm 5 min  
    allow_concurrent_inputs=10,  # Handle concurrent requests  
)  
def inference():  
    pass
```

### 模型加载最佳实践[​](#模型加载最佳实践 "模型加载最佳实践的直接链接")

```
@app.cls(gpu="A100")  
class Model:  
    @modal.enter()  # Run once at container start  
    def load(self):  
        self.model = load_model()  # Load during warm-up  
  
    @modal.method()  
    def predict(self, x):  
        return self.model(x)
```

## 并行处理[​](#并行处理 "并行处理的直接链接")

```
@app.function()  
def process_item(item):  
    return expensive_computation(item)  
  
@app.function()  
def run_parallel():  
    items = list(range(1000))  
    # Fan out to parallel containers  
    results = list(process_item.map(items))  
    return results
```

## 常用配置[​](#常用配置 "常用配置的直接链接")

```
@app.function(  
    gpu="A100",  
    memory=32768,              # 32GB RAM  
    cpu=4,                     # 4 CPU cores  
    timeout=3600,              # 1 hour max  
    container_idle_timeout=120,# Keep warm 2 min  
    retries=3,                 # Retry on failure  
    concurrency_limit=10,      # Max concurrent containers  
)  
def my_function():  
    pass
```

## 调试[​](#调试 "调试的直接链接")

```
# Test locally  
if __name__ == "__main__":  
    result = my_function.local()  
  
# View logs  
# modal app logs my-app
```

## 常见问题[​](#常见问题 "常见问题的直接链接")

| 问题 | 解决方案 |
| --- | --- |
| 冷启动延迟 | 增大 `container_idle_timeout`，使用 `@modal.enter()` |
| GPU 内存溢出 | 使用更大 GPU（`A100-80GB`），启用梯度检查点 |
| 镜像构建失败 | 固定依赖版本，检查 CUDA 兼容性 |
| 超时错误 | 增大 `timeout`，添加检查点 |

## 参考资料[​](#参考资料 "参考资料的直接链接")

* **[高级用法](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/modal/references/advanced-usage.md)** - 多 GPU、分布式训练、成本优化
* **[故障排查](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/modal/references/troubleshooting.md)** - 常见问题与解决方案

## 资源[​](#资源 "资源的直接链接")

* **文档**：<https://modal.com/docs>
* **示例**：<https://github.com/modal-labs/modal-examples>
* **定价**：<https://modal.com/pricing>
* **Discord**：<https://discord.gg/modal>

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [何时使用 Modal](#何时使用-modal)
* [快速开始](#快速开始)
  + [安装](#安装)
  + [GPU Hello World](#gpu-hello-world)
  + [基础推理端点](#基础推理端点)
* [核心概念](#核心概念)
  + [关键组件](#关键组件)
  + [执行模式](#执行模式)
* [GPU 配置](#gpu-配置)
  + [可用 GPU](#可用-gpu)
  + [GPU 规格配置模式](#gpu-规格配置模式)
* [容器镜像](#容器镜像)
* [持久存储](#持久存储)
* [Web 端点](#web-端点)
  + [FastAPI 端点装饰器](#fastapi-端点装饰器)
  + [完整 ASGI 应用](#完整-asgi-应用)
  + [Web 端点类型](#web-端点类型)
* [动态批处理](#动态批处理)
* [密钥管理](#密钥管理)
* [定时任务](#定时任务)
* [性能优化](#性能优化)
  + [冷启动缓解](#冷启动缓解)
  + [模型加载最佳实践](#模型加载最佳实践)
* [并行处理](#并行处理)
* [常用配置](#常用配置)
* [调试](#调试)
* [常见问题](#常见问题)
* [参考资料](#参考资料)
* [资源](#资源)