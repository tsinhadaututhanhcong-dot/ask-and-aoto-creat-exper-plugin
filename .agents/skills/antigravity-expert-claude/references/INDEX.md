# Master Index

Nguon: https://antigravity.google/llms.txt (render qua headless browser)
Index nay duoc nhom theo san pham Antigravity (2.0 / IDE / CLI / SDK / dung chung / marketing).
KHONG co trang doi chieu chinh thuc giua cac san pham (khac voi Claude Code). Neu mot tinh nang chi thay nhac o mot san pham, KHONG duoc suy dien la san pham khac cung co - phai tra loi la 'chi thay xac nhan o <san pham X>, chua thay tai lieu cho <san pham Y>'.

## Antigravity 2.0 (ung dung desktop, command center)

- [Antigravity 2.0](concepts/product-antigravity-2.md): Graphical command center interface for monitoring and managing active background agents.
- [Overview](concepts/docs-overview.md): Overview of the 2.0 interface.
- [Getting Started](concepts/docs-getting-started.md): Quickstart guide.
- [Features](concepts/docs-features.md): Major components and features of the UI.
- [Projects](concepts/docs-projects.md): Configuring workspaces, directory bounds, and paths.
- [Settings](concepts/docs-settings.md): User configuration options.
- [Agent Settings](concepts/docs-agent-settings.md): System prompt, tool rules, and runtime adjustments.
- [Artifact Review](concepts/docs-artifact-review.md): Interface for approving agent plans and tasks.
- [Model Context Protocol (MCP)](concepts/docs-mcp.md): Extending agent tools using standard MCP servers.
- [Skills](concepts/docs-skills.md): Specifying packaged skill scripts and instructions.
- [Rules & Workflows](concepts/docs-rules-workflows.md): Designing workflow boundaries and system instructions.
- [Plugins](concepts/docs-plugins.md): Extending GUI features via plugins.
- [Hooks](concepts/docs-hooks.md): Custom lifecycle trigger hooks.
- [Sidecars](concepts/docs-sidecars.md): Long-running background scripts.
- [Permissions](concepts/docs-permissions.md): Sandbox controls and folder permissions.
- [Subagents](concepts/docs-subagents.md): Orchestrating multiple subagents in parallel.
- [Artifacts](concepts/docs-artifacts.md): Managing structured deliverables.
- [Implementation Plan](concepts/docs-implementation-plan.md): Structure of files created for proposing code updates.
- [Walkthrough](concepts/docs-walkthrough.md): Structural representation of walkthrough reviews.
- [Screenshots](concepts/docs-screenshots.md): How visual artifacts capture layout updates.

## Antigravity IDE

- [Antigravity IDE](concepts/product-antigravity-ide.md): Fully featured development editor integrating agentic workflows and interactive artifact review.
- [IDE Overview](concepts/docs-ide-overview.md): Editor integrations and features.
- [IDE Getting Started](concepts/docs-ide-getting-started.md): Setup and config inside the editor.
- [Tab Completion](concepts/docs-ide-tab.md): Real-time code completion models.
- [Agent Side Panel](concepts/docs-ide-agent-side-panel.md): Interacting with agents alongside the text buffer.
- [Reviewing Changes](concepts/docs-ide-review-changes-editor.md): In-line code diff review and modification.
- [IDE Implementation Plan](concepts/docs-ide-implementation-plan.md): File-level planning and code generation.
- [IDE Walkthrough](concepts/docs-ide-walkthrough.md): Interactive codebase tour artifacts.
- [IDE Screenshots](concepts/docs-ide-screenshots.md): Triggering screenshot generation inside the editor.
- [IDE Browser Recordings](concepts/docs-ide-browser-recordings.md): Video artifact tracking.
- [Browser Integration](concepts/docs-ide-browser.md): Chrome driver setup for interactive web testing.
- [Allowlist & Denylist](concepts/docs-ide-allowlist-denylist.md): Domain access rules for agents.
- [Chrome Profiles](concepts/docs-ide-separate-chrome-profile.md): Isolating development data.
- [IDE MCP Servers](concepts/docs-ide-mcp.md): Editor-level tool integration.
- [IDE Skills](concepts/docs-ide-skills.md): Loading custom scripts for inline code modification.
- [IDE Rules](concepts/docs-ide-rules.md): Contextual behavior guidelines.
- [IDE Workflows](concepts/docs-ide-workflows.md): Pre-configured multi-step plans.
- [IDE Plugins](concepts/docs-ide-plugins.md): Extensibility mechanisms.
- [IDE Hooks](concepts/docs-ide-hooks.md): Triggering agent execution on text events.
- [IDE Settings](concepts/docs-ide-settings.md): Editor UI preferences.

## Antigravity CLI

- [Download for Linux](concepts/download-linux.md): Download CLI for Linux environments.
- [Antigravity CLI](concepts/product-antigravity-cli.md): Lightweight, terminal-first interface for developers who work in the shell.
- [CLI Overview](concepts/docs-cli-overview.md): CLI architecture and usage patterns.
- [CLI Getting Started](concepts/docs-cli-getting-started.md): Quick launch instructions.
- [CLI Installation](concepts/docs-cli-install.md): Setting up dependencies and command line tools.
- [CLI Tutorial](concepts/docs-cli-tutorial.md): Stepping through a real-world debugging task.
- [CLI Usage](concepts/docs-cli-using.md): Primary prompt flow and keyboard commands.
- [CLI Features](concepts/docs-cli-features.md): Shell-specific features and utilities.
- [Migration from gcli](concepts/docs-cli-gcli-migration.md): Upgrading legacy CLI tools.
- [Prompting Best Practices](concepts/docs-cli-prompting.md): Writing clear instructions for CLI agents.
- [CLI Artifacts](concepts/docs-cli-artifacts.md): Reviewing deliverables in the terminal.
- [CLI Conversations](concepts/docs-cli-conversations.md): Managing back-and-forth prompt history.
- [CLI Subagents](concepts/docs-cli-subagents.md): Delegating CLI tasks to sub-sessions.
- [CLI Permissions](concepts/docs-cli-permissions.md): Shell-specific capability boundaries.
- [CLI Sandbox](concepts/docs-cli-sandbox.md): Running tools inside isolated sandboxes.
- [CLI Settings](concepts/docs-cli-settings.md): Storing prompt defaults and global parameters.
- [CLI Credits](concepts/docs-cli-credits.md): Tracking billing and token quotas.
- [CLI Plugins](concepts/docs-cli-plugins.md): Registering shell extensions.
- [CLI Status Line](concepts/docs-cli-statusline.md): Interpreting shell prompts and state badges.
- [CLI Title Bar](concepts/docs-cli-title.md): Shell configuration indicators.
- [CLI Best Practices](concepts/docs-cli-best-practices.md): Optimizing shell prompt sequences.
- [CLI Troubleshooting](concepts/docs-cli-troubleshooting.md): Recovering from common sandbox errors.
- [CLI Reference](concepts/docs-cli-reference.md): Complete reference card of commands and shortcuts.

## Antigravity SDK

- [Antigravity SDK](concepts/product-antigravity-sdk.md): Python SDK to program custom agents, tools, MCP integrations, and tasks.
- [SDK Overview](concepts/docs-sdk-overview.md): Python API reference and runtime binary installation.

## Dung chung nhieu san pham

- [Changelog](concepts/changelog.md): Detailed historical release updates.
- [Releases](concepts/releases.md): Summary of major software releases.
- [Enterprise](concepts/use-cases-enterprise.md): Tailored for corporate teams, secure permissions, and cloud-scale collaboration.
- [Frontend](concepts/use-cases-frontend.md): Browser-in-the-loop verification, UI screenshotting, and visual feedback loops.
- [Fullstack](concepts/use-cases-fullstack.md): Grounding development in verifiable artifacts, tasks, and editor handoffs.
- [Science](concepts/use-cases-science.md): Specialized workflows integrated with major scientific databases and frontier models like AlphaGenome.
- [Documentation Home](concepts/docs-home.md): Getting started guide for the platform.
- [Build with Google](concepts/docs-build-with-google.md): How to connect with Gemini and build solutions.
- [Models](concepts/docs-models.md): Supported LLM classes (Pro, Flash, etc.).
- [Enterprise Features](concepts/docs-enterprise.md): Organization level deployments.
- [Frequently Asked Questions](concepts/docs-faq.md): General help and troubleshooting.

## Trang marketing / khong phai tai lieu ky thuat

- [Homepage](concepts/index.md): Main landing page.
- [Download for macOS](concepts/download.md): Download clients for macOS (Apple Silicon).
- [Pricing](concepts/pricing.md): Plans, credits, and enterprise tiers.
- [Support](concepts/support.md): Support resources and contact info.
- [Terms](concepts/terms.md): Terms and conditions.
- [Press](concepts/press.md): Media kit and assets.
- [Product Directory](concepts/product.md): Directory list of all Google Antigravity products.
- [Use Cases Directory](concepts/use-cases.md): Directory list of all enterprise, frontend, fullstack, science, and marketing use cases.
- [Organization Interest Form](concepts/interest-form.md): Form to request access for teams and enterprise plans.
- [LLMs Resource Index](concepts/llmstxt.md): This page, listing all available paths and resources for LLM processing.
- [Firebase Studio Migration](concepts/docs-firebase-studio-migration.md): Transitioning project settings from Firebase Studio.
- [Plans & Pricing](concepts/docs-plans.md): Choosing the right subscription plan.
