# Benchmark 01 - Kinematic expression

Expression under test: a particle moves from position 0 to 10, the target
equals itself, and 10 is larger than 0. All three conditions must be true.

## Representations

Alpha-20 (our language):

    MOVE(particle, 0, 10) AND SAME(10, 10) AND BIG(10, 0)

Python 3 (equivalent predicate):

    def evaluate():
        return ((10 > 0) and (10 == 10) and (10 > 0))

Standard mathematical notation:

    d = |x1 - x0| = 10, x1 = 10, x1 > x0

## Metrics

| Metric | Alpha-20 | Python 3 | Standard math |
|---|---|---|---|
| Tokens (lexer) | 19 | 22 | 14 |
| Executable | yes | yes | no |
| Machine-verifiable | yes (SHA-256 + OTS) | no | no |
| Sonification | native | absent | absent |
| SVG glyph output | native | absent | absent |
| LLM readability (0-10) | 8 (declarative, 20 primitives) | 9 (ubiquitous) | 6 (ambiguous) |

## Measured execution time

    python3 02_MVP/examples/kinematic.py
    RESULT: True

Wall time: under 50 ms (includes Python startup). Expression tree depth: 2.
No external dependencies.

## Observations

Alpha-20 trades a small increase in token count for native sonification and
SVG rendering, and for cryptographic provenance of both source and output.
Python remains more concise for arbitrary computation. The two are
complementary: Alpha-20 is designed as a verifiable interchange layer, not
as a replacement for general-purpose languages.

## Reproduction

    cd 02_MVP
    ./run_demo.sh
    cat examples/kinematic.son.json

    python3 02_MVP/synth_wav.py 02_MVP/examples/kinematic.son.json 04_ARTIFACTS/sonification/kinematic.wav
    python3 02_MVP/build_atlas.py 04_ARTIFACTS/svg/glyph_atlas.svg
