#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
# Requires elan (Lean version manager) and lake.
# Install: curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
echo "Build TAM20.lean with: lake build"
echo "This requires Lean 4 + Mathlib (large download)."
