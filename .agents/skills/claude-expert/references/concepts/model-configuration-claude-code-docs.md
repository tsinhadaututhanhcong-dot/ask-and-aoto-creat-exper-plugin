---
type: Reference
title: Model configuration - Claude Code Docs
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Model configuration - Claude Code Docs
**Source:** [https://code.claude.com/docs/en/model-config](https://code.claude.com/docs/en/model-config)

## [​](#available-models) Available models

For the `model` setting in Claude Code, you can configure either:

* A **model alias**
* A **model name**
  + Anthropic API: a full **[model name](https://platform.claude.com/docs/en/about-claude/models/overview)**
  + Bedrock: an inference profile ARN
  + Foundry: a deployment name
  + Vertex: a version name

`ANTHROPIC_BASE_URL` changes where requests are sent, not which model answers them. To route Claude through an LLM gateway, see [LLM gateways](/docs/en/llm-gateway).

### [​](#model-aliases) Model aliases

Model aliases provide a convenient way to select model settings without
remembering exact version numbers:

| Model alias | Behavior |
| --- | --- |
| **`default`** | Special value that clears any model override and reverts to the recommended model for your account type. Not itself a model alias |
| **`best`** | Uses Fable 5 where your organization has access to it, otherwise the latest Opus model |
| **`fable`** | Uses Claude Fable 5 for your hardest and longest-running tasks |
| **`sonnet`** | Uses the latest Sonnet model for daily coding tasks |
| **`opus`** | Uses the latest Opus model for complex reasoning tasks |
| **`haiku`** | Uses the fast and efficient Haiku model for simple tasks |
| **`sonnet[1m]`** | Uses Sonnet with a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) for long sessions |
| **`opus[1m]`** | Uses Opus with a [1 million token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) for long sessions |
| **`opusplan`** | Special mode that uses `opus` during plan mode, then switches to `sonnet` for execution |

On the Anthropic API, `opus` resolves to Opus 4.8 and `sonnet` resolves to Sonnet 4.6. On [Claude Platform on AWS](/docs/en/claude-platform-on-aws), `opus` resolves to Opus 4.7 and `sonnet` resolves to Sonnet 4.6. On Bedrock, Vertex, and Foundry, `opus` resolves to Opus 4.6 and `sonnet` resolves to Sonnet 4.5; newer models are available on those providers by selecting the full model name explicitly or setting `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_SONNET_MODEL`.
Aliases point to the recommended version for your provider and update over time. To pin to a specific version, use the full model name, for example `claude-opus-4-8`, or set the corresponding environment variable like `ANTHROPIC_DEFAULT_OPUS_MODEL`.

Opus 4.8 requires Claude Code v2.1.154 or later. Run `claude update` to upgrade.

### [​](#work-with-fable-5) Work with Fable 5

[Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) is the most capable model in Claude Code, suited to tasks larger than a single sitting. It sustains long autonomous sessions, investigates before acting, and verifies its work more often than smaller models.
Fable 5 is not the default model. Select it with `/model fable`. Requests that its safety classifiers flag, most often in cybersecurity and biology domains, trigger [automatic model fallback](#automatic-model-fallback).
To get the most from Fable 5:

* **Describe the outcome, not the steps**: hand it the result you want and let it plan the path. To keep it working until that outcome holds, [set a goal](/docs/en/goal).
* **Hand it ambiguous problems**: root-cause investigations, outage debugging, and architecture decisions are where the extra investigation and verification pay off.
* **Skip the verification reminders**: it verifies its own work with less prompting, so reminders to test or check are usually unnecessary.
* **Size up larger tasks**: give it work you would normally break into pieces. It holds long sessions without losing the thread.

Fable 5 requires Claude Code v2.1.170 or later. Older versions do not show Fable 5 in the model picker and cannot select it. Run `claude update` to upgrade. Fable 5 is not available under [zero data retention](/docs/en/zero-data-retention), where the `/model` picker either omits it or shows it disabled.

### [​](#setting-your-model) Setting your model

You can configure your model in several ways, listed in order of priority:

1. **During session**: use `/model <alias|name>` to switch immediately, or run `/model` with no argument to open the picker. The picker asks for confirmation when the conversation has prior output, since the next response re-reads the full history without cached context
2. **At startup**: launch with `claude --model <alias|name>`
3. **Environment variable**: set `ANTHROPIC_MODEL=<alias|name>`
4. **Settings**: configure permanently in your settings file using the `model` field

As of v2.1.153, `/model` saves your choice as the default for new sessions by writing the `model` field in your user settings. In the picker:

* `Enter`: switch model and save as your default
* `s`: switch model for this session only

Typing `/model <name>` directly behaves like `Enter`. Project and managed settings still take precedence and reapply on the next launch.
In v2.1.144 through v2.1.152, `/model` applied to the current session only and `d` in the picker saved a default.
The `--model` flag and `ANTHROPIC_MODEL` environment variable apply only to the session you launch with them. To run different models in different terminals at the same time, launch each one with its own `--model` flag rather than switching with `/model`.
Resumed sessions started with `claude --resume`, `--continue`, or the `/resume` picker keep the model they were using when the transcript was saved, regardless of the current `model` setting. If that model has been retired or is excluded by [`availableModels`](#restrict-model-selection), the session falls through to the normal precedence order. This prevents another session’s `/model` choice from changing the model on resume.
When the active model at startup comes from project or managed settings rather than your own selection, the startup header shows which settings file set it. Run `/model` to override; the project or managed setting reapplies on the next launch.
When the requested model has a scheduled retirement date or is automatically remapped to a newer version, Claude Code shows a warning that names the requested model. Interactive sessions show it as a startup notice. From v2.1.182, the same warning is written to stderr in [non-interactive mode](/docs/en/headless) when using the default text output format. The check also covers a `model` set in [subagent frontmatter](/docs/en/sub-agents). The stderr warning is suppressed for `--output-format json` and `stream-json`; read the actual model from the `modelUsage` field of the [result message](/docs/en/headless#get-structured-output) instead.
Example usage:

```