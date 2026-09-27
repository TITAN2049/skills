#!/usr/bin/env bash
# Run from any working directory: bash /path/to/toolkit/install.sh --project /path/to/app
set -euo pipefail

SDLC_SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'HELP'
Install the Codex SDLC toolkit (macOS, Linux, WSL, or Git Bash).

  bash install.sh                         Install for your user account
  bash install.sh --project /path/to/app   Install for one existing project
  bash install.sh --user --dry-run        Preview a personal installation
  bash install.sh --project . --doctor    Check an installation without writes
  bash install.sh --user --update         Update unmodified managed files
  bash install.sh --user --uninstall      Remove unmodified managed files

Requires Python 3.11+. No downloads, sudo, pip packages, or config rewrites.
Set SDLC_PYTHON to a Python executable path if it is not on PATH.
Start a new Codex conversation in VS Code after installation.
HELP
  exit 0
fi

SDLC_PYTHON_EXECUTABLE=""
sdlc_python_supported() {
  local SDLC_PROBE_OUTPUT
  SDLC_PROBE_OUTPUT=$("$1" -c 'import sys; sys.exit(1) if sys.version_info < (3, 11) else None; print("sdlc-python-ok")' 2>/dev/null) || return 1
  [[ "$SDLC_PROBE_OUTPUT" == "sdlc-python-ok" ]]
}

if [[ -n "${SDLC_PYTHON:-}" ]]; then
  if sdlc_python_supported "$SDLC_PYTHON"; then
    SDLC_PYTHON_EXECUTABLE="$SDLC_PYTHON"
  else
    printf '%s\n' 'SDLC_PYTHON must point to a working Python 3.11+ executable.' >&2
    exit 1
  fi
else
  for SDLC_CANDIDATE in python3 python; do
    if command -v "$SDLC_CANDIDATE" >/dev/null 2>&1 && sdlc_python_supported "$SDLC_CANDIDATE"; then
      SDLC_PYTHON_EXECUTABLE="$SDLC_CANDIDATE"
      break
    fi
  done
fi

if [[ -z "$SDLC_PYTHON_EXECUTABLE" ]]; then
  printf '%s\n' 'Python 3.11+ was not found. Install it from https://www.python.org/downloads/,' \
    'then rerun this command, or set SDLC_PYTHON to its executable path.' >&2
  exit 1
fi

# Default to personal scope, including for --doctor/--update/--dry-run.
SDLC_HAS_SCOPE=false
for SDLC_ARGUMENT in "$@"; do
  case "$SDLC_ARGUMENT" in
    --user|--project|--project=*) SDLC_HAS_SCOPE=true ;;
  esac
done
if [[ "$SDLC_HAS_SCOPE" == false ]]; then
  set -- --user "$@"
fi

exec "$SDLC_PYTHON_EXECUTABLE" "$SDLC_SCRIPT_DIR/scripts/install.py" "$@"
