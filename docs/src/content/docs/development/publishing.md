---
title: Publishing
description: How the web documentation is built and deployed.
---

The [Docs workflow](https://github.com/max-models/derham/blob/main/.github/workflows/docs.yml) builds the site on pushes and pull requests to `main`. It installs TeX Live and the notebook dependencies, executes the guide, compiles the Starlight site, checks its pages and base paths, and uploads the static files as a Pages artifact.

A successful push to `main` deploys that artifact to GitHub Pages at [max-models.github.io/derham](https://max-models.github.io/derham/). In the repository's **Settings → Pages**, set the build source to **GitHub Actions**. The deploy job uses the `github-pages` environment.

The site lives under the `/derham` base path. Keep links to internal pages base-aware and check the built output before publishing:

```bash
make docs-build
```

Notebook-generated MDX, images, and the build directory are ignored by Git; CI recreates them from the source notebooks. The printable PDF manual is built separately from `derham.tex`.
