#!/usr/bin/env python3
"""Generate 04_ARTIFACTS/svg/glyph_atlas.svg - 4x5 grid of all 20 primitives."""
import json
import sys
from pathlib import Path

LEX = json.loads(Path("01_SPECIFICATION/primitive_lexicon.json").read_text())
CELL, COLS, ROWS = 140, 4, 5
W, H = COLS * CELL, ROWS * CELL + 40

def glyph(pid, cx, cy):
    table = {
        "EXIST": f'<circle cx="{cx}" cy="{cy}" r="20" fill="#1f77b4"/>',
        "CAUSE": f'<line x1="{cx-25}" y1="{cy}" x2="{cx+25}" y2="{cy}" stroke="#d62728" stroke-width="4" marker-end="url(#a)"/>',
        "PART":  f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="#2ca02c" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="10" fill="#2ca02c"/>',
        "SAME":  f'<rect x="{cx-26}" y="{cy-14}" width="24" height="28" fill="#9467bd"/><rect x="{cx+2}" y="{cy-14}" width="24" height="28" fill="#9467bd"/>',
        "ONE":   f'<circle cx="{cx}" cy="{cy}" r="8" fill="#8c564b"/>',
        "ALL":   f'<rect x="{cx-24}" y="{cy-24}" width="48" height="48" fill="#e377c2"/>',
        "NOT":   f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="#7f7f7f" stroke-width="3"/><line x1="{cx-16}" y1="{cy+16}" x2="{cx+16}" y2="{cy-16}" stroke="#7f7f7f" stroke-width="3"/>',
        "IF":    f'<polygon points="{cx},{cy-24} {cx+24},{cy} {cx},{cy+24} {cx-24},{cy}" fill="none" stroke="#bcbd22" stroke-width="3"/>',
        "DO":    f'<circle cx="{cx}" cy="{cy}" r="18" fill="#17becf"/>',
        "HAPPEN":f'<path d="M{cx-25},{cy} Q{cx-13},{cy-20} {cx},{cy} T{cx+25},{cy}" fill="none" stroke="#ff7f0e" stroke-width="3"/>',
        "KNOW":  f'<ellipse cx="{cx}" cy="{cy}" rx="28" ry="15" fill="none" stroke="#1f77b4" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="7" fill="#1f77b4"/>',
        "SEE":   f'<polygon points="{cx},{cy-24} {cx+24},{cy+16} {cx-24},{cy+16}" fill="none" stroke="#2ca02c" stroke-width="3"/><circle cx="{cx}" cy="{cy+3}" r="7" fill="#2ca02c"/>',
        "BIG":   f'<circle cx="{cx}" cy="{cy}" r="30" fill="#d62728"/>',
        "LIVE":  f'<path d="M{cx},{cy-20} C{cx+34},{cy-13} {cx+34},{cy+13} {cx},{cy+20}" fill="none" stroke="#2ca02c" stroke-width="3"/>',
        "DIE":   f'<path d="M{cx},{cy-20} C{cx+34},{cy-13} {cx+34},{cy+13} {cx},{cy+20} L{cx+5},{cy+22}" fill="none" stroke="#7f7f7f" stroke-width="3"/>',
        "MOVE":  f'<path d="M{cx-25},{cy} Q{cx},{cy-25} {cx+25},{cy}" fill="none" stroke="#17becf" stroke-width="4" marker-end="url(#a)"/>',
        "THINK": f'<circle cx="{cx-14}" cy="{cy}" r="10" fill="none" stroke="#9467bd" stroke-width="3"/><circle cx="{cx+14}" cy="{cy}" r="10" fill="none" stroke="#9467bd" stroke-width="3"/><line x1="{cx-4}" y1="{cy}" x2="{cx+4}" y2="{cy}" stroke="#9467bd" stroke-width="3"/>',
        "SAY":   f'<rect x="{cx-24}" y="{cy-16}" width="48" height="26" fill="none" stroke="#ff7f0e" stroke-width="3"/><polygon points="{cx-7},{cy+10} {cx},{cy+22} {cx+7},{cy+10}" fill="#ff7f0e"/>',
        "TRUE":  f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="#1f77b4" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#1f77b4" stroke-width="3"/>',
        "GOOD":  f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#2ca02c" stroke-width="3"/><line x1="{cx-10}" y1="{cy}" x2="{cx+10}" y2="{cy}" stroke="#2ca02c" stroke-width="3"/><line x1="{cx}" y1="{cy-10}" x2="{cx}" y2="{cy+10}" stroke="#2ca02c" stroke-width="3"/>',
    }
    return table[pid]

def main(dst):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0,10 3,0 6" fill="context-stroke"/></marker></defs>',
        '<rect width="100%" height="100%" fill="#fafafa"/>',
        f'<text x="{W//2}" y="28" font-family="monospace" font-size="16" text-anchor="middle" fill="#222">ALPHA-20 GLYPH ATLAS - 20 primitives, layers L0-L4</text>',
    ]
    for i, p in enumerate(LEX["primitives"]):
        col, row = i % COLS, i // COLS
        cx, cy = col * CELL + CELL // 2, row * CELL + CELL // 2 + 40
        parts.append(f'<rect x="{col*CELL}" y="{row*CELL+40}" width="{CELL}" height="{CELL}" fill="none" stroke="#ddd"/>')
        parts.append(glyph(p["id"], cx, cy))
        parts.append(f'<text x="{cx}" y="{cy+CELL//2-14}" font-family="monospace" font-size="11" text-anchor="middle" fill="#222">{p["id"]}</text>')
        parts.append(f'<text x="{cx}" y="{cy+CELL//2-2}" font-family="monospace" font-size="9" text-anchor="middle" fill="#888">{p["layer"]}</text>')
    parts.append("</svg>")
    Path(dst).write_text("\n".join(parts))
    print("wrote " + dst + " (" + str(len(parts)) + " elements)")

if __name__ == "__main__":
    main(sys.argv[1])
