---
title: Remove user settings and state (Windows PowerShell)
date_created: 2026-06-29
tags: [concept, auto-generated]
platform: cli
---

# Remove user settings and state (Windows PowerShell)
```powershell
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force
```
