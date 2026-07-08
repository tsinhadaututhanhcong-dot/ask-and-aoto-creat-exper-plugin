# Heartmula — HeartMuLa：基于歌词与标签的类 Suno 歌曲生成 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/media/media-heartmula](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/media/media-heartmula)

本页总览

HeartMuLa：基于歌词与标签的类 Suno 歌曲生成。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/media/heartmula` |
| 版本 | `1.0.0` |
| 平台 | linux, macos, windows |
| 标签 | `music`, `audio`, `generation`, `ai`, `heartmula`, `heartcodec`, `lyrics`, `songs` |
| 相关 skill | `audiocraft` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# HeartMuLa - 开源音乐生成

## 概述[​](#概述 "概述的直接链接")

HeartMuLa 是一系列开源音乐基础模型（Apache-2.0），可根据歌词和标签生成音乐，支持多语言。能从歌词与标签生成完整歌曲，是开源领域中可与 Suno 媲美的方案。包含：

* **HeartMuLa** — 音乐语言模型（3B/7B），从歌词与标签生成音乐
* **HeartCodec** — 12.5Hz 音乐编解码器，用于高保真音频重建
* **HeartTranscriptor** — 基于 Whisper 的歌词转录工具
* **HeartCLAP** — 音频-文本对齐模型

## 使用场景[​](#使用场景 "使用场景的直接链接")

* 用户希望从文本描述生成音乐/歌曲
* 用户需要开源的 Suno 替代方案
* 用户需要本地/离线音乐生成
* 用户询问 HeartMuLa、heartlib 或 AI 音乐生成相关内容

## 硬件要求[​](#硬件要求 "硬件要求的直接链接")

* **最低配置**：8GB 显存，配合 `--lazy_load true`（按需加载/卸载模型）
* **推荐配置**：16GB+ 显存，可在单 GPU 上流畅运行
* **多 GPU**：使用 `--mula_device cuda:0 --codec_device cuda:1` 将模型分布到多张 GPU
* 3B 模型在 lazy\_load 模式下峰值显存约为 6.2GB

## 安装步骤[​](#安装步骤 "安装步骤的直接链接")

### 1. 克隆仓库[​](#1-克隆仓库 "1. 克隆仓库的直接链接")

```
cd ~/  # 或目标目录  
git clone https://github.com/HeartMuLa/heartlib.git  
cd heartlib
```

### 2. 创建虚拟环境（需要 Python 3.10）[​](#2-创建虚拟环境需要-python-310 "2. 创建虚拟环境（需要 Python 3.10）的直接链接")

```
uv venv --python 3.10 .venv  
. .venv/bin/activate  
uv pip install -e .
```

### 3. 修复依赖兼容性问题[​](#3-修复依赖兼容性问题 "3. 修复依赖兼容性问题的直接链接")

**重要**：截至 2026 年 2 月，固定的依赖版本与较新的包存在冲突。请应用以下修复：

```
# 升级 datasets（旧版本与当前 pyarrow 不兼容）  
uv pip install --upgrade datasets  
  
# 升级 transformers（需要兼容 huggingface-hub 1.x）  
uv pip install --upgrade transformers
```

### 4. 修补源代码（transformers 5.x 必须执行）[​](#4-修补源代码transformers-5x-必须执行 "4. 修补源代码（transformers 5.x 必须执行）的直接链接")

**补丁 1 — RoPE 缓存修复**，文件：`src/heartlib/heartmula/modeling_heartmula.py`：

在 `HeartMuLa` 类的 `setup_caches` 方法中，在 `reset_caches` 的 try/except 块之后、`with device:` 块之前，添加 RoPE 重新初始化代码：

```
# Re-initialize RoPE caches that were skipped during meta-device loading  
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE  
for module in self.modules():  
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:  
        module.rope_init()  
        module.to(device)
```

**原因**：`from_pretrained` 首先在 meta 设备上创建模型；`Llama3ScaledRoPE.rope_init()` 在 meta 张量上跳过缓存构建，且在权重加载到真实设备后也不会重建。

**补丁 2 — HeartCodec 加载修复**，文件：`src/heartlib/pipelines/music_generation.py`：

在所有 `HeartCodec.from_pretrained()` 调用中添加 `ignore_mismatched_sizes=True`（共 2 处：`__init__` 中的 eager 加载和 `codec` 属性中的 lazy 加载）。

**原因**：VQ codebook 的 `initted` buffer 在 checkpoint 中形状为 `[1]`，而模型中为 `[]`。数据相同，仅为标量与 0 维张量的差异，可安全忽略。

### 5. 下载模型检查点[​](#5-下载模型检查点 "5. 下载模型检查点的直接链接")

```
cd heartlib  # 项目根目录  
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'  
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'  
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

三个检查点可并行下载，总大小为数 GB。

## GPU / CUDA[​](#gpu--cuda "GPU / CUDA的直接链接")

HeartMuLa 默认使用 CUDA（`--mula_device cuda --codec_device cuda`）。如果用户已安装支持 CUDA 的 PyTorch 并拥有 NVIDIA GPU，则无需额外配置。

* 已安装的 `torch==2.4.1` 开箱即支持 CUDA 12.1
* `torchtune` 可能显示版本为 `0.4.0+cpu` — 这只是包元数据，实际仍通过 PyTorch 使用 CUDA
* 如需确认 GPU 是否被使用，可查看输出中的 "CUDA memory" 行（例如 "CUDA memory before unloading: 6.20 GB"）
* **没有 GPU？** 可使用 `--mula_device cpu --codec_device cpu` 在 CPU 上运行，但生成速度会**极慢**（单首歌曲可能需要 30-60 分钟以上，而 GPU 约需 4 分钟）。CPU 模式还需要大量内存（12GB+ 空闲）。如果用户没有 NVIDIA GPU，建议使用云 GPU 服务（Google Colab 免费 T4、Lambda Labs 等）或访问在线 demo：<https://heartmula.github.io/>

## 使用方法[​](#使用方法 "使用方法的直接链接")

### 基本生成[​](#基本生成 "基本生成的直接链接")

```
cd heartlib  
. .venv/bin/activate  
python ./examples/run_music_generation.py \  
  --model_path=./ckpt \  
  --version="3B" \  
  --lyrics="./assets/lyrics.txt" \  
  --tags="./assets/tags.txt" \  
  --save_path="./assets/output.mp3" \  
  --lazy_load true
```

### 输入格式[​](#输入格式 "输入格式的直接链接")

**标签**（逗号分隔，无空格）：

```
piano,happy,wedding,synthesizer,romantic
```

或

```
rock,energetic,guitar,drums,male-vocal
```

**歌词**（使用方括号结构标签）：

```
[Intro]  
  
[Verse]  
Your lyrics here...  
  
[Chorus]  
Chorus lyrics...  
  
[Bridge]  
Bridge lyrics...  
  
[Outro]
```

### 关键参数[​](#关键参数 "关键参数的直接链接")

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--max_audio_length_ms` | 240000 | 最大时长（毫秒，240s = 4 分钟） |
| `--topk` | 50 | Top-k 采样 |
| `--temperature` | 1.0 | 采样温度（temperature） |
| `--cfg_scale` | 1.5 | 无分类器引导（classifier-free guidance）缩放比例 |
| `--lazy_load` | false | 按需加载/卸载模型（节省显存） |
| `--mula_dtype` | bfloat16 | HeartMuLa 的数据类型（推荐 bf16） |
| `--codec_dtype` | float32 | HeartCodec 的数据类型（推荐 fp32 以保证质量） |

### 性能[​](#性能 "性能的直接链接")

* RTF（实时率）≈ 1.0 — 生成一首 4 分钟的歌曲约需 4 分钟
* 输出：MP3，48kHz 立体声，128kbps

## 注意事项[​](#注意事项 "注意事项的直接链接")

1. **不要对 HeartCodec 使用 bf16** — 会降低音频质量。请使用 fp32（默认值）。
2. **标签可能被忽略** — 已知问题（#90）。歌词往往占主导地位；建议尝试调整标签顺序。
3. **macOS 上 Triton 不可用** — GPU 加速仅支持 Linux/CUDA。
4. 上游 issue 中报告了 **RTX 5080 不兼容**问题。
5. 依赖版本冲突需要按上述说明手动升级并打补丁。

## 相关链接[​](#相关链接 "相关链接的直接链接")

* 仓库：<https://github.com/HeartMuLa/heartlib>
* 模型：<https://huggingface.co/HeartMuLa>
* 论文：<https://arxiv.org/abs/2601.10547>
* 许可证：Apache-2.0

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [概述](#概述)
* [使用场景](#使用场景)
* [硬件要求](#硬件要求)
* [安装步骤](#安装步骤)
  + [1. 克隆仓库](#1-克隆仓库)
  + [2. 创建虚拟环境（需要 Python 3.10）](#2-创建虚拟环境需要-python-310)
  + [3. 修复依赖兼容性问题](#3-修复依赖兼容性问题)
  + [4. 修补源代码（transformers 5.x 必须执行）](#4-修补源代码transformers-5x-必须执行)
  + [5. 下载模型检查点](#5-下载模型检查点)
* [GPU / CUDA](#gpu--cuda)
* [使用方法](#使用方法)
  + [基本生成](#基本生成)
  + [输入格式](#输入格式)
  + [关键参数](#关键参数)
  + [性能](#性能)
* [注意事项](#注意事项)
* [相关链接](#相关链接)