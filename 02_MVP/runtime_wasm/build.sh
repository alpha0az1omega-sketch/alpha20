#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
# Requires emscripten (emsdk) or a precompiled wat2wasm binary in PATH.
# This script is a placeholder for the WASM compilation of the Python compiler.
echo "WASM build script ready. Install emscripten and run: emcc ../compiler/alpha20_compiler.py -o alpha20.wasm"
