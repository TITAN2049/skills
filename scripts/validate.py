#!/usr/bin/env python3
"""Validate this package's constrained metadata, references, and generated TOML."""
import json
from pathlib import Path
import re
import sys
import tomllib

from build import ROOT, generated_files


def metadata(text):
    """Read the single-line string frontmatter used by this package (not general YAML)."""
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0]:
        raise ValueError("Expected opening YAML frontmatter")
    values = {}
    for line in parts[1].splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in values:
            raise ValueError(f"Invalid or duplicate metadata: {line}")
        value = value.strip()
        if value.startswith('"'):
            value = json.loads(value)
        elif ": " in value or value.startswith(("'", "[", "{", "|", ">", "&", "*", "!")):
            raise ValueError("Use a JSON-quoted single-line string for complex metadata")
        values[key] = value
    return values, parts[2]


def validate():
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    roles = catalog["roles"]
    names = [role["skill"] for role in roles]
    errors = []
    if len(set(names)) != len(names):
        errors.append("Duplicate skill names")
    actual = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    if actual != set(names):
        errors.append(f"Skill/catalog mismatch: {actual ^ set(names)}")
    for role in roles:
        name = role["skill"]
        try:
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                raise ValueError("Invalid skill name")
            path = ROOT / "skills" / name / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            front, body = metadata(text)
            if set(front) != {"name", "description"} or front["name"] != name:
                raise ValueError("Skill frontmatter does not match directory")
            description = front["description"]
            if not isinstance(description, str) or not 1 <= len(description) <= 1024:
                raise ValueError("Description must have 1–1024 characters")
            if len(body.strip()) < 100 or re.search(r"\b(TODO|TBD|FIXME)\b", body):
                raise ValueError("Empty or unfinished skill body")
            if not 25 <= len(role["summary"]) <= 64:
                raise ValueError("UI summary must have 25–64 characters")
            if "$" + name not in role["prompt"]:
                raise ValueError("Default prompt must invoke its skill")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
                if "://" not in target and not target.startswith("#"):
                    if not (path.parent / target.split("#")[0]).is_file():
                        raise ValueError(f"Broken reference: {target}")
            agent_name = name.replace("-", "_")
            config = tomllib.loads((ROOT / "agents" / f"{agent_name}.toml").read_text(encoding="utf-8"))
            if set(config) != {"name", "description", "developer_instructions"}:
                raise ValueError("Unexpected role overrides or missing native agent fields")
            if config["name"] != agent_name or "$" + name not in config["developer_instructions"]:
                raise ValueError("Role-to-skill mapping mismatch")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"{name}: {exc}")
    expected_agents = {name.replace("-", "_") for name in names}
    if {p.stem for p in (ROOT / "agents").glob("*.toml")} != expected_agents:
        errors.append("Agent directory differs from catalog")
    for path, content in generated_files():
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            errors.append(f"Generated file stale: {path.relative_to(ROOT)}")
    manager = (ROOT / "skills/sdlc-manager/SKILL.md").read_text(encoding="utf-8")
    for name in names:
        if name != "sdlc-manager" and ("$" + name not in manager or name.replace("-", "_") not in manager):
            errors.append(f"Manager routing missing: {name}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(roles)} skills, native agents, UI metadata, references, and manager routes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
