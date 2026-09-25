"""Exercise installer ownership and filesystem safety in isolated temporary trees."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install.py"
SPEC = importlib.util.spec_from_file_location("sdlc_install", MODULE_PATH)
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="sdlc-installer-test-")
        self.addCleanup(temporary.cleanup)
        self.sandbox = Path(temporary.name)
        self.source = self.sandbox / "toolkit"
        self.target = self.sandbox / "project"
        self.target.mkdir()
        self.source.mkdir()
        self.catalog = {
            "version": "1.0.0",
            "roles": [{"skill": "sdlc-testing"}, {"skill": "sdlc-security"}],
        }
        self.expected = {}
        for role in self.catalog["roles"]:
            name = role["skill"]
            skill_bytes = f"---\nname: {name}\ndescription: Test fixture.\n---\n".encode()
            self.write(self.source / "skills" / name / "SKILL.md", skill_bytes)
            self.expected[f".agents/skills/{name}/SKILL.md"] = skill_bytes
            reference_bytes = f"A reference for {name}.\n".encode()
            self.write(self.source / "skills" / name / "references" / "guide.md", reference_bytes)
            self.expected[f".agents/skills/{name}/references/guide.md"] = reference_bytes
            agent = name.replace("-", "_") + ".toml"
            agent_bytes = f'name = "{name}"\n'.encode()
            self.write(self.source / "agents" / agent, agent_bytes)
            self.expected[f".codex/agents/{agent}"] = agent_bytes
        self.write_catalog()
        root_patch = mock.patch.object(installer, "ROOT", self.source)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    @staticmethod
    def write(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def write_catalog(self):
        (self.source / "catalog.json").write_text(json.dumps(self.catalog), encoding="utf-8")

    @staticmethod
    def snapshot(root):
        """Capture content and directories, including a symlink without following it."""
        result = {}
        for path in root.rglob("*"):
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = ("symlink", str(path.readlink()))
            elif path.is_dir():
                result[rel] = ("directory",)
            else:
                result[rel] = ("file", path.read_bytes(), path.stat().st_mtime_ns)
        return result

    def run_install(self, root=None, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            count = installer.run(root or self.target, **kwargs)
        return count, output.getvalue()

    def manifest(self, root=None):
        return json.loads(((root or self.target) / installer.MANIFEST).read_text(encoding="utf-8"))

    def assert_payload(self, root=None):
        root = root or self.target
        for rel, expected in self.expected.items():
            self.assertEqual((root / rel).read_bytes(), expected, rel)

    def test_fresh_install_copies_skills_references_agents_and_tracks_ownership(self):
        count, _ = self.run_install()
        self.assertEqual(count, len(self.expected))
        self.assert_payload()
        manifest = self.manifest()
        self.assertEqual(manifest["format"], 1)
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertEqual(set(manifest["files"]), set(self.expected))
        for rel, contents in self.expected.items():
            self.assertEqual(manifest["files"][rel], installer.digest(contents))
        installed = {p.relative_to(self.target).as_posix() for p in self.target.rglob("*") if p.is_file()}
        self.assertEqual(installed, set(self.expected) | {installer.MANIFEST.as_posix()})

    def test_dry_run_prints_actions_without_creating_files_or_directories(self):
        before = self.snapshot(self.target)
        count, output = self.run_install(dry_run=True)
        self.assertEqual(count, len(self.expected))
        self.assertIn("WOULD CREATE", output)
        self.assertEqual(self.snapshot(self.target), before)

    def test_second_install_is_idempotent_including_manifest(self):
        self.run_install()
        before = self.snapshot(self.target)
        count, _ = self.run_install()
        self.assertEqual(count, 0)
        self.assertEqual(self.snapshot(self.target), before)

    def test_update_replaces_only_unchanged_managed_content(self):
        self.run_install()
        rel = ".agents/skills/sdlc-testing/SKILL.md"
        new_content = self.expected[rel] + b"Updated test guidance.\n"
        self.write(self.source / "skills/sdlc-testing/SKILL.md", new_content)
        self.catalog["version"] = "1.1.0"
        self.write_catalog()
        before = self.snapshot(self.target)
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertEqual(self.snapshot(self.target), before)
        count, _ = self.run_install(update=True)
        self.assertEqual(count, 1)
        self.expected[rel] = new_content
        self.assert_payload()
        self.assertEqual(self.manifest()["version"], "1.1.0")
        self.assertEqual(self.manifest()["files"][rel], installer.digest(new_content))

    def test_update_refuses_local_edits_without_partial_changes(self):
        self.run_install()
        self.write(self.target / ".codex/agents/sdlc_security.toml", b"Local agent customization.\n")
        self.write(self.source / "skills/sdlc-testing/SKILL.md", b"New upstream skill.\n")
        self.write(self.source / "agents/sdlc_security.toml", b"New upstream agent.\n")
        before = self.snapshot(self.target)
        with self.assertRaisesRegex(installer.InstallError, "No files changed"):
            self.run_install(update=True)
        self.assertEqual(self.snapshot(self.target), before)

    def test_conflict_preflight_prevents_even_earlier_creates(self):
        self.write(self.target / ".codex/agents/sdlc_security.toml", b"Existing independent agent.\n")
        before = self.snapshot(self.target)
        with self.assertRaisesRegex(installer.InstallError, "sdlc_security.toml"):
            self.run_install(update=True)
        self.assertEqual(self.snapshot(self.target), before)
        self.assertFalse((self.target / ".agents").exists())
        self.assertFalse((self.target / installer.MANIFEST).exists())

    def test_uninstall_preserves_edits_identical_preexisting_files_and_unrelated_files(self):
        preexisting = ".agents/skills/sdlc-testing/SKILL.md"
        edited = ".codex/agents/sdlc_security.toml"
        self.write(self.target / preexisting, self.expected[preexisting])
        self.write(self.target / ".codex/config.toml", b"Unrelated configuration.\n")
        self.run_install()
        self.assertNotIn(preexisting, self.manifest()["files"])
        self.write(self.target / edited, b"My edited agent.\n")
        count, output = self.run_install(uninstall=True)
        self.assertEqual(count, len(self.expected) - 2)
        self.assertIn("PRESERVE locally edited file", output)
        self.assertEqual((self.target / preexisting).read_bytes(), self.expected[preexisting])
        self.assertEqual((self.target / edited).read_bytes(), b"My edited agent.\n")
        self.assertEqual((self.target / ".codex/config.toml").read_bytes(), b"Unrelated configuration.\n")
        for rel in set(self.expected) - {preexisting, edited}:
            self.assertFalse((self.target / rel).exists(), rel)
        self.assertEqual(set(self.manifest()["files"]), {edited})

    def test_clean_uninstall_removes_managed_files_and_manifest(self):
        self.run_install()
        count, _ = self.run_install(uninstall=True)
        self.assertEqual(count, len(self.expected))
        self.assertFalse((self.target / installer.MANIFEST).exists())
        self.assertFalse(any(path.is_file() for path in self.target.rglob("*")))

    def test_dry_run_uninstall_does_not_delete_or_rewrite_anything(self):
        self.run_install()
        before = self.snapshot(self.target)
        count, output = self.run_install(uninstall=True, dry_run=True)
        self.assertEqual(count, len(self.expected))
        self.assertIn("WOULD REMOVE", output)
        self.assertEqual(self.snapshot(self.target), before)

    def test_destination_symlinks_are_rejected_before_mutation(self):
        for kind in ("parent", "file", "dangling", "manifest"):
            with self.subTest(kind=kind):
                root = self.sandbox / f"destination-{kind}"
                root.mkdir()
                outside = self.sandbox / f"outside-{kind}"
                outside.mkdir()
                if kind == "parent":
                    (root / ".agents").symlink_to(outside, target_is_directory=True)
                else:
                    relative = installer.MANIFEST if kind == "manifest" else Path(".codex/agents/sdlc_security.toml")
                    link = root / relative
                    link.parent.mkdir(parents=True)
                    target = outside / "protected.txt"
                    if kind != "dangling":
                        target.write_bytes(b"Do not change.\n")
                    link.symlink_to(target)
                before = self.snapshot(root)
                outside_before = self.snapshot(outside)
                with self.assertRaisesRegex(installer.InstallError, "symlink"):
                    self.run_install(root)
                self.assertEqual(self.snapshot(root), before)
                self.assertEqual(self.snapshot(outside), outside_before)

    def test_source_file_symlink_is_rejected_without_writes(self):
        source_file = self.source / "skills/sdlc-testing/SKILL.md"
        outside = self.sandbox / "external-skill.md"
        outside.write_bytes(source_file.read_bytes())
        source_file.unlink()
        source_file.symlink_to(outside)
        with self.assertRaisesRegex(installer.InstallError, "symlink"):
            self.run_install()
        self.assertEqual(self.snapshot(self.target), {})

    def test_source_skill_directory_symlink_is_rejected_without_writes(self):
        source_dir = self.source / "skills/sdlc-testing"
        outside = self.sandbox / "external-skill-directory"
        source_dir.rename(outside)
        source_dir.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(installer.InstallError, "symlink"):
            self.run_install()
        self.assertEqual(self.snapshot(self.target), {})

    def test_cli_user_and_project_scopes_write_only_beneath_selected_root(self):
        fake_home = self.sandbox / "fake-home"
        fake_home.mkdir()
        for user_scope, root in ((False, self.target), (True, fake_home)):
            with self.subTest(scope="user" if user_scope else "project"):
                args = [str(MODULE_PATH)] + (["--user"] if user_scope else ["--project", str(root)])
                with mock.patch("sys.argv", args), mock.patch.object(Path, "home", return_value=fake_home):
                    with contextlib.redirect_stdout(io.StringIO()):
                        installer.main()
                self.assert_payload(root)
                self.assertEqual(set(self.manifest(root)["files"]), set(self.expected))
                self.assertFalse((root / "skills").exists())
                self.assertFalse((root / "agents").exists())
        self.assertEqual({p.name for p in fake_home.iterdir()}, {".agents", ".codex"})
        self.assertEqual({p.name for p in self.target.iterdir()}, {".agents", ".codex"})


if __name__ == "__main__":
    unittest.main()
