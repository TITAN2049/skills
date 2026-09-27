#!/usr/bin/env python3
"""Report static context size; character counts are not measured model tokens."""
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    roles = json.loads((ROOT / "catalog.json").read_text())["roles"]
    descriptions = []
    instructions = []
    for role in roles:
        skill = ROOT / "skills" / role["skill"] / "SKILL.md"
        raw = skill.read_text().split("description: ", 1)[1].splitlines()[0]
        descriptions.append(len(json.loads(raw) if raw.startswith('"') else raw))
        agent = ROOT / "agents" / (role["skill"].replace("-", "_") + ".toml")
        instructions.append(len(tomllib.loads(agent.read_text())["developer_instructions"]))
    print(json.dumps({
        "roles": len(roles),
        "discovery_description_characters": sum(descriptions),
        "longest_description_characters": max(descriptions),
        "mean_agent_instruction_characters": round(sum(instructions) / len(instructions)),
        "shared_collaboration_characters": len((ROOT / "shared/collaboration.md").read_text()),
        "limits": "Static characters only; excludes host instructions, paths, tool output, execution, and model-specific tokenization."
    }, indent=2))


if __name__ == "__main__":
    main()
