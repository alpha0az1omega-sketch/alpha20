# ALPHA-20

Universal Executable, Sonorous, and Cryptographic Language.

Alpha-20 is a formal language built on 20 semantic primitives across 5 layers
(L0-L4). It compiles to Python and WebAssembly, renders deterministic SVG glyphs,
synthesizes audio via the Web Audio API, and seals every state change with
SHA-256 and OpenTimestamps.

## Quick Start

    git clone <your-repo-url>
    cd alpha20
    python3 02_MVP/run_demo.sh

## Verification

    shasum -a 256 -c 00_MANIFEST/manifest_sha256.txt
    gpg --verify 00_MANIFEST/manifest_sha256.txt.asc 00_MANIFEST/manifest_sha256.txt
    ots verify 00_MANIFEST/manifest_sha256.txt.ots

## Agentic Glyph

Open `04_ARTIFACTS/svg/glyph_agentic_v2.svg` in a browser (via `python3 -m http.server 8765` for full functionality).
Click `EVALUATE + PLAY` to execute and hear an expression, then `SEAL` to hash the state.

## License

CC BY 4.0 (specification) / MIT (code).
