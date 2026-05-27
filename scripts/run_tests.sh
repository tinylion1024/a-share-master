#!/bin/sh
set -eu

export PYTHONDONTWRITEBYTECODE=1

TARGET="${1:-tests/skills}"
shift || true

if python3 -m pytest --version >/dev/null 2>&1; then
  python3 -m pytest "$TARGET" "$@"
else
  case "$TARGET" in
    *.py)
      MODULE=$(printf '%s' "$TARGET" | sed 's#^./##; s#/#.#g; s#\.py$##')
      python3 -m unittest "$MODULE"
      ;;
    *)
      python3 -m unittest discover -s "$TARGET" -p 'test_*.py'
      ;;
  esac
fi
