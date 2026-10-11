import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate, AGENTS, SKILLS, REQUIRED_FILES


def _tracked_paths(root):
    """Inspect Git's index only; never open ignored local credentials."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "-z"],
            capture_output=True, check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        raise RuntimeError("Cannot inspect tracked paths; Git and a checkout are required") from None
    if result.stdout and not result.stdout.endswith(b"\0"):
        raise RuntimeError("Invalid Git path inventory: missing NUL terminator")
    return [path.decode("utf-8", errors="surrogateescape")
            for path in result.stdout.split(b"\0") if path]


def _sensitive_paths(paths):
    """Limited filename policy matching the ignored credential families.

    Names do not establish whether a file contains a secret. .env.example
    remains allowed and must contain placeholders only.
    """
    def sensitive(name):
        name = name.casefold()
        return (name == ".env" or (name.startswith(".env.") and name != ".env.example")
                or name.startswith("id_rsa") or name.endswith((".pem", ".key", ".p12")))

    return [path for path in paths if any(sensitive(name) for name in path.split("/"))]


class SensitivePathTests(unittest.TestCase):
    def test_rejects_tracked_sensitive_names_at_any_depth(self):
        paths = [".env", "config/.env.production", "credentials/service.key",
                 "keys/private.pem", "keys/archive.p12", "nested/id_rsa.backup",
                 "nested/SERVICE.KEY", ".env/config", "keys/id_rsa/backup"]
        self.assertEqual(_sensitive_paths(paths), paths)

    def test_allows_placeholder_examples_and_ordinary_files(self):
        paths = [".env.example", "config/.env.example", "README.md",
                 "docs/env-guide.md", "public-key.pub", "envelope.txt"]
        self.assertEqual(_sensitive_paths(paths), [])

    def test_nul_inventory_preserves_newlines_and_nested_paths(self):
        result = subprocess.CompletedProcess([], 0, stdout=b"docs/a\nb.md\0config/.env\0")
        with mock.patch.object(subprocess, "run", return_value=result):
            paths = _tracked_paths(ROOT)
        self.assertEqual(paths, ["docs/a\nb.md", "config/.env"])
        self.assertEqual(_sensitive_paths(paths), ["config/.env"])

    def test_ignored_local_files_are_not_examined(self):
        result = subprocess.CompletedProcess([], 0, stdout=b"README.md\0.env.example\0")
        with mock.patch.object(subprocess, "run", return_value=result), \
                mock.patch.object(Path, "exists", side_effect=AssertionError("Local file probe")):
            self.assertEqual(_sensitive_paths(_tracked_paths(ROOT)), [])

    def test_inventory_failures_do_not_pass(self):
        for failure in (FileNotFoundError("Git unavailable"),
                        subprocess.CalledProcessError(128, ["git"])):
            with self.subTest(failure=type(failure).__name__):
                with mock.patch.object(subprocess, "run", side_effect=failure):
                    with self.assertRaisesRegex(RuntimeError, "Cannot inspect tracked paths"):
                        _tracked_paths(ROOT)

    def test_truncated_inventory_is_rejected(self):
        result = subprocess.CompletedProcess([], 0, stdout=b"credentials/service.key")
        with mock.patch.object(subprocess, "run", return_value=result):
            with self.assertRaisesRegex(RuntimeError, "missing NUL terminator"):
                _tracked_paths(ROOT)


def _fixture_source(root, path):
    """Resolve and reject external links before any source read/enumeration."""
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError("fixture source escapes root: " + str(path))
    return resolved


def build_fixture(source, destination):
    """Copy only the template contract, never application/dependency/data trees.

Containment is checked before every source read and directory enumeration;
this is a static fixture builder, not protection against concurrent link swaps.
"""
    source = Path(source).resolve(strict=True)
    destination = Path(destination)

    def copy(relative):
        path = _fixture_source(source, source / relative)
        if not path.is_file():
            raise ValueError("fixture source is not a file: " + str(path))
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())

    for relative in (*REQUIRED_FILES, ".codex/config.toml"):
        copy(relative)
    agents = _fixture_source(source, source / ".codex/agents")
    for entry in sorted(agents.iterdir()):
        if entry.suffix == ".toml":
            copy(Path(".codex/agents") / entry.name)
    skills = _fixture_source(source, source / ".agents/skills")
    for entry in sorted(skills.iterdir()):
        directory = _fixture_source(source, entry)
        if directory.is_dir():
            copy(Path(".agents/skills") / entry.name / "SKILL.md")


class TemplateTests(unittest.TestCase):
    def setUp(self):
        # All negative tests edit isolated copies under this chat's work folder.
        self.temporary = tempfile.TemporaryDirectory(prefix="template-regression-", dir=ROOT.parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "template"
        build_fixture(ROOT, self.root)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def edit(self, relative, before, after):
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(before, text)
        self.write(relative, text.replace(before, after))

    def assert_error(self, expected):
        errors = validate(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_configuration(self):
        self.assertEqual(validate(self.root), [])

    def test_expected_team_size(self):
        self.assertEqual(len(AGENTS), 9)
        self.assertEqual(len(SKILLS), 7)

    def test_no_sensitive_tracked_paths(self):
        self.assertEqual(_sensitive_paths(_tracked_paths(ROOT)), [])

    def test_agents_array_regression(self):
        self.write(".codex/config.toml", "agents = []\n")
        self.assert_error("agents must be a TOML table")

    def test_agent_name_array_regression(self):
        self.edit(".codex/agents/backend.toml", 'name = "backend"', 'name = ["backend"]')
        self.assert_error("requires nonempty string name")

    def test_empty_agent_name(self):
        self.edit(".codex/agents/backend.toml", 'name = "backend"', 'name = " "')
        self.assert_error("requires nonempty string name")

    def test_invalid_config_toml(self):
        self.write(".codex/config.toml", "[agents\n")
        self.assert_error("invalid Codex config")

    def test_invalid_agent_toml(self):
        self.write(".codex/agents/backend.toml", "name = [\n")
        self.assert_error("invalid agent backend.toml")

    def test_invalid_encoding(self):
        (self.root / ".codex/config.toml").write_bytes(b"\xff")
        self.assert_error("invalid Codex config")

    def test_duplicate_agent_name(self):
        shutil.copy2(self.root / ".codex/agents/backend.toml", self.root / ".codex/agents/duplicate.toml")
        self.assert_error("duplicate agent: backend")

    def test_missing_agent(self):
        (self.root / ".codex/agents/backend.toml").unlink()
        self.assert_error("agent roster mismatch: backend")

    def test_missing_skill(self):
        shutil.rmtree(self.root / ".agents/skills/planning")
        self.assert_error("missing skill: planning")

    def test_missing_skill_file(self):
        (self.root / ".agents/skills/planning/SKILL.md").unlink()
        self.assert_error("invalid skill planning")

    def test_missing_required_document(self):
        (self.root / "docs/START_HERE.md").unlink()
        self.assert_error("missing: docs/START_HERE.md")

    def test_invalid_concurrency(self):
        for value in ("true", "0", "-1", "9", "1.5", '"4"'):
            with self.subTest(value=value):
                self.write(".codex/config.toml", "[agents]\nenabled = true\nmax_concurrent_threads_per_session = " + value + "\n")
                self.assert_error("invalid concurrency limit")

    def test_concurrency_boundaries(self):
        for value in (1, 8):
            with self.subTest(value=value):
                self.write(".codex/config.toml", f"[agents]\nenabled = true\nmax_concurrent_threads_per_session = {value}\n")
                self.assertEqual(validate(self.root), [])

    def test_agents_disabled(self):
        self.edit(".codex/config.toml", "enabled = true", "enabled = false")
        self.assert_error("agents.enabled must be true")

    def test_disabled_skill(self):
        path = self.root / ".codex/config.toml"
        self.write(".codex/config.toml", path.read_text(encoding="utf-8") + '\n[[skills.config]]\npath = ".agents/skills/planning"\nenabled = false\n')
        self.assert_error("disabled skill in Codex config")

    def test_invalid_skill_config_types(self):
        for value in ('skills = []\n', '[skills]\nconfig = "wrong"\n', '[skills]\nconfig = [1]\n'):
            with self.subTest(value=value):
                self.write(".codex/config.toml", value + "[agents]\nenabled = true\nmax_concurrent_threads_per_session = 4\n")
                self.assert_error("skills")

    def test_frontmatter_closing_delimiter_required(self):
        self.write(".agents/skills/planning/SKILL.md", "---\nname: planning\ndescription: A plan\nBody\n")
        self.assert_error("missing closing delimiter")

    def test_frontmatter_values_and_body(self):
        for value in ("", '""', "' '", "[]", "{}", "|", "true", "123", "*alias"):
            with self.subTest(value=value):
                self.write(".agents/skills/planning/SKILL.md", f"---\nname: planning\ndescription: {value}\n---\nBody\n")
                self.assert_error("invalid or empty description")
        self.write(".agents/skills/planning/SKILL.md", "---\nname: planning\ndescription: A plan\n---\n \n")
        self.assert_error("empty body")

    def test_frontmatter_duplicate_field(self):
        self.write(".agents/skills/planning/SKILL.md", "---\nname: planning\nname: planning\ndescription: Plan\n---\nBody\n")
        self.assert_error("expected exactly name and description")

    def test_frontmatter_scalar_quotes(self):
        self.write(".agents/skills/planning/SKILL.md", "---\nname: \"planning\"\ndescription: 'A user''s plan'\n---\nBody\n")
        self.assertEqual(validate(self.root), [])

    def test_plain_frontmatter_rejects_yaml_types_and_invalid_prefixes(self):
        for value in (".nan", ".inf", "0xFF", "0o77", "- invalid", "%invalid", "]invalid", "}invalid",
                      "on", "off", "yes", "no", "y", "n", "NULL", "False", "YES"):
            with self.subTest(value=value):
                self.write(".agents/skills/planning/SKILL.md", f"---\nname: planning\ndescription: {value}\n---\nBody\n")
                self.assert_error("invalid or empty description")

    def test_quoted_frontmatter_preserves_string_values(self):
        for value in (".nan", ".inf", "0xFF", "0o77", "- invalid", "%invalid", "]invalid", "}invalid",
                      "on", "off", "yes", "no", "y", "n", "null", "false", "123"):
            for quote in ('"', "'"):
                with self.subTest(value=value, quote=quote):
                    self.write(".agents/skills/planning/SKILL.md", f"---\nname: planning\ndescription: {quote}{value}{quote}\n---\nBody\n")
                    self.assertEqual(validate(self.root), [])

    def test_skill_name_slug(self):
        for name in ("Planning", "has_space", "has space", "équipe", "a/b", "-name", "name-", "a--b", "a" * 64):
            with self.subTest(name=name):
                self.write(".agents/skills/planning/SKILL.md", f'---\nname: "{name}"\ndescription: Plan\n---\nBody\n')
                self.assert_error("invalid skill name slug")
        name = "a" * 63
        self.write(f".agents/skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: Plan\n---\nBody\n")
        self.write(".agents/skills/planning/SKILL.md", "---\nname: planning\ndescription: Plan\n---\nBody\n")
        self.assertEqual(validate(self.root), [])

    def test_fixture_excludes_application_and_dependencies(self):
        for relative in ("application/private-data.bin", "node_modules/package/index.js", "data/customer.csv", ".git/config"):
            self.write(relative, "must not enter fixture")
        destination = Path(self.temporary.name) / "minimal"
        build_fixture(self.root, destination)
        self.assertEqual(validate(destination), [])
        for excluded in ("application", "node_modules", "data", ".git", "tests", "scripts"):
            self.assertFalse((destination / excluded).exists())

    def test_fixture_rejects_external_file_and_directory_links(self):
        for relative in ("README.md", ".codex/agents", ".agents/skills/planning"):
            with self.subTest(relative=relative):
                path = self.root / relative
                outside = Path(self.temporary.name) / "outside-fixture-source"
                is_directory = path.is_dir()
                path.rename(outside)
                try:
                    path.symlink_to(outside, target_is_directory=is_directory)
                except (OSError, NotImplementedError) as exc:
                    outside.rename(path)
                    self.skipTest("fixture symlink unavailable: " + str(exc))
                try:
                    with self.assertRaisesRegex(ValueError, "fixture source escapes root"):
                        build_fixture(self.root, Path(self.temporary.name) / "rejected-fixture")
                finally:
                    path.unlink()
                    outside.rename(path)

    def test_extra_skill_duplicate_name(self):
        shutil.copytree(self.root / ".agents/skills/planning", self.root / ".agents/skills/extra")
        self.assert_error("duplicate skill name: planning")

    def test_extra_skill_unique_name(self):
        self.write(".agents/skills/extra/SKILL.md", "---\nname: extra\ndescription: Extra skill\n---\nBody\n")
        self.assertEqual(validate(self.root), [])

    def test_required_skill_name_matches_directory(self):
        self.edit(".agents/skills/planning/SKILL.md", "name: planning", "name: another")
        self.assert_error("skill name does not match directory: planning")

    def test_role_sandbox_contract(self):
        for name in ("architect", "designer", "security", "tech_lead", "backend", "frontend", "database", "devops", "qa"):
            relative = f".codex/agents/{name.replace('_', '-')}.toml"
            path = self.root / relative
            original = path.read_text(encoding="utf-8")
            expected = "read-only" if name in {"architect", "designer", "security"} else "workspace-write"
            with self.subTest(name=name):
                self.edit(relative, f'sandbox_mode = "{expected}"', 'sandbox_mode = "danger-full-access"')
                self.assert_error("invalid sandbox for " + name)
                self.write(relative, original)

    def test_config_path_escape(self):
        path = self.root / ".codex/config.toml"
        self.write(".codex/config.toml", path.read_text(encoding="utf-8") + '\n[[skills.config]]\npath = "../outside"\nenabled = true\n')
        self.assert_error("path escapes template root")

    def test_symlink_escape(self):
        # Windows may require developer mode or a symlink privilege.
        for relative in (".codex/config.toml", ".codex/agents/backend.toml", ".agents/skills/planning/SKILL.md"):
            with self.subTest(relative=relative):
                target = Path(self.temporary.name) / "outside.txt"
                original = (self.root / relative).read_text(encoding="utf-8")
                target.write_text(original, encoding="utf-8")
                path = self.root / relative
                path.unlink()
                try:
                    path.symlink_to(target)
                except (OSError, NotImplementedError) as exc:
                    path.write_text(original, encoding="utf-8")
                    self.skipTest("symlink unavailable: " + str(exc))
                try:
                    self.assert_error("path escapes template root")
                finally:
                    path.unlink()
                    path.write_text(original, encoding="utf-8")

    def test_directory_symlink_escape(self):
        for relative in (".codex/agents", ".agents/skills/planning"):
            with self.subTest(relative=relative):
                path = self.root / relative
                outside = Path(self.temporary.name) / "outside-directory"
                path.rename(outside)
                try:
                    path.symlink_to(outside, target_is_directory=True)
                except (OSError, NotImplementedError) as exc:
                    outside.rename(path)
                    self.skipTest("directory symlink unavailable: " + str(exc))
                try:
                    self.assert_error("path escapes template root")
                finally:
                    path.unlink()
                    outside.rename(path)

    def test_cli_invalid_configuration_exits_one_without_traceback(self):
        for target, text in ((".codex/config.toml", "agents = []\n"),
                             (".codex/agents/backend.toml", 'name = ["backend"]\n'),
                             (".codex/config.toml", "[agents\n")):
            with self.subTest(target=target, text=text):
                original = (self.root / target).read_text(encoding="utf-8")
                self.write(target, text)
                result = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), str(self.root)], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("INVALID TEMPLATE:", result.stdout)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                self.write(target, original)

    def test_cli_valid_configuration(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK:", result.stdout)


if __name__ == "__main__":
    unittest.main()
