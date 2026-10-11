---
name: planning
description: Plan substantial repository changes and native specialist delegation with dependencies and acceptance criteria.
---

# Planning

## Purpose

Produce an actionable plan aligned with the user's scope and the repository's actual capabilities.

## When to use

Use for substantial multi-file work, architecture decisions or specialist coordination. A trivial edit does not need a full plan.

## Method

1. Read the request, AGENTS.md, project brief and affected code/toolchain. Separate known requirements from assumptions and missing decisions.
2. Define outcomes, exclusions, invariants, acceptance criteria and significant risks. Preserve existing user authorization.
3. Split work into milestones with prerequisites. Specify the smallest relevant specialists, exclusive file ownership or worktrees, and the evidence each task must return.
4. Delegate independent tasks using available native tools; sequence dependent changes after their inputs are ready. Treat runtime capacity as a ceiling, not a target.
5. Choose verification commands from installed tooling. Identify integration order, recovery needs and human decisions before irreversible actions.

## Validation

Every task has a bounded scope, dependencies, an owner and observable acceptance criteria. Shared-file edits are serialized. Runtime limitations and unresolved decisions are explicit.

## Expected result

A concise development plan, dependency/ownership table, verification strategy and decision list that the Tech Lead can execute.
