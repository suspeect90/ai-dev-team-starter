---
name: systematic-debugging
description: Investigate a reproducible defect and verify its root cause before applying a focused fix.
---

# Systematic Debugging

## Purpose

Resolve the cause of an observed failure with a change whose behavior can be demonstrated.

## When to use

Use for bugs, unexpected behavior or failing checks. Do not invent a defect or add instrumentation when ordinary inspection already establishes the cause.

## Method

1. Record expected and observed behavior, relevant versions and the smallest reproducible input.
2. Inspect the responsible execution path and collect only the necessary sanitized evidence.
3. Form plausible hypotheses and use a discriminating check to rule them in or out; record the result.
4. Apply the smallest coherent fix within assigned ownership after the cause is established. Add a regression test when it provides lasting protection.
5. Rerun the original reproduction and relevant tests. If investigation is blocked by permissions, dependencies or environment differences, return the blocker with a precise next step.

## Validation

The original failure is observed or explicitly marked unreproduced; the proposed cause explains the evidence, and the fix is verified against the original trigger without hiding failures.

## Expected result

Root cause, focused change, reproduction commands, before/after results and any unresolved environmental uncertainty.
