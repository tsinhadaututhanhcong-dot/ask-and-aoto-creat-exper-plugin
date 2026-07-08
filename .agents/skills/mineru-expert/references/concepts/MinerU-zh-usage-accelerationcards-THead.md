---
type: Reference
title: "THead - MinerU"
description: "**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/THead/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/THead/)"
timestamp: 2026-07-06T03:34:16Z
---
# THead - MinerU
**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/THead/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/THead/)

# THead

## 1. 测试平台

以下为本指南测试使用的平台信息，供参考：

```
os: Ubuntu 22.04   
cpu: INTEL x86_64
ppu: ZW810E  
driver: 1.4.0
docker: 26.1.4
```

## 2. 环境准备

Note

ppu加速卡支持使用`vllm`或`lmdeploy`进行VLM模型推理加速。请根据实际需求选择安装和使用其中之一:

### 2.1 使用 Dockerfile 构建镜像 （vllm）

```
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/docker/china/ppu.Dockerfile
docker build --network=host -t mineru:ppu-vllm-latest -f ppu.Dockerfile .
```

### 2.2 使用 Dockerfile 构建镜像 （lmdeploy）

```
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/docker/china/ppu.Dockerfile
# 将基础镜像从 vllm 切换为 lmdeploy
sed -i '3s/^/# /' ppu.Dockerfile && sed -i '5,6s/^# //' ppu.Dockerfile
docker build --network=host -t mineru:ppu-lmdeploy-latest -f ppu.Dockerfile .
```

## 3. 启动 Docker 容器

```
docker run --privileged=true \
  --name mineru_docker \
  --device=/dev/alixpu \
  --device=/dev/alixpu_ctl \
  --ipc=host \
  --network=host \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --shm-size=500g \
  -v /mnt:/mnt \
  -v /datapool:/datapool \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e MINERU_MODEL_SOURCE=local \
  -it mineru:ppu-vllm-latest \
  /bin/bash
```

Tip

请根据实际情况选择使用`vllm`或`lmdeploy`版本的镜像，如需使用lmdeploy，替换上述命令中的`mineru:ppu-vllm-latest`为`mineru:ppu-lmdeploy-latest`即可。

执行该命令后，您将进入到Docker容器的交互式终端，您可以直接在容器内运行MinerU相关命令来使用MinerU的功能。
您也可以直接通过替换`/bin/bash`为服务启动命令来启动MinerU服务，详细说明请参考[通过命令启动服务](https://opendatalab.github.io/MinerU/zh/usage/quick_usage/#apiwebuihttp-clientserver)。

## 4. 注意事项

不同环境下，MinerU对ppu加速卡的支持情况如下表所示：

| 使用场景 | | 容器环境 | |
| --- | --- | --- | --- |
| vllm | lmdeploy |
| 命令行工具(mineru) | pipeline | 🟢 | 🟢 |
| <vlm/hybrid>-engine | 🟢 | 🟢 |
| <vlm/hybrid>-http-client | 🟢 | 🟢 |
| fastapi服务(mineru-api) | pipeline | 🟢 | 🟢 |
| <vlm/hybrid>-engine | 🟢 | 🟢 |
| <vlm/hybrid>-http-client | 🟢 | 🟢 |
| gradio界面(mineru-gradio) | pipeline | 🟢 | 🟢 |
| <vlm/hybrid>-engine | 🟢 | 🟢 |
| <vlm/hybrid>-http-client | 🟢 | 🟢 |
| openai-server服务（mineru-openai-server） | | 🟢 | 🟢 |

注：  
🟢: 支持，运行较稳定，精度与Nvidia GPU基本一致  
🟡: 支持但较不稳定，在某些场景下可能出现异常，或精度存在一定差异  
🔴: 不支持，无法运行，或精度存在较大差异

Tip

* PPU加速卡指定可用加速卡的方式与NVIDIA GPU类似，请参考[使用指定GPU设备](https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/#cuda_visible_devices)章节说明。
* 在T-Head平台可以通过`ppu-smi`命令查看加速卡的使用情况，并根据需要指定空闲的加速卡ID以避免资源冲突。

回到页面顶部

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/](./MinerU-zh-usage-advancedcliparameters.md)
- [https://opendatalab.github.io/MinerU/zh/usage/quick_usage/](./MinerU-zh-usage-quickusage.md)
