# Petdex — Install and select animated petdex mascots for Hermes | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-petdex](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/productivity/productivity-petdex)

本页总览

Install and select animated petdex mascots for Hermes.

## Skill metadata[​](#skill-metadata "Skill metadata的直接链接")

|  |  |
| --- | --- |
| Source | Bundled (installed by default) |
| Path | `skills/productivity/petdex` |
| Version | `1.0.0` |
| Author | Hermes Agent |
| License | MIT |
| Platforms | linux, macos, windows |
| Tags | `petdex`, `mascot`, `display`, `cli`, `tui`, `desktop` |

## Reference: full SKILL.md[​](#reference-full-skillmd "Reference: full SKILL.md的直接链接")

信息

The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.

# Petdex Skill

Browse, install, and select animated "pet" mascots from the public
[petdex](https://github.com/crafter-station/petdex) gallery. An installed pet
reacts to agent activity (idle, running a tool, reviewing, error, done) across
the Hermes CLI, TUI, and desktop app. This skill drives the `hermes pets` CLI
and the `display.pet` config — it does not generate sprites.

## When to Use[​](#when-to-use "When to Use的直接链接")

* The user wants a desktop/terminal mascot or asks about "pets" / petdex.
* The user wants to change, preview, or disable the active pet.
* Diagnosing why a pet isn't showing (terminal graphics support, config).

## Prerequisites[​](#prerequisites "Prerequisites的直接链接")

* Network access to `petdex.dev` for the gallery/manifest (read-only, no auth).
* Pillow (a core Hermes dependency) for sprite decoding — already installed.
* For full-fidelity terminal rendering: a graphics-capable terminal (kitty,
  Ghostty, WezTerm, iTerm2, or sixel). Otherwise a truecolor Unicode
  half-block fallback is used automatically.

## How to Run[​](#how-to-run "How to Run的直接链接")

Use the `terminal` tool to run `hermes pets <subcommand>`.

## Quick Reference[​](#quick-reference "Quick Reference的直接链接")

| Goal | Command |
| --- | --- |
| Browse the gallery | `hermes pets list` (add a substring to filter: `hermes pets list cat`) |
| List installed pets | `hermes pets list --installed` |
| Install a pet | `hermes pets install <slug>` (add `--select` to make it active) |
| Set the active pet | `hermes pets select <slug>` (omit slug for a picker) |
| Resize the pet everywhere | `hermes pets scale <factor>` (e.g. `0.5`, clamped 0.1–3.0) |
| Preview/animate in terminal | `hermes pets show [slug] [--cycle] [--state run]` |
| Disable the pet | `hermes pets off` |
| Remove a pet | `hermes pets remove <slug>` |
| Diagnose setup | `hermes pets doctor` |

## Procedure[​](#procedure "Procedure的直接链接")

1. Find a pet: `hermes pets list <query>` and note its `slug`.
2. Install + activate: `hermes pets install <slug> --select`.
3. Preview it: `hermes pets show` (Ctrl+C to stop).
4. Confirm setup: `hermes pets doctor` — shows the resolved pet, configured
   render mode, detected terminal graphics protocol, and effective mode.

Pets install into `<HERMES_HOME>/pets/<slug>/` (profile-aware). Selecting a pet
writes `display.pet.slug` + `display.pet.enabled` to `config.yaml`.

## Configuration[​](#configuration "Configuration的直接链接")

Under `display.pet` in `config.yaml`:

* `enabled` (bool) — master on/off.
* `slug` (str) — active pet; empty = first installed.
* `render_mode` — `auto` (detect) | `kitty` | `iterm` | `sixel` | `unicode` | `off`.
* `scale` (float) — on-screen size of the native 192×208 frames (default 0.33,
  clamped 0.1–3.0). One knob resizes every surface; set it with
  `hermes pets scale <factor>`, the `/pet scale` slash command, or the desktop
  Appearance slider.
* `unicode_cols` (int) — width in columns for the Unicode fallback.

## Pitfalls[​](#pitfalls "Pitfalls的直接链接")

* A pet only shows once one is installed AND selected (`enabled: true`).
* Inside a pipe/redirect (no TTY) terminal rendering is disabled by design.
* The petdex npm CLI installs to `~/.codex/pets`; Hermes uses its own
  profile-scoped `<HERMES_HOME>/pets/` instead — install through `hermes pets`.

## Verification[​](#verification "Verification的直接链接")

* `hermes pets doctor` reports `✓ ready` when a pet is installed, selected,
  enabled, and Pillow is importable.

* [Skill metadata](#skill-metadata)
* [Reference: full SKILL.md](#reference-full-skillmd)
* [When to Use](#when-to-use)
* [Prerequisites](#prerequisites)
* [How to Run](#how-to-run)
* [Quick Reference](#quick-reference)
* [Procedure](#procedure)
* [Configuration](#configuration)
* [Pitfalls](#pitfalls)
* [Verification](#verification)