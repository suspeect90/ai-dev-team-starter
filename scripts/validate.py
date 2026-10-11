#!/usr/bin/env python3
"""Static validation of a reusable Codex team template (Python 3.11+)."""
from pathlib import Path
import tomllib
import sys

ROOT = Path(__file__).resolve().parents[1]
AGENTS = {"architect", "backend", "frontend", "database", "designer", "security", "qa", "devops", "tech_lead"}
SKILLS = {"planning", "code-review", "systematic-debugging", "test-strategy", "security-audit", "database-change", "release-readiness"}

def validate(root=ROOT):
    errors = []
    for relative in ("README.md", "AGENTS.md", "docs/PROJECT_BRIEF.md", ".github/workflows/validate.yml"):
        if not (root / relative).is_file():
            errors.append("missing: " + relative)
    try:
        data = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
        cfg = data.get("agents", {})
        if cfg.get("enabled") is not True:
            errors.append("agents.enabled must be true")
        count = cfg.get("max_concurrent_threads_per_session")
        if type(count) is not int or not 1 <= count <= 8:
            errors.append("invalid concurrency limit")
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append("invalid Codex config: " + str(exc))
    found = set()
    for path in sorted((root / ".codex/agents").glob("*.toml")):
        try:
            agent = tomllib.loads(path.read_text(encoding="utf-8"))
            for field in ("name", "description", "developer_instructions"):
                if not isinstance(agent.get(field), str) or not agent[field].strip():
                    errors.append(str(path.name) + " missing " + field)
            name = agent.get("name")
            if name in found:
                errors.append("duplicate agent: " + str(name))
            found.add(name)
            if agent.get("sandbox_mode") not in ("read-only", "workspace-write"):
                errors.append("invalid sandbox for " + str(name))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(str(path.name) + ": " + str(exc))
    if found != AGENTS:
        errors.append("agent roster mismatch: " + str(AGENTS.symmetric_difference(found)))
    for name in SKILLS:
        path = root / ".agents/skills" / name / "SKILL.md"
        if not path.is_file():
            errors.append("missing skill: " + name)
            continue
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n") or ("\nname: " + name + "\n") not in content or "\ndescription: " not in content:
            errors.append("invalid frontmatter: " + name)
    return errors

if __name__ == "__main__":
    failures = validate()
    if failures:
        print("INVALID TEMPLATE:")
        for error in failures:
            print("- " + error)
        sys.exit(1)
    print("OK: validated 9 agents, 7 skills and required repository structure.")
