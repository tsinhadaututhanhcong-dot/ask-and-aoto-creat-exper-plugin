---
title: Browser Integration
date_created: 2026-07-01
source_url: https://antigravity.google/docs/ide/browser
description: Chrome driver setup for interactive web testing.
tags: [concept, llms-txt, js-rendered]
platform: ide
---

* side\_navigation
* Antigravity IDE
>* Browser
>* Overview

# Browser Overview[link](#browser-overview)

Google Antigravity can open, read, and actuate a local Chrome browser, enabling you to test development websites, read documentation sources, and automate a variety of browser tasks.

---

## Core Mechanisms[link](#core-mechanisms)

Using the specialized [Browser Subagent](/docs/subagents), Antigravity operates on browser tabs as needed, capturing screenshots and saving action videos as interactive artifacts.

To completely disable browser tools, you can toggle the **Browser Tools** setting in the "Browser" section of the User Settings.

---

## Deep Dive[link](#deep-dive)

Explore the key security and privacy features of Antigravity's browser integration:

security

Allowlist & Denylist keyboard\_arrow\_right

Learn about the two-layer security model (Denylist and Allowlist) used to control URL access.account\_box

Isolated Profile keyboard\_arrow\_right

Understand how the agent executes inside a completely separate Chrome profile to protect your personal data.

On this Page