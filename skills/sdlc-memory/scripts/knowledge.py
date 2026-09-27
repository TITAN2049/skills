#!/usr/bin/env python3
"""Bounded, project-local curated notes; no command execution or source snapshots."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import stat
import sys
import time

MAX_NOTES = 100
MAX_BODY = 4000
MAX_SUMMARY = 180
MAX_TITLE = 160
MAX_EVIDENCE = 32
MAX_PATH = 512
MAX_STORE_BYTES = 4 * 1024 * 1024
MAX_EVIDENCE_BYTES = 16 * 1024 * 1024
MAX_READ_CHARS = 4500
MAX_TTL = 3650
ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")
HASH_PATTERN = re.compile(r"[a-f0-9]{64}\Z")
GIT_HASH = re.compile(r"(?:[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\Z")
SECRET_PATTERN = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
    r"|\bAKIA[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9]{20,}\b"
    r"|\bsk-[A-Za-z0-9_-]{20,}\b"
    r"|\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"
)
SECRET_ASSIGNMENT = re.compile(
    r"\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret)"
    r"\s*[:=]\s*[\"']?([^\s\"',;]{8,})", re.IGNORECASE
)


class KnowledgeError(Exception):
    pass


def fail(message):
    raise KnowledgeError(message)


def exact_keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        fail(f"Invalid {label} fields")


def text_field(value, maximum, label, multiline=False):
    if not isinstance(value, str) or not 1 <= len(value) <= maximum:
        fail(f"{label} must contain 1–{maximum} characters")
    if any(ord(c) < 32 and (not multiline or c not in "\n\r\t") for c in value):
        fail(f"{label} contains control characters")
    try:
        value.encode("utf-8")
    except UnicodeError:
        fail(f"{label} is not valid UTF-8 text")
    return value


def note_id(value):
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
        fail("ID must be 1–64 lowercase letters, digits, hyphens or underscores; start with a letter/digit")
    return value


def check_secrets(*values):
    for value in values:
        if SECRET_PATTERN.search(value):
            fail("Note resembles secret material; remove credentials or private keys")
        for match in SECRET_ASSIGNMENT.finditer(value):
            candidate = match.group(1).lower()
            if not (candidate.startswith(("<", "${", "your_", "example", "placeholder", "redacted"))
                    or set(candidate) <= {"x", "*", "."}):
                fail("Note resembles a credential assignment; use a non-secret description")


def evidence_path(value):
    text_field(value, MAX_PATH, "Evidence path")
    if "\\" in value or value.startswith("/") or any(p in ("", ".", "..") for p in value.split("/")):
        fail("Evidence must use a confined relative path without dot segments or backslashes")
    parts = PurePosixPath(value).parts
    for part in parts:
        lower = part.lower()
        if (lower in {".git", ".sdlc", ".ssh", ".aws", ".netrc", ".npmrc", ".pypirc", ".envrc"}
                or lower == ".env" or lower.startswith(".env.")
                or "credential" in lower or "private_key" in lower or "private-key" in lower
                or lower in {"secret", "secrets", "secrets.json", "secrets.yaml", "secrets.yml"}
                or lower.startswith(("id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"))
                or lower.endswith((".pem", ".key", ".p12", ".pfx", ".jks"))
                or lower.startswith(("service-account", "service_account"))):
            fail("Evidence path resembles credentials, private keys, or tool metadata")
    return value


def require_anchored_filesystem():
    required = (os.open, os.mkdir, os.stat, os.unlink, os.rmdir, os.rename)
    if (not all(operation in os.supports_dir_fd for operation in required)
            or os.stat not in os.supports_follow_symlinks
            or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY")):
        fail("Safe knowledge storage requires dir_fd/no-follow support; use macOS, Linux, or WSL")


@contextmanager
def regular_file(path, root=None, anchored_fd=None):
    """Reject special files/symlinks; anchor evidence traversal with dir_fd where supported."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = None
    directory_fd = None
    try:
        if anchored_fd is not None:
            fd = os.open(path.name, flags, dir_fd=anchored_fd)
        elif root is not None:
            require_anchored_filesystem()
            parts = path.relative_to(root).parts
            directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            directory_fd = os.open(root, directory_flags)
            for part in parts[:-1]:
                next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
                os.close(directory_fd)
                directory_fd = next_fd
            fd = os.open(parts[-1], flags, dir_fd=directory_fd)
        else:
            if path.is_symlink():
                fail("Symlink files are not allowed")
            fd = os.open(path, flags)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            fail("Only regular files are allowed")
        with os.fdopen(fd, "rb") as stream:
            fd = None
            yield stream
    finally:
        if fd is not None:
            os.close(fd)
        if directory_fd is not None:
            os.close(directory_fd)


def bounded_bytes(path, maximum, root=None, anchored_fd=None):
    with regular_file(path, root, anchored_fd) as stream:
        if os.fstat(stream.fileno()).st_size > maximum:
            fail(f"File exceeds {maximum} bytes")
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        fail(f"File exceeds {maximum} bytes")
    return data


def fingerprint(root, relative):
    evidence_path(relative)
    with regular_file(root / relative, root) as stream:
        before = os.fstat(stream.fileno())
        if before.st_size > MAX_EVIDENCE_BYTES:
            fail("Evidence file exceeds 16 MiB")
        digest = hashlib.sha256()
        size = 0
        while chunk := stream.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_EVIDENCE_BYTES:
                fail("Evidence file exceeds 16 MiB")
            digest.update(chunk)
        after = os.fstat(stream.fileno())
        signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        if signature(before) != signature(after):
            fail("Evidence changed while being hashed; retry after edits settle")
    return digest.hexdigest()


def git_provenance(root):
    """Read only bounded Git metadata; never invoke git or discover source contents."""
    result = {"branch": None, "head": None}
    try:
        git_dir = root / ".git"
        if git_dir.is_symlink():
            return result
        if git_dir.is_file():
            pointer = bounded_bytes(git_dir, 8192).decode("utf-8").strip()
            if not pointer.startswith("gitdir: "):
                return result
            git_dir = (root / pointer[8:]).resolve()
        if not git_dir.is_dir():
            return result
        head = bounded_bytes(git_dir / "HEAD", 8192).decode("utf-8").strip()
        if GIT_HASH.fullmatch(head):
            result["head"] = head.lower()
            return result
        if not head.startswith("ref: refs/heads/"):
            return result
        reference = head[5:]
        branch = reference[len("refs/heads/"):]
        if (not 1 <= len(branch) <= 256 or any(ord(c) < 33 for c in branch)
                or any(p in ("", ".", "..") for p in reference.split("/")) or "\\" in reference):
            return result
        result["branch"] = branch
        common_dir = git_dir
        if (git_dir / "commondir").is_file():
            common_dir = (git_dir / bounded_bytes(git_dir / "commondir", 8192).decode("utf-8").strip()).resolve()
        for base in dict.fromkeys((git_dir, common_dir)):
            try:
                revision = bounded_bytes(base / reference, 8192).decode("ascii").strip()
                if GIT_HASH.fullmatch(revision):
                    result["head"] = revision.lower()
                    return result
            except OSError:
                pass
        try:
            packed = bounded_bytes(common_dir / "packed-refs", 1024 * 1024).decode("ascii")
            for line in packed.splitlines():
                pieces = line.split(" ", 1)
                if len(pieces) == 2 and pieces[1] == reference and GIT_HASH.fullmatch(pieces[0]):
                    result["head"] = pieces[0].lower()
                    break
        except OSError:
            pass
    except (OSError, UnicodeError, KnowledgeError, ValueError):
        pass
    return result


def repo_identity(root):
    return hashlib.sha256(str(root).encode("utf-8")).hexdigest()


def new_store(root):
    return {"version": 1, "repo_root": str(root), "repo_id": repo_identity(root), "notes": {}}


def validate_store(store, root):
    exact_keys(store, ("version", "repo_root", "repo_id", "notes"), "store")
    if type(store["version"]) is not int or store["version"] != 1:
        fail("Unsupported knowledge store version")
    if store["repo_root"] != str(root) or store["repo_id"] != repo_identity(root):
        fail("Knowledge store belongs to a different repository root")
    notes = store["notes"]
    if not isinstance(notes, dict) or len(notes) > MAX_NOTES:
        fail("Knowledge store exceeds 100 notes or has invalid notes")
    for key, note in notes.items():
        note_id(key)
        exact_keys(note, ("id", "title", "summary", "body", "evidence", "created_at", "updated_at", "expires_at", "provenance"), "note")
        if note["id"] != key:
            fail("Note ID differs from its store key")
        text_field(note["title"], MAX_TITLE, "Title")
        text_field(note["summary"], MAX_SUMMARY, "Summary")
        text_field(note["body"], MAX_BODY, "Body", multiline=True)
        check_secrets(note["title"], note["summary"], note["body"])
        evidence = note["evidence"]
        if not isinstance(evidence, list) or not 1 <= len(evidence) <= MAX_EVIDENCE:
            fail("Notes require 1–32 evidence files")
        seen = set()
        for item in evidence:
            exact_keys(item, ("path", "sha256"), "evidence")
            relative = evidence_path(item["path"])
            if relative in seen or not isinstance(item["sha256"], str) or not HASH_PATTERN.fullmatch(item["sha256"]):
                fail("Invalid or duplicate evidence fingerprint")
            seen.add(relative)
        dates = [note[k] for k in ("created_at", "updated_at", "expires_at")]
        if any(type(value) is not int or not 0 <= value <= 253402300799 for value in dates):
            fail("Invalid note timestamps")
        if not dates[0] <= dates[1] <= dates[2] or dates[2] - dates[1] > MAX_TTL * 86400:
            fail("Invalid note expiration interval")
        provenance = note["provenance"]
        exact_keys(provenance, ("branch", "head"), "provenance")
        if provenance["branch"] is not None:
            text_field(provenance["branch"], 256, "Saved branch")
        if provenance["head"] is not None and (not isinstance(provenance["head"], str) or not GIT_HASH.fullmatch(provenance["head"])):
            fail("Invalid saved Git revision")
    return store


def metadata_dir(root):
    path = root / ".sdlc"
    if path.is_symlink():
        fail(".sdlc must not be a symlink")
    if not path.exists():
        return None
    if not path.is_dir():
        fail(".sdlc must be a directory")
    return path


class MetadataHandle:
    def __init__(self, root_fd, fd):
        self.root_fd = root_fd
        self.fd = fd

    def ensure_current(self):
        current = os.stat(".sdlc", dir_fd=self.root_fd, follow_symlinks=False)
        pinned = os.fstat(self.fd)
        if (not stat.S_ISDIR(current.st_mode)
                or (current.st_dev, current.st_ino) != (pinned.st_dev, pinned.st_ino)):
            fail(".sdlc was replaced during the operation; no writes follow its replacement")


@contextmanager
def metadata_handle(root, create=False):
    require_anchored_filesystem()
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    root_fd = os.open(root, flags)
    fd = None
    try:
        if create:
            try:
                os.mkdir(".sdlc", mode=0o700, dir_fd=root_fd)
            except FileExistsError:
                pass
        fd = os.open(".sdlc", flags, dir_fd=root_fd)
        handle = MetadataHandle(root_fd, fd)
        handle.ensure_current()
        yield handle
    finally:
        if fd is not None:
            os.close(fd)
        os.close(root_fd)


def no_duplicate_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            fail("Knowledge store contains duplicate JSON keys")
        value[key] = item
    return value


def load_store(root, handle=None):
    if handle is None:
        directory = metadata_dir(root)
        if directory is None:
            return None
    else:
        handle.ensure_current()
        directory = Path(".")
    try:
        data = bounded_bytes(directory / "knowledge.json", MAX_STORE_BYTES,
                             root if handle is None else None,
                             handle.fd if handle is not None else None)
    except FileNotFoundError:
        return None
    try:
        store = json.loads(data, object_pairs_hook=no_duplicate_keys)
    except (ValueError, UnicodeError, RecursionError) as exc:
        fail(f"Invalid knowledge JSON ({type(exc).__name__})")
    return validate_store(store, root)


@contextmanager
def write_lock(handle):
    lock = "knowledge.lock"
    deadline = time.monotonic() + 1.0
    while True:
        handle.ensure_current()
        try:
            os.mkdir(lock, mode=0o700, dir_fd=handle.fd)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                fail("Knowledge store is busy; retry later. Existing locks are never stolen")
            time.sleep(0.05)
    identity = os.stat(lock, dir_fd=handle.fd, follow_symlinks=False)
    try:
        handle.ensure_current()
        yield
    finally:
        current = os.stat(lock, dir_fd=handle.fd, follow_symlinks=False)
        if (not stat.S_ISDIR(current.st_mode)
                or (current.st_dev, current.st_ino) != (identity.st_dev, identity.st_ino)):
            fail("Owned lock was replaced; refusing to remove another owner's lock")
        os.rmdir(lock, dir_fd=handle.fd)


def atomic_save(handle, store):
    data = json.dumps(store, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(data) > MAX_STORE_BYTES:
        fail("Knowledge store exceeds 4 MiB; remove or shorten notes")
    handle.ensure_current()
    name = f".knowledge-{secrets.token_hex(16)}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    fd = os.open(name, flags, mode=0o600, dir_fd=handle.fd)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        handle.ensure_current()
        os.replace(name, "knowledge.json", src_dir_fd=handle.fd, dst_dir_fd=handle.fd)
        os.fsync(handle.fd)
        handle.ensure_current()
    finally:
        try:
            os.unlink(name, dir_fd=handle.fd)
        except FileNotFoundError:
            pass


def freshness(root, note):
    reasons = set()
    if int(time.time()) >= note["expires_at"]:
        reasons.add("expired")
    for item in note["evidence"]:
        try:
            if fingerprint(root, item["path"]) != item["sha256"]:
                reasons.add("evidence_changed")
        except FileNotFoundError:
            reasons.add("evidence_missing")
        except (OSError, KnowledgeError):
            reasons.add("evidence_unavailable_or_unsafe")
    return ("stale" if reasons else "fresh"), sorted(reasons)


def emit(value):
    print(json.dumps(value, ensure_ascii=False, separators=(",", ":")))


def read_note(root, note, allow_stale):
    status, reasons = freshness(root, note)
    result = {key: note[key] for key in ("id", "title", "summary", "updated_at", "provenance")}
    result.update(status=status, reasons=reasons, evidence_count=len(note["evidence"]))
    result["evidence_paths"] = [item["path"] for item in note["evidence"][:3]]
    result["evidence_paths_omitted"] = max(0, len(note["evidence"]) - 3)
    # Display only paths that fit; the stored evidence set remains complete.
    while len(json.dumps(result, ensure_ascii=False, separators=(",", ":"))) > MAX_READ_CHARS - 100:
        if not result["evidence_paths"]:
            fail("Note metadata exceeds the read output budget")
        result["evidence_paths"].pop()
        result["evidence_paths_omitted"] += 1
    if status == "stale" and not allow_stale:
        result["body_withheld"] = True
        emit(result)
        return 3
    result["body"] = note["body"]
    result["body_truncated"] = False
    # JSON escapes can make a 4,000-character body exceed the output budget.
    while len(json.dumps(result, ensure_ascii=False, separators=(",", ":"))) > MAX_READ_CHARS:
        result["body_truncated"] = True
        extra = len(json.dumps(result, ensure_ascii=False, separators=(",", ":"))) - MAX_READ_CHARS
        result["body"] = result["body"][:-max(1, extra)]
        if not result["body"] and len(json.dumps(result, ensure_ascii=False, separators=(",", ":"))) > MAX_READ_CHARS:
            fail("Note metadata exceeds the read output budget")
    emit(result)
    return 0


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo", required=True, help="Explicit repository root; storage stays in this root")
    commands = cli.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="At most 10 matching summaries, never bodies")
    listing.add_argument("--query", default="")
    reading = commands.add_parser("read", help="Read a note only if its recorded evidence is fresh")
    reading.add_argument("id")
    reading.add_argument("--allow-stale", action="store_true")
    saving = commands.add_parser("save", help="Save/replace one explicitly curated note")
    saving.add_argument("id")
    saving.add_argument("--title", required=True)
    saving.add_argument("--summary", required=True)
    saving.add_argument("--body-file", type=Path, required=True)
    saving.add_argument("--evidence", action="append", required=True)
    saving.add_argument("--ttl-days", type=int, default=30)
    deleting = commands.add_parser("delete", help="Delete one explicit ID without creating a missing store")
    deleting.add_argument("id")
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        root = Path(args.repo).resolve(strict=True)
        if not root.is_dir():
            fail("--repo must be an existing directory")
        if args.command == "list":
            if len(args.query) > 200:
                fail("Query must be at most 200 characters")
            store = load_store(root) or new_store(root)
            query = args.query.casefold()
            matches = [note for note in store["notes"].values()
                       if query in " ".join(note[key] for key in ("id", "title", "summary")).casefold()]
            matches.sort(key=lambda note: (-note["updated_at"], note["id"]))
            summaries = []
            for note in matches[:10]:
                status, reasons = freshness(root, note)
                summaries.append({**{key: note[key] for key in ("id", "title", "summary")},
                                  "status": status, "reasons": reasons})
            emit({"notes": summaries, "total_matches": len(matches)})
            return 0
        note_id(args.id)
        if args.command in ("read", "delete"):
            store = load_store(root)
            if store is None or args.id not in store["notes"]:
                fail("Note not found; no store was created")
            if args.command == "read":
                return read_note(root, store["notes"][args.id], args.allow_stale)
            with metadata_handle(root) as handle, write_lock(handle):
                store = load_store(root, handle)
                if store is None or args.id not in store["notes"]:
                    fail("Note no longer exists")
                del store["notes"][args.id]
                atomic_save(handle, store)
            emit({"id": args.id, "deleted": True})
            return 0
        title = text_field(args.title, MAX_TITLE, "Title")
        summary = text_field(args.summary, MAX_SUMMARY, "Summary")
        body = bounded_bytes(args.body_file, MAX_BODY * 4).decode("utf-8")
        text_field(body, MAX_BODY, "Body", multiline=True)
        check_secrets(title, summary, body)
        if not 1 <= len(args.evidence) <= MAX_EVIDENCE or len(set(args.evidence)) != len(args.evidence):
            fail("Save requires 1–32 distinct evidence paths")
        if not 1 <= args.ttl_days <= MAX_TTL:
            fail("TTL must be 1–3650 days")
        evidence = [{"path": evidence_path(value), "sha256": fingerprint(root, value)} for value in args.evidence]
        with metadata_handle(root, create=True) as handle, write_lock(handle):
            store = load_store(root, handle) or new_store(root)
            replacing = args.id in store["notes"]
            if not replacing and len(store["notes"]) >= MAX_NOTES:
                fail("Knowledge store has 100 notes; delete one or replace an explicit ID")
            now = int(time.time())
            note = {"id": args.id, "title": title, "summary": summary, "body": body,
                    "evidence": evidence, "created_at": store["notes"].get(args.id, {}).get("created_at", now),
                    "updated_at": now, "expires_at": now + args.ttl_days * 86400,
                    "provenance": git_provenance(root)}
            store["notes"][args.id] = note
            validate_store(store, root)
            atomic_save(handle, store)
        emit({"id": args.id, "saved": True, "replaced": replacing, "evidence_count": len(evidence)})
        return 0
    except (KnowledgeError, OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(f"knowledge: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
