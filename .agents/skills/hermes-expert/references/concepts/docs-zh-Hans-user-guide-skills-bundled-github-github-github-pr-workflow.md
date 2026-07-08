# Github Pr Workflow — GitHub PR 生命周期：分支、提交、开启、CI、合并 | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/github/github-github-pr-workflow](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/github/github-github-pr-workflow)

本页总览

GitHub PR 生命周期：分支、提交、开启、CI、合并。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 内置（默认安装） |
| 路径 | `skills/github/github-pr-workflow` |
| 版本 | `1.1.0` |
| 作者 | Hermes Agent |
| 许可证 | MIT |
| 平台 | linux, macos, windows |
| 标签 | `GitHub`, `Pull-Requests`, `CI/CD`, `Git`, `Automation`, `Merge` |
| 相关 skill | [`github-auth`](/docs/zh-Hans/user-guide/skills/bundled/github/github-github-auth), [`github-code-review`](/docs/zh-Hans/user-guide/skills/bundled/github/github-github-code-review) |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# GitHub Pull Request 工作流

管理 PR 生命周期的完整指南。每个章节优先展示 `gh` 方式，再给出适用于无 `gh` 环境的 `git` + `curl` 备用方案。

## 前提条件[​](#前提条件 "前提条件的直接链接")

* 已通过 GitHub 认证（参见 `github-auth` skill）
* 位于含有 GitHub 远程仓库的 git 仓库中

### 快速认证检测[​](#快速认证检测 "快速认证检测的直接链接")

```
# Determine which method to use throughout this workflow  
if command -v gh &>/dev/null && gh auth status &>/dev/null; then  
  AUTH="gh"  
else  
  AUTH="git"  
  # Ensure we have a token for API calls  
  if [ -z "$GITHUB_TOKEN" ]; then  
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then  
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')  
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then  
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')  
    fi  
  fi  
fi  
echo "Using: $AUTH"
```

### 从 Git 远程地址提取 Owner/Repo[​](#从-git-远程地址提取-ownerrepo "从 Git 远程地址提取 Owner/Repo的直接链接")

许多 `curl` 命令需要 `owner/repo`。从 git 远程地址中提取：

```
# Works for both HTTPS and SSH remote URLs  
REMOTE_URL=$(git remote get-url origin)  
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')  
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)  
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)  
echo "Owner: $OWNER, Repo: $REPO"
```

---

## 1. 创建分支[​](#1-创建分支 "1. 创建分支的直接链接")

此部分为纯 `git` 操作——两种方式完全相同：

```
# Make sure you're up to date  
git fetch origin  
git checkout main && git pull origin main  
  
# Create and switch to a new branch  
git checkout -b feat/add-user-authentication
```

分支命名规范：

* `feat/description` — 新功能
* `fix/description` — 缺陷修复
* `refactor/description` — 代码重构
* `docs/description` — 文档
* `ci/description` — CI/CD 变更

## 2. 提交变更[​](#2-提交变更 "2. 提交变更的直接链接")

使用 agent 的文件工具（`write_file`、`patch`）进行修改，然后提交：

```
# Stage specific files  
git add src/auth.py src/models/user.py tests/test_auth.py  
  
# Commit with a conventional commit message  
git commit -m "feat: add JWT-based user authentication  
  
- Add login/register endpoints  
- Add User model with password hashing  
- Add auth middleware for protected routes  
- Add unit tests for auth flow"
```

提交信息格式（Conventional Commits）：

```
type(scope): short description  
  
Longer explanation if needed. Wrap at 72 characters.
```

类型：`feat`、`fix`、`refactor`、`docs`、`test`、`ci`、`chore`、`perf`

## 3. 推送分支并创建 PR[​](#3-推送分支并创建-pr "3. 推送分支并创建 PR的直接链接")

### 推送分支（两种方式相同）[​](#推送分支两种方式相同 "推送分支（两种方式相同）的直接链接")

```
git push -u origin HEAD
```

### 创建 PR[​](#创建-pr "创建 PR的直接链接")

**使用 gh：**

```
gh pr create \  
  --title "feat: add JWT-based user authentication" \  
  --body "## Summary  
- Adds login and register API endpoints  
- JWT token generation and validation  
  
## Test Plan  
- [ ] Unit tests pass  
  
Closes #42"
```

选项：`--draft`、`--reviewer user1,user2`、`--label "enhancement"`、`--base develop`

**使用 git + curl：**

```
BRANCH=$(git branch --show-current)  
  
curl -s -X POST \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  -H "Accept: application/vnd.github.v3+json" \  
  https://api.github.com/repos/$OWNER/$REPO/pulls \  
  -d "{  
    \"title\": \"feat: add JWT-based user authentication\",  
    \"body\": \"## Summary\nAdds login and register API endpoints.\n\nCloses #42\",  
    \"head\": \"$BRANCH\",  
    \"base\": \"main\"  
  }"
```

响应 JSON 中包含 PR 的 `number`——请保存以供后续命令使用。

若要创建草稿 PR，在 JSON body 中添加 `"draft": true`。

## 4. 监控 CI 状态[​](#4-监控-ci-状态 "4. 监控 CI 状态的直接链接")

### 检查 CI 状态[​](#检查-ci-状态 "检查 CI 状态的直接链接")

**使用 gh：**

```
# One-shot check  
gh pr checks  
  
# Watch until all checks finish (polls every 10s)  
gh pr checks --watch
```

**使用 git + curl：**

```
# Get the latest commit SHA on the current branch  
SHA=$(git rev-parse HEAD)  
  
# Query the combined status  
curl -s \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \  
  | python3 -c "  
import sys, json  
data = json.load(sys.stdin)  
print(f\"Overall: {data['state']}\")  
for s in data.get('statuses', []):  
    print(f\"  {s['context']}: {s['state']} - {s.get('description', '')}\")"  
  
# Also check GitHub Actions check runs (separate endpoint)  
curl -s \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \  
  | python3 -c "  
import sys, json  
data = json.load(sys.stdin)  
for cr in data.get('check_runs', []):  
    print(f\"  {cr['name']}: {cr['status']} / {cr['conclusion'] or 'pending'}\")"
```

### 轮询直至完成（git + curl）[​](#轮询直至完成git--curl "轮询直至完成（git + curl）的直接链接")

```
# Simple polling loop — check every 30 seconds, up to 10 minutes  
SHA=$(git rev-parse HEAD)  
for i in $(seq 1 20); do  
  STATUS=$(curl -s \  
    -H "Authorization: token $GITHUB_TOKEN" \  
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \  
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")  
  echo "Check $i: $STATUS"  
  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] || [ "$STATUS" = "error" ]; then  
    break  
  fi  
  sleep 30  
done
```

## 5. 自动修复 CI 失败[​](#5-自动修复-ci-失败 "5. 自动修复 CI 失败的直接链接")

当 CI 失败时，进行诊断并修复。此循环适用于两种认证方式。

### 第一步：获取失败详情[​](#第一步获取失败详情 "第一步：获取失败详情的直接链接")

**使用 gh：**

```
# List recent workflow runs on this branch  
gh run list --branch $(git branch --show-current) --limit 5  
  
# View failed logs  
gh run view <RUN_ID> --log-failed
```

**使用 git + curl：**

```
BRANCH=$(git branch --show-current)  
  
# List workflow runs on this branch  
curl -s \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" \  
  | python3 -c "  
import sys, json  
runs = json.load(sys.stdin)['workflow_runs']  
for r in runs:  
    print(f\"Run {r['id']}: {r['name']} - {r['conclusion'] or r['status']}\")"  
  
# Get failed job logs (download as zip, extract, read)  
RUN_ID=<run_id>  
curl -s -L \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \  
  -o /tmp/ci-logs.zip  
cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
```

### 第二步：修复并推送[​](#第二步修复并推送 "第二步：修复并推送的直接链接")

定位问题后，使用文件工具（`patch`、`write_file`）进行修复：

```
git add <fixed_files>  
git commit -m "fix: resolve CI failure in <check_name>"  
git push
```

### 第三步：验证[​](#第三步验证 "第三步：验证的直接链接")

使用第 4 节中的命令重新检查 CI 状态。

### 自动修复循环模式[​](#自动修复循环模式 "自动修复循环模式的直接链接")

当被要求自动修复 CI 时，遵循以下循环：

1. 检查 CI 状态 → 识别失败项
2. 读取失败日志 → 理解错误原因
3. 使用 `read_file` + `patch`/`write_file` → 修复代码
4. `git add . && git commit -m "fix: ..." && git push`
5. 等待 CI → 重新检查状态
6. 若仍失败则重复（最多 3 次，之后询问用户）

## 6. 合并[​](#6-合并 "6. 合并的直接链接")

**使用 gh：**

```
# Squash merge + delete branch (cleanest for feature branches)  
gh pr merge --squash --delete-branch  
  
# Enable auto-merge (merges when all checks pass)  
gh pr merge --auto --squash --delete-branch
```

**使用 git + curl：**

```
PR_NUMBER=<number>  
  
# Merge the PR via API (squash)  
curl -s -X PUT \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \  
  -d "{  
    \"merge_method\": \"squash\",  
    \"commit_title\": \"feat: add user authentication (#$PR_NUMBER)\"  
  }"  
  
# Delete the remote branch after merge  
BRANCH=$(git branch --show-current)  
git push origin --delete $BRANCH  
  
# Switch back to main locally  
git checkout main && git pull origin main  
git branch -d $BRANCH
```

合并方式：`"merge"`（合并提交）、`"squash"`、`"rebase"`

### 启用自动合并（curl）[​](#启用自动合并curl "启用自动合并（curl）的直接链接")

```
# Auto-merge requires the repo to have it enabled in settings.  
# This uses the GraphQL API since REST doesn't support auto-merge.  
PR_NODE_ID=$(curl -s \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \  
  | python3 -c "import sys,json; print(json.load(sys.stdin)['node_id'])")  
  
curl -s -X POST \  
  -H "Authorization: token $GITHUB_TOKEN" \  
  https://api.github.com/graphql \  
  -d "{\"query\": \"mutation { enablePullRequestAutoMerge(input: {pullRequestId: \\\"$PR_NODE_ID\\\", mergeMethod: SQUASH}) { clientMutationId } }\"}"
```

## 7. 完整工作流示例[​](#7-完整工作流示例 "7. 完整工作流示例的直接链接")

```
# 1. Start from clean main  
git checkout main && git pull origin main  
  
# 2. Branch  
git checkout -b fix/login-redirect-bug  
  
# 3. (Agent makes code changes with file tools)  
  
# 4. Commit  
git add src/auth/login.py tests/test_login.py  
git commit -m "fix: correct redirect URL after login  
  
Preserves the ?next= parameter instead of always redirecting to /dashboard."  
  
# 5. Push  
git push -u origin HEAD  
  
# 6. Create PR (picks gh or curl based on what's available)  
# ... (see Section 3)  
  
# 7. Monitor CI (see Section 4)  
  
# 8. Merge when green (see Section 6)
```

## 常用 PR 命令参考[​](#常用-pr-命令参考 "常用 PR 命令参考的直接链接")

| 操作 | gh | git + curl |
| --- | --- | --- |
| 列出我的 PR | `gh pr list --author @me` | `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"` |
| 查看 PR diff | `gh pr diff` | `git diff main...HEAD`（本地）或 `curl -H "Accept: application/vnd.github.diff" ...` |
| 添加评论 | `gh pr comment N --body "..."` | `curl -X POST .../issues/N/comments -d '{"body":"..."}'` |
| 请求审查 | `gh pr edit N --add-reviewer user` | `curl -X POST .../pulls/N/requested_reviewers -d '{"reviewers":["user"]}'` |
| 关闭 PR | `gh pr close N` | `curl -X PATCH .../pulls/N -d '{"state":"closed"}'` |
| 检出他人的 PR | `gh pr checkout N` | `git fetch origin pull/N/head:pr-N && git checkout pr-N` |

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [前提条件](#前提条件)
  + [快速认证检测](#快速认证检测)
  + [从 Git 远程地址提取 Owner/Repo](#从-git-远程地址提取-ownerrepo)
* [1. 创建分支](#1-创建分支)
* [2. 提交变更](#2-提交变更)
* [3. 推送分支并创建 PR](#3-推送分支并创建-pr)
  + [推送分支（两种方式相同）](#推送分支两种方式相同)
  + [创建 PR](#创建-pr)
* [4. 监控 CI 状态](#4-监控-ci-状态)
  + [检查 CI 状态](#检查-ci-状态)
  + [轮询直至完成（git + curl）](#轮询直至完成git--curl)
* [5. 自动修复 CI 失败](#5-自动修复-ci-失败)
  + [第一步：获取失败详情](#第一步获取失败详情)
  + [第二步：修复并推送](#第二步修复并推送)
  + [第三步：验证](#第三步验证)
  + [自动修复循环模式](#自动修复循环模式)
* [6. 合并](#6-合并)
  + [启用自动合并（curl）](#启用自动合并curl)
* [7. 完整工作流示例](#7-完整工作流示例)
* [常用 PR 命令参考](#常用-pr-命令参考)

## Related Files
> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.

- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/github/github-github-auth](./docs-zh-Hans-user-guide-skills-bundled-github-github-github-auth.md)
- [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/github/github-github-code-review](./docs-zh-Hans-user-guide-skills-bundled-github-github-github-code-review.md)
