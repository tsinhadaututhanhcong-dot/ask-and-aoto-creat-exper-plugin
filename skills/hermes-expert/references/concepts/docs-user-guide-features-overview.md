# Features Overview | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/user-guide/features/overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview)

On this page

Hermes Agent includes a rich set of capabilities that extend far beyond basic chat. From persistent memory and file-aware context to browser automation and voice conversations, these features work together to make Hermes a powerful autonomous assistant.

Don't know where to start?

`hermes setup --portal` covers a model provider plus all four Tool Gateway tools (web search, image generation, TTS, browser) in one command. See [Nous Portal](/docs/integrations/nous-portal).

## Core[​](#core "Direct link to Core")

* **[Tools & Toolsets](/docs/user-guide/features/tools)** — Tools are functions that extend the agent's capabilities. They're organized into logical toolsets that can be enabled or disabled per platform, covering web search, terminal execution, file editing, memory, delegation, and more.
* **[Skills System](/docs/user-guide/features/skills)** — On-demand knowledge documents the agent can load when needed. Skills follow a progressive disclosure pattern to minimize token usage and are compatible with the [agentskills.io](https://agentskills.io/specification) open standard.
* **[Persistent Memory](/docs/user-guide/features/memory)** — Bounded, curated memory that persists across sessions. Hermes remembers your preferences, projects, environment, and things it has learned via `MEMORY.md` and `USER.md`.
* **[Context Files](/docs/user-guide/features/context-files)** — Hermes automatically discovers and loads project context files (`.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `.cursorrules`) that shape how it behaves in your project.
* **[Context References](/docs/user-guide/features/context-references)** — Type `@` followed by a reference to inject files, folders, git diffs, and URLs directly into your messages. Hermes expands the reference inline and appends the content automatically.
* **[Checkpoints](/docs/user-guide/checkpoints-and-rollback)** — Hermes automatically snapshots your working directory before making file changes, giving you a safety net to roll back with `/rollback` if something goes wrong.

## Automation[​](#automation "Direct link to Automation")

* **[Scheduled Tasks (Cron)](/docs/user-guide/features/cron)** — Schedule tasks to run automatically with natural language or cron expressions. Jobs can attach skills, deliver results to any platform, and support pause/resume/edit operations.
* **[Subagent Delegation](/docs/user-guide/features/delegation)** — The `delegate_task` tool spawns child agent instances with isolated context, restricted toolsets, and their own terminal sessions. Run 3 concurrent subagents by default (configurable) for parallel workstreams.
* **[Code Execution](/docs/user-guide/features/code-execution)** — The `execute_code` tool lets the agent write Python scripts that call Hermes tools programmatically, collapsing multi-step workflows into a single LLM turn via sandboxed RPC execution.
* **[Event Hooks](/docs/user-guide/features/hooks)** — Run custom code at key lifecycle points. Gateway hooks handle logging, alerts, and webhooks; plugin hooks handle tool interception, metrics, and guardrails.
* **[Batch Processing](/docs/user-guide/features/batch-processing)** — Run the Hermes agent across hundreds or thousands of prompts in parallel, generating structured ShareGPT-format trajectory data for training data generation or evaluation.

## Media & Web[​](#media--web "Direct link to Media & Web")

* **[Voice Mode](/docs/user-guide/features/voice-mode)** — Full voice interaction across CLI and messaging platforms. Talk to the agent using your microphone, hear spoken replies, and have live voice conversations in Discord voice channels.
* **[Browser Automation](/docs/user-guide/features/browser)** — Full browser automation with multiple backends: Browserbase cloud, Browser Use cloud, local Chrome/Brave/Chromium/Edge via CDP, or local Chromium. Navigate websites, fill forms, and extract information.
* **[Vision & Image Paste](/docs/user-guide/features/vision)** — Multimodal vision support. Paste images from your clipboard into the CLI and ask the agent to analyze, describe, or work with them using any vision-capable model.
* **[Image Generation](/docs/user-guide/features/image-generation)** — Generate images from text prompts using FAL.ai. Nine models supported (FLUX 2 Klein/Pro, GPT-Image 1.5/2, Nano Banana Pro, Ideogram V3, Recraft V4 Pro, Qwen, Z-Image Turbo); pick one via `hermes tools`.
* **[Voice & TTS](/docs/user-guide/features/tts)** — Text-to-speech output and voice message transcription across all messaging platforms, with ten native provider options: Edge TTS (free), ElevenLabs, OpenAI TTS, MiniMax, Mistral Voxtral, Google Gemini, xAI, NeuTTS, KittenTTS, and Piper — plus custom command providers for any local TTS CLI.

## Integrations[​](#integrations "Direct link to Integrations")

* **[MCP Integration](/docs/user-guide/features/mcp)** — Connect to any MCP server via stdio or HTTP transport. Access external tools from GitHub, databases, file systems, and internal APIs without writing native Hermes tools. Includes per-server tool filtering and sampling support.
* **[Provider Routing](/docs/user-guide/features/provider-routing)** — Fine-grained control over which AI providers handle your requests. Optimize for cost, speed, or quality with sorting, whitelists, blacklists, and priority ordering.
* **[Fallback Providers](/docs/user-guide/features/fallback-providers)** — Automatic failover to backup LLM providers when your primary model encounters errors, including independent fallback for auxiliary tasks like vision and compression.
* **[Credential Pools](/docs/user-guide/features/credential-pools)** — Distribute API calls across multiple keys for the same provider. Automatic rotation on rate limits or failures.
* **[Prompt caching](/docs/user-guide/configuration#prompt-caching)** — Built-in cross-session 1-hour prefix cache for Claude on native Anthropic, OpenRouter, and Nous Portal. Always-on; no configuration required.
* **[Memory Providers](/docs/user-guide/features/memory-providers)** — Plug in external memory backends (Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory) for cross-session user modeling and personalization beyond the built-in memory system.
* **[API Server](/docs/user-guide/features/api-server)** — Expose Hermes as an OpenAI-compatible HTTP endpoint. Connect any frontend that speaks the OpenAI format — Open WebUI, LobeChat, LibreChat, and more.
* **[IDE Integration (ACP)](/docs/user-guide/features/acp)** — Use Hermes inside ACP-compatible editors such as VS Code, Zed, and JetBrains. Chat, tool activity, file diffs, and terminal commands render inside your editor.
* **[Batch Processing](/docs/user-guide/features/batch-processing)** — Run the agent over many prompts or tasks in parallel from the CLI, with structured outputs and trajectory capture suitable for evals or downstream training pipelines.

## Customization[​](#customization "Direct link to Customization")

* **[Personality & SOUL.md](/docs/user-guide/features/personality)** — Fully customizable agent personality. `SOUL.md` is the primary identity file — the first thing in the system prompt — and you can swap in built-in or custom `/personality` presets per session.
* **[Skins & Themes](/docs/user-guide/features/skins)** — Customize the CLI's visual presentation: banner colors, spinner faces and verbs, response-box labels, branding text, and the tool activity prefix.
* **[Plugins](/docs/user-guide/features/plugins)** — Add custom tools, hooks, and integrations without modifying core code. Three plugin types: general plugins (tools/hooks), memory providers (cross-session knowledge), and context engines (alternative context management). Managed via the unified `hermes plugins` interactive UI.

* [Core](#core)
* [Automation](#automation)
* [Media & Web](#media--web)
* [Integrations](#integrations)
* [Customization](#customization)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/integrations/nous-portal](./docs-integrations-nous-portal.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback](./docs-user-guide-checkpoints-and-rollback.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/configuration](./docs-user-guide-configuration.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/acp](./docs-user-guide-features-acp.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server](./docs-user-guide-features-api-server.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing](./docs-user-guide-features-batch-processing.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/browser](./docs-user-guide-features-browser.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution](./docs-user-guide-features-code-execution.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files](./docs-user-guide-features-context-files.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references](./docs-user-guide-features-context-references.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools](./docs-user-guide-features-credential-pools.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/cron](./docs-user-guide-features-cron.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation](./docs-user-guide-features-delegation.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers](./docs-user-guide-features-fallback-providers.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks](./docs-user-guide-features-hooks.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/image-generation](./docs-user-guide-features-image-generation.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp](./docs-user-guide-features-mcp.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/memory](./docs-user-guide-features-memory.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers](./docs-user-guide-features-memory-providers.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/personality](./docs-user-guide-features-personality.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins](./docs-user-guide-features-plugins.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing](./docs-user-guide-features-provider-routing.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/skills](./docs-user-guide-features-skills.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/skins](./docs-user-guide-features-skins.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/tools](./docs-user-guide-features-tools.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/tts](./docs-user-guide-features-tts.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/vision](./docs-user-guide-features-vision.md)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode](./docs-user-guide-features-voice-mode.md)
