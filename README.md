# Elastic Docs Content

![GitHub deployments](https://img.shields.io/github/deployments/elastic/docs-content/docs-preview?logo=elastic&label=docs-preview&link=https%3A%2F%2Fdocs-v3-preview.elastic.dev%2Felastic%2Fdocs-content%2Ftree%2Fmain)

This repo is the source for the narrative user documentation published at <https://www.elastic.co/docs/>: concepts, guides, and troubleshooting for Elastic products. It covers current versions and deployments: Elastic Stack v9 and Serverless, Elastic Cloud Enterprise v4, Elastic Cloud on Kubernetes v3 and later, Elastic Cloud Hosted, and a range of Elastic tools.

Pages are MyST Markdown with Elastic extensions, built by [docs-builder](https://elastic.github.io/docs-builder/). After a merge to `main`, the published site refreshes within minutes.

## What belongs here, and what doesn't

This repo hosts the cross-product, narrative user documentation for the products and versions above. Some content lives elsewhere:

- **Reference docs that sit next to the code they describe.** Reference content generated from or maintained alongside a codebase stays in that code repo. API references are the clearest case: they're generated from OpenAPI specs, most often in `elastic/kibana` or `elastic/elasticsearch-specification`, not authored as Markdown here. The same holds for other in-repo reference material that ships with the product.
- **Legacy-version content.** Documentation for versions earlier than the ones this repo covers, essentially Elastic v8 and before, lives in the respective code repositories, on older branches, in AsciiDoc, and is not built by docs-builder. Update those repos directly when relevant, but only for a clear product behavior change or critical fix.

## Repository layout

| Path | What it documents |
|---|---|
| `get-started/` | Onboarding and first-run content across products. Fundamental knowledge about Elastic |
| `solutions/` | Docs for solutions and serverless project types packaged on top of Elasticsearch and Kibana: Search, Observability, Security, Vector DB |
| `explore-analyze/` | Home for core Kibana features such as Discover, dashboards, visualizations, alerting, AI features, ML |
| `deploy-manage/` | Deploying, scaling, securing, and operating orchestrators, clusters, deployments, and projects |
| `manage-data/` | Ingesting, transforming, and lifecycle-managing data |
| `reference/` | Reference material such as settings, APIs, CLIs, and config that isn't naturally sitting in other code repos |
| `troubleshoot/` | Troubleshooting and diagnostics |
| `release-notes/` | Release notes and changelogs for Elastic products. Generally generated from code changes. |
| `cloud-account/` | Elastic Cloud account and billing |
| `extend/` | Extending and integrating with Elastic, for external developers |
| `contribute-docs/` | The public contribution guide: style, content types, cumulative docs, syntax |
| `serverless/`, `archive.md` | Serverless landing content and archived material. This content should not be updated. It's legacy and no longer published. |

Key files:

| File | Purpose |
|---|---|
| `docset.yml` | Site config: navigation, products, substitutions |
| `redirects.yml` | Redirect map for moved, renamed, or deleted pages. Update it when you move or delete a page. |
| `frontmatter.config.yml` | Frontmatter schema and defaults |
| `versions.md` | Version and lifecycle reference |

Reusable prose lives in `_snippets/` folders and is pulled in with an `include` directive. Check for an existing snippet before duplicating content across pages.

## Contribute

New to contributing? Start with the [contribution guide](https://www.elastic.co/docs/contribute-docs), which covers our style, content types, and how to [build and preview locally with docs-builder](https://www.elastic.co/docs/contribute-docs/locally).

If you find any bugs in our documentation, or want to request an enhancement, [open an issue](https://github.com/elastic/docs-content/issues). We also welcome contributions in the form of PRs. Before you submit a PR, make sure that you have signed our [Contributor License Agreement](https://www.elastic.co/contributor-agreement/).

We write our docs in Markdown. Refer to our [syntax quick reference](https://elastic.co/docs/contribute-docs/syntax-quick-reference) for examples and additional functionality. If you contribute with the help of AI agents or tools, see [`AGENTS.md`](AGENTS.md) and [`AI.md`](AI.md).

### Preview your changes

When you open a PR, your changes are built, deployed, and ready to be previewed within minutes.

## License

[![CC BY-NC-ND 4.0][cc-by-nc-nd-image]][cc-by-nc-nd] [![CC BY-NC-ND 4.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License][cc-by-nc-nd].

[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-nc-nd-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-nc-nd-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg
