# AI Dev Team Starter

Reusable Codex development team: **9 specialist roles, 7 engineering skills, native orchestration instructions and structural CI**. No application stack is imposed.

**Template version: 0.2.0, integrated into main.** Real native task-based delegation is exercised during finalization; automatic custom TOML discovery and sandbox application require verification in your target runtime. See [verification evidence](docs/VERIFICATION.md) and [audit](docs/AUDIT.md).

## Included

- `AGENTS.md`: primary Tech Lead, ownership, security and verification contract.
- `.codex/config.toml`: four open child threads excluding the parent where supported; runtime limits may be lower.
- `.codex/agents/`: tech_lead, architect, backend, frontend, database, security, qa, devops and designer.
- `.agents/skills/`: planning, code-review, systematic-debugging, test-strategy, security-audit, database-change and release-readiness.
- `scripts/validate.py`, `tests/`: Python 3.11+ standard-library structural checks and regression tests.
- `.github/workflows/validate.yml`: Linux/Windows, Python 3.11/3.12 checks on PRs and main.
- `docs/`: onboarding, collaboration, real smoke test, evidence, security and maintenance.
- `templates/stacks/`: optional examples; any stack can be documented in the project brief.

## Start

1. Choose **Use this template → Create a new repository** on GitHub. The source was confirmed `is_template: true` on 2026-10-11.
2. Clone your new repository and open its root in Codex. Inspect/trust its project configuration through the client's controls.
3. Fill `docs/PROJECT_BRIEF.md` and run:

Use Python 3.11+ and Git from the checkout root. The tracked-file check inspects Git's index; it does not read ignored local credentials.

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

4. Follow [the practical guide](docs/START_HERE.md), then [the isolated smoke test](docs/SMOKE_TEST.md) in the target environment.

> Voici mon idée d'application. Analyse le besoin, propose l'architecture, prépare le plan de développement et mobilise les spécialistes nécessaires.

The primary agent coordinates by default. Native delegation and named custom-role selection depend on the runtime; copying files neither grants permissions nor installs plugins/models/tools.

## Maintenance and limits

Templates create snapshots, not automatic updates. Follow [maintenance](docs/MAINTENANCE.md) for versioned changes without overwriting project customizations. Template CI validates infrastructure; every derived application adds checks for its actual stack.

No production deployment or real data deletion happens automatically. A successful structural test is not proof of role discovery, enforced sandbox boundaries or application security.

## Official references

- [Codex subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Skills authoring and discovery](https://learn.chatgpt.com/docs/build-skills)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [GitHub template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
