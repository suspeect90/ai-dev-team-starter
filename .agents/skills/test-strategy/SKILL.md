---
name: test-strategy
description: Design and execute meaningful acceptance and regression tests for a defined change.
---

# Test Strategy

## Purpose

Provide independent evidence that a change meets its contract and handles relevant failure modes.

## When to use

Use for QA assignments, significant features or regression-test planning. Match depth to risk and available tools.

## Method

1. Derive cases from acceptance criteria, invariants, permissions and failure modes rather than mirroring implementation details.
2. Put isolated logic in unit tests, real boundaries in integration tests and essential user journeys in end-to-end tests when those layers add confidence.
3. Cover relevant boundary inputs, invalid requests, authorization and concurrent/retry behavior. Choose deterministic isolated fixtures.
4. Inspect installed test tooling and execute the selected commands in approved environments. Own test paths explicitly; coordinate shared fixtures and dependency files.
5. Investigate failures and return reproduction details. After integration or a fix, rerun the affected checks on the final candidate revision.

## Validation

Evidence includes environment, exact commands and passed/failed/skipped counts. Planned, executed and unexecuted checks are distinguished; acceptance gaps remain visible.

## Expected result

A risk-based test plan, useful test changes where assigned, execution results and a readiness recommendation.
