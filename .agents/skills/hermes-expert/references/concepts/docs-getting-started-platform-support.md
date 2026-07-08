# Platform Support | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/getting-started/platform-support](https://hermes-agent.nousresearch.com/docs/getting-started/platform-support)

On this page

Hermes Agent maintains support for many platforms and distribution methods, but we can't support every possible install method.

---

## Tier 1[​](#tier-1 "Direct link to Tier 1")

We strive to never break installations and updates for these. Issues & regressions in Tier 1 are our first priority and take precedence over other platforms.

| OS / Architecture | Installation methods | Notes |
| --- | --- | --- |
| **macOS** (Apple Silicon) | [Hermes Desktop](https://hermes-agent.nousresearch.com/), [`install.sh`](/docs/getting-started/installation#linux--macos--wsl2--android-termux) |  |
| [**Windows 10 / 11**](/docs/user-guide/windows-native) (x86\_64, aarch64) | [Hermes Desktop](https://hermes-agent.nousresearch.com/), [`install.ps1`](/docs/getting-started/installation#windows-native) | A few features are [not available](/docs/user-guide/windows-native#feature-matrix). |
| **Linux / [WSL2](/docs/user-guide/windows-wsl-quickstart)** (x86\_64, aarch64) | [`install.sh`](/docs/getting-started/installation#linux--macos--wsl2--android-termux) | We test on the latest Ubuntu and WSL2. If your distro has glibc, systemd, and follows the Filesystem Hierarchy Standard, it's likely to work pretty well. |
| [**Docker Container**](/docs/user-guide/docker#quick-start) (x86\_64, aarch64) | [`docker pull`](/docs/user-guide/docker#quick-start) | Docker installs do not support `hermes update`. Updating is done by running a new image. |

---

## Tier 2[​](#tier-2 "Direct link to Tier 2")

These platforms are maintained in-tree only as a best effort.
Releases may break them, and we can't promise we'll fix them promptly when they break.

PRs will be accepted to fix issues with them, but they will take precedence below fixing issues with Tier 1 platforms.

| OS / Architecture | Installation methods | Notes |
| --- | --- | --- |
| **Android (Termux)** (aarch64) | [`install.sh`](/docs/getting-started/installation#linux--macos--wsl2--android-termux) | A few features are [not available](/docs/getting-started/termux#known-limitations-on-phones). |
| **Nix** (MacOS, Linux, NixOS) | [`install.sh`](/docs/getting-started/nix-setup) | Breaks often due to node.js packaging woes. Best of luck~! <3 |

## Unsupported[​](#unsupported "Direct link to Unsupported")

These platforms and distribution methods are **not** supported.
We suggest that you migrate to a supported distribution method or platform.
They may be broken right now, they may break more in the future.
PRs to fix them will *not* be accepted, and any code that keeps compatibility with them may be removed at any point.

* installs via the AUR (we might upstream patches if it helps out <3)
* macOS on x86 (Intel) processors
* installs via `pypi` (e.g. `uv tool install hermes-agent`, `pip install hermse-agent`, etc.)
* installs via `brew` (`brew install hermes-agent`)

If you are using an unsupported distribution method, please read the [the installation guide](/docs/getting-started/installation) to learn how to switch to a supported one.

* [Tier 1](#tier-1)
* [Tier 2](#tier-2)
* [Unsupported](#unsupported)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/](./index.md)
- [https://hermes-agent.nousresearch.com/docs/getting-started/installation](./docs-getting-started-installation.md)
- [https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup](./docs-getting-started-nix-setup.md)
- [https://hermes-agent.nousresearch.com/docs/getting-started/termux](./docs-getting-started-termux.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/docker](./docs-user-guide-docker.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/windows-native](./docs-user-guide-windows-native.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/windows-wsl-quickstart](./docs-user-guide-windows-wsl-quickstart.md)
