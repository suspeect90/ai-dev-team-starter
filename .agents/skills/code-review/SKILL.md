---
name: code-review
description: Review actual changes for correctness, regressions, security and missing tests.
---

# Code Review

1. Read the diff against the right base and inspect nearby code paths.
2. Check compatibility, input validation, authorization, concurrency, error handling and data integrity.
3. Identify concrete regressions with path and reproducible scenario.
4. Prioritize findings by severity; distinguish blockers and suggestions.
5. Do not assert tests were run without execution evidence.
