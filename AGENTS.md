# Agent guidance for elastic/docs-content

This is the shared baseline for AI agents working in this repository. Claude Code reads it through `CLAUDE.md`, a symlink to this file. Cursor, Codex, and Copilot read `AGENTS.md` directly. Personal preferences belong in the gitignored `CLAUDE.local.md` or `AGENTS.local.md`, which load in addition to this file.

Keep this file lean: it points to the [`contribute-docs/`](contribute-docs/index.md) guide rather than restating it. Two resources back it up. When the **Elastic docs skills** are installed, reach for the relevant skill first, since it's the fast path. When a skill doesn't fit or you're unsure, the contribution guide has the deeper context, and unlike the skills it's always present in this repo. If this file and the contribution guide ever disagree, the guide wins, so fix this file.

## What this repo is

The source for the narrative documentation published at <https://www.elastic.co/docs/>: concepts, guides, and troubleshooting for users of all Elastic products. It covers current versions and deployments: Elastic Stack v9 and Serverless, Elastic Cloud Enterprise v4, Elastic Cloud on Kubernetes v3 and later, Elastic Cloud Hosted, and a range of Elastic tools.

Pages are [MyST Markdown](https://elastic.github.io/docs-builder/syntax/) with Elastic extensions, built by [docs-builder](https://elastic.github.io/docs-builder/). After a merge to `main`, the published site refreshes within minutes, followed by a cache refresh.

## What belongs here, and what doesn't

This repo hosts the cross-product, narrative user documentation for the products and versions already described. Some content lives elsewhere:

- **Reference docs that sit next to the code they describe.** Reference content generated from or maintained alongside a codebase stays in that code repo. API references are the clearest case: they're generated from OpenAPI specs, most often in `elastic/kibana` or `elastic/elasticsearch-specification`, not authored as Markdown here. The same holds for other in-repo reference material that ships with the product.
- **Legacy-version content.** Documentation for versions earlier than the ones this repo covers, essentially Elastic v8 and before, lives in the respective code repositories, on older branches, in AsciiDoc, and is not built by docs-builder. Update those repos directly when relevant, but only for a clear product behavior change or critical fix.

## Core principles

- **Verify before you draft.** For anything the product actually does, such as UI labels, defaults, and behavior, the source of truth is the product's code repo at `HEAD`, not the issue or PR description. Never publish something the model inferred without checking source. Because these are cumulative docs, also confirm a statement holds for earlier relevant product minor versions when there is any doubt: A page must stay true for users on any version that this repo documents.
- **Find the canonical home for content.** Search for a page that already covers the topic before adding a new one.
- **Place content where it belongs, once.** Put each detail in its single most correct page, not everywhere the feature is mentioned. When a feature appears in several places, keep them consistent and update all of them. Reuse shared content with a snippet, though a single duplication across a couple of pages beats maintaining an include. See [content types](contribute-docs/content-types/index.md).
- **Cumulative docs.** These docs serve every supported version at once. Preserve existing content and scope new content with `applies_to` rather than overwriting. See the [cumulative-docs guide](contribute-docs/how-to/cumulative-docs/index.md).
- **Don't assume existing content already follows every rule.** Consistency with surrounding pages is a good default, but the existing docs are not guaranteed correct. When content obviously diverges from the documented best practices, prefer fixing or improving it over matching the divergence.
- **Write for the reader, not the PR.** Translate developer jargon into user language. One precise sentence beats three vague ones.

## Repo layout

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
| `contribute-docs/` | The public contribution guide: style, content types, cumulative docs, syntax. The canonical source this file points to. |
| `serverless/`, `archive.md` | Serverless landing content and archived material. This content should not be updated. It's legacy and no longer published. |

Key files:

| File | Purpose |
|---|---|
| `docset.yml` | Site config: navigation, products, substitutions |
| `redirects.yml` | Redirect map for moved, renamed, or deleted pages. Update it when you move or delete a page. |
| `frontmatter.config.yml` | Frontmatter schema and defaults |
| `versions.md` | Version and lifecycle reference |

Reusable prose lives in `_snippets/` folders and is pulled in with an `include` directive. Check for an existing snippet before duplicating content across pages.

## Writing and style

The style guide is the source of truth: [voice and tone](contribute-docs/style-guide/voice-tone.md), [word choice](contribute-docs/style-guide/word-choice.md), [formatting](contribute-docs/style-guide/formatting.md), [UI writing](contribute-docs/style-guide/ui-writing.md), [grammar and spelling](contribute-docs/style-guide/grammar-spelling.md), and [accessibility](contribute-docs/style-guide/accessibility.md). Much of it is enforced by [Vale](contribute-docs/vale-linter.md).

High-signal conventions:

- Second person, present tense, active voice. Sentence case for headings.
- Bold UI labels and controls, such as **Save**, **Add panel**, and **Settings**.
- Separate navigation steps with ` → `, as in **Add** → **Controls** → **Variable control**.
- Use MyST directives per the [syntax quick reference](contribute-docs/syntax-quick-reference.md). Keep content in prose where it reads naturally, and don't stack admonitions.
- Write links with the [docs-builder link syntax](https://elastic.github.io/docs-builder/syntax/links/), including the cross-repo `<repo>://` form. Validate them with the `crosslink-validator` skill.

## Before you open a PR

Opening a PR builds a preview automatically. The link appears on the PR and updates within minutes. Before requesting review, check your changes for:

- **Content type compliance**: the right structure and depth for the page's type.
- **applies_to and cumulative-docs compliance**: correct scoping for versions and deployments.
- **Style compliance**: apply the [Vale](contribute-docs/vale-linter.md) recommendations where relevant.
- **Accuracy against the product code**: labels, defaults, and behavior verified at `HEAD`.

Preview locally with `docs-builder serve`, or run `docs-builder` with no argument for a full build that surfaces errors ([build locally](contribute-docs/locally.md)). Run Vale on changed files. When you move, rename, or delete a page that has already been published, add the redirect in `redirects.yml`. For AI-assisted contributions specifically, read [`AI.md`](AI.md).

## Tooling

The **Elastic docs skills** (from <https://github.com/elastic/elastic-docs-skills>) cover the common tasks. Install them, then reach for the one that fits. When a skill doesn't cover your case, fall back to the contribution guide, as described at the top of this file.

| Task | Skill |
|---|---|
| Issue to drafted PR, end to end | `accept-docs-quest` |
| `applies_to` tagging and cumulative docs | `docs-applies-to-tagging` |
| Content type structure and depth | `docs-content-type-checker` |
| Style, voice, and grammar | `docs-check-style` |
| MyST and directive syntax | `docs-syntax-help` |
| Internal jargon | `docs-flag-jargon-skill` |
| Frontmatter completeness and descriptions | `docs-frontmatter-audit`, `docs-frontmatter-description` |
| Page opening (H1, intro, requirements) | `docs-page-opening-optimizer` |
| Code sample validation | `docs-validate-code-samples` |
| Cross-link validation | `crosslink-validator` |
| Redirects | `docs-redirects` |

The **elastic-docs MCP**, when available, searches the published corpus, finds related pages, and checks coherence.

## What not to do

The core principles cover most of this. Beyond them:

- Don't update release notes manually as part of a regular docs change. They're produced from code changes, not hand-edited here.
- Don't add or replace screenshots on a hunch. Flag the screenshots that need updating and let a human capture them.
- Don't restructure or rename pages beyond the task, unless the change is required for the new content to make sense.
