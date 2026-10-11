# AI Dev Team Starter

Reusable **GitHub repository template** for working with Codex subagents, local skills and practical software engineering safeguards.

**Status: v0.1.0.** Agent/skill configuration and repository structure can be statically validated. A live Codex delegation test must still be run before treating the team as operational.

## What is inside

- `AGENTS.md`: orchestration, security rules, testing standards and delivery contract.
- `.codex/config.toml`: Codex multi-agent settings (up to 4 spawned threads).
- `.codex/agents/`: 9 role definitions (including an optional dedicated tech lead).
- `.agents/skills/`: 7 process skills with portable `SKILL.md` definitions.
- `scripts/validate.py` + `tests/`: local structural checks.
- `.github/workflows/validate.yml`: structural validation in GitHub Actions.
- `templates/stacks/`: optional Laravel/Next.js/Postgres, Next.js fullstack and mobile guidance.
- `docs/`: brief, operating guide, security and template maintenance.

## Start a new project

1. On this source repository, choose **Settings → General → Template repository** (requires appropriate GitHub permissions).
2. Use **Use this template → Create a new repository**. Prefer Private for client or business applications.
3. Clone the newly created repository and open its root in a compatible Codex environment.
4. Fill `docs/PROJECT_BRIEF.md`, select a stack profile, and keep `AGENTS.md` relevant.
5. Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` (Python 3.11+).
6. Paste the bootstrap prompt from `docs/START_HERE.md` into Codex.
7. Run the read-only multi-agent smoke test in `docs/START_HERE.md` before production use.

## Why this is a template

Each new repository receives a snapshot of the files, **not automatic updates** from this repository. Follow `docs/MAINTENANCE.md` for versioned updates. A repository template does not install plugins or grant access to GitHub, hosting providers, secrets or local developer tools.

## Safety

Do not auto-deploy or change real financial data. All sensitive operations require human review and authorization. Only claim the tests and runtime checks that have actually run.

## Official references

- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Codex config reference](https://developers.openai.com/codex/config-reference)
- [GitHub template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
