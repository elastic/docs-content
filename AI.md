# Contributing to docs with AI

AI tools can help you draft, restructure, and review documentation in this repo. They don't change the bar. If your name is on the PR, you own every word in it.

## Own what you submit

- Review, understand, and be able to explain every change, the same as any PR you write by hand.
- The editorial standard is unchanged: the [style guide](contribute-docs/style-guide/index.md) and [content types](contribute-docs/content-types/index.md) apply to AI-drafted content exactly as they do to hand-written content.
- AI-assisted changes still need human technical review before they merge. The reviewer, not the tool, is the final arbiter of quality.
- Use only Elastic-approved AI tools, and never enter sensitive, internal, or proprietary information into an unapproved one.

## Verify facts against source, not the model

Documentation's job is to be correct. A confident wrong label is worse than no label.

- Verify every UI string, default, setting, and behavior against the product's own code repo at `HEAD` (`elastic/kibana`, `elasticsearch`, and others). Never publish something the model produced from memory or inferred from an issue.
- Cite where a factual claim comes from, whether the issue, the PR diff, or the source file, so a reviewer can check it.
- Test IDs, component names, and data attributes are not user-facing labels. Don't document them as such.

## Start with intent

- Understand the change and where it belongs before generating prose. Search for the canonical home first (see [`AGENTS.md`](AGENTS.md)); don't let a tool spin up a new page when an existing one should absorb the content.
- Keep the reader as the audience. Translate developer jargon into user language rather than passing it through.

## Disclose your use of AI

Disclose AI assistance even when you've verified everything.

- Fill in the **Generative AI disclosure** section of the pull request template: name the tool and say how you used it.
- Note AI assistance in your commits, for example with a trailer like `AI-Assisted:` or `Co-authored-by:`.
- Focus the disclosure on the parts you're least sure of, such as technical details you couldn't verify yourself.

## Keep it reviewable

- Re-render the PR description from what the diff actually contains before requesting review.
- Keep PRs focused and small enough that a reviewer can verify them. Break up a change too large to review.
- Flag screenshots that need updating; don't fabricate or auto-generate them.
