#!/bin/bash
# ALPHA_ARCHIVE_000 MASTER VERIFICATION (Universal v3)
set -uo pipefail
cd "$(dirname "$0")"

echo "=== ALPHA_ARCHIVE_000 MASTER VERIFICATION ==="
echo "Checking integrity of cryptographic proofs..."

echo "[1/3] Checking SHA-256 hashes (latest manifests)..."
shasum -a 256 -c 00_MANIFEST/manifest_phase6_sha256.txt 2>/dev/null | grep -v "OK" || true
shasum -a 256 -c 00_MANIFEST/manifest_phase13_sha256.txt 2>/dev/null | grep -v "OK" || true
echo "  -> Hash checks complete (silent = all OK)."

echo "[2/3] Checking GPG signatures..."
gpg --import 09_PUBLIC_KEYS/alpha0az1omega_pubkey.asc 2>/dev/null || true
for asc in 00_MANIFEST/manifest_*.asc; do
  base="${asc%.asc}"
  if ! gpg --verify "$asc" "$base" >/dev/null 2>&1; then
    echo "  -> FAILED: Signature invalid in $asc"
  fi
done
echo "  -> Signature checks complete (silent = all OK)."

echo "[3/3] Checking OpenTimestamps proofs..."
for ots in 00_MANIFEST/manifest_*.ots; do
  # On capture la sortie standard et d'erreur
  OUT=$(ots verify "$ots" 2>&1)
  # Si la sortie ne contient ni "Success", ni "Pending", ni "Bitcoin block", c'est une erreur
  if [[ "$OUT" != *"Success"* ]] && [[ "$OUT" != *"Pending"* ]] && [[ "$OUT" != *"Bitcoin block"* ]]; then
     echo "  -> WARNING: Invalid OTS for $ots"
  fi
done
echo "  -> OTS checks complete (Pending is normal for recent proofs)."

echo "=== VERIFICATION COMPLETE ==="
