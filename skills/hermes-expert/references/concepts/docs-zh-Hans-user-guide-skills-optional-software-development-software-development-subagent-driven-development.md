# Subagent Driven Development — Execute plans via delegate_task subagents (2-stage review) | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/software-development/software-development-subagent-driven-development](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/software-development/software-development-subagent-driven-development)

本页总览

Execute plans via delegate\_task subagents (2-stage review).

## Skill metadata[​](#skill-metadata "Skill metadata的直接链接")

|  |  |
| --- | --- |
| Source | Optional — install with `hermes skills install official/software-development/subagent-driven-development` |
| Path | `optional-skills/software-development/subagent-driven-development` |
| Version | `1.1.0` |
| Author | Hermes Agent (adapted from obra/superpowers) |
| License | MIT |
| Platforms | linux, macos, windows |
| Tags | `delegation`, `subagent`, `implementation`, `workflow`, `parallel` |
| Related skills | [`plan`](/docs/zh-Hans/docs/user-guide/skills/bundled/software-development/software-development-plan), [`requesting-code-review`](/docs/zh-Hans/docs/user-guide/skills/bundled/software-development/software-development-requesting-code-review), [`test-driven-development`](/docs/zh-Hans/docs/user-guide/skills/bundled/software-development/software-development-test-driven-development) |

## Reference: full SKILL.md[​](#reference-full-skillmd "Reference: full SKILL.md的直接链接")

信息

The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.

# Subagent-Driven Development

## Overview[​](#overview "Overview的直接链接")

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use[​](#when-to-use "When to Use的直接链接")

Use this skill when:

* You have an implementation plan (from the `plan` skill or user requirements)
* Tasks are mostly independent
* Quality and spec compliance are important
* You want automated review between tasks

**vs. manual execution:**

* Fresh context per task (no confusion from accumulated state)
* Automated review process catches issues early
* Consistent quality checks across all tasks
* Subagents can ask questions before starting work

## The Process[​](#the-process "The Process的直接链接")

### 1. Read and Parse Plan[​](#1-read-and-parse-plan "1. Read and Parse Plan的直接链接")

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```
# Read the plan  
read_file("docs/plans/feature-plan.md")  
  
# Create todo list with all tasks  
todo([  
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},  
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},  
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},  
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow[​](#2-per-task-workflow "2. Per-Task Workflow的直接链接")

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent[​](#step-1-dispatch-implementer-subagent "Step 1: Dispatch Implementer Subagent的直接链接")

Use `delegate_task` with complete context:

```
delegate_task(  
    goal="Implement Task 1: Create User model with email and password_hash fields",  
    context="""  
    TASK FROM PLAN:  
    - Create: src/models/user.py  
    - Add User class with email (str) and password_hash (str) fields  
    - Use bcrypt for password hashing  
    - Include __repr__ for debugging  
  
    FOLLOW TDD:  
    1. Write failing test in tests/models/test_user.py  
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)  
    3. Write minimal implementation  
    4. Run: pytest tests/models/test_user.py -v (verify PASS)  
    5. Run: pytest tests/ -q (verify no regressions)  
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"  
  
    PROJECT CONTEXT:  
    - Python 3.11, Flask app in src/app.py  
    - Existing models in src/models/  
    - Tests use pytest, run from project root  
    - bcrypt already in requirements.txt  
    """,  
    toolsets=['terminal', 'file']  
)
```

#### Step 2: Dispatch Spec Compliance Reviewer[​](#step-2-dispatch-spec-compliance-reviewer "Step 2: Dispatch Spec Compliance Reviewer的直接链接")

After the implementer completes, verify against the original spec:

```
delegate_task(  
    goal="Review if implementation matches the spec from the plan",  
    context="""  
    ORIGINAL TASK SPEC:  
    - Create src/models/user.py with User class  
    - Fields: email (str), password_hash (str)  
    - Use bcrypt for password hashing  
    - Include __repr__  
  
    CHECK:  
    - [ ] All requirements from spec implemented?  
    - [ ] File paths match spec?  
    - [ ] Function signatures match spec?  
    - [ ] Behavior matches expected?  
    - [ ] Nothing extra added (no scope creep)?  
  
    OUTPUT: PASS or list of specific spec gaps to fix.  
    """,  
    toolsets=['file']  
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer[​](#step-3-dispatch-code-quality-reviewer "Step 3: Dispatch Code Quality Reviewer的直接链接")

After spec compliance passes:

```
delegate_task(  
    goal="Review code quality for Task 1 implementation",  
    context="""  
    FILES TO REVIEW:  
    - src/models/user.py  
    - tests/models/test_user.py  
  
    CHECK:  
    - [ ] Follows project conventions and style?  
    - [ ] Proper error handling?  
    - [ ] Clear variable/function names?  
    - [ ] Adequate test coverage?  
    - [ ] No obvious bugs or missed edge cases?  
    - [ ] No security issues?  
  
    OUTPUT FORMAT:  
    - Critical Issues: [must fix before proceeding]  
    - Important Issues: [should fix]  
    - Minor Issues: [optional]  
    - Verdict: APPROVED or REQUEST_CHANGES  
    """,  
    toolsets=['file']  
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete[​](#step-4-mark-complete "Step 4: Mark Complete的直接链接")

```
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review[​](#3-final-review "3. Final Review的直接链接")

After ALL tasks are complete, dispatch a final integration reviewer:

```
delegate_task(  
    goal="Review the entire implementation for consistency and integration issues",  
    context="""  
    All tasks from the plan are complete. Review the full implementation:  
    - Do all components work together?  
    - Any inconsistencies between tasks?  
    - All tests passing?  
    - Ready for merge?  
    """,  
    toolsets=['terminal', 'file']  
)
```

### 4. Verify and Commit[​](#4-verify-and-commit "4. Verify and Commit的直接链接")

```
# Run full test suite  
pytest tests/ -q  
  
# Review all changes  
git diff --stat  
  
# Final commit if needed  
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity[​](#task-granularity "Task Granularity的直接链接")

**Each task = 2-5 minutes of focused work.**

**Too big:**

* "Implement user authentication system"

**Right size:**

* "Create User model with email and password fields"
* "Add password hashing function"
* "Create login endpoint"
* "Add JWT token generation"
* "Create registration endpoint"

## Red Flags — Never Do These[​](#red-flags--never-do-these "Red Flags — Never Do These的直接链接")

* Start implementation without a plan
* Skip reviews (spec compliance OR code quality)
* Proceed with unfixed critical/important issues
* Dispatch multiple implementation subagents for tasks that touch the same files
* Make subagent read the plan file (provide full text in context instead)
* Skip scene-setting context (subagent needs to understand where the task fits)
* Ignore subagent questions (answer before letting them proceed)
* Accept "close enough" on spec compliance
* Skip review loops (reviewer found issues → implementer fixes → review again)
* Let implementer self-review replace actual review (both are needed)
* **Start code quality review before spec compliance is PASS** (wrong order)
* Move to next task while either review has open issues

## Handling Issues[​](#handling-issues "Handling Issues的直接链接")

### If Subagent Asks Questions[​](#if-subagent-asks-questions "If Subagent Asks Questions的直接链接")

* Answer clearly and completely
* Provide additional context if needed
* Don't rush them into implementation

### If Reviewer Finds Issues[​](#if-reviewer-finds-issues "If Reviewer Finds Issues的直接链接")

* Implementer subagent (or a new one) fixes them
* Reviewer reviews again
* Repeat until approved
* Don't skip the re-review

### If Subagent Fails a Task[​](#if-subagent-fails-a-task "If Subagent Fails a Task的直接链接")

* Dispatch a new fix subagent with specific instructions about what went wrong
* Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes[​](#efficiency-notes "Efficiency Notes的直接链接")

**Why fresh subagent per task:**

* Prevents context pollution from accumulated state
* Each subagent gets clean, focused context
* No confusion from prior tasks' code or reasoning

**Why two-stage review:**

* Spec review catches under/over-building early
* Quality review ensures the implementation is well-built
* Catches issues before they compound across tasks

**Cost trade-off:**

* More subagent invocations (implementer + 2 reviewers per task)
* But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills[​](#integration-with-other-skills "Integration with Other Skills的直接链接")

### With plan[​](#with-plan "With plan的直接链接")

This skill EXECUTES plans created by the `plan` skill:

1. User requirements → plan → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development[​](#with-test-driven-development "With test-driven-development的直接链接")

Implementer subagents should follow TDD:

1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review[​](#with-requesting-code-review "With requesting-code-review的直接链接")

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging[​](#with-systematic-debugging "With systematic-debugging的直接链接")

If a subagent encounters bugs during implementation:

1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow[​](#example-workflow "Example Workflow的直接链接")

```
[Read plan: docs/plans/auth-feature.md]  
[Create todo list with 5 tasks]  
  
--- Task 1: Create User model ---  
[Dispatch implementer subagent]  
  Implementer: "Should email be unique?"  
  You: "Yes, email must be unique"  
  Implementer: Implemented, 3/3 tests passing, committed.  
  
[Dispatch spec reviewer]  
  Spec reviewer: ✅ PASS — all requirements met  
  
[Dispatch quality reviewer]  
  Quality reviewer: ✅ APPROVED — clean code, good tests  
  
[Mark Task 1 complete]  
  
--- Task 2: Password hashing ---  
[Dispatch implementer subagent]  
  Implementer: No questions, implemented, 5/5 tests passing.  
  
[Dispatch spec reviewer]  
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")  
  
[Implementer fixes]  
  Implementer: Added validation, 7/7 tests passing.  
  
[Dispatch spec reviewer again]  
  Spec reviewer: ✅ PASS  
  
[Dispatch quality reviewer]  
  Quality reviewer: Important: Magic number 8, extract to constant  
  Implementer: Extracted MIN_PASSWORD_LENGTH constant  
  Quality reviewer: ✅ APPROVED  
  
[Mark Task 2 complete]  
  
... (continue for all tasks)  
  
[After all tasks: dispatch final integration reviewer]  
[Run full test suite: all passing]  
[Done!]
```

## Remember[​](#remember "Remember的直接链接")

```
Fresh subagent per task  
Two-stage review every time  
Spec compliance FIRST  
Code quality SECOND  
Never skip reviews  
Catch issues early
```

**Quality is not an accident. It's the result of systematic process.**

## Further reading (load when relevant)[​](#further-reading-load-when-relevant "Further reading (load when relevant)的直接链接")

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

* **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
* **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.

Both references adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).

* [Skill metadata](#skill-metadata)
* [Reference: full SKILL.md](#reference-full-skillmd)
* [Overview](#overview)
* [When to Use](#when-to-use)
* [The Process](#the-process)
  + [1. Read and Parse Plan](#1-read-and-parse-plan)
  + [2. Per-Task Workflow](#2-per-task-workflow)
  + [3. Final Review](#3-final-review)
  + [4. Verify and Commit](#4-verify-and-commit)
* [Task Granularity](#task-granularity)
* [Red Flags — Never Do These](#red-flags--never-do-these)
* [Handling Issues](#handling-issues)
  + [If Subagent Asks Questions](#if-subagent-asks-questions)
  + [If Reviewer Finds Issues](#if-reviewer-finds-issues)
  + [If Subagent Fails a Task](#if-subagent-fails-a-task)
* [Efficiency Notes](#efficiency-notes)
* [Integration with Other Skills](#integration-with-other-skills)
  + [With plan](#with-plan)
  + [With test-driven-development](#with-test-driven-development)
  + [With requesting-code-review](#with-requesting-code-review)
  + [With systematic-debugging](#with-systematic-debugging)
* [Example Workflow](#example-workflow)
* [Remember](#remember)
* [Further reading (load when relevant)](#further-reading-load-when-relevant)