# Real isolated orchestration test

This procedure exercises native delegation without creating an application or a permanent test repository. Static validation and a read-only conversation are not substitutes.

## Prepare

Use a temporary directory outside the tracked project files but inside an approved writable workspace. Record the actual runtime, branch/revision, role selection mode and capacity. Never copy credentials or production data.

Ask the primary Tech Lead to perform this mission:

> Run a real native multi-agent test in an isolated temporary workspace. Have architect define a contract for a pure Python function that validates portable relative artifact paths. Have backend implement it only in its assigned module. Once complete, independently ask security to review it read-only and QA to write/run acceptance tests in its own test file. Run security and QA concurrently when capacity allows. Review findings, assign any fix to backend, then rerun affected tests and synthesize the observed results. Load the repository role instructions and relevant skills. Do not claim automatic TOML role selection unless the native interface confirms it. Do not develop business code or access production.

## Contract and ownership

The function performs no I/O. Accept relative POSIX paths with ordinary names/spaces; reject traversal, absolute/drive/UNC paths, empty segments, control characters, Windows reserved names/characters, URLs and trailing dot/space segments. State length/type rules. Lexical validation does not prove containment after resolving symlinks.

Architect: contract only. Backend: implementation module only. QA: independent test file only. Security: no writes. Parent: integration/checks and evidence.

The flow must show architect completion before backend, then backend completion before security/QA. Record native handles and actual returned results. Observe real test execution, failures and reruns, not just a narrative.

## Evidence and cleanup

Retain a sanitized summary of roles, handles, input contracts, ownership, commands, counts, findings, fixes and limits. Verify that only assigned files changed and that production/business files were untouched.

After all agents complete, export useful evidence and delete only the verified temporary test directory inside the approved workspace. For a Git worktree use its native archive/removal mechanism; preserve needed commits first.

If the runtime lacks native spawning, named-role selection or discovery, record the exact limitation. Sequential work may still be useful but cannot be reported as a successful multi-agent test. Review-only agents sharing a writable sandbox are not proof of enforced read-only isolation.
