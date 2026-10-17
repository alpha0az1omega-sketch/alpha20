#!/usr/bin/env python3
"""Agentic SVG builder for ALPHA_ARCHIVE_000 - Phase 6 (Audio).
Adds Web Audio API synthesis to the interactive SVG.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXICON = json.loads((ROOT / "01_SPECIFICATION" / "primitive_lexicon.json").read_text())
PRIMS = LEXICON["primitives"]

CELL = 140
COLS, ROWS = 4, 5
ATLAS_W, ATLAS_H = COLS * CELL, ROWS * CELL + 40

GLYPH_TABLE = {
    "EXIST": '<circle cx="{cx}" cy="{cy}" r="20" fill="#1f77b4"/>',
    "CAUSE": '<line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="#d62728" stroke-width="4" marker-end="url(#arrow)"/>',
    "PART":  '<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="#2ca02c" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="10" fill="#2ca02c"/>',
    "SAME":  '<rect x="{rx1}" y="{ry}" width="24" height="28" fill="#9467bd"/><rect x="{rx2}" y="{ry}" width="24" height="28" fill="#9467bd"/>',
    "ONE":   '<circle cx="{cx}" cy="{cy}" r="8" fill="#8c564b"/>',
    "ALL":   '<rect x="{rx1}" y="{ry}" width="48" height="48" fill="#e377c2"/>',
    "NOT":   '<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="#7f7f7f" stroke-width="3"/><line x1="{x1}" y1="{y2}" x2="{x2}" y2="{y1}" stroke="#7f7f7f" stroke-width="3"/>',
    "IF":    '<polygon points="{cx},{y1} {x2},{cy} {cx},{y2} {x1},{cy}" fill="none" stroke="#bcbd22" stroke-width="3"/>',
    "DO":    '<circle cx="{cx}" cy="{cy}" r="18" fill="#17becf"/>',
    "HAPPEN":'<path d="M{x1},{cy} Q{cx},{y1} {cx},{cy} T{x2},{cy}" fill="none" stroke="#ff7f0e" stroke-width="3"/>',
    "KNOW":  '<ellipse cx="{cx}" cy="{cy}" rx="28" ry="15" fill="none" stroke="#1f77b4" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="7" fill="#1f77b4"/>',
    "SEE":   '<polygon points="{cx},{y1} {x2},{y2} {x1},{y2}" fill="none" stroke="#2ca02c" stroke-width="3"/><circle cx="{cx}" cy="{cy3}" r="7" fill="#2ca02c"/>',
    "BIG":   '<circle cx="{cx}" cy="{cy}" r="30" fill="#d62728"/>',
    "LIVE":  '<path d="M{cx},{y1} C{x2},{cy1} {x2},{cy2} {cx},{y2}" fill="none" stroke="#2ca02c" stroke-width="3"/>',
    "DIE":   '<path d="M{cx},{y1} C{x2},{cy1} {x2},{cy2} {cx},{y2} L{cx5},{y2b}" fill="none" stroke="#7f7f7f" stroke-width="3"/>',
    "MOVE":  '<path d="M{x1},{cy} Q{cx},{y1} {x2},{cy}" fill="none" stroke="#17becf" stroke-width="4" marker-end="url(#arrow)"/>',
    "THINK": '<circle cx="{cx1}" cy="{cy}" r="10" fill="none" stroke="#9467bd" stroke-width="3"/><circle cx="{cx2}" cy="{cy}" r="10" fill="none" stroke="#9467bd" stroke-width="3"/><line x1="{x3}" y1="{cy}" x2="{x4}" y2="{cy}" stroke="#9467bd" stroke-width="3"/>',
    "SAY":   '<rect x="{rx1}" y="{ry}" width="48" height="26" fill="none" stroke="#ff7f0e" stroke-width="3"/><polygon points="{px1},{py1} {cx},{py2} {px2},{py1}" fill="#ff7f0e"/>',
    "TRUE":  '<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="#1f77b4" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#1f77b4" stroke-width="3"/>',
    "GOOD":  '<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#2ca02c" stroke-width="3"/><line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="#2ca02c" stroke-width="3"/><line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2}" stroke="#2ca02c" stroke-width="3"/>',
}

def render_glyph(pid, cx, cy):
    t = GLYPH_TABLE[pid]
    return t.format(
        cx=cx, cy=cy, x1=cx-25, x2=cx+25, y1=cy-24, y2=cy+24,
        rx1=cx-26, rx2=cx+2, ry=cy-14, cx1=cx-14, cx2=cx+14,
        x3=cx-4, x4=cx+4, cy1=cy-13, cy2=cy+13, cy3=cy+3,
        cx5=cx+5, y2b=cy+22, px1=cx-7, px2=cx+7, py1=cy+10, py2=cy+22,
    )

def build_atlas_layer():
    parts = [
        f'<g id="atlas" aria-label="ALPHA-20 glyph atlas">',
        f'<text x="{ATLAS_W//2}" y="28" font-family="monospace" font-size="16" text-anchor="middle" fill="#222">ALPHA-20 GLYPH ATLAS - 20 primitives</text>',
    ]
    for i, p in enumerate(PRIMS):
        col, row = i % COLS, i // COLS
        cx, cy = col * CELL + CELL // 2, row * CELL + CELL // 2 + 40
        parts.append(f'<rect x="{col*CELL}" y="{row*CELL+40}" width="{CELL}" height="{CELL}" fill="none" stroke="#ddd"/>')
        parts.append(render_glyph(p["id"], cx, cy))
        parts.append(f'<text x="{cx}" y="{cy+CELL//2-14}" font-family="monospace" font-size="11" text-anchor="middle" fill="#222">{p["id"]}</text>')
        parts.append(f'<text x="{cx}" y="{cy+CELL//2-2}" font-family="monospace" font-size="9" text-anchor="middle" fill="#888">{p["layer"]}</text>')
    parts.append("</g>")
    return "\n".join(parts)

def build_state_layer():
    # Injecting the full sonification lexicon into the state for the audio engine
    initial = {
        "version": "0.2.0",
        "sealed": False,
        "last_hash": None,
        "history": [],
        "lexicon": {p["id"]: p["sonification"] for p in PRIMS},
    }
    return f'<metadata id="alpha-state">{json.dumps(initial, ensure_ascii=False)}</metadata>'

def build_js():
    return r"""
(function () {
  "use strict";
  var SVG_NS = "http://www.w3.org/2000/svg";
  var stateEl = document.getElementById("alpha-state");
  var logEl = document.getElementById("log");
  var dynEl = document.getElementById("dynamic-layer");
  var inputEl = document.getElementById("expr");
  var outEl = document.getElementById("result");
  var audioCtx = null;

  function getState() { return JSON.parse(stateEl.textContent); }
  function setState(s) { stateEl.textContent = JSON.stringify(s); }

  function log(msg) {
    var t = document.createElementNS(SVG_NS, "tspan");
    t.setAttribute("x", "20"); t.setAttribute("dy", "1.2em"); t.textContent = msg;
    logEl.appendChild(t);
    if (logEl.childNodes.length > 5) { logEl.removeChild(logEl.firstChild); }
  }

  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') { audioCtx.resume(); }
  }

  // --- Alpha-20 tokenizer / parser ---
  function tokenize(src) {
    var re = /\s*(\d+\.\d+|\d+|[A-Za-z_][A-Za-z0-9_]*|"[^"]*"|[(),])/g;
    var toks = [], m;
    while ((m = re.exec(src)) !== null) { toks.push(m[1]); }
    return toks;
  }
  function parse(toks) {
    var i = 0;
    function peek() { return toks[i]; }
    function eat(v) { if (toks[i] !== v) throw new Error("expected " + v); i++; }
    function expr() {
      if (peek() === "IF") { eat("IF"); var c = expr(); eat("THEN"); var t = expr(); var e = null; if (peek() === "ELSE") { eat("ELSE"); e = expr(); } return {op:"IF", c:c, t:t, e:e}; }
      if (peek() === "NOT") { eat("NOT"); return {op:"NOT", v:expr()}; }
      var left = atom();
      while (peek() === "AND" || peek() === "OR") { var op = toks[i++]; var right = atom(); left = {op:op, l:left, r:right}; }
      return left;
    }
    function atom() {
      var t = peek();
      if (/^\d/.test(t)) { i++; return {op:"NUM", v:parseFloat(t)}; }
      if (t === "(") { eat("("); var e = expr(); eat(")"); return e; }
      if (/^[A-Za-z_]/.test(t)) {
        var name = toks[i++];
        if (peek() === "(") { eat("("); var args = []; if (peek() !== ")") { args.push(expr()); while (peek() === ",") { eat(","); args.push(expr()); } } eat(")"); return {op:"CALL", name:name, args:args}; }
        return {op:"ID", name:name};
      }
      throw new Error("unexpected " + t);
    }
    var ast = expr();
    return ast;
  }

  function evalNode(n) {
    if (n.op === "NUM") return n.v;
    if (n.op === "ID") return n.name;
    if (n.op === "AND") return evalNode(n.l) && evalNode(n.r);
    if (n.op === "OR") return evalNode(n.l) || evalNode(n.r);
    if (n.op === "NOT") return !evalNode(n.v);
    if (n.op === "IF") return evalNode(n.c) ? evalNode(n.t) : (n.e ? evalNode(n.e) : null);
    if (n.op === "CALL") {
      var a = n.args.map(evalNode);
      if (n.name === "SAME") return a[0] === a[1];
      if (n.name === "BIG") return a[0] > a[1];
      if (n.name === "MOVE") return (a[2] - a[1]) > 0;
      return true; // default true for visual primitives
    }
    return null;
  }

  function collectPrims(n, acc) {
    acc = acc || [];
    if (!n) return acc;
    if (n.op === "CALL") { acc.push(n.name); n.args.forEach(function (a) { collectPrims(a, acc); }); }
    if (n.op === "AND" || n.op === "OR") { collectPrims(n.l, acc); collectPrims(n.r, acc); }
    if (n.op === "NOT") { collectPrims(n.v, acc); }
    if (n.op === "IF") { collectPrims(n.c, acc); collectPrims(n.t, acc); if (n.e) { collectPrims(n.e, acc); } }
    return acc;
  }

  // --- Audio Synthesis Engine ---
  function playSonification(prims) {
    initAudio();
    var lex = getState().lexicon;
    var startTime = audioCtx.currentTime + 0.1;

    prims.forEach(function(pid, index) {
      var son = lex[pid];
      if (!son) return;
      
      var dur = (son.duration_ms || 200) / 1000;
      var freq = son.freq_hz || son.freq_start || 440;
      var freqEnd = son.freq_end || freq;

      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, startTime);
      if (freqEnd !== freq) {
        osc.frequency.exponentialRampToValueAtTime(freqEnd, startTime + dur);
      }

      // ADSR mapping
      var adsr = son.adsr || [0.01, 0.05, 0.7, 0.24];
      var attack = dur * adsr[0];
      var decay = dur * adsr[1];
      var sustain = adsr[2];
      var release = dur * adsr[3];

      gain.gain.setValueAtTime(0, startTime);
      gain.gain.linearRampToValueAtTime(1, startTime + attack);
      gain.gain.linearRampToValueAtTime(sustain, startTime + attack + decay);
      gain.gain.setValueAtTime(sustain, startTime + dur - release);
      gain.gain.linearRampToValueAtTime(0, startTime + dur);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start(startTime);
      osc.stop(startTime + dur);

      startTime += dur + 0.05; // 50ms gap
    });
  }

  // --- Cryptography ---
  function sha256Fallback(ascii) {
    // Same as Phase 5
    function rightRotate(v, a) { return (v >>> a) | (v << (32 - a)); }
    var mathPow = Math.pow, maxWord = mathPow(2, 32), result = "", words = [], asciiBitLength = ascii.length * 8;
    var hash = sha256Fallback.h = sha256Fallback.h || [];
    var k = sha256Fallback.k = sha256Fallback.k || [];
    var primeCounter = k.length;
    var isComposite = {};
    for (var candidate = 2; primeCounter < 64; candidate++) {
      if (!isComposite[candidate]) {
        for (var i = 0; i < 313; i += candidate) { isComposite[i] = candidate; }
        hash[primeCounter] = (mathPow(candidate, .5) * maxWord) | 0;
        k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
      }
    }
    ascii += "\x80";
    while (ascii.length % 64 - 56) ascii += "\x00";
    for (i = 0; i < ascii.length; i++) { var j = ascii.charCodeAt(i); if (j >> 8) return; words[i >> 2] |= j << ((3 - i) % 4) * 8; }
    words[words.length] = ((asciiBitLength / maxWord) | 0); words[words.length] = asciiBitLength;
    for (j = 0; j < words.length;) {
      var w = words.slice(j, j += 16);
      var oldHash = hash.slice(0, 8);
      for (i = 0; i < 64; i++) {
        var w15 = w[i - 15], w2 = w[i - 2];
        var a = hash[0], e = hash[4];
        var temp1 = hash[7] + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) + ((e & hash[5]) ^ ((~e) & hash[6])) + k[i] + (w[i] = (i < 16) ? w[i] : (w[i - 16] + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) + w[i - 7] + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))) | 0);
        var temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
        hash = [(temp1 + temp2) | 0].concat(hash); hash[4] = (hash[4] + temp1) | 0;
      }
      for (i = 0; i < 8; i++) hash[i] = (hash[i] + oldHash[i]) | 0;
    }
    for (i = 0; i < 8; i++) { for (j = 3; j + 1; j--) { var b = (hash[i] >> (j * 8)) & 255; result += ((b < 16) ? 0 : "") + b.toString(16); } }
    return result;
  }

  function sha256(text) {
    if (window.crypto && window.crypto.subtle) {
      var buf = new TextEncoder().encode(text);
      return window.crypto.subtle.digest("SHA-256", buf).then(function (h) {
        return Array.from(new Uint8Array(h)).map(function (b) { return b.toString(16).padStart(2, "0"); }).join("");
      });
    }
    return Promise.resolve(sha256Fallback(text));
  }

  // --- Actions ---
  function renderGlyphs(prims) {
    while (dynEl.firstChild) dynEl.removeChild(dynEl.firstChild);
    prims.forEach(function (p, idx) {
      var g = document.createElementNS(SVG_NS, "g");
      g.setAttribute("transform", "translate(" + (560 + (idx % 2) * 80) + "," + (40 + Math.floor(idx / 2) * 80) + ")");
      var c = document.createElementNS(SVG_NS, "circle");
      c.setAttribute("cx", "30"); c.setAttribute("cy", "30"); c.setAttribute("r", "20"); c.setAttribute("fill", "#1f77b4"); c.setAttribute("opacity", "0.85");
      var t = document.createElementNS(SVG_NS, "text");
      t.setAttribute("x", "30"); t.setAttribute("y", "70"); t.setAttribute("font-family", "monospace"); t.setAttribute("font-size", "10"); t.setAttribute("text-anchor", "middle"); t.setAttribute("fill", "#222");
      t.textContent = p;
      g.appendChild(c); g.appendChild(t); dynEl.appendChild(g);
    });
  }

  function onEvaluate() {
    try {
      var src = (inputEl.value || "MOVE(particle, 0, 10) AND SAME(10, 10) AND BIG(10, 0)").trim();
      var ast = parse(tokenize(src));
      var val = evalNode(ast);
      var prims = collectPrims(ast);
      
      renderGlyphs(prims);
      playSonification(prims); // TRIGGER AUDIO
      
      var s = getState();
      s.history.push({ expr: src, value: val, prims: prims, at: new Date().toISOString() });
      s.sealed = false; s.last_hash = null;
      setState(s);
      
      outEl.textContent = "RESULT: " + String(val);
      log("evaluated & played: " + src);
    } catch (e) {
      outEl.textContent = "ERROR: " + e.message;
      log("error: " + e.message);
    }
  }

  function onSeal() {
    var s = getState(); var canon = JSON.stringify(s);
    sha256(canon).then(function (h) {
      s.sealed = true; s.last_hash = h; setState(s);
      outEl.textContent = "SEALED: " + h.slice(0, 16) + "...";
      log("sealed: " + h.slice(0, 16) + "...");
    });
  }

  function onReset() {
    setState({ version: "0.2.0", sealed: false, last_hash: null, history: [], lexicon: getState().lexicon });
    renderGlyphs([]);
    outEl.textContent = "RESET"; log("state reset");
  }

  document.getElementById("btn-eval").addEventListener("click", onEvaluate);
  document.getElementById("btn-seal").addEventListener("click", onSeal);
  document.getElementById("btn-reset").addEventListener("click", onReset);
})();
"""

def build_interaction_layer():
    y0 = ATLAS_H + 40
    return f'''
<g id="interaction" transform="translate(0,{y0})" aria-label="Agentic controls">
  <rect x="20" y="0" width="760" height="180" rx="8" fill="#fff" stroke="#ccc"/>
  <text x="40" y="28" font-family="monospace" font-size="14" fill="#222">ALPHA-20 AGENTIC GLYPH - stateful, sonorous, self-sealing</text>
  <foreignObject x="40" y="44" width="720" height="40">
    <input xmlns="http://www.w3.org/1999/xhtml" id="expr" type="text" value="MOVE(particle, 0, 10) AND SAME(10, 10) AND BIG(10, 0)" style="width:700px;font-family:monospace;font-size:13px;padding:6px;border:1px solid #aaa;border-radius:4px"/>
  </foreignObject>
  <g id="btn-eval" role="button" tabindex="0" transform="translate(40,100)">
    <rect width="140" height="40" rx="6" fill="#1f77b4"/><text x="70" y="25" text-anchor="middle" fill="#fff" font-family="monospace" font-size="13">EVALUATE + PLAY</text>
  </g>
  <g id="btn-seal" role="button" tabindex="0" transform="translate(200,100)">
    <rect width="140" height="40" rx="6" fill="#2ca02c"/><text x="70" y="25" text-anchor="middle" fill="#fff" font-family="monospace" font-size="13">SEAL</text>
  </g>
  <g id="btn-reset" role="button" tabindex="0" transform="translate(360,100)">
    <rect width="140" height="40" rx="6" fill="#7f7f7f"/><text x="70" y="25" text-anchor="middle" fill="#fff" font-family="monospace" font-size="13">RESET</text>
  </g>
  <text id="result" x="540" y="126" font-family="monospace" font-size="12" fill="#222">RESULT: -</text>
  <text id="log" x="20" y="160" font-family="monospace" font-size="10" fill="#666"></text>
</g>
<g id="dynamic-layer" transform="translate(0,0)"></g>
'''

def main():
    W, H = 800, ATLAS_H + 40 + 180 + 20
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
        '<title>ALPHA-20 Agentic Glyph - phase 6 audio</title>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0,10 3,0 6" fill="context-stroke"/></marker></defs>',
        '<rect width="100%" height="100%" fill="#fafafa"/>',
        build_state_layer(), build_atlas_layer(), build_interaction_layer(),
        '<script type="application/ecmascript"><![CDATA[', build_js(), ']]></script>', '</svg>'
    ]
    out = ROOT / "04_ARTIFACTS" / "svg" / "glyph_agentic_v2.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(svg))
    print(f"wrote {out} ({out.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
