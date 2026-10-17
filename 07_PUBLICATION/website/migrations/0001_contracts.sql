CREATE TABLE IF NOT EXISTS contracts (
  id TEXT PRIMARY KEY,
  proposer TEXT NOT NULL,
  expression TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  signature TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  verified_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_contracts_proposer ON contracts(proposer);
