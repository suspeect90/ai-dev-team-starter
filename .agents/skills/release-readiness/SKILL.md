---
name: release-readiness
description: Assess whether an exact release candidate is ready using observed checks and recovery evidence.
---

# Release Readiness

## Purpose

Give the human release owner a grounded go/no-go recommendation.

## When to use

Use before a release or when explicitly assessing readiness. The assessment alone does not authorize deployment.

## Method

1. Identify the candidate revision and summarize compatibility, migration and operational changes.
2. Inspect actual CI/check results for that revision and run missing permitted local checks that materially affect readiness. Report stale or unavailable results.
3. Assess applicable migration order, secret configuration, monitoring, backup/recovery and rollback evidence.
4. Confirm that independent review findings and acceptance gaps are resolved or explicitly accepted by the responsible human.
5. State go/no-go, remaining risks and the exact approvals/actions needed. Execute production deployment only when explicitly authorized for that target and candidate.

## Validation

The recommendation refers to the candidate that will ship; failures, skips, missing evidence and untested recovery paths are visible.

## Expected result

Release candidate, verification evidence, go/no-go rationale, recovery procedure and remaining decisions.
