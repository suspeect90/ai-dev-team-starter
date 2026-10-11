---
name: database-change
description: Plan and verify schema, migration or data-access changes for the project's actual database engine.
---

# Database Change

## Purpose

Maintain data integrity and compatibility while evolving storage or improving a measured query.

## When to use

Use for schema/migration changes, backfills, constraints or query optimization. Inspect the chosen engine rather than assuming PostgreSQL or relational storage.

## Method

1. Read the current schema, engine/version, migration history, consumers and representative query patterns.
2. Identify integrity invariants, compatibility windows, expected volume and concurrent writers. Prefer additive changes when possible.
3. Define migration/backfill order and evaluate locks, retries, index behavior and recovery. Separate long backfills when that reduces risk.
4. Validate against isolated representative fixtures; check constraints and both old/new consumer compatibility where required. Measure query plans or engine-equivalent diagnostics before claiming a speedup.
5. Return commands, data/recovery implications and execution evidence. Prepare destructive changes for review and obtain human authorization before running them or changing production data.

## Validation

The migration preserves stated invariants, has a tested or explicitly untested recovery procedure, and lists assumptions about backups, volume and engine behavior.

## Expected result

Assigned schema/query changes, rollout and recovery plan, test/measurement results and required human decisions.
