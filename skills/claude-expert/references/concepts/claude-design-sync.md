---
type: Reference
title: Claude Design Sync - Claude Code
date_created: 2026-06-29
tags: [concept, auto-generated, design]
platform: integration
---

# Claude Design Sync - Claude Code

**Source:** Learned from Claude Design Beta interface (Chat Mode)

Claude Design is a feature available in Claude Desktop (Chat Mode) that allows you to create polished visual outputs, prototypes, slides, and one-pagers by collaborating with Claude.

## Synchronizing Your Design System

If your design system already lives in code (e.g., React components, design tokens), you can synchronize it directly with Claude without needing to manually upload files or connect external design tools like Figma.

Claude Code provides the `/design-sync` command to automatically read and sync your tokens and React components directly into Claude Design.

### How to use `/design-sync`

1. Open your terminal.
2. Navigate to the root directory of your design system package:
   ```bash
   $ cd path/to/your-design-system
   ```
3. Start Claude Code:
   ```bash
   $ claude
   ```
4. Run the `/design-sync` slash command inside the Claude Code interactive prompt:
   ```bash
   > /design-sync
   ```

Claude Code will read your tokens and React components directly and sync them with your Claude account, making them available when you use the **Claude Design Beta** feature in the desktop app's Chat tab to generate high-fidelity UI.
