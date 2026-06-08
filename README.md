# README

This is the repo for the OBIS website, https://obis.org/.  It is based on [Jekyll](https://github.com/jekyll/jekyll).

## Reporting Issues and Suggesting Improvements

If you find a bug or have a suggestion, you can submit an issue using the [Issues tab](https://github.com/iobis/obis-website/issues) at the top of this page.

1. Click **New issue**.
2. Give your issue a short, descriptive title.
3. In the description, include as much detail as possible — what you expected to happen, what actually happened, and steps to reproduce the problem.
4. Click **Submit new issue**.

You'll need a free GitHub account to submit an issue. If you don't have one, you can create one at https://github.com/signup.

---

## Development & Deployment

This repository has two deployment targets:

- **`dev` branch** → https://dev.obis.org (staging)
- **`main` branch** → https://obis.org (production)

- PRs are required to merge into master — no one can push directly without a review
- Only @pieterprovoost can force push — everyone else is blocked from overriding history

### Dev Workflow

1. Create a feature branch from `dev` and make your changes.
2. Open a pull request into `dev`. Once merged, the site will automatically deploy to https://dev.obis.org — you can monitor progress under the [Actions tab](https://github.com/iobis/obis-website/actions) (`Deploy to server (DEV)`).
3. Review your changes on the dev site.
4. When ready for production, open a pull request from `dev` into `master`. Once merged, the production site will update automatically (`Deploy to server (PROD)`).

### Add a page

Most content on this site lives in one of two places:

- **Collection pages** — add a new Markdown file to the relevant `_collection` folder (see [Collections](#collections) below). `_posts` and `_usecases` use the filename format `YYYY-MM-DD-your-title.md`. All other collections use plain descriptive slugs (e.g. `obis_export.md`). Refer to an existing file in the same collection for the expected format.
- **Standalone pages** — add a Markdown file to the appropriate top-level folder (e.g. `data/`, `about/`, `whatwedo/`) or to the root of the repo.

All pages should include a YAML front matter block at the top. Refer to an existing page in the same folder for the expected fields.

### Collections

Jekyll collections group related content so it can be iterated over and rendered with shared layouts and templates.  This website currently has the following collections:

- **`_posts`** — news and blog posts (built-in Jekyll collection)
- **`_usecases`** — scientific use cases featuring OBIS data
- **`_partnerships`** — institutional partnerships
- **`_data_products`** — data products derived from OBIS
- **`_sources`** — external data sources integrated with OBIS
