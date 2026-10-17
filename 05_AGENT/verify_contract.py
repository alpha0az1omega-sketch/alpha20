#!/usr/bin/env python3
"""Create and verify Alpha-20 agent contracts."""
import hashlib, json, subprocess, sys
from pathlib import Path

def sha256_file(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()

def create_contract(expr_file, out_json):
    expr = Path(expr_file).read_text().strip()
    h = hashlib.sha256(expr.encode()).hexdigest()
    contract = {
        "contract_id": "generated-" + h[:8],
        "proposer": "alpha0az1omega",
        "expression": expr,
        "sha256": h,
        "timestamp": "2026-10-17T14:30:00Z"
    }
    Path(out_json).write_text(json.dumps(contract, indent=2))
    print(f"Contract created: {out_json}, sha256={h}")

def verify_contract(json_file):
    c = json.loads(Path(json_file).read_text())
    recomputed = hashlib.sha256(c["expression"].encode()).hexdigest()
    assert recomputed == c["sha256"], "Hash mismatch"
    print(f"Contract {c['contract_id']} verified. Hash matches.")

if __name__ == "__main__":
    if sys.argv[1] == "create":
        create_contract(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "verify":
        verify_contract(sys.argv[2])
