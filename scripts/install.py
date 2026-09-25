#!/usr/bin/env python3
"""Install this toolkit for one project or your user account (Python 3.11+)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(".codex/sdlc-toolkit-manifest.json")


class InstallError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def payload():
    """Only install the catalog's skills and matching native agent definitions."""
    for directory in (ROOT / "skills", ROOT / "agents"):
        if directory.is_symlink():
            raise InstallError(f"Source symlink is unsupported: {directory}")
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    files = {}
    for role in catalog["roles"]:
        name = role["skill"]
        source = ROOT / "skills" / name
        if source.is_symlink():
            raise InstallError(f"Source symlink is unsupported: {source}")
        if not (source / "SKILL.md").is_file():
            raise InstallError(f"Missing skill: {name}")
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise InstallError(f"Source symlink is unsupported: {path}")
            if path.is_file():
                rel = Path(".agents/skills") / name / path.relative_to(source)
                files[rel.as_posix()] = path.read_bytes()
        agent = name.replace("-", "_") + ".toml"
        agent_path = ROOT / "agents" / agent
        if agent_path.is_symlink():
            raise InstallError(f"Source symlink is unsupported: {agent_path}")
        files[(Path(".codex/agents") / agent).as_posix()] = agent_path.read_bytes()
    return catalog["version"], files


def safe_path(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise InstallError(f"Unsafe path in installation: {relative}")
    current = root
    for index, part in enumerate(rel.parts):
        current = current / part
        if current.is_symlink():
            raise InstallError(f"Refusing to follow destination symlink: {current}")
        if current.exists() and index < len(rel.parts) - 1 and not current.is_dir():
            raise InstallError(f"Destination parent is not a directory: {current}")
    if current.exists() and not current.is_file():
        raise InstallError(f"Destination is not a regular file: {current}")
    return current


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".sdlc-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_manifest(path, allowed):
    if not path.exists():
        return {}
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
        files = content["files"]
        if content.get("format") != 1 or not isinstance(files, dict):
            raise ValueError("Unrecognized format")
        for rel, sha in files.items():
            if rel not in allowed or not isinstance(sha, str) or len(sha) != 64:
                raise ValueError(f"Unrecognized managed entry: {rel}")
        return files
    except (KeyError, ValueError, TypeError) as exc:
        raise InstallError(f"Invalid manifest {path}: {exc}") from exc


def run(root, *, dry_run=False, update=False, uninstall=False):
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise InstallError(f"Target must be an existing directory: {root}")
    version, files = payload()
    manifest_path = safe_path(root, MANIFEST)
    previous = read_manifest(manifest_path, files)
    operations = []
    owned = dict(previous)
    conflicts = []
    preserved = []
    keys = previous if uninstall else files
    # Check every destination before any writes or deletes.
    for rel in keys:
        path = safe_path(root, rel)
        current = path.read_bytes() if path.exists() else None
        if uninstall:
            if current is None:
                owned.pop(rel, None)
            elif digest(current) == previous[rel]:
                operations.append(("REMOVE", path, None))
                owned.pop(rel, None)
            else:
                preserved.append(rel)
            continue
        desired = files[rel]
        if current == desired:
            if rel in previous:
                owned[rel] = digest(desired)
        elif current is None:
            operations.append(("CREATE", path, desired))
            owned[rel] = digest(desired)
        elif update and rel in previous and digest(current) == previous[rel]:
            operations.append(("UPDATE", path, desired))
            owned[rel] = digest(desired)
        else:
            conflicts.append(rel)
    if conflicts:
        raise InstallError(
            "No files changed. Existing files differ:\n  " + "\n  ".join(conflicts)
            + "\nUse --update for unchanged files from an earlier toolkit installation. "
            "For local edits or unowned files, compare and merge manually first."
        )
    for action, path, _ in operations:
        print(f"{'WOULD ' if dry_run else ''}{action} {path.relative_to(root)}")
    for rel in preserved:
        print(f"PRESERVE locally edited file: {rel}")
    if not dry_run:
        for action, path, data in operations:
            if action == "REMOVE":
                path.unlink()
            else:
                atomic_write(path, data)
        if owned or not uninstall:
            content = {"format": 1, "version": version, "files": owned}
            encoded = (json.dumps(content, indent=2, sort_keys=True) + "\n").encode()
            if not manifest_path.exists() or manifest_path.read_bytes() != encoded:
                atomic_write(manifest_path, encoded)
        elif manifest_path.exists():
            manifest_path.unlink()
    verb = "Uninstall" if uninstall else "Install"
    print(f"{verb} {'preview' if dry_run else 'complete'}: {len(operations)} file changes; target {root}")
    if preserved:
        print("Edited files and their manifest entries remain; no local edits were deleted.")
    return len(operations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, help="Existing repository root")
    scope.add_argument("--user", action="store_true", help="Install in ~/.agents and ~/.codex")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changing files")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--update", action="store_true", help="Update only unmodified managed files")
    mode.add_argument("--uninstall", action="store_true", help="Remove only unmodified managed files")
    args = parser.parse_args()
    try:
        run(Path.home() if args.user else args.project, dry_run=args.dry_run,
            update=args.update, uninstall=args.uninstall)
    except (InstallError, OSError) as exc:
        parser.exit(1, f"Installation stopped: {exc}\n")


if __name__ == "__main__":
    main()
