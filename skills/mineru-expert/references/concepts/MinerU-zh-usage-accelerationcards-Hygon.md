---
type: Reference
title: "Hygon - MinerU"
description: "**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Hygon/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Hygon/)"
timestamp: 2026-07-06T03:34:16Z
---
# Hygon - MinerU
**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Hygon/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Hygon/)

# Hygon

## 1. 测试平台

以下为本指南测试使用的平台信息，供参考：

```
os: Ubuntu 22.04.3 LTS  
cpu: Hygon C86-4G(x86-64)
dcu: BW200
driver: 6.3.13-V1.12.0a
docker: 20.10.24
```

## 2. 环境准备

### 2.1 使用 Dockerfile 构建镜像

```
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/docker/china/dcu.Dockerfile
docker build --network=host -t mineru:dcu-vllm-latest -f dcu.Dockerfile .
```

## 3. 启动 Docker 容器

```
docker run -u root --name mineru_docker \
    --network=host \
    --ipc=host \
    --shm-size=16G \
    --device=/dev/kfd \
    --device=/dev/mkfd \
    --device=/dev/dri \
    -v /opt/hyhal:/opt/hyhal \
    --group-add video \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    -e MINERU_MODEL_SOURCE=local \
    -it mineru:dcu-vllm-latest \
    /bin/bash
```

执行该命令后，您将进入到Docker容器的交互式终端，您可以直接在容器内运行MinerU相关命令来使用MinerU的功能。
您也可以直接通过替换`/bin/bash`为服务启动命令来启动MinerU服务，详细说明请参考[通过命令启动服务](https://opendatalab.github.io/MinerU/zh/usage/quick_usage/#apiwebuihttp-clientserver)。

## 4. 注意事项

不同环境下，MinerU对Hygon加速卡的支持情况如下表所示：

| 使用场景 | | 容器环境 | |
| --- | --- | --- | --- |
| vllm |
| 命令行工具(mineru) | pipeline | 🟢 |
| <vlm/hybrid>-engine | 🟢 |
| <vlm/hybrid>-http-client | 🟢 |
| fastapi服务(mineru-api) | pipeline | 🟢 |
| <vlm/hybrid>-engine | 🟢 |
| <vlm/hybrid>-http-client | 🟢 |
| gradio界面(mineru-gradio) | pipeline | 🟢 |
| <vlm/hybrid>-engine | 🟢 |
| <vlm/hybrid>-http-client | 🟢 |
| openai-server服务（mineru-openai-server） | | 🟢 |

注：  
🟢: 支持，运行较稳定，精度与Nvidia GPU基本一致  
🟡: 支持但较不稳定，在某些场景下可能出现异常，或精度存在一定差异  
🔴: 不支持，无法运行，或精度存在较大差异

Tip

* DCU加速卡指定可用加速卡的方式与AMD GPU类似，请参考[GPU isolation techniques](https://rocm.docs.amd.com/en/docs-6.2.4/conceptual/gpu-isolation.html)
* 在Hygon平台可以通过`hy-smi`命令查看加速卡的使用情况，并根据需要指定空闲的加速卡ID以避免资源冲突。

回到页面顶部

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/zh/usage/quick_usage/](./MinerU-zh-usage-quickusage.md)
