---
name: code-review
description: Independently review an actual diff for correctness, regressions and missing verification.
---

# Code Review

## Purpose

Find actionable defects in the proposed change before integration or release.

## When to use

Use for substantive changes or an explicit code-review request. Inspect the requested revision and base; do not treat style preferences as defects.

## Method

1. Identify the exact base and candidate revision. Read the diff and nearby callers, contracts and tests.
2. Trace changed behavior for compatibility, validation, authorization, error recovery, concurrency and data integrity relevant to the change.
3. For each issue, establish a concrete trigger and explain why the changed code causes the failure. Reference the affected file/location.
4. Check whether existing tests exercise the risky behavior. Run narrowly useful checks when permitted and distinguish observed execution from proposed tests.
5. Return prioritized findings to the author or Tech Lead. Review fixes against the same contract; do not edit the implementation while acting as its independent reviewer.

## Validation

Findings are supported by code or execution evidence and include impact and remediation. Scope, revision and untested paths are reported; a clean review is limited to what was inspected.

## Expected result

Prioritized actionable findings or a scoped no-findings result, plus exact verification evidence and remaining test gaps.
