#!/usr/bin/env python3
"""Generate a cryptographic commitment for identity proof."""
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "07_PUBLICATION" / "identity_vault.txt"
OUT = ROOT / "07_PUBLICATION" / "identity_commitment.txt"

def main():
    if not VAULT.exists():
        print(f"Create {VAULT} with your real identity first.")
        return
    
    content = VAULT.read_bytes()
    h = hashlib.sha256(content).hexdigest()
    
    OUT.write_text(
        "ALPHA-20 IDENTITY COMMITMENT\n"
        f"SHA-256: {h}\n"
        "This hash proves the existence of the identity_vault.txt file without revealing its contents.\n"
    )
    print(f"Commitment written to {OUT}. Hash: {h}")

if __name__ == "__main__":
    main()
