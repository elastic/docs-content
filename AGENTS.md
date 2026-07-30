# Agent guidance for elastic/docs-content

This is the shared baseline for AI agents working in this repository. Claude Code reads it through `CLAUDE.md`, a symlink to this file. Cursor, Codex, and Copilot read `AGENTS.md` directly. Personal preferences belong in the gitignored `CLAUDE.local.md` or `AGENTS.local.md`, which load in addition to this file.

Keep this file lean. It points to the contribution guide in [`contribute-docs/`](contribute-docs/index.md) rather than restating it. If the two disagree, the contribution guide wins, so fix this file.

## What this repo is

The source for the narrative documentation published at <https://www.elastic.co/docs/>: concepts, guides, and troubleshooting for users of all Elastic products. It covers current versions and deployments: Elastic Stack v9 and Serverless, Elastic Cloud Enterprise v4, Elastic Cloud on Kubernetes v3 and later, Elastic Cloud Hosted, and a range of Elastic tools.

Pages are [MyST Markdown](https://elastic.github.io/docs-builder/syntax/) with Elastic extensions, built by [docs-builder](https://elastic.github.io/docs-builder/). After a merge to `main`, the published site refreshes within minutes, followed by a cache refresh.

## What belongs here, and what doesn't

This repo hosts the cross-product user documentation for the versions listed above. Two things live elsewhere:

- **API references.** These are generated from OpenAPI specs and hosted in specific repositories, most often `elastic/kibana` or `elastic/elasticsearch-specification`. They are not authored as Markdown here.
- **Legacy-version content.** Anything for versions earlier than those above, essentially Elastic v8 and earlier, lives in the respective code repositories, on older branches, in AsciiDoc, and is not built by docs-builder. Update it when a change is relevant to those versions, but not in this repo. Opening pull requests against those targets is encouraged, though the general rule is to do so only for a clear product behavior change or a critical fix.

## Finding a page from its URL

To locate the source file behind a published page, strip `https://www.elastic.co/docs/` from the URL and append `.md`:

```
https://www.elastic.co/docs/explore-analyze/discover/document-explorer
→ explore-analyze/discover/document-explorer.md
```

This is a rule of thumb for finding files, not for writing links. Links in the docs follow their own rules, defined in [the docs-builder link syntax](https://elastic.github.io/docs-builder/syntax/links/).

## Core principles

- **Verify before you draft.** For anything the product actually does, such as UI labels, defaults, and behavior, the source of truth is the product's code repo at `HEAD`, not the issue or PR description. Never publish something the model inferred without checking source. Because these are cumulative docs, also confirm a statement holds for earlier v9 minors when there is any doubt. A page must stay true for users on any supported v9 minor.
- **Find the canonical home before creating a page.** Search existing pages first. A new page is the last resort, since most content extends a page that already exists.
- **Place content where it belongs, once.** Each content type and each page has a defined role and depth. See [content types](contribute-docs/content-types/index.md). Put information in its most correct place. Minor details belong where they are relevant, not repeated everywhere a feature is mentioned. A feature is often documented in several places for good reasons: when you change one, check the others so you do not introduce inconsistencies, and update every place that needs it. When the same content genuinely has to appear in more than one place, a [snippet](contribute-docs/syntax-quick-reference.md) is the clean way to reuse it, though a single duplication across a couple of pages is acceptable rather than maintaining an include.
- **Cumulative docs.** These docs serve every supported version at once. Preserve existing content and scope new content with `applies_to` rather than overwriting. See the [cumulative-docs guide](contribute-docs/how-to/cumulative-docs/index.md).
- **Don't assume existing content already follows every rule.** Consistency with surrounding pages is a good default, but the existing docs are not guaranteed correct. When content obviously diverges from the documented best practices, prefer fixing or improving it over matching the divergence.
- **Write for the reader, not the PR.** Translate developer jargon into user language. One precise sentence beats three vague ones.

## Repo layout

| Path | What it documents |
|---|---|
| `get-started/` | Onboarding and first-run content across products |
| `solutions/` | Solution docs for Search, Observability, and Security |
| `explore-analyze/` | Discover, dashboards, visualizations, alerting, AI features, ML |
| `deploy-manage/` | Deploying, scaling, securing, and operating clusters and projects |
| `manage-data/` | Ingesting, transforming, and lifecycle-managing data |
| `reference/` | Reference material such as settings, APIs, CLIs, and config |
| `troubleshoot/` | Troubleshooting and diagnostics |
| `release-notes/` | Release notes and changelogs for Elastic Stack and Serverless |
| `cloud-account/` | Elastic Cloud account and billing |
| `extend/` | Extending and integrating with Elastic |
| `contribute-docs/` | The public contribution guide: style, content types, cumulative docs, syntax. The canonical source this file points to. |
| `serverless/`, `archive.md` | Serverless landing content and archived material |

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

## Before you open a PR

Opening a PR builds a preview automatically. The link appears on the PR and updates within minutes. Before requesting review, check your changes for:

- **Content type compliance**: the right structure and depth for the page's type.
- **applies_to and cumulative-docs compliance**: correct scoping for versions and deployments.
- **Style compliance**: apply the [Vale](contribute-docs/vale-linter.md) recommendations where relevant.
- **Accuracy against the product code**: labels, defaults, and behavior verified at `HEAD`.

Preview locally with docs-builder ([build locally](contribute-docs/locally.md)) and run Vale on changed files. When you move, rename, or delete a page, add the redirect in `redirects.yml`. For AI-assisted contributions specifically, read [`AI.md`](AI.md).

## Tooling

Some agents have Elastic docs tooling available. If yours does, use it:

- The **Elastic docs skills** (<https://github.com/elastic/elastic-docs-skills>) for authoring and validation workflows, such as content-type checks, `applies_to` tagging, style checks, and crosslink validation.
- The **elastic-docs MCP** for searching the published corpus, finding related pages, and checking coherence.

## What not to do

- Don't invent UI labels, defaults, or behavior. Verify against the product's code repo at `HEAD`.
- Don't create a new page before searching for a page that can absorb the content.
- Don't duplicate prose across pages when a `_snippets/` include is the better fit.
- Don't delete content for a still-supported version. Scope it with `applies_to` instead.
- Don't add or replace screenshots on a hunch. Flag the screenshots that need updating and let a human capture them.
- Don't restructure or rename pages beyond the task, unless the change is required for the new content to make sense.
