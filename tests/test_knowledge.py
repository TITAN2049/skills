"""Behavioral checks for project-local knowledge, using only temporary fixtures."""

from copy import deepcopy
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/sdlc-memory/scripts/knowledge.py"


def load_helper():
    specification = importlib.util.spec_from_file_location("knowledge_under_test", SCRIPT)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="sdlc-knowledge-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "project"
        self.repo.mkdir()
        (self.repo / "src").mkdir()
        self.source = self.repo / "src/app.py"
        self.source.write_text("SOURCE_CONTENT_MUST_NOT_BE_COPIED = 1\n", encoding="utf-8")
        self.body = self.base / "curated.txt"
        self.body.write_text("The entry point is src/app.py; this is a curated finding.", encoding="utf-8")
        self.store = self.repo / ".sdlc/knowledge.json"

    def command(self, *args, repo=None):
        return [sys.executable, "-B", str(SCRIPT), "--repo", str(repo or self.repo), *args]

    def run_cli(self, *args, expected=0, repo=None):
        result = subprocess.run(self.command(*args, repo=repo), text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, expected, (args, result.stdout, result.stderr))
        return result

    def save_args(self, note="routing", title="Routing entry", summary="Verified entry point.", evidence=None, ttl=30):
        args = ["save", note, "--title", title, "--summary", summary,
                "--body-file", str(self.body), "--ttl-days", str(ttl)]
        for path in evidence if evidence is not None else ["src/app.py"]:
            args.extend(["--evidence", path])
        return args

    def save(self, note="routing", **kwargs):
        return self.run_cli(*self.save_args(note, **kwargs))

    def stored(self):
        return json.loads(self.store.read_text(encoding="utf-8"))

    def replace_store(self, value):
        self.store.write_text(json.dumps(value), encoding="utf-8")

    def test_missing_store_read_operations_do_not_create_storage(self):
        self.assertEqual(json.loads(self.run_cli("list").stdout)["notes"], [])
        self.run_cli("read", "missing", expected=2)
        self.run_cli("delete", "missing", expected=2)
        self.assertFalse((self.repo / ".sdlc").exists())

    def test_save_stores_curated_text_and_hashes_without_copying_sources(self):
        self.save()
        note = self.stored()["notes"]["routing"]
        self.assertEqual(note["evidence"], [{"path": "src/app.py", "sha256": hashlib.sha256(self.source.read_bytes()).hexdigest()}])
        self.assertEqual(note["expires_at"] - note["updated_at"], 30 * 86400)
        self.assertNotIn("SOURCE_CONTENT_MUST_NOT_BE_COPIED", self.store.read_text())
        self.assertEqual(json.loads(self.run_cli("read", "routing").stdout)["body"], self.body.read_text())
        self.assertEqual(set(path.name for path in self.store.parent.iterdir()), {"knowledge.json"})

    def test_listing_is_compact_filtered_and_bounded(self):
        self.save()
        store = self.stored()
        original = store["notes"]["routing"]
        store["notes"] = {}
        for number in range(12):
            note = deepcopy(original)
            note["id"] = f"note-{number:02}"
            note["title"] = "Special routing" if number == 11 else "Other concern"
            note["body"] = "BODY_ONLY_SEARCH_MARKER"
            store["notes"][note["id"]] = note
        self.replace_store(store)
        listed = json.loads(self.run_cli("list").stdout)
        self.assertEqual(len(listed["notes"]), 10)
        self.assertEqual(listed["total_matches"], 12)
        self.assertTrue(all("body" not in note for note in listed["notes"]))
        selected = json.loads(self.run_cli("list", "--query", "SPECIAL").stdout)
        self.assertEqual([note["id"] for note in selected["notes"]], ["note-11"])
        self.assertEqual(json.loads(self.run_cli("list", "--query", "BODY_ONLY_SEARCH_MARKER").stdout)["notes"], [])

    def test_content_changes_are_stale_even_when_mtime_is_preserved(self):
        self.save()
        original = self.source.stat()
        self.source.write_text("SOURCE_CONTENT_MUST_NOT_BE_COPIED = 2\n")
        os.utime(self.source, ns=(original.st_atime_ns, original.st_mtime_ns))
        result = json.loads(self.run_cli("read", "routing", expected=3).stdout)
        self.assertEqual(result["status"], "stale")
        self.assertIn("evidence_changed", result["reasons"])
        self.assertNotIn("body", result)
        self.assertNotIn(self.body.read_text(), json.dumps(result))
        allowed = json.loads(self.run_cli("read", "routing", "--allow-stale").stdout)
        self.assertEqual(allowed["status"], "stale")
        self.assertEqual(allowed["body"], self.body.read_text())

    def test_missing_and_expired_evidence_withhold_body(self):
        self.save()
        self.source.unlink()
        missing = json.loads(self.run_cli("read", "routing", expected=3).stdout)
        self.assertIn("evidence_missing", missing["reasons"])
        store = self.stored()
        note = store["notes"]["routing"]
        note["created_at"] = note["updated_at"] = int(time.time()) - 86401
        note["expires_at"] = int(time.time()) - 1
        self.replace_store(store)
        expired = json.loads(self.run_cli("read", "routing", expected=3).stdout)
        self.assertIn("expired", expired["reasons"])
        self.assertNotIn("body", expired)

    def test_branch_and_commit_provenance_do_not_invalidate_unchanged_evidence(self):
        git = self.repo / ".git"
        (git / "refs/heads").mkdir(parents=True)
        (git / "HEAD").write_text("ref: refs/heads/main\n")
        (git / "refs/heads/main").write_text("a" * 40 + "\n")
        self.save()
        self.assertEqual(self.stored()["notes"]["routing"]["provenance"], {"branch": "main", "head": "a" * 40})
        (git / "HEAD").write_text("ref: refs/heads/feature\n")
        (git / "refs/heads/feature").write_text("b" * 40 + "\n")
        (self.repo / "unrelated.txt").write_text("Changed by another commit")
        self.assertEqual(json.loads(self.run_cli("read", "routing").stdout)["status"], "fresh")
        self.save()
        self.assertEqual(self.stored()["notes"]["routing"]["provenance"], {"branch": "feature", "head": "b" * 40})

    def test_same_id_replaces_and_delete_removes_only_that_note(self):
        self.save()
        self.save("other")
        self.body.write_text("A replacement explicitly verified by the caller.")
        result = json.loads(self.save().stdout)
        self.assertTrue(result["replaced"])
        self.assertEqual(len(self.stored()["notes"]), 2)
        self.assertEqual(json.loads(self.run_cli("read", "routing").stdout)["body"], self.body.read_text())
        self.run_cli("delete", "routing")
        self.assertEqual(set(self.stored()["notes"]), {"other"})
        self.run_cli("read", "routing", expected=2)

    def test_read_and_list_leave_existing_store_and_project_unchanged(self):
        self.save()
        before = {str(p.relative_to(self.repo)): (p.stat().st_mtime_ns, p.read_bytes())
                  for p in self.repo.rglob("*") if p.is_file()}
        self.run_cli("list")
        self.run_cli("read", "routing")
        after = {str(p.relative_to(self.repo)): (p.stat().st_mtime_ns, p.read_bytes())
                 for p in self.repo.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_text_evidence_and_ttl_limits_reject_overflow(self):
        for kwargs in ({"summary": "s" * 181}, {"title": "t" * 161}, {"ttl": 0}, {"ttl": 3651},
                       {"evidence": []}, {"evidence": ["src/app.py"] * 33},
                       {"evidence": ["src/app.py", "src/app.py"]}):
            with self.subTest(kwargs=kwargs):
                self.run_cli(*self.save_args(**kwargs), expected=2)
        self.body.write_text("b" * 4001)
        self.run_cli(*self.save_args(), expected=2)
        self.assertFalse(self.store.exists())

    def test_note_count_limit_allows_explicit_replacement(self):
        self.save()
        store = self.stored()
        template = store["notes"]["routing"]
        store["notes"] = {}
        for number in range(100):
            note = deepcopy(template)
            note["id"] = f"note-{number}"
            store["notes"][note["id"]] = note
        self.replace_store(store)
        before = self.store.read_bytes()
        self.run_cli(*self.save_args("overflow"), expected=2)
        self.assertEqual(self.store.read_bytes(), before)
        self.save("note-0")
        self.assertEqual(len(self.stored()["notes"]), 100)

    def test_evidence_confinement_secret_paths_and_nonregular_files(self):
        for path in ("../outside.txt", str(self.source), "src/../src/app.py", "src"):
            with self.subTest(path=path):
                self.run_cli(*self.save_args(evidence=[path]), expected=2)
        for filename in (".env", ".env.local", "credentials.json", "id_rsa", "private-key.pem"):
            (self.repo / filename).write_text("not a real secret")
            self.run_cli(*self.save_args(evidence=[filename]), expected=2)
        self.assertFalse(self.store.exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "Filesystem does not support symlinks")
    def test_symlink_files_directories_and_store_are_rejected(self):
        (self.repo / "linked.py").symlink_to(self.source)
        (self.repo / "linked-directory").symlink_to(self.repo / "src", target_is_directory=True)
        for evidence in ("linked.py", "linked-directory/app.py"):
            self.run_cli(*self.save_args(evidence=[evidence]), expected=2)
        self.save()
        self.source.unlink()
        self.source.symlink_to(self.body)
        result = json.loads(self.run_cli("read", "routing", expected=3).stdout)
        self.assertNotIn("body", result)
        self.assertIn("evidence_unavailable_or_unsafe", result["reasons"])
        self.store.unlink()
        self.store.symlink_to(self.body)
        self.run_cli("list", expected=2)
        self.run_cli(*self.save_args(evidence=["linked.py"]), expected=2)

    @unittest.skipUnless(hasattr(os, "symlink"), "Filesystem does not support symlinks")
    def test_symlink_metadata_directory_cannot_write_outside_root(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.repo / ".sdlc").symlink_to(outside, target_is_directory=True)
        self.run_cli("list", expected=2)
        self.run_cli(*self.save_args(), expected=2)
        self.assertEqual(list(outside.iterdir()), [])

    def test_secret_note_scanner_does_not_echo_secret_text(self):
        secret = "password=demonstration_secret_value_123"
        self.body.write_text(secret)
        result = self.run_cli(*self.save_args(), expected=2)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertFalse(self.store.exists())

    def test_all_readers_reject_corrupt_oversized_or_wrong_root_store(self):
        self.save()
        original = self.stored()
        for corrupt in ({**original, "notes": []}, {**original, "repo_id": "0" * 64},
                        {**original, "unexpected": True}):
            self.replace_store(corrupt)
            for command in (("list",), ("read", "routing"), ("delete", "routing")):
                self.run_cli(*command, expected=2)
        self.store.write_text('{"version":1,"version":1}')
        self.run_cli("list", expected=2)
        self.store.write_bytes(b" " * (4 * 1024 * 1024 + 1))
        self.run_cli("list", expected=2)
        self.replace_store(original)
        other = self.base / "other-root"
        (other / ".sdlc").mkdir(parents=True)
        (other / ".sdlc/knowledge.json").write_bytes(self.store.read_bytes())
        self.run_cli("list", repo=other, expected=2)

    def test_read_output_is_bounded_even_when_json_escaping_expands_body(self):
        self.body.write_text("\n" * 4000)
        self.save(title='"' * 160, summary="\\" * 180)
        result = self.run_cli("read", "routing")
        self.assertLessEqual(len(result.stdout.rstrip("\n")), 4500)
        decoded = json.loads(result.stdout)
        self.assertTrue(decoded["body_truncated"])
        self.assertIn("body", decoded)

    def test_maximum_escaped_metadata_fits_both_fresh_and_withheld_reads(self):
        # Each component is legal and beneath filesystem component limits; the
        # registered paths reach the full schema limit and double under JSON.
        paths = []
        for index in range(3):
            relative = "/".join(['"' * 170, '"' * 170, str(index) + '"' * 169])
            self.assertEqual(len(relative), 512)
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("explicit evidence")
            paths.append(relative)
        branch = '"' * 127 + "/" + '"' * 128
        git = self.repo / ".git"
        reference = git / "refs/heads" / branch
        reference.parent.mkdir(parents=True)
        reference.write_text("a" * 40)
        (git / "HEAD").write_text("ref: refs/heads/" + branch)
        note_id = "n" * 64
        self.save(note_id, title='"' * 160, summary='"' * 180, evidence=paths)
        fresh = self.run_cli("read", note_id)
        self.assertLessEqual(len(fresh.stdout.rstrip("\n")), 4500)
        self.assertEqual(json.loads(fresh.stdout)["status"], "fresh")
        (self.repo / paths[0]).write_text("changed")
        stale = self.run_cli("read", note_id, expected=3)
        self.assertLessEqual(len(stale.stdout.rstrip("\n")), 4500)
        result = json.loads(stale.stdout)
        self.assertNotIn("body", result)
        self.assertGreater(result["evidence_paths_omitted"], 0)

    @unittest.skipUnless(hasattr(os, "symlink"), "Filesystem does not support symlinks")
    def test_directory_replacement_during_save_or_delete_cannot_redirect_writes(self):
        self.save()
        module = load_helper()
        for operation in ("save", "delete"):
            with self.subTest(operation=operation):
                old_store = self.store.read_bytes()
                directory = self.store.parent
                moved = self.repo / "moved-metadata"
                outside = self.base / f"outside-{operation}"
                outside.mkdir()

                def swap():
                    directory.rename(moved)
                    directory.symlink_to(outside, target_is_directory=True)

                if operation == "save":
                    def replace_during_provenance(root):
                        swap()
                        return {"branch": None, "head": None}
                    replacement = patch.object(module, "git_provenance", replace_during_provenance)
                    args = self.save_args("new-note")
                else:
                    original = module.atomic_save

                    def replace_before_commit(handle, store):
                        swap()
                        return original(handle, store)
                    replacement = patch.object(module, "atomic_save", replace_before_commit)
                    args = ["delete", "routing"]
                with replacement, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    code = module.main(["--repo", str(self.repo), *args])
                self.assertEqual(code, 2)
                self.assertEqual(list(outside.iterdir()), [])
                self.assertEqual((moved / "knowledge.json").read_bytes(), old_store)
                self.assertFalse((moved / "knowledge.lock").exists())
                directory.unlink()
                moved.rename(directory)

    def test_unsupported_filesystem_fails_before_creating_storage(self):
        module = load_helper()
        with patch.object(module.os, "supports_dir_fd", set()), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = module.main(["--repo", str(self.repo), *self.save_args()])
        self.assertEqual(code, 2)
        self.assertFalse((self.repo / ".sdlc").exists())

    def test_busy_lock_bounds_mutations_without_blocking_readers_or_stealing(self):
        self.save()
        lock = self.store.parent / "knowledge.lock"
        lock.mkdir()
        before = self.store.read_bytes()
        started = time.monotonic()
        self.run_cli(*self.save_args("other"), expected=2)
        self.run_cli("delete", "routing", expected=2)
        self.assertLess(time.monotonic() - started, 5)
        self.assertTrue(lock.is_dir())
        self.assertEqual(self.store.read_bytes(), before)
        self.run_cli("list")
        self.run_cli("read", "routing")
        lock.rmdir()

    def test_concurrent_saves_do_not_lose_successful_notes(self):
        processes = [subprocess.Popen(self.command(*self.save_args(note)), text=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) for note in ("first", "second")]
        for process in processes:
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, (stdout, stderr))
        self.assertEqual(set(self.stored()["notes"]), {"first", "second"})
        self.assertFalse((self.store.parent / "knowledge.lock").exists())


if __name__ == "__main__":
    unittest.main()
