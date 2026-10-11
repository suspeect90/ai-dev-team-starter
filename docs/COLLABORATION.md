# Native multi-agent collaboration

The primary agent coordinates the task. Nine specialists are available as project-scoped standalone TOML definitions; they are selected as needed, not all started for every request.

| Role | Responsibility | Default sandbox |
| --- | --- | --- |
| tech_lead | Scoped coordination and integration | workspace-write |
| architect | Architecture and contracts | read-only |
| backend | Server/API implementation | workspace-write |
| frontend | UI implementation | workspace-write |
| database | Schema, migration and query work | workspace-write |
| security | Independent vulnerability review | read-only |
| qa | Independent tests and verification | workspace-write |
| devops | Assigned CI/development infrastructure | workspace-write |
| designer | UI/UX specifications and review | read-only |

## Task contract and sequence

For each delegated task, record role, native handle, input revision, prerequisites, allowed read scope, **exclusive write paths**, acceptance criteria, expected output and check commands. Keep this small task ledger in the conversation or the project's existing planning document; no additional service is needed.

Example: architect defines a contract first. Backend and frontend then implement agreed interfaces in disjoint paths. Database migration work precedes tests that depend on that schema. Once integration is stable, security and independent code/QA reviews can run in parallel. The author fixes findings, then the Tech Lead verifies the final integrated revision.

For significant changes, use an architect or QA agent that did not author the implementation for independent code review. Security contributes a distinct security review. QA may write assigned tests but must not alter application code to satisfy them.

## File conflicts and worktrees

Never assign the same file to concurrent writers. Shared manifests, lockfiles, API specifications and fixtures have one owner; serialize changes to them. Pause/reassign a task before changing its ownership. Read-only reviewers inspect a stable revision.

For long independent tasks, separate branches/worktrees are useful when the repository supports them. Use disjoint paths even across worktrees; worktrees isolate checkouts but do not remove semantic conflicts. Integrate one reviewed commit at a time, resolve conflicts with the owning specialist, then test the combined result.

Use the available native worktree tools or standard Git commands. Preserve dirty/user work and never force-push or reset away work to resolve a conflict.

## Capacity and permissions

The configured limit is four open spawned threads **excluding the primary**. Runtime policies, account access and host limits may reduce this. During the 2026-10-11 test, this chat allowed four agents total (primary plus at most three children). Completed children may still occupy open-thread capacity in some clients; use supported lifecycle tools and wait for results.

A TOML sandbox is a default configuration layer. Runtime permission choices can override it, so do not treat prompt ownership or the TOML as proof of access isolation. QA/DevOps/Tech Lead need workspace writes for their assigned tests/configuration/integration; security/architect/designer are intended as read-only.

Use native named roles when supported. This chat exposes native task-based spawn/message/wait tools but no named TOML-role selector, so its tests explicitly load the repository instructions into real subagents. That proves execution and handoff in this mode, not automatic TOML discovery or sandbox enforcement.

## Results and recovery

A specialist returns changed files, exact commands/results, findings, remaining risks and blockers. The primary confirms completion from native handles, checks the actual diff, integrates and validates. No production deployment follows automatically.

On interruption: inspect native agent status, ask still-running tasks for progress, confirm ownership, inspect the dirty worktree and last test evidence, and resume at the first unmet prerequisite. Never launch a duplicate writer against an unfinished task.
