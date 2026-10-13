// @ts-check
import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';

const base = '/derham';
export default defineConfig({
  site: 'https://max-models.github.io',
  base,
  markdown: { processor: unified({ remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex] }) },
  integrations: [starlight({
    title: 'derham',
    description: 'De Rham complexes and FEEC diagrams in LaTeX.',
    customCss: ['katex/dist/katex.min.css', './src/styles/custom.css'],
    components: { Header: './src/components/Header.astro' },
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/max-models/derham' }],
    editLink: { baseUrl: 'https://github.com/max-models/derham/edit/main/docs/' },
    lastUpdated: true,
    plugins: process.env.DOCS_VALIDATE_LINKS === 'false' ? [] : [starlightLinksValidator({ errorOnLocalLinks: false })],
    sidebar: [
      { label: 'Getting started', items: [
        { label: 'Installation', slug: 'getting-started/installation' },
        { label: 'Quickstart', slug: 'getting-started/quickstart' },
      ] },
      { label: 'Guides', items: [{ autogenerate: { directory: 'guides' } }] },
      { label: 'Reference', items: [
        { label: 'Commands and options', slug: 'reference/options' },
        { label: 'Mathematical conventions', slug: 'reference/conventions' },
      ] },
      { label: 'Development', items: [
        { label: 'Building the docs', slug: 'development/docs' },
        { label: 'Publishing', slug: 'development/publishing' },
      ] },
    ],
  })],
});
