---
type: Reference
title: CLI Tutorial
date_created: 2026-07-01
source_url: https://antigravity.google/docs/cli/tutorial
description: Stepping through a real-world debugging task.
tags: [concept, llms-txt, js-rendered]
platform: cli
---

* side\_navigation
* Antigravity CLI
>* Tutorial

# Antigravity CLI Tutorial[link](#antigravity-cli-tutorial)

Learn how to launch Antigravity CLI, collaborate with an autonomous local agent, review generated files, and execute terminal test commands.

## Overview[link](#overview)

This guide walks you through a rapid onboarding exercise. You will direct an autonomous agent to create a Python utility script, review the changes, and verify its execution.

## Step-by-step[link](#step-by-step)

1. Create a clean project directory and launch the Antigravity TUI

content\_copy

```
               mkdir agy-demo && cd agy-demo
   agy
```

info

**First Launch**: If running `agy` for the first time, follow the terminal instructions to complete silent authentication. See [Installation & Auth](/docs/cli/install) for troubleshooting details.

1. Prompt the agent to generate a Python scraping script

Type the following instruction in the prompt box at the bottom of your screen and press `Enter`:

content\_copy

```
               Write a simple python script to fetch web page text
```

The agent reads the workspace, determines that no files exist, and formulates a plan to create a script. You will see real-time updates as the agent performs reasoning and schedules actions.

1. Open the artifact review screen to inspect the proposed code

Once the agent finishes generating the file, a notification appears. Press `ctrl+r` to enter the **Artifact Review** screen.

* Navigate to the newly created `main.py` using `↑`/`↓`.
* Review the complete file content and diff.
* Press `y` to approve the creation of `main.py`.
* Press `Esc` to close the review panel and return to the primary prompt.

1. Execute a test command with the agent to verify the output

Direct the agent to run the Python script to verify its behavior. Type the following command in the prompt box and press `Enter`:

content\_copy

```
               Run the python script and show me the output
```

The agent proposes to run `python3 main.py`. Press `y` to confirm and execute the command. The agent runs the script locally and streams the standard output directly into your terminal screen.

1. Exit the Antigravity session

Once you complete your task, press `ctrl+d` (or type `/exit`) in the prompt box to close the TUI and restore your original shell session.

## Next steps[link](#next-steps)

Now that you have executed your first agent-assisted workflow, learn how to configure the CLI and master core concepts:

* **[Installation & Auth](/docs/cli/install)**: Detailed instructions on installing `agy` and setting up SSH profiles.
* **[Prompting & Interaction](/docs/cli/prompting)**: Best practices for multiline inputs, pasting media files, and active interrupt controls.
* **[Reviewing Artifacts](/docs/cli/artifacts)**: Deep dive into the "Trust through Transparency" architectural pattern.

On this Page