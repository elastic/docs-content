---
navigation_title: "Content types"
description: "Overview of guidelines for choosing the appropriate content types in the Elastic documentation."
---

# Elastic Docs content types

When pages use the right content type(s), it's easier for users to find the information they need and efficiently complete tasks. Consistent structure across pages of a given type also makes the docs easier to write, review, and maintain over time.

For contributors, content types provide a repeatable, proven formula for structuring docs pages. Instead of figuring out from scratch how to organize each page, you can lean on established structures, checklists, and best practices that handle the predictable parts for you. This means less guesswork when drafting, faster and more objective reviews, and a shared vocabulary for giving and receiving feedback.

Before you start drafting a new docs page, identify the appropriate content type for your page.
Use these guidelines as a framework, not a rulebook. You should adapt structure and syntax where necessary to best serve users, but you should rarely need to deviate from the best practices.

:::{tip}
Need help choosing a content type or structuring a new page? Reach out to the docs team using the `@elastic/docs` handle in GitHub or post in the [community docs channel](https://elasticstack.slack.com/archives/C09EUND5612). (Elasticians can also use the internal [#docs](https://elastic.slack.com/archives/C0JF80CJZ) Slack channel.)
:::

## When to use

Each content type guide includes structure rules, best practices, and a checklist. You can use them at any point in your workflow: when drafting, reviewing, or assessing the quality of existing pages. The following sections describe different ways to put them to work.

Once you get into the habit of using these guidelines, they become a natural tool to reach for when working on documentation. You shouldn't need to context-switch or change your workflow to get value from them.

Use them whenever you're:

- **Drafting a new page**: Identify the content type, then use the matching guidelines and template as your starting point.
- **Reviewing a PR**: Pull up the relevant content type guide and check the page against its checklist and best practices.
- **Updating an existing page**: Use the guidelines to check the page's structure and identify issues before you being, to ensure your changes make sense.
- **Auditing a content set**: Use the guidelines to assess consistency and coverage across multiple pages. This works best [with an LLM](#with-an-llm-or-ai-agent), which can process many pages at once.

:::{tip}
You don't always need to restructure a page from scratch to match a template: the checklists and best practices are useful as a quick health check on work in progress, or to help fix the biggest problems with a specific page.
:::

## How to use

You can work through the guides by hand for a quick health check, or feed them to an LLM alongside your content for a more thorough, automated comparison. Either way, the guides are designed to be useful in whatever workflow you already have.

### Manually

You don't need any tooling to get value from the guides. Here are some ways to use them by hand:

- **Learn the basics:** Read through the guides to build a mental model of how each content type works and when to use it.
- **Study real examples:** Each guide links to existing pages that demonstrate the content type well.
- **Draft a new page:** Use the relevant guide and template as your starting structure, then fill in the details.
- **Review a page:** Use the checklist as a quick pass/fail scan when reviewing a PR.
- **Diagnose a hard-to-read page:** Check which content types are present, whether they're cleanly separated, and where the structure breaks down.
- **Back up your feedback:** Reference specific guidelines in PR comments to explain your suggestions.

### With an LLM or AI agent

The guides are particularly powerful when combined with GenAI models by putting them into your LLM or AI agent's context. Here are some ways to put them to work:

- **Draft a new page:** Paste the relevant guide and template into a chat and ask the LLM to help you scaffold or flesh out your draft or notes.
- **Review a page:** Feed one or more guides along with the page and ask the LLM to identify what content types are present, whether each section is internally consistent, and how well they score against the checklists.
- **Diagnose a hard-to-read page:** Give the LLM all the guides plus the page and ask it to determine what types are mixed in, whether they're cleanly separated, and where the structure breaks down.
- **Establish persistent instructions:** Add the guides to your LLM's context window or system prompt so they're always available when you're working on docs.
- **Build it into your tooling:** Attach the guides to an AI-assisted PR review workflow, or include them in a custom agent, GPT, or project that you use for docs work.

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

## Guidelines per content type

- [Changelogs](changelogs.md)
- [How-to guides](how-tos.md)
- [Overviews](overviews.md)
- [Troubleshooting](troubleshooting.md)
- [Tutorials](tutorials.md)

## Templates per content type

Refer to [our templates](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/) for each content type to get started quickly.
