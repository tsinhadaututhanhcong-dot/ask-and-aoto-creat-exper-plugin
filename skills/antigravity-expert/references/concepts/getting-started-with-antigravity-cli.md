---
type: Reference
title: "Getting Started with Antigravity CLI"
description: "> Nguồn: Google Antigravity Master Corpus"
timestamp: 2026-07-06T03:34:16Z
---
# Getting Started with Antigravity CLI

> Nguồn: Google Antigravity Master Corpus
> Phân loại: concept
> Trạng thái: active
> Ngày tạo: 2026-06-21


*Source URL*: https://antigravity.google/docs/cli-getting-started

### Installation

**Mac/Linux:**

content\_copy

```
            curl -fsSL https://antigravity.google/cli/install.sh | bash
```

**Windows PowerShell:**

content\_copy

```
            irm https://antigravity.google/cli/install.ps1 | iex
```

**Windows CMD:**

content\_copy

```
            curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### Authentication

Antigravity CLI attempts to authenticate you silently using your operating system's secure keyring. If no saved session is found, it will fall back to a browser-based Google Sign-In.

* **Local Machine**: The CLI will automatically open your default browser to the Google Sign-In page.
* **Remote / SSH Session**: The CLI will detect that you are in an SSH session and print a secure authorization URL. Copy this URL into your local browser to sign in, and then paste the resulting authorization code back into the CLI prompt.
* **Logging Out**: To terminate your session and remove saved credentials, run the command `/logout`.

To login with your enterprise credentials, connect your GCP project as you onboard. For more information, visit the [Enterprise Documentation Page](/docs/enterprise).



---