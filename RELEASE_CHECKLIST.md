# ALPHA_ARCHIVE_000 - Release Checklist

Before pressing "Publish" on any platform, ensure the following:

- [ ] `verify_all.sh` returns no warnings.
- [ ] `npm run build` succeeds in `07_PUBLICATION/website/`.
- [ ] The GitHub `repo_content` is updated with the latest files from Phases 1-16.
- [ ] The public GPG key is available at `alpha0az1omega.com/alpha0az1omega_pubkey.asc`.

## Cloudflare Deployment (Dynamic Modules)

- [ ] Create D1 Database: `npx wrangler d1 create alpha20-contracts`
- [ ] Update `database_id` in `wrangler.jsonc`
- [ ] Create KV Namespace: `npx wrangler kv namespace create OTS_CACHE`
- [ ] Update `id` in `wrangler.jsonc`
- [ ] Apply Migration: `npx wrangler d1 execute alpha20-contracts --file=migrations/0001_contracts.sql`
- [ ] Push code to GitHub.
- [ ] Connect GitHub to Cloudflare Pages (Root: `07_PUBLICATION/website`, Build: `npm run build`, Output: `dist`).
- [ ] Change GoDaddy nameservers to Cloudflare.

## Publishing

1. Publish RO-Crate ZIP to Zenodo.
2. Publish NFT to OpenSea.
3. Post on social media.
