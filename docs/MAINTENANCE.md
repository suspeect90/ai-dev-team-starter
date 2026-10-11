# Maintaining the team template

GitHub templates create snapshots, not automatically synchronized descendants. VERSION records the team contract version independently of the application version.

## Version and update policy

Use semantic versions: patch for compatible corrections, minor for compatible capabilities/procedures, major for breaking role names, contracts or paths. Update VERSION and CHANGELOG.md together and include migration notes where behavior changes.

Maintain a branch/PR for changes to agents, skills, validation and workflows. Run structural validation, negative regression tests and a real isolated delegation test for substantial changes. Inspect CI for the exact candidate revision before merging.

## Derived projects

Add the source repository as an optional upstream remote, fetch the desired release/tag, and compare the relevant files. Template repositories can have unrelated histories: do not blindly merge an entire upstream history. Copy or apply reviewed targeted differences on a new branch, preserve project-specific AGENTS.md, briefs, agent/skill instructions and CI, then test and open a PR.

Git patches/file comparisons are sufficient; no synchronization service is required. Never automatically overwrite a project's instructions or lockfiles. Existing generated repositories do not inherit new settings or skills.

## Skills and runtime compatibility

Repository skills live in .agents/skills/<name>/SKILL.md. Keep precise trigger metadata; edit existing skills rather than adding duplicates. Preserve frontmatter and validate it. The local standard-library checker intentionally accepts only the template's flat one-line name/description format; it is not a general YAML parser. Add an appropriate parser/test before adopting richer metadata.

Codex normally detects skill edits automatically; restart if the list remains stale. Skills with names also present in user plugins may appear twice: identify the repository path.

Periodically check official Codex formats and installed runtime capabilities. Do not pin a model unavailable to all users. Recheck tool permissions and the effective concurrency cap per environment.

## CI maintenance

Actions are pinned to verified commit SHAs. Review upstream changes and replace pins deliberately; do not assume a moving tag is immutable. The template CI checks configuration on Python 3.11/3.12 and Linux/Windows. Derived projects add their own stack-specific tests, lint/type/build checks without removing infrastructure validation.

Release tags may be created after review/merge according to the human maintainer's release policy. Template version 0.2.0 is integrated into main; no release tag or deployment is created automatically.
