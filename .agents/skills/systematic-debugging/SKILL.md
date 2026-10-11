---
name: systematic-debugging
description: Reproduce bugs and prove their root cause before changing code.
---

# Systematic Debugging

1. Document observed behavior, expected behavior, environment and reproduction steps.
2. Collect narrow logs and trace the responsible code without leaking credentials.
3. Form competing hypotheses and test the cheapest discriminating checks.
4. Fix the actual root cause with the smallest defensible change.
5. Add a regression test where practical; rerun reproduction and report outcomes.
