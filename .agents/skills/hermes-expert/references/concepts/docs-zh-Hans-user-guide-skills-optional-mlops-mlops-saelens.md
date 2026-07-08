# 稀疏自编码器训练 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-saelens](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-saelens)

本页总览

提供使用 SAELens 训练和分析稀疏自编码器（SAE）的指导，将神经网络激活分解为可解释特征。适用于发现可解释特征、分析叠加现象，或研究语言模型中的单义性表示。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 通过 `hermes skills install official/mlops/saelens` 安装 |
| 路径 | `optional-skills/mlops/saelens` |
| 版本 | `1.0.0` |
| 作者 | Orchestra Research |
| 许可证 | MIT |
| 依赖 | `sae-lens>=6.0.0`, `transformer-lens>=2.0.0`, `torch>=2.0.0` |
| 平台 | linux, macos, windows |
| 标签 | `Sparse Autoencoders`, `SAE`, `Mechanistic Interpretability`, `Feature Discovery`, `Superposition` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发该 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# SAELens：用于机制可解释性的稀疏自编码器

SAELens 是训练和分析稀疏自编码器（SAE）的主要库。SAE 是一种将多义性神经网络激活分解为稀疏、可解释特征的技术，基于 Anthropic 在单义性方面的开创性研究。

**GitHub**：[jbloomAus/SAELens](https://github.com/jbloomAus/SAELens)（1,100+ stars）

## 问题背景：多义性与叠加（Superposition）[​](#问题背景多义性与叠加superposition "问题背景：多义性与叠加（Superposition）的直接链接")

神经网络中的单个神经元是**多义性**的——它们在多种语义不同的上下文中激活。这是因为模型使用**叠加**（superposition）来表示比神经元数量更多的特征，从而使可解释性变得困难。

**SAE 的解决方案**：将密集激活分解为稀疏的单义性特征——对于任意给定输入，通常只有少量特征激活，且每个特征对应一个可解释的概念。

## 何时使用 SAELens[​](#何时使用-saelens "何时使用 SAELens的直接链接")

**在以下情况下使用 SAELens：**

* 发现模型激活中的可解释特征
* 理解模型学到了哪些概念
* 研究叠加现象和特征几何结构
* 执行基于特征的引导（steering）或消融（ablation）
* 分析安全相关特征（欺骗、偏见、有害内容）

**在以下情况下考虑替代方案：**

* 需要基础激活分析 → 直接使用 **TransformerLens**
* 需要因果干预实验 → 使用 **pyvene** 或 **TransformerLens**
* 需要生产环境引导 → 考虑直接激活工程

## 安装[​](#安装 "安装的直接链接")

```
pip install sae-lens
```

要求：Python 3.10+，transformer-lens>=2.0.0

## 核心概念[​](#核心概念 "核心概念的直接链接")

### SAE 学到了什么[​](#sae-学到了什么 "SAE 学到了什么的直接链接")

SAE 通过稀疏瓶颈重建模型激活：

```
Input Activation → Encoder → Sparse Features → Decoder → Reconstructed Activation  
    (d_model)       ↓        (d_sae >> d_model)    ↓         (d_model)  
                 sparsity                      reconstruction  
                 penalty                          loss
```

**损失函数**：`MSE(original, reconstructed) + L1_coefficient × L1(features)`

### 关键验证（Anthropic 研究）[​](#关键验证anthropic-研究 "关键验证（Anthropic 研究）的直接链接")

在《Towards Monosemanticity》中，人工评估者发现 **70% 的 SAE 特征具有真正的可解释性**。发现的特征包括：

* DNA 序列、法律语言、HTTP 请求
* 希伯来文本、营养声明、代码语法
* 情感、命名实体、语法结构

## 工作流 1：加载和分析预训练 SAE[​](#工作流-1加载和分析预训练-sae "工作流 1：加载和分析预训练 SAE的直接链接")

### 步骤说明[​](#步骤说明 "步骤说明的直接链接")

```
from transformer_lens import HookedTransformer  
from sae_lens import SAE  
  
# 1. 加载模型和预训练 SAE  
model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")  
sae, cfg_dict, sparsity = SAE.from_pretrained(  
    release="gpt2-small-res-jb",  
    sae_id="blocks.8.hook_resid_pre",  
    device="cuda"  
)  
  
# 2. 获取模型激活  
tokens = model.to_tokens("The capital of France is Paris")  
_, cache = model.run_with_cache(tokens)  
activations = cache["resid_pre", 8]  # [batch, pos, d_model]  
  
# 3. 编码为 SAE 特征  
sae_features = sae.encode(activations)  # [batch, pos, d_sae]  
print(f"Active features: {(sae_features > 0).sum()}")  
  
# 4. 找出每个位置的顶部特征  
for pos in range(tokens.shape[1]):  
    top_features = sae_features[0, pos].topk(5)  
    token = model.to_str_tokens(tokens[0, pos:pos+1])[0]  
    print(f"Token '{token}': features {top_features.indices.tolist()}")  
  
# 5. 重建激活  
reconstructed = sae.decode(sae_features)  
reconstruction_error = (activations - reconstructed).norm()
```

### 可用预训练 SAE[​](#可用预训练-sae "可用预训练 SAE的直接链接")

| Release | 模型 | 层 |
| --- | --- | --- |
| `gpt2-small-res-jb` | GPT-2 Small | 多个残差流 |
| `gemma-2b-res` | Gemma 2B | 残差流 |
| HuggingFace 上的各类 SAE | 搜索标签 `saelens` | 各种 |

### 检查清单[​](#检查清单 "检查清单的直接链接")

* 使用 TransformerLens 加载模型
* 为目标层加载匹配的 SAE
* 将激活编码为稀疏特征
* 识别每个 token 的顶部激活特征
* 验证重建质量

## 工作流 2：训练自定义 SAE[​](#工作流-2训练自定义-sae "工作流 2：训练自定义 SAE的直接链接")

### 步骤说明[​](#步骤说明-1 "步骤说明的直接链接")

```
from sae_lens import SAE, LanguageModelSAERunnerConfig, SAETrainingRunner  
  
# 1. 配置训练  
cfg = LanguageModelSAERunnerConfig(  
    # 模型  
    model_name="gpt2-small",  
    hook_name="blocks.8.hook_resid_pre",  
    hook_layer=8,  
    d_in=768,  # 模型维度  
  
    # SAE 架构  
    architecture="standard",  # 或 "gated"、"topk"  
    d_sae=768 * 8,  # 扩展因子为 8  
    activation_fn="relu",  
  
    # 训练  
    lr=4e-4,  
    l1_coefficient=8e-5,  # 稀疏性惩罚  
    l1_warm_up_steps=1000,  
    train_batch_size_tokens=4096,  
    training_tokens=100_000_000,  
  
    # 数据  
    dataset_path="monology/pile-uncopyrighted",  
    context_size=128,  
  
    # 日志  
    log_to_wandb=True,  
    wandb_project="sae-training",  
  
    # 检查点  
    checkpoint_path="checkpoints",  
    n_checkpoints=5,  
)  
  
# 2. 训练  
trainer = SAETrainingRunner(cfg)  
sae = trainer.run()  
  
# 3. 评估  
print(f"L0 (avg active features): {trainer.metrics['l0']}")  
print(f"CE Loss Recovered: {trainer.metrics['ce_loss_score']}")
```

### 关键超参数[​](#关键超参数 "关键超参数的直接链接")

| 参数 | 典型值 | 效果 |
| --- | --- | --- |
| `d_sae` | 4–16× d\_model | 特征更多，容量更大 |
| `l1_coefficient` | 5e-5 到 1e-4 | 越高 = 越稀疏，精度越低 |
| `lr` | 1e-4 到 1e-3 | 标准优化器学习率 |
| `l1_warm_up_steps` | 500–2000 | 防止特征早期死亡 |

### 评估指标[​](#评估指标 "评估指标的直接链接")

| 指标 | 目标值 | 含义 |
| --- | --- | --- |
| **L0** | 50–200 | 每个 token 的平均激活特征数 |
| **CE Loss Score** | 80–95% | 相对原始模型恢复的交叉熵 |
| **Dead Features** | <5% | 从不激活的特征比例 |
| **Explained Variance** | >90% | 重建质量 |

### 检查清单[​](#检查清单-1 "检查清单的直接链接")

* 选择目标层和 hook 点
* 设置扩展因子（d\_sae = 4–16× d\_model）
* 调整 L1 系数以获得期望的稀疏度
* 启用 L1 预热以防止特征死亡
* 训练期间监控指标（W&B）
* 验证 L0 和 CE loss 恢复情况
* 检查死亡特征比例

## 工作流 3：特征分析与引导[​](#工作流-3特征分析与引导 "工作流 3：特征分析与引导的直接链接")

### 分析单个特征[​](#分析单个特征 "分析单个特征的直接链接")

```
from transformer_lens import HookedTransformer  
from sae_lens import SAE  
import torch  
  
model = HookedTransformer.from_pretrained("gpt2-small", device="cuda")  
sae, _, _ = SAE.from_pretrained(  
    release="gpt2-small-res-jb",  
    sae_id="blocks.8.hook_resid_pre",  
    device="cuda"  
)  
  
# 找出激活特定特征的内容  
feature_idx = 1234  
test_texts = [  
    "The scientist conducted an experiment",  
    "I love chocolate cake",  
    "The code compiles successfully",  
    "Paris is beautiful in spring",  
]  
  
for text in test_texts:  
    tokens = model.to_tokens(text)  
    _, cache = model.run_with_cache(tokens)  
    features = sae.encode(cache["resid_pre", 8])  
    activation = features[0, :, feature_idx].max().item()  
    print(f"{activation:.3f}: {text}")
```

### 特征引导（Feature Steering）[​](#特征引导feature-steering "特征引导（Feature Steering）的直接链接")

```
def steer_with_feature(model, sae, prompt, feature_idx, strength=5.0):  
    """将 SAE 特征方向添加到残差流。"""  
    tokens = model.to_tokens(prompt)  
  
    # 从解码器获取特征方向  
    feature_direction = sae.W_dec[feature_idx]  # [d_model]  
  
    def steering_hook(activation, hook):  
        # 在所有位置添加缩放后的特征方向  
        activation += strength * feature_direction  
        return activation  
  
    # 带引导的生成  
    output = model.generate(  
        tokens,  
        max_new_tokens=50,  
        fwd_hooks=[("blocks.8.hook_resid_pre", steering_hook)]  
    )  
    return model.to_string(output[0])
```

### 特征归因（Feature Attribution）[​](#特征归因feature-attribution "特征归因（Feature Attribution）的直接链接")

```
# 哪些特征对特定输出影响最大？  
tokens = model.to_tokens("The capital of France is")  
_, cache = model.run_with_cache(tokens)  
  
# 获取最后位置的特征  
features = sae.encode(cache["resid_pre", 8])[0, -1]  # [d_sae]  
  
# 计算每个特征的 logit 归因  
# 特征贡献 = 特征激活 × 解码器权重 × 反嵌入  
W_dec = sae.W_dec  # [d_sae, d_model]  
W_U = model.W_U    # [d_model, vocab]  
  
# 对 "Paris" logit 的贡献  
paris_token = model.to_single_token(" Paris")  
feature_contributions = features * (W_dec @ W_U[:, paris_token])  
  
top_features = feature_contributions.topk(10)  
print("Top features for 'Paris' prediction:")  
for idx, val in zip(top_features.indices, top_features.values):  
    print(f"  Feature {idx.item()}: {val.item():.3f}")
```

## 常见问题与解决方案[​](#常见问题与解决方案 "常见问题与解决方案的直接链接")

### 问题：死亡特征比例过高[​](#问题死亡特征比例过高 "问题：死亡特征比例过高的直接链接")

```
# 错误：无预热，特征早期死亡  
cfg = LanguageModelSAERunnerConfig(  
    l1_coefficient=1e-4,  
    l1_warm_up_steps=0,  # 不推荐！  
)  
  
# 正确：预热 L1 惩罚  
cfg = LanguageModelSAERunnerConfig(  
    l1_coefficient=8e-5,  
    l1_warm_up_steps=1000,  # 逐步增加  
    use_ghost_grads=True,   # 复活死亡特征  
)
```

### 问题：重建效果差（CE 恢复率低）[​](#问题重建效果差ce-恢复率低 "问题：重建效果差（CE 恢复率低）的直接链接")

```
# 降低稀疏性惩罚  
cfg = LanguageModelSAERunnerConfig(  
    l1_coefficient=5e-5,  # 越低 = 重建越好  
    d_sae=768 * 16,       # 更大容量  
)
```

### 问题：特征不可解释[​](#问题特征不可解释 "问题：特征不可解释的直接链接")

```
# 提高稀疏性（更高的 L1）  
cfg = LanguageModelSAERunnerConfig(  
    l1_coefficient=1e-4,  # 越高 = 越稀疏，可解释性越强  
)  
# 或使用 TopK 架构  
cfg = LanguageModelSAERunnerConfig(  
    architecture="topk",  
    activation_fn_kwargs={"k": 50},  # 恰好 50 个激活特征  
)
```

### 问题：训练时内存错误[​](#问题训练时内存错误 "问题：训练时内存错误的直接链接")

```
cfg = LanguageModelSAERunnerConfig(  
    train_batch_size_tokens=2048,  # 减小批次大小  
    store_batch_size_prompts=4,    # 缓冲区中更少的 prompt  
    n_batches_in_buffer=8,         # 更小的激活缓冲区  
)
```

## 与 Neuronpedia 集成[​](#与-neuronpedia-集成 "与 Neuronpedia 集成的直接链接")

在 [neuronpedia.org](https://neuronpedia.org) 浏览预训练 SAE 特征：

```
# 特征通过 SAE ID 索引  
# 示例：gpt2-small 第 8 层特征 1234  
# → neuronpedia.org/gpt2-small/8-res-jb/1234
```

## 关键类参考[​](#关键类参考 "关键类参考的直接链接")

| 类 | 用途 |
| --- | --- |
| `SAE` | 稀疏自编码器模型 |
| `LanguageModelSAERunnerConfig` | 训练配置 |
| `SAETrainingRunner` | 训练循环管理器 |
| `ActivationsStore` | 激活收集与批处理 |
| `HookedSAETransformer` | TransformerLens + SAE 集成 |

## 参考文档[​](#参考文档 "参考文档的直接链接")

详细的 API 文档、教程和高级用法，请参阅 `references/` 文件夹：

| 文件 | 内容 |
| --- | --- |
| [references/README.md](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/saelens/references/README.md) | 概述与快速入门指南 |
| [references/api.md](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/saelens/references/api.md) | SAE、TrainingSAE、配置的完整 API 参考 |
| [references/tutorials.md](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/mlops/saelens/references/tutorials.md) | 训练、分析、引导的分步教程 |

## 外部资源[​](#外部资源 "外部资源的直接链接")

### 教程[​](#教程 "教程的直接链接")

* [基础加载与分析](https://github.com/jbloomAus/SAELens/blob/main/tutorials/basic_loading_and_analysing.ipynb)
* [训练稀疏自编码器](https://github.com/jbloomAus/SAELens/blob/main/tutorials/training_a_sparse_autoencoder.ipynb)
* [ARENA SAE 课程](https://www.lesswrong.com/posts/LnHowHgmrMbWtpkxx/intro-to-superposition-and-sparse-autoencoders-colab)

### 论文[​](#论文 "论文的直接链接")

* [Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features) — Anthropic（2023）
* [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/) — Anthropic（2024）
* [Sparse Autoencoders Find Highly Interpretable Features](https://arxiv.org/abs/2309.08600) — Cunningham et al.（ICLR 2024）

### 官方文档[​](#官方文档 "官方文档的直接链接")

* [SAELens 文档](https://jbloomaus.github.io/SAELens/)
* [Neuronpedia](https://neuronpedia.org) — 特征浏览器

## SAE 架构[​](#sae-架构 "SAE 架构的直接链接")

| 架构 | 描述 | 适用场景 |
| --- | --- | --- |
| **Standard** | ReLU + L1 惩罚 | 通用 |
| **Gated** | 学习门控机制 | 更好的稀疏性控制 |
| **TopK** | 恰好 K 个激活特征 | 一致的稀疏性 |

```
# TopK SAE（恰好 50 个特征激活）  
cfg = LanguageModelSAERunnerConfig(  
    architecture="topk",  
    activation_fn="topk",  
    activation_fn_kwargs={"k": 50},  
)
```

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [问题背景：多义性与叠加（Superposition）](#问题背景多义性与叠加superposition)
* [何时使用 SAELens](#何时使用-saelens)
* [安装](#安装)
* [核心概念](#核心概念)
  + [SAE 学到了什么](#sae-学到了什么)
  + [关键验证（Anthropic 研究）](#关键验证anthropic-研究)
* [工作流 1：加载和分析预训练 SAE](#工作流-1加载和分析预训练-sae)
  + [步骤说明](#步骤说明)
  + [可用预训练 SAE](#可用预训练-sae)
  + [检查清单](#检查清单)
* [工作流 2：训练自定义 SAE](#工作流-2训练自定义-sae)
  + [步骤说明](#步骤说明-1)
  + [关键超参数](#关键超参数)
  + [评估指标](#评估指标)
  + [检查清单](#检查清单-1)
* [工作流 3：特征分析与引导](#工作流-3特征分析与引导)
  + [分析单个特征](#分析单个特征)
  + [特征引导（Feature Steering）](#特征引导feature-steering)
  + [特征归因（Feature Attribution）](#特征归因feature-attribution)
* [常见问题与解决方案](#常见问题与解决方案)
  + [问题：死亡特征比例过高](#问题死亡特征比例过高)
  + [问题：重建效果差（CE 恢复率低）](#问题重建效果差ce-恢复率低)
  + [问题：特征不可解释](#问题特征不可解释)
  + [问题：训练时内存错误](#问题训练时内存错误)
* [与 Neuronpedia 集成](#与-neuronpedia-集成)
* [关键类参考](#关键类参考)
* [参考文档](#参考文档)
* [外部资源](#外部资源)
  + [教程](#教程)
  + [论文](#论文)
  + [官方文档](#官方文档)
* [SAE 架构](#sae-架构)