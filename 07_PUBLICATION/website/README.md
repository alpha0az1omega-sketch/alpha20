# Alpha-20 Website (Cloudflare Pages)

This directory contains the Astro website and Cloudflare Pages Functions.

## Cloudflare Setup

Before deploying, you must create the D1 database and KV namespace.

### 1. Create D1 Database
Run the following command in your terminal (requires Wrangler CLI):
    npx wrangler d1 create alpha20-contracts

Copy the `database_id` returned and paste it into `wrangler.jsonc` under `d1_databases`.

### 2. Create KV Namespace
Run:
    npx wrangler kv namespace create OTS_CACHE

Copy the `id` returned and paste it into `wrangler.jsonc` under `kv_namespaces`.

### 3. Apply Database Migrations
Run:
    npx wrangler d1 execute alpha20-contracts --file=migrations/0001_contracts.sql

### 4. Deploy
Connect your GitHub repository to Cloudflare Pages.
- Framework preset: Astro
- Build command: npm run build
- Build output directory: dist
