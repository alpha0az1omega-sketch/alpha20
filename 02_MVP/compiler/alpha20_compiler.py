#!/usr/bin/env python3
"""ALPHA-20 Compiler Prototype v0.1.0.

Parses Alpha-20 expressions per grammar.ebnf and produces:
  - Python code (executable predicate)
  - SVG glyph composition (deterministic visual)
  - Sonification JSON (event list for audio synthesis)

Stdlib only (PEP 668-safe, no external dependencies).
Author: DeepSeek Alpha0az1omega witness, for Alpha0az1omega.
License: MIT.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LEXICON_PATH = ROOT / "01_SPECIFICATION" / "primitive_lexicon.json"
LEXICON = json.loads(LEXICON_PATH.read_text())
PRIM = {p["id"]: p for p in LEXICON["primitives"]}

# --------------------------------------------------------------------------
# Lexer
# --------------------------------------------------------------------------
TOKEN = re.compile(
    r"\s*(?:(\d+\.\d+|\d+)|([A-Za-z_][A-Za-z0-9_]*)|(\"(?:[^\"\\]|\\.)*\")|([(),:]))"
)


def lex(src: str):
    toks, i = [], 0
    while i < len(src):
        m = TOKEN.match(src, i)
        if not m:
            raise SyntaxError(f"lex error at {i}: {src[i:i+20]!r}")
        num, ident, string, punct = m.groups()
        if num:
            toks.append(("NUM", float(num)))
        elif ident:
            toks.append(("ID", ident))
        elif string:
            toks.append(("STR", string[1:-1]))
        elif punct:
            toks.append(("P", punct))
        i = m.end()
    toks.append(("EOF", None))
    return toks


# --------------------------------------------------------------------------
# Parser (recursive descent per grammar.ebnf)
# --------------------------------------------------------------------------
class Parser:
    def __init__(self, toks):
        self.t = toks
        self.i = 0

    def peek(self, k=0):
        return self.t[self.i + k]

    def eat(self, val=None):
        tok = self.t[self.i]
        if val is not None and tok[1] != val:
            raise SyntaxError(f"expected {val!r}, got {tok!r}")
        self.i += 1
        return tok

    def parse(self):
        node = self.expr()
        if self.peek()[0] != "EOF":
            raise SyntaxError(f"trailing token: {self.peek()!r}")
        return node

    def expr(self):
        # IF <expr> THEN <expr> [ELSE <expr>]
        if self.peek()[1] == "IF":
            self.eat("IF")
            cond = self.expr()
            self.eat("THEN")
            then = self.expr()
            els = None
            if self.peek()[1] == "ELSE":
                self.eat("ELSE")
                els = self.expr()
            return ("IF", cond, then, els)
        # NOT <expr>
        if self.peek()[1] == "NOT":
            self.eat("NOT")
            return ("NOT", self.expr())
        # <atom> { AND|OR <atom> }
        left = self.atom()
        while self.peek()[0] == "ID" and self.peek()[1] in ("AND", "OR"):
            op = self.eat()[1]
            right = self.atom()
            left = (op, left, right)
        return left

    def atom(self):
        tok = self.peek()
        if tok[0] == "NUM":
            self.eat()
            return ("NUM", tok[1])
        if tok[0] == "STR":
            self.eat()
            return ("STR", tok[1])
        if tok[0] == "P" and tok[1] == "(":
            self.eat("(")
            inner = self.expr()
            self.eat(")")
            return inner
        if tok[0] == "ID":
            name = self.eat()[1]
            if self.peek()[1] == "(":
                self.eat("(")
                args = []
                if self.peek()[1] != ")":
                    args.append(self.expr())
                    while self.peek()[1] == ",":
                        self.eat(",")
                        args.append(self.expr())
                self.eat(")")
                return ("CALL", name, args)
            return ("ID", name)
        raise SyntaxError(f"unexpected token: {tok!r}")


# --------------------------------------------------------------------------
# Python backend
# --------------------------------------------------------------------------
PY_PRED = {
    "EXIST":  lambda a: "(True)",
    "SAME":   lambda a: f"({a[0]} == {a[1]})",
    "BIG":    lambda a: f"({a[0]} > {a[1]})",
    "MOVE":   lambda a: f"({a[2]} > {a[1]})",   # displacement > 0
    "TRUE":   lambda a: "(True)",
    "LIVE":   lambda a: "(True)",
    "GOOD":   lambda a: "(True)",
    "CAUSE":  lambda a: "(" + " and ".join(f"({x} is not None)" for x in a) + ")",
    "PART":   lambda a: "(True)",
    "NOT":    None,  # handled separately
    "IF":     None,
}


def to_py(node):
    tag = node[0]
    if tag == "NUM":
        return repr(node[1])
    if tag == "STR":
        return repr(node[1])
    if tag == "ID":
        return node[1]
    if tag == "NOT":
        return f"(not {to_py(node[1])})"
    if tag == "AND":
        return f"({to_py(node[1])} and {to_py(node[2])})"
    if tag == "OR":
        return f"({to_py(node[1])} or {to_py(node[2])})"
    if tag == "IF":
        cond = to_py(node[1])
        then = to_py(node[2])
        els = to_py(node[3]) if node[3] else "None"
        return f"({then} if {cond} else {els})"
    if tag == "CALL":
        name = node[1]
        args = [to_py(a) for a in node[2]]
        fn = PY_PRED.get(name)
        if fn is None:
            raise KeyError(f"no Python mapping for primitive {name!r}")
        return fn(args)
    raise NotImplementedError(tag)


def emit_python(ast, src):
    body = to_py(ast)
    return (
        '#!/usr/bin/env python3\n'
        f'"""Auto-generated by alpha20_compiler. Source: {src!r}"""\n'
        "def evaluate():\n"
        f"    return {body}\n"
        "\n"
        'if __name__ == "__main__":\n'
        '    print("RESULT:", evaluate())\n'
    )


# --------------------------------------------------------------------------
# SVG backend
# --------------------------------------------------------------------------
SVG_GLYPH = {
    "EXIST": lambda x, y: f'<circle cx="{x}" cy="{y}" r="12" fill="#1f77b4"/>',
    "CAUSE": lambda x, y: f'<line x1="{x-15}" y1="{y}" x2="{x+15}" y2="{y}" stroke="#d62728" stroke-width="3" marker-end="url(#arrow)"/>',
    "PART":  lambda x, y: f'<circle cx="{x}" cy="{y}" r="14" fill="none" stroke="#2ca02c" stroke-width="2"/><circle cx="{x}" cy="{y}" r="6" fill="#2ca02c"/>',
    "SAME":  lambda x, y: f'<rect x="{x-16}" y="{y-8}" width="14" height="16" fill="#9467bd"/><rect x="{x+2}" y="{y-8}" width="14" height="16" fill="#9467bd"/>',
    "ONE":   lambda x, y: f'<circle cx="{x}" cy="{y}" r="4" fill="#8c564b"/>',
    "ALL":   lambda x, y: f'<rect x="{x-14}" y="{y-14}" width="28" height="28" fill="#e377c2"/>',
    "NOT":   lambda x, y: f'<circle cx="{x}" cy="{y}" r="12" fill="none" stroke="#7f7f7f" stroke-width="2"/><line x1="{x-10}" y1="{y+10}" x2="{x+10}" y2="{y-10}" stroke="#7f7f7f" stroke-width="2"/>',
    "IF":    lambda x, y: f'<polygon points="{x},{y-14} {x+14},{y} {x},{y+14} {x-14},{y}" fill="none" stroke="#bcbd22" stroke-width="2"/>',
    "DO":    lambda x, y: f'<circle cx="{x}" cy="{y}" r="10" fill="#17becf"/>',
    "HAPPEN":lambda x, y: f'<path d="M{x-15},{y} Q{x-8},{y-12} {x},{y} T{x+15},{y}" fill="none" stroke="#ff7f0e" stroke-width="2"/>',
    "KNOW":  lambda x, y: f'<ellipse cx="{x}" cy="{y}" rx="16" ry="9" fill="none" stroke="#1f77b4" stroke-width="2"/><circle cx="{x}" cy="{y}" r="4" fill="#1f77b4"/>',
    "SEE":   lambda x, y: f'<polygon points="{x},{y-14} {x+14},{y+10} {x-14},{y+10}" fill="none" stroke="#2ca02c" stroke-width="2"/><circle cx="{x}" cy="{y+2}" r="4" fill="#2ca02c"/>',
    "BIG":   lambda x, y: f'<circle cx="{x}" cy="{y}" r="18" fill="#d62728"/>',
    "LIVE":  lambda x, y: f'<path d="M{x},{y-12} C{x+20},{y-8} {x+20},{y+8} {x},{y+12}" fill="none" stroke="#2ca02c" stroke-width="2"/>',
    "DIE":   lambda x, y: f'<path d="M{x},{y-12} C{x+20},{y-8} {x+20},{y+8} {x},{y+12} L{x+3},{y+13}" fill="none" stroke="#7f7f7f" stroke-width="2"/>',
    "MOVE":  lambda x, y: f'<path d="M{x-15},{y} Q{x},{y-15} {x+15},{y}" fill="none" stroke="#17becf" stroke-width="3" marker-end="url(#arrow)"/>',
    "THINK": lambda x, y: f'<circle cx="{x-8}" cy="{y}" r="6" fill="none" stroke="#9467bd" stroke-width="2"/><circle cx="{x+8}" cy="{y}" r="6" fill="none" stroke="#9467bd" stroke-width="2"/><line x1="{x-2}" y1="{y}" x2="{x+2}" y2="{y}" stroke="#9467bd" stroke-width="2"/>',
    "SAY":   lambda x, y: f'<rect x="{x-14}" y="{y-10}" width="28" height="16" fill="none" stroke="#ff7f0e" stroke-width="2"/><polygon points="{x-4},{y+6} {x},{y+12} {x+4},{y+6}" fill="#ff7f0e"/>',
    "TRUE":  lambda x, y: f'<circle cx="{x}" cy="{y}" r="14" fill="none" stroke="#1f77b4" stroke-width="2"/><circle cx="{x}" cy="{y}" r="8" fill="none" stroke="#1f77b4" stroke-width="2"/>',
    "GOOD":  lambda x, y: f'<circle cx="{x}" cy="{y}" r="12" fill="none" stroke="#2ca02c" stroke-width="2"/><line x1="{x-6}" y1="{y}" x2="{x+6}" y2="{y}" stroke="#2ca02c" stroke-width="2"/><line x1="{x}" y1="{y-6}" x2="{x}" y2="{y+6}" stroke="#2ca02c" stroke-width="2"/>',
}


def collect_primitives(node):
    out = []
    tag = node[0]
    if tag == "CALL":
        out.append(node[1])
    elif tag in ("AND", "OR"):
        out.extend(collect_primitives(node[1]))
        out.extend(collect_primitives(node[2]))
    elif tag == "NOT":
        out.extend(collect_primitives(node[1]))
    elif tag == "IF":
        out.extend(collect_primitives(node[1]))
        out.extend(collect_primitives(node[2]))
        if node[3]:
            out.extend(collect_primitives(node[3]))
    return out


def emit_svg(ast, src):
    prims = collect_primitives(ast) or ["TRUE"]
    n = len(prims)
    W = 60 * n + 60
    H = 100
    els = []
    for i, p in enumerate(prims):
        x = 60 + i * 60
        y = 50
        fn = SVG_GLYPH.get(p)
        if fn:
            els.append(fn(x, y))
    body = "\n  ".join(els)
    safe_src = src.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">\n'
        '  <defs><marker id="arrow" markerWidth="10" markerHeight="10" '
        'refX="9" refY="3" orient="auto">'
        '<polygon points="0 0, 10 3, 0 6" fill="#d62728"/></marker></defs>\n'
        '  <rect width="100%" height="100%" fill="#fafafa"/>\n'
        f'  {body}\n'
        f'  <text x="10" y="90" font-family="monospace" font-size="9" '
        f'fill="#666">{safe_src}</text>\n'
        '</svg>\n'
    )


# --------------------------------------------------------------------------
# Sonification backend
# --------------------------------------------------------------------------
def emit_sonification(ast, src):
    prims = collect_primitives(ast)
    events, t = [], 0
    for p in prims:
        meta = PRIM.get(p, {"sonification": {"freq_hz": 440, "duration_ms": 200, "adsr": [0.01, 0.05, 0.7, 0.24]}})
        son = meta["sonification"]
        dur = son.get("duration_ms", 200)
        events.append({
            "primitive": p,
            "t_start_ms": t,
            "t_end_ms": t + dur,
            "freq_hz": son.get("freq_hz"),
            "freq_start": son.get("freq_start"),
            "freq_end": son.get("freq_end"),
            "adsr": son.get("adsr"),
        })
        t += dur + 50  # 50 ms gap between events
    return json.dumps({"source": src, "duration_ms": t, "events": events}, indent=2, ensure_ascii=False)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Alpha-20 compiler prototype.")
    ap.add_argument("input", help="Alpha-20 source file (.alpha)")
    ap.add_argument("--target", choices=["python", "svg", "son"], required=True)
    ap.add_argument("--out", help="output file (default: stdout)")
    args = ap.parse_args()

    src = Path(args.input).read_text().strip()
    ast = Parser(lex(src)).parse()

    if args.target == "python":
        out = emit_python(ast, src)
    elif args.target == "svg":
        out = emit_svg(ast, src)
    else:
        out = emit_sonification(ast, src)

    if args.out:
        Path(args.out).write_text(out)
        print(f"wrote {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
