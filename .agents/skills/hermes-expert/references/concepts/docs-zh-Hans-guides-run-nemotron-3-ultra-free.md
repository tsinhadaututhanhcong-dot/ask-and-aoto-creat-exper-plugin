# Run Nemotron 3 Ultra free in Hermes Agent | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/run-nemotron-3-ultra-free](https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/run-nemotron-3-ultra-free)

本页总览

Nous Research has been inducted into the **Nemotron Coalition** of leading AI labs working with **NVIDIA** to advance open frontier foundation models. In honor of this, we've partnered with **Nebius** to provide **Nemotron 3 Ultra** free on [Nous Portal](https://portal.nousresearch.com) for two weeks (**June 4th – June 18th**). Follow the instructions below to try the model in your Hermes Agent today.

Limited-time offer

The `nvidia/nemotron-3-ultra:free` tier is available from **June 4th to June 18th**. The `:free` tag is what keeps it on the no-cost plan — pick that exact variant.

Pick whichever install fits you. The **desktop app** is the easiest — no terminal required. If you live in a terminal, the **command-line** install is right below it.

## Option A — Desktop app (recommended)[​](#option-a--desktop-app-recommended "Option A — Desktop app (recommended)的直接链接")

The simplest path: a one-click installer with a guided, point-and-click setup. No terminal needed.

### 1. Download and install[​](#1-download-and-install "1. Download and install的直接链接")

[Download the Hermes Desktop installer](https://hermes-agent.nousresearch.com/) for macOS or Windows, then open it. On first launch it finishes setting itself up (usually under a minute).

### 2. Connect Nous Portal[​](#2-connect-nous-portal "2. Connect Nous Portal的直接链接")

When the app opens, you'll see a "Let's get you set up" screen. Click **Nous Portal** (marked **Recommended**). Your browser opens — create a [Nous Portal](https://portal.nousresearch.com) account (or sign in), choose the **Free** plan, and authorize Hermes. The app connects automatically.

### 3. Pick the free Nemotron 3 Ultra model[​](#3-pick-the-free-nemotron-3-ultra-model "3. Pick the free Nemotron 3 Ultra model的直接链接")

After connecting, the app shows a **Default model** card. Click **Change**, search for **nemotron 3 ultra**, and select the variant tagged **Free tier**:

```
nvidia/nemotron-3-ultra:free
```

The `:free` tag is what keeps it on the no-cost tier — pick that variant.

### 4. Start chatting[​](#4-start-chatting "4. Start chatting的直接链接")

Click **Start chatting**. That's it — you're talking to Nemotron 3 Ultra, free.

## Option B — Command line[​](#option-b--command-line "Option B — Command line的直接链接")

Prefer the terminal?

### 1. Install Hermes Agent[​](#1-install-hermes-agent "1. Install Hermes Agent的直接链接")

On macOS/Linux/WSL2/Android, run

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

On Windows, run

```
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Prefer to review first? Download [`install.sh`](https://hermes-agent.nousresearch.com/install.sh), inspect it, then run it.

After it finishes, reload your shell:

```
source ~/.bashrc   # or source ~/.zshrc
```

### 2. Run Quick Setup[​](#2-run-quick-setup "2. Run Quick Setup的直接链接")

```
hermes setup
```

Select **Quick Setup**. Hermes opens a browser tab and waits for you to finish the next steps.

### 3. Create a Nous Portal account[​](#3-create-a-nous-portal-account "3. Create a Nous Portal account的直接链接")

In the browser, create a [Nous Portal](https://portal.nousresearch.com) account (or sign in) and choose the **Free** plan.

### 4. Connect your account[​](#4-connect-your-account "4. Connect your account的直接链接")

When prompted to connect your account to Hermes Agent, click **Connect**. You'll see a confirmation once it's linked.

### 5. Select the free Nemotron 3 Ultra model[​](#5-select-the-free-nemotron-3-ultra-model "5. Select the free Nemotron 3 Ultra model的直接链接")

Return to your terminal. From the model list, select:

```
nvidia/nemotron-3-ultra:free
```

The `:free` tag is what keeps it on the no-cost tier, so make sure you pick that variant.

### 6. Start chatting[​](#6-start-chatting "6. Start chatting的直接链接")

Complete the remaining Quick Setup prompts, then run:

```
hermes
```

That's it — you're talking to Nemotron 3 Ultra, free.

## Switching to it later[​](#switching-to-it-later "Switching to it later的直接链接")

Already set up with another model?

* **Desktop app:** open the model picker, search for **nemotron 3 ultra**, and select the **Free tier** variant.
* **CLI / TUI:** switch any time from inside a session with `/model nvidia/nemotron-3-ultra:free`, or run `/model` to open the picker and choose it from the list.

## Troubleshooting[​](#troubleshooting "Troubleshooting的直接链接")

* **Don't see the model in the list?** Make sure you finished the Nous Portal connection and that you're on the **Free** plan. In the CLI, `hermes portal info` confirms you're logged in and routing through Nous.
* **Picked the wrong variant?** Re-select `nvidia/nemotron-3-ultra:free` — the `:free` suffix is required to stay on the no-cost tier.
* **Browser didn't open / you're on a remote host (CLI)?** See [OAuth over SSH / Remote Hosts](/docs/zh-Hans/guides/oauth-over-ssh) for port-forwarding workarounds.

## See also[​](#see-also "See also的直接链接")

* **[Desktop App](/docs/zh-Hans/user-guide/desktop)** — The native one-click app (macOS, Windows, Linux)
* **[Run Hermes Agent with Nous Portal](/docs/zh-Hans/guides/run-hermes-with-nous-portal)** — Full Portal walkthrough: models, Tool Gateway, and verification
* **[Nous Portal integration](/docs/zh-Hans/integrations/nous-portal)** — What's in the subscription
* **[Quickstart](/docs/zh-Hans/getting-started/quickstart)** — Install-to-chat in under 5 minutes

* [Option A — Desktop app (recommended)](#option-a--desktop-app-recommended)
  + [1. Download and install](#1-download-and-install)
  + [2. Connect Nous Portal](#2-connect-nous-portal)
  + [3. Pick the free Nemotron 3 Ultra model](#3-pick-the-free-nemotron-3-ultra-model)
  + [4. Start chatting](#4-start-chatting)
* [Option B — Command line](#option-b--command-line)
  + [1. Install Hermes Agent](#1-install-hermes-agent)
  + [2. Run Quick Setup](#2-run-quick-setup)
  + [3. Create a Nous Portal account](#3-create-a-nous-portal-account)
  + [4. Connect your account](#4-connect-your-account)
  + [5. Select the free Nemotron 3 Ultra model](#5-select-the-free-nemotron-3-ultra-model)
  + [6. Start chatting](#6-start-chatting)
* [Switching to it later](#switching-to-it-later)
* [Troubleshooting](#troubleshooting)
* [See also](#see-also)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/](./index.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/getting-started/quickstart](./docs-zh-Hans-getting-started-quickstart.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/oauth-over-ssh](./docs-zh-Hans-guides-oauth-over-ssh.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/guides/run-hermes-with-nous-portal](./docs-zh-Hans-guides-run-hermes-with-nous-portal.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/integrations/nous-portal](./docs-zh-Hans-integrations-nous-portal.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/desktop](./docs-zh-Hans-user-guide-desktop.md)
