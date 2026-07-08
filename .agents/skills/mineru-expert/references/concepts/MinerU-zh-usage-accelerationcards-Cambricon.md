---
type: Reference
title: "Cambricon - MinerU"
description: "**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Cambricon/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Cambricon/)"
timestamp: 2026-07-06T03:34:16Z
---
# Cambricon - MinerU
**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Cambricon/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Cambricon/)

# Cambricon

## 1. 测试平台

以下为本指南测试使用的平台信息，供参考：

```
os: Ubuntu 22.04.5 LTS  
cpu: Hygon Hygon C86 7490
mlu: MLU590-M9D
driver: v6.2.11
docker: 28.3.0
```

## 2. 环境准备

Note

Cambricon加速卡支持使用`lmdeploy`或`vllm`进行VLM模型推理加速。请根据实际需求选择安装和使用其中之一:

### 2.1 使用 Dockerfile 构建镜像 （lmdeploy）

```
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/docker/china/mlu.Dockerfile
docker build --network=host -t mineru:mlu-lmdeploy-latest -f mlu.Dockerfile .
```

### 2.2 使用 Dockerfile 构建镜像 （vllm）

```
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/docker/china/mlu.Dockerfile
# 将基础镜像从 lmdeploy 切换为 vllm
sed -i -e '3,4s/^/# /' -e '6,7s/^# //' mlu.Dockerfile
docker build --network=host -t mineru:mlu-vllm-latest -f mlu.Dockerfile .
```

## 3. 启动 Docker 容器

```
docker run --name mineru_docker \
   --privileged \
   --ipc=host \
   --network=host \
   --shm-size=400g \
   --ulimit memlock=-1 \
   -v /dev:/dev \
   -v /lib/modules:/lib/modules:ro \
   -v /usr/bin/cnmon:/usr/bin/cnmon \
   -e MINERU_MODEL_SOURCE=local \
   -e MINERU_LMDEPLOY_DEVICE=camb \
   -it mineru:mlu-lmdeploy-latest \
   /bin/bash
```

Tip

请根据实际情况选择使用`vllm`或`lmdeploy`版本的镜像，如需使用`vllm`,请执行以下操作：

* 替换上述命令中的`mineru:mlu-lmdeploy-latest`为`mineru:mlu-vllm-latest`
* 进入容器后，通过以下命令切换venv环境：

  ```
  source /torch/venv3/pytorch_infer/bin/activate
  ```
* 切换成功后，您可以在命令行前看到`(pytorch_infer)`的标识，这表示您已成功进入`vllm`的虚拟环境。

执行该命令后，您将进入到Docker容器的交互式终端，您可以直接在容器内运行MinerU相关命令来使用MinerU的功能。
您也可以直接通过替换`/bin/bash`为服务启动命令来启动MinerU服务，详细说明请参考[通过命令启动服务](https://opendatalab.github.io/MinerU/zh/usage/quick_usage/#apiwebuihttp-clientserver)。

## 4. 注意事项

Note

**兼容性说明**：由于寒武纪（Cambricon）目前对 vLLM v1 引擎的支持尚待完善，MinerU 现阶段采用 v0 引擎作为适配方案。
受此限制，vLLM 的异步引擎（Async Engine）功能存在兼容性问题，可能导致部分使用场景无法正常运行。
我们将持续跟进寒武纪对 vLLM v1 引擎的支持进展，并及时在 MinerU 中进行相应的适配与优化。

不同环境下，MinerU对Cambricon加速卡的支持情况如下表所示：

Tip

* `lmdeploy`黄灯问题为不能输入文件夹使用批量解析功能，输入单个文件时表现正常。
* `vllm`黄灯问题为在精度未对齐，在部分场景下可能出现预期外结果。

| 使用场景 | | 容器环境 | |
| --- | --- | --- | --- |
| vllm | lmdeploy |
| 命令行工具(mineru) | pipeline | 🟢 | 🟢 |
| <vlm/hybrid>-engine | 🟡 | 🟡 |
| <vlm/hybrid>-http-client | 🟡 | 🟢 |
| fastapi服务(mineru-api) | pipeline | 🟢 | 🟢 |
| <vlm/hybrid>-engine | 🔴 | 🟢 |
| <vlm/hybrid>-http-client | 🟡 | 🟢 |
| gradio界面(mineru-gradio) | pipeline | 🟢 | 🟢 |
| <vlm/hybrid>-engine | 🔴 | 🟢 |
| <vlm/hybrid>-http-client | 🟡 | 🟢 |
| openai-server服务（mineru-openai-server） | | 🟡 | 🟢 |

注：  
🟢: 支持，运行较稳定，精度与Nvidia GPU基本一致  
🟡: 支持但较不稳定，在某些场景下可能出现异常，或精度存在一定差异  
🔴: 不支持，无法运行，或精度存在较大差异

Tip

* Cambricon加速卡指定可用加速卡的方式与NVIDIA GPU类似，请参考[使用指定GPU设备](https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/#cuda_visible_devices)章节说明,
  将环境变量`CUDA_VISIBLE_DEVICES`替换为`MLU_VISIBLE_DEVICES`即可。
* 在Cambricon平台可以通过`cnmon`命令查看加速卡的使用情况，并根据需要指定空闲的加速卡ID以避免资源冲突。

回到页面顶部

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/](./MinerU-zh-usage-advancedcliparameters.md)
- [https://opendatalab.github.io/MinerU/zh/usage/quick_usage/](./MinerU-zh-usage-quickusage.md)
