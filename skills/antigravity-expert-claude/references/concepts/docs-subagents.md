---
type: Reference
title: Subagents
date_created: 2026-07-01
source_url: https://antigravity.google/docs/subagents
description: Orchestrating multiple subagents in parallel.
tags: [concept, llms-txt, js-rendered]
platform: antigravity-2.0
---

* side\_navigation
* Antigravity 2.0
>* Agent Capabilities
>* Subagents

# Asynchronous Subagents[link](#asynchronous-subagents)

Subagents are an excellent way to parallelize complex tasks and preserve the context of your main agent. Instead of executing every step serially, an agent can delegate tasks—such as running tests or performing extensive codebase searches—to dedicated subagents. This architecture frees the parent agent to continue working on other tasks in parallel and prevents its context window from being polluted by the details of a subagent's work.

## Invoking Subagents[link](#invoking-subagents)

The parent agent calls the `invoke_subagent` tool to spawn a new concurrent session with a dedicated role and initial prompt.

* **Workspace Options**: The subagent can either inherit the same workspace as its parent or create an isolated Git worktree.
* **Context Isolation**: The subagent runs using the same model as its parent but does not inherit the parent's existing conversation history (context window), starting with a clean slate.
* **Execution**: Once invoked, the subagent immediately begins executing its task. A parent agent can invoke multiple subagents at any time.
* **Monitoring**: You can directly monitor the progress of any subagent by clicking into its conversation via the subagent panel.

## Subagent Lifecycle and States[link](#subagent-lifecycle-and-states)

Subagents run asynchronously in the background, allowing the parent agent to delegate a task and immediately resume its own work. At any point, a subagent exists in one of three states:

### 1. Running[link](#1-running)

The subagent is actively executing its task, calling tools, and generating responses.

* **Cancellation**: You can cancel a running subagent by clicking the **Stop Subagent** button in the subagent panel. This instantly cancels generation and transitions the subagent to an idle state.
* **Parent Control**: The parent agent can also interrupt a subagent (by sending a message) or kill it entirely.

### 2. Idle[link](#2-idle)

The subagent has completed its task, sent a message containing the results to its parent agent, and stopped execution.

* **Re-awakening**: An idle agent can be awoken and return to the *Running* state upon receiving a message from another agent (it does not have to be its parent).
* **Context Retention**: When awoken, the agent retains all context from its prior work.

### 3. Killed[link](#3-killed)

The subagent is permanently terminated and cannot be re-awoken.

* **Cleanup**: Any temporary Git worktrees generated for the subagent are automatically cleaned up.
* **Visibility**: You and other agents can still view the historical conversation transcript of a killed subagent.

## Inter-Agent Communication[link](#inter-agent-communication)

Agents communicate by sending messages to each other using unique agent IDs.

* **Flexible Routing**: Agents can communicate not only with their direct parents or subagents, but also with any other active agent whose ID is known.
* **Auto-Wake**: If an idle agent receives a message, it is automatically re-awakened to process the new information.
* **Shared Transcripts**: Agents can view each other's conversation transcripts, providing a comprehensive view of the collaborative workflow.

## Built-In vs. Custom Subagents[link](#built-in-vs-custom-subagents)

### Built-In Subagents[link](#built-in-subagents)

Antigravity comes pre-packaged with several specialized subagents:

* **`research`**: Optimized for codebase research, navigation, and exploration.
* **`browser`**: Operates sandboxed web browsers to perform interactive browser tasks (invoked exclusively via the `/browser` slash command).
* **`self`**: A direct clone of the calling agent, sharing the identical system prompt and toolsets.

### Custom Subagents[link](#custom-subagents-2)

Agents can define their own custom subagents dynamically using the `define_subagent` tool.

* **Configuration**: Define a custom system prompt and specific toolsets for read-only, write (including running terminal commands), and subagent delegation capabilities.
* **Scope**: Once defined, the custom subagent can be invoked repeatedly for the remainder of the conversation.

## Delegation Hierarchy and Limits[link](#delegation-hierarchy-and-limits)

Subagents can invoke their own subagents, enabling multiple layers of delegation and hierarchical team structures.

warning

**Nesting Depth Limit**: A maximum nesting depth of **10 levels** (layers of subagents beneath the main agent) is strictly enforced to prevent runaway resource exhaustion.

## Permissions and Configuration Inheritance[link](#permissions-and-configuration-inheritance)

Subagents inherit their parent's safety configurations to maintain robust security boundaries:

* **Inherited Scopes**: Subagents automatically inherit the parent's allowed terminal command prefixes and file read/write directory scopes. A subagent cannot perform any action that the user has not already approved for the parent.
* **Workspace Access**: Parent agents retain full access to their subagents' workspaces, including those operating on isolated Git worktrees.
* **Permission Bubbling**: If a subagent encounters a tool call that requires explicit user confirmation, the request is automatically bubbled up to the subagent panel UI for your approval.

## Multi-Agent Teamwork (Ultra Plan Only)[link](#multi-agent-teamwork-ultra-plan-only)

Antigravity 2.0 introduces advanced multi-agent orchestration for extremely complex tasks.

star

**Ultra Plan Exclusive**: The `/teamwork-preview` slash command is currently in preview and is exclusive to users on the **Ultra ($200/mo) plan**.

Using `/teamwork-preview` prompts the main agent to launch a collaborative multi-agent framework. This framework features built-in error recovery, automatic retries, and coordination logic, allowing you to simply define the high-level goal while the platform manages the overhead of a cooperative agent team.

On this Page