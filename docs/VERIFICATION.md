# Verification evidence — 2026-10-11

This record separates structural checks, real agent execution and unverified native discovery. It does not certify all nine roles or future applications.

## Environment and baseline

- Windows host; bundled Python 3.12 used by the primary/technical agent. The independent reviewer also executed the suite using local Python 3.13.5.
- Codex CLI observed: 0.162.0-alpha.17.2.
- Source revision: b1d4fffffabaffdf2099ce01f649c60c52003b41.
- Baseline validator: exit 0; existing suite: 3 tests passed.
- Existing GitHub Actions [run 38101172427](https://github.com/suspeect90/ai-dev-team-starter/actions/runs/38101172427): success for that source revision.
- GitHub repository metadata: private, is_template true. No permanent test repository created.

## Real native delegation

Native tasks confirmed by the chat's collaboration tools:

| Handle | Work | Ownership and observed result |
| --- | --- | --- |
| /root/audit_architect | Full independent audit, then smoke architecture contract | Read-only; all 32 original files read; contract returned before implementation |
| /root/validator_engineer | Validator correction, then smoke backend | Assigned files only; artifact_path.py delivered after architect contract; 7 valid, 11 invalid, 4 wrong-type direct checks passed |
| /root/security_reviewer | Independent infrastructure and smoke security review | No writes; 15 valid, 39 invalid, 6 wrong-type checks passed; lexical scope explicit |
| /root/qa_verifier | Independent smoke acceptance tests | Separate test file; 18 tests and 2,699 subTest cases passed, zero failures/skips; primary rerun confirmed |
| /root | Tech Lead orchestration | Native dispatch/status/result collection, file ownership, review fixes, final verification and integration |

Architect preceded backend. Backend completed before security and QA, which ran independently in parallel on a stable implementation. No application or business feature was built.

The isolated function validates literal portable relative artifact paths without I/O; it rejects traversal, absolute paths, Windows reserved names, invalid Unicode/control characters and overlong segments/paths. It does not guarantee physical containment after symlink/junction resolution.

## Review and structural checks

The first corrected suite passed 32 tests without skips. Independent code/security reviewers found additional issues before publication: ambiguous plain YAML values, incomplete required guide inventory, and whole-repository test fixtures following links/copying application data. The final correction rejects ambiguous/invalid plain scalars, requires the new guides and uses confined minimal fixtures; its final execution is recorded below.

Smoke QA command: python -B -m unittest -v test_artifact_path in the isolated workspace. The independent QA run passed 18 tests and 2,699 subTest cases, zero failures/errors/skips; the primary rerun also passed (1.066s). Coverage included all 65 Cc, 170 Cf and 2,048 Cs characters, reserved DOS names, UTF-8 boundaries and common I/O guards.

SHA-256 evidence before cleanup:
- artifact_path.py: 7595451dcc2c49cdd647941a8fa5a1a0e537a8cedecea84992caa801e8807961
- test_artifact_path.py: fde4a43aca6c32800c3c8a462d37db7114da843bf22d2f7c937ac21423011a4e
- CONTRACT.md: 739529421d78aca76dab703537f0d98efcab38b04be20d9b4b428fcd9f0f0b53

Final corrected infrastructure suite: 37 tests passed, zero failures/skips, as executed by the technical agent using bundled Python 3.12.14. Validator exit 0 and git diff --check passed. Primary verification before publication: python -B scripts/validate.py exited 0; python -B -m unittest discover -s tests -v passed all 37 tests, zero failures/skips (27.980s); git diff --check exited 0. Independent reviewers confirmed their findings resolved. Candidate PR CI is reported separately in the PR and final report for its exact head revision; the baseline run alone does not establish that result.

## Limits observed

1. This chat exposes native task-based collaboration, without a custom TOML named-role selector. Specialists explicitly read their repository role/skill instructions. Real execution is established in that mode; automatic TOML role selection and application of role sandbox layers are not established.
2. The chat permits four active agents total, including the primary. The repository config requests four spawned child threads excluding the primary on compatible clients; the host limit remains authoritative.
3. Local CLI debug prompt-input and a bounded app-server initialize/skills-list probe both failed with filesystem access denied before initialization. Native automatic local role/skill discovery is therefore unverified, not reported as successful.
4. The skill-creator quick_validate.py invocation failed because PyYAML is absent from the bundled Python. The repository's standard-library flat-frontmatter checks are executed instead; the upstream YAML validator is not claimed to pass.
5. Only the tested technical/backend, architect, security and QA chain has live behavioral evidence. Frontend, database, designer, DevOps and delegated tech_lead have structural/contract review, not separate live role exercises.
6. Local tests do not establish Linux or Python 3.11 execution; those results must come from the PR's exact GitHub Actions run. A successful source-commit run is not a successful candidate run.

The temporary test files are removed after verification; their sanitized result and hashes are retained here. No temporary test application is tracked in this repository. A narrowly scoped private-key/token-pattern scan returned no matching files; this is not a comprehensive secret audit.

## Reproduce in a target project

Follow START_HERE.md and SMOKE_TEST.md in a trusted target checkout. Confirm the actual client role/skill list, runtime cap and sandbox policy, then run the isolated native scenario before treating automatic custom-role loading as verified.
