# Ocr And Documents — 从 PDF/扫描件中提取文本（pymupdf、marker-pdf） | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-ocr-and-documents](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-ocr-and-documents)

本页总览

从 PDF/扫描件中提取文本（pymupdf、marker-pdf）。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/productivity/ocr-and-documents` |
| 版本 | `2.3.0` |
| 作者 | Hermes Agent |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `PDF`, `Documents`, `Research`, `Arxiv`, `Text-Extraction`, `OCR` |
| 相关 skill | [`powerpoint`](/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-powerpoint) |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# PDF 与文档提取

对于 DOCX：使用 `python-docx`（解析实际文档结构，远优于 OCR）。
对于 PPTX：参见 `powerpoint` skill（使用 `python-pptx`，完整支持幻灯片/备注）。
本 skill 涵盖 **PDF 及扫描文档**。

## 第一步：是否有远程 URL？[​](#第一步是否有远程-url "第一步：是否有远程 URL？的直接链接")

如果文档有 URL，**始终优先尝试 `web_extract`**：

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])  
web_extract(urls=["https://example.com/report.pdf"])
```

这通过 Firecrawl 实现 PDF 转 Markdown，无需本地依赖。

仅在以下情况使用本地提取：文件在本地、`web_extract` 失败，或需要批量处理。

## 第二步：选择本地提取器[​](#第二步选择本地提取器 "第二步：选择本地提取器的直接链接")

| 功能 | pymupdf（约 25MB） | marker-pdf（约 3-5GB） |
| --- | --- | --- |
| **基于文本的 PDF** | ✅ | ✅ |
| **扫描 PDF（OCR）** | ❌ | ✅（支持 90+ 种语言） |
| **表格** | ✅（基础） | ✅（高精度） |
| **公式 / LaTeX** | ❌ | ✅ |
| **代码块** | ❌ | ✅ |
| **表单** | ❌ | ✅ |
| **页眉/页脚去除** | ❌ | ✅ |
| **阅读顺序检测** | ❌ | ✅ |
| **图片提取** | ✅（嵌入图片） | ✅（含上下文） |
| **图片 → 文本（OCR）** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown 输出** | ✅（通过 pymupdf4llm） | ✅（原生，质量更高） |
| **安装体积** | 约 25MB | 约 3-5GB（PyTorch + 模型） |
| **速度** | 即时 | 约 1-14 秒/页（CPU），约 0.2 秒/页（GPU） |

**决策原则**：除非需要 OCR、公式、表单或复杂版面分析，否则使用 pymupdf。

如果用户需要 marker-pdf 的功能但系统磁盘空间不足约 5GB：

> "此文档需要 OCR/高级提取（marker-pdf），这需要约 5GB 用于 PyTorch 和模型。您的系统剩余 [X]GB 可用空间。可选方案：释放磁盘空间、提供 URL 以使用 web\_extract，或我可以尝试 pymupdf——它适用于基于文本的 PDF，但不支持扫描文档或公式。"

---

## pymupdf（轻量级）[​](#pymupdf轻量级 "pymupdf（轻量级）的直接链接")

```
pip install pymupdf pymupdf4llm
```

**通过辅助脚本**：

```
python scripts/extract_pymupdf.py document.pdf              # 纯文本  
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown  
python scripts/extract_pymupdf.py document.pdf --tables      # 表格  
python scripts/extract_pymupdf.py document.pdf --images out/ # 提取图片  
python scripts/extract_pymupdf.py document.pdf --metadata    # 标题、作者、页数  
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # 指定页面
```

**内联方式**：

```
python3 -c "  
import pymupdf  
doc = pymupdf.open('document.pdf')  
for page in doc:  
    print(page.get_text())  
"
```

---

## marker-pdf（高质量 OCR）[​](#marker-pdf高质量-ocr "marker-pdf（高质量 OCR）的直接链接")

```
# 先检查磁盘空间  
python scripts/extract_marker.py --check  
  
pip install marker-pdf
```

**通过辅助脚本**：

```
python scripts/extract_marker.py document.pdf                # Markdown  
python scripts/extract_marker.py document.pdf --json         # 含元数据的 JSON  
python scripts/extract_marker.py document.pdf --output_dir out/  # 保存图片  
python scripts/extract_marker.py scanned.pdf                 # 扫描 PDF（OCR）  
python scripts/extract_marker.py document.pdf --use_llm      # LLM 增强精度
```

**CLI**（随 marker-pdf 一同安装）：

```
marker_single document.pdf --output_dir ./output  
marker /path/to/folder --workers 4    # 批量处理
```

---

## Arxiv 论文[​](#arxiv-论文 "Arxiv 论文的直接链接")

```
# 仅摘要（快速）  
web_extract(urls=["https://arxiv.org/abs/2402.03300"])  
  
# 完整论文  
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])  
  
# 搜索  
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## 拆分、合并与搜索[​](#拆分合并与搜索 "拆分、合并与搜索的直接链接")

pymupdf 原生支持这些操作——使用 `execute_code` 或内联 Python：

```
# 拆分：将第 1-5 页提取为新 PDF  
import pymupdf  
doc = pymupdf.open("report.pdf")  
new = pymupdf.open()  
for i in range(5):  
    new.insert_pdf(doc, from_page=i, to_page=i)  
new.save("pages_1-5.pdf")
```

```
# 合并多个 PDF  
import pymupdf  
result = pymupdf.open()  
for path in ["a.pdf", "b.pdf", "c.pdf"]:  
    result.insert_pdf(pymupdf.open(path))  
result.save("merged.pdf")
```

```
# 在所有页面中搜索文本  
import pymupdf  
doc = pymupdf.open("report.pdf")  
for i, page in enumerate(doc):  
    results = page.search_for("revenue")  
    if results:  
        print(f"Page {i+1}: {len(results)} match(es)")  
        print(page.get_text("text"))
```

无需额外依赖——pymupdf 在一个包内涵盖拆分、合并、搜索和文本提取。

---

## 注意事项[​](#注意事项 "注意事项的直接链接")

* `web_extract` 始终是 URL 的首选方案
* pymupdf 是安全的默认选择——即时可用，无需模型，适用于所有环境
* marker-pdf 用于 OCR、扫描文档、公式、复杂版面——仅在需要时安装
* 两个辅助脚本均支持 `--help` 查看完整用法
* marker-pdf 首次使用时会将约 2.5GB 的模型下载至 `~/.cache/huggingface/`
* 对于 Word 文档：`pip install python-docx`（优于 OCR——解析实际文档结构）
* 对于 PowerPoint：参见 `powerpoint` skill（使用 python-pptx）

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [第一步：是否有远程 URL？](#第一步是否有远程-url)
* [第二步：选择本地提取器](#第二步选择本地提取器)
* [pymupdf（轻量级）](#pymupdf轻量级)
* [marker-pdf（高质量 OCR）](#marker-pdf高质量-ocr)
* [Arxiv 论文](#arxiv-论文)
* [拆分、合并与搜索](#拆分合并与搜索)
* [注意事项](#注意事项)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-powerpoint](./docs-zh-Hans-user-guide-skills-bundled-productivity-productivity-powerpoint.md)
