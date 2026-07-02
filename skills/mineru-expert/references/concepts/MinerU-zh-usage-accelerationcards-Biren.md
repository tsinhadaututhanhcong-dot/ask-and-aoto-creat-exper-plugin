# Biren - MinerU
**Source:** [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Biren/](https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Biren/)

# Biren

## 1. 测试平台

以下为本指南测试使用的平台信息，供参考：

```
os: Ubuntu 22.04.4 LTS
cpu: Intel x86-64
gpu: Biren 106C
driver: 1.10.0
docker: 28.0.4
```

## 2. 环境准备

### 2.1 下载并加载镜像 （vllm）

```
wget http://birentech.com/xxx/MinerU/mineru-vllm.tar 链接获取请联系壁仞内部人员（邮箱：MonaLiu@birentech.com）
docker load -i mineru-vllm.tar
```

## 3. 启动 Docker 容器

```
docker run -it --name mineru_docker \
    --privileged \
    --network=host \
    --shm-size=100G \
    -e MINERU_MODEL_SOURCE=local \
    -e MINERU_DEVICE_MODEL=supa \
    -e SHAPE_TRANSFORM_GRANK=true \
    mineru:biren-vllm-latest \
    /bin/bash
```

执行该命令后，您将进入到Docker容器的交互式终端，您可以直接在容器内运行MinerU相关命令来使用MinerU的功能。
您也可以直接通过替换`/bin/bash`为服务启动命令来启动MinerU服务，详细说明请参考[通过命令启动服务](https://opendatalab.github.io/MinerU/zh/usage/quick_usage/#apiwebuihttp-clientserver)。

## 4. 注意事项

不同环境下，MinerU对Biren加速卡的支持情况如下表所示：

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

* Biren加速卡指定可用加速卡的方式与NVIDIA GPU类似，请参考[使用指定GPU设备](https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/#cuda_visible_devices)章节说明,
  将环境变量`CUDA_VISIBLE_DEVICES`替换为`SUPA_VISIBLE_DEVICES`即可。
* 在壁仞平台可以通过`brsmi`命令查看加速卡的使用情况，并根据需要指定空闲的加速卡ID以避免资源冲突。

回到页面顶部

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/](./MinerU-zh-usage-advancedcliparameters.md)
- [https://opendatalab.github.io/MinerU/zh/usage/quick_usage/](./MinerU-zh-usage-quickusage.md)
