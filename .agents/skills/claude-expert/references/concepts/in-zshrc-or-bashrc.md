---
type: Reference
title: In ~/.zshrc or ~/.bashrc
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: shared
---

# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

The `$-` variable contains shell flags, and `i` means interactive. Hooks run in non-interactive shells, so the echo is skipped.

### [​](#debug-techniques) Debug techniques

The transcript view, toggled with `Ctrl+O`, shows a one-line summary for each hook that fired: success is silent, blocking errors show stderr, and non-blocking errors show a `<hook name> hook error` notice followed by the first line of stderr.
For full execution details including which hooks matched, their exit codes, stdout, and stderr, read the debug log. Start Claude Code with `claude --debug-file /tmp/claude.log` to write to a known path, then `tail -f /tmp/claude.log` in another terminal. If you started without that flag, run `/debug` mid-session to enable logging and find the log path.

## [​](#learn-more) Learn more

* [Hooks reference](/docs/en/hooks): full event schemas, JSON output format, async hooks, and MCP tool hooks
* [Security considerations](/docs/en/hooks#security-considerations): review before deploying hooks in shared or production environments
* [Bash command validator example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): complete reference implementation

Was this page helpful?

YesNo

[Share session output as artifacts](/docs/en/artifacts)[Push external events to Claude](/docs/en/channels)

⌘I

---