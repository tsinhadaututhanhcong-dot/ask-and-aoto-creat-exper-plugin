---
type: Reference
title: "Antigravity Browser"
description: "> Nguồn: Google Antigravity Master Corpus"
timestamp: 2026-07-06T03:34:16Z
---
# Antigravity Browser

> Nguồn: Google Antigravity Master Corpus
> Phân loại: concept
> Trạng thái: active
> Ngày tạo: 2026-06-21


*Source URL*: https://antigravity.google/docs/browser

Google Antigravity can open, read, and actuate a local Chrome browser, enabling you to test development websites, read documentation sources, and automate a variety of browser tasks.

---

## Core Mechanisms

Using the specialized [Browser Subagent](/docs/subagents), Antigravity operates on browser tabs as needed, capturing screenshots and saving action videos as interactive artifacts.

To completely disable browser tools, you can toggle the **Browser Tools** setting in the "Browser" section of the User Settings.

---

## Security: Allowlist & Denylist

The browser enforces a two-layer security model to control URL access:

1. **Denylist**: Real-time check against Google's server-side database to block known dangerous or malicious hostnames.
2. **Allowlist**: A customizable local text file initialized with `localhost`. If the agent tries to open a non-allowlisted page, a dialog will prompt you to approve and add the domain to your trusted allowlist.

---

## Isolated Profile

To protect your personal data, the agent executes inside a completely separate, isolated Chrome profile:

* **Cookie Isolation**: Does not share cookies, history, or active sessions from your primary Google Chrome profile.
* **Persistence**: All credentials and cookies entered in the agentic browser profile remain persisted across sessions.
* **Dock Isolation**: Renders as a separate application icon in your macOS dock when your primary browser is open.



---