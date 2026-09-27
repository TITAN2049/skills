"""Run the shell entry point and read-only doctor against temporary installations."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASH = "/bin/bash"


class ShellInstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="sdlc-shell-test-")
        self.addCleanup(temporary.cleanup)
        self.sandbox = Path(temporary.name)
        self.toolkit = self.sandbox / "toolkit 'quotes' $(touch INJECTED) ; spaces"
        self.project = self.sandbox / "project [one] $cash ; spaces"
        self.cwd = self.sandbox / "unrelated working directory"
        for path in (self.toolkit, self.project, self.cwd):
            path.mkdir()
        (self.toolkit / "scripts").mkdir()
        shutil.copy2(ROOT / "install.sh", self.toolkit / "install.sh")
        shutil.copy2(ROOT / "scripts/install.py", self.toolkit / "scripts/install.py")
        self.catalog = {"version": "1.0.0", "roles": [{"skill": "sdlc-testing"}]}
        self.write_catalog()
        self.skill_rel = ".agents/skills/sdlc-testing/SKILL.md"
        self.agent_rel = ".codex/agents/sdlc_testing.toml"
        self.skill = b"---\nname: sdlc-testing\ndescription: Test fixture.\n---\nBehavioral testing.\n"
        self.agent = (
            b'name = "sdlc_testing"\n'
            b'description = "A testing specialist."\n'
            b'developer_instructions = "Use $sdlc-testing."\n'
        )
        self.write(self.toolkit / "skills/sdlc-testing/SKILL.md", self.skill)
        self.write(self.toolkit / "agents/sdlc_testing.toml", self.agent)
        self.environment = dict(os.environ)
        self.environment["SDLC_PYTHON"] = sys.executable

    @staticmethod
    def write(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def write_catalog(self):
        (self.toolkit / "catalog.json").write_text(json.dumps(self.catalog), encoding="utf-8")

    @staticmethod
    def snapshot(root):
        """Include directory timestamps so temporary writes cannot pass unnoticed."""
        result = {}
        for path in [root, *root.rglob("*")]:
            rel = path.relative_to(root).as_posix()
            stat = path.lstat()
            if path.is_symlink():
                result[rel] = ("symlink", str(path.readlink()), stat.st_mtime_ns)
            elif path.is_dir():
                result[rel] = ("directory", stat.st_mtime_ns)
            else:
                result[rel] = ("file", path.read_bytes(), stat.st_mtime_ns)
        return result

    def shell(self, *args, toolkit=None, environment=None):
        return subprocess.run(
            [BASH, str((toolkit or self.toolkit) / "install.sh"), *map(str, args)],
            cwd=self.cwd,
            env=environment or self.environment,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def install(self):
        result = self.shell("--project", self.project)
        self.assert_success(result)
        return result

    def doctor(self):
        before = self.snapshot(self.project)
        result = self.shell("--project", self.project, "--doctor")
        self.assertEqual(self.snapshot(self.project), before, "doctor modified its target")
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        return result

    def test_install_from_unrelated_cwd_with_literal_spaces_and_metacharacters(self):
        source_before = self.snapshot(self.toolkit)
        self.install()
        self.assertEqual((self.project / self.skill_rel).read_bytes(), self.skill)
        self.assertEqual((self.project / self.agent_rel).read_bytes(), self.agent)
        self.assertEqual(self.snapshot(self.toolkit), source_before)
        self.assertEqual(list(self.cwd.iterdir()), [])
        self.assertFalse((self.cwd / "INJECTED").exists())
        self.assertFalse((self.sandbox / "INJECTED").exists())

    def test_project_equals_argument_preserves_the_entire_path(self):
        result = self.shell(f"--project={self.project}")
        self.assert_success(result)
        self.assertEqual((self.project / self.skill_rel).read_bytes(), self.skill)
        self.assertEqual((self.project / self.agent_rel).read_bytes(), self.agent)
        self.assertEqual(list(self.cwd.iterdir()), [])

    def test_dry_run_does_not_write_to_project_source_or_current_directory(self):
        before = {root: self.snapshot(root) for root in (self.project, self.toolkit, self.cwd)}
        result = self.shell("--project", self.project, "--dry-run")
        self.assert_success(result)
        self.assertIn(self.skill_rel, result.stdout)
        for root, snapshot in before.items():
            self.assertEqual(self.snapshot(root), snapshot, str(root))

    def test_default_user_routing_only_executes_an_inert_argv_stub(self):
        stub = self.sandbox / "stub toolkit with spaces"
        (stub / "scripts").mkdir(parents=True)
        shutil.copy2(ROOT / "install.sh", stub / "install.sh")
        (stub / "scripts/install.py").write_text(
            "import json, sys\nprint(json.dumps(sys.argv[1:]))\n", encoding="utf-8"
        )
        cases = (
            ([], ["--user"]),
            (["--doctor"], ["--user", "--doctor"]),
            (["--update", "--dry-run"], ["--user", "--update", "--dry-run"]),
            (["--user", "--dry-run"], ["--user", "--dry-run"]),
            ([f"--project={self.project}"], [f"--project={self.project}"]),
        )
        before = self.snapshot(self.sandbox)
        for arguments, expected in cases:
            with self.subTest(arguments=arguments):
                result = self.shell(*arguments, toolkit=stub)
                self.assert_success(result)
                self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(self.snapshot(self.sandbox), before)

    def test_invalid_python_override_fails_cleanly_without_writes(self):
        environment = dict(self.environment)
        environment["SDLC_PYTHON"] = str(self.sandbox / "not a Python executable")
        before = self.snapshot(self.sandbox)
        result = self.shell("--project", self.project, environment=environment)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SDLC_PYTHON", result.stderr)
        self.assertIn("Python", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.snapshot(self.sandbox), before)

    def test_non_python_executable_cannot_report_a_successful_install(self):
        executable = self.sandbox / "successful command that is not Python"
        executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        executable.chmod(0o755)
        environment = dict(self.environment)
        environment["SDLC_PYTHON"] = str(executable)
        before = self.snapshot(self.sandbox)
        result = self.shell("--project", self.project, environment=environment)
        self.assertNotEqual(result.returncode, 0, "A non-Python command silently reported installation success")
        self.assertIn("SDLC_PYTHON", result.stderr)
        self.assertEqual(self.snapshot(self.sandbox), before)

    def test_doctor_succeeds_for_an_intact_installation_without_writes(self):
        self.install()
        self.write(self.project / ".codex/config.toml", b"[agents]\nenabled = true\n")
        self.assert_success(self.doctor())

    def test_doctor_reports_a_missing_file_without_recreating_it(self):
        self.install()
        (self.project / self.skill_rel).unlink()
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING " + self.skill_rel, result.stdout)
        self.assertFalse((self.project / self.skill_rel).exists())

    def test_doctor_reports_local_modification_without_reverting_it(self):
        self.install()
        changed = self.skill + b"Personal testing guidance.\n"
        (self.project / self.skill_rel).write_bytes(changed)
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DIFFERS " + self.skill_rel, result.stdout)
        self.assertEqual((self.project / self.skill_rel).read_bytes(), changed)

    def test_doctor_reports_damaged_agent_toml_and_missing_required_fields(self):
        self.install()
        for contents in (b'name = "unterminated', b'name = "sdlc_testing"\n'):
            with self.subTest(contents=contents):
                (self.project / self.agent_rel).write_bytes(contents)
                result = self.doctor()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("INVALID agent " + self.agent_rel, result.stdout)

    def test_doctor_reports_disabled_target_agents_without_enabling_them(self):
        self.install()
        config = b"[agents]\nenabled = false\n"
        self.write(self.project / ".codex/config.toml", config)
        result = self.doctor()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DISABLED", result.stdout)
        self.assertEqual((self.project / ".codex/config.toml").read_bytes(), config)

    def test_doctor_reports_invalid_target_config_without_repairing_it(self):
        self.install()
        for contents in (b"[agents\n", b"agents = 42\n"):
            with self.subTest(contents=contents):
                self.write(self.project / ".codex/config.toml", contents)
                result = self.doctor()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("INVALID target .codex/config.toml", result.stdout)

    def test_update_and_uninstall_are_forwarded_and_preserve_unrelated_config(self):
        config = b"[agents]\nenabled = true\n"
        self.write(self.project / ".codex/config.toml", config)
        self.install()
        updated = self.skill + b"New upstream testing guidance.\n"
        (self.toolkit / "skills/sdlc-testing/SKILL.md").write_bytes(updated)
        self.catalog["version"] = "1.1.0"
        self.write_catalog()
        self.assert_success(self.shell("--project", self.project, "--update"))
        self.assertEqual((self.project / self.skill_rel).read_bytes(), updated)
        manifest = json.loads((self.project / ".codex/sdlc-toolkit-manifest.json").read_text())
        self.assertEqual(manifest["version"], "1.1.0")
        self.assert_success(self.doctor())
        self.assert_success(self.shell("--project", self.project, "--uninstall"))
        self.assertFalse((self.project / self.skill_rel).exists())
        self.assertFalse((self.project / self.agent_rel).exists())
        self.assertFalse((self.project / ".codex/sdlc-toolkit-manifest.json").exists())
        self.assertEqual((self.project / ".codex/config.toml").read_bytes(), config)


if __name__ == "__main__":
    unittest.main()
