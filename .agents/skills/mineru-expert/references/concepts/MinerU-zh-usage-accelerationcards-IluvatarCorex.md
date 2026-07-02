# IluvatarCorex - MinerU
**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/IluvatarCorex/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/IluvatarCorex/)

# IluvatarCorex

## 1. 测试平台

以下为本指南测试使用的平台信息，供参考：

```
os: Ubuntu 22.04.5 LTS  
cpu: Intel x86-64
gpu: Iluvatar BI-V150
driver: 4.4.0
docker: 28.1.1
```

## 2. 环境准备

### 2.1 使用 Dockerfile 构建镜像

```
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/docker/china/corex.Dockerfile
docker build --network=host -t mineru:corex-vllm-latest -f corex.Dockerfile .
```

## 3. 启动 Docker 容器

```
docker run --name mineru_docker \
   -v /usr/src:/usr/src \
   -v /lib/modules:/lib/modules \
   -v /dev:/dev \
   --privileged \
   --cap-add=ALL \
   --pid=host \
   --group-add video \
   --network=host \
   --shm-size '400gb' \
   --ulimit memlock=-1 \
   --security-opt seccomp=unconfined \
   --security-opt apparmor=unconfined \
   -e VLLM_ENFORCE_CUDA_GRAPH=1 \
   -e MINERU_MODEL_SOURCE=local \
   -e MINERU_VLLM_DEVICE=corex \
   -it mineru:corex-vllm-latest \
   /bin/bash
```

执行该命令后，您将进入到Docker容器的交互式终端，您可以直接在容器内运行MinerU相关命令来使用MinerU的功能。
您也可以直接通过替换`/bin/bash`为服务启动命令来启动MinerU服务，详细说明请参考[通过命令启动服务](https://opendatalab.github.io/MinerU/zh/usage/quick_usage/#apiwebuihttp-clientserver)。

## 4. 注意事项

Tip

目前Iluvatar方案使用vllm作为推理引擎时，可能出现服务停止后显存无法正常释放的问题，如果遇到该问题，请重启Docker容器以释放显存。

不同环境下，MinerU对Iluvatar加速卡的支持情况如下表所示：

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

* Iluvatar加速卡指定可用加速卡的方式与NVIDIA GPU类似，请参考[使用指定GPU设备](https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/#cuda_visible_devices)章节说明
* 在Iluvatar平台可以通过`ixsmi`命令查看加速卡的使用情况，并根据需要指定空闲的加速卡ID以避免资源冲突。

回到页面顶部

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/](./MinerU-zh-usage-advancedcliparameters.md)
- [https://opendatalab.github.io/MinerU/zh/usage/quick_usage/](./MinerU-zh-usage-quickusage.md)
