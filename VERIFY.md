# Verification Guide for ALPHA_ARCHIVE_000

This document explains how to cryptographically verify the integrity of this archive.

## 1. Verify SHA-256 Hashes

Ensure the files have not been modified since the manifest was created.

    shasum -a 256 -c 00_MANIFEST/manifest_phase10_sha256.txt

## 2. Verify GPG Signatures

Ensure the manifests were signed by Alpha0az1omega.

    gpg --import 09_PUBLIC_KEYS/alpha0az1omega_pubkey.asc
    gpg --verify 00_MANIFEST/manifest_phase10_sha256.txt.asc 00_MANIFEST/manifest_phase10_sha256.txt

## 3. Verify OpenTimestamps Proofs

Ensure the archive existed at a specific point in time (anchored in the Bitcoin blockchain).

    ots verify 00_MANIFEST/manifest_phase10_sha256.txt.ots

Note: If the proof is "Pending", Bitcoin has not yet confirmed the block. Retry later.

## 4. Verify the Agentic Glyph

Open `04_ARTIFACTS/svg/glyph_agentic_v2.svg` in a browser via a local server:

    python3 -m http.server 8765

Go to http://127.0.0.1:8765/04_ARTIFACTS/svg/glyph_agentic_v2.svg, click EVALUATE + PLAY, and then SEAL. The generated hash should match the internal state.
