---
title: Deny specific skills
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# Deny specific skills
Skill(deploy *)
```

Permission syntax: `Skill(name)` for exact match, `Skill(name *)` for prefix match with any arguments.
**Hide individual skills** by adding `disable-model-invocation: true` to their frontmatter. This removes the skill from Claude’s context entirely.

The `user-invocable` field only controls menu visibility, not Skill tool access. Use `disable-model-invocation: true` to block programmatic invocation.

### [​](#override-skill-visibility-from-settings) Override skill visibility from settings

The `skillOverrides` setting controls skill visibility from your [settings](/docs/en/settings) instead of the skill’s own frontmatter. Use it for skills whose SKILL.md you don’t want to edit, such as ones checked into a shared project repo or provided by an MCP server. The `/skills` menu writes it for you: highlight a skill and press `Space` to cycle states, then `Enter` to save to `.claude/settings.local.json`.
Each key is a skill name and each value is one of four states:

| Value | Listed to Claude | In `/` menu |
| --- | --- | --- |
| `"on"` | Name and description | Yes |
| `"name-only"` | Name only | Yes |
| `"user-invocable-only"` | Hidden | Yes |
| `"off"` | Hidden | Hidden |

A skill that is absent from `skillOverrides` is treated as `"on"`. The example below collapses one skill to its name and turns another off entirely:

```
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

Plugin skills are not affected by `skillOverrides`. Manage those through `/plugin` instead.

## [​](#evaluate-and-iterate-on-a-skill) Evaluate and iterate on a skill

Seeing a skill trigger tells you Claude found it, not that it did what you intended. To know a skill is working, measure two things separately: whether Claude invokes it on the prompts it should, and whether the output matches what you expect when it does.
The check for both is a baseline comparison. Collect a few realistic prompts, run each one in a fresh session with the skill available and again with it [disabled](#override-skill-visibility-from-settings), and compare the results. A fresh session matters because leftover context from authoring the skill will mask gaps in the written instructions.

### [​](#run-evals-with-skill-creator) Run evals with skill-creator

The [`skill-creator` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) automates the comparison loop inside Claude Code. Install it from the official marketplace:

```
/plugin install skill-creator@claude-plugins-official
```

If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you haven’t added it before. Then retry the install.
After installing, run `/reload-plugins` to make the plugin’s skills available in the current session. Then ask Claude to evaluate an existing skill, for example `evaluate my summarize-changes skill with skill-creator`. The plugin walks you through writing test cases and runs the loop:

* **Test cases**: stores prompts, input files, and expected behavior in `evals/evals.json` inside the skill directory
* **Isolated runs**: spawns a [subagent](/docs/en/sub-agents) per test case so each run starts with a clean context, and records token count and duration
* **Grading**: checks each assertion against the output and writes pass or fail with evidence to `grading.json`
* **Benchmark**: aggregates pass rate, time, and tokens for with-skill versus without-skill into `benchmark.json` so you can compare the pass-rate improvement against the token and time overhead
* **Version comparison**: runs a blind A/B between two versions of the skill so you can confirm an edit is an improvement before committing it
* **Description tuning**: generates should-trigger and should-not-trigger prompts, measures the hit rate, and proposes description edits when the skill activates on the wrong requests
* **Review viewer**: opens an HTML report where you inspect each output and record qualitative feedback that the next iteration reads

For the eval file format and the full iteration workflow, see [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) on agentskills.io. For background on the benchmark and comparison modes, see the [skill-creator announcement](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills).

## [​](#share-skills) Share skills

Skills can be distributed at different scopes depending on your audience:

* **Project skills**: Commit `.claude/skills/` to version control
* **Plugins**: Create a `skills/` directory in your [plugin](/docs/en/plugins)
* **Managed**: Deploy organization-wide through [managed settings](/docs/en/settings#settings-files)

### [​](#generate-visual-output) Generate visual output

Skills can bundle and run scripts in any language, giving Claude capabilities beyond what’s possible in a single prompt. One powerful pattern is generating visual output: interactive HTML files that open in your browser for exploring data, debugging, or creating reports.
This example creates a codebase explorer: an interactive tree view where you can expand and collapse directories, see file sizes at a glance, and identify file types by color.
Create the Skill directory:

```
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Save this to `~/.claude/skills/codebase-visualizer/SKILL.md`. The description tells Claude when to activate this Skill, and the instructions tell Claude to run the bundled script. The script path uses [`${CLAUDE_SKILL_DIR}`](#available-string-substitutions) so it resolves correctly whether the skill is installed at the personal, project, or plugin level:

```
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python3 *)
---