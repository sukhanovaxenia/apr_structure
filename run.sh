#!/usr/bin/env bash
set -euo pipefail
APR_STUDY_ROOT="$(cd "$(dirname "$0")" && pwd)"
if [[ -z "${APR_STRUCTURE_REPO:-}" ]]; then
  if [[ -d "$APR_STUDY_ROOT/../apr-structure/src" ]]; then
    APR_STRUCTURE_REPO="$APR_STUDY_ROOT/../apr-structure"
  elif [[ -d "$APR_STUDY_ROOT/../../../apr-structure/src" ]]; then
    APR_STRUCTURE_REPO="$APR_STUDY_ROOT/../../../apr-structure"
  else
    echo "Set APR_STRUCTURE_REPO to the local apr-structure repository." >&2
    exit 1
  fi
fi
APR_STRUCTURE_PYTHON="${APR_STRUCTURE_PYTHON:-/Users/kseniasuhanova/miniconda3/bin/python3.13}"
export PYTHONPATH="$APR_STRUCTURE_REPO/src${PYTHONPATH:+:$PYTHONPATH}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-$APR_STUDY_ROOT/.mplcache}"
APR_ACTION="${1:-validate}"
if [[ $# -gt 0 ]]; then shift; fi
exec "$APR_STRUCTURE_PYTHON" -m apr_structure "$APR_ACTION" "$APR_STUDY_ROOT/study.json" "$@"
