import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import pagefind from '@itsmatteomanf/astro-pagefind';

export default defineConfig({
  site: 'https://alpha0az1omega.com',
  integrations: [react(), pagefind()],
});
