# 使用指南 - MinerU
**Source:** [https://opendatalab.github.io/MinerU/zh/usage/](https://opendatalab.github.io/MinerU/zh/usage/)

# 使用指南

本章节提供了项目的完整使用说明。我们将通过以下几个部分，帮助您从基础到进阶逐步掌握项目的使用方法：

## 目录

* 本地部署
  + [基础使用](quick_usage/) - 快速上手和基本使用
  + [模型源配置](model_source/) - 模型源的详细配置说明
  + [命令行工具](cli_tools/) - 命令行工具的详细参数说明
  + [命令行进阶参数](advanced_cli_parameters/) - 一些适配命令行工具的进阶参数说明
* 其他加速卡适配（🚀官方支持/❤️社区贡献）
  + [昇腾 Ascend](acceleration_cards/Ascend/) 🚀
  + [平头哥 T-Head](acceleration_cards/THead/) 🚀
  + [沐曦 METAX](acceleration_cards/METAX/) 🚀
  + [海光 Hygon](acceleration_cards/Hygon/) 🚀
  + [燧原 Enflame](acceleration_cards/Enflame/) 🚀
  + [摩尔线程 MooreThreads](acceleration_cards/MooreThreads/) 🚀
  + [天数智芯 IluvatarCorex](acceleration_cards/IluvatarCorex/) 🚀
  + [寒武纪 Cambricon](acceleration_cards/Cambricon/) 🚀
  + [昆仑芯 Kunlunxin](acceleration_cards/Kunlunxin/) 🚀
  + [太初元碁 Tecorigin](acceleration_cards/Tecorigin/) ❤️
  + [壁仞 Biren](acceleration_cards/Biren/) ❤️
  + [AMD #3662](https://github.com/opendatalab/MinerU/discussions/3662) ❤️
  + [瀚博 VastAI #4237](https://github.com/opendatalab/MinerU/discussions/4237) ❤️
* 插件与生态
  + [Cherry Studio](plugin/Cherry_Studio/)
  + [Sider](plugin/Sider/)
  + [Dify](plugin/Dify/)
  + [n8n](plugin/n8n/)
  + [Coze](plugin/Coze/)
  + [FastGPT](plugin/FastGPT/)
  + [ModelWhale](plugin/ModelWhale/)
  + [DingTalk](plugin/DingTalk/)
  + [DataFlow](plugin/DataFlow/)
  + [BISHENG](plugin/BISHENG/)
  + [RagFlow](plugin/RagFlow/)

## 开始使用

自 3.0 起，`mineru` 默认作为基于 `mineru-api` 的编排客户端运行；`mineru-router` 的多服务、多 GPU 用法也会在本章的基础使用与命令行工具章节中说明。

建议按照上述顺序阅读文档，这样可以帮助您更好地理解和使用项目功能。

如果您在使用过程中遇到问题，请查看 [FAQ](../faq/)

回到页面顶部

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/zh/faq/](./MinerU-zh-faq.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Ascend/](./MinerU-zh-usage-accelerationcards-Ascend.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Biren/](./MinerU-zh-usage-accelerationcards-Biren.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Cambricon/](./MinerU-zh-usage-accelerationcards-Cambricon.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Enflame/](./MinerU-zh-usage-accelerationcards-Enflame.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Hygon/](./MinerU-zh-usage-accelerationcards-Hygon.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/IluvatarCorex/](./MinerU-zh-usage-accelerationcards-IluvatarCorex.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Kunlunxin/](./MinerU-zh-usage-accelerationcards-Kunlunxin.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/METAX/](./MinerU-zh-usage-accelerationcards-METAX.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/MooreThreads/](./MinerU-zh-usage-accelerationcards-MooreThreads.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/THead/](./MinerU-zh-usage-accelerationcards-THead.md)
- [https://opendatalab.github.io/MinerU/zh/usage/acceleration_cards/Tecorigin/](./MinerU-zh-usage-accelerationcards-Tecorigin.md)
- [https://opendatalab.github.io/MinerU/zh/usage/advanced_cli_parameters/](./MinerU-zh-usage-advancedcliparameters.md)
- [https://opendatalab.github.io/MinerU/zh/usage/cli_tools/](./MinerU-zh-usage-clitools.md)
- [https://opendatalab.github.io/MinerU/zh/usage/model_source/](./MinerU-zh-usage-modelsource.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/BISHENG/](./MinerU-zh-usage-plugin-BISHENG.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/Cherry_Studio/](./MinerU-zh-usage-plugin-CherryStudio.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/Coze/](./MinerU-zh-usage-plugin-Coze.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/DataFlow/](./MinerU-zh-usage-plugin-DataFlow.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/Dify/](./MinerU-zh-usage-plugin-Dify.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/DingTalk/](./MinerU-zh-usage-plugin-DingTalk.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/FastGPT/](./MinerU-zh-usage-plugin-FastGPT.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/ModelWhale/](./MinerU-zh-usage-plugin-ModelWhale.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/RagFlow/](./MinerU-zh-usage-plugin-RagFlow.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/Sider/](./MinerU-zh-usage-plugin-Sider.md)
- [https://opendatalab.github.io/MinerU/zh/usage/plugin/n8n/](./MinerU-zh-usage-plugin-n8n.md)
- [https://opendatalab.github.io/MinerU/zh/usage/quick_usage/](./MinerU-zh-usage-quickusage.md)
