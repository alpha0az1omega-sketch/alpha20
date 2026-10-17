#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
# Install AssemblyScript compiler locally if not present
if ! command -v npx &> /dev/null; then
  echo "npx not found. Install Node.js first."
  exit 1
fi
npx --yes assemblyscript@latest init . --yes
# The actual compiler logic would be in assembly/index.ts (not included here).
# This script sets up the toolchain.
echo "AssemblyScript toolchain ready."
echo "Next: write assembly/index.ts with the Alpha-20 parser, then run: npm run asbuild"
