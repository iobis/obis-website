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
- **`master` branch** → https://obis.org (production)

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

All pages should include a YAML front matter block at the top. The available fields are:

```
layout: # Should alwasy be 'post'
title: # An excellent title, in quotes.
subtitle: # An excellent subtitle, in quotes.
lang: en # Usually 'en' for English, but could be other value.
author: # Should alwasy be 'OBIS'
tags: #consult Laurent
purpose: # Should alwasy be 'news'
feed: # Should alwasy be 'true'
image: # link to image on internet or to image in `assets/images`
imageCaption: # a description of the image. Include link to WoRMS record if you reference a taxon.
imageAlt: # Text in quotes. Should clearly describe the image and might need more detail than the caption.
imageLicense: # a description of the license under which the image is being used. Use links to give credit and make it easy for users to find the license.

#### Example frontmatter block

```
---
layout: post
title: "The new OBIS website is live!"
subtitle: "Please be our cleaner shrimp."
lang: en
author: OBIS
tags:
purpose: news
feed: true
image: https://inaturalist-open-data.s3.amazonaws.com/photos/398634387/large.jpg
imageCaption: "A [Pacific cleaner shrimp (_Lysmata amboinensis_)](https://marinespecies.org/aphia.php?p=taxdetails&id=241289) cleans the mouth of a fish on the coast of Umkhanyakude, South Africa"
imageAlt: "A Pacific cleaner shrimp (Lysmata amboinensis) cleans the mouth of a fish on the coast of Umkhanyakude, South Africa"
imageLicense: "Ambon Cleaner Shrimp (_Lysmata amboinensis_) Umkhanyakude, ZA-NL, ZA. by aspearton via [inaturalist.org](https://www.inaturalist.org/photos/398634387), licensed under [CC-BY-NC](https://creativecommons.org/licenses/by-nc/4.0/)"

---

Your post text starts here. You can use any valid Markdown to style it...

```

### Collections

Jekyll collections group related content so it can be iterated over and rendered with shared layouts and templates.  This website currently has the following collections:

- **`_posts`** — news and blog posts (built-in Jekyll collection)
- **`_usecases`** — scientific use cases featuring OBIS data
- **`_partnerships`** — institutional partnerships
- **`_data_products`** — data products derived from OBIS
- **`_sources`** — external data sources integrated with OBIS