# Agent guidance for elastic/docs-content

This is the shared baseline for AI agents working in this repository. Claude Code reads it through `CLAUDE.md`, a symlink to this file. Cursor, Codex, and Copilot read `AGENTS.md` directly. Personal preferences belong in the gitignored `CLAUDE.local.md` or `AGENTS.local.md`, which load in addition to this file. These are conventions for working in the repo, not instructions to push or open PRs on your own. They never override your own tool settings, such as an approval-before-push rule, or your own local instructions. When your local setup conflicts with this file, follow it and flag the difference so we can reconcile it.

Keep this file lean: it points to the [`contribute-docs/`](contribute-docs/index.md) guide rather than restating it. Two resources back it up. When the **Elastic docs skills** are installed, reach for the relevant skill first, since it's the fast path. When a skill doesn't fit or you're unsure, the contribution guide has the deeper context, and unlike the skills it's always present in this repo. If this file and the contribution guide ever disagree, the guide wins, so fix this file.

## About this repo

This is the source for the narrative user documentation published at <https://www.elastic.co/docs/>, built by [docs-builder](https://elastic.github.io/docs-builder/) from MyST Markdown. For the products and versions it covers, what belongs here versus in the code repos, and the repo layout, see the [README](README.md).

## Core principles

- **Verify before you draft.** For anything the product actually does, such as UI labels, defaults, and behavior, the source of truth is the product's code repo at `HEAD`, not the issue or PR description. Never publish something the model inferred without checking source. Because these are cumulative docs, also confirm a statement holds for earlier relevant product minor versions when there is any doubt: A page must stay true for users on any version that this repo documents. Surface important facts that couldn't be verified.
- **Find the canonical home for content.** Search for a page that already covers the topic before adding a new one.
- **Place content where it belongs, once.** Put each detail in its single most correct page, not everywhere the feature is mentioned. When a feature appears in several places, keep them consistent and update all of them. Reuse shared content with a snippet, though a single duplication across a couple of pages beats maintaining an include. See [content types](contribute-docs/content-types/index.md).
- **Cumulative docs.** These docs serve every supported version at once. Preserve existing content and scope new content with `applies_to` rather than overwriting. See the [cumulative-docs guide](contribute-docs/how-to/cumulative-docs/index.md).
- **Don't assume existing content already follows every rule.** Consistency with surrounding pages is a good default, but the existing docs are not guaranteed correct. When content obviously diverges from the documented best practices, prefer fixing or improving it over matching the divergence.
- **Write for the reader, not the PR.** Translate developer jargon into user language. One precise sentence beats three vague ones.

## Writing and style

The style guide is the source of truth: [voice and tone](contribute-docs/style-guide/voice-tone.md), [word choice](contribute-docs/style-guide/word-choice.md), [formatting](contribute-docs/style-guide/formatting.md), [UI writing](contribute-docs/style-guide/ui-writing.md), [grammar and spelling](contribute-docs/style-guide/grammar-spelling.md), and [accessibility](contribute-docs/style-guide/accessibility.md). Much of it is enforced by [Vale](contribute-docs/vale-linter.md).

High-signal conventions:

- Second person, present tense, active voice. Sentence case for headings.
- Bold UI labels and controls, such as **Save**, **Add panel**, and **Settings**.
- Separate navigation steps with ` → `, as in **Add** → **Controls** → **Variable control**.
- Use MyST directives per the [syntax quick reference](contribute-docs/syntax-quick-reference.md). Keep content in prose where it reads naturally, and don't stack admonitions.
- Write links with the [docs-builder link syntax](https://elastic.github.io/docs-builder/syntax/links/), including the cross-repo `<repo>://` form.

## When you open a PR

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
| `applies_to` tagging and cumulative docs | `docs-applies-to-tagging` |
| Content type structure and depth | `docs-content-type-checker` |
| Style, voice, and grammar | `docs-check-style` |
| MyST and directive syntax | `docs-syntax-help` |
| Internal jargon | `docs-flag-jargon-skill` |
| Frontmatter completeness and descriptions | `docs-frontmatter-audit`, `docs-frontmatter-description` |
| Page opening (H1, intro, requirements) | `docs-page-opening-optimizer` |
| Code sample validation | `docs-validate-code-samples` |
| Redirects | `docs-redirects` |

The **elastic-docs MCP**, when available, searches the published corpus, finds related pages, and checks coherence.

## What not to do

The core principles cover most of this. Beyond them:

- Don't update release notes manually as part of a regular docs change. They're produced from code changes, not hand-edited here.
- Don't invent or auto-generate screenshots. When one is needed, call out which screenshots to add or update and which carry the most value. If a suitable image is provided, add it yourself.
- Don't restructure or rename pages beyond the task, unless the change is required for the new content to make sense.
