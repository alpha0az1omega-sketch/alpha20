#!/bin/bash
# run_demo.sh — end-to-end test of the Alpha-20 compiler.
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/4] Compiling kinematic.alpha -> python"
python3 compiler/alpha20_compiler.py examples/kinematic.alpha --target python --out examples/kinematic.py

echo "[2/4] Compiling kinematic.alpha -> svg"
python3 compiler/alpha20_compiler.py examples/kinematic.alpha --target svg --out examples/kinematic.svg

echo "[3/4] Compiling kinematic.alpha -> sonification JSON"
python3 compiler/alpha20_compiler.py examples/kinematic.alpha --target son --out examples/kinematic.son.json

echo "[4/4] Executing generated Python"
python3 examples/kinematic.py

echo "--- Artifacts ---"
ls -la examples/
