#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
# Requires emsdk activated (source /path/to/emsdk/emsdk_env.sh)
# Compile a minimal C interpreter (to be written) to WASM.
echo "Place alpha20_interpreter.c here, then run:"
echo "emcc alpha20_interpreter.c -O3 -s WASM=1 -o alpha20.js"
