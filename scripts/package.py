#!/usr/bin/env python3
"""Build a portable toolkit ZIP after validating the source package."""
from pathlib import Path
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/validate.py")], check=True)
    output = ROOT / "dist/codex-sdlc-toolkit.zip"
    output.parent.mkdir(exist_ok=True)
    files = [ROOT / name for name in ("README.md", "catalog.json", "install.sh", ".gitignore")]
    for name in ("skills", "agents", "scripts", "shared", "tests", "docs", "evals"):
        files.extend(path for path in (ROOT / name).rglob("*")
                     if path.is_file() and path.name != ".DS_Store"
                     and "__pycache__" not in path.parts and path.suffix != ".pyc")
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(files):
            if path.is_symlink():
                raise ValueError(f"Do not package source symlinks: {path}")
            archive.write(path, str(Path("codex-sdlc-toolkit") / path.relative_to(ROOT)))
    with ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
    print(f"Packaged {len(files)} files: {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
