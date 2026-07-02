# FAQ - MinerU
**Source:** [https://opendatalab.github.io/MinerU/faq/](https://opendatalab.github.io/MinerU/faq/)

# Frequently Asked Questions

If your question is not listed, try using [DeepWiki](https://deepwiki.com/opendatalab/MinerU)'s AI assistant for common issues.

For unresolved problems, join our [Discord](https://discord.gg/Tdedn9GTXq) or [WeChat](https://mineru.net/community-portal/?aliasId=3c430f94) community for support.

What should I do if inference is slow after installing directly on Windows?

### What should I do if inference is slow after installing directly on Windows?

If inference is slow after a direct Windows installation, CUDA acceleration dependencies are usually not installed correctly. Choose the solution based on your GPU architecture:

* Volta / Turing / Ampere / Ada Lovelace GPUs, such as V100, 20 series, T4, 30 series, and 40 series: install CUDA-enabled `torch` and `torchvision` directly. Go to the [PyTorch official website](https://pytorch.org/get-started/locally/) and select the Windows installation command that matches your CUDA version.
* Blackwell GPUs, such as the RTX 50xx series: install the `lmdeploy 0.11.1 + cu128` Windows wheel. Set `PYTHON_VERSION` to your current Python version, for example `310` / `311` / `312` / `313` for Python 3.10 / 3.11 / 3.12 / 3.13.

```
$env:LMDEPLOY_VERSION = "0.11.1"
$env:PYTHON_VERSION = "312"

$wheel = "https://github.com/InternLM/lmdeploy/releases/download/v$($env:LMDEPLOY_VERSION)/lmdeploy-$($env:LMDEPLOY_VERSION)+cu128-cp$($env:PYTHON_VERSION)-cp$($env:PYTHON_VERSION)-win_amd64.whl"
pip install $wheel --extra-index-url https://download.pytorch.org/whl/cu128
```

If you are using a Blackwell GPU and have already installed the cu128 version of `torch`, define `$wheel` first and then run the following command to avoid downloading a lower-version `torch` again:

```
pip install $wheel --no-dependencies
```


Encountered the error `ImportError: libGL.so.1: cannot open shared object file: No such file or directory` in Ubuntu 22.04 on WSL2

### Encountered the error `ImportError: libGL.so.1: cannot open shared object file: No such file or directory` in Ubuntu 22.04 on WSL2

The `libgl` library is missing in Ubuntu 22.04 on WSL2. You can install the `libgl` library with the following command to resolve the issue:

```
sudo apt-get install libgl1-mesa-glx
```

Reference: [#388](https://github.com/opendatalab/MinerU/issues/388)


Missing text information in parsing results when installing and using on Linux systems.

### Missing text information in parsing results when installing and using on Linux systems.

MinerU uses `pypdfium2` instead of `pymupdf` as the PDF page rendering engine in versions >=2.0 to resolve AGPLv3 license issues. On some Linux distributions, due to missing CJK fonts, some text may be lost during the process of rendering PDFs to images.
To solve this problem, you can install the noto font package with the following commands, which are effective on Ubuntu/Debian systems:

```
sudo apt update
sudo apt install fonts-noto-core
sudo apt install fonts-noto-cjk
fc-cache -fv
```

You can also directly use our [Docker deployment](../quick_start/docker_deployment/) method to build the image, which includes the above font packages by default.

Reference: [#2915](https://github.com/opendatalab/MinerU/issues/2915)

Back to top

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://opendatalab.github.io/MinerU/quick_start/docker_deployment/](./MinerU-quickstart-dockerdeployment.md)
