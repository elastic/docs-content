---
navigation_title: "Content types"
description: "Overview of guidelines for choosing the appropriate content types in the Elastic documentation."
---

# Elastic Docs content types

Content types are proven structures for common kinds of documentation pages. They help readers find information and complete tasks efficiently. They help contributors and reviewers work more effectively, with less guesswork, faster reviews, and a shared vocabulary for feedback.

Each content type gives you a template, a checklist, and a set of best practices so you can focus on *what* you're writing rather than *how* to structure it. Pick the type that matches what you're writing, follow the guide, and you'll produce a page that's consistent, scannable, and easy to maintain.

## When to use

Each content type guide includes structure rules, best practices, and a checklist. You can use them at any point in your workflow: when drafting, reviewing, or assessing the quality of existing pages. The following sections describe different ways to put them to work.

Use them whenever you're:

- **Drafting a new page**: Identify the content type, then use the matching guidelines and template as your starting point.
- **Reviewing a PR**: Pull up the relevant content type guide and check the page against its checklist and best practices.
- **Updating an existing page**: Use the guidelines to check the page's structure and identify issues before you begin, to ensure your changes make sense.
- **Auditing a content set**: Use the guidelines to assess consistency and coverage across multiple pages. This works best [with an LLM](#with-an-llm-or-ai-agent), which can process many pages at once.

:::{tip}
You don't always need to restructure a page from scratch to match a template: the checklists and best practices are useful as a quick health check on work in progress, or to help fix the biggest problems with a specific page.
:::

## How to use

You can work through the guides by hand for a quick health check, or feed them to an LLM for a different kind of leverage. Either way, the guides are designed to be useful in whatever workflow you already have.

### Manually

You don't need any tooling to get value from the guides. Here are some ways to use them by hand:

- **Learn the basics:** Read through the guides to build a mental model of how each content type works and when to use it.
- **Study real examples:** Each guide links to existing pages that demonstrate the content type well.
- **Draft a new page:** Use the template as your starting structure, then fill in the details following the guidelines.
- **Simplify reviews:** Use the checklist as a quick pass/fail scan when reviewing a PR.
- **Diagnose a hard-to-read page:** Check which content types are present, whether they're cleanly separated, and where the structure breaks down.
- **Back up your feedback:** Reference specific guidelines in PR comments to explain your suggestions.

### With an LLM or AI agent

The guides are particularly powerful when combined with LLMs by putting them into your LLM or AI agent's context. Here are some ways to put them to work:

- **Scaffold a draft faster:** Instead of manually working through the template, paste the relevant guide and your rough notes into a chat and let the LLM produce a structured first draft you can refine.
- **Review against multiple content types at once:** An LLM can check a page against several guides simultaneously, flagging mixed content types and scoring against checklists. Especially useful when you're reviewing outside your area of expertise.
- **Audit across many pages:** This is where LLMs really shine. Feed the guides alongside a set of pages and ask for a consistency and coverage report. Something that would take hours to do manually.
- **Diagnose structural problems:** Give the LLM all the guides plus a page that feels "off" and ask it to pinpoint where the structure breaks down. It can often spot issues (like interleaved content types) that are hard to see when you're close to the content.
- **Make the guides always available:** Add them to your LLM's system prompt, a custom project, or an AI-assisted PR review workflow so they're applied automatically without extra effort.

## Mixing different content types

Some documentation pages combine multiple content types.

Mixing different types is fine as long as each section is clearly delineated and serves a distinct purpose. For example, a page about configuring authentication might include:

1. A brief overview of authentication concepts (explanation)
2. Step-by-step instructions to set up authentication (how-to)
3. A reference table of authentication settings (reference)

This works because each section is clearly separated and serves a distinct purpose. You shouldn't embed the settings table in the middle of the instructions, or interrupt the steps with conceptual explanations. This would break the flow and make it hard to scan the page for specific information.

When mixing content types, ensure that the overall structure and flow remain clear and logical for users. Use headings and sections to delineate different content types as needed.

:::{note}
The exception to this rule is the tutorial content type. A tutorial should always be a standalone page.
:::

## Pick a content type

Each guide covers the structure, best practices, and checklist for a specific content type. Start with the one that matches what you're writing.

| Your writing goal | Start here |
|---|---|
| Introduce a feature or concept | [Overview](overviews.md) |
| Complete a single, focused task | [How-to](how-tos.md) |
| Build a longer-form, learning-focused guide | [Tutorial](tutorials.md) |
| Troubleshoot common issues | [Troubleshooting](troubleshooting.md) |
| Signal what changed in a release | [Changelog](changelogs.md) |

## Templates per content type

Each content type has a matching template you can copy as a starting point. These include the recommended structure and placeholder text to fill in.

Refer to [our templates](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/) for each content type to get started quickly.

:::{tip}
Need help choosing a content type or structuring a new page? Reach out to the docs team using the `@elastic/docs` handle in GitHub or post in the [community docs channel](https://elasticstack.slack.com/archives/C09EUND5612). (Elasticians can also use the internal [#docs](https://elastic.slack.com/archives/C0JF80CJZ) Slack channel.)
:::
