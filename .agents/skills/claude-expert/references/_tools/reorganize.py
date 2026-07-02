#!/usr/bin/env python3
"""One-shot reorganizer for the claude-expert wiki.

Reads references/INDEX.md, classifies every fragment by the platform of its
nearest preceding source-page anchor, writes a `platform:` field into each
concepts/*.md frontmatter, and regenerates INDEX.md grouped by platform with
the official cross-reference comparison docs pinned first.

Run once from anywhere: `python reorganize.py`. Paths are derived from this
file's own location, not hardcoded.
"""
import re
from collections import defaultdict
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
REFERENCES = SKILL_ROOT / "references"
CONCEPTS = REFERENCES / "concepts"
INDEX_PATH = REFERENCES / "INDEX.md"

PAGE_RE = re.compile(r"^- \[(.+)\]\(concepts/(.+\.md)\)$")

# Platform label -> section heading in the regenerated INDEX.md
SECTION_TITLES = {
    "reference-comparison": "Bảng đối chiếu nền tảng chính thức (tra trước tiên)",
    "cli": "CLI (dòng lệnh, terminal)",
    "desktop": "Desktop (ứng dụng độc lập, tab Code)",
    "vscode": "VS Code extension",
    "jetbrains": "JetBrains IDEs",
    "web": "Web (claude.ai/code)",
    "sdk": "Agent SDK / lập trình",
    "enterprise-provider": "Nhà cung cấp doanh nghiệp (Bedrock / Vertex AI / Foundry / admin)",
    "integration": "Tích hợp bên ngoài (GitHub, GitLab, Slack, Chrome, Code Review)",
    "shared": "Dùng chung mọi nền tảng",
    "misc": "Khác / chưa phân loại",
}
SECTION_ORDER = ["reference-comparison", "cli", "desktop", "vscode", "jetbrains",
                  "web", "sdk", "enterprise-provider", "integration", "shared", "misc"]

# Platform of each distinct source-page anchor title seen in INDEX.md.
PAGE_PLATFORM = {
    "Claude Design Sync - Claude Code": "integration",
    "Overview - Claude Code Docs": "shared",
    "Set up Claude Code for your organization - Claude Code Docs": "enterprise-provider",
    "Escalate hard decisions with the advisor tool - Claude Code Docs": "cli",
    "How the agent loop works - Claude Code Docs": "shared",
    "Use Claude Code features in the SDK - Claude Code Docs": "sdk",
    "Track cost and usage - Claude Code Docs": "shared",
    "Give Claude custom tools - Claude Code Docs": "sdk",
    "Rewind file changes with checkpointing - Claude Code Docs": "shared",
    "Intercept and control agent behavior with hooks - Claude Code Docs": "shared",
    "Hosting the Agent SDK - Claude Code Docs": "sdk",
    "Connect to external tools with MCP - Claude Code Docs": "sdk",
    "Migrate to Claude Agent SDK - Claude Code Docs": "sdk",
    "Modifying system prompts - Claude Code Docs": "sdk",
    "Observability with OpenTelemetry - Claude Code Docs": "shared",
    "Agent SDK overview - Claude Code Docs": "sdk",
    "Configure permissions - Claude Code Docs": "shared",
    "Plugins in the SDK - Claude Code Docs": "sdk",
    "Agent SDK reference - Python - Claude Code Docs": "sdk",
    "Quickstart - Claude Code Docs": "cli",
    "Securely deploying AI agents - Claude Code Docs": "sdk",
    "Persist sessions to external storage - Claude Code Docs": "sdk",
    "Work with sessions - Claude Code Docs": "sdk",
    "Agent Skills in the SDK - Claude Code Docs": "sdk",
    "Slash Commands in the SDK - Claude Code Docs": "sdk",
    "Stream responses in real-time - Claude Code Docs": "sdk",
    "Streaming Input - Claude Code Docs": "sdk",
    "Get structured output from agents - Claude Code Docs": "sdk",
    "Subagents in the SDK - Claude Code Docs": "sdk",
    "Todo Lists - Claude Code Docs": "shared",
    "Scale to many tools with tool search - Claude Code Docs": "shared",
    "Agent SDK reference - TypeScript - Claude Code Docs": "sdk",
    "TypeScript SDK V2 session API (removed) - Claude Code Docs": "sdk",
    "Handle approvals and user input - Claude Code Docs": "sdk",
    "Orchestrate teams of Claude Code sessions - Claude Code Docs": "cli",
    "Manage multiple agents with agent view - Claude Code Docs": "cli",
    "Run agents in parallel - Claude Code Docs": "cli",
    "Claude Code on Amazon Bedrock - Claude Code Docs": "enterprise-provider",
    "Track team usage with analytics - Claude Code Docs": "enterprise-provider",
    "Share session output as artifacts - Claude Code Docs": "shared",
    "Authentication - Claude Code Docs": "shared",
    "Configure auto mode - Claude Code Docs": "shared",
    "Claude Code on Microsoft Foundry - Claude Code Docs": "enterprise-provider",
    "Best practices for Claude Code - Claude Code Docs": "shared",
    "Champion kit - Claude Code Docs": "misc",
    "Claude Code changelog - Claude Code Docs": "shared",
    "Push events into a running session with channels - Claude Code Docs": "cli",
    "Channels reference - Claude Code Docs": "cli",
    "Checkpointing - Claude Code Docs": "shared",
    "Use Claude Code with Chrome (beta) - Claude Code Docs": "integration",
    "Use Claude Code on the web - Claude Code Docs": "web",
    "Explore the .claude directory - Claude Code Docs": "shared",
    "Claude Code on Claude Platform on AWS - Claude Code Docs": "enterprise-provider",
    "CLI reference - Claude Code Docs": "cli",
    "Code Review - Claude Code Docs": "integration",
    "Commands - Claude Code Docs": "shared",
    "Common workflows - Claude Code Docs": "shared",
    "Communications kit - Claude Code Docs": "misc",
    "Let Claude use your computer from the CLI - Claude Code Docs": "cli",
    "Explore the context window - Claude Code Docs": "shared",
    "Manage costs effectively - Claude Code Docs": "shared",
    "Data usage - Claude Code Docs": "shared",
    "Debug your configuration - Claude Code Docs": "cli",
    "Launch sessions from links - Claude Code Docs": "shared",
    "Desktop application - Claude Code Docs": "desktop",
    "Get started with the desktop app - Claude Code Docs": "desktop",
    "Schedule recurring tasks in Claude Code Desktop - Claude Code Docs": "desktop",
    "Development containers - Claude Code Docs": "cli",
    "Discover and install prebuilt plugins through marketplaces - Claude Code Docs": "shared",
    "Environment variables - Claude Code Docs": "cli",
    "Error reference - Claude Code Docs": "shared",
    "Speed up responses with fast mode - Claude Code Docs": "cli",
    "Feature availability - Claude Code Docs": "reference-comparison",
    "Extend Claude Code - Claude Code Docs": "shared",
    "Fullscreen rendering - Claude Code Docs": "cli",
    "Claude Code GitHub Actions - Claude Code Docs": "integration",
    "Claude Code with GitHub Enterprise Server - Claude Code Docs": "integration",
    "Claude Code GitLab CI/CD - Claude Code Docs": "integration",
    "Glossary - Claude Code Docs": "shared",
    "Keep Claude working toward a goal - Claude Code Docs": "shared",
    "Claude Code on Google Vertex AI - Claude Code Docs": "enterprise-provider",
    "Run Claude Code programmatically - Claude Code Docs": "cli",
    "Hooks reference - Claude Code Docs": "shared",
    "Automate actions with hooks - Claude Code Docs": "shared",
    "How Claude Code works - Claude Code Docs": "shared",
    "Interactive mode - Claude Code Docs": "cli",
    "JetBrains IDEs - Claude Code Docs": "jetbrains",
    "Customize keyboard shortcuts - Claude Code Docs": "cli",
    "Set up Claude Code in a monorepo or large codebase - Claude Code Docs": "shared",
    "Legal and compliance - Claude Code Docs": "shared",
    "LLM gateways - Claude Code Docs": "enterprise-provider",
    "Connect Claude Code to an LLM gateway - Claude Code Docs": "enterprise-provider",
    "Gateway protocol reference - Claude Code Docs": "enterprise-provider",
    "Roll out an LLM gateway for your organization - Claude Code Docs": "enterprise-provider",
    "Control MCP server access for your organization - Claude Code Docs": "enterprise-provider",
    "Connect Claude Code to tools via MCP - Claude Code Docs": "shared",
    "Connect to MCP servers - Claude Code Docs": "shared",
    "How Claude remembers your project - Claude Code Docs": "shared",
    "Model configuration - Claude Code Docs": "shared",
    "Monitoring - Claude Code Docs": "shared",
    "Enterprise network configuration - Claude Code Docs": "enterprise-provider",
    "Output styles - Claude Code Docs": "shared",
    "Choose a permission mode - Claude Code Docs": "shared",
    "Platforms and integrations - Claude Code Docs": "reference-comparison",
    "Constrain plugin dependency versions - Claude Code Docs": "shared",
    "Recommend your plugin from your CLI - Claude Code Docs": "cli",
    "Create and distribute a plugin marketplace - Claude Code Docs": "shared",
    "Recommend plugins for your org - Claude Code Docs": "shared",
    "Create plugins - Claude Code Docs": "shared",
    "Plugins reference - Claude Code Docs": "shared",
    "How Claude Code uses prompt caching - Claude Code Docs": "shared",
    "Prompt library - Claude Code Docs": "shared",
    "Continue local sessions from any device with Remote Control - Claude Code Docs": "cli",
    "Automate work with routines - Claude Code Docs": "shared",
    "Choose a sandbox environment - Claude Code Docs": "shared",
    "Configure the sandboxed Bash tool - Claude Code Docs": "shared",
    "Run prompts on a schedule - Claude Code Docs": "cli",
    "Security - Claude Code Docs": "shared",
    "Catch security issues as Claude writes code - Claude Code Docs": "shared",
    "Configure server-managed settings - Claude Code Docs": "enterprise-provider",
    "Manage sessions - Claude Code Docs": "cli",
    "Claude Code settings - Claude Code Docs": "shared",
    "Advanced setup - Claude Code Docs": "cli",
    "Extend Claude with skills - Claude Code Docs": "shared",
    "Claude Code in Slack - Claude Code Docs": "integration",
    "Customize your status line - Claude Code Docs": "cli",
    "Create custom subagents - Claude Code Docs": "shared",
    "Configure your terminal for Claude Code - Claude Code Docs": "cli",
    "Terminal guide for new users - Claude Code Docs": "cli",
    "Enterprise deployment overview - Claude Code Docs": "enterprise-provider",
    "Tools reference - Claude Code Docs": "shared",
    "Troubleshoot installation and login - Claude Code Docs": "cli",
    "Troubleshooting - Claude Code Docs": "shared",
    "Plan in the cloud with ultraplan - Claude Code Docs": "cli",
    "Find bugs with ultrareview - Claude Code Docs": "cli",
    "Voice dictation - Claude Code Docs": "shared",
    "Use Claude Code in VS Code - Claude Code Docs": "vscode",
    "Get started with Claude Code on the web - Claude Code Docs": "web",
    "What's new - Claude Code Docs": "shared",
    "Orchestrate subagents at scale with dynamic workflows - Claude Code Docs": "shared",
    "Run parallel sessions with worktrees - Claude Code Docs": "shared",
    "Zero data retention - Claude Code Docs": "enterprise-provider",
}
# The 14 weekly changelog pages all inherit "shared"
for week in range(13, 27):
    pass  # exact titles vary (dates); handled by prefix match fallback below

# Known filename collisions already resolved by hand (see COLLISIONS.md):
# old slug -> list of (title, new_filename) replacing the single old link
REMAP = {
    "basic-syntax.md": [
        ("Basic syntax (HTTP transport)", "basic-syntax--http-transport.md"),
        ("Basic syntax (SSE transport, deprecated)", "basic-syntax--sse-transport.md"),
        ("Basic syntax (stdio transport)", "basic-syntax--stdio-transport.md"),
        ("Basic syntax (add-json)", "basic-syntax--add-json.md"),
        ("Basic syntax (import from Claude Desktop)", "basic-syntax--add-from-claude-desktop.md"),
        ("Basic syntax (use Claude Code as an MCP server)", "basic-syntax--serve.md"),
    ],
    "enable-bedrock.md": [
        ("Enable Bedrock (corporate proxy tab)", "enable-bedrock--corporate-proxy.md"),
        ("Enable Bedrock (LLM gateway tab)", "enable-bedrock--llm-gateway.md"),
    ],
    "enable-microsoft-foundry.md": [
        ("Enable Microsoft Foundry (corporate proxy tab)", "enable-microsoft-foundry--corporate-proxy.md"),
        ("Enable Microsoft Foundry (LLM gateway tab)", "enable-microsoft-foundry--llm-gateway.md"),
    ],
    "enable-vertex.md": [
        ("Enable Vertex (corporate proxy tab)", "enable-vertex--corporate-proxy.md"),
        ("Enable Vertex (LLM gateway tab)", "enable-vertex--llm-gateway.md"),
    ],
    "configure-llm-gateway.md": [
        ("Configure LLM gateway (Amazon Bedrock)", "configure-llm-gateway--bedrock.md"),
        ("Configure LLM gateway (Microsoft Foundry)", "configure-llm-gateway--foundry.md"),
        ("Configure LLM gateway (Google Vertex AI)", "configure-llm-gateway--vertex.md"),
    ],
    "remove-user-settings-and-state.md": [
        ("Remove user settings and state (Windows PowerShell)", "remove-user-settings-and-state--windows.md"),
        ("Remove user settings and state (macOS, Linux, WSL)", "remove-user-settings-and-state--macos-linux-wsl.md"),
    ],
    "remove-project-specific-settings-run-from-your-project-directory.md": [
        ("Remove project-specific settings (Windows PowerShell — run from your project directory)",
         "remove-project-specific-settings--windows.md"),
        ("Remove project-specific settings (macOS, Linux, WSL — run from your project directory)",
         "remove-project-specific-settings--macos-linux-wsl.md"),
    ],
}


def classify_page(title: str) -> str:
    if title in PAGE_PLATFORM:
        return PAGE_PLATFORM[title]
    if title.startswith("Week ") and "- Claude Code Docs" in title:
        return "shared"
    return "misc"


def main():
    lines = INDEX_PATH.read_text(encoding="utf-8").splitlines()

    current_page = None
    current_platform = "misc"
    # ordered list of (title, filename, platform); de-duplicated by filename
    entries = []
    seen_filenames = set()
    unclassified_pages = set()

    for line in lines:
        m = PAGE_RE.match(line)
        if not m:
            continue
        title, filename = m.group(1), m.group(2)
        is_page_anchor = title.endswith("- Claude Code Docs") or title.endswith("- Claude Code")
        if is_page_anchor:
            current_page = title
            current_platform = classify_page(title)
            if current_platform == "misc" and title not in PAGE_PLATFORM:
                unclassified_pages.add(title)

        if filename in REMAP:
            for new_title, new_filename in REMAP[filename]:
                if new_filename in seen_filenames:
                    continue
                seen_filenames.add(new_filename)
                entries.append((new_title, new_filename, current_platform))
            continue

        if filename in seen_filenames:
            continue
        seen_filenames.add(filename)
        entries.append((title, filename, current_platform))

    if unclassified_pages:
        print("WARNING: pages with no platform mapping (defaulted to misc):")
        for p in sorted(unclassified_pages):
            print(f"  - {p}")

    # Write platform: into each concept file's frontmatter
    counts = defaultdict(int)
    missing_files = []
    for title, filename, platform in entries:
        counts[platform] += 1
        path = CONCEPTS / filename
        if not path.exists():
            missing_files.append(filename)
            continue
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            end = text.index("\n---\n", 4)
            frontmatter = text[4:end]
            body = text[end + 5:]
            if "platform:" not in frontmatter:
                frontmatter = frontmatter.rstrip("\n") + "\n" + f"platform: {platform}\n"
            new_text = f"---\n{frontmatter}---\n{body}"
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")

    if missing_files:
        print("WARNING: entries in INDEX.md with no matching file on disk:")
        for f in missing_files:
            print(f"  - {f}")

    # Regenerate INDEX.md, grouped by platform
    by_platform = defaultdict(list)
    for title, filename, platform in entries:
        by_platform[platform].append((title, filename))

    out = ["# Master Index", "",
           "Index này được phân nhóm theo nền tảng trong hệ sinh thái Claude "
           "(CLI / Desktop / VS Code / JetBrains / Web / Agent SDK / nhà cung cấp doanh nghiệp / tích hợp / dùng chung).",
           "Mục đầu tiên là bảng đối chiếu chính thức - luôn tra ở đó TRƯỚC khi hỏi \"nền tảng X có tính năng Y không\".",
           ""]
    for platform in SECTION_ORDER:
        items = by_platform.get(platform)
        if not items:
            continue
        out.append(f"## {SECTION_TITLES[platform]}")
        out.append("")
        for title, filename in items:
            out.append(f"- [{title}](concepts/{filename})")
        out.append("")

    INDEX_PATH.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")

    print("\nDone. Entry counts by platform:")
    for platform in SECTION_ORDER:
        if platform in counts:
            print(f"  {platform}: {counts[platform]}")
    print(f"Total entries: {sum(counts.values())}")


if __name__ == "__main__":
    main()
