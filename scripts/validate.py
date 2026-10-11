#!/usr/bin/env python3
"""Static template validation using Python 3.11+ and the standard library.

Frontmatter supports exactly two one-line string fields, name and description,
between standalone --- delimiters. Plain text, JSON-style double quotes and
YAML-style single quotes are accepted. Plain strings must start with an ASCII
letter or underscore and cannot be implicit YAML boolean/null values. Skill
names are lowercase ASCII letter/digit/hyphen slugs shorter than 64 characters.
Collections, multiline values, aliases, tags and implicit non-string values
are unsupported. This is not a general YAML
parser. Structure does not establish semantic quality or runtime availability.
The concurrency ceiling of 8 is template policy, distinct from runtime slots.
"""
import json
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
AGENTS = {"architect", "backend", "frontend", "database", "designer", "security", "qa", "devops", "tech_lead"}
SKILLS = {"planning", "code-review", "systematic-debugging", "test-strategy", "security-audit", "database-change", "release-readiness"}
READ_ONLY = {"architect", "designer", "security"}
REQUIRED_FILES = (
    "README.md", "AGENTS.md", "docs/PROJECT_BRIEF.md", ".github/workflows/validate.yml",
    "docs/START_HERE.md", "docs/MAINTENANCE.md", "docs/SECURITY.md", "VERSION", "CHANGELOG.md",
    "docs/COLLABORATION.md", "docs/SMOKE_TEST.md", "docs/AUDIT.md", "docs/VERIFICATION.md",
    "templates/stacks/nextjs-fullstack.md", "templates/stacks/mobile.md",
    "templates/stacks/laravel-nextjs-postgres.md",
)


def _inside(root, path, errors):
    """Resolve before reading, including parent-directory and file symlinks."""
    try:
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            errors.append("path escapes template root: " + str(path))
            return None
        return resolved
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append("invalid path " + str(path) + ": " + str(exc))
        return None


def _toml(path, errors, label):
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        errors.append("invalid " + label + ": " + str(exc))
        return None


def _scalar(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, str) and parsed.strip() else None
        except json.JSONDecodeError:
            return None
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            return None
        inner = value[1:-1]
        if "'" in inner.replace("''", ""):
            return None
        parsed = inner.replace("''", "'")
        return parsed if parsed.strip() else None
    if not re.match(r"[A-Za-z_]", value) or value.lower() in {
        "null", "true", "false", "on", "off", "yes", "no", "y", "n"
    }:
        return None
    if re.search(r":\s|\s#", value) or value.startswith("#"):
        return None
    return value


def _skill(content):
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None, "missing opening delimiter"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "missing closing delimiter"
    fields = {}
    for line in lines[1:end]:
        key, separator, raw = line.partition(":")
        if not separator or key not in {"name", "description"} or key in fields:
            return None, "expected exactly name and description fields"
        value = _scalar(raw)
        if value is None:
            return None, "invalid or empty " + key
        fields[key] = value
    if set(fields) != {"name", "description"}:
        return None, "expected exactly name and description fields"
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]) or len(fields["name"]) >= 64:
        return None, "invalid skill name slug (lowercase letters/digits/hyphens, under 64 characters)"
    if not "\n".join(lines[end + 1:]).strip():
        return None, "empty body"
    return fields, None


def validate(root=ROOT) -> list[str]:
    errors = []
    try:
        root = Path(root).resolve()
    except (OSError, RuntimeError, ValueError, TypeError) as exc:
        return ["invalid template root: " + str(exc)]
    for relative in REQUIRED_FILES:
        path = _inside(root, root / relative, errors)
        if path is not None and not path.is_file():
            errors.append("missing: " + relative)

    config_path = _inside(root, root / ".codex/config.toml", errors)
    data = _toml(config_path, errors, "Codex config") if config_path is not None else None
    if data is not None:
        cfg = data.get("agents")
        if not isinstance(cfg, dict):
            errors.append("agents must be a TOML table")
        else:
            if cfg.get("enabled") is not True:
                errors.append("agents.enabled must be true")
            count = cfg.get("max_concurrent_threads_per_session")
            if type(count) is not int or not 1 <= count <= 8:
                errors.append("invalid concurrency limit: expected integer from 1 to 8")
        skill_cfg = data.get("skills", {})
        if not isinstance(skill_cfg, dict):
            errors.append("skills must be a TOML table")
        else:
            entries = skill_cfg.get("config", [])
            if not isinstance(entries, list):
                errors.append("skills.config must be an array of tables")
            else:
                for entry in entries:
                    if not isinstance(entry, dict):
                        errors.append("skills.config entries must be tables")
                        continue
                    path = entry.get("path")
                    if not isinstance(path, str) or not path.strip():
                        errors.append("skills.config entry requires a nonempty path")
                    else:
                        _inside(root, root / path, errors)
                    if "enabled" in entry and type(entry["enabled"]) is not bool:
                        errors.append("skills.config enabled must be boolean")
                    if entry.get("enabled") is False:
                        errors.append("disabled skill in Codex config: " + str(path))

    found = set()
    agent_dir = _inside(root, root / ".codex/agents", errors)
    try:
        agent_paths = sorted(agent_dir.glob("*.toml")) if agent_dir is not None else []
    except OSError as exc:
        errors.append("cannot list agents: " + str(exc))
        agent_paths = []
    for original in agent_paths:
        path = _inside(root, original, errors)
        agent = _toml(path, errors, "agent " + original.name) if path is not None else None
        if agent is None:
            continue
        for field in ("name", "description", "developer_instructions"):
            if not isinstance(agent.get(field), str) or not agent[field].strip():
                errors.append(original.name + " requires nonempty string " + field)
        name = agent.get("name")
        if not isinstance(name, str) or not name.strip():
            continue
        if name in found:
            errors.append("duplicate agent: " + name)
        found.add(name)
        sandbox = "read-only" if name in READ_ONLY else "workspace-write"
        if agent.get("sandbox_mode") != sandbox:
            errors.append("invalid sandbox for " + name + ": expected " + sandbox)
    if found != AGENTS:
        errors.append("agent roster mismatch: " + ", ".join(sorted(AGENTS.symmetric_difference(found))))

    skill_dir = _inside(root, root / ".agents/skills", errors)
    try:
        directories = sorted(skill_dir.iterdir()) if skill_dir is not None and skill_dir.is_dir() else []
    except OSError as exc:
        errors.append("cannot list skills: " + str(exc))
        directories = []
    found_dirs = set()
    found_names = set()
    for directory in directories:
        safe_dir = _inside(root, directory, errors)
        if safe_dir is None or not safe_dir.is_dir():
            continue
        found_dirs.add(directory.name)
        path = _inside(root, safe_dir / "SKILL.md", errors)
        if path is None:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append("invalid skill " + directory.name + ": " + str(exc))
            continue
        fields, reason = _skill(content)
        if fields is None:
            errors.append("invalid frontmatter/body for " + directory.name + ": " + reason)
            continue
        name = fields["name"]
        if name in found_names:
            errors.append("duplicate skill name: " + name)
        found_names.add(name)
        if name != directory.name:
            errors.append("skill name does not match directory: " + directory.name)
    for name in sorted(SKILLS - found_dirs):
        errors.append("missing skill: " + name)
    return errors


if __name__ == "__main__":
    failures = validate(Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT)
    if failures:
        print("INVALID TEMPLATE:")
        for error in failures:
            print("- " + error)
        sys.exit(1)
    print("OK: validated 9 agents, 7 required skills and repository structure.")
