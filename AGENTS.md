# Agent guidance — elastic/docs-content

This file is the shared baseline for any AI agent working in this repository. It applies across all subdirectories.

- **Claude Code** reads it through `CLAUDE.md`, which is a symlink to this file.
- **Cursor**, **Codex**, and **Copilot** read `AGENTS.md` directly.
- **Personal preferences** go in `CLAUDE.local.md` (Claude Code) or `AGENTS.local.md` (other tools). Both are gitignored and load in addition to this file. Keep individual workflow, aliases, and experiments there, not here.

Keep this file lean. It routes to the canonical contribution guide in [`contribute-docs/`](contribute-docs/index.md) (published at <https://www.elastic.co/docs/contribute-docs>); it does not restate it. When guidance and the published contribution guide disagree, the contribution guide wins — fix this file.

---

## What this repo is

The user-facing source for <https://www.elastic.co/docs/>. Pages are [MyST Markdown](https://elastic.github.io/docs-builder/syntax/) with Elastic extensions, built by [docs-builder](https://elastic.github.io/docs-builder/). The published site refreshes within hours of a merge to `main`.

URL paths map directly to file paths. Strip `https://www.elastic.co/docs/` and append `.md`:

```
https://www.elastic.co/docs/explore-analyze/discover/document-explorer
→ explore-analyze/discover/document-explorer.md
```

## What belongs here — and what doesn't

This repo hosts the **core, cross-product user documentation** for Elastic products (current versions, both Elastic Stack and Serverless).

It is **not** the home for:

- **In-repo developer and reference docs** that live in each code repo's own `docs/` folder (`elastic/kibana`, `elasticsearch`, `beats`, `logstash`, and others). Those stay in the code repo and may be referenced from here.
- **API reference**, which is generated from OpenAPI specs, not authored as Markdown here.
- **Legacy-version content** still served from older documentation repos.

When a topic clearly belongs to a code repo's own docs, say so rather than adding it here.

## Core principles

- **Verify before you draft.** For anything the product actually does — UI labels, defaults, behavior — the source of truth is the product's code repo at `HEAD`, not the issue or PR description. Never publish a label, default, or behavior the model inferred without checking source.
- **Find the canonical home before creating a page.** Search existing pages first. A new page is the last resort; most content extends a page that already exists.
- **Cumulative docs.** These docs serve every supported version at once. Preserve existing content and scope new content with `applies_to` rather than overwriting. See [the cumulative-docs guide](contribute-docs/how-to/cumulative-docs/index.md).
- **Write to a content type.** Every page is an overview, how-to, tutorial, troubleshooting, reference, or changelog page — and follows that type's structure. See [content types](contribute-docs/content-types/index.md).
- **Write for the reader, not the PR.** Translate developer jargon into user language. One precise sentence beats three vague ones.

## Repo layout

| Path | What it documents |
|---|---|
| `get-started/` | Onboarding and first-run content across products |
| `solutions/` | Solution docs — Search, Observability, Security |
| `explore-analyze/` | Discover, dashboards, visualizations, alerting, AI features, ML |
| `deploy-manage/` | Deploying, scaling, securing, and operating clusters and projects |
| `manage-data/` | Ingesting, transforming, and lifecycle-managing data |
| `reference/` | Reference material — settings, APIs, CLIs, config |
| `troubleshoot/` | Troubleshooting and diagnostics |
| `release-notes/` | Release notes and changelogs for Elastic Stack and Serverless |
| `cloud-account/` | Elastic Cloud account and billing |
| `extend/` | Extending and integrating with Elastic |
| `contribute-docs/` | The public contribution guide — style, content types, cumulative docs, syntax. **The canonical source this file points to.** |
| `serverless/`, `archive.md` | Serverless landing content and archived material |

Key files:

| File | Purpose |
|---|---|
| `docset.yml` | Site config — navigation, products, substitutions |
| `redirects.yml` | Redirect map for moved, renamed, or deleted pages. Update it when you move or delete a page. |
| `frontmatter.config.yml` | Frontmatter schema and defaults |
| `versions.md` | Version and lifecycle reference |

Reusable prose lives in `_snippets/` folders and is pulled in with `:::{include}`. Check for an existing snippet before duplicating content across pages.

## Writing and style

The style guide is the source of truth: [voice and tone](contribute-docs/style-guide/voice-tone.md), [word choice](contribute-docs/style-guide/word-choice.md), [formatting](contribute-docs/style-guide/formatting.md), [UI writing](contribute-docs/style-guide/ui-writing.md), [grammar and spelling](contribute-docs/style-guide/grammar-spelling.md), and [accessibility](contribute-docs/style-guide/accessibility.md). Much of it is enforced by [Vale](contribute-docs/vale-linter.md) — run it before opening a PR.

High-signal conventions:

- Second person, present tense, active voice. Sentence case for headings.
- Bold UI labels and controls: **Save**, **Add panel**, **Settings**.
- Separate navigation steps with ` → `: **Add** → **Controls** → **Variable control**.
- Use MyST directives (admonitions, tabs, includes) per the [syntax quick reference](contribute-docs/syntax-quick-reference.md). Don't reach for an admonition when the content can flow in prose, and don't stack admonitions.

## Build, preview, and validate

- **PR preview.** Opening a PR builds and deploys a preview automatically; the link appears on the PR.
- **Local preview.** Use docs-builder — see [build locally](contribute-docs/locally.md).
- **Style.** Run [Vale](contribute-docs/vale-linter.md) on changed files.
- **CI sweeps.** Automated checks in `.github/workflows/` review style, `applies_to`, frontmatter, coherence, page openings, and links. Expect them to run on your PR.

## Working in this repo

- Follow the pull request template and sign the [CLA](https://www.elastic.co/contributor-agreement/) before your first PR.
- When you move, rename, or delete a page, add the redirect in `redirects.yml`.
- Scope version- or deployment-specific content with `applies_to` — see the [cumulative-docs guide](contribute-docs/how-to/cumulative-docs/index.md) and the [`applies_to` syntax](https://elastic.github.io/docs-builder/syntax/applies/).
- For AI-assisted contributions specifically, read [`AI.md`](AI.md).

## What not to do

- Don't invent UI labels, defaults, or behavior. Verify against the product's code repo at `HEAD`.
- Don't create a new page before searching for a page that can absorb the content.
- Don't duplicate prose across pages — use a `_snippets/` include.
- Don't delete content for a still-supported version. Scope it with `applies_to` instead.
- Don't add or replace screenshots on a hunch. Flag the screenshots that need updating and let a human capture them.
- Don't restructure or rename pages beyond the task unless the change is required for the new content to make sense.
