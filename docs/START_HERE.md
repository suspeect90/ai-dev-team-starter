# Start a project with the AI development team

Paste this into Codex after opening the repository:

> Read AGENTS.md, docs/PROJECT_BRIEF.md, .codex/config.toml and inspect available skills and agent definitions. Confirm whether subagent delegation is actually supported in the current runtime. Work as the Tech Lead. First explore the repository read-only, propose an MVP architecture, risk register, acceptance criteria, test plan, and independently delegable tasks. Do not modify business code before I approve the proposed scope. Do not assume any test passed or agent ran unless observed.

## Safe smoke test

Ask the primary agent:

> Independently ask the `architect` and `security` agents to review AGENTS.md without editing files. Compare their conclusions and explicitly confirm which subagents actually launched.

If subagents are unavailable, perform sequential reviews and report the limitation. Read-only review is not a substitute for execution testing.
