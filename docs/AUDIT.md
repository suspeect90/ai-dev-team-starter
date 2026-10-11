# Initial audit — 2026-10-11

Source: private repository suspeect90/ai-dev-team-starter, main commit b1d4fffffabaffdf2099ce01f649c60c52003b41. All 32 original tracked files were fetched by exact revision and inspected, including nine agent TOMLs, seven skills, workflow, validator/tests, docs and optional stack profiles. An independent architect read all 32 files.

Git clone failed in the restricted shell with a getaddrinfo thread error. The connected GitHub tools supplied the exact files and commit metadata. Blob/tree/commit hashes were verified and restored into a shallow local Git checkout rooted at the original commit; no fabricated baseline was substituted.

## Baseline results

- python scripts/validate.py: exit 0.
- python -m unittest discover -s tests -v: 3 tests passed.
- Latest existing GitHub Actions run: [38101172427](https://github.com/suspeect90/ai-dev-team-starter/actions/runs/38101172427), success for the source commit, observed through GitHub.
- Repository API returned is_template: true and private: true. Template activation was already complete.

## Reproduced defects and corrections

| Finding | Observed baseline behavior | Correction |
| --- | --- | --- |
| agents = [] | AttributeError in validator | Check table types before .get |
| agent name as array | TypeError adding to set | Validate string before set operations |
| Skill frontmatter lacks closing delimiter and has empty description | Accepted as valid | Parse closed flat metadata block; nonempty strings/body |
| Sandbox modes not checked per role | Structural acceptance contradicted role responsibilities | Verify reviewer/read-only and writer contracts |
| Missing negative regression coverage | Three mostly positive checks | Isolated malformed-input, CLI and symlink regression cases |
| Tech Lead/DevOps/QA default read-only | Cannot fully carry out assigned integration/CI/test writes in clients honoring defaults | workspace-write with exclusive ownership and action limits |
| Short skills lack explicit validation/output contracts | Generic procedures and weak handoff | Improve seven existing skills without adding duplicates |
| Ambiguous plain YAML scalars | Invalid syntax/numeric metadata accepted in first correction | Strict documented scalar subset and quoted-value regression cases |
| Whole-repository fixtures | Could follow external links and copy application/dependency/data trees | Minimal infrastructure snapshot; resolve containment before each source read/enumeration |
| Sparse onboarding | No practical recovery/project switching/full orchestration exercise | Add operating guides and isolated test procedure |
| Mutable action tags and single-platform validation | No immutable action identity or portability matrix | Verified SHA pins, bounded CI and four combinations |

The standalone .codex/agents TOML format, agents.enabled, max_concurrent_threads_per_session and .agents/skills placement already matched current official documentation. They were retained. The limit excludes the parent on compatible Codex clients; this chat has a lower host cap of four total agents.

The brief is intentionally empty for future projects. No application code or application tests were expected or added. Optional stack profiles remain optional.

## Official sources actually consulted

- [Native subagents and standalone custom agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Skill locations and discovery](https://learn.chatgpt.com/docs/build-skills)
- [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [GitHub template option](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)

## Evidence boundaries

Static checks do not establish native discovery, agent launch or enforced access isolation. Codex CLI 0.162.0-alpha.17.2 was observed locally. debug prompt-input and app-server initialization failed with filesystem access denied; automatic local discovery is therefore unverified. Native collaboration tools in this chat are separately exercised with explicitly read role/skill contracts. See VERIFICATION.md for the execution results and limitations.
