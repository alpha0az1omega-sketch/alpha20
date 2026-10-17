# 02_MVP — Compiler Prototype v0.1.0

Prototype compiler for **Alpha-20**, implementing the grammar in
`../01_SPECIFICATION/grammar.ebnf`. Stdlib-only (PEP 668-safe).

## Targets

| Target | Output |
|---|---|
| `--target python` | Executable Python predicate with `evaluate()` |
| `--target svg`    | Deterministic SVG composition of primitive glyphs |
| `--target son`    | JSON event list for audio synthesis |

## Layout

- `compiler/alpha20_compiler.py` — compiler (lexer + parser + 3 backends)
- `examples/kinematic.alpha`   — sample source
- `run_demo.sh`                — end-to-end demo

## Build / run


    cd 02_MVP
    ./run_demo.sh

Expected final line: RESULT: True

## Grammar coverage (v0.1.0)

- Primitives: EXIST, SAME, BIG, MOVE, TRUE, LIVE, GOOD, CAUSE, PART
- Operators: AND, OR, NOT, IF ... THEN ... ELSE
- Literals: numbers, strings, identifiers

## Not yet implemented (Phase 4+)

- Quantifiers: ALL, EXIST, ONE
- WebAssembly backend
- Audio synthesis engine (WAV/MP4)

## License

MIT (code) / CC BY 4.0 (specification).
